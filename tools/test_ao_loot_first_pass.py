#!/usr/bin/env python3
"""Source-level safety checks for AO's unmerged starter-loot pilot.

These checks do NOT replace Gradle compilation or a real Lootr 2-player test.
"""
import importlib.util
import io
import json
import pathlib
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDON = ROOT / "addons/ao-starter-chest/src/main/resources"
RINGS = ROOT / "release_030/overrides/config/paxi/datapacks/ao_flight_balance/data/flight_rings/recipe"
TABLE = ADDON / "data/minecraft/loot_table/chests/spawn_bonus_chest.json"

def check():
    t = json.loads(TABLE.read_text())
    assert t["type"] == "minecraft:chest" and len(t["pools"]) == 3
    stones = t["pools"][0]["entries"]
    assert len(stones) == 5 and all(e["type"] == "minecraft:item" for e in stones)
    assert {e["name"] for e in stones} == {
        "enigmaticlegacyplus:blazing_core",
        "enigmaticlegacyplus:golem_heart",
        "enigmaticlegacyplus:ocean_stone",
        "enigmaticlegacyplus:angel_blessing",
        "enigmaticlegacyplus:lost_engine",
    }
    assert all(e.get("weight", 1) == 1 for e in stones)
    torch = t["pools"][1]["entries"]
    assert len(torch) == 1 and torch[0]["name"] == "minecraft:torch"
    assert torch[0]["functions"][0]["count"]["min"] == 32
    assert torch[0]["functions"][0]["count"]["max"] == 48
    meat = t["pools"][2]["entries"]
    assert {e["name"] for e in meat} == {
        "minecraft:cooked_beef", "minecraft:cooked_porkchop",
        "minecraft:cooked_chicken", "minecraft:cooked_mutton",
    }
    assert all(e["functions"][0]["count"]["min"] == 16
               and e["functions"][0]["count"]["max"] == 48 for e in meat)
    m = json.loads((ADDON / "data/neoforge/loot_modifiers/global_loot_modifiers.json").read_text())
    assert m["replace"] is False and "ao_starter_chest:starter_affix" in m["entries"]
    assert json.loads((ADDON / "data/ao_starter_chest/loot_modifiers/starter_affix.json").read_text())["type"] == "ao_starter_chest:starter_affix"
    basic = json.loads((RINGS / "basic_ring.json").read_text())
    assert basic["key"]["D"]["item"] == "minecraft:nether_star"
    advanced = json.loads((RINGS / "advanced_ring.json").read_text())
    assert advanced["pattern"] == ["ENE", "DAD", "IRI"]
    assert {k:v["item"] for k,v in advanced["key"].items()} == {
        "E":"minecraft:ender_eye", "N":"irons_spellbooks:cinder_essence",
        "D":"minecraft:netherite_ingot", "A":"flight_rings:basic_ring",
        "I":"irons_spellbooks:arcane_ingot", "R":"ars_nouveau:air_essence",
    }
    # Simulated Goblin JSON: the transformer must preserve output data and
    # all other trades while failing if special components are missing.
    p = ROOT / "tools/build_ao_goblin_tuned_trade_override.py"
    spec = importlib.util.spec_from_file_location("ao_goblin", p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    armor = ["helmet", "chestplate", "leggings", "boots"]
    def mock(part):
        return {"offer_item": {
                    "id":f"minecraft:chainmail_{part}",
                    "components":{"minecraft:attribute_modifiers":{"modifiers":[]},
                                  "minecraft:max_damage":123,
                                  "minecraft:lore":[]}},
                "payment_item":{"id":"minecraft:iron_ingot","count":2},
                "secondary_payment_item":{"id":"minecraft:emerald","count":7},
                "max_trades":1}
    sample = {"trades":[mock(part) for part in armor]+[{"offer_item":{"id":"minecraft:apple"}, "payment_item":{"id":"minecraft:emerald"}}]}
    result = module.transform(sample)
    assert len(result["trades"]) == 5
    for trade in result["trades"][:4]:
        assert trade["payment_item"] == {"id":"minecraft:diamond","count":32}
        assert trade["secondary_payment_item"] == {"id":"irons_spellbooks:cinder_essence","count":4}
        assert "minecraft:attribute_modifiers" in trade["offer_item"]["components"]
    assert result["trades"][-1]["offer_item"]["id"] == "minecraft:apple"
    native_override = ROOT / "release_030/overrides/config/paxi/datapacks/ao_goblin_trades/data/goblintraders/goblin_trades/goblin_trader/epic.json"
    native = json.loads(native_override.read_text())
    assert native.get("replace") is False and len(native["trades"]) == 22
    tuned = [x for x in native["trades"] if x.get("offer_item", {}).get("id") in {
        f"minecraft:chainmail_{part}" for part in ("helmet", "chestplate", "leggings", "boots")
    }]
    assert len(tuned) == 4
    for offer in tuned:
        assert offer["payment_item"] == {"id":"minecraft:diamond","count":32}
        assert offer["secondary_payment_item"] == {"id":"irons_spellbooks:cinder_essence","count":4}
        assert offer["max_trades"] == 1
        assert "minecraft:attribute_modifiers" in offer["offer_item"]["components"]
        assert "minecraft:max_damage" in offer["offer_item"]["components"]
    assert json.loads((native_override.parents[4] / "pack.mcmeta").read_text())["pack"]["pack_format"] == 48

    print("AO loot source checks passed: ring recipes, three starter pools, affix modifier definition and synthetic and pinned-native Goblin trade transform.")
    print("NOT TESTED: live native Goblin JAR output, compilation, real Apotheosis affix rolls, Lootr / Minecraft runtime.")

if __name__ == "__main__":
    check()
