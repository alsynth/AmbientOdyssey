"""Synthetic ZIP test: profiler A/B must preserve all pinned modpacks."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile
from tools.make_v041_spark_profiler_ab import build, verify, CONFIG

class SparkAandBTests(unittest.TestCase):
    def test_only_profiler_config_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/"a.zip"; b=Path(tmp)/"b.zip"
            with ZipFile(a,"w") as z:
                z.writestr("manifest.json",json.dumps({
                    "files":[{"projectID":i,"fileID":i+1000} for i in range(329)],
                    "minecraft":{"version":"1.21.1"},"name":"AO","version":"0.4.1"}))
                z.writestr(CONFIG,json.dumps({"backgroundProfiler":True,"other":"keep"}))
                z.writestr("overrides/config/paxi/datapacks/foo/bar.json","{}")
            build(a,b)
            verify(a,b)
            with ZipFile(b) as z:
                self.assertFalse(json.loads(z.read(CONFIG))["backgroundProfiler"])
            with ZipFile(a) as z:
                self.assertTrue(json.loads(z.read(CONFIG))["backgroundProfiler"])

    def test_no_inplace_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/"same.zip"
            with self.assertRaises(AssertionError):build(f,f)

if __name__=="__main__":
    unittest.main()
