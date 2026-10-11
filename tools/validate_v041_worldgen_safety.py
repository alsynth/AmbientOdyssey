#!/usr/bin/env python3
"""Verify source and source-backed Luki single-pool Paxi registry repair."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"release_030/overrides/config/paxi/datapacks/ao_lukis_mansion_native_pool"
assert (BASE/"pack.mcmeta").exists()
data=json.loads((BASE/"data/mansions/worldgen/template_pool/mansion/bottom_back_left.json").read_text())
assert data["name"]=="mansions:mansion/bottom_back_left"
assert data["fallback"]=="minecraft:empty"
assert data["elements"]==[{"weight":1,"element":{"location":"mansions:mansion/bottom_back_left","processors":"mansions:mansion_texture","projection":"rigid","element_type":"minecraft:single_pool_element"}}]
m=(ROOT/"addons/ao-worldgen-safety/src/main/java/dev/ambientodyssey/worldgensafety/mixin/HominidFinalizeSpawnMixin.java").read_text()
for key in ("HominidClientEvents","FinalizeSpawnEvent","getClass() != Zombie.class","!level.getServer().isSameThread()","ci.cancel()"):
    assert key in m,key
print("PASS: native pinned mansion piece pool and narrow Hominid offthread event guard")
