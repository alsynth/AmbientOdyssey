#!/usr/bin/env python3
"""Ambient Odyssey v0.4 experimental: read-only ZIP/installed-instance preflight.

This is NOT a Minecraft runtime test and DOES NOT install, delete or edit mods.
Python 3.10+ standard library only. Output intentionally excludes raw log lines,
full paths, usernames and IPs. Use --help for profile/ZIP modes.
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "0.4.1-experimental-trek-structures"
EXPECTED_COUNT = 331
CRITICAL_PINS = {
    1418999: (8296269, "Trek structure expansion"),
    618790: (7033510, "Mine Cells"),
    318449: (5845879, "Cardinal Components API"),
    890127: (8654089, "Sinytra Connector"),
    889079: (8726480, "Forgified Fabric API"),
    532610: (6785734, "NeoForge owo-lib"),
    520110: (6375480, "Iceberg"),
    623764: (5988164, "JamLib"),
    1202066: (8952784, "Questlog"),
}
EXTRA_PINS = {
    895603: (5924310, "Armor Trim Item Fix"),
    315811: (6530833, "Shulker Box Tooltip"),
    233071: (8697050, "Crafting Tweaks"),
    407206: (7057837, "Chat Heads"),
    535489: (7032247, "Sound Physics Remastered"),
    388800: (6794589, "Polymorph"),
    637808: (8309583, "Brewin' And Chewin'"),
    352222: (8828150, "Dimensional Dungeons"),
    1668579: (9084406, "Ancient Remnants"),
    1473837: (8450385, "TarotCards Remastered"),
    961988: (6179576, "Aquaculture Delight"),
    1365790: (9111385, "End Remastered Additions"),
}
EXPECTED_JARS = {
    "minecells": "minecells-2.0.3.jar",
    "cardinal-components": "cardinal-components-api-6.1.2.jar",
    "connector": "connector-2.0.0-beta.17+1.21.1-full.jar",
    "forgified_fabric_api": "forgified-fabric-api-0.116.15+2.3.5+1.21.1.jar",
    "owo": "owo-lib-neoforge-0.12.15.5-beta.1+1.21.jar",
    "iceberg": "Iceberg-1.21.1-neoforge-1.3.0.jar",
    "jamlib": "jamlib-neoforge-1.2.2-build.2+1.21.1.jar",
    "armor_trim_item_fix": "ArmorTrimItemFix-neoforge-1.21.1-1.2.0.jar",
    "shulker_box_tooltip": "shulkerboxtooltip-neoforge-5.1.6+1.21.1.jar",
    "crafting_tweaks": "craftingtweaks-neoforge-1.21.1-21.1.11.jar",
    "chat_heads": "chat_heads-0.14.0-neoforge-1.21.jar",
    "sound_physics": "sound-physics-remastered-neoforge-1.21.1-1.5.1.jar",
    "polymorph": "polymorph-neoforge-1.1.0+1.21.1.jar",
    "brewin_and_chewin": "BrewinAndChewin-neoforge-4.5.0+1.21.1.jar",
    "dimensional_dungeons": "dimdungeons-210-neoforge-1.21.1.jar",
    "ancient_remnants": "ancient_remnants-1.5.2+1.21.1-neoforge.jar",
    "tarotcards": "tarotcards-2.3.5-neoforge-1.21.1.jar",
    "aquaculture_delight": "aquaculturedelight-1.2.0-neoforge-1.21.1.jar",
    "end_remastered_additions": "endrem_additions-neoforge-1.2.0.jar",
    "questlog": "questlog-neoforge-1.21.1-3.4.1.jar",
}
PATTERNS = {
    "fatal_mixin": r"MixinApplyError|MixinTransformerError|Mixin config .* failed",
    "mod_loading": r"ModLoadingException|LoadingFailedException|Mod loading has failed",
    "missing_class": r"NoClassDefFoundError|ClassNotFoundException",
    "binary_linkage": r"NoSuchMethodError|NoSuchFieldError|IncompatibleClassChangeError",
    "registry_or_datapack": r"Failed to parse.*(registry|tag|recipe|loot|datapack)|Couldn't load tag|Unknown registry key",
    "out_of_memory": r"OutOfMemoryError|java heap space",
    "server_stall": r"Can't keep up! Is the server overloaded",
}
CORE = {"minecells", "connector", "forgified_fabric_api", "owo", "iceberg", "jamlib", "cardinal-components"}

def check_zip(path):
    out = {"checked": True, "issues": [], "warnings": [], "facts": {}}
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            out["facts"]["archive_bytes"] = path.stat().st_size
            out["facts"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            out["facts"]["entries"] = len(names)
            if z.testzip() is not None:
                out["issues"].append("Archive CRC/integrity failure")
            if len(names) != len(set(names)):
                out["issues"].append("Duplicate archive paths")
            if "manifest.json" not in names:
                out["issues"].append("Missing root manifest.json")
                return out
            m = json.loads(z.read("manifest.json"))
            files = m.get("files", [])
            by_id = {int(e["projectID"]): int(e["fileID"]) for e in files}
            out["facts"]["manifest_version"] = m.get("version")
            out["facts"]["manifest_refs"] = len(files)
            out["facts"]["primary_loader"] = m.get("minecraft", {}).get("modLoaders")
            if m.get("version") != VERSION:
                out["issues"].append("Wrong experimental candidate manifest version")
            if len(by_id) != EXPECTED_COUNT or len(files) != EXPECTED_COUNT:
                out["issues"].append("Expected 331 unique CurseForge project references")
            if m.get("minecraft", {}).get("version") != "1.21.1":
                out["issues"].append("Wrong Minecraft version")
            if m.get("minecraft", {}).get("modLoaders") != [{"id":"neoforge-21.1.252", "primary":True}]:
                out["issues"].append("Wrong primary NeoForge loader")
            for pid,(fid,label) in {**CRITICAL_PINS,**EXTRA_PINS}.items():
                if by_id.get(pid) != fid:
                    out["issues"].append(label + " exact project/file pin missing")
            for disallowed in (306612,284876,631098,1100379,368293,1071336):
                if disallowed in by_id:
                    out["issues"].append("Known conflicting project ID in manifest: " + str(disallowed))
            bundled = [n for n in names if n.startswith("overrides/mods/") and n.endswith(".jar")]
            out["facts"]["embedded_jar_count"] = len(bundled)
            if len(bundled) > 1 or (bundled and bundled != ["overrides/mods/neoreefredux-1.0.jar"]):
                out["issues"].append("Unexpected third-party JAR embedded in ZIP")
            if not bundled:
                out["warnings"].append("Reference-only export; NeoReefRedux is NOT embedded")
            necessary = [
                "overrides/config/paxi/datapacks/ao_server_rules/data/ambient_odyssey/function/server_rules.mcfunction",
                "overrides/config/paxi/datapacks/ao_technical_fixes/pack.mcmeta",
                "overrides/config/paxi/datapacks/ao_v041_runtime_fixes/pack.mcmeta",
                "overrides/config/questlog-client.toml",
            ]
            for name in necessary:
                if name not in names:
                    out["issues"].append("Missing important data override: " + name.split("/")[-1])
    except (OSError,zipfile.BadZipFile,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        out["issues"].append("Unable to parse requested ZIP: " + type(exc).__name__)
    return out

def profile_root(p):
    p = p.expanduser().resolve()
    if (p / "mods").is_dir(): return p
    if (p / ".minecraft" / "mods").is_dir(): return p / ".minecraft"
    return p

def check_profile(profile):
    base = profile_root(profile)
    out = {"checked": True, "issues": [], "warnings": [], "facts": {}}
    mods = base / "mods"
    if not mods.is_dir():
        out["issues"].append("Mods folder absent; choose the installed instance directory")
        return out
    names = sorted(p.name for p in mods.iterdir() if p.is_file() and p.suffix.lower() in (".jar", ".disabled"))
    low = {n.lower() for n in names}
    out["facts"]["mod_files"] = len(names)
    out["facts"]["critical_present"] = {}
    out["facts"]["extra_new_present"] = {}
    for label, fn in EXPECTED_JARS.items():
        found = fn.lower() in low
        category = "critical_present" if label in CORE else "extra_new_present"
        out["facts"][category][label] = found
        if not found:
            (out["issues"] if label in CORE else out["warnings"]).append(
                ("Missing core binary: " if label in CORE else "New addon not found by exact filename: ") + label)
    for forbidden in ("fabric-api-", "dimdoors-", "dimensionaldoors-"):
        matches = [n for n in low if n.startswith(forbidden)]
        if matches:
            out["issues"].append("Forbidden/conflicting installed mod family: " + forbidden)
    for prefix in ("connector-", "owo-lib-", "forgified-fabric-api-"):
        matches = [n for n in low if n.startswith(prefix)]
        if len(matches) > 1:
            out["issues"].append("Duplicate bridge/library JAR family: " + prefix)
    logs = [base / "logs" / "latest.log", base / "logs" / "debug.log"]
    reports = defaultdict(int)
    inspected = []
    for file in logs:
        if file.is_file():
            try:
                # Read only recent 3 MiB, without logging raw lines or private addresses.
                with file.open("rb") as fh:
                    fh.seek(max(0, file.stat().st_size - 3_000_000))
                    data = fh.read().decode("utf-8", "replace")
                inspected.append(file.name)
                for label,pattern in PATTERNS.items():
                    reports[label] += len(re.findall(pattern, data, re.IGNORECASE))
            except OSError:
                out["warnings"].append("A log file was unreadable")
    out["facts"]["logs_checked"] = inspected
    out["facts"]["log_signal_counts"] = dict(reports)
    if not inspected:
        out["warnings"].append("No startup logs yet; this is a pre-launch file audit only")
    elif any(reports.get(k,0) for k in ("fatal_mixin","mod_loading","missing_class","binary_linkage","out_of_memory")):
        out["warnings"].append("Startup logs contain severe error signatures; inspect the original local logs")
    if (base / "config" / "paxi").exists():
        out["facts"]["paxi_present"] = True
    else:
        out["warnings"].append("Paxi configuration directory absent or not initialized")
    out["warnings"].append("Exact filename checks may flag CurseForge-renamed JARs; inspect the actual mod metadata before changing files")
    out["warnings"].append("Passing this report cannot establish runtime compatibility, correct gameplay or server sidedness")
    return out

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--zip", type=Path, help="CurseForge experimental export ZIP")
    group.add_argument("--profile", type=Path, help="Installed CurseForge instance directory (containing mods/)")
    parser.add_argument("--report", type=Path, help="Optional output JSON path; never touches the instance")
    a = parser.parse_args()
    details = check_zip(a.zip) if a.zip else check_profile(a.profile)
    result = {"pack": VERSION, "mode": "zip" if a.zip else "profile",
              "status": "BLOCKED" if details["issues"] else "PREFLIGHT_PASS",
              "runtime_verified": False, **details}
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(raw, end="")
    if a.report:
        if a.report.exists():
            parser.error("Refusing to overwrite an existing report; choose a new --report path")
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(raw, encoding="utf-8")
    return 2 if details["issues"] else 0

if __name__ == "__main__":
    sys.exit(main())
