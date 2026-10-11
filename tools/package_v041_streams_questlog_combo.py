#!/usr/bin/env python3
"""Create the full AO combined ZIP from the Mine Cells working control ZIP.

Restores *exactly* Streams Reflowing 2.14.4 (project 1581408/file 9060294)
and bundles the three AO-authored addons. Preserves all 328 control references,
content/worldgen repairs, Luki/DnT resource pack, and the proven rollback.

Usage:
python tools/package_v041_streams_questlog_combo.py \
  --source build/ao-v041-328-control.zip \
  --questlog-jar addons/ao-questlog-betterinventory/build/libs/ao-questlog-betterinventory-0.1.2.jar \
  --streams-jar build/streams-addon/ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar \
  --safety-jar addons/ao-worldgen-safety/build/libs/ao-worldgen-safety-0.1.0-experimental.jar \\
  --output build/Ambient-Odyssey-v0.4.1-WORLDGEN-SAFETY-TEST.zip

And --verify --output ZIP for independent revalidation.
"""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

STREAM_PROJECT=1581408
STREAM_FILE=9060294
QL_PROJECT=1202066
QL_FILE=8952784
BI_PROJECT=1618019
BI_FILE=9099710
BASE_REMOVED={832882,1430156,1581408}
QUESTLOG_JAR="ao-questlog-betterinventory-0.1.2.jar"
STREAMS_JAR="ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar"
SAFETY_JAR="ao-worldgen-safety-0.1.0-experimental.jar"
JARS={"overrides/mods/"+QUESTLOG_JAR,"overrides/mods/"+STREAMS_JAR,"overrides/mods/"+SAFETY_JAR}
NAME="Ambient Odyssey v0.4.1 - Worldgen Safety and Data Repairs"
VERSION="0.4.1-experimental-worldgen-safety"

def jar_check(name, blob):
    with ZipFile(BytesIO(blob)) as z:
        assert z.testzip() is None
        paths=z.namelist()
        assert "META-INF/neoforge.mods.toml" in paths
        toml=z.read("META-INF/neoforge.mods.toml").decode("utf-8")
        if name==STREAMS_JAR:
            assert 'modId="ao_streams_minecells"' in toml
            assert 'versionRange="[2.14.4,2.14.5)"' in toml
            for c in ("StreamsChunkDeferralMixin","StreamsStructureProtectionMixin"):
                assert f"dev/ambientodyssey/compat/mixin/{c}.class" in paths
            assert "ao_streams_minecells.mixins.json" in paths
        elif name==SAFETY_JAR:
            assert 'modId="ao_worldgen_safety"' in toml
            assert "ao_worldgen_safety.mixins.json" in paths
            assert "dev/ambientodyssey/worldgensafety/mixin/HominidFinalizeSpawnMixin.class" in paths
            assert "dev/ambientodyssey/worldgensafety/mixin/TansWorldgenMarkerSchedulingMixin.class" in paths
        else:
            assert 'modId="aoquestlogbridge"' in toml
            assert "QuestlogBetterInventoryBridge$QuestlogTab.class" in " ".join(paths)
            assert "0.1.2" in toml

def validate(path):
    with ZipFile(path) as z:
        assert z.testzip() is None, "ZIP CRC error"
        names=z.namelist()
        assert len(names)==len(set(names))
        assert "manifest.json" in names
        m=json.loads(z.read("manifest.json"))
        files=m["files"]
        refs={f["projectID"]:f["fileID"] for f in files}
        assert len(files)==len(refs)==329, len(refs)
        assert refs[STREAM_PROJECT]==STREAM_FILE
        assert refs[QL_PROJECT]==QL_FILE and refs[BI_PROJECT]==BI_FILE
        assert not ({832882,1430156}&refs.keys())
        assert m["minecraft"]["version"]=="1.21.1"
        assert m["minecraft"]["modLoaders"]==[{"id":"neoforge-21.1.252","primary":True}]
        assert m["name"]==NAME and m["version"]==VERSION
        assert {p for p in names if p.startswith("overrides/mods/")}==JARS
        for jar in JARS:
            assert jar in names
            jar_check(jar.removeprefix("overrides/mods/"),z.read(jar))
        native_pool = ("overrides/config/paxi/datapacks/ao_lukis_mansion_native_pool/"
             "data/mansions/worldgen/template_pool/mansion/bottom_back_left.json")
        pool=json.loads(z.read(native_pool))
        assert pool["fallback"]=="minecraft:empty"
        assert len(pool["elements"])==1 and pool["elements"][0]["element"]["location"]=="mansions:mansion/bottom_back_left"
        assert pool["elements"][0]["element"]["processors"]=="mansions:mansion_texture"
        for stem in ("trial_key","ominous_trial_key"):
            assert "overrides/config/paxi/resourcepacks/ao_lukis_dnt_key_compat/assets/minecraft/models/item/"+stem+".json" in names
    print("PASS 329 CF refs including Streams Reflowing 2.14.4, three AO addon jars, Mine Cells rollback exclusions, Luki key repair")
    print("STATIC only: dedicated server and updated combined profile not runtime-tested")

def build(source,quest,streams,safety,target):
    assert source.resolve()!=target.resolve()
    assert quest.name==QUESTLOG_JAR and streams.name==STREAMS_JAR and safety.name==SAFETY_JAR
    quest_bytes=quest.read_bytes()
    streams_bytes=streams.read_bytes()
    safety_bytes=safety.read_bytes()
    jar_check(QUESTLOG_JAR,quest_bytes)
    jar_check(STREAMS_JAR,streams_bytes)
    jar_check(SAFETY_JAR,safety_bytes)
    with ZipFile(source) as src:
        assert src.testzip() is None
        m=json.loads(src.read("manifest.json"))
        refs={f["projectID"]:f["fileID"] for f in m["files"]}
        assert len(refs)==328 and BASE_REMOVED.isdisjoint(refs.keys()),"must start from proven control profile"
        assert refs[QL_PROJECT]==QL_FILE and refs[BI_PROJECT]==BI_FILE
        assert not any(n.startswith("overrides/mods/") for n in src.namelist()),"Control must not already include AO addon"
        m["files"].append({"projectID":STREAM_PROJECT,"fileID":STREAM_FILE,"required":True})
        m["name"]=NAME
        m["version"]=VERSION
        target.parent.mkdir(parents=True,exist_ok=True)
        with ZipFile(target,"w") as dest:
            for info in src.infolist():
                if info.filename=="manifest.json":
                    data=(json.dumps(m,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
                else:
                    data=src.read(info.filename)
                dest.writestr(info,data)
            dest.writestr("overrides/mods/"+QUESTLOG_JAR,quest_bytes)
            dest.writestr("overrides/mods/"+STREAMS_JAR,streams_bytes)
            dest.writestr("overrides/mods/"+SAFETY_JAR,safety_bytes)
    validate(target)
    print("OUTPUT",target, target.stat().st_size,"sha256",hashlib.sha256(target.read_bytes()).hexdigest())

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path)
    p.add_argument("--questlog-jar",type=Path)
    p.add_argument("--streams-jar",type=Path)
    p.add_argument("--safety-jar",type=Path)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    if a.verify:
        validate(a.output)
    else:
        assert a.source and a.questlog_jar and a.streams_jar and a.safety_jar
        build(a.source,a.questlog_jar,a.streams_jar,a.safety_jar,a.output)
