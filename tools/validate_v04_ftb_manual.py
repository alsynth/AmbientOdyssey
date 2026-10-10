#!/usr/bin/env python3
"""AO Q1 FTB reference book: authored content and SNBT static gate.

All 29 pages are optional checkmark reference material with zero rewards,
zero dependencies and no claims about performing the described gameplay.
Minecraft client/server GUI behavior remains NOT TESTED.

Requires Python 3.11+, nbtlib==2.0.4 in CI.
"""
import json
import re
from pathlib import Path
import nbtlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"release_030/overrides/config/ftbquests/quests"
INDEX=ROOT/"docs/questing/FTB_MANUAL_Q1_INDEX.json"
EXPECTED={"ao_field_manual":14,"ao_tips_tricks":8,"ao_keybinds":7}
HEX=re.compile(r"^[A-F0-9]{16}$")

def parse_ftb_text(s):
    """Strictly parse the JSON-like FTB SNBT after adding omitted row separators.

    FTB's own SNBT dialect permits newline-separated compound keys and list
    entries without commas. nbtlib is stricter. Only normalize delimiters in
    memory for validation; never rewrite the game's original SNBT files.
    """
    lines=s.splitlines()
    significant=[i for i,line in enumerate(lines) if line.strip() and not line.lstrip().startswith("//")]
    for pos, idx in enumerate(significant[:-1]):
        now=lines[idx].strip()
        nxt=lines[significant[pos+1]].strip()
        if not now.endswith(("{","[",":",",")) and not nxt.startswith(("}","]")):
            lines[idx] += ","
    return nbtlib.parse_nbt("\n".join(lines))

def parse(path):
    return parse_ftb_text(Path(path).read_text(encoding="utf-8-sig"))

def run():
    data=json.loads(INDEX.read_text(encoding="utf-8"))
    records=data["article_index"]
    assert len(records)==29==data["article_count"]
    assert {g["slug"]:g["number"] for g in data["chapters"]}==EXPECTED
    lang=parse(BASE/"lang/en_us.snbt")
    idset=set()
    articleids=set()
    taskids=set()
    seen_chapters=set()
    for slug, count in EXPECTED.items():
        path=BASE/"chapters"/(slug+".snbt")
        ch=parse(path)
        assert str(ch["filename"])==slug
        cid=str(ch["id"])
        assert HEX.fullmatch(cid)
        assert cid not in idset
        idset.add(cid)
        assert ch["icon"]["id"] in ("minecraft:knowledge_book","minecraft:spyglass","minecraft:recovery_compass")
        assert str(ch.get("progression_mode",""))=="flexible"
        assert len(ch["quests"])==count
        assert not ch.get("always_invisible",False)
        assert len(ch.get("quest_links",[]))==0
        assert "chapter."+cid+".title" in lang
        seen_chapters.add(slug)
        for q in ch["quests"]:
            qid=str(q["id"])
            assert HEX.fullmatch(qid) and qid not in idset
            idset.add(qid);articleids.add(qid)
            assert bool(q["optional"]) and bool(q["disable_toast"])
            assert not q.get("dependencies",[])
            assert not q.get("rewards",[])
            assert len(q["tasks"])==1
            task=q["tasks"][0]
            tid=str(task["id"])
            assert HEX.fullmatch(tid) and tid not in idset
            idset.add(tid);taskids.add(tid)
            assert str(task["type"])=="checkmark"
            titlekey=f"quest.{qid}.title"
            desckey=f"quest.{qid}.quest_desc"
            taskkey=f"task.{tid}.title"
            for key in (titlekey,desckey,taskkey):
                assert key in lang,(slug,key)
            assert len(str(lang[titlekey]))>=7
            assert len(lang[desckey])>=3
            assert "mark page as read" in str(lang[taskkey]).lower()
            body="\n".join(map(str,lang[desckey])).lower()
            assert "no quest rewards" in body or "no rewards" in body or "educational reference" in body
    assert seen_chapters==set(EXPECTED)
    assert {x["id"] for x in records}==articleids
    assert {x["task_id"] for x in records}==taskids
    assert all(x["chapter"] in EXPECTED for x in records)
    assert len({(x["chapter"],x["article_number"]) for x in records})==29
    assert "quest.2B70445E6CD99EDB.quest_desc" in lang
    assert "quest.2B70445E6CD99EDB.quest_desc" in (BASE/"lang/en_us.snbt").read_text(encoding="utf-8")
    assert (BASE/"chapters/when_dungeons_arise.snbt").exists()
    assert not data["required_rewards"] and not data["mandatory_dependencies"]
    print(json.dumps({"status":"STATIC_VALIDATION_PASS","field_manual":14,"tips":8,
           "controls":7,"articles":29,"unique_ids":len(idset),
           "rewards":0,"prerequisites":0,"runtime_tested":False},indent=2))
    return 29

if __name__=="__main__":
    run()
