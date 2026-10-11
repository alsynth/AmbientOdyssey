#!/usr/bin/env python3
"""Reversible v0.4.1 A/B profiler toggle; no claimed speed improvement.

Creates a separately named import ZIP whose ONLY changed override is Spark's
backgroundProfiler setting. All mod, addon, quest and worldgen resources remain
byte-identical, and original package is never overwritten.
"""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

CONFIG="overrides/config/spark/config.json"

def build(source, target):
    assert source.resolve()!=target.resolve()
    with ZipFile(source) as src:
        assert src.testzip() is None
        names=src.namelist()
        assert CONFIG in names and "manifest.json" in names
        conf=json.loads(src.read(CONFIG))
        assert conf.get("backgroundProfiler") is True, "expected profiler baseline ON"
        conf["backgroundProfiler"]=False
        manifest=json.loads(src.read("manifest.json"))
        assert len(manifest["files"])==330, "requires consolidated 330-reference source"
        assert not manifest["version"].endswith("-spark-off")
        manifest["version"]+="-spark-off"
        manifest["name"]+=" [Spark Background OFF A/B]"
        target.parent.mkdir(parents=True,exist_ok=True)
        with ZipFile(target,"w") as dst:
            for inf in src.infolist():
                blob=src.read(inf.filename)
                if inf.filename==CONFIG:
                    blob=(json.dumps(conf,indent=2)+"\n").encode("utf-8")
                if inf.filename=="manifest.json":
                    blob=(json.dumps(manifest,indent=2)+"\n").encode("utf-8")
                dst.writestr(inf,blob)
    verify(source,target)
    print("OUTPUT",target,sha(target.read_bytes()))

def sha(value):
    return hashlib.sha256(value).hexdigest()

def verify(source, target):
    with ZipFile(source) as old, ZipFile(target) as new:
        assert old.testzip() is None and new.testzip() is None
        before=old.namelist()
        after=new.namelist()
        assert before==after, "members drift"
        assert len(after)==len(set(after)), "duplicate members"
        modified=[name for name in after if old.read(name)!=new.read(name)]
        assert set(modified)=={CONFIG,"manifest.json"}, modified
        original=json.loads(old.read("manifest.json"))
        edited=json.loads(new.read("manifest.json"))
        assert original["files"]==edited["files"]
        assert original["minecraft"]==edited["minecraft"]
        assert json.loads(old.read(CONFIG))["backgroundProfiler"] is True
        assert json.loads(new.read(CONFIG))["backgroundProfiler"] is False
        assert set(original)-{"name","version"} == set(edited)-{"name","version"}
        assert all(original[k]==edited[k] for k in original if k not in {"name","version"})
    print("PASS profiler-only A/B variant, no other overrides or mods changed")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    p.add_argument("target",type=Path)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    if a.verify:verify(a.source,a.target)
    else:build(a.source,a.target)
