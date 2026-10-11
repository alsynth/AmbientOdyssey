#!/usr/bin/env python3
"""Inspect the exact pinned Dungeon Crawl 2.3.17 spawner bytecode.

Read-only investigation: do NOT modify chunk storage or synthetic spawner NBT
without a reproducible placed-structure test proving block-entity lifecycle.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import zipfile

JAR_SHA256="853cd59208f17c25188a419b48d1a9fed3acebf676bb1ddd026fa4e7fb56dad4"
URL="https://cdn.modrinth.com/data/q0rRg4lH/versions/D7lKpb69/DungeonCrawl-NeoForge-1.21-2.3.17.jar"
CLASS="xiroc.dungeoncrawl.dungeon.block.Spawner"
ROOT=Path(__file__).resolve().parents[1]


def analyze(javap):
    needle="public void place(net.minecraft.world.level.LevelAccessor,"
    section=javap.split(needle,1)
    assert len(section)==2, "Pinned spawner placement signature changed"
    body=section[1].split("\n  public ",1)[0]
    needles={
        "worldgen_setblock":"LevelAccessor.setBlock:",
        "block_entity_lookup":"LevelAccessor.getBlockEntity:",
        "guard_instanceof":"class net/minecraft/world/level/block/entity/SpawnerBlockEntity",
        "random_monster":"RandomMonster.randomMonster:",
    }
    offsets={}
    for key, token in needles.items():
        match=re.search(r"(?m)^\s*(\d+):.*"+re.escape(token),body)
        assert match is not None, f"Missing pinned bytecode operation: {key}"
        offsets[key]=int(match.group(1))
    assert offsets["worldgen_setblock"]<offsets["block_entity_lookup"]<offsets["guard_instanceof"]<offsets["random_monster"],offsets
    return {
        "operation_offsets":offsets,
        "native_flow":"setBlock(SPAWNER) then immediate LevelAccessor.getBlockEntity, instanceof guard, configurable entity spawn data",
        "known_risk":"WorldGenRegion may not return a live BlockEntity immediately; native code path reports failure rather than configuring spawner",
        "safe_fix_ready":False,
        "why_no_patch":"Not enough runtime evidence to choose chunk pending-NBT, immediate BE placement, deferred task, or upstream fix safely",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path)
    args=p.parse_args()
    if args.jar:
        source=args.jar
        payload=source.read_bytes()
    else:
        req=urllib.request.Request(URL,headers={"User-Agent":"AmbientOdyssey-DungeonCrawlAudit/1.0"})
        with urllib.request.urlopen(req,timeout=90) as f:payload=f.read(10_000_000)
        source=ROOT/"build/native-jars/dungeoncrawl-source.jar"
        source.parent.mkdir(parents=True,exist_ok=True)
        source.write_bytes(payload)
    actual=hashlib.sha256(payload).hexdigest()
    assert actual==JAR_SHA256, (actual,JAR_SHA256)
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        assert CLASS.replace(".","/")+".class" in z.namelist()
    a=subprocess.run(["javap","-classpath",str(source),"-c","-p",CLASS],
                     check=True,capture_output=True,text=True,timeout=45)
    found=analyze(a.stdout)
    found.update({"native_jar_sha256":actual,"class":CLASS,
                  "fix_applied":False,"minecraft_runtime_tested":False})
    dest=ROOT/"build/v041-dungeoncrawl-spawner-lifecycle.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(found,indent=2)+"\n")
    print(json.dumps(found,indent=2))

if __name__=="__main__":
    main()
