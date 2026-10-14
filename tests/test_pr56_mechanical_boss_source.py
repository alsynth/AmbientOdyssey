"""PR56 native boss-signal probe: synthetic only, no boss identity inference."""
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("audit_pr56_mechanical_boss_foundry",ROOT/"tools/audit_pr56_mechanical_boss_foundry.py")
scan=importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)


class NativeBossSourceSafety(unittest.TestCase):
    def test_named_spawner_signal_only_when_native_named(self):
        template={
          "palette":[{"Name":"minecraft:spawner"},{"Name":"minecraft:stone"}],
          "blocks":[
            {"state":0,"pos":[4,64,4],"nbt":{
                "SpawnData":{"entity":{"id":"minecraft:ravager","CustomName":'{"text":"Guardian"}',
                    "Attributes":[{"Name":"minecraft:generic.max_health","Base":220}],
                    "ArmorItems":[{"id":"minecraft:diamond_chestplate"}]}}
            }},
            {"state":1,"pos":[0,0,0],"nbt":{"CustomName":'{"text":"Decoration"}'}}
          ]}
        counts,records=scan.summarize_nbt(template,"test_structure.nbt")
        self.assertEqual(counts["minecraft:spawner"],1)
        self.assertEqual(len(records),1)
        self.assertEqual(records[0]["spawn_entities"][0]["entity_id"],"minecraft:ravager")
        self.assertIn("CustomName",records[0]["spawn_entities"][0]["unusual_entity_markers"])
        self.assertIn("Attributes",records[0]["spawn_entities"][0]["unusual_entity_markers"])
        self.assertNotIn("minecraft:diamond_chestplate",str(records[0]["spawn_entities"][0]["entity_id"]))

    def test_generic_spawner_is_not_boss_proof(self):
        src={"palette":[{"Name":"minecraft:spawner"}],
             "blocks":[{"state":0,"nbt":{"SpawnData":{"entity":{"id":"minecraft:skeleton"}}}}]}
        c,records=scan.summarize_nbt(src,"ordinary.nbt")
        self.assertEqual(c["minecraft:spawner"],1)
        self.assertEqual(records[0]["spawn_entities"][0]["unusual_entity_markers"],{})

    def test_jigsaw_child_pool_reference_is_reported_not_automatically_fixed(self):
        obj={"palette":[{"Name":"minecraft:jigsaw"}],
             "blocks":[{"state":0,"pos":[1,2,3],
                        "nbt":{"pool":"dungeons_arise:underworld/foundry/foundry_corridor_gears"}}]}
        counters,flags=scan.summarize_nbt(obj,"foundry_bridge.nbt")
        self.assertEqual(counters["minecraft:jigsaw"],1)
        self.assertEqual(len(flags),1)
        self.assertEqual(flags[0]["jigsaw_pool_reference"],
                         "dungeons_arise:underworld/foundry/foundry_corridor_gears")

    def test_explicit_custom_name_is_distinct_from_default_health_and_attributes(self):
        default=scan.summarize_entity({"id":"minecraft:creeper","Health":20.0,
                                      "Attributes":[{"Name":"minecraft:generic.max_health","Base":20}]})
        named=scan.summarize_entity({"id":"minecraft:blaze",
                                    "CustomName":'{"text":"Foundry Guardian"}',
                                    "Health":55.0})
        self.assertNotIn("CustomName",default["unusual_entity_markers"])
        self.assertEqual(named["unusual_entity_markers"]["Health"],55.0)
        self.assertIn("Foundry Guardian",named["unusual_entity_markers"]["CustomName"])

    def test_mount_is_preserved_but_not_promoted_to_boss(self):
        source={"SpawnPotentials":[{"data":{"entity":{
            "id":"minecraft:ravager","Passengers":[{"id":"minecraft:creeper"}]}}}]}
        entities=scan.entity_payloads(source)
        self.assertEqual(len(entities),1)
        summary=scan.summarize_entity(entities[0])
        self.assertEqual(summary["entity_id"],"minecraft:ravager")
        self.assertEqual(summary["passengers"][0]["id"],"minecraft:creeper")
        self.assertEqual(summary["unusual_entity_markers"],{})

if __name__=="__main__":
    unittest.main()
