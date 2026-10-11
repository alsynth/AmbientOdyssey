"""Static conversion guards for exact-source Mine Cells 2.0.3 1.21.1 recipes."""
import unittest
from tools.generate_v042_minecells_recipes import convert,validate

class MinecellsCodecBridgeTests(unittest.TestCase):
    def test_create_crushing_preserves_bonus_chance_and_native_vanilla_id(self):
        old={"fabric:load_conditions":[{"condition":"fabric:all_mods_loaded","values":["create"]}],
             "type":"create:crushing","processingTime":50,
             "ingredients":[[{"item":"minecells:corpse"},{"item":"minecells:rotting_corpse"}]],
             "results":[{"item":"rotten_flesh","count":6},
                        {"item":"bone","chance":0.25,"count":4},
                        {"item":"bone_meal","count":2,"chance":0.25}]}
        new=convert(old);validate(old,new)
        self.assertEqual(new["processing_time"],50)
        self.assertEqual([x["id"] for x in new["results"]],
                         ["minecraft:rotten_flesh","minecraft:bone","minecraft:bone_meal"])
        self.assertEqual(new["results"][1]["chance"],0.25)
        self.assertEqual(len(new["ingredients"][0]),2)

    def test_create_filling_fabric_bucket_to_neoforge_single(self):
        old={"fabric:load_conditions":[{"condition":"fabric:all_mods_loaded","values":["create"]}],
             "type":"create:filling",
             "ingredients":[{"item":"bucket"},{"amount":81000,"fluid":"minecells:sewage"}],
             "results":[{"item":"minecells:sewage_bucket"}]}
        new=convert(old);validate(old,new)
        self.assertEqual(new["ingredients"][1],{"type":"neoforge:single","amount":1000,"fluid":"minecells:sewage"})
        self.assertEqual(new["ingredients"][0]["item"],"minecraft:bucket")

    def test_farmer_cutting_uses_1211_tool_and_result_codecs(self):
        old={"fabric:load_conditions":[{"condition":"fabric:all_mods_loaded","values":["farmersdelight"]}],
             "type":"farmersdelight:cutting","ingredients":[{"item":"minecells:putrid_log"}],
             "tool":{"type":"farmersdelight:tool","tag":"c:tools/axes"},
             "result":[{"item":"minecells:stripped_putrid_log"},{"item":"farmersdelight:tree_bark"}],
             "sound":"minecraft:item.axe.strip"}
        new=convert(old);validate(old,new)
        self.assertEqual(new["tool"][0],{"type":"farmersdelight:item_ability","action":"axe_strip"})
        self.assertEqual(new["result"][0]["item"],{"id":"minecells:stripped_putrid_log","count":1})
        self.assertEqual(new["sound"],{"sound_id":"minecraft:item.axe.strip"})

    def test_fails_on_unknown_invented_conditions(self):
        with self.assertRaises(AssertionError):
            convert({"type":"create:crushing","fabric:load_conditions":[],
                     "ingredients":[{"item":"minecells:cage"}],
                     "results":[{"item":"minecells:broken_cage"}]})

    def test_fails_on_unknown_fabric_fluid_amount(self):
        with self.assertRaises(AssertionError):
            convert({"type":"create:filling",
                     "fabric:load_conditions":[{"condition":"fabric:all_mods_loaded","values":["create"]}],
                     "ingredients":[{"item":"bucket"},{"fluid":"minecells:sewage","amount":90000}],
                     "results":[{"item":"minecells:sewage_bucket"}]})
if __name__=="__main__":unittest.main()
