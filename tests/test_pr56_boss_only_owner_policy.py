"""PR56 owner priority protection: Mechanical Nest boss, not minion DD."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/"docs/balance/DD_OWNER_BOSS_CENTRIC_SCOPE_20261014.json"
CANDIDATE=ROOT/"experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json"

class OwnerBossCentricGuard(unittest.TestCase):
    def test_mechanical_nest_boss_priority_blocks_blanket_mob_scaling_rollout(self):
        p=json.loads(POLICY.read_text(encoding="utf-8"))
        self.assertFalse(p["natural_generation_verified"])
        self.assertFalse(p["boss_spawn_verified"])
        nest=next(r for r in p["rules"] if r["structure_id"]=="dungeons_arise:mechanical_nest")
        self.assertEqual(nest["provisional_structure_tier"],5)
        self.assertEqual(nest["encounter_importance"],"BOSS_PRIMARY")
        self.assertEqual(nest["ordinary_spawner_mob_balancing_priority"],"DEPRIORITIZED")
        self.assertEqual(nest["native_mounted_encounters"],"PRESERVE_UNALTERED")
        self.assertEqual(nest["boss_entity_id"],"UNVERIFIED")
        self.assertFalse(nest["executable_approval_for_live_scaling"])
        self.assertFalse(nest["existing_pr56_candidate_gameplay_modified"])
        self.assertIn("UNDEPLOYED_DRAFT",nest["generic_dungeon_difficulty_zone"])

    def test_existing_draft_is_not_silent_approval_to_buff_all_nest_mobs(self):
        obj=json.loads(CANDIDATE.read_text(encoding="utf-8"))
        zones=[z for dim in obj["dimensions"] for z in dim["zones"]
                if z["zone_matches"].get("structure")=="dungeons_arise:mechanical_nest"]
        self.assertEqual(len(zones),1)
        self.assertEqual(zones[0]["difficulty"]["name"],"ao_tier_5")
        # This rule is an old candidate to revisit, NOT the owner's approved
        # boss-specific end-state. Do not toggle the candidate on globally.
        p=json.loads(POLICY.read_text(encoding="utf-8"))
        self.assertTrue(any(
            r["structure_id"]=="dungeons_arise:mechanical_nest"
            and not r["executable_approval_for_live_scaling"]
            for r in p["rules"]))

    def test_foundry_missing_native_reference_is_not_fixed_by_guess(self):
        p=json.loads(POLICY.read_text(encoding="utf-8"))
        foundry=next(r for r in p["rules"] if r["structure_id"]=="dungeons_arise:foundry")
        self.assertEqual(foundry["native_jigsaw_missing_reference"],
                         "dungeons_arise:underworld/foundry/foundry_corridor_gears")
        self.assertFalse(foundry["executable_approval_for_live_scaling"])

if __name__=="__main__":
    unittest.main()
