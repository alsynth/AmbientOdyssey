"""PR56 SHA1-pinned Dungeons Arise + IDAS actual native biome tag closure.

Reads exact mod JAR JSONs and AO Paxi source overrides; no mod/profile edits.
AO Paxi source additions are NOT a complete runtime tag resolution because
Minecraft and other mods can provide additional tags or higher priority data.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
PAXI=ROOT/"release_030/overrides/config/paxi/datapacks"
ROSTER=ROOT/"docs/audits/CURRENT_BIOME_ROSTER.json"
PINS={
 "dungeons_arise":{
   "sha1":"c651339154da7b9e9cf47a80fdef22c4d59cad5c",
   "file":"DungeonsArise-1.21.1-2.1.68-release.jar",
   "project":442508,"fileID":7150870,
   "targets":("dungeons_arise:bandit_towers","dungeons_arise:bandit_village",
              "dungeons_arise:ceryneian_hind","dungeons_arise:scorched_mines",
              "dungeons_arise:shiraz_palace"),
 },
 "idas":{
   "sha1":"154f275823f5f949ed492ac6ce078a80fc3c759a",
   "file":"idas-1.13.7+1.21.1-neoforge.jar",
   "project":605375,"fileID":8232359,
   "targets":("idas:desert_pyramid","idas:desert_ruins",
              "idas:labyrinth","idas:necromancers_spire"),
 }
}

def sha1(path):
 h=hashlib.sha1()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 return h.hexdigest()

def load_z(z,key):
 try:
  with z.open(key) as s:return json.load(s)
 except KeyError:return None

def tag_id(src):
 parts=src.split("/")
 return parts[1]+":"+src.split("/tags/worldgen/biome/")[1][:-5]

def source_dict(jar):
 with zipfile.ZipFile(jar) as z:
  names=z.namelist()
  structures={};tags={};sets={}
  for src in names:
   if not src.startswith("data/") or not src.endswith(".json"):continue
   if "/worldgen/structure/" in src:
    key=src.split("/")[1]+":"+src.split("/worldgen/structure/")[1][:-5]
    structures[key]={"path":src,"json":load_z(z,src)}
   elif "/tags/worldgen/biome/" in src:
    tags[tag_id(src)]={"path":src,"json":load_z(z,src)}
   elif "/worldgen/structure_set/" in src:
    key=src.split("/")[1]+":"+src.split("/worldgen/structure_set/")[1][:-5]
    sets[key]={"path":src,"json":load_z(z,src)}
 return structures,tags,sets

def tag_entries(j):
 out=[]
 for v in j.get("values",[]) if isinstance(j,dict) else []:
  if isinstance(v,str):out.append(v)
  elif isinstance(v,dict) and isinstance(v.get("id"),str):out.append(v["id"])
 return out

def paxi_biome_tags_and_resources():
 tag_source=defaultdict(list);worldgen=defaultdict(list)
 for pack in sorted(PAXI.iterdir()):
  if not pack.is_dir():continue
  data=pack/"data"
  if not data.is_dir():continue
  for path in data.rglob("*.json"):
   rel=path.relative_to(pack).as_posix()
   if "/tags/worldgen/biome/" not in rel and "/worldgen/structure/" not in rel and "/worldgen/structure_set/" not in rel:continue
   obj=json.loads(path.read_text(encoding="utf-8"))
   if "/tags/worldgen/biome/" in rel:
    id=tag_id(rel)
    tag_source[id].append({"pack":pack.name,"file":rel,"replace":obj.get("replace",False),"values":tag_entries(obj)})
   else:
    worldgen[rel].append({"pack":pack.name,"json":obj})
 return dict(tag_source),dict(worldgen)

def inspect(label,path,ao_tags,ao_world,curated):
 pin=PINS[label]
 digest=sha1(path)
 if digest!=pin["sha1"]:raise RuntimeError("Wrong "+label+" JAR SHA1: "+digest)
 structs,native_tags,native_sets=source_dict(path)
 out={}
 for sid in pin["targets"]:
  r=structs.get(sid)
  if not r:raise RuntimeError("Missing native source definition: "+sid)
  obj=r["json"]
  selected=obj.get("biomes")
  selectors=[selected] if isinstance(selected,str) else selected if isinstance(selected,list) else []
  visited=set();records={};resolved=set();missing=set()
  stack=[x for x in selectors if isinstance(x,str)]
  while stack:
   current=stack.pop()
   if not current.startswith("#"):
    resolved.add(current);continue
   id=current[1:]
   if id in visited:continue
   visited.add(id)
   native=native_tags.get(id)
   overlays=ao_tags.get(id,[])
   sources=[]
   if native:
    sources.append({"source":"pinned_native_jar","values":tag_entries(native["json"]),
                    "replace":native["json"].get("replace",False)})
   sources.extend([{"source":"AO_Paxi:"+v["pack"],"values":v["values"],
                     "replace":v["replace"]} for v in overlays])
   if not sources:missing.add(id)
   for source in sources:
    for entry in source["values"]:
     stack.append(entry)
   records[id]={"native_present":native is not None,
                "paxi_sources":[p["pack"] for p in overlays],
                "contributing_sources":sources}
  members=[]
  for set_id,set_row in native_sets.items():
   if any(e.get("structure")==sid for e in set_row["json"].get("structures",[]) if isinstance(e,dict)):
    members.append({"set_id":set_id,"native_placement":set_row["json"].get("placement"),
                    "AO_Paxi_structure_set_candidates":ao_world.get(set_row["path"],[])})
  out[sid]={
   "native_structure_file":r["path"],
   "native_structure_definition":obj,
   "source_selector_tags":records,
   "missing_or_external_tag_definitions":sorted(missing),
   "all_source_possible_direct_biome_ids":sorted(resolved),
   "curated_direct_biome_overlap":sorted(curated&resolved),
   "native_structure_set_memberships":members,
   "AO_Paxi_same_structure_resource":ao_world.get(r["path"],[]),
   "runtime_biome_tag_closure_proven":False,
   "runtime_generation_verified":False,
  }
 return {"mod":label,"jar_sha1":digest,"pin":pin,"native_structure_count":len(structs),
         "native_biome_tag_count":len(native_tags),
         "native_set_count":len(native_sets),"targets":out}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--dungeons-arise",type=Path,required=True,dest="dungeons_arise")
 p.add_argument("--idas",type=Path,required=True)
 p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 roster=json.loads(ROSTER.read_text(encoding="utf-8"))
 curated={k+":"+v for k,vals in roster.items() for v in vals}
 ao_tags,ao_world=paxi_biome_tags_and_resources()
 providers={name:inspect(name,getattr(a,name),ao_tags,ao_world,curated) for name in PINS}
 result={"scope":"SHA1_VERIFIED_PR50_JAR_PLUS_REPO_AO_PAXI_SOURCES_NOT_FULL_GAME_REGISTRY",
         "AO_Paxi_pack_count":len([x for x in PAXI.iterdir() if x.is_dir()]),
         "providers":providers,"curated_count":len(curated),
         "no_current_modpack_gameplay_changes":True}
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 for name,mod in providers.items():
  print(name,"verified_SHA1",mod["jar_sha1"],"native_structures",mod["native_structure_count"])
  for sid,row in mod["targets"].items():
   print(sid,"curated_biomes",row["curated_direct_biome_overlap"],
         "missing_external_tags",row["missing_or_external_tag_definitions"],
         "paxi_structure_override",len(row["AO_Paxi_same_structure_resource"]))
 print("REPORT:",a.out)

if __name__=="__main__":
 main()
