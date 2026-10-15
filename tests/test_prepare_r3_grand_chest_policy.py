"""No-JAR static tests of per-chest R3 candidate policy generation.

The output is REVIEW-ONLY; these tests cannot approve live loot or create R3 JARs.
"""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r3_grand_candidate',ROOT/'tools/prepare_r3_grand_chest_policy.py')
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)

class PerChestGrandCandidates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads(tool.AUDIT.read_text(encoding='utf-8'))
        cls.r2=json.loads(tool.R2.read_text(encoding='utf-8'))

    def test_all_14_existing_contexts_preserved_but_8_borrowed_sources_replaced(self):
        candidate, review=tool.produce(self.source,self.r2)
        self.assertEqual(len(candidate),14)
        self.assertEqual(len(review),14)
        self.assertEqual(sum(r['replaces_structure_wide_borrowing'] for r in review),8)
        self.assertEqual({(r['structure'],r['table']) for r in candidate},
                         {(r['structure'],r['table']) for r in self.r2})
        self.assertTrue(all(r['source_resource']==tool.table_resource(r['table']) for r in candidate))
        self.assertTrue(all(r['chance']==.05 and r['tier']>=3 for r in candidate))
        self.assertTrue(all(r['source_approval']=='NEEDS_INSTALLED_JAR_REVALIDATION' for r in review))
        self.assertTrue(all(r['best_pool_category_approval']=='NEEDS_MANUAL_REVIEW' for r in review))

    def test_keep_kayra_library_treasure_uses_own_source_in_preview(self):
        candidate,_=tool.produce(self.source,self.r2)
        row=next(r for r in candidate if r['table'].endswith('/keep_kayra_library_treasure'))
        self.assertEqual(row['source_resource'],
                         'data/dungeons_arise/loot_table/chests/keep_kayra/keep_kayra_library_treasure.json')
        self.assertEqual(row['pool_index'],2)
        self.assertEqual(row['tier'],6)

    def test_committed_review_only_preview_matches_generated_candidate(self):
        expected,_=tool.produce(self.source,self.r2)
        actual=json.loads((ROOT/'docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json').read_text())
        self.assertEqual(actual,expected)

    def test_committed_review_ledger_does_not_mark_source_approved(self):
        _,expected=tool.produce(self.source,self.r2)
        ledger=json.loads((ROOT/'docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_REVIEW_LEDGER.json').read_text())
        self.assertEqual(ledger['status'],'R3_CANDIDATES_ONLY_NOT_APPROVED_OR_COMPILED')
        self.assertEqual(ledger['candidates'],expected)
        self.assertTrue(all(e['best_pool_category_approval']=='NEEDS_MANUAL_REVIEW' for e in ledger['candidates']))

    def test_invalid_source_missing_prevents_candidate(self):
        with self.assertRaisesRegex(ValueError,'No audited original native candidate'):
            tool.produce([],self.r2)

    def test_invalid_pool_index_prevents_candidate(self):
        source=[dict(x) for x in self.source]
        row=next(r for r in source if r['status']=='CANDIDATE_SOURCE_VERIFIED'
                 and r['structure']=='dungeons_arise:keep_kayra')
        row['selected_pool']=row['pool_count']+1
        with self.assertRaisesRegex(ValueError,'Pool index'):
            tool.produce(source,self.r2)

    def test_changed_5_percent_chance_blocks_promotion(self):
        bad=[dict(x) for x in self.r2];bad[0]['chance']=.25
        with self.assertRaisesRegex(ValueError,'owner-approved 5%'):
            tool.produce(self.source,bad)

    def test_corrupted_source_hash_blocks_promotion(self):
        source=[dict(x) for x in self.source]
        row=next(r for r in source if r['status']=='CANDIDATE_SOURCE_VERIFIED')
        row['source_sha256']='abcd'
        with self.assertRaisesRegex(ValueError,'Expected source SHA'):
            tool.produce(source,self.r2)

if __name__=='__main__':unittest.main()
