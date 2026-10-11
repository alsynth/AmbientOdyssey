#!/usr/bin/env python3
"""Fail-closed verification of exactly two source-checked private IDAS NBT overrides."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import nbtlib
from repair_v041_idas_create_items import OUT, REPORT, TEMPLATES, OLD, NEW

PACK="overrides/config/paxi/datapacks/ao_idas_create_item_compat/"

def assert_content(blob, expected):
    nbt=nbtlib.File.parse(io.BytesIO(gzip.decompress(blob)))
    count=0
    def scan(node, path=()):
        nonlocal count
        if isinstance(node,dict):
            if str(node.get("id",""))==NEW and "Items" in path:
                count+=1
            if str(node.get("id",""))==OLD and "Items" in path:
                raise AssertionError("legacy Create ID remains")
            for k,v in node.items():scan(v,(*path,str(k)))
        elif isinstance(node,(list,tuple)):
            for i,v in enumerate(node):scan(v,(*path,i))
    scan(nbt)
    assert count==expected,(count,expected)
    return count

def validate(archive):
    report=json.loads(REPORT.read_text())
    assert report["replacements"]==7
    assert report["old_item"]==OLD and report["new_item"]==NEW
    assert set(report["source_templates"])==set(TEMPLATES)
    with ZipFile(archive) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        pack=json.loads(z.read(PACK+"pack.mcmeta"))
        assert pack["pack"]["pack_format"]==48
        exact={n for n in names if n.startswith(PACK) and n.endswith(".nbt")}
        assert exact=={PACK+p for p in TEMPLATES}
        for member,count in TEMPLATES.items():
            blob=z.read(PACK+member)
            assert hashlib.sha256(blob).hexdigest()==report["source_templates"][member]["patched_sha256"]
            assert_content(blob,count)
    print("PASS: two private SHA-checked IDAS templates / seven crushed_raw_iron substitutions / no other native NBT overrides")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("zip",type=Path)
    validate(p.parse_args().zip)
