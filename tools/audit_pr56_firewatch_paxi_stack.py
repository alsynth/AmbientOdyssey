"""PR56 research-only Paxi structure resource precedence and pack-discovery audit.

Audits all unpacked Paxi datapack roots and (optionally) the exact PR50 branch's
historical repo snapshot. Does not assert the repo snapshot is a materialized
full-import ZIP or a live Minecraft server. Does not edit source files.

python tools/audit_pr56_firewatch_paxi_stack.py \
    --current release_030/overrides/config/paxi/datapacks \
    --reference /tmp/pr50-paxi \
    --out /tmp/pr56-paxi-stack.json
"""
import argparse
import hashlib
import json
from pathlib import Path

STRUCTURES = ("birch", "cherry", "forest", "savanna")
DNT_COLLECTIONS = ("birch_forests", "cherry_forests", "savannas")
TOWER_SET = "data/nova_structures/worldgen/structure_set/firewatch_towers.json"
PAXI_PREFIX = Path("release_030/overrides/config/paxi/datapacks")
CURATION_PREFIX = "data/nova_structures/worldgen/structure/"
KNOWN_INTENTIONAL_EXCLUSIONS = ("village_jungle.json", "remnant_birch_graveyard.json")
EXACT_KEYS = {
    *(f"data/nova_structures/worldgen/structure/firewatch_tower_{v}.json" for v in STRUCTURES),
    *(f"data/nova_structures/tags/worldgen/biome/collections/{v}.json" for v in DNT_COLLECTIONS),
    *(f"data/ambient_odyssey/tags/worldgen/biome/firewatch_compatible/{v}.json" for v in STRUCTURES),
    TOWER_SET,
}
SOURCE_PACK_NAMES = {
    "ambient_odyssey", "ao_biome_replacement", "ao_compatibility",
    "ao_content_overrides", "ao_dnt_trek_curation", "ao_dragon_caves",
    "ao_flight_balance", "ao_lukis_mansion_native_pool", "ao_server_rules",
    "ao_structure_density", "ao_structure_repairs", "ao_technical_fixes",
    "ao_v041_runtime_fixes", "ao_worldgen_final_fixes",
}

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def inventory(root):
    if not root.is_dir():
        raise FileNotFoundError("Missing Paxi root: " + str(root))
    result={"root_label":str(root), "datapack_directories":[], "target_resources":{},
            "intentional_dnt_exclusions":[], "archive_packs":[], "broken_json":[],
            "all_data_files_scanned":0, "all_datapack_mcmeta":{}}
    for pack in sorted(root.iterdir()):
        if pack.is_file() and pack.suffix.lower() in (".zip", ".jar"):
            result["archive_packs"].append(pack.name)
            continue
        if not pack.is_dir():
            continue
        result["datapack_directories"].append(pack.name)
        if (pack/"pack.mcmeta").exists():
            result["all_datapack_mcmeta"][pack.name]=read_json(pack/"pack.mcmeta")
        for path in pack.rglob("*"):
            if not path.is_file() or not path.as_posix().lower().endswith(".json"):
                continue
            rel=path.relative_to(pack).as_posix()
            result["all_data_files_scanned"]+=1
            if rel in EXACT_KEYS:
                try:
                    obj=read_json(path)
                    item={"pack":pack.name,"sha256":sha256(path),"relative_path":rel}
                    if rel.startswith("data/nova_structures/worldgen/structure/"):
                        item["biomes"]=obj.get("biomes")
                        item["type"]=obj.get("type")
                        item["start_pool"]=obj.get("start_pool")
                    elif "/tags/" in rel:
                        item["values"]=obj.get("values")
                        item["replace"]=obj.get("replace",False)
                    result["target_resources"].setdefault(rel,[]).append(item)
                except (ValueError,UnicodeError) as err:
                    result["broken_json"].append([pack.name,rel,str(err)])
            if (pack.name=="ao_dnt_trek_curation" and
                rel.startswith(CURATION_PREFIX) and
                rel[len(CURATION_PREFIX):] in KNOWN_INTENTIONAL_EXCLUSIONS):
                try:
                    j=read_json(path)
                    result["intentional_dnt_exclusions"].append({
                        "id":"nova_structures:"+path.stem,
                        "selector":j.get("biomes"),
                        "sha256":sha256(path)
                    })
                except (ValueError,UnicodeError) as err:
                    result["broken_json"].append([pack.name,rel,str(err)])
    return result

