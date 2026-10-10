#!/usr/bin/env python3
"""Export source-verified Ambient Odyssey quests for Cloudflare Workers.

No runtime Minecraft state, player names, or world progress is read or exported.
Examples:
    python tools/export_cloudflare_quests.py
    python tools/export_quest_atlas.py --check
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "release_030/overrides/config/questlog"
SITE = ROOT / "integrations/cloudflare/generated"
INDEX = ROOT / "docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json"
OUT_JSON = SITE / "quest-data.json"
OUT_JS = SITE / "quest-data.mjs"


def load_atlas():
    source_index = json.loads(INDEX.read_text(encoding="utf-8"))
    chapters = []
    for file in sorted((SOURCE / "chapters").glob("*.json")):
        chapter = json.loads(file.read_text(encoding="utf-8"))
        chapters.append({
            "id": file.stem,
            "name": chapter["name"],
            "icon": chapter.get("icon", {}).get("item", ""),
            "order": chapter["order"],
        })
    chapters.sort(key=lambda c: (c["order"], c["id"]))
    chapter_ids = {c["id"] for c in chapters}
    quests = []
    for file in sorted((SOURCE / "quests").glob("*.json")):
        quest = json.loads(file.read_text(encoding="utf-8"))
        chapter = quest["chapter"].removeprefix("questlog:")
        assert chapter in chapter_ids, (file.name, chapter)
        quests.append({
            "id": file.stem,
            "chapter": chapter,
            "title": quest["title"],
            "description": quest.get("description", ""),
            "icon": quest.get("icon", {}).get("item", ""),
            "sort_order": quest["sort_order"],
            "objectives": quest.get("objectives", []),
            "rewards": quest.get("rewards", []),
            "prerequisites": quest.get("prerequisites", []),
            "repeatable": quest.get("repeatable", False),
            "global": quest.get("global", False),
        })
    order = {c["id"]: c["order"] for c in chapters}
    quests.sort(key=lambda q: (order[q["chapter"]], q["sort_order"], q["id"]))
    assert len(quests) == source_index["quest_count"], "Site/pack quest count drift"
    assert len(chapters) == source_index["chapter_count"], "Site/pack chapter count drift"
    assert {q["id"] for q in quests} == {e["id"] for e in source_index["entries"]}
    assert len({q["id"] for q in quests}) == len(quests), "Duplicate Quest ID"
    for chapter in chapters:
        chapter["quest_count"] = sum(q["chapter"] == chapter["id"] for q in quests)
    return {
        "schema": "ambient_odyssey_quest_atlas_v1",
        "version": "v0.4h Q1 experimental",
        "game_version": source_index["minecraft"],
        "questlog_version": source_index["questlog"],
        "data_status": "source-authored; full game runtime not verified",
        "chapters": chapters,
        "quests": quests,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed website JSON/JS differs from current Questlog source")
    args = parser.parse_args()
    data = load_atlas()
    serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    javascript = "const questAtlas = " + serialized.rstrip("\n") + ";\nexport default questAtlas;\n"
    if args.check:
        published = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        assert published == data, "Cloudflare data JSON is stale. Run python tools/export_cloudflare_quests.py"
        text = OUT_JS.read_text(encoding="utf-8")
        assert text.startswith("const questAtlas = ") and text.endswith(";\nexport default questAtlas;\n")
        assert json.loads(text[len("const questAtlas = "):-len(";\nexport default questAtlas;\n")]) == data, "Cloudflare data module is stale"
        print(f"PASS_STATIC_SOURCE_PARITY: {len(data['quests'])} quests, {len(data['chapters'])} chapters; no player data")
        return
    SITE.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(serialized, encoding="utf-8")
    OUT_JS.write_text(javascript, encoding="utf-8")
    print(f"Exported {len(data['quests'])} quests / {len(data['chapters'])} chapters to {SITE}")


if __name__ == "__main__":
    main()
