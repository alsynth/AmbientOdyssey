"""Synthetic tests for experimental R3 Grand Treasure staging.

No private R2 zip, official mod JAR, or Minecraft runtime required.
"""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('stage_r3',ROOT/'tools/stage_r3_grand_policy.py')
stage_r3=importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage_r3)

def enc(x): return (json.dumps(x,indent=2)+'\n').encode()
def h(x):return hashlib.sha256(x).hexdigest()

class ReviewedR3Grand(unittest.TestCase):
    def setUp(self):
        self.candidates=[
            {'structure':'dungeons_arise:keep_kayra','tier':6,
             'table':'dungeons_arise:chests/keep_kayra/keep_kayra_library_treasure',
             'source_resource':'data/dungeons_arise/loot_table/chests/keep_kayra/keep_kayra_library_treasure.json',
             'source_sha256':'a'*64,'pool_index':2,'chance':0.05},
            {'structure':'dungeons_arise:keep_kayra','tier':6,
             'table':'dungeons_arise:chests/keep_kayra/keep_kayra_normal',
             'source_resource':'data/dungeons_arise/loot_table/chests/keep_kayra/keep_kayra_normal.json',
             'source_sha256':'b'*64,'pool_index':1,'chance':0.05},
        ]
        self.base={'bosses':{'bosses_of_mass_destruction:lich':5},
                   'regalia':['artifacts:lucky_scarf'],
                   'native_gems':'UNCHANGED',
                   'grand_treasure':[dict(self.candidates[0],source_resource='data/dungeons_arise/loot_table/chests/keep_kayra/keep_kayra_garden_normal.json'),
                                     dict(self.candidates[1],source_resource='data/dungeons_arise/loot_table/chests/keep_kayra/keep_kayra_garden_normal.json')]}
        self.cbytes=enc(self.candidates)
        self.audit={'status':'STATIC_JAR_EVIDENCE_ONLY_NOT_RUNTIME_ACCEPTED',
                    'candidate_input_sha256':h(self.cbytes),
                    'grand_context_count':2,
                    'grand':[]}
        for row in self.candidates:
            selected=row['pool_index']
            pools=[{'pool_index':j,'entries':[{'type':'minecraft:item','name':'minecraft:diamond','weight':1,'has_children':False}],
                    'native_rolls':1} for j in range(selected+1)]
            self.audit['grand'].append({
                'structure':row['structure'],'trigger_table':row['table'],
                'static_status':'SOURCE_STATIC_VERIFIED_NOT_RUNTIME_APPROVED','blockers':[],
                'selected_native_source':row['source_resource'],'same_table':True,
                'expected_source_sha256':row['source_sha256'],
                'actual_source_sha256_matches':True,'pool_index':selected,
                'source_jar_candidates':['DungeonsArise.jar'],
                'potential_paxi_overrides':[],
                'native_all_pools_for_human_comparison':pools,
            })
        self.abytes=enc(self.audit)
        self.index=stage_r3.mappings(self.candidates)
        self.review=stage_r3.draft(self.index,self.cbytes,self.audit,self.abytes)

    def approve(self):
        approval=json.loads(json.dumps(self.review))
        approval['status']='REVIEWED_FOR_EXPERIMENTAL_BUILD'
        for row in approval['decisions']:
            row['reviewed_category_fit']=True
            row['reviewed_native_entries_weights_conditions_functions']=True
            row['approved_for_experimental_build']=True
            row['reviewer_rationale']='Confirmed matching chest treasure category, no progression trophies.'
        return approval

    def stage(self,approved=None):
        return stage_r3.stage(self.index,self.cbytes,self.audit,self.abytes,approved if approved is not None else self.approve(),self.base)

    def test_positive_stage_replaces_only_grand_and_is_experimental(self):
        compiled,report=self.stage()
        self.assertEqual(compiled['grand_treasure'],self.candidates)
        self.assertEqual({k:v for k,v in compiled.items() if k!='grand_treasure'},
                         {k:v for k,v in self.base.items() if k!='grand_treasure'})
        self.assertEqual(report['approved_context_count'],2)
        self.assertFalse(report['minecraft_runtime_tested'])
        self.assertFalse(report['native_lootr_multiplayer_tested'])
        self.assertEqual(report['cross_table_borrowing_count'],0)

    def test_draft_explicitly_denies_approvals_by_default(self):
        self.assertEqual(self.review['status'],'DRAFT_NOT_APPROVED')
        for row in self.review['decisions']:
            self.assertFalse(row['approved_for_experimental_build'])
            self.assertFalse(row['reviewed_category_fit'])
        with self.assertRaisesRegex(ValueError,'explicitly marked REVIEWED_FOR_EXPERIMENTAL_BUILD'):
            self.stage(self.review)

    def test_reject_unverified_native_jar_hash(self):
        self.audit['grand'][0]['actual_source_sha256_matches']=False
        self.abytes=enc(self.audit);self.review=stage_r3.draft(self.index,self.cbytes,self.audit,self.abytes)
        with self.assertRaisesRegex(ValueError,'Native loot resource SHA'):
            self.stage()

    def test_reject_paxi_precedence_conflict(self):
        self.audit['grand'][0]['potential_paxi_overrides']=['pack/data/dungeons_arise/loot_table/chests/a.json']
        self.abytes=enc(self.audit);self.review=stage_r3.draft(self.index,self.cbytes,self.audit,self.abytes)
        with self.assertRaisesRegex(ValueError,'Paxi precedence'):
            self.stage()

    def test_reject_cross_table_pool_even_if_reviewer_approved(self):
        self.audit['grand'][0]['same_table']=False
        self.abytes=enc(self.audit);self.review=stage_r3.draft(self.index,self.cbytes,self.audit,self.abytes)
        with self.assertRaisesRegex(ValueError,'another source'):
            self.stage()

    def test_reject_unapproved_extra_chest_context(self):
        candidate=dict(self.candidates[0]);candidate['table']='dungeons_arise:chests/keep_kayra/bonus'
        candidate['source_resource']=stage_r3.table_resource(candidate['table'])
        idx=stage_r3.mappings(self.candidates+[candidate])
        with self.assertRaisesRegex(ValueError,'Audit chest count'):
            stage_r3.stage(idx,self.cbytes,self.audit,self.abytes,self.approve(),self.base)

    def test_reject_composite_native_pool(self):
        self.audit['grand'][0]['native_all_pools_for_human_comparison'][2]['entries'][0]['type']='minecraft:loot_table'
        self.abytes=enc(self.audit);self.review=stage_r3.draft(self.index,self.cbytes,self.audit,self.abytes)
        with self.assertRaisesRegex(ValueError,'Unsafe composite'):
            self.stage()

    def test_reject_different_native_audit_receipt(self):
        wrong=self.approve();wrong['audit_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'different installed-JAR audit'):
            self.stage(wrong)

    def test_reject_unreviewed_source_functions(self):
        approval=self.approve()
        approval['decisions'][0]['reviewed_native_entries_weights_conditions_functions']=False
        with self.assertRaisesRegex(ValueError,'Manual source/category approval incomplete'):
            self.stage(approval)

    def test_actual_14_contexts_are_not_auto_approved(self):
        cbytes=stage_r3.CANDIDATES.read_bytes()
        source=stage_r3.mappings(json.loads(cbytes))
        self.assertEqual(len(source),14)
        self.assertEqual(sum(not (r['table'].endswith('/keep_kayra_garden_normal')) for r in source.values())>0,True)
        self.assertEqual(len({stage_r3.key(r) for r in source.values()}),14)

if __name__=='__main__': unittest.main()