def compare(cur,ref):
    diffs=[]
    names=sorted(set(cur["target_resources"])|set(ref["target_resources"]))
    for name in names:
        curv=[(x["pack"],x["sha256"]) for x in cur["target_resources"].get(name,[])]
        refv=[(x["pack"],x["sha256"]) for x in ref["target_resources"].get(name,[])]
        if curv!=refv:
            diffs.append({"resource":name,"current":curv,"reference":refv})
    curpacks=set(cur["datapack_directories"])
    refpacks=set(ref["datapack_directories"])
    return {"target_resource_differences":diffs,
            "new_datapack_directories":sorted(curpacks-refpacks),
            "missing_datapack_directories":sorted(refpacks-curpacks)}

def audit(current,reference=None):
    cur=inventory(current)
    ref=inventory(reference) if reference else None
    target_collisions={k:v for k,v in cur["target_resources"].items() if len(v)>1}
    cur_intrusions={k:v for k,v in cur["target_resources"].items() if (
        k.startswith("data/ambient_odyssey/tags/worldgen/biome/firewatch_compatible/") or
        k.startswith("data/nova_structures/worldgen/structure/firewatch_tower_") or
        k.startswith("data/nova_structures/tags/worldgen/biome/collections/"))}
    issues=[]
    if cur["archive_packs"]:issues.append("UNEXPANDED_ARCHIVED_DATAPACKS_PRESENT")
    if cur["broken_json"]:issues.append("INVALID_TARGETED_SOURCE_JSON")
    if target_collisions:issues.append("EXISTING_TARGET_RESOURCE_COLLISIONS")
    if cur_intrusions:issues.append("CURRENT_PAXI_TOWER_OR_SHARED_TAG_OVERRIDE_ALREADY_PRESENT")
    missing_exclusions=sorted(set(KNOWN_INTENTIONAL_EXCLUSIONS)-
                              {x["id"].split(":")[-1]+".json" for x in cur["intentional_dnt_exclusions"]})
    if missing_exclusions:issues.append("CURATION_EXPECTED_EXCLUSIONS_MISSING")
    if ref:
        if ref["archive_packs"]:issues.append("REFERENCE_HAS_ARCHIVE_DATAPACKS")
        if ref["broken_json"]:issues.append("REFERENCE_HAS_INVALID_SOURCE_JSON")
    comparison=compare(cur,ref) if ref else None
    return {
        "scope":"REPOSITORY_SOURCE_ONLY__NOT_MATERIALIZED_FULL_IMPORT_OR_LIVE_PAXI",
        "source_pr50_branch_compared":ref is not None,
        "source_changes_safe_to_apply":not issues,
        "detected_gates":issues,
        "missing_expected_curation_files":missing_exclusions,
        "current":cur, "pr50_reference":ref, "comparison":comparison,
        "live_resource_winner_runtime_tested":False,
        "live_generation_runtime_tested":False,
        "active_modpack_changed":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--current",type=Path,default=PAXI_PREFIX)
    p.add_argument("--reference",type=Path)
    p.add_argument("--out",type=Path,required=True)
    opts=p.parse_args()
    report=audit(opts.current,opts.reference)
    opts.out.parent.mkdir(parents=True,exist_ok=True)
    opts.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("Current Paxi packs:",len(report["current"]["datapack_directories"]))
    print("Target resource collisions:",len([1 for x in report["current"]["target_resources"].values() if len(x)>1]))
    print("Current modified tower/collection selectors:",[x for x in report["current"]["target_resources"] if "firewatch" in x or "collections/" in x])
    print("Expected curation exclusions:",report["current"]["intentional_dnt_exclusions"])
    print("Source PR50 comparison:",report["comparison"])
    print("Gates:",report["detected_gates"])
    print("FULL REPORT:",opts.out.as_posix())
    return 1 if report["detected_gates"] else 0

if __name__=="__main__":
    raise SystemExit(main())
