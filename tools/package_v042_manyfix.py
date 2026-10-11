#!/usr/bin/env python3
"""AO v0.4.2: promote validated 329-source combo to one 330-ref many-fix test.

Only adds a *pinned* Dungeon Difficulty 3.9.2 native NeoForge project and one
source-backed explicit dungeon configuration. Copies ALL prior files unmodified,
including three AO addon jars and native Paxi. Does not merge divergent branches.
No runtime claims. Source manifest bytes differ only in name/version/addition.
"""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath
try:
    from tools.validate_ao_balance_lab import check_config
except ModuleNotFoundError:
    from validate_ao_balance_lab import check_config

ROOT=Path(__file__).resolve().parents[1]
PILOT=ROOT/"experiments/ao-balance-lab/config/dungeon_difficulty_v2.json"
DEST="overrides/config/dungeon_difficulty_v2.json"
BASE_COUNT=329
TARGET_COUNT=330
PROJECT=645559
FILE=9110961
NAME="Ambient Odyssey v0.4.2 - Recipes Spawner Questlog Integrated TEST"
VERSION="0.4.2-experimental-recipe-spawner-ui"
CONTROL_VERSION="0.4.2-experimental-recipe-spawner-ui-core"
ADDONS={
"overrides/mods/ao-questlog-betterinventory-0.1.3.jar",
"overrides/mods/ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar",
"overrides/mods/ao-worldgen-safety-0.1.2-experimental.jar",
}
RETAIN_PINS={
1581408:9060294, # Streams Reflowing
1202066:8952784, # Questlog
1618019:9099710, # Better Inventory
}
EXCLUDED={832882,1430156}

def digest(b):return hashlib.sha256(b).hexdigest()
def refs(manifest):
    result={x["projectID"]:x["fileID"] for x in manifest["files"]}
    assert len(result)==len(manifest["files"]),"Duplicate project in manifest"
    return result
def archive_safety(z):
    paths=z.namelist()
    assert z.testzip() is None
    assert len(paths)==len(set(paths))
    assert "manifest.json" in paths
    for p in paths:
        pp=PurePosixPath(p)
        assert not pp.is_absolute() and ".." not in pp.parts and "\\" not in p,p

def input_guard(z):
    archive_safety(z)
    manifest=json.loads(z.read("manifest.json"))
    p=refs(manifest)
    assert manifest["version"]==CONTROL_VERSION,manifest["version"]
    assert len(p)==BASE_COUNT and PROJECT not in p
    assert not EXCLUDED.intersection(p)
    assert all(p.get(k)==v for k,v in RETAIN_PINS.items())
    assert {n for n in z.namelist() if n.startswith("overrides/mods/") and n.endswith(".jar")}==ADDONS
    assert DEST not in z.namelist()
    return manifest,p

def verify(source,out):
    with zipfile.ZipFile(source) as a,zipfile.ZipFile(out) as z:
        original,old=input_guard(a)
        archive_safety(z)
        new=json.loads(z.read("manifest.json"))
        found=refs(new)
        assert len(found)==TARGET_COUNT
        assert found=={**old,PROJECT:FILE}
        assert new["name"]==NAME and new["version"]==VERSION
        assert new["minecraft"]==original["minecraft"]
        assert set(z.namelist())==set(a.namelist())|{DEST}
        conf=json.loads(z.read(DEST))
        assert conf==json.loads(PILOT.read_text())
        check_config(conf)
        for item in a.namelist():
            if item=="manifest.json":continue
            assert digest(a.read(item))==digest(z.read(item)),("UNEXPECTED CHANGE",item)
        for mod in ADDONS:
            assert z.read(mod)==a.read(mod)
        for chap in ["field_manual.snbt","keybind_cheatsheet.snbt","tips_and_tricks.snbt"]:
            p="overrides/config/ftbquests/quests/chapters/"+chap
            assert z.read(p)==a.read(p)
        assert any("ao_v041_trek_create_rarity_test" in p for p in z.namelist())
        assert json.loads(z.read(
            "overrides/config/paxi/datapacks/ao_compatibility/data/curios/curios/slots/amulet.json"
        ))=={"size":1,"operation":"SET","replace":False}
    print("PASS v0.4.2 final: 329 -> 330 locked refs, exact 1 DD pin + exact 1 dungeon config, 3 compiled addons and all user-approved preexisting overrides byte-identical")
    print("NOT RUNTIME TESTED, developer private CurseForge import only")

def build(source,out):
    assert source.resolve()!=out.resolve()
    with zipfile.ZipFile(source) as original:
        manifest,previous=input_guard(original)
        data=json.loads(PILOT.read_text())
        check_config(data)
        manifest["files"].append({"projectID":PROJECT,"fileID":FILE,"required":True})
        manifest["name"]=NAME
        manifest["version"]=VERSION
        out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,"w",allowZip64=True) as z:
            for item in original.infolist():
                contents=(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n").encode() if item.filename=="manifest.json" else original.read(item.filename)
                z.writestr(item,contents)
            z.writestr(DEST,PILOT.read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
    verify(source,out)
    print("OUTPUT",out,"sha256",digest(out.read_bytes()))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    (verify if a.verify else build)(a.source,a.output)
