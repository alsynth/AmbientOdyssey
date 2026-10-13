#!/usr/bin/env python3
"""Deterministic offline test for the experimental AO loot overlay packager.

Uses entirely synthetic ZIPs/JARs. Does not claim a real CurseForge import works.
"""
import hashlib, importlib.util, json, pathlib, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
module_path = ROOT / "tools/package_ao_loot_economy_pilot.py"
spec = importlib.util.spec_from_file_location("ao_package", module_path)
pkg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pkg)

def make_zip(path, items):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in items.items():
            z.writestr(name, data)

def check():
    with tempfile.TemporaryDirectory(prefix="ao-loot-pack-test-") as d:
        work = pathlib.Path(d)
        base = work / "base.zip"
        addon = work / "addon.jar"
        original_config = b'[whitelist]\nloot_table_forced_whitelist = []\nrandomise_seed = true\n'
        manifest = {"minecraft": {"version":"1.21.1", "modLoaders":[{"id":"neoforge-21.1.252","primary":True}]},
                    "files":[{"projectID":i,"fileID":i+1000,"required":True} for i in range(1,339)],
                    "name":"Synthetic AO baseline","version":"synthetic"}
        members = {"manifest.json":json.dumps(manifest),
                   "overrides/config/lootr-common.toml":original_config}
        for ring in ["basic_ring.json","advanced_ring.json"]:
            name=pkg.RECIPE_ROOT+ring
            members[name]=json.dumps({"type":"minecraft:crafting_shaped","result":{"id":"flight_rings:"+ring.removesuffix(".json")}})
        for i in range(7):
            members[f"overrides/mods/test-original-{i}.jar"] = b"TESTJAR"+bytes([i])
        members["overrides/config/questlog/quests/test.json"]=b'{"test":true}'
        make_zip(base,members)
        bundled = {"META-INF/neoforge.mods.toml": b'[[mods]]\nmodId="ao_starter_chest"\n'}
        for p in [
            "data/minecraft/loot_table/chests/spawn_bonus_chest.json",
            "data/ao_starter_chest/loot_modifiers/starter_affix.json",
            "data/neoforge/loot_modifiers/global_loot_modifiers.json"
        ]:
            bundled[p] = (ROOT/"addons/ao-starter-chest/src/main/resources"/p).read_bytes()
        make_zip(addon, bundled)
        allowed_sha=hashlib.sha256(base.read_bytes()).hexdigest()
        out1=work/"test-a.zip"
        out2=work/"test-b.zip"
        first=pkg.build(base, addon, out1, expected_sha=allowed_sha)
        second=pkg.build(base, addon, out2, expected_sha=allowed_sha)
        assert first["cf_references_preserved"]==338
        assert first["inherited_private_jars_preserved"]==7 and first["new_custom_mods"]==1
        assert out1.read_bytes()==out2.read_bytes(), "Nondeterministic packager output"
        with zipfile.ZipFile(out1) as z:
            assert z.read("overrides/config/questlog/quests/test.json")==b'{"test":true}'
            assert b"spawn_bonus_chest" in z.read("overrides/config/lootr-common.toml")
            assert z.read(pkg.MOD_ROOT+pkg.STARTER_NAME)==addon.read_bytes()
            assert len(json.loads(z.read("manifest.json"))["files"])==338
        try:
            pkg.build(base, addon, work/"bad.zip", expected_sha="0"*64)
        except ValueError as e:
            assert "SHA mismatch" in str(e)
        else:
            raise AssertionError("Accepted mismatched untrusted baseline")
        print("PASS: additive overlay, protected unrelated quests/JARs, pinned manifest, deterministic ZIP, strict baseline rejection")
        print("NOT TESTED: real base ZIP, full import, GameTest, Lootr conversions")

if __name__=="__main__":
    check()
