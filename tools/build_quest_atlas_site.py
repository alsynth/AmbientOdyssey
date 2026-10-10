#!/usr/bin/env python3
"""Create a deterministic, fully offline Ambient Odyssey website ZIP."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
FILES = (
    "index.html",
    "quests.html",
    "assets/quest-atlas.css",
    "assets/quest-atlas.js",
    "quest-data.json",
    "quest-data.js",
    "README.md",
)
STAMP = (2026, 10, 10, 0, 0, 0)


def build(output: Path):
    for relative in FILES:
        if not (SITE / relative).is_file():
            raise FileNotFoundError(SITE / relative)
    data = json.loads((SITE / "quest-data.json").read_text(encoding="utf-8"))
    assert len(data["quests"]) == 50 and len(data["chapters"]) == 13
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for relative in FILES:
            info = zipfile.ZipInfo(relative, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (SITE / relative).read_bytes())
    with zipfile.ZipFile(output) as z:
        assert z.namelist() == list(FILES)
        assert z.testzip() is None
        assert b'window.AO_QUEST_DATA' in z.read("quest-data.js")
        assert b'Quest Atlas' in z.read("quests.html")
        assert b'Development Roadmap' in z.read("index.html")
    print(f"PASS_STATIC_OFFLINE_ZIP bytes={output.stat().st_size} sha256={hashlib.sha256(output.read_bytes()).hexdigest()}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/Ambient_Odyssey_Roadmap_Quest_Atlas_Q1.zip")
    args = parser.parse_args()
    build(args.output)
