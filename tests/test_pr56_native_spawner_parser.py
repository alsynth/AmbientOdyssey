"""Fast parser regressions for read-only PR56 native jigsaw/NBT source audit.

Synthetic NBT structures protect against treating equipment as mob entity IDs.
Nothing here proves a live Minecraft entity-spawn event.
"""
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/audit_pr56_native_template_spawners.py"
spec=importlib.util.spec_from_file_location("audit_pr56_native_template_spawners",SCRIPT)
scan=importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)

class NativeSourceParserSafety(unittest.TestCase):
    def test_pools_follow_weighted_single_and_list_elements(self):
        pool={"elements":[
            {"weight":3,"element":{"element_type":"minecraft:single_pool_element","location":"dungeons_arise:some/spawner"}},
            {"weight":1,"element":{"element_type":"minecraft:list_pool_element","elements":[
                {"element_type":"minecraft:legacy_single_pool_element","location":"dungeons_arise:some/hall"}]}},
        ]}
        self.assertEqual(scan.pool_elements(pool),["dungeons_arise:some/hall","dungeons_arise:some/spawner"])

    def test_spawner_entity_not_item_ids(self):
        root={"palette":[{"Name":"minecraft:spawner"},{"Name":"minecraft:jigsaw"}],
              "blocks":[
                  {"state":0,"nbt":{
                      "SpawnData":{"entity":{"id":"minecraft:pillager","HandItems":[{"id":"minecraft:diamond_sword"}]}},
                      "SpawnPotentials":[{"data":{"entity":{"id":"minecraft:zombie",
                                             "ArmorItems":[{"id":"minecraft:netherite_chestplate"}]}}}],
                      "id":"minecraft:mob_spawner",
                      "Items":[{"id":"minecraft:diamond_axe"}]}},
                  {"state":1,"nbt":{"pool":"dungeons_arise:more/spawners"}}]}
        parsed=scan.extract_template(root)
        self.assertEqual(parsed["normal_spawners"],1)
        self.assertEqual(parsed["trial_spawners"],0)
        self.assertEqual(parsed["normal_spawn_entity_ids"],["minecraft:pillager","minecraft:zombie"])
        self.assertEqual(parsed["jigsaw_child_pools"],["dungeons_arise:more/spawners"])
        for item in ("minecraft:diamond_sword","minecraft:netherite_chestplate",
                     "minecraft:mob_spawner","minecraft:diamond_axe"):
            self.assertNotIn(item,parsed["normal_spawn_entity_ids"])

    def test_trial_spawner_does_not_get_classified_normal(self):
        j={"palette":[{"Name":"minecraft:trial_spawner"}],
           "blocks":[{"state":0,"nbt":{
               "normal_config":{"spawn_potentials":[{"data":{"entity":{"id":"minecraft:skeleton"}}}]},
               "ominous_config":{"spawn_potentials":[{"data":{"entity":{"id":"minecraft:breeze"}}}]}}}]}
        o=scan.extract_template(j)
        self.assertEqual(o["normal_spawners"],0)
        self.assertEqual(o["trial_spawners"],1)
        self.assertEqual(o["trial_spawn_entity_ids"],["minecraft:breeze","minecraft:skeleton"])

    def test_nbt_truncated_and_unknown_tag_rejected(self):
        with self.assertRaises(ValueError):
            scan.nbt_from_bytes(b"\x0a\x00\x00\x03\x00\x04hello")
        with self.assertRaises(ValueError):
            scan.nbt_from_bytes(b"\x0d\x00\x00")

if __name__=="__main__":
    unittest.main()
