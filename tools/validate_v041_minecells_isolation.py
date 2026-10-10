#!/usr/bin/env python3
"""Static Mine Cells hydrology-isolation check; never claims successful gameplay."""
import argparse
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REL = "release_030/overrides/config/paxi/datapacks/ao_compatibility/data/streamsreflowing/tags/worldgen/biome/no_streams.json"
BIOMES = {
    "minecells:black_bridge",
    "minecells:insufferable_crypt",
    "minecells:prison",
    "minecells:promenade",
    "minecells:ramparts",
}

def check(payload):
    assert payload["replace"] is False
    assert set(payload["values"]) == BIOMES, payload
    assert len(payload["values"]) == len(BIOMES)
    print("PASS Mine Cells hydrology blacklist: five custom biomes only")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", type=Path)
    args = ap.parse_args()
    local = json.loads((ROOT / REL).read_text(encoding="utf-8"))
    check(local)
    source = (ROOT / "compile_compatibility_031.py").read_text(encoding="utf-8")
    assert "write_tag('streamsreflowing', 'no_streams', minecells_biomes)" in source
    assert all(b in source for b in BIOMES)
    if args.archive:
        with zipfile.ZipFile(args.archive) as z:
            entry = "overrides/config/paxi/datapacks/ao_compatibility/data/streamsreflowing/tags/worldgen/biome/no_streams.json"
            assert entry in z.namelist(), "Datapack isolation lost from CurseForge ZIP"
            check(json.loads(z.read(entry)))
        print("PASS archive includes the same isolation tag")
    print("STATIC ONLY: portal-to-Promenade, jigsaw geometry and worldgen performance must be tested in Minecraft")

if __name__ == "__main__":
    main()
