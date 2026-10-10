"""Offline synthetic JAR tests: never download mods or use production saves."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.audit_installed_jars_v04 import scan, evaluate, get_dir

def jar(path, member, raw):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(member, raw)

def native(mid, required=()):
    table = f'[[mods]]\nmodId="{mid}"\n'
    for dep in required:
        table += f'\n[[dependencies.{mid}]]\nmodId="{dep}"\ntype="required"\nside="BOTH"\n'
    return table

class InstalledJarAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "mods").mkdir()
    def write_native(self, filename, modid, required=()):
        jar(self.root / "mods" / filename, "META-INF/neoforge.mods.toml", native(modid, required))
    def test_native_mods_dependencies_and_missing_only_warn(self):
        self.write_native("questlog.jar", "questlog", ("cloth_config",))
        self.write_native("cloth.jar", "cloth_config")
        r = scan(self.root / "mods")
        self.assertEqual(set(r["ids"]), {"questlog", "cloth_config"})
        self.assertEqual(r["unresolved_dependencies"], [])
        self.assertEqual(evaluate(r)["status"], "STATIC_REVIEW")
    def test_duplicate_native_mod_id_blocks(self):
        self.write_native("a.jar", "questlog")
        self.write_native("b.jar", "questlog")
        r = scan(self.root / "mods")
        self.assertEqual(len(r["duplicate_mod_ids"]), 1)
        self.assertEqual(evaluate(r)["status"], "BLOCKED")
    def test_fabric_bridge_dep_is_warning_not_fake_success(self):
        jar(self.root / "mods" / "minecells.jar", "fabric.mod.json",
            json.dumps({"id": "minecells", "depends": {"minecraft": "1.21.1",
                                                    "fabric-api-base": "*"}}))
        r = scan(self.root / "mods")
        self.assertTrue(r["unresolved_dependencies"][0]["bridge_candidate"])
        self.assertEqual(evaluate(r)["status"], "STATIC_REVIEW")
    def test_corrupt_jar_is_reported(self):
        (self.root / "mods" / "broken.jar").write_bytes(b"not a jar")
        self.write_native("good.jar", "questlog")
        r = scan(self.root / "mods")
        self.assertTrue(r["invalid_jars"])
        self.assertEqual(evaluate(r)["status"], "STATIC_REVIEW")
    def test_server_missing_required_gameplay_mods_blocks(self):
        self.write_native("questlog.jar", "questlog")
        jar(self.root / "mods" / "minecells.jar", "fabric.mod.json", '{"id":"minecells"}')
        client = scan(self.root / "mods")
        other = self.root / "server" / "mods"
        other.mkdir(parents=True)
        jar(other / "questlog.jar", "META-INF/neoforge.mods.toml", native("questlog"))
        result = evaluate(client, scan(other))
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["comparison"]["required_server_mod_ids_missing"], ["minecells"])
    def test_client_server_complete_static_only(self):
        self.write_native("questlog.jar", "questlog")
        jar(self.root / "mods" / "minecells.jar", "fabric.mod.json", '{"id":"minecells"}')
        client=scan(self.root / "mods")
        result=evaluate(client,client)
        self.assertEqual(result["status"], "STATIC_REVIEW")
        self.assertFalse(result["runtime_tested"])
    def test_instance_directory(self):
        self.assertEqual(get_dir(self.root), self.root / "mods")

if __name__ == "__main__":
    unittest.main()
