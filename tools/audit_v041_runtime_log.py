#!/usr/bin/env python3
"""Review a locally held AO client log without copying or publishing personal paths.

Produces only aggregate severities and typed issues, not raw lines or identities.
For Minecraft 1.21.1 / NeoForge 21.1.252. Read-only; no runtime claims.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ISSUE_MARKERS = {
    "invalid_air_item": "Item must not be minecraft:air",
    "invalid_registry_item": "Unknown registry key in ResourceKey[minecraft:root / minecraft:item]",
    "unknown_legacy_attribute": "Ignoring unknown attribute 'forge:",
    "cosmetic_model_missing": "missing model for variant:",
    "texture_missing": "Missing textures in model",
    "mansion_missing_pool": "Couldn't find template pool reference: mansions:mansion/bottom_back_left",
    "dungeon_crawl_spawner": "Failed to fetch a mob spawner",
    "poi_mismatch": "POI data mismatch",
    "offthread_entity_creation": "trying to add an entity from offthread",
    "questlog_sync": "Received quest & chapter sync from server",
    "streams_biome_missing": "streamsreflowing:stream (from",
    "broken_bumblezone_trade": "Trade result entry is set to required",
    "jei_long_recipe_registration": "Registering recipes: jei:minecraft is running and has taken",
    "minecells_arrival": "Reloading pipeline on dimension change: minecraft:overworld => minecells:prison",
}
ALLOWED_OWNERS=("HominidClientEvents.onEntityJoinWorld","tanshugetrees_core.game.GameUtils$Mob.summon",
                "tanshugetrees_handcode.systems.world_gen.TreePlacer")

def analyze(text):
    lines=text.splitlines()
    stall_pattern=re.compile(r"Can't keep up!.*?Running (\d+)ms")
    stalls=[int(m.group(1)) for line in lines if (m:=stall_pattern.search(line))]
    counts={name:sum(value in line for line in lines) for name,value in ISSUE_MARKERS.items()}
    error_count=sum("/ERROR]" in line for line in lines)
    warn_count=sum("/WARN]" in line for line in lines)
    owners=[owner for owner in ALLOWED_OWNERS if any(owner in line for line in lines)]
    streams_mod=any("Found mod file" in line and "streamsreflowing" in line.lower() for line in lines)
    bridge_mod=any("Found mod file" in line and "ambientodyssey-streams-minecells" in line.lower() for line in lines)
    return {
        "status":"SOURCE_LOG_ONLY_NO_OPTIMIZATION_CLAIM",
        "lines":len(lines),"log_errors":error_count,"log_warnings":warn_count,
        "typed_events":counts,
        "server_stalls_ms":{"count":len(stalls),"worst":max(stalls) if stalls else 0,
                            "all_descending":sorted(stalls,reverse=True)},
        "offthread_stack_owners":owners,
        "profile":{"streams_reflowing_file_present":streams_mod,
                   "ao_minecells_streams_addon_file_present":bridge_mod},
        "notes":[
          "Counts are log messages, not unique causal errors.",
          "An integrated-server delay cannot distinguish chunkgen/main tick/GC without profiler evidence.",
          "Missing Streams biome tags in a profile without Streams may be resolved by the combined pack.",
          "Raw log lines and local user/account paths are never included in the output."
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("log",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=analyze(a.log.read_text(errors="replace"))
    out=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(exist_ok=True,parents=True)
        a.output.write_text(out)
    else:print(out,end="")

if __name__=="__main__":
    main()
