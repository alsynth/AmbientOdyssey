#!/usr/bin/env python3
"""Verify exact-scoped Mine Cells AO protection, not gameplay compatibility."""
import argparse
import json
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BASE="release_030/overrides/config/paxi/datapacks/ao_minecells_dimension_guards/"
DIMS={"minecells:black_bridge","minecells:insufferable_crypt","minecells:prison","minecells:promenade","minecells:ramparts"}
TAN="data/tanshugetrees/neoforge/biome_modifier/world_gen_before_plants.json"
STREAM="data/streamsreflowing/tags/worldgen/biome/no_streams.json"
MARK="data/ambient_odyssey/tags/worldgen/biome/minecells_protected.json"

def validate(load):
    p=json.loads(load(TAN))
    assert p=={"type":"neoforge:add_features","biomes":{"type":"neoforge:not","value":sorted(DIMS)},"features":"tanshugetrees:world_gen_before_plants","step":"underground_decoration"},p
    for path in (STREAM,MARK):
        x=json.loads(load(path))
        assert x.get("replace") is False
        assert set(x.get("values",[]))==DIMS and len(x["values"])==5,x
    meta=json.loads(load("pack.mcmeta"))
    assert meta["pack"]["pack_format"]==48
    print("PASS: Tan's feature now targets complement of all 5 Mine Cells biomes; streams carved out")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",type=Path)
    a=ap.parse_args()
    validate(lambda p:(ROOT/(BASE+p)).read_text(encoding="utf-8"))
    if a.archive:
        with zipfile.ZipFile(a.archive) as z:
            assert z.testzip() is None
            names=z.namelist()
            assert "manifest.json" in names
            assert len(json.loads(z.read("manifest.json"))["files"])==331
            assert all("overrides/config/paxi/datapacks/ao_minecells_dimension_guards/"+p in names for p in [TAN,STREAM,MARK,"pack.mcmeta"])
            validate(lambda p:z.read("overrides/config/paxi/datapacks/ao_minecells_dimension_guards/"+p).decode("utf-8"))
        print("PASS: importable ZIP includes guarded Paxi datapack and retains all 331 CurseForge refs")
    print("STATIC ONLY: full dungeon generation, entry safety and Promenade exit are untested")

if __name__=="__main__":
    main()
