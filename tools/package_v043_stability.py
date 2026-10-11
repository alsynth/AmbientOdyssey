#!/usr/bin/env python3
"""Produce the Hominid-free v0.4.3 private CurseForge ZIP from the exact
previously CI-built user-tested v0.4.2 full archive. Deliberate DELTA builder:
all earlier content, source-verified repairs and 330 pinned mods are preserved
apart from one explicitly removed mod and one independently pinned compatibility
patch. Never edits the rollback profile. No runtime claims.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED

PREVIOUS_VERSION = "0.4.2-experimental-spellstone-difficulty"
VERSION = "0.4.3-experimental-hominid-free-stability"
NAME = "Ambient Odyssey v0.4.3 - Hominid-Free Stability TEST"
EXPECTED_BASE_SHA = "d4f928aec66c9dceea275b71db299a871cdac1ba9d07c83f91bb20c2a9b32be3"
HOMINID = 1221597
PATCH_PROJECT, PATCH_FILE = 1657433, 8673508
OLD_QUEST = "overrides/mods/ao-questlog-betterinventory-0.1.3.jar"
NEW_QUEST = "overrides/mods/ao-questlog-betterinventory-0.1.4.jar"
OLD_SAFETY = "overrides/mods/ao-worldgen-safety-0.1.3-experimental.jar"
NEW_SAFETY = "overrides/mods/ao-worldgen-safety-0.1.4-experimental.jar"
HOMINID_CONFIG = "overrides/config/hominid-common.toml"
REMOVE = {OLD_QUEST, OLD_SAFETY, HOMINID_CONFIG}
ADD = {NEW_QUEST, NEW_SAFETY}
PRESERVE = {
    "overrides/mods/ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar",
    "overrides/config/dungeon_difficulty/difficulty_v2.json",
    "overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json",
    "overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/spellstone.json",
}
def sha(b):
    return hashlib.sha256(b).hexdigest()

def data_manifest(z):
    a=json.loads(z.read("manifest.json"))
    assert len(a["files"])==len({x["projectID"] for x in a["files"]}), "Duplicated manifest project"
    return a

def safe(z):
    assert z.testzip() is None
    allnames=z.namelist()
    assert "manifest.json" in allnames and len(allnames)==len(set(allnames))
    for n in allnames:
        a=PurePosixPath(n)
        assert not a.is_absolute() and ".." not in a.parts and "\\" not in n, n

def validate_addon(which, blob):
    with ZipFile(io.BytesIO(blob)) as a:
        safe(a) if "manifest.json" in a.namelist() else None
        assert a.testzip() is None
        meta=a.read("META-INF/neoforge.mods.toml").decode()
        if which==NEW_SAFETY:
            assert 'modId="ao_worldgen_safety"' in meta
            assert 'version="0.1.4-experimental"' in meta
            assert 'modId="hominid"' not in meta
            cfg=json.loads(a.read("ao_worldgen_safety.mixins.json"))
            assert "HominidFinalizeSpawnMixin" not in cfg["mixins"]
            assert set(cfg["mixins"])=={
                "TansWorldgenMarkerSchedulingMixin",
                "DungeonCrawlSpawnerPendingNbtMixin",
                "DungeonCrawlOptionalTradeAirMixin",
            }
            assert not any("HominidFinalizeSpawnMixin" in n for n in a.namelist())
            assert "dev/ambientodyssey/worldgensafety/DungeonDifficultyDeferredEvaluation.class" in a.namelist()
        else:
            assert 'modId="aoquestlogbridge"' in meta
            assert 'version="0.1.4"' in meta
            assert "QuestlogBetterInventoryBridge$QuestlogTab.class" in " ".join(a.namelist())

def validate(base,out,quest,safety):
    with ZipFile(base) as a, ZipFile(out) as z:
        safe(a);safe(z)
        old=data_manifest(a);new=data_manifest(z)
        assert old["version"]==PREVIOUS_VERSION
        assert new["version"]==VERSION and new["name"]==NAME
        assert old["minecraft"]==new["minecraft"]
        orig={f["projectID"]:f["fileID"] for f in old["files"]}
        updated={f["projectID"]:f["fileID"] for f in new["files"]}
        assert len(orig)==330 and HOMINID in orig and PATCH_PROJECT not in orig
        assert len(updated)==330 and HOMINID not in updated and updated[PATCH_PROJECT]==PATCH_FILE
        assert updated=={**{k:v for k,v in orig.items() if k!=HOMINID},PATCH_PROJECT:PATCH_FILE}
        before=set(a.namelist());after=set(z.namelist())
        assert REMOVE.issubset(before),REMOVE-before
        assert ADD.isdisjoint(before)
        assert after==(before-REMOVE)|ADD
        assert PRESERVE.issubset(after)
        assert not any("hominid" in n.lower() for n in after)
        for n in before-REMOVE-{"manifest.json"}:
            assert sha(a.read(n))==sha(z.read(n)), "Unintended modified old asset: "+n
        assert z.read(NEW_QUEST)==quest.read_bytes()
        assert z.read(NEW_SAFETY)==safety.read_bytes()
        validate_addon(NEW_QUEST,z.read(NEW_QUEST))
        validate_addon(NEW_SAFETY,z.read(NEW_SAFETY))
        assert new["files"][-1]["projectID"]==PATCH_PROJECT
    print("PASS exact 330->330 CurseForge pins, Hominid removed, SubtleEnd compatibility added, two versioned native AO addons, all other user-approved data byte-identical.")
    print("STATIC ONLY: client and multiplayer tests required.")

def build(base,out,quest,safety):
    assert base.resolve()!=out.resolve()
    assert sha(base.read_bytes())==EXPECTED_BASE_SHA, "The starting archive is NOT the exact previously tested v0.4.2 ZIP"
    validate_addon(NEW_QUEST,quest.read_bytes())
    validate_addon(NEW_SAFETY,safety.read_bytes())
    with ZipFile(base) as a:
        safe(a)
        old=data_manifest(a)
        assert old["version"]==PREVIOUS_VERSION
        orig={x["projectID"]:x["fileID"] for x in old["files"]}
        assert len(orig)==330 and HOMINID in orig and PATCH_PROJECT not in orig
        assert REMOVE.issubset(set(a.namelist()))
        old["files"]=[x for x in old["files"] if x["projectID"]!=HOMINID]
        old["files"].append({"projectID":PATCH_PROJECT,"fileID":PATCH_FILE,"required":True})
        old["name"]=NAME;old["version"]=VERSION
        out.parent.mkdir(parents=True,exist_ok=True)
        with ZipFile(out,"w",allowZip64=True) as z:
            for item in a.infolist():
                if item.filename in REMOVE: continue
                contents=(json.dumps(old,indent=2,ensure_ascii=False)+"\n").encode() if item.filename=="manifest.json" else a.read(item.filename)
                z.writestr(item,contents)
            z.writestr(NEW_QUEST,quest.read_bytes(),compress_type=ZIP_DEFLATED)
            z.writestr(NEW_SAFETY,safety.read_bytes(),compress_type=ZIP_DEFLATED)
    validate(base,out,quest,safety)
    print("OUTPUT",out,"bytes",out.stat().st_size,"SHA256",sha(out.read_bytes()))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--base",type=Path,required=True)
    p.add_argument("--quest",type=Path,required=True)
    p.add_argument("--safety",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    (validate if a.verify else build)(a.base,a.output,a.quest,a.safety)
