#!/usr/bin/env python3
"""Static fail-closed AO Questlog 3.4.1 Q1 authoring and localization audit.

Does not claim Minecraft has parsed these files, registered the objective IDs,
awarded progression correctly, or synchronized in multiplayer.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"release_030/overrides/config/questlog"
INDEX=ROOT/"docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json"
RES=re.compile(r"^(?:minecraft|questlog|minecells):[a-z0-9_./-]+$")
OBJECTIVES={"read","item_obtain","item_equip","stat","or","visit_biome","visit_structure",
            "visit_dimension","enchant","quest_complete","entity_kill"}
REWARDS={"item","experience"}
ICONIDS={"minecraft:book","minecraft:compass","minecraft:iron_sword","minecraft:spyglass",
         "minecraft:brush","minecraft:enchanted_book","minecraft:nether_star",
         "minecraft:amethyst_shard","minecraft:heart_of_the_sea","minecraft:enchanting_table",
         "minecraft:blaze_rod","minecraft:oak_sapling","minecraft:ender_eye"}

def validate_objective(o, known, deps):
    assert isinstance(o,dict),o
    typ=o.get("type","")
    assert typ.startswith("questlog:"),typ
    short=typ.split(":")[1]
    assert short in OBJECTIVES,typ
    assert isinstance(o.get("name",""),str)
    if short=="or":
        a=o.get("objectives")
        assert isinstance(a,list) and len(a)>=2 and len(a)<=6
        for x in a: validate_objective(x,known,deps)
        return
    if short=="quest_complete":
        target=o.get("quest","")
        assert target.startswith("questlog:")
        target=target.split(":")[1]
        assert target in known,target
        deps.add(target)
        return
    if short=="read":
        assert "required_amount" not in o
        return
    if short=="enchant":
        assert not any(k in o for k in ("item","enchantment")), "Flexible enchant only"
        return
    if short=="stat":
        assert o.get("stat") in {"minecraft:walk_one_cm","minecraft:fish_caught"}
    else:
        key={"item_obtain":"item","item_equip":"item","visit_biome":"biome",
             "visit_structure":"structure","visit_dimension":"dimension","entity_kill":"entity"}.get(short)
        assert key
        val=o.get(key)
        assert isinstance(val,str) and RES.fullmatch(val),o
        if short=="item_equip":
            assert o.get("slot") in {"chest","feet","head","legs","mainhand","offhand"}
        # Q1 proves only vanilla IDs; no guessed/unconfirmed modded registries.
        assert val.startswith("minecraft:") or (short=="visit_structure" and val=="minecells:overworld_portal"), val
    assert 1<=o.get("required_amount",1)<=12000

def validate():
    index=json.loads(INDEX.read_text(encoding="utf-8"))
    questDir=SOURCE/"quests"
    chapterDir=SOURCE/"chapters"
    entries=index["entries"]
    known={e["id"] for e in entries}
    assert len(entries)==len(known)==index["quest_count"]==52
    assert index["chapter_count"]==13
    assert all(re.fullmatch(r"[a-z0-9_]+",n) for n in known)
    chapterFiles=sorted(chapterDir.glob("*.json"))
    questFiles=sorted(questDir.glob("*.json"))
    assert len(chapterFiles)==13 and len(questFiles)==50
    assert {p.stem for p in questFiles}==known
    chapters={}
    for file in chapterFiles:
        o=json.loads(file.read_text(encoding="utf-8"))
        assert isinstance(o["name"],str) and len(o["name"])>4
        assert o["icon"]["item"] in ICONIDS
        assert isinstance(o["order"],int) and 0<=o["order"]<=12
        assert not o["hidden"]
        chapters[file.stem]=o
    assert len({c["order"] for c in chapters.values()})==13
    assert sum(c["default_chapter"] for c in chapters.values())==1
    assert chapters["first_pages"]["default_chapter"]
    assert set(chapters)=={e["chapter"] for e in entries}
    deps={}
    stat=Counter()
    reward_totals=Counter()
    for e in entries:
        slug=e["id"]
        q=json.loads((questDir/(slug+".json")).read_text(encoding="utf-8"))
        assert e["source_seed"] in ("new-q1",slug)
        assert q["chapter"]=="questlog:"+e["chapter"]
        assert not q.get("repeatable",False) and not q.get("global",False)
        assert not q.get("hidden",False)
        assert isinstance(q["title"],str) and 5<=len(q["title"])<=80
        assert isinstance(q["description"],str) and len(q["description"])>=140
        assert q["icon"]["item"].startswith("minecraft:")
        assert 1<=len(q["objectives"])<=4
        prereqs=q.get("prerequisites",[])
        assert len(prereqs)<=2
        deps[slug]=set()
        for obj in prereqs: 
            assert obj["type"]=="questlog:quest_complete",slug
            validate_objective(obj,known,deps[slug])
        assert slug not in deps[slug]
        for obj in q["objectives"]:
            validate_objective(obj,known,set())
            stat[obj["type"]]+=1
        rewards=q.get("rewards",[])
        assert len(rewards)<=2
        for rew in rewards:
            assert rew["type"].split(":")[1] in REWARDS
            if rew["type"]=="questlog:experience":
                assert 0<rew["experience"]<=200
                assert rew.get("levels",False) is False
                reward_totals["experience"]+=rew["experience"]
            else:
                assert rew["item"].startswith("minecraft:")
                assert 1<=rew["count"]<=16
                reward_totals["item"]+=rew["count"]
        assert [x["type"] for x in q["objectives"]]==e["objective_types"]
        assert len(rewards)==e["rewards"]
    def visit(slug,active,done):
        if slug in done:return
        assert slug not in active,("Quest prerequisite cycle",slug)
        active.add(slug)
        for d in deps[slug]:visit(d,active,done)
        active.remove(slug)
        done.add(slug)
    done=set()
    for slug in known:visit(slug,set(),done)
    assert len(done)==50
    assert "ao_first_pages_01_welcome_to_ambient_odyssey" in known
    assert not deps["ao_first_pages_01_welcome_to_ambient_odyssey"]
    # The separate cursed route must never become a required ancestor of another chapter.
    cursed={x for x in known if x.startswith("ao_enigmatic_cursed")}
    for slug,d in deps.items():
        if slug not in cursed:
            assert not (d & cursed),(slug,d)
    # No authoring of externally fabricated boss/dimension registries yet.
    assert stat["questlog:read"]>0 and stat["questlog:item_obtain"]>0
    assert reward_totals["experience"]<1500 and reward_totals["item"]<120
    print(json.dumps({"status":"PASS_STATIC_ONLY","quest_count":len(known),
        "chapters":len(chapters),"objective_types":dict(stat),
        "reward_totals":dict(reward_totals),"cycles":0,
        "server_runtime_verified":False,"client_runtime_verified":False},indent=2))
    return len(known)

if __name__=="__main__":
    validate()
