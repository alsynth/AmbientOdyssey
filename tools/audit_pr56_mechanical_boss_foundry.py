"""PR56 exact pinned WDA boss-marker and unresolved-jigsaw-reference audit.

This extracts *source evidence only* from the SHA1-pinned PR50 Dungeons Arise
2.1.68 JAR. It does NOT presume Mechanical Nest includes a particular native
boss or that the boss is necessarily from WDA, and it never changes configs.

Usage: python tools/audit_pr56_mechanical_boss_foundry.py --jar FILE --out FILE
"""
import argparse
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

try:
    from audit_pr56_native_template_spawners import (
        nbt_from_bytes, loc_to_resource, pool_elements, sha1,
        nearby_native_resources,
    )
    from pr56_stream_nbt import extract_selected
except ModuleNotFoundError:
    from tools.audit_pr56_native_template_spawners import (
        nbt_from_bytes, loc_to_resource, pool_elements, sha1,
        nearby_native_resources,
    )
    from tools.pr56_stream_nbt import extract_selected

PINNED_SHA1="c651339154da7b9e9cf47a80fdef22c4d59cad5c"
ROOT=Path(__file__).resolve().parents[1]
SECTIONS=("mechanical_nest","foundry")
SIGNAL_FIELDS=("CustomName","custom_name","Tags","tags","Health","health",
               "Attributes","attributes","ActiveEffects","active_effects",
               "DeathLootTable","DeathLootTableSeed","DeathTime",
               "PersistenceRequired","CanPickUpLoot","NoAI","IsBaby",
               "equipped","equipment","HandItems","ArmorItems")
SPECIAL_BLOCKS={"minecraft:spawner","minecraft:trial_spawner",
                "minecraft:command_block","minecraft:chain_command_block",
                "minecraft:repeating_command_block","minecraft:structure_block",
                "minecraft:jigsaw"}
FLAGS=("boss","guardian","captain","king","queen","champion",
       "mechanical_nest","mechanical_nest_","foundry")

def normalize(value):
    if isinstance(value,str):return value
    if isinstance(value,(int,float,bool)):return value
    if isinstance(value,list):return [normalize(x) for x in value[:8]]
    if isinstance(value,dict):
        return {k:normalize(v) for k,v in value.items() if k in SIGNAL_FIELDS or k in ("id","value","name")}
    return str(value)[:200]

def entity_payloads(spawner):
    """Walk ONLY canonical spawn payload keys; no item/equipment ID search."""
    entities=[]
    def visit(node,level=0):
        if level>15:return
        if isinstance(node,dict):
            for k in ("entity","Entity"):
                v=node.get(k)
                if isinstance(v,dict) and isinstance(v.get("id"),str):
                    entities.append(v)
            for k in ("SpawnData","SpawnPotentials","spawn_data",
                      "spawn_potentials","normal_config","ominous_config",
                      "data","Data"):
                v=node.get(k)
                if isinstance(v,(dict,list)):visit(v,level+1)
        elif isinstance(node,list):
            for x in node:visit(x,level+1)
    visit(spawner)
    return entities

def summarize_entity(entity):
    if not isinstance(entity,dict):return None
    mob=entity.get("id")
    if not isinstance(mob,str):return None
    markers={k:normalize(entity[k]) for k in SIGNAL_FIELDS if k in entity}
    mounts=[]
    for p in entity.get("Passengers",[]) if isinstance(entity.get("Passengers"),list) else []:
        if isinstance(p,dict) and isinstance(p.get("id"),str):
            mounts.append({"id":p["id"],"markers":{k:normalize(p[k]) for k in SIGNAL_FIELDS if k in p}})
    return {"entity_id":mob,"unusual_entity_markers":markers,
            "passengers":mounts}

