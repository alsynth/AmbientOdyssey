"""Synthetic archive tests; do not represent actual Minecraft gameplay testing."""
import io
import json
import pathlib
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
from perf_preflight_v04 import scan_bytes, compare, read_import_bytes

def makezip(distance="12", extra=None):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("manifest.json", json.dumps({"version": "test", "files": [{"projectID": 1, "fileID": 2}]}))
        z.writestr("overrides/config/defaultoptions/options.txt", "renderDistance:" + distance + "\nsimulationDistance:6\n")
        for k, value in (extra or {}).items():
            z.writestr(k, value)
    return buf.getvalue()

class TestPerfPreflight(unittest.TestCase):
    def test_manifest_and_defaults(self):
        report, files = scan_bytes(makezip(), expected_refs=1)
        self.assertEqual(report["manifest"]["pinned_references"], 1)
        self.assertEqual(report["configuration_samples"]["options"]["settings"]["renderDistance"], "12")
        self.assertEqual(len(files), 1)

    def test_outer_artifact_chooses_variant(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "outer.zip"
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("build/one-CF-References.zip", makezip("12"))
                z.writestr("build/one-PRIVATE.zip", makezip("8"))
            ref, _, was_outer = read_import_bytes(p, "references")
            priv, _, _ = read_import_bytes(p, "private")
            self.assertTrue(was_outer)
            self.assertEqual(scan_bytes(ref, expected_refs=1)[0]["configuration_samples"]["options"]["settings"]["renderDistance"], "12")
            self.assertEqual(scan_bytes(priv, expected_refs=1)[0]["configuration_samples"]["options"]["settings"]["renderDistance"], "8")

    def test_diff_and_spark_flag(self):
        old = scan_bytes(makezip(), expected_refs=1)
        new = scan_bytes(makezip("10", {"overrides/config/spark/config.json": '{"backgroundProfiler":true}'}), expected_refs=1)
        diff = compare(old, new)
        self.assertTrue(diff["same_pinned_roster"])
        self.assertEqual(diff["modified_overrides"], ["overrides/config/defaultoptions/options.txt"])
        self.assertIn("overrides/config/spark/config.json", diff["added_overrides"])
        self.assertTrue(any("Spark" in issue for issue in new[0]["issues_to_investigate"]))

    def test_unsafe_path(self):
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            scan_bytes(makezip(extra={"overrides/../oops": "x"}), expected_refs=1)

if __name__ == "__main__":
    unittest.main()
