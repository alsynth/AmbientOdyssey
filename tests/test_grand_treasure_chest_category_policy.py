"""Static regression: R3 Grand Treasure selection must remain chest-specific.

The currently built private R2 archive and compiled campaign JAR still use their
older mapping until an explicitly reviewed R3 policy is generated and compiled.
"""
import ast
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/handoffs/loot-update-20261015/chest-source-audit.json'
GRAND=ROOT/'docs/handoffs/loot-update-20261015/grand-treasure-candidates.json'
ALTERNATIVES=ROOT/'docs/handoffs/loot-update-20261015/R3_SAME_TABLE_GRAND_ALTERNATIVES_UNAPPROVED.json'

def table_resource(table):
    ns,path=table.split(':',1)
    return f'data/{ns}/loot_table/{path}.json'

class GrandChestCategoryPolicy(unittest.TestCase):
    def test_generator_has_no_structure_wide_winner_reassignment(self):
        source=(ROOT/'tools/audit_additive_loot_sources.py').read_text(encoding='utf-8')
        ast.parse(source)  # compile without requiring locally installed nbtlib
        self.assertNotIn("best=max(candidates,key=lambda m:m['selection_score'])",source)
        self.assertNotIn("for key in ['source_resource','source_sha256','pool_index','selection_score']:m[key]=best[key]",source)
        self.assertIn("category-appropriate loot per chest",source)

    def test_eight_cross_table_r2_mappings_have_own_native_candidates(self):
        current=json.loads(GRAND.read_text())
        alternatives=json.loads(ALTERNATIVES.read_text())['alternatives']
        rows=json.loads(AUDIT.read_text())
        by_context={(r['structure'],r['table']):r for r in rows}
        cross=[r for r in current if r['source_resource'] != table_resource(r['table'])]
        self.assertEqual(len(current),14)
        self.assertEqual(len(cross),8)
        self.assertEqual(len(alternatives),8)
        alternatives_by_key={(r['structure'],r['trigger_table']):r for r in alternatives}
        self.assertEqual(set(alternatives_by_key),{(r['structure'],r['table']) for r in cross})
        for c in cross:
            key=(c['structure'],c['table'])
            alt=alternatives_by_key[key];original=by_context[key]
            self.assertEqual(original['status'],'CANDIDATE_SOURCE_VERIFIED')
            self.assertEqual(alt['same_table_candidate_source'],table_resource(c['table']))
            self.assertEqual(alt['same_table_source_sha256'],original['source_sha256'])
            self.assertEqual(alt['same_table_candidate_pool_index'],original['selected_pool'])
            self.assertEqual(alt['owner_approval'],'NOT_DECIDED')

    def test_r2_current_mapping_is_not_misreported_as_r3_approved(self):
        current=json.loads(GRAND.read_text())
        self.assertEqual(sum(r['source_resource'] != table_resource(r['table']) for r in current),8)

if __name__=='__main__':unittest.main()
