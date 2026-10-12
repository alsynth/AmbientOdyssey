#!/usr/bin/env python3
"""Package the two-addon update, optionally patching an exact v0.4.5 import."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
TRIM = "ao-affix-trims-0.1.1-experimental.jar"
QUEST = "ao-questlog-betterinventory-0.1.5.jar"
OLD_VERSION = "0.4.5-experimental-custom-integration"
NEW_VERSION = "0.4.5.1-affix-trims-questlog-fix-test"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def jar(path, modid, version, required, excluded):
    data = path.read_bytes()
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        meta = z.read("META-INF/neoforge.mods.toml").decode()
        assert modid in meta and version in meta
        assert required in z.namelist() and excluded not in z.namelist()
    return data

def write_zip(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as z:
        for name, data in sorted(entries.items()):
            info = ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, data)
    with ZipFile(path) as z:
        assert z.testzip() is None
    print(path, sha(path.read_bytes()))

def run(args):
    trim = jar(args.trim, "ao_affix_trims", "0.1.1-experimental",
               "dev/ambientodyssey/affixtrims/mixin/AffixLootCreationMixin.class",
               "dev/ambientodyssey/affixtrims/AffixTrimGameTests.class")
    quest = jar(args.quest, "aoquestlogbridge", "0.1.5",
                "dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge.class",
                "dev/ambientodyssey/questlogbridge/QuestlogPlacementQA.class")
    entries = {
        "mods/" + TRIM: trim,
        "mods/" + QUEST: quest,
        "INSTALL.cmd": b'@echo off\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL.ps1"\r\npause\r\n',
        "INSTALL.ps1": (ROOT / "tools/install_affix_questlog_fix.ps1").read_bytes(),
        "SHA256.json": (json.dumps({TRIM: sha(trim), QUEST: sha(quest)}, indent=2) + "\n").encode(),
        "README.txt": ("Armor trims + Questlog Q update\n\nClose Minecraft. Extract this ZIP and double-click INSTALL.cmd.\n"
                       "Choose the CurseForge profile you actually play (v0.4.5 or your newer v0.4.6 test kit).\n"
                       "The installer backs up and replaces only the two AO addon JARs and disables the duplicate native Q button.\n"
                       "It preserves other mods, configuration sections, quests and saves.\n\n"
                       "Verified: eight native trim tests; actual Better Inventory/Questlog client at GUI scales 2,3,4.\n"
                       "Q is immediately right of Settings. Existing trims and loot stats are preserved.\n"
                       "Full pack multiplayer/visual conflicts still need playtesting. This is not a complete v0.4.6 port.\n").encode(),
    }
    write_zip(args.output, entries)
    if args.base:
        assert args.import_output and args.base.resolve() != args.import_output.resolve()
        with ZipFile(args.base) as z:
            assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
            base = {n: z.read(n) for n in z.namelist()}
        manifest = json.loads(base["manifest.json"])
        assert manifest["version"] == OLD_VERSION
        assert len(manifest["files"]) == 330
        assert len({f["projectID"] for f in manifest["files"]}) == 330
        old_addons = {n for n in base if n.startswith("overrides/mods/ao-affix-trims-")
                      or n.startswith("overrides/mods/ao-questlog-betterinventory-")}
        assert old_addons == {"overrides/mods/ao-affix-trims-0.1.0-experimental.jar",
                              "overrides/mods/ao-questlog-betterinventory-0.1.4.jar"}
        new = {n: b for n, b in base.items() if n not in old_addons}
        manifest["version"] = NEW_VERSION
        manifest["name"] = "Ambient Odyssey - Armor Trims and Questlog Fix TEST"
        new["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
        new["overrides/mods/" + TRIM] = trim
        new["overrides/mods/" + QUEST] = quest
        # The exact v045 baseline already disables the duplicate standalone Q.
        import tomllib
        assert not tomllib.loads(new["overrides/config/questlog-client.toml"].decode())["button"]["enabled"]
        for name, data in base.items():
            if name not in old_addons and name != "manifest.json":
                assert new[name] == data, name
        write_zip(args.import_output, new)
        with ZipFile(args.import_output) as z:
            actual = json.loads(z.read("manifest.json"))
            original = json.loads(base["manifest.json"])
            assert actual["files"] == original["files"] and actual["minecraft"] == original["minecraft"]
            assert set(z.namelist()) == set(new)
            for name, data in new.items():
                assert z.read(name) == data, name
        print("PASS: 330 pins unchanged; only two AO addons and manifest identity changed")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--trim", type=Path, default=ROOT / "addons/ao-affix-trims/build/libs" / TRIM)
    p.add_argument("--quest", type=Path, default=ROOT / "addons/ao-questlog-betterinventory/build/libs" / QUEST)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--base", type=Path)
    p.add_argument("--import-output", type=Path)
    run(p.parse_args())
