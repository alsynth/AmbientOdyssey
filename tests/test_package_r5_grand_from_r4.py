"""Synthetic R4 -> R5 Grand import package tests (no private binary required)."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r5package',ROOT/'tools/package_r5_grand_from_r4.py')
packer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(packer)

def h(x):return hashlib.sha256(x).hexdigest()
IMPOSSIBLE=b'{"criteria":{"locked":{"trigger":"minecraft:impossible"}}}'
GATE_MEMBERS=sorted('overrides/'+r for r in packer.GATE_FILES)

class R5ImportFromR4(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.base=self.root/'R4.zip'
        self.newjar=self.root/'new.jar'
        self.receipt=self.root/'reviewed-patch.json'
        self.out=self.root/'R5.zip'
        self.original=b'R4 campaign synthetic JAR'
        self.newjar.write_bytes(b'R5 candidate synthetic JAR')
        manifest={'name':'R4','version':'0.5.4','files':[{'projectID':123,'fileID':456},{'projectID':789,'fileID':101}]}
        packer.write_zip(self.base,{
            'manifest.json':json.dumps(manifest).encode(),
            packer.CAMPAIGN_PATH:self.original,
            'overrides/config/brutalbosses.json':b'{"healthMultiplier":4}',
            'overrides/config/dungeon_difficulty/difficulty_v2.json':b'{"zones":30}',
            # R4 shipped this unobtainable gate; R5 must replace it.
            packer.PINNACLE_MEMBER:IMPOSSIBLE,
            'overrides/config/paxi/datapacks/ao_campaign_gates/pack.mcmeta':b'{"pack":{"pack_format":48}}',
            'overrides/config/paxi/datapacks/ao_campaign/data/ao_campaign/advancement/milestones/tier_5.json':IMPOSSIBLE,
        })
        self.inputs={
            'status':'R5_GRAND_RESOURCE_ONLY_EXPERIMENTAL_JAR_NOT_RUNTIME_TESTED',
            'basis_release_sha256':h(self.base.read_bytes()),
            'basis_campaign_jar_sha256':h(self.original),
            'patched_campaign_jar_sha256':h(self.newjar.read_bytes()),
            'only_modified_jar_member':'ao_loot_policy.json',
            'minecraft_runtime_tested':False,
            'lootr_multiplayer_tested':False,
            'changed_grand_pool_indices':[[f'test:chests/t{i}',i,1] for i in range(5)],
        }
        self.receipt.write_text(json.dumps(self.inputs))

    def build(self):
        return packer.build(self.base,self.newjar,self.receipt,self.out,
            expected_base=h(self.base.read_bytes()),
            expected_campaign=h(self.original),expected_pins=2,expected_jar_count=1)

    def test_only_two_import_members_change(self):
        r=self.build()
        self.assertEqual(r['cf_references'],2)
        self.assertEqual(r['custom_addon_jar_count'],1)
        self.assertEqual(r['changed_members'],sorted(['manifest.json',packer.CAMPAIGN_PATH,*GATE_MEMBERS]))
        self.assertFalse(r['minecraft_runtime_tested'])
        old=packer.read_members(self.base)
        new=packer.read_members(self.out)
        self.assertEqual(old['overrides/config/brutalbosses.json'],new['overrides/config/brutalbosses.json'])
        self.assertEqual(old['overrides/config/dungeon_difficulty/difficulty_v2.json'],
                         new['overrides/config/dungeon_difficulty/difficulty_v2.json'])
        self.assertEqual(json.loads(old['manifest.json'])['files'],json.loads(new['manifest.json'])['files'])
        self.assertEqual(new[packer.CAMPAIGN_PATH],self.newjar.read_bytes())
        self.assertEqual(packer.read_members(self.root/'R5-Rollback.zip')[packer.CAMPAIGN_PATH],self.original)
        self.assertTrue((self.root/'R5.zip.report.json').exists())
        for m in GATE_MEMBERS:
            self.assertEqual(new[m],(packer.GATE_SOURCE_ROOT/m[len('overrides/'):]).read_bytes())
        rollback=packer.read_members(self.root/'R5-Rollback.zip')
        self.assertEqual(rollback[packer.PINNACLE_MEMBER],IMPOSSIBLE)
        added=json.loads(rollback['ROLLBACK-RECEIPT.json'])['added_members_delete_on_rollback']
        self.assertEqual(added,sorted(m for m in GATE_MEMBERS if 'resourcepacks' in m))

    def test_r4_impossible_pinnacle_never_ships(self):
        self.build()
        new=packer.read_members(self.out)
        self.assertEqual(packer.impossible_gates(new),[])
        self.assertIn(packer.CORNELIA,new[packer.PINNACLE_MEMBER].decode())

    def test_code_granted_campaign_milestones_are_allowed(self):
        self.build()
        name='overrides/config/paxi/datapacks/ao_campaign/data/ao_campaign/advancement/milestones/tier_5.json'
        self.assertEqual(packer.read_members(self.out)[name],IMPOSSIBLE)

    def rebase_with(self,name,data):
        members=packer.read_members(self.base);members[name]=data
        self.base.unlink();packer.write_zip(self.base,members)
        d=dict(self.inputs);d['basis_release_sha256']=h(self.base.read_bytes())
        self.receipt.write_text(json.dumps(d))

    def test_reject_other_impossible_gate_in_r4(self):
        self.rebase_with('overrides/config/paxi/datapacks/x/data/apotheosis/advancement/progression/ancient.json',IMPOSSIBLE)
        with self.assertRaisesRegex(ValueError,'Gate safeguard'):self.build()
        self.assertFalse(self.out.exists())

    def test_reject_unapproved_source_gate(self):
        gate=self.root/'gate'
        for rel in packer.GATE_FILES:
            (gate/rel).parent.mkdir(parents=True,exist_ok=True)
            (gate/rel).write_bytes((packer.GATE_SOURCE_ROOT/rel).read_bytes())
        (gate/packer.GATE_FILES[1]).write_bytes(IMPOSSIBLE)
        with self.assertRaisesRegex(ValueError,'approved epic gear'):
            packer.build(self.base,self.newjar,self.receipt,self.out,expected_base=h(self.base.read_bytes()),
                expected_campaign=h(self.original),expected_pins=2,expected_jar_count=1,gate_root=gate)

    def test_reject_existing_output(self):
        self.out.write_bytes(b'exists')
        with self.assertRaisesRegex(ValueError,'Never overwrite'):self.build()

    def test_reject_wrong_original_r4_hash(self):
        with self.assertRaisesRegex(ValueError,'R4 base ZIP SHA256'):
            packer.build(self.base,self.newjar,self.receipt,self.out,expected_base='0'*64,
                         expected_campaign=h(self.original),expected_pins=2,expected_jar_count=1)

    def test_reject_tampered_reviewed_campaign(self):
        self.newjar.write_bytes(b'different from receipt')
        with self.assertRaisesRegex(ValueError,'Patched campaign JAR hash'):
            self.build()

    def test_reject_fabricated_runtime_success_in_receipt(self):
        d=dict(self.inputs);d['lootr_multiplayer_tested']=True
        self.receipt.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'Unverified R4-source'):
            self.build()

    def test_reject_missing_reviewed_pool_change(self):
        d=dict(self.inputs);d['changed_grand_pool_indices']=d['changed_grand_pool_indices'][:4]
        self.receipt.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'Unverified R4-source'):
            self.build()

    def test_reject_unexpected_campaign_version_in_roster(self):
        wrong=packer.read_members(self.base)
        wrong['overrides/mods/ao-campaign-0.3.3-experimental.jar']=wrong.pop(packer.CAMPAIGN_PATH)
        self.base.unlink()
        packer.write_zip(self.base,wrong)
        with self.assertRaisesRegex(ValueError,'compiled campaign JAR differs'):
            self.build()

if __name__=='__main__':unittest.main()
