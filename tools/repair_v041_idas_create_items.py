#!/usr/bin/env python3
"""Generate private, source-pinned 1.21.1 IDAS Ancient Mines Create-item corrections.

No binary JAR modifications. A SHA-checked official IDAS JAR supplies the two
native structure templates; all non-target NBT compounds are preserved.
Generated native NBT is for a PRIVATE user test profile, not public redistribution.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import quote
import zipfile

import nbtlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release_030/overrides/config/paxi/datapacks/ao_idas_create_item_compat"
MOD = "idas-1.13.7+1.21.1-neoforge.jar"
PROJECT = 605375
OLD = "create:crushed_iron_ore"
NEW = "create:crushed_raw_iron"
TEMPLATES = {
    "data/idas/structure/ancient_mines/ancient_mines_hall2.nbt": 3,
    "data/idas/structure/ancient_mines/ancient_mines_hall3.nbt": 4,
}
REPORT = ROOT / "build/v041-idas-create-source-repair.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def edit_template(raw, expected):
    original = gzip.decompress(raw)
    doc = nbtlib.File.parse(io.BytesIO(original))
    before = copy.deepcopy(doc)
    touched = []

    def recurse(node, path=()):
        if isinstance(node, dict):
            if str(node.get("id", "")) == OLD:
                # The source audit located these in actual block-entity inventories.
                # Do not silently patch unrelated recipes, filters or arbitrary tags.
                assert "Items" in path, f"unexpected old item location {path}"
                assert "Count" in node or "count" in node, f"missing stack count {path}"
                node["id"] = nbtlib.String(NEW)
                touched.append("/" + "/".join(map(str, path)))
            for k, v in node.items():
                recurse(v, (*path, str(k)))
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                recurse(v, (*path, i))

    recurse(doc)
    assert len(touched) == expected, (len(touched), expected, touched)

    # Undo ONLY the seven rewritten ids in a second copy, then compare against
    # the parsed upstream tree to exclude unrelated semantic mutations.
    restored = copy.deepcopy(doc)
    # Check all changes using explicit paths, including original slot positions.
    for path in touched:
        keys = path.strip("/").split("/")
        element = restored
        for key in keys:
            element = element[int(key)] if isinstance(element, (list, tuple)) else element[key]
        assert str(element["id"]) == NEW
        element["id"] = nbtlib.String(OLD)
    assert restored == before, "an unrelated NBT value was modified"

    buf = io.BytesIO()
    doc.write(buf)
    rewritten = gzip.compress(buf.getvalue(), compresslevel=9, mtime=0)
    parsed_again = nbtlib.File.parse(io.BytesIO(gzip.decompress(rewritten)))
    assert parsed_again == doc, "NBT write/read did not round-trip"
    return rewritten, touched


def make(source_jar: Path, dest=OUT, expected_sha=None):
    raw = source_jar.read_bytes()
    actual = sha(raw)
    if expected_sha:
        assert actual == expected_sha, f"Unexpected IDAS source hash: {actual}"
    created = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as jar:
        assert jar.testzip() is None
        for member, count in TEMPLATES.items():
            patched, paths = edit_template(jar.read(member), count)
            output = dest / member
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(patched)
            created[member] = {
                "native_sha256": sha(jar.read(member)),
                "patched_sha256": sha(patched),
                "exact_item_paths": paths,
                "count": len(paths),
            }
    (dest / "pack.mcmeta").write_text(json.dumps({
        "pack": {"pack_format": 48,
                 "description": "AO private: IDAS Ancient Mines Create crushed iron 1.21.1 item ID"}
    }, indent=2) + "\n")
    assert sum(v["count"] for v in created.values()) == 7
    report = {"source_jar_filename": MOD, "official_source_sha256": actual,
              "scope": "two exact Ancient Mines templates only",
              "old_item": OLD, "new_item": NEW, "replacements": 7,
              "source_templates": created,
              "runtime_tested": False,
              "redistribution": "private test only, do not publish author-owned NBT"}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"source_sha256": actual, "templates": 2,
                      "replacements": 7, "report": str(REPORT)}))
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path)
    p.add_argument("--source-sha256")
    p.add_argument("--no-download", action="store_true")
    args = p.parse_args()
    if args.jar:
        assert args.source_sha256, "explicit --jar requires --source-sha256"
        make(args.jar, expected_sha=args.source_sha256)
    else:
        assert not args.no_download
        from audit_remaining_jigsaw_nbt_086 import indexed_jars, manifest_pairs, fetch
        refs = manifest_pairs()
        fid = refs[PROJECT]  # Pinned 1.21.1 IDAS file from original AO manifest
        jar_record = indexed_jars()[MOD]
        s = str(fid)
        url = ("https://mediafilez.forgecdn.net/files/" +
               f"{int(s[:-3])}/{int(s[-3:]):03d}/" + quote(MOD))
        binary = fetch(url, limit=100_000_000, timeout=120)
        assert sha(binary) == jar_record["sha256"], "Pinned IDAS JAR SHA mismatch"
        path = ROOT / "build/native-jars/idas-source.jar"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(binary)
        make(path, expected_sha=jar_record["sha256"])


if __name__ == "__main__":
    main()
