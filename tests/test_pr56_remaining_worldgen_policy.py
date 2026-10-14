"""Safety checks for PR56 non-firewatch removed-biome source findings.

Checks repo-source invariants from SHA1-pinned PR50 native archives and
the AO Paxi snapshot. Not a claim of runtime datapack priority, natural
generation or final approved biome-selection policy.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"docs/balance/DD_ADVENTURE_LUKI_PASTERDREAM_PINNED_NATIVE_20261014.json"
AO_PAXI=ROOT/"release_030/overrides/config/paxi/datapacks"
CURATED=ROOT/"docs/audits/CURRENT_BIOME_ROSTER.json"

class PR56NativeWorldgenSourcePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.p=cls.report["providers"]

    def test_sha1_pinned_sources_and_no_runtime_claims(self):
        pins={"adventuredungeons":"706092299886721473b0ef7d5e4f7aa2a073c8de",
              "lukis":"a07986ac59268f1343737b81acd24ad34e5371ca",
              "pasterdream":"d5d95c8a049d868a844132ac1e47261eff0067f8"}
        self.assertEqual(set(self.p),set(pins))
        for key,sha in pins.items():
            with self.subTest(provider=key):
                row=self.p[key]
                self.assertEqual(row["verified_sha1"],sha)
                self.assertFalse(row["actual_game_runtime_tested"])
                self.assertFalse(row["effective_external_tag_resolution_tested"])
                self.assertTrue(row["no_worldgen_files_changed"])
                self.assertFalse(row["target_ids_missing_exact_native_structure_json"])

    def test_AO_village_set_does_not_revert_to_lukis_native_values(self):
        source=self.p["lukis"]["selected_sets"]["minecraft:villages"]["source_content"]
        native=source["placement"]
        path=AO_PAXI/"ao_structure_density/data/minecraft/worldgen/structure_set/villages.json"
        current=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(native["spacing"],50)
        self.assertEqual(native["separation"],35)
        self.assertEqual(current["placement"]["spacing"],36)
        self.assertEqual(current["placement"]["separation"],8)
        self.assertEqual(current["placement"]["salt"],10387312)
        self.assertEqual(
            {x["structure"] for x in current["structures"]},
            {x["structure"] for x in source["structures"]},
        )
        source_snapshot=self.p["lukis"]["native_vs_AO_village_structure_set"]
        self.assertTrue(source_snapshot["preserve_existing_AO_override_no_auto_reversion"])
        self.assertFalse(source_snapshot["profile_runtime_resource_winner_verified"])
        self.assertEqual(source_snapshot["AO_Paxi_source_overrides"][0]["pack"],"ao_structure_density")
        self.assertEqual(source_snapshot["AO_Paxi_source_overrides"][0]["placement"],current["placement"])

    def test_adventure_camp_source_uses_external_pillager_outpost_tag(self):
        structure=self.p["adventuredungeons"]["selected_structures"][
            "adventuredungeons:underground_camp"]["source_content"]
        self.assertEqual(structure["biomes"],"#minecraft:has_structure/pillager_outpost")
        self.assertEqual(structure["type"],"minecraft:jigsaw")
        native_set=self.p["adventuredungeons"]["selected_sets"][
            "adventuredungeons:underground_camp"]["source_content"]
        self.assertEqual(native_set["placement"]["spacing"],35)
        self.assertEqual(native_set["placement"]["separation"],12)
        self.assertFalse(self.p["adventuredungeons"]["AO_Paxi_source_override_candidates"])

    def test_pasterdream_named_picnic_biomes_have_source_json(self):
        picnic=self.p["pasterdream"]["selected_structures"][
            "pasterdream:picnic_basket_structure"]["source_content"]
        clover=self.p["pasterdream"]["selected_structures"][
            "pasterdream:fourleaf_clover_plant"]["source_content"]
        self.assertEqual(clover["biomes"],"plains")
        self.assertEqual(len(picnic["biomes"]),5)
        self.assertEqual(picnic["biomes"][0],"plains")
        named=self.p["pasterdream"]["pasterdream_referenced_native_biome_files"]
        self.assertEqual(set(named),set(picnic["biomes"][1:]))
        self.assertTrue(all(r["native_biome_json_present"] and
                            not r["runtime_dimension_and_registration_verified"] for r in named.values()))

    def test_shared_c_is_plains_not_same_as_c_plains(self):
        native_yung=json.loads((ROOT/"docs/balance/DD_YUNGS_MINE_SHAFT_NATIVE_BIOME_SOURCE_20261014.json").read_text(encoding="utf-8"))
        oak=native_yung["target_results"]["bettermineshafts:mineshaft_oak"]
        self.assertIn("c:plains",oak["unresolved_nested_native_tags"])
        tag=AO_PAXI/"ao_compatibility/data/c/tags/worldgen/biome/is_plains.json"
        self.assertTrue(tag.exists())
        self.assertFalse((AO_PAXI/"ao_compatibility/data/c/tags/worldgen/biome/plains.json").exists())
        self.assertNotEqual("c:plains","c:is_plains")


if __name__=="__main__":
    unittest.main()
