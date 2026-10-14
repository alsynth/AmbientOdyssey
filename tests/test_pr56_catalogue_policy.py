"""Fail-closed static guard for PR56 research ledgers (not an in-game test).

Run: python -m unittest discover -s tests -p 'test_pr56_catalogue_policy.py' -v
All files are text snapshots. These tests do NOT certify natural worldgen,
source-entity attitude, live DD behavior, or owner approval of provisional tiers.
"""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BAL = ROOT / "docs" / "balance"


def read_rows(name):
    with (BAL / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def by_id(rows):
    ids = [row["structure_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate structure_id in catalogue")
    return {row["structure_id"]: row for row in rows}


class PR56CataloguePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads((BAL / "DD_MAPPING_PROGRESS_BASELINE_20261014.json").read_text(encoding="utf-8"))
        cls.tiers = by_id(read_rows("DD_FULL_FIRST_PASS_TIER_MAP_20261014.csv"))
        cls.confidence = by_id(read_rows("DD_PROVISIONAL_CATEGORIES_CONFIDENCE_20261014.csv"))
        cls.native = by_id(read_rows("DD_KNOWN_NATIVE_ID_MAPPING_LEDGER_20261014.csv"))
        cls.nbt = by_id(read_rows("DD_NATIVE_NBT_EVIDENCE_20261014.csv"))
        cls.owner = by_id(read_rows("DD_OWNER_PROTECTED_26_SPAWNER_STRUCTURES_20261014.csv"))
        cls.critical = by_id(read_rows("DD_POSTMAP_CRITICAL_34_TIER_REVIEW_20261014.csv"))
        cls.pregen = by_id(read_rows("DD_29_WORLDGEN_LEGACY_EVIDENCE_CROSSCHECK_20261014.csv"))
        cls.matcher = read_rows("DD_POSTMAP_FIVE_SITE_ENTITY_MATCHER_20261014.csv")
        cls.candidate = json.loads(
            (ROOT / "experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json").read_text(encoding="utf-8")
        )

    def test_known_inventory_is_one_to_one_and_not_claimed_full_registry(self):
        expected = self.baseline["known_unique_ID_union"]
        self.assertEqual(expected, 1240)
        self.assertEqual(len(self.tiers), expected)
        self.assertEqual(self.tiers.keys(), self.confidence.keys())
        self.assertEqual(self.tiers.keys(), self.native.keys())
        self.assertEqual(len(self.nbt), 1219)  # history-only pre-21 scoped-client IDs
        self.assertFalse(self.baseline["registered_ID_enumeration_complete"])
        self.assertFalse(self.baseline["tested_natural_structure_generation"])
        for key, row in self.tiers.items():
            self.assertIn(row["proposed_tier"], {str(i) for i in range(10)}, key)
            self.assertEqual(row["proposed_tier"], self.confidence[key]["provisional_tier"], key)
            self.assertEqual(row["proposed_tier"], self.native[key]["current_working_tier"], key)
            self.assertEqual(row["eligible_for_live_DD"], "NO", key)
            self.assertEqual(self.confidence[key]["eligible_for_DD"], "NO", key)

    def test_26_owner_approved_tier_zero_and_spawner_signals_preserved(self):
        self.assertEqual(len(self.owner), 26)
        self.assertEqual(self.baseline["owner_approved_native_tier0_ids"], 26)
        for key, row in self.owner.items():
            with self.subTest(structure=key):
                self.assertEqual(row["owner_approved_tier"], "0")
                self.assertEqual(row["owner_review_hold"], "NO")
                self.assertEqual(row["eligible_for_DD_rule"], "NO")
                self.assertGreater(int(row["associated_source_NBT_spawner_indicator_count"]), 0)
                self.assertEqual(self.tiers[key]["proposed_tier"], "0")
                self.assertEqual(self.native[key]["current_working_tier"], "0")
                self.assertEqual(self.confidence[key]["provisional_tier"], "0")
                self.assertEqual(self.confidence[key]["tier_confidence"], "OWNER_APPROVED")
                self.assertEqual(self.nbt[key]["dd_working_tier"], "0")
                self.assertEqual(self.tiers[key]["eligible_for_live_DD"], "NO")

    def test_dungeon_crawl_tier_three_without_floor_split(self):
        key = "dungeoncrawl:dungeon"
        self.assertEqual(self.baseline["owner_approved_dungeon_crawl_overall_tier"], 3)
        self.assertTrue(self.baseline["dungeon_crawl_single_tier_all_floors"])
        self.assertTrue(self.baseline["dungeon_crawl_floor_split_cancelled_by_owner"])
        self.assertFalse(self.baseline["dungeon_crawl_floor_split_config_implemented"])
        for row, field in ((self.tiers[key], "proposed_tier"),
                           (self.confidence[key], "provisional_tier"),
                           (self.native[key], "current_working_tier"),
                           (self.nbt[key], "dd_working_tier"),
                           (self.critical[key], "first_pass_tier")):
            self.assertEqual(row[field], "3")
        self.assertIn("NO_FLOOR_SPLIT", self.critical[key]["action_on_tier"])
        self.assertEqual(self.tiers[key]["eligible_for_live_DD"], "NO")

    def test_critical_34_and_historical_pregen_29_are_not_deployable(self):
        self.assertEqual(len(self.critical), 34)
        self.assertEqual(len(self.pregen), 29)
        self.assertTrue(set(self.pregen).issubset(set(self.critical)))
        self.assertTrue(all(row["live_DD_allowed"] == "NO" for row in self.critical.values()))
        self.assertTrue(all(row["live_DD_allowed"] == "NO" and row["natural_generation_verified"] == "NO"
                            for row in self.pregen.values()))
        self.assertEqual(
            {k for k, row in self.pregen.items()
             if row["static_risk_flag"] == "HISTORIC_ZERO_CURATED_BIOME_MATCH__SUSPECT_SEL"},
            {"nova_structures:firewatch_tower_" + suffix for suffix in
             ("birch", "cherry", "forest", "mangrove", "savanna", "swamp")}
        )
        self.assertEqual(self.pregen["ctov:pillager_outpost_mesa"]["historical_set_ids"],
                         "NONE_IN_HISTORICAL_INDEX")
        self.assertEqual(self.critical["minecraft:end_city"]["live_DD_allowed"], "NO")

    def test_five_site_matcher_is_type_regex_only(self):
        difficulty = [t for t in self.candidate["difficulty_types"]
                      if t["name"] in {"ao_tier_" + str(n) for n in range(2, 7)}]
        self.assertEqual(len(difficulty), 5)
        expressions = {t["entities"][0]["entity_matches"]["type"] for t in difficulty}
        self.assertEqual(len(expressions), 1)
        for tier in difficulty:
            self.assertEqual(tier["entities"][0]["entity_matches"]["attitude"], "HOSTILE")
        regex = re.compile(next(iter(expressions))[1:])
        self.assertEqual(len(self.matcher), 8)
        self.assertEqual(len({row["site"] for row in self.matcher}), 5)
        for row in self.matcher:
            expected = "YES" if regex.fullmatch(row["entity_id"]) else "NO"
            self.assertEqual(row["regex_match"], expected, row["entity_id"])
            self.assertEqual(row["native_placement_tested"], "NO")
            self.assertEqual(row["attitude_checked"], "NO")
        self.assertEqual(sum(x["regex_match"] == "YES" for x in self.matcher), 3)


if __name__ == "__main__":
    unittest.main()
