"""Static, SHA1-pinned Minecraft structure-template encounter scan (not a runtime test).

Traces a selected native jigsaw structure's start pool through native template
JSON and embedded jigsaw block 'pool' references, then inspects NBT palettes,
mob/trial spawner block-entity IDs and template entity IDs. Incomplete source
graphs, missing pools, unsupported NBT and bounded scans are ALWAYS reported
as incomplete: zero evidence is never proof that a dungeon has no encounters.
No files in the client/pack are modified.
"""
import argparse
import difflib
import gzip
import hashlib
import io
import json
import struct
import zlib
import zipfile
from collections import Counter, deque
from pathlib import Path
try:
 from pr56_stream_nbt import extract_selected
except ModuleNotFoundError:
 from tools.pr56_stream_nbt import extract_selected

PINS={
 "dungeons_arise":{"sha1":"c651339154da7b9e9cf47a80fdef22c4d59cad5c",
  "structures":("bandit_towers","foundry","illager_fort","keep_kayra","mechanical_nest","plague_asylum","aviary")},
 "idas":{"sha1":"154f275823f5f949ed492ac6ce078a80fc3c759a",
  "structures":("pillager_camp","labyrinth","necromancers_spire")},
}

class NBTReader:
 def __init__(self,data):
  self.bio=io.BytesIO(data)
  self.depth=0
 def read(self,n):
  b=self.bio.read(n)
  if len(b)!=n:raise ValueError("truncated NBT")
  return b
 def unpack(self,fmt):
  return struct.unpack(">"+fmt,self.read(struct.calcsize(">"+fmt)))[0]
 def name(self):
  n=self.unpack("H")
  if n>65535:raise ValueError("NBT name too long")
  return self.read(n).decode("utf-8",errors="replace")
 def payload(self,typ,depth=0):
  if depth>80:raise ValueError("NBT overdeep")
  if typ==0:return None
  if typ==1:return self.unpack("b")
  if typ==2:return self.unpack("h")
  if typ==3:return self.unpack("i")
  if typ==4:return self.unpack("q")
  if typ==5:return self.unpack("f")
  if typ==6:return self.unpack("d")
  if typ==7:
   n=self.unpack("i")
   if n<0 or n>12000000:raise ValueError("bad NBT byte array length")
   self.read(n);return {"_byte_array_length":n}
  if typ==8:return self.name()
  if typ==9:
   subtype=self.unpack("B");n=self.unpack("i")
   if n<0 or n>200000:raise ValueError("bad NBT list length")
   return [self.payload(subtype,depth+1) for _ in range(n)]
  if typ==10:
   o={}
   while True:
    child=self.unpack("B")
    if child==0:break
    key=self.name()
    o[key]=self.payload(child,depth+1)
   return o
  if typ in (11,12):
   n=self.unpack("i")
   if n<0 or n>12000000:raise ValueError("bad NBT array length")
   self.read(n*(4 if typ==11 else 8))
   return {"_numeric_array_length":n}
  raise ValueError("Unsupported NBT type "+str(typ))
 def root(self):
  typ=self.unpack("B")
  if typ!=10:raise ValueError("Expected named root NBT compound")
  self.name()
  return self.payload(10)

def nbt_from_bytes(raw):
 if len(raw)>22000000:raise ValueError("NBT template compressed byte limit exceeded")
 if raw[:2]==b"\x1f\x8b":raw=gzip.decompress(raw)
 elif raw[:1]==b"x":
  try:raw=zlib.decompress(raw)
  except zlib.error:pass
 if len(raw)>42000000:raise ValueError("NBT inflated byte limit exceeded")
 return NBTReader(raw).root()

def sha1(path):
 h=hashlib.sha1()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
 return h.hexdigest()

def loc_to_resource(ns,location,category):
 if not isinstance(location,str) or not location or location=="minecraft:empty":return None
 mod,_,path=location.partition(":")
 if not path:mod,path=ns,mod
 return f"data/{mod}/{category}/{path}"

def pool_elements(obj):
 found=[]
 def visit(obj):
  if isinstance(obj,dict):
   location=obj.get("location")
   if isinstance(location,str) and obj.get("element_type") in (
    "minecraft:single_pool_element","minecraft:legacy_single_pool_element",
    "integrated_api:integrated_api_single_pool_element"):
    found.append(location)
   if isinstance(obj.get("element"),dict):
    visit(obj["element"])
   for child in obj.get("elements",[]) if isinstance(obj.get("elements"),list) else []:
    visit(child)
  elif isinstance(obj,list):
   for item in obj:visit(item)
 visit(obj.get("elements",[]))
 return sorted(set(found))

