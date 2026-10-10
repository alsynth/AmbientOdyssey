#!/usr/bin/env python3
"""Source-backed Test8.6 structure-generation regression gates (no Minecraft runtime assertion)."""
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parent
PACKS = ROOT / "release_030/overrides/config/paxi/datapacks"
BASE = PACKS / "ao_worldgen_final_fixes/data"
INDEX = ROOT / "release_030/evidence/jar-resource-index-test6.json.gz"
COOK_NAMES = ("cook_additions_1_pool","cook_additions_2_pool","cook_additions_3_pool","cook_additions_4_pool","cook_end_1_pool")

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def check():
    passes = 0
    def require(label, expected):
        nonlocal passes
        assert expected, label
        passes += 1
    data = json.loads(gzip.decompress(INDEX.read_bytes()))
    poolindex = data["resources"]["worldgen/template_pool"]
    require("Test6 source index is available", isinstance(poolindex, dict))
    total = 0
    for ident in COOK_NAMES:
        native = poolindex[f"farmers_structures:{ident}"][0]
        require(f"{ident} exact installed-jar provenance", native["jar"] == "FarmersStructures-1.0.6-1.21.1_neoforge.jar")
        source = native["data"]
        alias = read(BASE / f"minecraft/worldgen/template_pool/{ident}.json")
        require(f"{ident} fixed minecraft lookup key", alias["name"] == f"minecraft:{ident}")
        require(f"{ident} retained native fallback", alias["fallback"] == source["fallback"] == "minecraft:empty")
        require(f"{ident} native piece weights and processors intact", alias["elements"] == source["elements"])
        total += len(alias["elements"])
    require("All original 71 Farmer cook pieces retained", total == 71)
    angler=read(BASE / "minecraft/worldgen/template_pool/angler_additions_3_pool.json")
    cook3=read(BASE / "minecraft/worldgen/template_pool/cook_additions_3_pool.json")
    require("Native Farmer 1.0.6 cook additions 3 mistaken angler reference repaired", angler["name"]=="minecraft:angler_additions_3_pool" and angler["elements"]==cook3["elements"] and angler["fallback"]==cook3["fallback"])


    archa = read(BASE / "archaion/worldgen/structure/ancient_keep.json")
    first = read(BASE / "archaion/worldgen/template_pool/ancient_keep/start.json")
    rooms = read(BASE / "archaion/worldgen/template_pool/ancient_keep/rooms.json")
    roomx = read(BASE / "archaion/worldgen/template_pool/ancient_keep/rooms_x.json")
    require("Archaion root selects dedicated valid start", archa["start_pool"] == "archaion:ancient_keep/start" and archa["start_jigsaw_name"] == "archaion:arena_mainhall")
    require("Archaion first piece native arena only", len(first["elements"]) == 1 and first["elements"][0]["element"]["location"] == "archaion:ancient_keep/arena")
    require("Archaion selection keeps processor", first["elements"][0]["element"]["processors"] == "minecraft:ancient_city_start_degradation")
    require("Previously corrupt rooms excluded", len(rooms["elements"]) == 10 and len(roomx["elements"]) == 7 and all("misc_room" not in elt["element"]["location"] for pool in (rooms,roomx) for elt in pool["elements"]))

    train = read(BASE / "create_easy_structures/worldgen/template_pool/undergroundtrain_station.json")
    require("Create Easy missing pool explicitly defined", train["name"] == "create_easy_structures:undergroundtrain_station")
    require("Unsupported station connector gracefully terminates", train["fallback"] == "minecraft:empty" and train["elements"] == [{"weight": 1, "element": {"element_type":"minecraft:empty_pool_element"}}])

    lock = read(ROOT / "release_030/release-lock.json")
    require("Test8.6 scoped version", lock["version"] in ("0.3.8-worldgen-prefreeze-test1.6", "0.3.8-worldgen-prefreeze-test1.7"))
    ids = {k:lock["additions"][k]["id"] for k in ("structure-better-bastions","structure-lukis-woodland-mansions")}
    require("All three Test8.5 mods kept", ids == {"structure-better-bastions":8988949, "structure-lukis-woodland-mansions":7227735} and lock["private_modrinth_addons"][0]["version_id"] == "PVzfioBU")
    print(f"PASS: {passes} source-backed Test8.6 generation repair checks, 71 native Farmer pieces retained.")
    print("NOT TESTED: game start, jigsaw matching, actual natural generation, structure layout, false-positive warning disappearance.")

if __name__ == "__main__":
    check()
