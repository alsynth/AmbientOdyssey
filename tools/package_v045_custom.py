#!/usr/bin/env python3
"""Reproducible, fail-closed AO v0.4.5 custom integration preview.

Input is the exact successful v0.4.4 private CurseForge ZIP. This inserts the
compiled AO Affix Trims JAR, updates TRMT's player erosion, and patches Malkuth's
first-piece pool without removing its other connector pieces. The original mod
pins and the tested old import remain unchanged. This package does not port
Apotheotic Additions.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT/"release_030/overrides"
OLD="0.4.4-experimental-preperformance"
NEW="0.4.5-experimental-custom-integration"
NAME="Ambient Odyssey v0.4.5 - Custom Integration PREVIEW"
CHANGES=[
"config/trmt.json",
"config/paxi/datapacks/ao_structure_repairs/data/fdbosses/worldgen/template_pool/malkuth_arena.json",
"config/paxi/datapacks/ao_structure_repairs/data/fdbosses/worldgen/structure/malkuth_arena.json",
"config/paxi/datapacks/ao_structure_repairs/data/ao_structure_repairs/worldgen/template_pool/malkuth_start.json",
]
JARNAME="ao-affix-trims-0.1.0-experimental.jar"
JARPATH="overrides/mods/"+JARNAME

def digest(b):return hashlib.sha256(b).hexdigest()
def check(z):
    assert z.testzip() is None,"Corrupt ZIP member"
    names=z.namelist()
    assert names.count("manifest.json")==1 and len(names)==len(set(names))
    assert all(not n.startswith("/") and ".." not in n.split("/") and "\\" not in n for n in names)
def verify(src,dst,addon):
    check(src);check(dst)
    a=json.loads(src.read("manifest.json"))
    b=json.loads(dst.read("manifest.json"))
    assert a["version"]==OLD and b["version"]==NEW
    assert b["name"]==NAME
    assert len(b["files"])==330 and a["files"]==b["files"] and a["minecraft"]==b["minecraft"]
    changes={"overrides/"+p for p in CHANGES}
    assert set(dst.namelist())==set(src.namelist())|changes|{JARPATH}
    for name in src.namelist():
        if name not in changes and name!="manifest.json":
            assert digest(dst.read(name))==digest(src.read(name)),name
    for p in CHANGES:
        assert dst.read("overrides/"+p)==(SOURCE/p).read_bytes(),p
    assert dst.read(JARPATH)==addon.read_bytes()
    with ZipFile(addon) as modjar:
        check(modjar)
        assert "ao_affix_trims" in modjar.read("META-INF/neoforge.mods.toml").decode()
        assert "ao_affix_trims:random_affix_armor_trim" in modjar.read("data/neoforge/loot_modifiers/global_loot_modifiers.json").decode()
    cfg=json.loads(dst.read("overrides/config/trmt.json"))
    assert cfg["erosionMultipliers"]["player"]==1.0
    p=lambda path:json.loads(dst.read("overrides/config/paxi/datapacks/ao_structure_repairs/data/"+path))
    full=p("fdbosses/worldgen/template_pool/malkuth_arena.json")
    start=p("ao_structure_repairs/worldgen/template_pool/malkuth_start.json")
    structure=p("fdbosses/worldgen/structure/malkuth_arena.json")
    assert len(full["elements"])==16, "The quarter-arena regression must not recur"
    assert len(start["elements"])==1 and start["elements"][0]["element"]["location"].endswith("part_1")
    assert structure["start_pool"]=="ao_structure_repairs:malkuth_start"
    print("PASS: archive integrity; 330 unchanged CF mod pins; source-perfect TRMT, full Malkuth and compiled trim addon")
    print("UNVERIFIED IN GAME: affix loot modifier order/mob drops, new Malkuth assembly, high-scale Questlog UI.")
    print("NOT INCLUDED: a NeoForge port of legacy Apotheotic Additions.")

def run(args):
    source=pathlib.Path(args.base)
    addon=pathlib.Path(args.addon)
    out=pathlib.Path(args.output)
    assert source.resolve()!=out.resolve()
    with ZipFile(source) as z:
        check(z)
        m=json.loads(z.read("manifest.json"))
        assert m["version"]==OLD,m["version"]
        m["version"]=NEW
        m["name"]=NAME
        entries={"overrides/"+p:p for p in CHANGES}
        if not args.verify:
            out.parent.mkdir(parents=True,exist_ok=True)
            with ZipFile(out,"w",allowZip64=True) as dst:
                for info in z.infolist():
                    name=info.filename
                    if name=="manifest.json": data=(json.dumps(m,indent=2)+"\n").encode()
                    elif name in entries:data=(SOURCE/entries[name]).read_bytes()
                    else:data=z.read(name)
                    dst.writestr(copy.copy(info),data)
                for name,path in entries.items():
                    if name not in z.namelist():dst.writestr(name,(SOURCE/path).read_bytes(),compress_type=ZIP_DEFLATED)
                assert JARPATH not in z.namelist()
                dst.writestr(JARPATH,addon.read_bytes(),compress_type=ZIP_DEFLATED)
        with ZipFile(out) as built:verify(z,built,addon)
    print("OUTPUT",out)
    print("SHA256",digest(out.read_bytes()))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--base",required=True)
    p.add_argument("--addon",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--verify",action="store_true")
    run(p.parse_args())
