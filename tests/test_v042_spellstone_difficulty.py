"""Source and native path regression for user's 2026-10-11 slot + dungeon reports."""
import json,re,unittest
from pathlib import Path
from tools.package_v042_manyfix import DEST,VERSION
from tools.validate_ao_balance_lab import check_config
R=Path(__file__).resolve().parents[1]

class SpellstoneDungeonDifficulty(unittest.TestCase):
    def test_original_spellstone_and_amulet_preserved_without_duplicate_slot(self):
        base=R/"release_030/overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots"
        assert json.loads((base/"spellstone.json").read_text())=={
            "size":1,"operation":"SET","replace":False,
            "icon":"enigmaticlegacyplus:slot/empty_spellstone_slot"
        }
        assert json.loads((base/"amulet.json").read_text())=={
            "size":1,"operation":"SET","replace":False
        }
        comp=(R/"compile_compatibility_031.py").read_text()
        assert "spellstone_slot.write_text(" in comp
        assert "amulet_slot.write_text(" in comp
        assert "enigmaticlegacyplus:slot/empty_spellstone_slot" in comp
        assert 'spellstone_slot = DATAPACK / ' in comp

    def test_dungeon_difficulty_actual_native_config_path_and_six_zones(self):
        self.assertEqual(DEST,"overrides/config/dungeon_difficulty/difficulty_v2.json")
        self.assertEqual(VERSION,"0.4.2-experimental-spellstone-difficulty")
        c=json.loads((R/"experiments/ao-balance-lab/config/dungeon_difficulty_v2.json").read_text())
        self.assertTrue(check_config(c))
        self.assertEqual(len(c["dimensions"][0]["zones"]),6)
        pattern=c["difficulty_types"][0]["entities"][0]["entity_matches"]["type"][1:]
        p=re.compile(pattern,re.IGNORECASE)
        for ordinary in ("minecraft:zombie","minecraft:pillager",
                         "illagerinvasion:alchemist","born_in_chaos_v1:fallen_zombie"):
            self.assertTrue(p.fullmatch(ordinary),ordinary)
        for boss in ("minecraft:wither","minecraft:ender_dragon",
                     "cataclysm:netherite_monstrosity",
                     "irons_spellbooks:dead_king",
                     "born_in_chaos_v1:nightmare_boss"):
            self.assertFalse(p.fullmatch(boss),boss)

    def test_deferred_difficulty_evaluation_never_force_heals_entities(self):
        s=(R/"addons/ao-worldgen-safety/src/main/java/dev/ambientodyssey/worldgensafety/DungeonDifficultyDeferredEvaluation.java").read_text()
        assert "Class.forName(SCALER)" in s
        assert "markEvaluated" in s
        assert "if (deltaTicks == 10" in s
        assert "isSameThread()" in s
        assert "MobCategory.MONSTER" in s
        assert "setHealth(" not in s
        assert "setBaseValue(" not in s
        t=(R/"addons/ao-worldgen-safety/src/main/java/dev/ambientodyssey/worldgensafety/WorldgenSafety.java").read_text()
        assert 'isLoaded("dungeon_difficulty")' in t
        assert "DungeonDifficultyDeferredEvaluation.register()" in t

if __name__=="__main__":unittest.main()
