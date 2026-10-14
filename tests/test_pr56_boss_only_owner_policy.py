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

    def test_native_source_does_not_invent_mechanical_nest_boss_identity(self):
        evidence=ROOT/"docs/balance/DD_MECHANICAL_NEST_FOUNDRY_NATIVE_BOSS_REFS_20261014.json"
        doc=json.loads(evidence.read_text(encoding="utf-8"))
        self.assertFalse(doc["mechanical_nest"]["native_boss_found_by_source_scan"])
        self.assertEqual(doc["mechanical_nest"]["boss_entity_id"],"UNKNOWN")
        named=doc["mechanical_nest"]["unique_explicit_custom_name_entities"]
        self.assertEqual({v["name"] for v in named},{"Gearling"})
        self.assertTrue(all(v["source_health"]==6 and v["is_baby"] for v in named))
        self.assertFalse(doc["native_boss_runtime_tested"])
        self.assertFalse(doc["live_dd_deployment_authorized"])
        gaps={v["ref"] for v in doc["mechanical_nest"]["native_resource_reference_gaps"]}
        self.assertEqual(gaps,{
            "dungeons_arise:mechanical_nest/mechanical_nest_spawner_6",
            "dungeons_arise:mechanical_nest/mechanical_nest_bridge_terminator_6_",
            "dungeons_arise:mechanical_nest/mechanical_nest_decoration"})
        self.assertTrue(all(
            any(marker in v["resolution"] for marker in ("NO_AUTOFIX","DO_NOT_RENAME"))
            for v in doc["mechanical_nest"]["native_resource_reference_gaps"]))

    def test_foundry_named_native_encounters_are_not_assumed_bosses(self):
        evidence=ROOT/"docs/balance/DD_MECHANICAL_NEST_FOUNDRY_NATIVE_BOSS_REFS_20261014.json"
        doc=json.loads(evidence.read_text(encoding="utf-8"))
        foundry=doc["foundry"]
        self.assertEqual({x["name"] for x in foundry["named_native_spawner_entity_types"]},
                         {"Foundry Guardian","Forge Sentry","Debris Miner"})
        self.assertEqual({x["source_health"] for x in foundry["named_native_spawner_entity_types"]},
                         {50,55,80})
        self.assertFalse(foundry["unresolved_jigsaw_pool_reference"]["change_authorized"])
    def test_foundry_missing_native_reference_is_not_fixed_by_guess(self):
        p=json.loads(POLICY.read_text(encoding="utf-8"))
        foundry=next(r for r in p["rules"] if r["structure_id"]=="dungeons_arise:foundry")
        self.assertEqual(foundry["native_jigsaw_missing_reference"],
                         "dungeons_arise:underworld/foundry/foundry_corridor_gears")
        self.assertFalse(foundry["executable_approval_for_live_scaling"])

if __name__=="__main__":
    unittest.main()
