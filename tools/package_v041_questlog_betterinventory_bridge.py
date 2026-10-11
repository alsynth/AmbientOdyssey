#!/usr/bin/env python3
"""Insert AO-authored Questlog/Better Inventory client bridge into the confirmed
328-ref Mine Cells control package. No third-party JARs are bundled or altered.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

NAME="ao-questlog-betterinventory-0.1.1.jar"
JAR_PATH="overrides/mods/"+NAME
CLASS="dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge.class"
EXPECTED_ABSENT={832882,1430156,1581408}

def validate(out):
    with ZipFile(out) as z:
        assert z.testzip() is None, "release CRC invalid"
        names=z.namelist()
        assert len(names)==len(set(names)),"duplicate zip entry"
        assert "manifest.json" in names and JAR_PATH in names
        m=json.loads(z.read("manifest.json"))
        r={i["projectID"]:i["fileID"] for i in m["files"]}
        assert len(r)==328,len(r)
        assert EXPECTED_ABSENT.isdisjoint(r), "Mine Cells working exclusions regressed"
        assert r[1202066]==8952784 and r[1618019]==9099710
        assert all(not n.startswith("overrides/mods/") or n==JAR_PATH for n in names),"unapproved embedded JAR"
        data=z.read(JAR_PATH)
        with ZipFile(BytesIO(data)) as j:
            assert j.testzip() is None
            assert CLASS in j.namelist() and "META-INF/neoforge.mods.toml" in j.namelist()
            toml=j.read("META-INF/neoforge.mods.toml").decode()
            assert 'modId="aoquestlogbridge"' in toml and '0.1.1' in toml
        for name in ["trial_key.json","ominous_trial_key.json"]:
            p="overrides/config/paxi/resourcepacks/ao_lukis_dnt_key_compat/assets/minecraft/models/item/"+name
            assert p in names, "lost Luki/DnT key patch"
        print("PASS: exactly 328 CurseForge refs, Questlog and Better Inventory pins, AO bridge owned JAR only, Luki keys kept")
        print("NOT RUNTIME TESTED: menu interactions, click, badges and multiplayer require user's client")

def build(source,jar,target):
    assert source.resolve()!=target.resolve()
    assert jar.name==NAME,jar.name
    with ZipFile(jar) as m:
        assert m.testzip() is None
        assert CLASS in m.namelist() and "META-INF/neoforge.mods.toml" in m.namelist()
    target.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(source) as sourcez:
        assert sourcez.testzip() is None
        assert JAR_PATH not in sourcez.namelist()
        with ZipFile(target,"w") as z:
            for info in sourcez.infolist():
                z.writestr(info,sourcez.read(info.filename))
            z.write(jar,JAR_PATH)
    validate(target)
    print("OUTPUT",target.name,"size",target.stat().st_size,"sha256",sha256(target.read_bytes()).hexdigest())

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path)
    ap.add_argument("--jar",type=Path)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--verify",action="store_true")
    x=ap.parse_args()
    if x.verify:
        validate(x.output)
    else:
        assert x.source and x.jar
        build(x.source,x.jar,x.output)
