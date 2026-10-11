#!/usr/bin/env python3
"""Conservative Dungeon Difficulty pilot schema and guardrail checks."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"experiments/ao-balance-lab/config/dungeon_difficulty_v2.json"
IDS={
"dungeoncrawl:dungeon","adventuredungeons:trialrooms",
"dungeons_arise:illager_fort","dungeons_arise:keep_kayra",
"dungeons_arise:plague_asylum","irons_spellbooks:catacombs",
}

def check_config(c):
    assert isinstance(c["dimensions"],list) and len(c["dimensions"])==1
    assert c["dimensions"][0]["world_matches"]["dimension"]=="minecraft:overworld"
    assert "difficulty" not in c["dimensions"][0] # No blanket overworld buff
    assert not c["per_player_difficulty"]["enabled"]
    assert not c["player_effects"]["enabled"]
    assert c["loot_scaling"]["armor"]==[] and c["loot_scaling"]["weapons"]==[]
    assert c["loot_scaling"]["smithing_upgrade"]["enabled"] is False
    types={t["name"]:t for t in c["difficulty_types"]}
    assert set(types)=={"ao_patrol","ao_dungeon","ao_trial"}
    assert all(t["allow_loot_scaling"] is False for t in types.values())
    assert all(len(t["entities"])==1 for t in types.values())
    for t in types.values():
        e=t["entities"][0]
        assert e["entity_matches"]["attitude"]=="HOSTILE"
        regex=e["entity_matches"]["type"]
        assert regex.startswith("~^minecraft:") and regex.endswith("$")
        assert all(m["attribute"].startswith("minecraft:generic.") for m in e["attributes"])
        assert all(m["value"]<=0.5 for m in e["attributes"])
        assert e["spawners"]["spawn_count_multiplier"]==0
    zs=c["dimensions"][0]["zones"]
    assert {z["zone_matches"]["structure"] for z in zs}==IDS
    assert len(zs)==len(IDS)
    for z in zs:
        assert z["difficulty"]["name"] in types
        assert z["difficulty"]["level"] in (2,3)
    assert c["dimensions"][0]["entities"]==[]
    return True

def main():
    data=json.loads(CONFIG.read_text())
    check_config(data)
    print("PASS DD 3.9.2 pilot schema & safety: 6 exact structures, boss whitelist, NO item loot/per-player effects")
if __name__=="__main__":main()