def summarize_nbt(root,path):
    palette=root.get("palette",[])
    if not palette and root.get("palettes"):palette=root["palettes"][0]
    if not isinstance(palette,list):palette=[]
    flags=[];counts=Counter()
    for b in root.get("blocks",[]) if isinstance(root.get("blocks"),list) else []:
        if not isinstance(b,dict):continue
        n=b.get("state")
        if not isinstance(n,int) or not 0<=n<len(palette):continue
        state=palette[n]
        block=state.get("Name","") if isinstance(state,dict) else ""
        if block not in SPECIAL_BLOCKS:continue
        counts[block]+=1
        record={"source_file":path,"block":block,"block_position":b.get("pos",[])}
        data=b.get("nbt",{}) if isinstance(b.get("nbt"),dict) else {}
        if block in ("minecraft:spawner","minecraft:trial_spawner"):
            record["spawn_entities"]=[x for x in (summarize_entity(e) for e in entity_payloads(data)) if x]
            record["block_entity_extra"]={k:normalize(data[k]) for k in SIGNAL_FIELDS if k in data}
        else:
            record["block_entity_extra"]={k:normalize(data[k]) for k in SIGNAL_FIELDS if k in data}
            if "Command" in data:record["command_sample"]=str(data["Command"])[:350]
            if block=="minecraft:jigsaw" and isinstance(data.get("pool"),str):
                record["jigsaw_pool_reference"]=data["pool"]
        if record.get("spawn_entities") or record.get("block_entity_extra") or record.get("command_sample") or record.get("jigsaw_pool_reference"):
            flags.append(record)
    for e in root.get("entities",[]) if isinstance(root.get("entities"),list) else []:
        if not isinstance(e,dict):continue
        summary=summarize_entity(e.get("nbt",{}))
        if summary:flags.append({"source_file":path,"block":"ENTITY",
                                 "entity_record":summary})
    return counts,flags

