#!/usr/bin/env python3
"""Fail-closed validation of AO World Tier rarity weight overrides vs pinned Apotheosis 8.9.0.

Only seven approved per-tier weight integers may differ from official installed rarity data.
Rarity rules, colors, attributes, all quality coefficients, and all other data are preserved.
No gameplay/loot drop-rate claims are made by this static comparison.
"""
import argparse
import copy
import json
from pathlib import Path
import zipfile

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "release_030/overrides/config/paxi/datapacks/ao_world_tier_balance"
RARITIES = ("common", "uncommon", "rare", "epic", "mythic")
TIERS = ("haven", "frontier", "ascent", "summit", "pinnacle")
OVERRIDES = {
    "uncommon": {"ascent": 350, "summit": 150},
    "rare": {"summit": 500, "pinnacle": 200},
    "epic": {"ascent": 50, "summit": 300},
    "mythic": {"pinnacle": 150},
}
BASELINE_WEIGHTS = {
    "haven": {"common": 600, "uncommon": 360, "rare": 40, "epic": 0, "mythic": 0},
    "frontier": {"common": 290, "uncommon": 600, "rare": 100, "epic": 10, "mythic": 0},
    "ascent": {"common": 100, "uncommon": 300, "rare": 500, "epic": 100, "mythic": 0},
    "summit": {"common": 0, "uncommon": 120, "rare": 290, "epic": 540, "mythic": 50},
    "pinnacle": {"common": 0, "uncommon": 0, "rare": 100, "epic": 650, "mythic": 250},
}
EXPECTED = {
    "haven": {"common": 600, "uncommon": 360, "rare": 40, "epic": 0, "mythic": 0},
    "frontier": {"common": 290, "uncommon": 600, "rare": 100, "epic": 10, "mythic": 0},
    "ascent": {"common": 100, "uncommon": 350, "rare": 500, "epic": 50, "mythic": 0},
    "summit": {"common": 0, "uncommon": 150, "rare": 500, "epic": 300, "mythic": 50},
    "pinnacle": {"common": 0, "uncommon": 0, "rare": 200, "epic": 650, "mythic": 150},
}

def validate(jar_path: Path) -> None:
    with zipfile.ZipFile(jar_path) as jar:
        available = set(jar.namelist())
        expected_paths = {
            "data/apotheosis/rarities/" + rarity + ".json" for rarity in RARITIES
        }
        missing = expected_paths - available
        if missing:
            raise ValueError("Missing pinned rarity definition(s) in JAR: " + ", ".join(sorted(missing)))
        native = {}
        actual = {}
        for rarity in RARITIES:
            resource = "data/apotheosis/rarities/" + rarity + ".json"
            orig = json.loads(jar.read(resource))
            native[rarity] = orig
            custom = ROOT / resource
            if rarity in OVERRIDES:
                if not custom.is_file():
                    raise ValueError("Missing required override: " + str(custom))
                overwritten = json.loads(custom.read_text(encoding="utf-8"))
                expect = copy.deepcopy(orig)
                for tier, weight in OVERRIDES[rarity].items():
                    if tier not in expect.get("weights", {}) or not isinstance(expect["weights"][tier].get("weight"), int):
                        raise ValueError("Unexpected native rarity weight shape: " + rarity + " " + tier)
                    expect["weights"][tier]["weight"] = weight
                if overwritten != expect:
                    raise ValueError("Non-approved modifications detected: " + resource)
                actual[rarity] = overwritten
            else:
                if custom.exists():
                    raise ValueError("Haven/common rarity override forbidden: " + str(custom))
                actual[rarity] = orig

        for tier in TIERS:
            before = {rarity: native[rarity]["weights"][tier]["weight"] for rarity in RARITIES}
            after = {rarity: actual[rarity]["weights"][tier]["weight"] for rarity in RARITIES}
            if before != BASELINE_WEIGHTS[tier]:
                raise ValueError(f"Pinned default {tier} diverged: {before}; inspect installed JAR")
            if after != EXPECTED[tier]:
                raise ValueError(f"Unexpected target {tier} weights: {after}")
            if sum(after.values()) != 1000:
                raise ValueError(f"Unexpected {tier} weight total: {sum(after.values())}")
            print(f"{tier:8} "+", ".join(f"{r}={after[r]/10:g}%" for r in RARITIES))
        pkg = json.loads((ROOT / "pack.mcmeta").read_text(encoding="utf-8"))
        if pkg.get("pack", {}).get("pack_format") != 48:
            raise ValueError("Expected Minecraft 1.21.1 pack_format 48")
        files = {p.name for p in (ROOT / "data/apotheosis/rarities").glob("*.json")}
        if files != {r + ".json" for r in OVERRIDES}:
            raise ValueError(f"Unexpected override rarity file set: {files}")
        print("PASS: 7 approved weight edits only; all pinned native rarity content, rules and quality retained.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pinned_apotheosis_jar", type=Path)
    args = parser.parse_args()
    validate(args.pinned_apotheosis_jar)

if __name__ == "__main__":
    main()
