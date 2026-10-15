#!/usr/bin/env python3
"""Fails closed if the exact pinned Apotheosis 8.9.0 loot modifiers differ.

AO only exempts minecraft:chests/spawn_bonus_chest from three native injectors.
No other native loot table pattern or chance may drift.
"""
import argparse
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OVERRIDE=ROOT/"release_030/overrides/config/paxi/datapacks/ao_starter_apotheosis_exemptions"
NAMES=("affix_conversion","affix_loot_injection")
BONUS={"chance":0.0,"pattern":{"domain":"minecraft","path_regex":"chests/spawn_bonus_chest"}}

def validate(jar):
    if not jar.exists():
        raise ValueError(f"Apotheosis 8.9.0 official JAR missing: {jar}")
    with zipfile.ZipFile(jar) as z:
        for name in NAMES:
            resource=f"data/apotheosis/loot_modifiers/{name}.json"
            native=json.loads(z.read(resource))
            staged=json.loads((OVERRIDE/resource).read_text(encoding="utf-8"))
            if staged.get("type")!=native.get("type") or staged.get("conditions")!=native.get("conditions"):
                raise ValueError(f"Changed native modifier type/conditions: {name}")
            if staged["entries"]!=[BONUS,*native["entries"]]:
                raise ValueError(f"Changed native non-Bonus loot entries for {name}; reject release")
    assert not (OVERRIDE/'data/apotheosis/loot_modifiers/gem_loot_injection.json').exists(), 'Native gems must remain untouched'
    print("PASS: 2 exact Bonus Chest affix-only exemptions; no native gem modifier override")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("jar",type=Path)
    args=ap.parse_args()
    validate(args.jar)

if __name__=="__main__":
    main()