def audit(jar):
    digest=sha1(jar)
    if digest!=PINNED_SHA1:
        raise RuntimeError("Wrong WDA JAR SHA-1: "+digest)
    report={"scope":"PINNED_PR50_SOURCE_ONLY_NOT_RUNTIME_BOSS_ID_CONFIRMATION",
            "native_sha1":digest,"providers_scanned":["dungeons_arise"],
            "structures":{},"no_gameplay_files_edited":True,
            "native_boss_identified":False,
            "native_boss_identity_status":"UNVERIFIED__SOURCE_SCAN_ONLY"}
    with zipfile.ZipFile(jar) as z:
        names=set(z.namelist())
        all_json={k:json.loads(z.read(k)) for k in sorted(names) if
                  k.startswith("data/dungeons_arise/worldgen/template_pool/")
                  and k.endswith(".json")}
        for label in SECTIONS:
            section_path=f"/structure/{label}/"
            candidates=sorted(n for n in names if n.startswith("data/dungeons_arise/")
                              and n.endswith(".nbt") and section_path in n)
            source_counts=Counter();signals=[];failure=[];interesting_paths=[]
            jigsaw_missing_native=[]
            named_spawner_entities=[];named_prebuilt_entities=[]
            native_pool_files={n for n in names if
                n.startswith("data/dungeons_arise/worldgen/template_pool/")
                and n.endswith(".json")}
            for name in candidates:
                try:
                    # These subtrees have been observed to fit the existing
                    # bounded source scanner; use selective mode on overflow.
                    try:root=nbt_from_bytes(z.read(name))
                    except ValueError as exc:
                        if "limit exceeded" in str(exc):
                            root,_meta=extract_selected(z,name)
                        else:raise
                    counts,flags=summarize_nbt(root,name)
                    source_counts.update(counts)
                    for f in flags:
                        ent=f.get("entity_record")
                        spawn=f.get("spawn_entities",[])
                        for entity in spawn:
                            if entity["unusual_entity_markers"].get("CustomName") or entity["unusual_entity_markers"].get("custom_name"):
                                named_spawner_entities.append({"source_file":name,**entity})
                        if ent and (ent["unusual_entity_markers"].get("CustomName") or ent["unusual_entity_markers"].get("custom_name")):
                            named_prebuilt_entities.append({"source_file":name,**ent})
                        reference=f.get("jigsaw_pool_reference")
                        if reference and reference!="minecraft:empty":
                            pool_ref=loc_to_resource("dungeons_arise",reference,"worldgen/template_pool")
                            if pool_ref and pool_ref+".json" not in native_pool_files:
                                jigsaw_missing_native.append({
                                    "source_file":name,"jigsaw_pool_reference":reference,
                                    "status":"MISSING_NATIVE_POOL_OR_EXTERNAL_DATAPACK",
                                    "suggestions":nearby_native_resources(names,"dungeons_arise",reference,"pool")
                                })
                        named=bool(ent and ent["unusual_entity_markers"]) or any(
                            x["unusual_entity_markers"] for x in spawn)
                        if named or f.get("command_sample"):
                            signals.append(f)
                        elif f.get("block") in ("minecraft:spawner","minecraft:trial_spawner"):
                            if f.get("spawn_entities"):
                                interesting_paths.append({
                                  "source_file":name,
                                  "entity_ids":sorted({e["entity_id"] for e in spawn}),
                                  "passengers":sorted({p["id"] for e in spawn for p in e["passengers"]})
                                })
                except (ValueError,KeyError,IndexError,RecursionError,EOFError) as exc:
                    failure.append({"source_file":name,"error":str(exc)[:300]})
            # Native pools only: missing refs might be shipped in a different
            # datapack, supplied by another mod, or simply a typo.
            resource_refs=[]
            for file,body in all_json.items():
                if label not in file:continue
                values=pool_elements(body)
                for v in values:
                    expected=loc_to_resource("dungeons_arise",v,"structure")+".nbt"
                    if expected not in names and expected.replace("/structure/","/structures/") not in names:
                        resource_refs.append({
                            "source_pool":file,"reference":v,
                            "status":"MISSING_FROM_PINNED_NATIVE_JAR",
                            "suggestions":nearby_native_resources(names,"dungeons_arise",v,"template")
                        })
                fallback=body.get("fallback")
                if fallback and fallback!="minecraft:empty":
                    expected=loc_to_resource("dungeons_arise",fallback,"worldgen/template_pool")+".json"
                    if expected not in names:
                        resource_refs.append({
                            "source_pool":file,"reference":fallback,"status":"MISSING_FALLBACK_POOL_FROM_PINNED_NATIVE_JAR",
                            "suggestions":nearby_native_resources(names,"dungeons_arise",fallback,"pool")
                        })
            native_related_paths=sorted(n for n in names if any(
                x in n.lower() for x in (label+"/",label+"_","boss", "bosses"))
                and n.startswith("data/dungeons_arise/"))
            boss_like=[r for r in signals if any(
                marker in json.dumps(r,sort_keys=True).lower()
                for marker in ("boss","guardian","captain","customname","health","attributes"))]
            report["structures"][label]={
                "native_nbt_files_checked":len(candidates),
                "native_spawner_and_special_block_counts":dict(source_counts),
                "named_or_attribute_or_command_signals":signals[:100],
                "explicit_custom_name_spawner_entities":named_spawner_entities[:60],
                "explicit_custom_name_prebuilt_entities":named_prebuilt_entities[:60],
                "explicit_custom_name_spawner_count":len(named_spawner_entities),
                "explicit_custom_name_prebuilt_count":len(named_prebuilt_entities),
                "jigsaw_block_pools_missing_from_native_jar":jigsaw_missing_native[:40],
                "jigsaw_pool_refs_truncated":len(jigsaw_missing_native)>40,
                "boss_like_signals":boss_like[:60],
                "signals_truncated":len(signals)>100 or len(boss_like)>60,
                "spawner_id_paths_without_special_fields":interesting_paths[:60],
                "nbt_parse_failures":failure[:35],
                "pool_resource_references_missing_in_native_jar":resource_refs[:75],
                "missing_resource_references_truncated":len(resource_refs)>75,
                "native_related_asset_paths":native_related_paths[:150],
                "native_asset_path_list_truncated":len(native_related_paths)>150,
                "source_packed_NBT_does_not_prove_actual_boss_runtime":True,
                "all_native_source_references_are_not_a_complete_effective_Paxi_registry":True,
            }
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    result=audit(args.jar)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for name,row in result["structures"].items():
        print("STRUCTURE",name,
              "nbt",row["native_nbt_files_checked"],
              "spawners",row["native_spawner_and_special_block_counts"],
              "named-signals",len(row["named_or_attribute_or_command_signals"]),
              "explicit-named-spawner-entities",row["explicit_custom_name_spawner_count"],
              "explicit-named-prebuilt",row["explicit_custom_name_prebuilt_count"],
              "jigsaw-missing-native-pools",len(row["jigsaw_block_pools_missing_from_native_jar"]),
              "boss-like",len(row["boss_like_signals"]),
              "missing-native-refs",len(row["pool_resource_references_missing_in_native_jar"]),
              "parser-errors",len(row["nbt_parse_failures"]))
        for named in row["explicit_custom_name_spawner_entities"][:15]:
            print("EXPLICIT NAMED SPAWNER",name,json.dumps(named,sort_keys=True)[:1300])
        for missing in row["jigsaw_block_pools_missing_from_native_jar"][:8]:
            print("JIGSAW MISSING NATIVE POOL",name,json.dumps(missing,sort_keys=True)[:900])
        for signal in row["boss_like_signals"][:10]:
            print("BOSS-LIKE SIGNAL",name,json.dumps(signal,sort_keys=True)[:950])
        for item in row["pool_resource_references_missing_in_native_jar"][:8]:
            print("MISSING NATIVE REF",name,json.dumps(item,sort_keys=True)[:800])
    print("SOURCE ONLY; boss identity not runtime verified")
    print("REPORT:",args.out)

if __name__=="__main__":
    main()
