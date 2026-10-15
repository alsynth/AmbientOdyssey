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
        self.assertEqual(r['changed_members'],['manifest.json',packer.CAMPAIGN_PATH])
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
