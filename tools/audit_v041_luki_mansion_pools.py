#!/usr/bin/env python3
"""Inspect pinned Luki Woodland Mansions 1.21.1 JAR for missing jigsaw pool refs.
Source-backed preparation only: no speculative datapack/pool changes.
"""
import gzip, hashlib, io, json, os, pathlib
from urllib.request import urlopen,Request
from zipfile import ZipFile
URL="https://cdn.modrinth.com/data/RZN5D3zs/versions/1fEmTmPi/lukis-woodland-mansions-v1.0.jar"
EXPECTED_SHA="61c477cbe76847a204157c92b944438edc610abd91c71aff1ab7e58aca3a1e65"
NEEDLE=b"mansions:mansion/bottom_back_left"
def main():
    req=Request(URL,headers={"User-Agent":"AmbientOdyssey-native-pool-audit/1.0"})
    data=urlopen(req,timeout=90).read()
    sha=hashlib.sha256(data).hexdigest()
    assert sha==EXPECTED_SHA,(sha,EXPECTED_SHA)
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        allfiles=z.namelist()
        pools={p for p in allfiles if "/worldgen/template_pool/" in p and p.endswith(".json")}
        expect="data/mansions/worldgen/template_pool/mansion/bottom_back_left.json"
        candidates=sorted(p for p in pools if any(w in p.lower() for w in ("bottom","back","left","mansion")))
        # Search references in actual native pool JSON and raw/generated nbt templates;
        # gzip decompress vanilla NBT (nbtlib not required for simple registry strings).
        uses=[]
        for p in allfiles:
            if not p.endswith((".json",".nbt",".mcfunction")):continue
            try:
                raw=z.read(p)
                if p.endswith(".nbt"):
                    try:raw=gzip.decompress(raw)
                    except OSError:pass
                if NEEDLE in raw:uses.append(p)
            except (ValueError,EOFError):continue
        result={"official_jar":URL,"source_sha256":sha,"logged_missing_reference":NEEDLE.decode(),
                "expected_pool_file":expect,"expected_pool_exists":expect in pools,
                "total_template_pools":len(pools),"native_mansion_pool_candidates":candidates,
                "actual_native_files_referencing_missing_pool":uses,
                "not_a_fix":"Inspect required target and source paths before designing a datapack alias."}
        p=pathlib.Path("build/v041-luki-mansion-pools.json");p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
if __name__=="__main__":main()
