"""Synthetic R4 campaign addon to R5 reviewed-Grand resource-only patch tests."""
import copy
import importlib.util
import io
import json
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
preview_tool=module('r5preview','tools/preview_r5_grand_from_r4.py')
patch_tool=module('r5patch','tools/patch_r5_grand_from_r4.py')
def encoded(x):return (json.dumps(x,indent=2)+'\n').encode()

def jar(policy,*,signed=False,bad_version=False):
    f=io.BytesIO()
    with zipfile.ZipFile(f,'w') as z:
        z.writestr('META-INF/neoforge.mods.toml','[[mods]]\nmodId="ao_campaign"\nversion="'+('0.3.1' if bad_version else '0.3.2-experimental')+'"\n')
        z.writestr('dev/ambientodyssey/campaign/GrandTreasure.class',b'\xca\xfe\xba\xbeGrand')
        z.writestr('dev/ambientodyssey/campaign/BossRewards.class',b'\xca\xfe\xba\xbeRewards')
        z.writestr('data/neoforge/loot_modifiers/global_loot_modifiers.json',b'{"replace":false}')
        z.writestr('ao_loot_policy.json',encoded(policy))
        if signed:z.writestr('META-INF/TEST.SF',b'sig')
    return f.getvalue()

class R5GrandAddonResourcePatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=json.loads(preview_tool.BASE.read_text())
        cls.proposal=json.loads(preview_tool.PROPOSALS.read_text())
        cls.new,cls.changed=preview_tool.transform(cls.base,cls.proposal)

    def setUp(self):
        self.preview={"status":"REVIEW_ONLY_NOT_A_COMPILED_RELEASE",
                      "changed_pools":copy.deepcopy(self.changed),
                      "policy":copy.deepcopy(self.new)}
        self.preview_bytes=encoded(self.preview)
        self.review=patch_tool.draft(self.preview,self.preview_bytes)
        self.binary=jar(self.base)

    def accept_exp(self):
        review=copy.deepcopy(self.review)
        review['status']='APPROVED_FOR_EXPERIMENTAL_TEST_ONLY'
        for row in review['decisions']:
            row.update({
                "installed_native_source_verified":True,
                "effective_paxi_source_verified":True,
                "native_entry_functions_and_category_reviewed":True,
                "approved_for_experimental_test_only":True,
                "reviewer_rationale":"Reviewed the exact native JAR source and category-specific pool."
            })
        return review

    def test_draft_is_unapproved_and_all_five_separate(self):
        self.assertEqual(self.review['status'],'DRAFT_NOT_APPROVED')
        self.assertEqual(len(self.review['decisions']),5)
        self.assertTrue(all(not r['approved_for_experimental_test_only'] for r in self.review['decisions']))
        with self.assertRaisesRegex(ValueError,'Approval status missing'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,self.review)

    def test_safe_resource_only_patch_preserves_every_class(self):
        altered,receipt=patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,self.accept_exp())
        base=dict((i.filename,data) for i,data in patch_tool.jar_entries(self.binary))
        new=dict((i.filename,data) for i,data in patch_tool.jar_entries(altered))
        self.assertEqual(set(base),set(new))
        self.assertEqual({k for k in base if base[k]!=new[k]},{"ao_loot_policy.json"})
        self.assertEqual(receipt['other_members_byte_identical'],len(base)-1)
        self.assertEqual(len(receipt['changed_grand_pool_indices']),5)
        self.assertFalse(receipt['lootr_multiplayer_tested'])
        self.assertFalse(receipt['minecraft_runtime_tested'])

    def test_reject_if_native_paxi_unreviewed(self):
        review=self.accept_exp()
        review['decisions'][0]['effective_paxi_source_verified']=False
        with self.assertRaisesRegex(ValueError,'Unverified native source, Paxi'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,review)

    def test_reject_changed_reviewed_pool_index(self):
        review=self.accept_exp()
        review['decisions'][0]['proposed_pool_index']+=1
        with self.assertRaisesRegex(ValueError,'another source hash or native pool'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,review)

    def test_reject_approval_for_other_preview(self):
        review=self.accept_exp()
        review['preview_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'another or modified preview'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,review)

    def test_reject_policy_not_only_grand(self):
        review=self.accept_exp()
        self.preview['policy']['regalia'].append('unapproved:bonus')
        with self.assertRaisesRegex(ValueError,'Non-Grand'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,review)

    def test_reject_stale_old_jar_with_different_pool_index(self):
        previous=copy.deepcopy(self.base)
        previous['grand_treasure'][0]['pool_index']+=1
        with self.assertRaisesRegex(ValueError,'exactly five'):
            patch_tool.build_resource_patch(jar(previous),self.preview,self.preview_bytes,self.accept_exp())

    def test_reject_cross_table_source_patches(self):
        self.preview['policy']['grand_treasure'][0]['source_resource']='data/minecraft/loot_table/chests/ancient_city.json'
        with self.assertRaisesRegex(ValueError,'Illegal field drift'):
            patch_tool.build_resource_patch(self.binary,self.preview,self.preview_bytes,self.accept_exp())

    def test_reject_wrong_compiled_campaign_version(self):
        with self.assertRaisesRegex(ValueError,'original R4 campaign 0.3.2'):
            patch_tool.build_resource_patch(jar(self.base,bad_version=True),self.preview,self.preview_bytes,self.accept_exp())

    def test_reject_signed_jar(self):
        with self.assertRaisesRegex(ValueError,'signed JAR'):
            patch_tool.build_resource_patch(jar(self.base,signed=True),self.preview,self.preview_bytes,self.accept_exp())

    def test_release_pins_are_exact_r4(self):
        self.assertEqual(patch_tool.CAMPAIGN_SHA,'802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7')
        self.assertEqual(patch_tool.R4_SHA,'31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d')

if __name__=='__main__':unittest.main()
