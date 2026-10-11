#!/usr/bin/env python3
"""Inspection-only report of official Streams Reflowing 2.14.4 binary; no redistribution."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile

VERSION = "2.14.4"
FILE_ID = 9060294
NAME = f"StreamsReflowing-1.21.1-neoforge-{VERSION}.jar"
URLS = [
    f"https://mediafilez.forgecdn.net/files/9060/294/{NAME}",
    f"https://edge.forgecdn.net/files/9060/294/{NAME}",
]
FOCUS = ("mixin", "structure", "worldgen", "chunk", "generation", "gen", "level", "region", "terrain", "hydro", "carve", "feature")

def acquire(dest: Path):
    if dest.is_file():
        return
    errors = []
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AmbientOdyssey-compat-audit/0.1"})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) < 50000 or data[:2] != b"PK":
                raise ValueError("Response is not a jar archive")
            dest.write_bytes(data)
            print("Source downloaded:", url)
            return
        except Exception as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError("Could not download pinned official jar:\n" + "\n".join(errors))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, default=Path("streams.jar"))
    p.add_argument("--out", type=Path, default=Path("build/streams-bytecode-audit"))
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    acquire(args.jar)
    jar_sha = hashlib.sha256(args.jar.read_bytes()).hexdigest()
    inventory = {"name": NAME, "file_id": FILE_ID, "sha256": jar_sha, "size": args.jar.stat().st_size}
    dump_dir = args.out / "javap"
    dump_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(args.jar) as z:
        entries = z.namelist()
        mixins = []
        for path in entries:
            if path.endswith(".json") and "mixin" in path.lower():
                try:
                    value = json.loads(z.read(path).decode("utf-8"))
                    if isinstance(value, dict) and ("mixins" in value or "client" in value or "server" in value):
                        mixins.append({"path": path, "data": value})
                except Exception:
                    pass
        inventory["mixin_configs"] = mixins
        inventory["neo_metadata_files"] = {}
        for path in entries:
            if "mods.toml" in path or path.endswith("MANIFEST.MF"):
                inventory["neo_metadata_files"][path] = z.read(path).decode("utf-8", "replace")[:4000]
        java_classes = [x[:-6].replace("/", ".") for x in entries if x.endswith(".class") and not x.startswith("META-INF/")]
        relevant = sorted(c for c in java_classes if any(x in c.lower() for x in FOCUS))
        focus = [c for c in relevant if any(x in c.lower() for x in ("mixin", "structure", "chunk", "worldgen", "feature", "generator"))]
        inventory["class_count"] = len(java_classes)
        inventory["relevant_classes"] = relevant
        inventory["focus_disassembly"] = focus
        (args.out / "mixin-configs.json").write_text(json.dumps(mixins, indent=2))
        (args.out / "manifest-and-classes.json").write_text(json.dumps(inventory, indent=2))
        print("JAR:", NAME, jar_sha, "classes:", len(java_classes))
        for m in mixins:
            print("MIXIN CONFIG:", m["path"], json.dumps(m["data"])[:6000])
        print("RELEVANT CLASS NAMES:\n" + "\n".join(relevant[:450]))
        for i, clazz in enumerate(focus[:120]):
            proc = subprocess.run(["javap", "-cp", str(args.jar), "-p", "-c", "-v", clazz], capture_output=True, text=True, timeout=25)
            if proc.returncode:
                print("javap FAILED", clazz, proc.stderr[:200])
                continue
            (dump_dir / (f"{i:03d}-" + clazz.replace(".", "_") + ".txt")).write_text(proc.stdout)
            lines = proc.stdout.splitlines()
            interesting = []
            for k, line in enumerate(lines):
                if any(token in line.lower() for token in ("org.spongepowered.asm.mixin.mixin", "inject", "redirect", "wrapoperation", "structurestart", "structureplacement", "findgenerationpoint", "getdimension", "getlevel", "generationstep", "getresourcekey")):
                    interesting.append(" | ".join(lines[max(0,k-1):min(len(lines),k+2)]).strip()[:480])
            print("CLASS:", clazz, "\n", "\n".join(interesting[:18]))
    print("REPORT_DIR:", args.out)

if __name__ == "__main__":
    main()
