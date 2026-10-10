#!/usr/bin/env python3
"""Ambient Odyssey candidate CurseForge ZIP preflight; standard library only.

Examples:
  python tools/preflight_v04.py path/to/candidate.zip
  python tools/preflight_v04.py path/to/candidate.zip --require-minecells
No Minecraft launch or mod binary compatibility is implied by a PASS.
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath
from hashlib import sha256

MINECELLS_PROJECT = 618790
MINECELLS_FILE = 7033510

def check(path, require_minecells=False):
    problems = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if z.testzip() is not None:
            problems.append("ZIP CRC failed")
        if len(names) != len(set(names)):
            problems.append("Duplicate ZIP members")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or "\\" in name or name.startswith("/"):
                problems.append(f"Unsafe ZIP path: {name}")
        if "manifest.json" not in names:
            problems.append("Missing root manifest.json")
            return problems, 0
        if not any(n.startswith("overrides/") for n in names):
            problems.append("Missing overrides/")
        if any(n.startswith("overrides/mods/") and n.lower().endswith(".jar") for n in names):
            problems.append("Bundled third-party mod jar inside overrides/mods/")
        manifest = json.loads(z.read("manifest.json"))
        if manifest.get("minecraft", {}).get("version") != "1.21.1":
            problems.append("Minecraft version is not 1.21.1")
        loaders = manifest.get("minecraft", {}).get("modLoaders", [])
        if not any(x.get("id") == "neoforge-21.1.252" and x.get("primary") for x in loaders):
            problems.append("Unexpected primary NeoForge loader")
        entries = manifest.get("files", [])
        by_project = {}
        for e in entries:
            pid, fid = e.get("projectID"), e.get("fileID")
            if pid in by_project:
                problems.append(f"Duplicate CurseForge project {pid}")
            by_project[pid] = fid
        if require_minecells and by_project.get(MINECELLS_PROJECT) != MINECELLS_FILE:
            problems.append("Mine Cells 618790:7033510 not pinned in manifest")
        if MINECELLS_PROJECT in by_project:
            print("WARNING: Mine Cells is Fabric-only; this ZIP check cannot verify Sinytra Connector interoperability.")
        return problems, len(entries)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("zip", type=Path)
    p.add_argument("--require-minecells", action="store_true")
    args = p.parse_args()
    if not args.zip.is_file():
        p.error("ZIP file not found")
    problems, count = check(args.zip, args.require_minecells)
    print(f"file={args.zip} bytes={args.zip.stat().st_size} sha256={sha256(args.zip.read_bytes()).hexdigest()} curseforge_projects={count}")
    for issue in problems:
        print("FAIL:", issue)
    print("STATIC PREFLIGHT:", "FAIL" if problems else "PASS (does not verify Minecraft runtime)")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
