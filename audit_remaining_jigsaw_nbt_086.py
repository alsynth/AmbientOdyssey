#!/usr/bin/env python3
"""Read-only binary provenance audit: exact pinned CurseForge JARs vs malformed jigsaw NBT.

Executed in GitHub CI; never mutates source, binaries or worldgen. Treat opaque
curseforge metadata as data only. Logs *evidence*, never invents NBT assets.
"""
import collections
import concurrent.futures
import gzip
import hashlib
import io
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request
import zipfile

import nbtlib

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release_030"
HEADERS = {"User-Agent": "AmbientOdyssey-SourceNBT-Audit/1.0", "Accept": "application/json"}

def fetch(url, limit=100000000, timeout=25):
    req=urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req,timeout=timeout) as f:
        data=f.read(limit+1)
        if len(data)>limit:
            raise ValueError("remote file too big")
        return data

def indexed_jars():
    p=RELEASE/"evidence/jar-resource-index-test6.json.gz"
    x=json.loads(gzip.decompress(p.read_bytes()))
    return {j["file"]:j for j in x["jars"]}

def manifest_pairs():
    lock=json.loads((RELEASE/"release-lock.json").read_text())
    with zipfile.ZipFile(ROOT/lock["baseline"]) as z:
        m=json.loads(z.read("manifest.json"))
    removed=set(lock["remove_projects"].values())
    pairs={x["projectID"]:x["fileID"] for x in m["files"] if x["projectID"] not in removed}
    for v in lock["additions"].values():
        pairs[v["projectId"]]=v["id"]
    if lock.get("default_integrated_patches"):
        v=lock["optional_integrated_patches"]
        pairs[v["projectId"]]=v["id"]
    return pairs

def resolve(item):
    pid,fid=item
    try:
        payload=json.loads(fetch(f"https://api.cfwidget.com/{pid}",limit=900000,timeout=18))
        record=next((f for f in payload.get("files",[]) if f.get("id")==fid),None)
        if not record:
            return pid,fid,None,"file not in CFWidget currently indexed releases"
        return pid,fid,record.get("name"),None
    except Exception as e:
        return pid,fid,None,type(e).__name__+":"+str(e)[:120]

def inspect_jar(entry, fid, filename):
    name=entry["file"]
    s=str(fid)
    url=f"https://mediafilez.forgecdn.net/files/{int(s[:-3])}/{int(s[-3:])}/{urllib.parse.quote(filename)}"
    try:
        raw=fetch(url,limit=100000000,timeout=90)
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=entry["sha256"]:
            return dict(jar=name,error="SHA mismatch vs user's exact Test6 binary",got_sha=digest,expected_sha=entry["sha256"],size=len(raw))
        matches=[]; examined=0; potential=0
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for file in z.namelist():
                if not file.endswith(".nbt") or "/structure/" not in file:
                    continue
                examined+=1
                blob=z.read(file)
                try: plain=gzip.decompress(blob)
                except Exception: continue
                # Search for NBT UTF-8 string with 10-byte length prefix.
                if b"minecraft:" not in plain or b"pool" not in plain or b"jigsaw" not in plain:
                    continue
                if b"\x00\x0aminecraft:" not in plain:
                    continue
                potential+=1
                try:
                    doc=nbtlib.File.parse(io.BytesIO(plain))
                    palette=doc["palette"]
                    for block in doc["blocks"]:
                        state=palette[int(block["state"])]
                        if str(state["Name"])!="minecraft:jigsaw": continue
                        tile=block.get("nbt",{})
                        pool=str(tile.get("pool",""))
                        if pool in ("minecraft:",""):
                            matches.append({"template":file,"pos":[int(x) for x in block["pos"]],"pool":pool,"name":str(tile.get("name","")),"target":str(tile.get("target","")),"final_state":str(tile.get("final_state","")),"sha256":hashlib.sha256(blob).hexdigest()})
                except Exception as e:
                    matches.append({"template":file,"parse_error":type(e).__name__+":"+str(e)[:150]})
        return dict(jar=name,fileid=fid,sha256=digest,examined=examined,potential=potential,matches=matches)
    except Exception as e:
        return dict(jar=name,fileid=fid,error=type(e).__name__+":"+str(e)[:160])

def main():
    start=time.monotonic()
    index=indexed_jars()
    candidates={name:item for name,item in index.items() if item.get("counts",{}).get("worldgen/template_pool",0)>0 or item.get("counts",{}).get("worldgen/structure",0)>0}
    print("INDEXED",len(index),"CANDIDATE_STRUCTURE_JARS",len(candidates),flush=True)
    pairs=manifest_pairs()
    print("CURRENT_MANIFEST_PROJECT_REFS",len(pairs),flush=True)
    resolved={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as exe:
        for pid,fid,filename,err in exe.map(resolve,pairs.items()):
            if filename: resolved[filename]=(pid,fid)
    print("RESOLVED_CURSEFORGE_FILENAME_COUNT",len(resolved),"missing",len(pairs)-len(resolved),flush=True)
    applicable=[]
    for name,entry in candidates.items():
        if name in resolved:
            applicable.append((entry,resolved[name][1],name))
    print("STRUCTURE_JARS_MAPPED",len(applicable),"out of",len(candidates),flush=True)
    missing=sorted(set(candidates)-set(resolved))
    print("UNMAPPED_STRUCTURE_JARS",json.dumps(missing)[:14000],flush=True)
    results=[]
    # CPU I/O: parallel fetch; individual NBT parsing is bounded by candidate-filter hits
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        fut=[exe.submit(inspect_jar,*item) for item in applicable]
        for f in concurrent.futures.as_completed(fut):
            a=f.result()
            results.append(a)
            if a.get("matches"):
                print("FOUND_BLANK_POOL",json.dumps(a,ensure_ascii=False)[:25000],flush=True)
            elif a.get("error"):
                print("AUDIT_ERROR",a["jar"],a["error"],flush=True)
            elif len(results)%15==0:
                print("PROGRESS",len(results),"/",len(applicable),flush=True)
    output={"method":"exact jar SHA and native compressed NBT parse","elapsed_seconds":time.monotonic()-start,
        "indexed_candidate_jars":len(candidates),"mapped_jars":len(applicable),
        "missing_jars":missing,"results":sorted(results,key=lambda x:x["jar"])}
    dest=Path("build/jigsaw-source-audit-086.json")
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(output,indent=2),encoding="utf-8")
    print("AUDIT_SUMMARY",json.dumps({"scanned":len(results),"blank_pool_templates":sum(len(x.get("matches",[])) for x in results),"unmapped":len(missing),"fetch_or_SHA_errors":sum(bool(x.get("error")) for x in results),"report":str(dest)}),flush=True)
if __name__=="__main__":
    main()
