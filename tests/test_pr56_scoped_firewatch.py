"""PR56 source-verified *isolated* four-firewatch-tower datapack safety.

This test reads the retained audit of the exact SHA1-pinned D&T v4.4.4
NeoForge JAR. A separate GitHub Actions native-JAR job independently
rechecks every field against a fresh download of that same pinned archive.
Neither test proves live Paxi priorities or natural placement.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DRAFT=ROOT/"experiments/structure-biome-compatibility/firewatch-structure-only-draft"
EVIDENCE=ROOT/"docs/balance/DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json"
CURATED=ROOT/"docs/audits/CURRENT_BIOME_ROSTER.json"
NAMES=("birch","cherry","forest","savanna")


class PR56IsolatedFirewatchSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence=json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.roster=json.loads(CURATED.read_text(encoding="utf-8"))
        cls.allowed={namespace+":"+b for namespace,biomes in cls.roster.items() for b in biomes}

    def test_exact_file_count_and_no_shared_collection_tag_mutation(self):
        self.assertEqual(self.evidence["sha1"],"249a5bdd0e8622b8a11f88758e6f5fd5fda036a3")
        self.assertEqual(self.evidence["native_structure_json_count"],96)
        pack=json.loads((DRAFT/"pack.mcmeta").read_text(encoding="utf-8"))
        self.assertEqual(pack["pack"]["pack_format"],48)
        self.assertIn("DRAFT",pack["pack"]["description"])
        data={p.relative_to(DRAFT).as_posix() for p in DRAFT.rglob("*.json")}
        expected={
            f"data/nova_structures/worldgen/structure/firewatch_tower_{suffix}.json"
            for suffix in NAMES
        }|{
            f"data/ambient_odyssey/tags/worldgen/biome/firewatch_compatible/{suffix}.json"
            for suffix in NAMES
        }
        self.assertEqual(data,expected)
        self.assertFalse(any("/worldgen/structure_set/" in item for item in data))
        self.assertFalse(any("/nova_structures/tags/" in item for item in data))
        self.assertFalse((ROOT/"release_030/overrides/config/paxi/datapacks/firewatch-structure-only-draft").exists())

    def test_all_four_fields_source_faithful_except_biomes(self):
        originals=self.evidence["four_original_native_structure_json"]
        for suffix in NAMES:
            with self.subTest(suffix=suffix):
                original=originals[suffix]
                actual=json.loads((DRAFT/f"data/nova_structures/worldgen/structure/firewatch_tower_{suffix}.json").read_text(encoding="utf-8"))
                expected=dict(original)
                expected["biomes"]="#ambient_odyssey:firewatch_compatible/"+suffix
                self.assertEqual(actual,expected)
                self.assertEqual(actual["start_pool"],original["start_pool"])
                self.assertEqual(actual["step"],original["step"])
                self.assertEqual(actual["type"],"minecraft:jigsaw")

    def test_new_private_biome_tags_preserve_origins_and_curated_ids(self):
        original=self.evidence["four_original_native_structure_json"]
        for suffix in NAMES:
            with self.subTest(suffix=suffix):
                path=DRAFT/f"data/ambient_odyssey/tags/worldgen/biome/firewatch_compatible/{suffix}.json"
                data=json.loads(path.read_text(encoding="utf-8"))
                self.assertFalse(data.get("replace",False))
                originals=original[suffix]["biomes"]
                anchor=originals if isinstance(originals,str) else originals[0]
                self.assertEqual(data["values"][0],anchor)
                self.assertGreaterEqual(len(data["values"]),2)
                self.assertEqual(len(data["values"]),len(set(data["values"])))
                self.assertTrue(all(x in self.allowed for x in data["values"][1:]))

    def test_source_shared_tag_consumers_show_why_old_bridge_is_blocked(self):
        for tag,at_least in (("birch_forests",22),("cherry_forests",19),("savannas",20)):
            row=self.evidence["candidate_tag_analysis"][tag]
            self.assertGreaterEqual(len(row["transitive_structure_consumers"]),at_least)
            self.assertIn("nova_structures:collections/land",row["transitive_tag_keys"])
        self.assertEqual(len(self.evidence["land_collection_direct_structure_consumers"]),17)


if __name__=="__main__":
    unittest.main()
