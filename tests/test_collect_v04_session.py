"""Synthetic test profile only — safe evidence bundling."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.collect_v04_session import selected_options, report, summary, save_snapshot

def native(path, mid, required=None):
    content = '[[mods]]\nmodId="' + mid + '"\n'
    if required:
        content += '\n[[dependencies.' + mid + ']]\nmodId="' + required + '"\ntype="required"\nside="BOTH"\n'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("META-INF/neoforge.mods.toml", content)

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "mods").mkdir()
        native(self.root / "mods" / "questlog.jar", "questlog", "cloth_config")
        native(self.root / "mods" / "cloth.jar", "cloth_config")
        (self.root / "options.txt").write_text(
          "renderDistance:12\nguiScale:3\nplayerName:SECRET\n"
          "soundCategory_weather:0.2\nserver_ip:192.0.2.1\n", encoding="utf-8")
    def test_allowlisted_video_only(self):
        d = selected_options(self.root)
        self.assertEqual(d["renderDistance"], "12")
        self.assertNotIn("playerName", d)
    def test_runtime_not_claimed(self):
        d = report(self.root)
        self.assertFalse(d["runtime_tested_by_snapshot"])
        self.assertEqual(d["installed_mods"]["jar_count"], 2)
        self.assertNotIn("SECRET", json.dumps(d))
        self.assertIn("NOT TESTED", summary(d))
    def test_no_raw_log_leak(self):
        logs = self.root / "logs"
        logs.mkdir()
        (logs / "latest.log").write_text(
           "SECRET player connected from 192.0.2.1\n"
           "java.lang.OutOfMemoryError\n", encoding="utf-8")
        output = self.root / "snapshot.zip"
        save_snapshot(self.root, output)
        with zipfile.ZipFile(output) as z:
            self.assertEqual(set(z.namelist()), {"report.json", "summary.md", "field-sheet.md"})
            blob = "\n".join(z.read(n).decode() for n in z.namelist())
            self.assertNotIn("SECRET", blob)
            self.assertNotIn("192.0.2.1", blob)
            self.assertIn("out_of_memory", blob)
    def test_server_comparison_is_not_certification(self):
        s = self.root / "server"
        (s / "mods").mkdir(parents=True)
        native(s / "mods" / "questlog.jar", "questlog")
        d = report(self.root, s)
        self.assertIn("minecells", d["server_comparison"]["required_server_mod_ids_missing"])
        self.assertFalse(d["runtime_tested_by_snapshot"])

if __name__ == "__main__":
    unittest.main()
