"""Static gate for the full Simply Swords sword-pool boss reward (owner decision, 15 Oct 2026).

Always checks the committed pool against its recorded JAR evidence. If the R4-pinned
simplyswords JAR is available (AO_SIMPLYSWORDS_JAR or the default local profile path),
also re-derives the pool from the JAR and requires byte-identical output.
"""
import json, os, re, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import compile_simplyswords_pool as gen

RES = ROOT / 'addons/ao-campaign/src/main/resources'
SRC = ROOT / 'addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign'
DEFAULT_JAR = Path(r'C:/Users/headq/curseforge/minecraft/Instances/Ambient Odyssey v0.4.9.1 - Structure Difficulty + Celestisynth TEST/mods/simplyswords-neoforge-1.70.2-1.21.1.jar')


class SimplySwordsFullPool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pool = json.loads((RES / 'ao_sword_pool.json').read_text(encoding='utf-8'))
        cls.evidence = json.loads(gen.EVIDENCE.read_text(encoding='utf-8'))
        cls.policy = json.loads((RES / 'ao_loot_policy.json').read_text(encoding='utf-8'))
        cls.rewards = (SRC / 'BossRewards.java').read_text(encoding='utf-8')

    def test_every_pool_id_resolves_in_pinned_jar_evidence(self):
        ids = self.pool['ids']
        self.assertEqual(self.pool['count'], len(ids)); self.assertEqual(len(ids), 133)
        self.assertEqual(ids, sorted(set(ids)))
        self.assertEqual(self.pool['source_jar_sha256'], gen.JAR_SHA256)
        rows = {r['id']: r for r in self.evidence['rows']}
        self.assertEqual(sorted(rows), ids)
        for i in ids:
            r = rows[i]
            self.assertTrue(i.startswith('simplyswords:'), i)
            self.assertTrue(r['registered_literal'] and r['item_model'] and r['lang_key'], i)
            self.assertTrue(r['in_simplyswords_swords'] or r['in_c_swords'], i)

    def test_pool_contains_all_registered_previous_uniques(self):
        registered_uniques = set(self.policy['unique_weapons']) - set(self.evidence['previous_58_uniques_not_registered'])
        self.assertEqual(len(registered_uniques), 57)
        self.assertTrue(registered_uniques <= set(self.pool['ids']))

    def test_no_non_weapon_and_no_owner_exclusion_applied(self):
        ids = set(self.pool['ids'])
        for item in ['simplyswords:runic_tablet', 'simplyswords:runefused_gem', 'simplyswords:netherfused_gem',
                     'simplyswords:empowered_remnant', 'simplyswords:contained_remnant', 'simplyswords:tampered_remnant',
                     'simplyswords:runic_forge']:
            self.assertNotIn(item, ids)
        self.assertEqual(self.pool['owner_exclusions_applied'], [])
        for group in self.evidence['owner_review_exclusion_candidates'].values():
            self.assertTrue(set(group) <= ids)  # listed for the owner, not removed

    def test_every_eligible_boss_uses_the_new_pool(self):
        # Every policy boss reaches createBonus through drops(); createBonus draws from swordPoolIds().
        self.assertRegex(self.rewards, r'var tier=tier\(id\);if\(tier==null\)return;')
        self.assertIn('for(var stack:createBonus(player,tier,player.getRandom()))', self.rewards)
        body = self.rewards[self.rewards.index('public static List<ItemStack> createBonus'):self.rewards.index('public void drops')]
        self.assertIn('swordPoolIds()', body)
        self.assertNotIn('uniqueIds()', body)
        self.assertIn('getResourceAsStream("/ao_sword_pool.json")', self.rewards)
        self.assertEqual(len(self.policy['bosses']), 32)  # boss mapping unchanged

    def test_independent_of_regalia_and_affixed_rolls(self):
        body = self.rewards[self.rewards.index('public static List<ItemStack> createBonus'):self.rewards.index('public void drops')]
        self.assertEqual(body.count('result.add('), 4)  # affixed, Regalia, sword, rare extras
        self.assertNotIn('simplyswords', json.dumps(self.policy['regalia']))
        self.assertIn('"simplyswords"', self.rewards[self.rewards.index('regaliaIds()'):self.rewards.index('swordPoolIds()')])

    def test_r4_policy_left_byte_identical_for_r5_toolchain(self):
        self.assertEqual(len(self.policy['unique_weapons']), 58)
        self.assertNotIn('sword_pool', self.policy)

    def test_rederive_from_jar_when_available(self):
        jar = Path(os.environ.get('AO_SIMPLYSWORDS_JAR', DEFAULT_JAR))
        if not jar.is_file(): self.skipTest('pinned Simply Swords JAR not available')
        pool, evidence = gen.build(jar)
        self.assertEqual((RES / 'ao_sword_pool.json').read_bytes(), gen.dump(pool))
        self.assertEqual(gen.EVIDENCE.read_bytes(), gen.dump(evidence))


if __name__ == '__main__':
    unittest.main()
