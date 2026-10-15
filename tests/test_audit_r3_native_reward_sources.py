"""Synthetic native reward JAR audit tests. No actual CurseForge mods necessary."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit_r3',ROOT/'tools/audit_r3_native_reward_sources.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class NativeRewardEvidence(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.mods=self.base/'mods';self.mods.mkdir()
        self.table={'type':'minecraft:chest','pools':[{'rolls':1,'entries':[
            {'type':'minecraft:item','name':'minecraft:diamond','weight':2}]}]}
        self.data=json.dumps(self.table).encode()
        self.src='data/testmod/loot_table/chests/best.json'
        self.trigger='data/testmod/loot_table/chests/ordinary.json'
        self.jar=self.mods/'testmod-1.0.jar'
        with zipfile.ZipFile(self.jar,'w') as f:
            f.writestr('META-INF/neoforge.mods.toml','[[mods]]\nmodId="testmod"\n')
            f.writestr(self.src,self.data)
            f.writestr(self.trigger,self.data)
            f.writestr('assets/testmod/models/item/amulet.json','{}')

    def row(self,table='testmod:chests/best'):
        return {'structure':'testmod:castle','tier':3,'table':table,
                'source_resource':self.src,'source_sha256':hashlib.sha256(self.data).hexdigest(),
                'pool_index':0,'chance':0.05}

    def test_direct_source_check(self):
        index,modids=audit.load_jar_index(self.mods)
        r=audit.grand_check([self.row()],self.mods,index)[0]
        self.assertEqual(r['static_status'],'SOURCE_STATIC_VERIFIED_NOT_RUNTIME_APPROVED')
        self.assertTrue(r['actual_source_sha256_matches'])
        self.assertTrue(r['same_table'])
        native=r['native_all_pools_for_human_comparison']
        self.assertEqual(len(native),1)
        self.assertEqual(native[0]['native_rolls'],1)
        self.assertEqual(native[0]['entries'][0]['name'],'minecraft:diamond')
        self.assertEqual(native[0]['entries'][0]['weight'],2)

    def test_cross_table_is_blocked_pending_owner_review(self):
        index,_=audit.load_jar_index(self.mods)
        r=audit.grand_check([self.row('testmod:chests/ordinary')],self.mods,index)[0]
        self.assertIn('CROSS_TABLE_SOURCE_CHOICE_NEEDS_INDEPENDENT_REVIEW',r['blockers'])
        self.assertEqual(r['static_status'],'BLOCKED')

    def test_changed_source_hash_is_blocked(self):
        index,_=audit.load_jar_index(self.mods)
        row=self.row();row['source_sha256']='0'*64
        r=audit.grand_check([row],self.mods,index)[0]
        self.assertIn('SOURCE_SHA256_CHANGED',r['blockers'])

    def test_paxi_collision_flags_even_if_original_jar_hash_matches(self):
        pack=self.base/'config/paxi/datapacks/testpack/data/testmod/loot_table/chests'
        pack.mkdir(parents=True);(pack/'best.json').write_text('{"pools":[]}')
        index,_=audit.load_jar_index(self.mods)
        r=audit.grand_check([self.row()],self.mods,index,self.base/'config/paxi/datapacks')[0]
        self.assertIn('PAXI_TABLE_OVERRIDE_PRECEDENCE_REQUIRES_RUNTIME_CONFIRMATION',r['blockers'])

    def test_catalogue_no_auto_approval_and_native_exclusions(self):
        index,modids=audit.load_jar_index(self.mods)
        rows=audit.regalia_check(self.mods,index,modids)
        self.assertGreater(len(rows),100)
        self.assertTrue(all(r['registered_item_verified'] is False for r in rows))
        self.assertTrue(any(r['currently_in_r2_reward_pool'] for r in rows))
        self.assertTrue(any(r['known_combat_risk_band'].startswith('C?') for r in rows))
        self.assertTrue(any(r['owner_disposition']=='NATIVE_ONLY_NO_NEW_REGALIA_REWARD' for r in rows
                            if r['id'].startswith('enigmaticlegacyplus:')))
        self.assertTrue(all(r['owner_disposition']!='ELIGIBILITY_APPROVED' for r in rows))

if __name__=='__main__':unittest.main()
