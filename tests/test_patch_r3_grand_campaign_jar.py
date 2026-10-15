"""Synthetic byte-for-byte R2 campaign JAR resource patch tests.

No private release, official mod JAR, or Java compilation is used.
"""
import hashlib
import importlib.util
import io
import json
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('patch_r3',ROOT/'tools/patch_r3_grand_campaign_jar.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
def old_rows():
    return [
        {'structure':'dungeons_arise:keep_kayra','tier':6,
         'table':f'dungeons_arise:chests/keep_kayra/chest_{i}',
         'source_resource':'data/dungeons_arise/loot_table/chests/keep_kayra/garden_normal.json',
         'source_sha256':'a'*64,'pool_index':1,'chance':.05,
         'selection_score':2.5} for i in range(14)]
def new_rows():
    return [
        {'structure':r['structure'],'tier':r['tier'],'table':r['table'],
         'source_resource':f"data/dungeons_arise/loot_table/{r['table'].split(':')[1]}.json",
         'source_sha256':'b'*64,'pool_index':2,'chance':.05} for r in old_rows()]

def jar(original,add_signed=False):
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w') as z:
        z.writestr('META-INF/neoforge.mods.toml','[[mods]]\nmodId="ao_campaign"\nversion="0.3.0-experimental"\n')
        z.writestr('dev/ambientodyssey/campaign/GrandTreasure.class',b'\xCA\xFE\xBA\xBEGRAND')
        z.writestr('dev/ambientodyssey/campaign/BossRewards.class',b'\xCA\xFE\xBA\xBEBOSS')
        z.writestr('ao_loot_policy.json',enc(original))
        z.writestr('data/ao_campaign/loot_modifiers/grand_treasure.json',b'{"conditions":[]}')
        if add_signed:z.writestr('META-INF/CERT.SF','signed')
    return mem.getvalue()

class R3ResourceOnlyPatch(unittest.TestCase):
    def setUp(self):
        self.old={'bosses':{'test:boss':5},'regalia':['artifacts:some_item'],'unique_weapons':['simplyswords:unique'],
                  'native_gems':'UNCHANGED','grand_treasure':old_rows()}
        self.new={**self.old,'grand_treasure':new_rows()}
        self.j=jar(self.old);self.policy=enc(self.new)
        self.receipt={'status':'STAGED_EXPERIMENTAL_SOURCE_REVIEW_ONLY_NOT_COMPILED_NOT_RUNTIME_TESTED',
                      'staged_policy_sha256':hashlib.sha256(self.policy).hexdigest()}

    def test_changes_only_policy_resource_no_java_bytecode(self):
        out,proof=p.patch_jar(self.j,self.policy,self.receipt)
        a={i.filename:b for i,b in p.archive_members(self.j)}
        b={i.filename:v for i,v in p.archive_members(out)}
        self.assertEqual(set(a),set(b))
        self.assertEqual([k for k in a if a[k]!=b[k]],['ao_loot_policy.json'])
        self.assertEqual(proof['changed_grand_source_contexts'],14)
        self.assertTrue(proof['all_compiled_classes_byte_identical'])
        self.assertFalse(proof['minecraft_runtime_tested'])

    def test_reject_non_grand_reward_changes(self):
        wrong={**self.new,'regalia':['other:unapproved']}
        contents=enc(wrong);self.receipt['staged_policy_sha256']=p.sha(contents)
        with self.assertRaisesRegex(ValueError,'non-Grand'):
            p.patch_jar(self.j,contents,self.receipt)

    def test_reject_untested_policy_instead_of_staged_receipt(self):
        self.receipt['status']='DRAFT_NOT_APPROVED'
        with self.assertRaisesRegex(ValueError,'staging receipt'):
            p.patch_jar(self.j,self.policy,self.receipt)

    def test_reject_bad_policy_hash(self):
        self.receipt['staged_policy_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'Staged policy hash'):
            p.patch_jar(self.j,self.policy,self.receipt)

    def test_reject_changed_chest_contexts(self):
        bad={**self.new,'grand_treasure':new_rows()[:-1]}
        b=enc(bad);self.receipt['staged_policy_sha256']=p.sha(b)
        with self.assertRaisesRegex(ValueError,'context count'):
            p.patch_jar(self.j,b,self.receipt)

    def test_reject_changed_chance(self):
        badrows=new_rows();badrows[0]['chance']=0.5
        b=enc({**self.new,'grand_treasure':badrows})
        self.receipt['staged_policy_sha256']=p.sha(b)
        with self.assertRaisesRegex(ValueError,'tier/chance'):
            p.patch_jar(self.j,b,self.receipt)

    def test_reject_borrowed_source(self):
        badrows=new_rows();badrows[0]['source_resource']='data/dungeons_arise/loot_table/chests/keep_kayra/garden_normal.json'
        b=enc({**self.new,'grand_treasure':badrows})
        self.receipt['staged_policy_sha256']=p.sha(b)
        with self.assertRaisesRegex(ValueError,'cross-chest'):
            p.patch_jar(self.j,b,self.receipt)

    def test_reject_signed_jar(self):
        with self.assertRaisesRegex(ValueError,'Signed JAR'):
            p.patch_jar(jar(self.old,add_signed=True),self.policy,self.receipt)

if __name__=='__main__':unittest.main()
