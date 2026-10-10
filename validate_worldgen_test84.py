#!/usr/bin/env python3
"""Static regression gates for AO Test8.4 prefreeze worldgen candidate.

Run from repository root: python validate_worldgen_test84.py
This is JSON/source validation, NOT a Minecraft worldgen acceptance test.
"""
from fractions import Fraction
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release_030"
PACKS = RELEASE / "overrides/config/paxi/datapacks"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def verify():
    checks = []
    def require(name, condition):
        assert condition, name
        checks.append(name)

    require("test8.4 manifest version label", load(RELEASE / "release-lock.json")["version"] in ("0.3.8-worldgen-prefreeze-test1.4", "0.3.8-worldgen-prefreeze-test1.5", "0.3.8-worldgen-prefreeze-test1.6", "0.3.8-worldgen-prefreeze-test1.7", "0.3.8-worldgen-prefreeze-test1.8", "0.3.8-worldgen-prefreeze-test1.9", "0.3.8-worldgen-prefreeze-test1.10", "0.4.0-a0-qol-quest-trial", "0.4.0-b1-living-world-batch", "0.4.0-c0-ecosystem-feedback", "0.4.0-d0-content-first"))
    pool = load(RELEASE / "biome-pools.json")
    roster = load(RELEASE / "biome-roster.json")
    compiled = load(PACKS / "ao_biome_replacement/data/ambient_odyssey/biolith/biome_placement.json")
    native = {f"{namespace}:{b}" for namespace, names in roster.items() for b in names}
    require("unchanged 8 replacement pools", len(pool["pools"]) == 8)
    require("unchanged 53 compiled placement replacements", len(compiled["replacements"]) == 53)
    require("unchanged 20 compiled climate guards", len(compiled["sub_biomes"]) == 20)
    expected = []
    for p in pool["pools"]:
        weights = {k: Fraction(str(v)) for k, v in p["biomes"].items()}
        require(p["name"] + " donor membership", set(weights).issubset(native))
        f = {b: w / sum(weights.values()) for b, w in weights.items()}
        vanilla = Fraction(str(p["vanilla_percent"])) / 100
        denominator = max(f.values()) + vanilla / (1 - vanilla)
        for target in p["targets"]:
            for biome, fraction in f.items():
                expected.append({"dimension": pool["dimension"], "target": target, "biome": biome,
                                 "proportion": round(float(fraction / denominator), 12)})
    require("compiled Biolith rules exactly match canonical pools", expected == compiled["replacements"])
    pmap = {p["name"]: p for p in pool["pools"]}
    require("prairie reductions match review", [pmap[k]["biomes"]["biomeswevegone:prairie"] for k in ("plains","savanna","windswept_savanna")] == [14, 18, 14])
    guard_map = {tuple(g["targets"]): g for g in pool["climate_guards"]}
    require("Skyris warm fallback no longer Prairie", guard_map[("biomeswevegone:skyris_vale",)]["biome"] == "regions_unexplored:grassland")
    floral_guard = [g for g in pool["climate_guards"] if g["targets"] == ["natures_spirit:floral_ridges"] and g["temperature"].get("min", 0) >= .55]
    require("hot floral fallback selects baobab", len(floral_guard) == 1 and floral_guard[0]["biome"] == "biomeswevegone:baobab_savanna")

    preset = load(RELEASE / "overrides/config/freeterraforged/presets/Ambient Odyssey 0.3.1.json")
    require("mountain variety within 0..1", preset["terrain"]["general"]["mountainVariety"] == .9)
    require("mountain-only scale adjusted", preset["terrain"]["mountains"]["verticalScale"] == 1.35)
    require("FTF unchanged broad relief", preset["terrain"]["general"]["globalVerticalScale"] == .6)
    require("FTF unchanged sea and bounds", (preset["world"]["properties"]["seaLevel"], preset["world"]["properties"]["worldHeight"]) == (63, 512))

    ice = load(RELEASE / "overrides/config/iceandfire/iaf-common.json")["worldgen"]
    require("all three underground dragon caves 0.72", all(ice[f"generate{d}DragonCaveChance"] == .72 for d in ("Fire","Ice","Lightning")))
    require("dragon surface roosts unchanged", all(ice[f"generate{d}DragonRoostChance"] == .5 for d in ("Fire","Ice","Lightning")))
    require("dangerous worldgen spawn protection unchanged", ice["dangerousDistanceLimit"] == 1000)
    final = PACKS / "ao_worldgen_final_fixes"
    require("loaded-compatible 1.21.1 datapack", load(final / "pack.mcmeta")["pack"]["pack_format"] == 48)
    for suffix, count in (("rooms", 10), ("rooms_x", 7)):
        p = final / f"data/archaion/worldgen/template_pool/ancient_keep/{suffix}.json"
        elements = load(p)["elements"]
        require(suffix + " valid remaining rooms", len(elements) == count and all(e["weight"] > 0 and e["element"]["element_type"] == "minecraft:single_pool_element" for e in elements))
        require(suffix + " excludes corrupt empty-NBT rooms", not any("misc_room" in e["element"]["location"] for e in elements))
    print(f"PASS: {len(checks)} Test8.4 static source/regeneration checks.")
    print("NOT TESTED: Minecraft launcher, random seeds, heights, cave frequency, jigsaw assembly, performance.")
if __name__ == "__main__":
    verify()
