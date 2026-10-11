#!/usr/bin/env python3
"""Produce the private v0.4.4 DATA/UI experiment as a small verified delta to
the known successful v0.4.3 user-playtested CurseForge ZIP.
This is deliberately NOT a claim that outstanding binary NBT/jigsaw issues are fixed.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, zipfile
from zipfile import ZipFile, ZIP_DEFLATED
P=pathlib.Path
NAME="Ambient Odyssey v0.4.4 - Preperformance Candidate TEST"
VERSION="0.4.4-experimental-preperformance"
OLD="0.4.3-experimental-hominid-free-stability"
ROOT=P(__file__).resolve().parents[1]
SOURCE=ROOT/"release_030/overrides"
PATHS=[
"config/questlog-client.toml",
"config/questlog/quests/ao_first_pages_14_find_minecells_overworld_portal.json",
"config/questlog/quests/ao_first_pages_15_defeat_your_first_monster.json",
"config/cristellib/block_factorys_bosses/structure_placement_config.json5",
"config/paxi/datapacks/ao_structure_density/data/minecraft/worldgen/structure_set/villages.json",
]
def sha(data):return hashlib.sha256(data).hexdigest()
def checkzip(z):
    bad=z.testzip()\n    assert bad is None, ("Corrupt ZIP entry", bad)
    names=z.namelist()
    assert names.count("manifest.json")==1 and len(names)==len(set(names))
    assert all(not P(n).is_absolute() and ".." not in n.split("/") and "\\" not in n for n in names)
def verify(a,z):
    checkzip(a);checkzip(z)
    b=json.loads(a.read("manifest.json"))
    m=json.loads(z.read("manifest.json"))
    assert b["version"]==OLD,(b["version"],OLD)
    assert m["version"]==VERSION and m["name"]==NAME
    assert b["files"]==m["files"] and b["minecraft"]==m["minecraft"]
    old=set(a.namelist());new=set(z.namelist())
    changes={"overrides/"+p for p in PATHS}
    assert new==old|changes
    for n in old-{"manifest.json"}-changes:
        assert sha(a.read(n))==sha(z.read(n)),n
    for p in PATHS:
        n="overrides/"+p
        assert z.read(n)==(SOURCE/p).read_bytes(),n
    assert "enabled = false" in z.read("overrides/config/questlog-client.toml").decode()
    village=json.loads(z.read("overrides/config/paxi/datapacks/ao_structure_density/data/minecraft/worldgen/structure_set/villages.json"))
    assert village["placement"]["spacing"]==36 and village["placement"]["separation"]==8
    assert len(village["structures"])==5
    assert len(m["files"])==330
    print("PASS: v0.4.4 delta CRC, safe archive paths, unchanged 330 third-party mods, exact changed files.")
    print("NOT TESTED: actual Minecraft runtime, Malkuth binary fix, invalid NBT ownership, full progression.")
def run(args):
    base=P(args.base);out=P(args.output)
    assert base.resolve()!=out.resolve()
    with ZipFile(base) as a:
        checkzip(a)
        m=json.loads(a.read("manifest.json"))
        assert m["version"]==OLD,m["version"]
        m["version"]=VERSION;m["name"]=NAME
        out.parent.mkdir(parents=True,exist_ok=True)
        if not args.verify:
            changes={"overrides/"+p:p for p in PATHS}
            with ZipFile(out,"w",allowZip64=True) as z:
                for info in a.infolist():
                    n=info.filename
                    data=(json.dumps(m,indent=2)+"\n").encode() if n=="manifest.json" else (
                         (SOURCE/changes[n]).read_bytes() if n in changes else a.read(n))
                    z.writestr(info,data)
                for n,p in changes.items():
                    if n not in a.namelist():z.writestr(n,(SOURCE/p).read_bytes(),compress_type=ZIP_DEFLATED)
        with ZipFile(out) as z:verify(a,z)
    print("OUTPUT:",out,"SHA256",sha(out.read_bytes()))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--base",required=True);p.add_argument("--output",required=True)
    p.add_argument("--verify",action="store_true")
    run(p.parse_args())
