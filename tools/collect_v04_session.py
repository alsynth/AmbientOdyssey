#!/usr/bin/env python3
"""Ambient Odyssey v0.4h: privacy-limited, read-only test-session snapshot.

Requires Python 3.11+. Does not launch Minecraft, upload files, copy raw logs,
copy screenshots, access networks, or alter the selected game directory.
"""
import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.audit_installed_jars_v04 import get_dir, scan, evaluate
from tools.diagnose_v04_instance import check_profile

VERSION = "0.4.0-experimental-minecells-fg-questlog"
VIDEO_KEYS = {"renderDistance", "simulationDistance", "guiScale",
              "maxFps", "enableVsync", "soundCategory_weather",
              "soundCategory_block"}

def selected_options(profile):
    file = get_dir(profile).parent / "options.txt"
    values = {}
    if file.is_file():
        try:
            with file.open(encoding="utf-8", errors="replace") as inp:
                for line in inp:
                    name, sep, value = line.partition(":")
                    if sep and name in VIDEO_KEYS:
                        val = value.strip()
                        if len(val) <= 16 and all(c in "0123456789.-truefals" for c in val):
                            values[name] = val
        except OSError:
            pass
    return values

def compact_scan(s):
    return {
        "jar_count": s["jar_count"], "metadata_read": s["metadata_read"],
        "formats": s["formats"], "duplicate_mod_ids": s["duplicate_mod_ids"][:40],
        "unreadable_files": s["invalid_jars"][:40],
        "unknown_metadata_files": s["unknown_metadata"][:40],
        "unresolved_declared_dependencies": s["unresolved_dependencies"][:80],
        "unresolved_omitted": max(0, len(s["unresolved_dependencies"]) - 80)
    }

def report(profile, server=None):
    p = check_profile(Path(profile))
    c = scan(get_dir(profile))
    verdict = evaluate(c)
    data = {
        "pack": VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "runtime_tested_by_snapshot": False,
        "profile_preflight": p,
        "video_settings": selected_options(profile),
        "installed_mods": compact_scan(c),
        "metadata_issues": verdict["issues"],
        "metadata_warnings": verdict["warnings"],
        "historical_inaccessible_native_records": 23
    }
    if server is not None:
        sr = scan(get_dir(server))
        diff = evaluate(c, sr)
        data["server_mods"] = compact_scan(sr)
        data["server_comparison"] = diff.get("comparison", {})
        data["server_metadata_issues"] = diff["issues"]
        data["server_metadata_warnings"] = diff["warnings"]
    return data

def summary(data):
    profile = data["profile_preflight"]
    facts = profile.get("facts", {})
    rows = [
        "# Ambient Odyssey v0.4h first-test summary", "",
        "**STATIC SNAPSHOT ONLY. No Minecraft runtime or multiplayer test performed.**", "",
        f"- Pack: {data['pack']}",
        f"- Snapshot UTC: {data['created_utc']}",
        f"- Profile issues: {len(profile.get('issues', []))}",
        f"- JAR files: {data['installed_mods']['jar_count']}",
        f"- Readable top-level mod metadata: {data['installed_mods']['metadata_read']}",
        f"- Duplicate mod ID groups: {len(data['installed_mods']['duplicate_mod_ids'])}",
        f"- Startup logs checked: {', '.join(facts.get('logs_checked', [])) or 'none'}",
        f"- Startup error signal counts: {json.dumps(facts.get('log_signal_counts', {}), sort_keys=True)}",
        f"- Selected video options: {json.dumps(data['video_settings'], sort_keys=True)}", "",
        "No raw log text, screenshots, full local paths, player names, account data,",
        "or server addresses are copied. JAR filenames are included: review before sharing.", "",
        "## Actual player test results — fill in manually", "",
        "| Check | Status | Screenshot / log reference |",
        "|---|---|---|",
        "| First main menu, no loading crash | NOT TESTED | |",
        "| Fresh disposable world generation and reload | NOT TESTED | |",
        "| Questlog journal button visible/clickable at GUI scale 3 | NOT TESTED | |",
        "| Questlog hotkey works; no quest content expected | NOT TESTED | |",
        "| JEI, FTB Quests, Accessories and Curios GUI fit | NOT TESTED | |",
        "| Mine Cells portal, death, boss, return | NOT TESTED | |",
        "| Dimensional Dungeons key/portal/return | NOT TESTED | |",
        "| Two-player server join, save and restart | NOT TESTED | |", "",
        "See field-sheet.md for the complete test order. Static checks never"
        " automatically mark gameplay cells PASS.", ""
    ]
    return "\n".join(rows)

def save_snapshot(profile, output, server=None):
    data = report(profile, server)
    source = ROOT / "docs/testing/V04H_TEST_SESSION_FIELD_SHEET.md"
    sheet = source.read_text(encoding="utf-8") if source.is_file() else ""
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("report.json", json.dumps(data, indent=2, sort_keys=True) + "\n")
        z.writestr("summary.md", summary(data))
        z.writestr("field-sheet.md", sheet)
    return data

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", type=Path, required=True,
                    help="Installed disposable CurseForge instance")
    ap.add_argument("--server", type=Path,
                    help="Optional separate dedicated server installation")
    ap.add_argument("--output", type=Path, required=True,
                    help="New ZIP filename; never overwrite existing evidence")
    args = ap.parse_args()
    if args.output.exists():
        ap.error("Output already exists. Refusing to overwrite evidence.")
    if not get_dir(args.profile).is_dir():
        ap.error("Installed profile mods directory absent")
    if args.server and not get_dir(args.server).is_dir():
        ap.error("Dedicated server mods directory absent")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = save_snapshot(args.profile, args.output, args.server)
    print(json.dumps({"created": args.output.name,
          "client_jar_count": data["installed_mods"]["jar_count"],
          "runtime_tested": False}, indent=2))
    print("ZIP excludes raw logs/screenshots; review metadata before sharing.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
