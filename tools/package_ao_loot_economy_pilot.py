#!/usr/bin/env python3
"""Reproducible additive AO loot test-import builder.

Inputs are the SHA-pinned v0.4.9.1 full import from PR50 and this branch's
compiled ao-starter-chest addon from GitHub Actions. Does NOT download files.
Always creates a NEW ZIP; never overwrites the base.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA256 = "dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f"
STARTER_NAME = "ao-starter-chest-0.2.0-experimental.jar"
RECIPE_ROOT = "overrides/config/paxi/datapacks/ao_flight_balance/data/flight_rings/recipe/"
GOBLIN_ROOT = "overrides/config/paxi/datapacks/ao_goblin_trades/"
MOD_ROOT = "overrides/mods/"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_zip(path):
    with zipfile.ZipFile(path, "r") as z:
        if z.testzip() is not None:
            raise ValueError("Corrupt input ZIP")
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Input contains duplicate members")
        return {i.filename: (i, z.read(i)) for i in z.infolist() if not i.is_dir()}

def checked_add(values, name, payload):
    if name in values:
        raise ValueError("Would overwrite unexpected existing content: " + name)
    values[name] = payload

def build(base_zip, addon_jar, output_zip, expected_sha=BASE_SHA256):
    base_zip, addon_jar, output_zip = map(Path, (base_zip, addon_jar, output_zip))
    if output_zip.resolve() in {base_zip.resolve(), addon_jar.resolve()}:
        raise ValueError("Output must not overwrite any input")
    if sha(base_zip.read_bytes()) != expected_sha:
        raise ValueError("Full import SHA mismatch: only approved PR50 archive is accepted")
    original = read_zip(base_zip)
    addon_members = read_zip(addon_jar)
    addon_toml = addon_members.get("META-INF/neoforge.mods.toml")
    if addon_toml is None or 'modId="ao_starter_chest"' not in addon_toml[1].decode():
        raise ValueError("Not an AO starter chest JAR")
    needed = [
        "data/ao_starter_chest/loot_modifiers/starter_affix.json",
        "data/neoforge/loot_modifiers/global_loot_modifiers.json",
    ]
    if "data/minecraft/loot_table/chests/spawn_bonus_chest.json" in addon_members:
        raise ValueError("Bonus contents must be additive; replacement table is forbidden")
    for name in needed:
        if name not in addon_members:
            raise ValueError("Missing starter addon resource " + name)
        json.loads(addon_members[name][1].decode("utf-8"))
    manifest = json.loads(original["manifest.json"][1])
    if manifest.get("minecraft", {}).get("version") != "1.21.1":
        raise ValueError("Unexpected Minecraft version")
    if manifest.get("minecraft", {}).get("modLoaders") != [{"id": "neoforge-21.1.252", "primary": True}]:
        raise ValueError("Unexpected NeoForge loader")
    if len(manifest.get("files", [])) != 338:
        raise ValueError("Unexpected pinned CF roster")
    mods = [n for n in original if n.startswith(MOD_ROOT) and n.endswith(".jar")]
    if len(mods) != 7 or any("ao-starter-chest" in x for x in mods):
        raise ValueError("Expected exactly seven inherited custom JARs")
    payload = {n:data for n,(_,data) in original.items()}
    changed = {}
    def add_or_replace(name, data, mode):
        if mode == "new" and name in payload:
            raise ValueError("New path already exists: " + name)
        if mode == "replace" and name not in payload:
            raise ValueError("Expected base path missing: " + name)
        old = payload.get(name)
        payload[name] = data
        changed[name] = {"before_sha256":sha(old) if old is not None else None,
                         "after_sha256":sha(data)}
    ring_source = ROOT / "release_030/overrides/config/paxi/datapacks/ao_flight_balance/data/flight_rings/recipe"
    for ring in ["basic_ring.json", "advanced_ring.json"]:
        fname = RECIPE_ROOT + ring
        data = (ring_source / ring).read_bytes()
        obj = json.loads(data)
        if obj.get("type") != "minecraft:crafting_shaped":
            raise ValueError("Invalid Flight Ring recipe: " + ring)
        add_or_replace(fname, data, "replace")
    exemptions = ROOT / "release_030/overrides/config/paxi/datapacks/ao_starter_apotheosis_exemptions"
    exemptions_root = "overrides/config/paxi/datapacks/ao_starter_apotheosis_exemptions/"
    for subpath in ("pack.mcmeta", "data/apotheosis/loot_modifiers/affix_conversion.json",
                    "data/apotheosis/loot_modifiers/affix_loot_injection.json",
                    "data/apotheosis/loot_modifiers/gem_loot_injection.json"):
        data = (exemptions / subpath).read_bytes()
        parsed = json.loads(data)
        if subpath != "pack.mcmeta":
            assert parsed["entries"][0] == {
                "chance": 0.0,
                "pattern": {"domain": "minecraft", "path_regex": "chests/spawn_bonus_chest"}
            }, f"Bonus-only loot injection exemption missing: {subpath}"
        add_or_replace(exemptions_root + subpath, data, "new")
    goblin = ROOT / "release_030/overrides/config/paxi/datapacks/ao_goblin_trades"
    for subpath in ["pack.mcmeta", "data/goblintraders/goblin_trades/goblin_trader/epic.json"]:
        data = (goblin / subpath).read_bytes()
        json.loads(data)
        add_or_replace(GOBLIN_ROOT + subpath, data, "new")
    lootr_path = "overrides/config/lootr-common.toml"
    existing = payload.get(lootr_path)
    if existing is None or b'loot_table_forced_whitelist = []' not in existing:
        raise ValueError("Lootr baseline differs; refusing blind config replacement")
    replacement = existing.replace(b'loot_table_forced_whitelist = []',
                                    b'loot_table_forced_whitelist = ["minecraft:chests/spawn_bonus_chest"]', 1)
    add_or_replace(lootr_path, replacement, "replace")
    add_or_replace(MOD_ROOT + STARTER_NAME, addon_jar.read_bytes(), "new")

    manifest["name"] = "Ambient Odyssey v0.4.9.1 - Loot Economy + Starter Chest TEST"
    manifest["version"] = "0.4.9.1-loot-economy-pilot"
    payload["manifest.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False)+"\n").encode()
    changed["manifest.json"] = {"before_sha256":sha(original["manifest.json"][1]),
                                "after_sha256":sha(payload["manifest.json"])}
    notes = (
        "EXPERIMENTAL AO LOOT PILOT - NOT RUNTIME ACCEPTED.\n"
        "Based on PR50 SHA256 " + expected_sha + "\n"
        "Starter chest: five eligible spellstones, genuine Apotheosis affix roll, torches/meat.\n"
        "Goblin Tuned chainmail: 32 diamonds + 4 Cinder Essence. Flight Ring recipes retuned.\n"
        "Exempts ONLY the starter Bonus Chest from three native Apotheosis random injectors.\n"
        "Lootr's forced whitelist is NOT proof that the vanilla Bonus Chest converts.\n"
        "Test on a NEW world with Bonus Chest ON and TWO different non-OP accounts,\n"
        "then dedicated-server persistence, all real affix rarities and normal loot preservation.\n"
    ).encode()
    add_or_replace("overrides/AO_TEST_NOTES/LOOT_ECONOMY_PILOT.txt", notes, "new")
    changed_order = sorted(payload)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in changed_order:
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError("Unsafe archive path")
            if name in original:
                info = original[name][0]
            else:
                info = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
            z.writestr(info, payload[name])
    check = read_zip(output_zip)
    if set(check) != set(payload) or any(check[n][1] != v for n,v in payload.items()):
        raise ValueError("Output content/CRC verification failed")
    unchanged = set(original) - set(changed)
    if any(check[n][1] != original[n][1] for n in unchanged):
        raise ValueError("Untouched base payload drifted")
    report = {"base_sha256": expected_sha, "addon_sha256": sha(addon_jar.read_bytes()),
              "output_sha256": sha(output_zip.read_bytes()), "changed": changed,
              "original_member_count": len(original), "result_member_count":len(check),
              "cf_references_preserved": len(manifest["files"]),
              "inherited_private_jars_preserved": len(mods),
              "new_custom_mods": 1,
              "minecraft_runtime_tested": False,
              "lootr_bonus_chest_conversion_tested": False}
    Path(str(output_zip)+".report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    return report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True,
                    help="Exact v0491 PR50 full import with SHA256 dd72daac...")
    ap.add_argument("--starter-jar", type=Path, required=True,
                    help="Compiled and CI-verified ao-starter-chest JAR")
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    build(a.base, a.starter_jar, a.output)

if __name__ == "__main__":
    main()
