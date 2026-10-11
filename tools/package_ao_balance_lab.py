#!/usr/bin/env python3
"""Isolated AO Balance Lab packager: add one official DD pin + one server config."""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PILOT_CONFIG = ROOT / "experiments/ao-balance-lab/config/dungeon_difficulty_v2.json"
TARGET_CONFIG = "overrides/config/dungeon_difficulty_v2.json"
DD_PROJECT = 645559
DD_FILE = 9110961
SOURCE_COUNT = 329
OUTPUT_COUNT = SOURCE_COUNT + 1
VERSION = "0.4.1-experimental-balance-lab-dd392"
NAME = "Ambient Odyssey v0.4.1 - Dungeon Difficulty Balance Lab TEST"
REQUIRED = {1581408:9060294, 618790:7033510, 890127:8654089, 889079:8726480, 318449:5845879, 1202066:8952784, 1618019:9099710}
EXCLUDED = {832882,1430156}

def sha(b): return sha256(b).hexdigest()
def validate_config(conf):
    from tools.validate_ao_balance_lab import check_config
    check_config(conf)

def inspect_base(zipfile_obj):
    z=zipfile_obj
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))
    assert "manifest.json" in names
    m=json.loads(z.read("manifest.json"))
    r={e["projectID"]:e["fileID"] for e in m["files"]}
    assert len(r)==len(m["files"])==SOURCE_COUNT, len(r)
    assert DD_PROJECT not in r, "Dungeon Difficulty already installed; refusing duplicate addition"
    assert all(r.get(pid)==fid for pid,fid in REQUIRED.items())
    assert not EXCLUDED.intersection(r)
    for n in names:
        p=PurePosixPath(n)
        assert not p.is_absolute() and ".." not in p.parts and "\\" not in n
    assert TARGET_CONFIG not in names, "Balance lab config already present in source"
    for jar in ("ao-questlog-betterinventory-0.1.1.jar","ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar"):
        assert "overrides/mods/"+jar in names
    return m, r

def verify(src, out):
    with zipfile.ZipFile(src) as s,zipfile.ZipFile(out) as z:
        m,r=inspect_base(s)
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        newm=json.loads(z.read("manifest.json"))
        refs={a["projectID"]:a["fileID"] for a in newm["files"]}
        assert len(refs)==len(newm["files"])==OUTPUT_COUNT
        assert refs=={**r,DD_PROJECT:DD_FILE}
        assert newm["name"]==NAME and newm["version"]==VERSION
        assert set(names)==set(s.namelist())|{TARGET_CONFIG}
        assert newm["minecraft"]==m["minecraft"]
        assert json.loads(z.read(TARGET_CONFIG))==json.loads(PILOT_CONFIG.read_bytes())
        validate_config(json.loads(z.read(TARGET_CONFIG)))
        for n in s.namelist():
            if n=="manifest.json": continue
            assert sha(s.read(n))==sha(z.read(n)), f"Unapproved payload drift: {n}"
    print("PASS balance pack: original 329 references + exactly one DD pin and one config; original addons and all other files byte-identical")
    print("NOT RUNTIME TESTED; DD data file acceptance must be checked inside Minecraft")

def build(src, out):
    with zipfile.ZipFile(src) as s:
        m,r=inspect_base(s)
        config=json.loads(PILOT_CONFIG.read_text())
        validate_config(config)
        m["name"]=NAME
        m["version"]=VERSION
        m["files"].append({"projectID":DD_PROJECT,"fileID":DD_FILE,"required":True})
        out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,"w",allowZip64=True) as z:
            for info in s.infolist():
                data=(json.dumps(m,indent=2,ensure_ascii=False)+"\n").encode("utf-8") if info.filename=="manifest.json" else s.read(info.filename)
                z.writestr(info,data)
            z.writestr(TARGET_CONFIG,PILOT_CONFIG.read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
    verify(src,out)
    print("OUTPUT:",str(out),"bytes:",out.stat().st_size,"sha256:",sha(out.read_bytes()))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    if args.verify: verify(args.source,args.output)
    else: build(args.source,args.output)
