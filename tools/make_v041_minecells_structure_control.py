#!/usr/bin/env python3
"""Build a Mine Cells STRUCTURE-PLACEMENT CONTROL from the validated 331-ref ZIP.

This creates a separate importable CurseForge test package; it NEVER changes
release-lock.json, the 331-ref build or any working/rollback source branch.
It excludes exactly three suspected worldgen participants to isolate a group
interaction. Success cannot be claimed without testing a fresh Minecraft world.

Usage:
  python tools/make_v041_minecells_structure_control.py BASELINE.zip OUTPUT.zip
  python tools/make_v041_minecells_structure_control.py --verify OUTPUT.zip --baseline BASELINE.zip
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

EXCLUDED = {
    832882: "Structure Essentials (structure placement mixins)",
    1430156: "Noisiumed (noise/chunk generation optimizations)",
    1581408: "Streams Reflowing (dimension-wide river/terrain hook)",
}
BASELINE_COUNT = 331
TEST_COUNT = BASELINE_COUNT - len(EXCLUDED)
NAME = "Ambient Odyssey 0.4.1 - Mine Cells Structure Control TEST"
VERSION = "0.4.1-experimental-minecells-structure-control"
REQUIRED_BRIDGE = {
    618790: 7033510,   # Mine Cells Fabric through Sinytra
    890127: 8654089,   # Sinytra Connector
    889079: 8726480,   # Forgified Fabric API
    532610: 6785734,   # owo-lib NeoForge
    318449: 5845879,   # Cardinal Components API
}

def read_manifest(z):
    return json.loads(z.read("manifest.json"))

def refs(manifest):
    files = manifest["files"]
    result = {e["projectID"]: e["fileID"] for e in files}
    assert len(files) == len(result), "duplicate projectIDs in manifest"
    return result

def validate_baseline(z):
    assert z.testzip() is None, "baseline ZIP CRC invalid"
    m = read_manifest(z)
    pins = refs(m)
    assert len(pins) == BASELINE_COUNT, len(pins)
    assert all(pid in pins for pid in EXCLUDED), "source candidate missing a group-isolation mod"
    assert all(pins.get(pid) == fid for pid, fid in REQUIRED_BRIDGE.items()), "Mine Cells bridge altered"
    assert m["minecraft"]["version"] == "1.21.1"
    assert m["minecraft"]["modLoaders"][0]["id"] == "neoforge-21.1.252"
    assert "overrides/config/paxi/datapacks/ao_compatibility/data/streamsreflowing/tags/worldgen/biome/no_streams.json" not in z.namelist(), "wrong input: hydrology-isolation build instead of combined six-fix"
    return m, pins

def validate_test(z, source_refs):
    assert z.testzip() is None, "test ZIP CRC invalid"
    members = z.namelist()
    assert len(members) == len(set(members)), "duplicate ZIP entries"
    assert "manifest.json" in members and any(p.startswith("overrides/") for p in members)
    for name in members:
        p = PurePosixPath(name)
        assert not p.is_absolute() and ".." not in p.parts and "\\" not in name, f"unsafe ZIP path: {name}"
    assert not any(n.startswith("overrides/mods/") and n.lower().endswith(".jar") for n in members), "embedded third party JAR"
    m = read_manifest(z)
    out_refs = refs(m)
    assert m["name"] == NAME and m["version"] == VERSION
    assert len(out_refs) == TEST_COUNT, len(out_refs)
    assert out_refs == {k:v for k,v in source_refs.items() if k not in EXCLUDED}, "unexpected differences in pinned mods"
    for pid, fid in REQUIRED_BRIDGE.items():
        assert out_refs.get(pid) == fid, f"lost Mine Cells bridge: {pid}"
    assert not any(pid in out_refs for pid in EXCLUDED)
    assert "overrides/config/paxi/datapacks/ao_compatibility/data/streamsreflowing/tags/worldgen/biome/no_streams.json" not in members
    print(f"PASS diagnostic control: {len(out_refs)} CurseForge references, exactly 3 removed, original overrides intact")
    print("NOT RUNTIME TESTED: verify full Mine Cells dungeon, safe entry, stairs and Promenade portal in a NEW world")

def build(source, target):
    assert source.resolve() != target.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, "r") as src:
        m, source_refs = validate_baseline(src)
        manifest = dict(m)
        manifest["name"] = NAME
        manifest["version"] = VERSION
        manifest["files"] = [e for e in m["files"] if e["projectID"] not in EXCLUDED]
        with zipfile.ZipFile(target, "w", allowZip64=True) as z:
            for item in src.infolist():
                if item.filename == "manifest.json":
                    data = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
                else:
                    data = src.read(item.filename)
                z.writestr(item, data)
    with zipfile.ZipFile(target) as z:
        validate_test(z, source_refs)
    print(f"OUTPUT {target.name}, bytes={target.stat().st_size}, sha256={hashlib.sha256(target.read_bytes()).hexdigest()}")

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path, nargs="?")
    p.add_argument("target", type=Path, nargs="?")
    p.add_argument("--verify", type=Path)
    p.add_argument("--baseline", type=Path)
    a = p.parse_args()
    if a.verify:
        assert a.baseline, "--baseline required with --verify"
        with zipfile.ZipFile(a.baseline) as z:
            _, oldrefs = validate_baseline(z)
        with zipfile.ZipFile(a.verify) as z:
            validate_test(z, oldrefs)
    else:
        if not a.source or not a.target:
            p.error("pass BASELINE.zip OUTPUT.zip")
        build(a.source, a.target)

if __name__ == "__main__":
    main()
