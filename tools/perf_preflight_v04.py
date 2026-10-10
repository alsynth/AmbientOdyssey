#!/usr/bin/env python3
"""Read-only static preflight for AO CurseForge import ZIPs and outer Actions artifacts.

Never measures in-game FPS/TPS, downloaded JAR integrity, or server compatibility.
"""
import argparse
import collections
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

CONFIGS = {
    "options": "overrides/config/defaultoptions/options.txt",
    "embeddium": "overrides/config/embeddium-options.json",
    "immediatelyfast": "overrides/config/immediatelyfast.json",
    "spark": "overrides/config/spark/config.json",
    "modernfix": "overrides/config/modernfix-common.toml",
    "lithium": "overrides/config/lithium.properties",
    "ferritecore": "overrides/config/ferritecore-mixin.toml",
    "structure_essentials": "overrides/config/structureessentials.json",
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_import_bytes(path, variant="references"):
    raw = Path(path).read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if "manifest.json" in archive.namelist():
            return raw, Path(path).name, False
        suffix = "-PRIVATE.zip" if variant == "private" else "-CF-References.zip"
        matches = [n for n in archive.namelist() if n.endswith(suffix)]
        if len(matches) != 1:
            raise ValueError("Expected one inner import ZIP ending " + suffix)
        raw = archive.read(matches[0])
        with zipfile.ZipFile(io.BytesIO(raw)) as inner:
            if "manifest.json" not in inner.namelist():
                raise ValueError("Inner ZIP has no root manifest.json")
        return raw, matches[0], True

def scan_bytes(data, inner_name="import.zip", outer=False, expected_refs=331):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        info = [x for x in archive.infolist() if not x.is_dir()]
        names = [x.filename for x in info]
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or "\\" in name:
                raise ValueError("Unsafe ZIP path: " + name)
        if len(set(names)) != len(names):
            raise ValueError("Duplicate ZIP member names")
        if "manifest.json" not in names:
            raise ValueError("Missing root manifest.json")
        manifest = json.loads(archive.read("manifest.json"))
        files = manifest.get("files", [])
        refs = [(f.get("projectID"), f.get("fileID")) for f in files]
        issues = []
        if len(files) != expected_refs:
            issues.append("Expected %s pinned refs, got %s" % (expected_refs, len(files)))
        if len({x[0] for x in refs}) != len(refs):
            issues.append("Duplicate CurseForge project ID")
        if len({n.casefold() for n in names}) != len(names):
            issues.append("Case-insensitive ZIP path collision")
        cfg = {}
        for label, name in CONFIGS.items():
            if name not in names:
                cfg[label] = {"present": False}
                continue
            raw = archive.read(name)
            item = {"present": True, "sha256": sha(raw)}
            if label == "options":
                lines = [line.split(":", 1) for line in raw.decode("utf-8").splitlines() if ":" in line]
                settings = dict(lines)
                item["settings"] = {k: settings.get(k) for k in (
                    "renderDistance", "simulationDistance", "maxFps", "enableVsync",
                    "soundCategory_weather", "soundCategory_ambient", "soundCategory_block"
                )}
            elif label in ("spark", "embeddium", "immediatelyfast"):
                parsed = json.loads(raw)
                if label == "spark":
                    item["backgroundProfiler"] = parsed.get("backgroundProfiler")
                if label == "embeddium":
                    item["performance"] = parsed.get("performance", {})
            cfg[label] = item
        if cfg["spark"].get("backgroundProfiler") is True:
            issues.append("MEASURE: Spark backgroundProfiler enabled; overhead unknown")
        if any(n.startswith("overrides/config/spark/tmp") for n in names):
            issues.append("REVIEW: temporary Spark cache/report paths shipped")
        if any(n.startswith("overrides/mods/") and n.endswith(".jar") for n in names):
            issues.append("DISTRIBUTION: bundled JARs need license/server-sidedness review")
        overrides = {n: sha(archive.read(n)) for n in names if n.startswith("overrides/")}
        report = {
            "test_level": "STATIC_ONLY_NOT_RUNTIME_TESTED",
            "inner_archive": inner_name, "is_outer_actions_artifact": outer,
            "sha256": sha(data), "member_count": len(info),
            "manifest": {"version": manifest.get("version"), "minecraft": manifest.get("minecraft"),
                "pinned_references": len(refs), "unique_projects": len({p for p, _ in refs}),
                "roster_sha256": sha(json.dumps(sorted(refs)).encode())},
            "configuration_samples": cfg, "issues_to_investigate": issues,
            "largest_files": [{"path": i.filename, "bytes": i.file_size}
                for i in sorted(info, key=lambda i: i.file_size, reverse=True)[:8]],
            "overrides_count": len(overrides),
            "limitations": ["Does not inspect downloaded mod JARs", "No actual client/server startup",
                "No FPS, frametime, MSPT, TPS, GC or chunk-generation measurements"]
        }
        return report, overrides

def compare(before, after):
    old_report, old_files = before
    new_report, new_files = after
    left, right = set(old_files), set(new_files)
    return {
        "same_pinned_roster": old_report["manifest"]["roster_sha256"] == new_report["manifest"]["roster_sha256"],
        "added_overrides": sorted(right - left),
        "removed_overrides": sorted(left - right),
        "modified_overrides": sorted(k for k in left & right if old_files[k] != new_files[k])
    }

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path, help="Inner CurseForge ZIP or outer GitHub artifact ZIP")
    p.add_argument("--variant", choices=["references", "private"], default="references")
    p.add_argument("--compare-to", type=Path)
    p.add_argument("--expected-refs", type=int, default=331)
    p.add_argument("--output", type=Path)
    args = p.parse_args(argv)
    try:
        raw, name, outer = read_import_bytes(args.archive, args.variant)
        current = scan_bytes(raw, name, outer, args.expected_refs)
        result = {"candidate": current[0]}
        if args.compare_to:
            old, old_name, old_outer = read_import_bytes(args.compare_to, args.variant)
            result["comparison"] = compare(scan_bytes(old, old_name, old_outer, expected_refs=0 if False else args.expected_refs), current)
        encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 0
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, UnicodeDecodeError) as exc:
        print("Static preflight failed: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
