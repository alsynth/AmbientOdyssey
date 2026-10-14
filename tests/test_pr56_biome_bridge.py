"""Static safety checks for the *inactive* PR56 curated-biome firewatch draft.

Run via `python -m unittest discover -s tests -p 'test_pr56_*.py' -v`.
Passing is NOT Minecraft/Paxi runtime or proof of structure natural placement.
"""
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "experiments" / "structure-biome-compatibility" / "firewatch-tag-bridge-draft"
ROSTER = ROOT / "docs" / "audits" / "CURRENT_BIOME_ROSTER.json"
BIOLITH = ROOT / "docs" / "audits" / "CURRENT_BIOLITH_PLACEMENT.json"
COMPAT = ROOT / "release_030" / "overrides" / "config" / "paxi" / "datapacks"

PROPOSALS = {
    "birch_forests": {
        "biomeswevegone:sakura_grove",
        "biomeswevegone:zelkova_forest",
        "regions_unexplored:maple_forest",
    },
    "cherry_forests": {
        "biomeswevegone:sakura_grove",
        "biomesoplenty:snowblossom_grove",
    },
    "savannas": {
        "biomeswevegone:prairie",
        "regions_unexplored:grassland",
        "natures_spirit:floral_ridges",
    },
}


class PR56FirewatchBiomeBridgeSafety(unittest.TestCase):
    def test_data_pack_is_valid_1211_and_isolated_from_active_paxi(self):
        pack = json.loads((DRAFT / "pack.mcmeta").read_text(encoding="utf-8"))
        self.assertEqual(pack["pack"]["pack_format"], 48)
        self.assertIn("EXPERIMENT", pack["pack"]["description"])
        self.assertFalse((COMPAT / DRAFT.name).exists())
        paths = {f.relative_to(DRAFT).as_posix() for f in DRAFT.rglob("*") if f.is_file()}
        expected = {"pack.mcmeta"} | {
            "data/nova_structures/tags/worldgen/biome/collections/" + name + ".json"
            for name in PROPOSALS
        }
        self.assertEqual(paths, expected)
        self.assertFalse(any("/worldgen/structure/" in f or "/worldgen/structure_set/" in f for f in paths))

    def test_proposed_collection_additions_only_use_curated_biomes(self):
        roster = json.loads(ROSTER.read_text(encoding="utf-8"))
        allowed = {prefix + ":" + biome for prefix, biomes in roster.items() for biome in biomes}
        for name, approved in PROPOSALS.items():
            path = DRAFT / "data/nova_structures/tags/worldgen/biome/collections" / (name + ".json")
            with self.subTest(tag=name):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIs(data["replace"], False)
                self.assertEqual(set(data["values"]), approved)
                self.assertEqual(len(data["values"]), len(approved))
                self.assertTrue(approved.issubset(allowed))
                self.assertFalse(any(v.startswith("#") or v.startswith("minecraft:") for v in approved))

    def test_direct_vanilla_firewatch_selectors_are_not_mistaken_for_tag_repairs(self):
        selectors = {}
        with (ROOT / "STRUCTURE_REGISTRY_CATALOG.csv").open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                selectors[row["structure_id"]] = row["biome_selector"]
        for suffix, vanilla in (("forest", "forest"), ("swamp", "swamp"),
                                ("mangrove", "mangrove_swamp")):
            key = "nova_structures:firewatch_tower_" + suffix
            with self.subTest(structure=key):
                self.assertEqual(json.loads(selectors[key]), ["minecraft:" + vanilla])
        targets = {x["target"] for x in json.loads(BIOLITH.read_text(encoding="utf-8"))["replacements"]}
        self.assertIn("minecraft:forest", targets)
        self.assertIn("minecraft:savanna", targets)
        self.assertNotIn("minecraft:swamp", targets)
        self.assertNotIn("minecraft:mangrove_swamp", targets)

    def test_intentional_dnt_birch_graveyard_exclusion_is_not_reenabled(self):
        original = (COMPAT / "ao_dnt_trek_curation/data/nova_structures/worldgen/structure/"
                    "remnant_birch_graveyard.json")
        self.assertEqual(
            json.loads(original.read_text(encoding="utf-8"))["biomes"],
            "#ambient_odyssey:dnt_trek_disabled",
        )


if __name__ == "__main__":
    unittest.main()
