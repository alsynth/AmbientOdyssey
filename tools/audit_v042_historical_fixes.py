#!/usr/bin/env python3
"""Cross-check historical AO features against CURRENT source, not old checkboxes.
No networking, no gameplay invocation. Missing source gates fail CI.
"""
from pathlib import Path
import re,json,argparse

ROOT=Path(__file__).resolve().parents[1]
def report(root=ROOT):
    checks=[]
    def get(path):return (root/path).read_text(encoding="utf-8")
    def add(key,path,ok,evidence,category="present_source_only"):
        checks.append(dict(feature=key,source=path,status=category if ok else "source_missing_or_drifted",
                           evidence=evidence))
    p="release_030/overrides/config/paxi/datapacks/ao_server_rules/data/ambient_odyssey/function/server_rules.mcfunction"
    v=get(p)
    add("30% sleep",p,"gamerule playersSleepingPercentage 30" in v,"Configured by vanilla load function; must test 2-player dedicated")
    add("fire and mob grief",p,all("gamerule "+k+" false" in v for k in ("doFireTick","mobGriefing")),
        "Global safety rules present, may affect boss encounters")
    p="release_030/overrides/config/defaultoptions/options.txt"
    v=get(p)
    add("12/6 client distances",p,all(k in v for k in ("renderDistance:12","simulationDistance:6")),
        "Default options only; existing player options may override")
    add("quiet rain/water defaults",p,all(k in v for k in ("soundCategory_weather:0.2","soundCategory_block:0.4")),
        "Default 20% weather and 40% block, not mix-fix to canopy ambient")
    p="release_030/overrides/config/mutantmonsters-common.toml"
    v=get(p)
    add("rare mutants",p,all(re.search(r"(?m)^mutant_"+k+r"_spawn_weight\s*=\s*0\.01$",v)
                             for k in ("zombie","creeper","skeleton","enderman")),
        "Native all-four rarity weight 0.01, minimum integer weight caveat")
    p="release_030/overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json"
    v=json.loads(get(p))
    add("Curios amulet slot",p,v=={"size":1,"operation":"SET","replace":False},
        "Source-verified Curios 1.21.1 nonreplacing slot, gameplay confirmation pending")
    p="release_030/overrides/config/paxi/datapacks/ao_compatibility/data/curios/tags/item/amulet.json"
    v=json.loads(get(p))
    add("Curios amulet items",p,not v.get("replace",True) and any(x.startswith("enigmaticlegacyplus:") for x in v["values"]),
        "Enigmatic items tagged; actual 1.21.1 item existence requires native validation")
    ids=[]
    for name,n in (("field_manual",15),("tips_and_tricks",9),("keybind_cheatsheet",8)):
        p="release_030/overrides/config/ftbquests/quests/chapters/"+name+".snbt"
        v=get(p); found=re.findall(r'tasks: \[\{ id: "([0-9A-F]{16})", type: "checkmark" \}\]',v);ids+=found
        add("manual_"+name,p,len(found)==n and "tasks: [ ]" not in v,
            f"{n} explicit click tasks; existing save state may remain completed")
    add("manual task uniqueness","release_030/overrides/config/ftbquests/quests/chapters",len(ids)==len(set(ids))==32,
        "32 unique stable task IDs")
    p="release_030/overrides/config/ftbquests/quests/chapters/when_dungeons_arise.snbt"
    v=get(p)
    add("WDA progression retained",p,"dungeons_arise:wda_root" in v and "rewards:" in v,
        "Original WDA tasks and rewards preserved; runtime progression not confirmed")
    p=root/"release_030/overrides/config/questlog"
    quests=list((p/"quests").glob("*.json"));chapters=list((p/"chapters").glob("*.json"))
    add("Q1 Questlog count","release_030/overrides/config/questlog",len(quests)==52 and len(chapters)==13,
        "Current approved base: 52 quests, 13 chapters; experimental campaign is a separate overlay")
    p="release_030/overrides/config/curios-common.toml"
    add("Curios conservative common config",p, bool(re.search(r"(?m)^slots = \[\]\s*$",get(p))),
        "Do not override other mod accessory slots through global TOML")
    p="release_030/overrides/config/defaultoptions/keybindings.txt"
    v=get(p); amount=len([line for line in v.splitlines() if line.strip() and not line.startswith("#")])
    add("limited keybind defaults",p,amount==3,
        "Only three specific defaults; full player keybinding overhaul NOT DONE")
    p="release_030/overrides/config/spark/config.json"
    add("Spark available",p,"backgroundProfiler" in get(p),
        "Logger/profiler unchanged; no claimed optimization")
    p="addons/ao-worldgen-safety/src/main/resources/META-INF/neoforge.mods.toml"
    native_metadata=get(p)
    hominid_java=list((root/'addons/ao-worldgen-safety/src/main/java').rglob('*Hominid*.java'))
    add("separate Hominid candidate",p,not hominid_java and not re.search(r'modId\s*=\s*[\"\']hominid[\"\']',native_metadata),
        "Owner superseded the Hominid candidate; replacement mixin and required dependency must remain absent",
        category="intentionally_excluded")
    p="tools/generate_v041_trek_create_rarity.py";v=get(p)
    add("approved structure rarity",p,all(x in v for x in
        ('"common":(24,21)','"medium":(30,26)','"rare":(48,44)','CREATE_RATIO=1.30','assert total==43')),
        "43 structure-set changes approved visually; no measured speedup")
    base=root/"release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes/data"
    count=len(list(base.rglob("recipe/*.json")))
    # wildcard path in Python: recipe/*.json returns files directly inside recipe folders;
    # deeper files require a tree walk.
    count=sum("/recipe/" in f.as_posix() for f in base.rglob("*.json"))
    add("15 migrated native recipes and 4 remaining containment guards","release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes",
        count>=19,f"{count} recipe overrides are disabled parse-error containment, not craftable recipe fixes")
    open_issues={
        "Questlog Q icon still mispositioned":"addons/ao-questlog-betterinventory/src/main/java/dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge.java",
        "Dungeon Crawl spawner block-entity lifecycle":"tools/audit_v041_dungeoncrawl_spawner.py",
        "504 air item messages not fully attributed":"audit_invalid_structure_items_089.py",
        "Natural forest-canopy sounds and Streams volume":"release_030/overrides/config/defaultoptions/options.txt",
        "Curios amulet slot acceptance":"release_030/overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json",
        "5–7-player dedicated server and chunkgen profiling":"V04_TESTING_CHECKLIST.md",
        "Q2 complex RPG and dimension quests":"docs/questing/MOD_DEPTH_REAUDIT_2026-10-10.csv",
        "full keybind overhaul":"release_030/overrides/config/defaultoptions/keybindings.txt",
        "Xaero World Map explored tiles disappearing":"release_030/overrides/config/xaero/world-map/client.cfg",
        "boss scaling and loot progression":"docs/questing/MOD_DEPTH_REAUDIT_2026-10-10.csv",
        "native shader and resource-pack ordering acceptance":"V04_TESTING_CHECKLIST.md",
        "Mine Cells 5 dimension multiplayer progression":"V04_TESTING_CHECKLIST.md",
    }
    for item,src in open_issues.items():checks.append(dict(feature=item,source=src,status="unresolved_or_runtime_untested",evidence="Not certified by current source; defer changes until evidence supports targeted solution"))
    return {"evidence_level":"SOURCE_ONLY_NOT_RUNTIME","checks":checks,
            "counts":{"present_source_only":sum(x["status"]=="present_source_only" for x in checks),
                      "gaps":sum(x["status"]=="source_missing_or_drifted" for x in checks),
                      "open":sum(x["status"]=="unresolved_or_runtime_untested" for x in checks)}}

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--output",type=Path);x=a.parse_args()
    report=report();payload=json.dumps(report,indent=2)+"\n"
    if x.output:
        x.output.parent.mkdir(parents=True,exist_ok=True)
        x.output.write_text(payload);print("REPORT",report["counts"])
    else:print(payload)
    assert report["counts"]["gaps"]==0,"Source gates drifted"
