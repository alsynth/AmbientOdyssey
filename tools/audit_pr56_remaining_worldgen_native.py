"""Fail-closed read-only PR56 three-provider native-structure worldgen audit.

Only JARs exactly SHA1-matching the PR50 338-mod manifest pins are accepted.
Native JSON structure and set documents are captured with provenance.
Not an in-game placement test; tags from base Minecraft and other mods
may change the effective loaded biome membership.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

PINS = {
    "adventuredungeons": {
        "name": "adventuredungeons-neoforge-1.21-1.3.1.jar",
        "projectID": 1111930, "fileID": 5808396,
        "sha1": "706092299886721473b0ef7d5e4f7aa2a073c8de",
        "targets": ("adventuredungeons:underground_camp",),
        "special_resource_terms": ("pillager_outpost", "underground_camp"),
    },
    "lukis": {
        "name": "lukis-grand-capitals-1.1.3.jar",
        "projectID": 1003666, "fileID": 7456302,
        "sha1": "a07986ac59268f1343737b81acd24ad34e5371ca",
        "targets": ("minecraft:village_plains", "minecraft:village_snowy"),
        "special_resource_terms": ("village_plains", "village_snowy", "villages"),
    },
    "pasterdream": {
        "name": "pasterdream-0.9.6.jar",
        "projectID": 1575033, "fileID": 8639119,
        "sha1": "d5d95c8a049d868a844132ac1e47261eff0067f8",
        "targets": ("pasterdream:fourleaf_clover_plant",
                    "pasterdream:picnic_basket_structure"),
        "special_resource_terms": ("fourleaf_clover", "picnic_basket"),
    },
}
ROSTER = Path("docs/audits/CURRENT_BIOME_ROSTER.json")

def digest(p):
    h = hashlib.sha1()
    with p.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def as_id(filename,kind):
    pieces=filename.split("/")
    return pieces[1]+":"+filename.split("/"+kind+"/",1)[1].rsplit(".",1)[0]

def maybe_json(zf,p):
    with zf.open(p) as stream:
        return json.load(stream)

def target_matches(value,names):
    if isinstance(value,dict):
        return any(target_matches(v,names) for v in value.values())
    if isinstance(value,list):
        return any(target_matches(x,names) for x in value)
    return any(x in str(value) for x in names)

def inspect(label,jar,curated):
    pin=PINS[label]
    sha=digest(jar)
    if sha!=pin["sha1"]:
        raise RuntimeError("Wrong native archive for "+label+": "+sha)
    struct_count=0;set_count=0;tag_count=0;other_source=0
    structures={}; sets={}; tags={};interesting={}; invalid={}
    with zipfile.ZipFile(jar) as zf:
        for src in zf.namelist():
            if not src.endswith(".json") or not src.startswith("data/"):
                continue
            if "/worldgen/structure/" in src:
                cat="structure"
                struct_count+=1
            elif "/worldgen/structure_set/" in src:
                cat="structure_set"
                set_count+=1
            elif "/tags/worldgen/biome/" in src:
                cat="biome_tag"
                tag_count+=1
            elif "/dimension/" in src or "/dimension_type/" in src or "/worldgen/biome/" in src:
                cat="dimension_or_biome"
                other_source+=1
            else:
                continue
            try:
                obj=maybe_json(zf,src)
            except (ValueError,UnicodeError) as exc:
                invalid[src]=str(exc)
                continue
            if cat=="structure":
                key=as_id(src,"structure")
                if key in pin["targets"] or target_matches(obj.get("biomes"),pin["special_resource_terms"]):
                    structures[key]={"source":src,"source_content":obj}
            elif cat=="structure_set":
                key=as_id(src,"structure_set")
                members=obj.get("structures",[])
                if (target_matches(members,pin["targets"]) or
                    target_matches(members,pin["special_resource_terms"]) or
                    target_matches(src,pin["special_resource_terms"])):
                    sets[key]={"source":src,"source_content":obj}
            elif cat=="biome_tag":
                key=as_id(src,"biome")
                if (target_matches(key,pin["special_resource_terms"]) or
                    target_matches(obj,pin["special_resource_terms"])):
                    tags[key]={"source":src,"source_content":obj}
            else:
                if target_matches(src,pin["special_resource_terms"]):
                    interesting[src]=obj
        # Also report all exact structure definitions, even if the JSON source
        # has no matching selector at all, without claiming runtime registration.
        for target in pin["targets"]:
            if target in structures:continue
            p="data/"+target.split(":")[0]+"/worldgen/structure/"+target.split(":")[1]+".json"
            if p in zf.namelist():
                structures[target]={"source":p,"source_content":maybe_json(zf,p)}
    return {
        "verified_sha1":sha,
        "pin":pin,
        "native_counts":{"structures":struct_count,"sets":set_count,"biome_tags":tag_count,
                         "dimension_or_biome_assets":other_source},
        "selected_structures":structures,
        "selected_sets":sets,
        "selected_biome_tags":tags,
        "selected_dimension_or_biome_assets":interesting,
        "invalid_native_json":invalid,
        "target_ids_missing_exact_native_structure_json":[k for k in pin["targets"] if k not in structures],
        "curated_modded_biome_count":len(curated),
        "actual_game_runtime_tested":False,
        "effective_external_tag_resolution_tested":False,
        "no_worldgen_files_changed":True,
    }

def main():
    parser=argparse.ArgumentParser()
    for label in PINS:
        parser.add_argument("--"+label,required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    roster=json.loads(ROSTER.read_text(encoding="utf-8"))
    curated={k+":"+v for k,vs in roster.items() for v in vs}
    out={label:inspect(label,getattr(args,label),curated) for label in PINS}
    result={"method":"PR50_SHA1_PINNED_NATIVE_JARS_ONLY; NO_RUNTIME_TEST",
            "providers":out,"curated_biomes":sorted(curated)}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for label,entry in out.items():
        print(label,"native_sha1",entry["verified_sha1"],
              "structure_matches",list(entry["selected_structures"]),
              "sets",list(entry["selected_sets"]),
              "tags",list(entry["selected_biome_tags"]),
              "missing_exact_source",entry["target_ids_missing_exact_native_structure_json"])
    print("REPORT:",args.out)

if __name__=="__main__":
    main()
