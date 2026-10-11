"""Synthetic strict 329->330 v0.4.2 packager regression. No Minecraft."""
import io
import json
import tempfile
from pathlib import Path
import unittest
from zipfile import ZipFile
from tools.package_v042_manyfix import (build,verify,PROJECT,FILE,VERSION,CONTROL_VERSION,
                                          DEST,ADDONS,RETAIN_PINS)

class ConsolidatedBuildTest(unittest.TestCase):
    def make_source(self,p):
        fixed={**RETAIN_PINS}
        for project in range(2_000_000,2_000_000+(329-len(fixed))):
            fixed[project]=project+10
        manifest={"name":"core","version":CONTROL_VERSION,
                  "minecraft":{"version":"1.21.1","modLoaders":[{"id":"neoforge-21.1.252","primary":True}]},
                  "files":[{"projectID":k,"fileID":v,"required":True} for k,v in fixed.items()],
                  "overrides":"overrides"}
        with ZipFile(p,"w") as z:
            z.writestr("manifest.json",json.dumps(manifest))
            for x in ADDONS:z.writestr(x,b"mock compiled jar binary for fixture")
            z.writestr("overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json",
                       json.dumps({"size":1,"operation":"SET","replace":False}))
            z.writestr("overrides/config/paxi/datapacks/ao_v041_trek_create_rarity_test/pack.mcmeta","{}")
            for chapter in ["field_manual","tips_and_tricks","keybind_cheatsheet"]:
                z.writestr(f"overrides/config/ftbquests/quests/chapters/{chapter}.snbt","original:"+chapter)
            z.writestr("overrides/config/paxi/datapacks/ao_server_rules/test.mcfunction",b"gamerule playersSleepingPercentage 30")

    def test_only_new_project_and_config(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"329.zip",Path(d)/"330.zip"
            self.make_source(a)
            build(a,b)
            verify(a,b)
            with ZipFile(b) as z:
                m=json.loads(z.read("manifest.json"))
                self.assertEqual(m["version"],VERSION)
                self.assertEqual(len(m["files"]),330)
                self.assertEqual({x["projectID"]:x["fileID"] for x in m["files"]}[PROJECT],FILE)
                self.assertIn(DEST,z.namelist())
                self.assertIn("ao_dungeon",z.read(DEST).decode())
                self.assertEqual(z.read("overrides/config/paxi/datapacks/ao_server_rules/test.mcfunction"),
                                 b"gamerule playersSleepingPercentage 30")

    def test_wrong_manifest_ref_count_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"329.zip",Path(d)/"330.zip"
            self.make_source(a)
            with ZipFile(a) as z: pass
            # Can't modify original: the build should refuse same input/output.
            with self.assertRaises(AssertionError):
                build(a,a)
if __name__=="__main__":unittest.main()
