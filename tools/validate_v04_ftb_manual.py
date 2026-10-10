#!/usr/bin/env python3
"""Read-only FTB Quests 2101.1.36 manual source checks (not a Minecraft parser).

Checks the three chapter files against the implementation index and language
table, preserved WDA chapter, unique IDs, localization, and no progression or
rewards. FTB's newline-tolerant SNBT dialect still requires in-game acceptance.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
QUESTS=ROOT/"release_030/overrides/config/ftbquests/quests"
INDEX=ROOT/"docs/questing/FTB_MANUAL_IMPLEMENTED_INDEX.json"
HEX=re.compile(r"^[A-F0-9]{16}$")
PAGE_ID=re.compile(r'(?m)^\s*id:\s*"([A-F0-9]{16})"\s*$')
LOC=re.compile(r'(?m)^\s*((?:chapter|quest)\.[A-F0-9]{16}\.(?:title|quest_subtitle|quest_desc))\s*:')
LANDING_REWARD_COUNT=0

def balanced(text):
    stack=[]
    quoted=False
    escape=False
    for ch in text:
        if quoted:
            if escape: escape=False
            elif ch=="\\": escape=True
            elif ch=='"': quoted=False
            continue
        if ch=='"':
            quoted=True
        elif ch in "{[": stack.append(ch)
        elif ch in "}]":
            assert stack and stack.pop()=={"}":"{","]":"["}[ch],"Invalid brackets"
    assert not quoted and not stack, "Invalid quote or bracket balance"

def validate():
    idx=json.loads(INDEX.read_text(encoding="utf-8"))
    assert idx["total_pages"]==32 and len(idx["chapters"])==idx["chapter_count"] if "chapter_count" in idx else len(idx["chapters"])==3
    manual_names={ch["slug"] for ch in idx["chapters"]} if all("slug" in ch for ch in idx["chapters"]) else set()
    assert idx["base_mod_count"]==331
    lang=(QUESTS/"lang/en_us.snbt").read_text(encoding="utf-8")
    balanced(lang)
    assert "chapter.231570DE6A7FCD52.title:" in lang
    existing=(QUESTS/"chapters/when_dungeons_arise.snbt").read_text(encoding="utf-8")
    assert 'id: "231570DE6A7FCD52"' in existing
    assert "dungeons_arise:wda_root" in existing
    assert "reward" in existing and "tasks:" in existing
    keys=LOC.findall(lang)
    assert len(keys)==len(set(keys)), "Duplicate localization keys (risk existing WDA overwritten)"
    known_ids=set(PAGE_ID.findall(existing))
    created_ids=set()
    for ch in idx["chapters"]:
        file=QUESTS/"chapters"/(ch["slug"]+".snbt")
        text=file.read_text(encoding="utf-8")
        balanced(text)
        assert text.startswith("{") and text.rstrip().endswith("}")
        assert f'filename: "{ch["slug"]}"' in text
        assert f'id: "{ch["chapter_id"]}"' in text
        assert 'progression_mode: "flexible"' in text
        assert 'group: ""' in text
        assert "quests: [" in text
        assert not re.search(r'(?m)^\s*(?:dependencies|prerequisites):',text)
        assert 'tasks: [ ]' in text and 'rewards: [ ]' in text
        assert len(re.findall(r'(?m)^\s*tasks: \[ \]\s*$',text))==ch["pages"]
        assert len(re.findall(r'(?m)^\s*rewards: \[ \]\s*$',text))==ch["pages"]
        chapter_ids=PAGE_ID.findall(text)
        assert len(chapter_ids)==ch["pages"]+1,(file,chapter_ids)
        assert chapter_ids[0]==ch["chapter_id"]
        assert chapter_ids[1:]==ch["page_ids"]
        for ident in chapter_ids:
            assert HEX.fullmatch(ident) and ident not in known_ids and ident not in created_ids,ident
            created_ids.add(ident)
        assert f"chapter.{ch['chapter_id']}.title" in keys
        assert len(ch["page_ids"])==len(ch["page_titles"])==ch["pages"]
        for qid in ch["page_ids"]:
            for suffix in ("title","quest_subtitle","quest_desc"):
                assert f"quest.{qid}.{suffix}" in keys,(qid,suffix)
    assert len(created_ids)==35
    assert sum(ch["pages"] for ch in idx["chapters"])==32
    # All entries are reference content, not reward grants or progression gates.
    print(json.dumps({"status":"PASS_STATIC_ONLY","manual_chapters":3,
        "manual_reference_pages":32,"new_ids":len(created_ids),
        "wda_chapter_preserved":True,"taskless":True,"rewards":0,
        "questlog_q1_unchanged":True,"ftb_in_game_tested":False},indent=2))
    return True

if __name__=="__main__":
    validate()
