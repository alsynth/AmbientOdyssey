#!/usr/bin/env python3
"""Fail-closed ZIP-level v0.4.2 combined recipe / spawner / Q acceptance preflight.

This is binary/source verification, NOT a Minecraft runtime claim.
"""
from __future__ import annotations
import argparse, hashlib, io, json
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
JAR_Q="overrides/mods/ao-questlog-betterinventory-0.1.3.jar"
JAR_SAFE="overrides/mods/ao-worldgen-safety-0.1.3-experimental.jar"
JAR_STREAM="overrides/mods/ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar"
RECIPE_ROOT="overrides/config/paxi/datapacks/ao_v041_runtime_fixes/data/"
LEFT_DISABLED={
"brewinandchewin/recipe/hamburger_with_cheese.json",
"brewinandchewin/recipe/pizza_from_dough.json",
"brewinandchewin/recipe/toast_with_cheese.json",
"dimdungeons/recipe/recipe_item_guidebook.json"}
def check(path):
    report=json.loads((ROOT/"build/v042-minecells-recipe-migration.json").read_text())
    assert report["migration_count"]==15
    with ZipFile(path) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        m=json.loads(z.read("manifest.json"))
        assert m["version"]=="0.4.2-experimental-recipe-spawner-ui"
        assert m["minecraft"]["version"]=="1.21.1"
        assert len(m["files"])==330
        pins={i["projectID"]:i["fileID"] for i in m["files"]}
        assert len(pins)==330
        assert pins[645559]==9110961
        assert pins[618790]==7033510
        assert pins[1581408]==9060294
        for jar in (JAR_Q,JAR_SAFE,JAR_STREAM):
            assert jar in names,jar
        paths={p for p in names if p.startswith(RECIPE_ROOT) and p.endswith(".json")}
        assert len(paths)==19,(len(paths),paths)
        found=set()
        for entry in report["records"]:
            path=RECIPE_ROOT+"minecells/recipe/"+entry["id"].split(":",1)[1]+".json"
            found.add(path)
            blob=z.read(path)
            assert hashlib.sha256(blob).hexdigest()==entry["override_sha256"],path
            recipe=json.loads(blob)
            assert "fabric:load_conditions" not in recipe,path
            assert recipe["neoforge:conditions"]==[
                {"type":"neoforge:mod_loaded","modid":"create" if recipe["type"].startswith("create:") else "farmersdelight"}
            ]
        for relative in LEFT_DISABLED:
            loc=RECIPE_ROOT+relative
            found.add(loc)
            assert json.loads(z.read(loc))=={"neoforge:conditions":[{"type":"neoforge:false"}]},loc
        assert paths==found,(len(paths),len(found))
        with ZipFile(io.BytesIO(z.read(JAR_SAFE))) as addon:
            assert addon.testzip() is None
            names2=set(addon.namelist())
            cfg=json.loads(addon.read("ao_worldgen_safety.mixins.json"))
            assert set(cfg["mixins"])=={
                "HominidFinalizeSpawnMixin","TansWorldgenMarkerSchedulingMixin",
                "DungeonCrawlSpawnerPendingNbtMixin","DungeonCrawlOptionalTradeAirMixin"
            }
            for cls in cfg["mixins"]:
                assert "dev/ambientodyssey/worldgensafety/mixin/"+cls+".class" in names2
            assert 'version="0.1.3-experimental"' in addon.read("META-INF/neoforge.mods.toml").decode()
        with ZipFile(io.BytesIO(z.read(JAR_Q))) as q:
            assert q.testzip() is None
            assert "0.1.3" in q.read("META-INF/neoforge.mods.toml").decode()
            assert "dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge$QuestlogTab.class" in q.namelist()
        assert json.loads(z.read(
          "overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json"
        ))=={"size":1,"operation":"SET","replace":False}
    print("PASS: 330 exact refs, 15 author-derived NeoForge recipes, 4 evidence-gated recipe disables, AO spawner & air mixins, Q 0.1.3, Curios, Streams and full ZIP integrity")
    print("NOT runtime-tested; spawner persistence requires new dungeon + save/reload test")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("archive",type=Path);args=p.parse_args()
    check(args.archive)