def mounted_entities(root, max_depth=16):
 """Trace NBT Passengers of an entity payload, never item/equipment IDs.

 Vanilla entity 'Passengers' is a list of passenger entity compounds attached
 to the vehicle root. A spawner may put this payload under SpawnData.entity or
 SpawnPotentials[].data.entity. This reports source relationships only.
 """
 pairs=set();passenger_ids=set()
 def visit(node, depth):
  if depth>max_depth or not isinstance(node,dict):return
  parent=node.get("id")
  for passenger in node.get("Passengers",[]) if isinstance(node.get("Passengers"),list) else []:
   if not isinstance(passenger,dict):continue
   rider=passenger.get("id")
   if isinstance(rider,str) and ":" in rider:
    passenger_ids.add(rider)
    if isinstance(parent,str) and ":" in parent:
     pairs.add((parent,rider))
   visit(passenger,depth+1)
 visit(root,0)
 return passenger_ids,pairs

def extract_template(nbt):
 palettes=nbt.get("palette",[])
 if not palettes and nbt.get("palettes"):palettes=nbt["palettes"][0]
 blocks=nbt.get("blocks",[])
 entities=nbt.get("entities",[])
 counts=Counter();mob_ids=set();trials=set();jigsaw_pools=set();unknown_ids=set()
 normal_passengers=set();trial_passengers=set();normal_mounts=set();trial_mounts=set()
 prebuilt_passengers=set();prebuilt_mounts=set()
 for block in blocks:
  if not isinstance(block,dict):continue
  state=block.get("state",-1)
  if not isinstance(state,int) or state<0 or state>=len(palettes):continue
  entry=palettes[state]
  if not isinstance(entry,dict):continue
  name=entry.get("Name","")
  detail=block.get("nbt",{}) or {}
  if name in ("minecraft:spawner","minecraft:trial_spawner"):
   counts[name]+=1
   ids=set()
   # Only collect the entity ID at a spawner's actual entity payload.
   # A broad recursive search for all keys named 'id' is WRONG: it
   # misclassifies equipment, enchanted books and item IDs as mobs.
   def scan(x,depth=0):
    if depth>18:return
    if isinstance(x,dict):
     for key in ("entity","Entity"):
      entity=x.get(key)
      if isinstance(entity,dict):
       value=entity.get("id")
       if isinstance(value,str) and ":" in value:ids.add(value)
       nested,pairs=mounted_entities(entity)
       if name=="minecraft:spawner":
        normal_passengers.update(nested);normal_mounts.update(pairs)
       else:
        trial_passengers.update(nested);trial_mounts.update(pairs)
     entity_id=x.get("EntityId")
     if isinstance(entity_id,str) and ":" in entity_id:ids.add(entity_id)
     for key in ("SpawnData","SpawnPotentials","spawn_data","spawn_potentials",
                 "data","Data","normal_config","ominous_config","spawn_potentials"):
      child=x.get(key)
      if isinstance(child,(dict,list)):scan(child,depth+1)
    elif isinstance(x,list):
     for y in x:scan(y,depth+1)
   scan(detail)
   if name=="minecraft:spawner":mob_ids.update(ids)
   else:trials.update(ids)
  if name=="minecraft:jigsaw":
   pool=detail.get("pool")
   if isinstance(pool,str) and pool!="minecraft:empty":jigsaw_pools.add(pool)
 for entity in entities:
  n=entity.get("nbt",{}) if isinstance(entity,dict) else {}
  value=n.get("id")
  if isinstance(value,str) and ":" in value:unknown_ids.add(value)
  nested,pairs=mounted_entities(n)
  prebuilt_passengers.update(nested);prebuilt_mounts.update(pairs)
 return {"normal_spawners":counts["minecraft:spawner"],
         "trial_spawners":counts["minecraft:trial_spawner"],
         "normal_spawn_entity_ids":sorted(mob_ids),
         "trial_spawn_entity_ids":sorted(trials),
         "prebuilt_entity_ids":sorted(unknown_ids),
         "normal_spawner_passenger_entity_ids":sorted(normal_passengers),
         "trial_spawner_passenger_entity_ids":sorted(trial_passengers),
         "prebuilt_passenger_entity_ids":sorted(prebuilt_passengers),
         "normal_spawner_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(normal_mounts)],
         "trial_spawner_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(trial_mounts)],
         "prebuilt_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(prebuilt_mounts)],
         "jigsaw_child_pools":sorted(jigsaw_pools)}

def nearby_native_resources(names, namespace, resource, kind, max_results=5):
    """Suggest filenames, never silently replace a missing jigsaw reference."""
    prefix=f"data/{namespace}/"
    candidates=sorted(n for n in names if n.startswith(prefix) and
                      ("/worldgen/template_pool/" in n if kind=="pool"
                       else ("/structure/" in n or "/structures/" in n)) and
                      n.endswith(".json" if kind=="pool" else ".nbt"))
    desired=(loc_to_resource(namespace,resource,"worldgen/template_pool")+".json"
             if kind=="pool" else
             loc_to_resource(namespace,resource,"structure")+".nbt")
    guesses=difflib.get_close_matches(desired,candidates,n=max_results,cutoff=.50)
    return {"missing_reference":resource,"expected_path":desired,
            "best_existing_native_paths":guesses,
            "automatic_fix_authorized":False}

