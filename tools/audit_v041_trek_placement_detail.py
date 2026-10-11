#!/usr/bin/env python3
"""Native Trek datapack footprint; flag placement rarity, not cosmetic structures."""
from collections import Counter
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile
from audit_v041_native_trek_create import LOCK,download,ROOT

OUT=ROOT/"build/trek_native_placement_detail.json"

def main():
    item=LOCK["additions"]["trek-structure-expansion"]
    blob=download(item)
    groups=Counter()
    entries=[]
    biome_tags=[]
    with ZipFile(io.BytesIO(blob)) as z:
        for name in z.namelist():
            if not name.startswith("data/"):continue
            parts=name.split("/")
            if len(parts)<3:continue
            if len(parts)>=4:groups[(parts[1],parts[2])]+=1
            if not name.endswith(".json"):continue
            if re.fullmatch(r"data/[^/]+/worldgen/(placed_feature|configured_feature|structure|structure_set|biome_modifier)/[^/]+\.json",name):
                try:data=json.loads(z.read(name))
                except Exception:continue
                e={"path":name}
                if "/placed_feature/" in name:
                    e["feature"]=data.get("feature")
                    e["placement"]=data.get("placement")
                elif "/configured_feature/" in name:
                    e["type"]=data.get("type")
                elif "/structure_set/" in name:
                    e["placement"]=data.get("placement")
                    e["structures"]=data.get("structures")
                else:e["type"]=data.get("type");e["biomes"]=data.get("biomes")
                entries.append(e)
            if "/tags/worldgen/biome/" in name:biome_tags.append(name)
    summary={
        "source":{"projectID":item["projectId"],"fileID":item["id"],"filename":item["fileName"]},
        "directory_groups": [{"namespace":x[0],"category":x[1],"count":n} for x,n in groups.most_common()],
        "worldgen_entries":sorted(entries,key=lambda x:x["path"]),
        "biome_tag_paths":sorted(biome_tags),
        "runtime_verified":False,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(summary,indent=2)+"\n")
    print("TREK_GROUP_COUNTS",json.dumps(summary["directory_groups"][:60]))
    for e in summary["worldgen_entries"]:
        if "/placed_feature/" in e["path"]:
            print("TREK_FEATURE",e["path"],json.dumps(e.get("placement"),separators=(",",":"))[:750])
    print("TREK_PLACED",sum("/placed_feature/" in e["path"] for e in entries),
          "STRUCT_SET",sum("/structure_set/" in e["path"] for e in entries),
          "NATIVE_REGISTRIES",len(entries))

if __name__=="__main__":main()
