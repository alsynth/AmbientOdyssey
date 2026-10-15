"""Synthetic tests for the R2-hash-gated R3 packager.

No private R2 ZIP, compiled Minecraft runtime, or CurseForge download required.
"""
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('package_r3_from_r2',ROOT/'tools/package_r3_from_r2.py')
pack=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)

def sha(b):return hashlib.sha256(b).hexdigest()

def jar(modid):
    f=io.BytesIO()
    with zipfile.ZipFile(f,'w') as z:
        z.writestr('META-INF/neoforge.mods.toml',f'[[mods]]\nmodId="{modid}"\nversion="0.3"\n')
    return f.getvalue()

def make_zip(path,data):
    with zipfile.ZipFile(path,'w') as z:
        for n,v in data.items():z.writestr(n,v)

class R3Bridge(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory();self.addCleanup(self.d.cleanup)
        self.root=Path(self.d.name);self.base=self.root/'r2.zip';self.out=self.root/'r3.zip'
        self.overlay=self.root/'over';self.overlay.mkdir()
        self.files={
            'manifest.json':json.dumps({'files':[{'projectID':1,'fileID':4},{'projectID':2,'fileID':5}]}).encode(),
            'overrides/mods/ao-campaign-old.jar':jar('ao_campaign'),
            'overrides/mods/ao-other.jar':jar('ao_other'),
            'overrides/config/example.json':b'{"kept":true}',
        }
        make_zip(self.base,self.files);self.plan=self.root/'plan.json'

    def change(self,action,path,data=None,reason='Owner-approved test',old_sha=None):
        d={'action':action,'path':path,'reason':reason}
        if action in ('replace','remove'):d['old_sha256']=old_sha or sha(self.files[path])
        if action!='remove':
            dest=self.overlay/path;dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data);d['new_sha256']=sha(data)
        return d

    def runplan(self,changes):
        self.plan.write_text(json.dumps({'format':'ao-r2-to-r3-1','reason':'test','changes':changes}))
        return pack.build(self.base,self.overlay,self.plan,self.out,
                          expected_base_sha=sha(self.base.read_bytes()),expected_pins=2,expected_jars=2)

    def test_add_plus_replace_preserves_existing_and_rollback(self):
        changes=[self.change('replace','overrides/mods/ao-campaign-old.jar',jar('ao_campaign')+b'changed'),
                 self.change('add','overrides/AO_TEST_NOTES/R3.txt',b'R3 test')]
        rec=self.runplan(changes)
        self.assertEqual(rec['status'],'STATIC_PACKAGE_CREATED_NOT_RUNTIME_TESTED')
        d=pack.read_archive(self.out)
        self.assertEqual(d['overrides/config/example.json'],self.files['overrides/config/example.json'])
        self.assertEqual(json.loads(d['manifest.json'])['files'],json.loads(self.files['manifest.json'])['files'])
        rollback=pack.read_archive(self.root/'r3-Rollback.zip')
        self.assertEqual(rollback['overrides/mods/ao-campaign-old.jar'],self.files['overrides/mods/ao-campaign-old.jar'])
        self.assertTrue((self.root/'r3.zip.report.json').exists())

    def test_reject_native_loot_table_overlay(self):
        c=self.change('add','overrides/config/paxi/datapacks/x/data/minecraft/loot_table/chests/stronghold.json',b'{}')
        with self.assertRaisesRegex(ValueError,'Native loot-table'):self.runplan([c])

    def test_reject_replacing_global_modifier_list(self):
        c=self.change('add','overrides/config/paxi/datapacks/x/data/neoforge/loot_modifiers/global_loot_modifiers.json',
                      b'{"replace":true,"entries":[]}')
        with self.assertRaisesRegex(ValueError,'Global loot modifiers'):self.runplan([c])

    def test_reject_duplicate_modids(self):
        c=self.change('replace','overrides/mods/ao-other.jar',jar('ao_campaign'))
        with self.assertRaisesRegex(ValueError,'Duplicate bundled addon'):self.runplan([c])

    def test_reject_bad_prior_hash(self):
        c=self.change('replace','overrides/config/example.json',b'new',old_sha='1'*64)
        with self.assertRaisesRegex(ValueError,'old_sha256'):self.runplan([c])

    def test_reject_output_overwrite(self):
        c=self.change('replace','overrides/config/example.json',b'new')
        self.runplan([c])
        with self.assertRaisesRegex(ValueError,'never overwrite'):self.runplan([c])

    def test_reject_file_content_mismatch(self):
        c=self.change('replace','overrides/config/example.json',b'new');c['new_sha256']='1'*64
        with self.assertRaisesRegex(ValueError,'new SHA256'):self.runplan([c])

    def test_reject_unsafe_traversal(self):
        c={'action':'add','path':'overrides/../bad','reason':'test','new_sha256':'1'*64}
        with self.assertRaisesRegex(ValueError,'Invalid or duplicate'):self.runplan([c])

    def test_reject_wrong_r2_base(self):
        c=self.change('replace','overrides/config/example.json',b'new')
        self.plan.write_text(json.dumps({'format':'ao-r2-to-r3-1','reason':'x','changes':[c]}))
        with self.assertRaisesRegex(ValueError,'R2 base SHA256'):
            pack.build(self.base,self.overlay,self.plan,self.out)

    def test_reject_cross_namespace_jar_loot_replacement(self):
        f=io.BytesIO()
        with zipfile.ZipFile(f,'w') as z:
            z.writestr('META-INF/neoforge.mods.toml','[[mods]]\nmodId="ao_other"\n')
            z.writestr('data/cataclysm/loot_table/chests/boss.json','{}')
        c=self.change('replace','overrides/mods/ao-other.jar',f.getvalue())
        with self.assertRaisesRegex(ValueError,'shadows a foreign/native loot table'):self.runplan([c])

if __name__=='__main__':unittest.main()
