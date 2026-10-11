#!/usr/bin/env python3
"""Native-only source audit for exactly pinned Trek and Create structure mods.

Downloads only the three filenames pinned in the repo lock from CurseForge's
file CDN, prints no private Minecraft runtime/player metadata. No source changes.
"""
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import quote
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/"release_030/release-lock.json").read_text())
SLUGS=("trek-structure-expansion","test6-create-structures-arise","test6-create-easy-structures")
RESULT=ROOT/"build/native_trek_create_density_catalogue.json"

def download(item):
    fid=item["id"]
    parts=f"{fid//1000}/{fid%1000:03d}"
    urls=[
      "https://mediafilez.forgecdn.net/files/"+parts+"/"+quote(item["fileName"]),
      "https://edge.forgecdn.net/files/"+parts+"/"+quote(item["fileName"]),
    ]
    errors=[]
    for url in urls:
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"AmbientOdyssey-SourceAuditor/1.0"})
            with urllib.request.urlopen(req,timeout=90) as f:blob=f.read(50_000_000)
            assert len(blob)<50_000_000
            with ZipFile(io.BytesIO(blob)) as z: assert z.testzip() is None
            return blob
        except Exception as exc:errors.append(type(exc).__name__)
    raise RuntimeError(f"Could not read pinned {item['fileName']}: {errors}")

def audit_zip(blob):
    sets=[]
    structures=[]
    cfg=[]
    with ZipFile(io.BytesIO(blob)) as z:
        for name in z.namelist():
            if name.endswith(".json") and re.fullmatch(r"data/[^/]+/worldgen/structure_set/.+\.json",name):
                try:
                    obj=json.loads(z.read(name))
                except (ValueError,UnicodeError):continue
                placement=obj.get("placement",{}) if isinstance(obj,dict) else {}
                sets.append({"path":name,"structures":obj.get("structures"),
                             "placement":{k:placement.get(k) for k in ("type","spacing","separation","frequency","frequency_reduction_method","salt") if k in placement}})
            elif re.fullmatch(r"data/[^/]+/worldgen/structure/.+\.json",name):
                structures.append(name)
            elif name.endswith((".toml",".json5",".cfg",".properties")) and (("config" in name.lower()) or ("structure" in name.lower())):
                cfg.append(name)
    return {"sets":sorted(sets,key=lambda x:x["path"]),"native_structures":sorted(structures),
            "related_configs":sorted(cfg)}

def main():
    result={"schema":"ao_native_trek_create_1_21_1","minecraft_runtime_tested":False,"mods":{}}
    for slug in SLUGS:
        item=LOCK["additions"][slug]
        raw=download(item)
        entry=audit_zip(raw)
        entry.update({"pin":{"projectID":item["projectId"],"fileID":item["id"],"filename":item["fileName"]},
                      "sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
                      "native_set_count":len(entry["sets"]),"native_structure_count":len(entry["native_structures"])})
        result["mods"][slug]=entry
        print("NATIVE AUDIT",slug,"bytes",len(raw),"sha256",entry["sha256"],
              "SETS",len(entry["sets"]),"STRUCTURES",len(entry["native_structures"]),"CONFIGS",len(entry["related_configs"]))
        for q in entry["sets"]:
            print("SET",q["path"],json.dumps(q["placement"],sort_keys=True),
                  "entries",len(q.get("structures") or []))
    RESULT.parent.mkdir(parents=True,exist_ok=True)
    RESULT.write_text(json.dumps(result,indent=2)+"\n")
    print("Saved native catalogue to artifact; no gameplay files altered")

if __name__=="__main__":main()
