#!/usr/bin/env python3
"""Read-only scan of installed Minecraft mod JAR resources for invalid item IDs.

Does not modify JAR files, worlds, saves or the CurseForge profile.
The scan locates likely source assets; a match is NOT automatic proof that
a particular asset was loaded at the observed chunk position.
Usage:
    py tools/trace_invalid_worldgen_items.py "C:/Users/.../curseforge/minecraft/Instances/AO/mods"
"""
import argparse
import gzip
import json
from pathlib import Path
from zipfile import ZipFile, BadZipFile

PATTERNS = (b"redeco:hammer", b"quark:frog_leg")
# minecraft:air is intentionally excluded by default: it is pervasive in
# legitimate NBT / configuration and its presence alone is not an invalid stack.
EXTS = (".nbt", ".json", ".json5", ".snbt", ".mcfunction", ".toml")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mods", type=Path, help="Path to the installed Minecraft mods directory")
    p.add_argument("--output", type=Path, default=Path("ao-invalid-item-sources.json"))
    args = p.parse_args()
    if not args.mods.is_dir():
        p.error(f"Not a directory: {args.mods}")
    matches = []
    scanned = 0
    for mod in sorted(args.mods.glob("*.jar")):
        try:
            with ZipFile(mod) as z:
                for info in z.infolist():
                    if not info.filename.lower().endswith(EXTS) or info.file_size > 200_000_000:
                        continue
                    scanned += 1
                    try:
                        data = z.read(info)
                        if data[:2] == bytes((31, 139)):
                            data = gzip.decompress(data)
                    except (OSError, BadZipFile, EOFError, RuntimeError, ValueError):
                        continue
                    for key in PATTERNS:
                        if key in data:
                            matches.append({"jar": mod.name, "resource":info.filename, "token": key.decode()})
        except (OSError, BadZipFile):
            matches.append({"jar": mod.name, "error": "Could not read JAR"})
    report = {"read_only":True,"mods_scanned":len(list(args.mods.glob("*.jar"))),
              "resources_scanned":scanned,"matches":matches,
              "note":"Review matched resources before replacing anything. No global ID substitution is safe."}
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved report: {args.output.resolve()}")

if __name__=="__main__":
    main()