def inspect(jar,label,max_pools=160,max_templates=400):
 expected=PINS[label]
 digest=sha1(jar)
 if digest!=expected["sha1"]:raise RuntimeError("Pinned native SHA1 mismatch "+digest+" for "+label)
 with zipfile.ZipFile(jar) as z:
  names=set(z.namelist())
  structures={}
  for name in expected["structures"]:
   sid=label+":"+name
   struct_path=loc_to_resource(label,sid,"worldgen/structure")+".json"
   if struct_path not in names:
    structures[sid]={"source_structure_present":False,"native_graph_complete":False,
                      "blocking_issue":"MISSING_NATIVE_STRUCTURE_DEFINITION"}
    continue
   definition=json.loads(z.read(struct_path))
   start=definition.get("start_pool")
   to_visit=deque([start] if isinstance(start,str) else [])
   seen_pools=set();seen_templates=set();errors=[];pairs=[];totals=Counter();mobs=set();trial=set();prebuilt=set()
   normal_passengers=set();trial_passengers=set();prebuilt_passengers=set()
   normal_mount_pairs=set();trial_mount_pairs=set();prebuilt_mount_pairs=set()
   while to_visit:
    if len(seen_pools)>=max_pools or len(seen_templates)>=max_templates:
     errors.append("SOURCE_GRAPH_BUDGET_EXCEEDED__TRUNCATED")
     break
    pool=to_visit.popleft()
    if pool in seen_pools:continue
    seen_pools.add(pool)
    file=loc_to_resource(label,pool,"worldgen/template_pool")
    file=(file+".json") if file else None
    if file not in names:
     errors.append("MISSING_NATIVE_OR_EXTERNAL_POOL:"+str(pool));continue
    try:body=json.loads(z.read(file))
    except (ValueError,KeyError) as e:
     errors.append("INVALID_NATIVE_POOL:"+str(pool)+":"+str(e));continue
    if body.get("fallback") and body["fallback"]!="minecraft:empty":to_visit.append(body["fallback"])
    elements_in_pool=pool_elements(body)
    if not elements_in_pool:
     errors.append("POOL_WITHOUT_RECOGNIZED_SINGLE_TEMPLATE_LOCATIONS:"+str(pool)+":"+
                   json.dumps(body,sort_keys=True)[:1100])
    for template in elements_in_pool:
     if template in seen_templates:continue
     if len(seen_templates)>=max_templates:
      errors.append("SOURCE_TEMPLATE_BUDGET_EXCEEDED__TRUNCATED");break
     seen_templates.add(template)
     resource=loc_to_resource(label,template,"structure")
     candidates=[resource+".nbt",resource.replace("/structure/","/structures/")+".nbt"] if resource else []
     actual=next((r for r in candidates if r in names),None)
     if actual is None:
      errors.append("MISSING_EXTERNAL_OR_NATIVE_TEMPLATE:"+str(template));continue
     try:
      if template.startswith("dungeons_arise:keep_kayra/"):
       selected,scan_info=extract_selected(z,actual)
       parsed=extract_template(selected)
      else:
       parsed=extract_template(nbt_from_bytes(z.read(actual)))
     except (ValueError,KeyError,IndexError,RecursionError,EOFError) as e:
      errors.append("NBT_PARSE_FAILED:"+template+":"+str(e));continue
     totals["normal_spawners"]+=parsed["normal_spawners"]
     totals["trial_spawners"]+=parsed["trial_spawners"]
     mobs.update(parsed["normal_spawn_entity_ids"])
     trial.update(parsed["trial_spawn_entity_ids"])
     prebuilt.update(parsed["prebuilt_entity_ids"])
     normal_passengers.update(parsed["normal_spawner_passenger_entity_ids"])
     trial_passengers.update(parsed["trial_spawner_passenger_entity_ids"])
     prebuilt_passengers.update(parsed["prebuilt_passenger_entity_ids"])
     normal_mount_pairs.update((p["vehicle"],p["passenger"]) for p in parsed["normal_spawner_mount_pairs"])
     trial_mount_pairs.update((p["vehicle"],p["passenger"]) for p in parsed["trial_spawner_mount_pairs"])
     prebuilt_mount_pairs.update((p["vehicle"],p["passenger"]) for p in parsed["prebuilt_mount_pairs"])
     to_visit.extend(parsed["jigsaw_child_pools"])
     if parsed["normal_spawners"] or parsed["trial_spawners"] or parsed["prebuilt_entity_ids"]:
      pairs.append({"template":template,"source_path":actual,
                    "normal_spawners":parsed["normal_spawners"],
                    "trial_spawners":parsed["trial_spawners"],
                    "normal_spawn_entity_ids":parsed["normal_spawn_entity_ids"],
                    "trial_spawn_entity_ids":parsed["trial_spawn_entity_ids"],
                    "prebuilt_entity_ids":parsed["prebuilt_entity_ids"],
                    "normal_spawner_passenger_entity_ids":parsed["normal_spawner_passenger_entity_ids"],
                    "normal_spawner_mount_pairs":parsed["normal_spawner_mount_pairs"],
                    "trial_spawner_mount_pairs":parsed["trial_spawner_mount_pairs"],
                    "prebuilt_mount_pairs":parsed["prebuilt_mount_pairs"]})
   if not seen_templates:
    errors.append("NO_NATIVE_TEMPLATES_RESOLVED_FROM_START_POOL__NOT_PROOF_NO_MOBS")
   missing_reference_diagnostics=[]
   for err in errors:
    if err.startswith("MISSING_NATIVE_OR_EXTERNAL_POOL:"):
     ref=err.split(":",1)[1]
     missing_reference_diagnostics.append(
         nearby_native_resources(names,label,ref,"pool"))
    elif err.startswith("MISSING_EXTERNAL_OR_NATIVE_TEMPLATE:"):
     ref=err.split(":",1)[1]
     missing_reference_diagnostics.append(
         nearby_native_resources(names,label,ref,"template"))
   structures[sid]={
    "source_structure_present":True,"native_start_pool":start,
    "pools_visited":len(seen_pools),"templates_inspected":len(seen_templates),
    "positive_source_template_samples":pairs[:70],
    "positive_samples_truncated":len(pairs)>70,
    "source_normal_spawner_blocks":totals["normal_spawners"],
    "source_trial_spawner_blocks":totals["trial_spawners"],
    "source_normal_spawner_entity_ids":sorted(mobs),
    "source_trial_spawner_entity_ids":sorted(trial),
    "source_prebuilt_entity_ids":sorted(prebuilt),
    "source_normal_spawner_passenger_entity_ids":sorted(normal_passengers),
    "source_trial_spawner_passenger_entity_ids":sorted(trial_passengers),
    "source_prebuilt_passenger_entity_ids":sorted(prebuilt_passengers),
    "source_normal_spawner_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(normal_mount_pairs)],
    "source_trial_spawner_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(trial_mount_pairs)],
    "source_prebuilt_mount_pairs":[{"vehicle":a,"passenger":b} for a,b in sorted(prebuilt_mount_pairs)],
    "native_graph_complete":not errors,
    "source_graph_errors":errors[:70],
    "unresolved_resource_reference_diagnostics":missing_reference_diagnostics[:15],
    "source_graph_errors_truncated":len(errors)>70,
    "source_templates_do_NOT_establish_runtime_spawn_or_weighted_pool_reachability":True,
    "natural_generation_tested":False,
   }
 return {"label":label,"native_SHA1":digest,"pinned_by_PR50":True,
         "source_graph_only_not_runtime":True,"structures":structures}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--dungeons-arise",type=Path,required=True,dest="dungeons_arise")
 p.add_argument("--idas",type=Path,required=True)
 p.add_argument("--out",type=Path,required=True)
 a=p.parse_args()
 result={"method":"PR50_SHA1_PINNED_JIGSAW_TEMPLATE_NBT_READ_ONLY_WITH_BOUNDS",
         "no_live_profile_or_DD_changes":True,
         "providers":{m:inspect(getattr(a,m),m) for m in PINS}}
 a.out.parent.mkdir(parents=True,exist_ok=True)
 a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 for prov,entry in result["providers"].items():
  print("PROVIDER:",prov,"SHA1:",entry["native_SHA1"])
  for id,x in entry["structures"].items():
   print(id,"pools:",x.get("pools_visited",0),"templates:",x.get("templates_inspected",0),
         "normal spawners:",x.get("source_normal_spawner_blocks",0),
         "trial:",x.get("source_trial_spawner_blocks",0),
         "mob IDs:",x.get("source_normal_spawner_entity_ids",[]),
         "spawner passengers:",x.get("source_normal_spawner_passenger_entity_ids",[]),
         "mount pairs:",x.get("source_normal_spawner_mount_pairs",[]),
         "graph complete:",x.get("native_graph_complete"),
         "issues:",len(x.get("source_graph_errors",[])),
         "start_pool:",x.get("native_start_pool"),
         "sample_issues:",x.get("source_graph_errors",[])[:3])
 print("EVIDENCE:",a.out)

if __name__=="__main__":main()
