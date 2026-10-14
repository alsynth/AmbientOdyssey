"""Read-only SHA-1-pinned native YUNG's Better Mineshafts biome eligibility probe.

Not a dynamic registry or natural-worldgen proof. Looks for native biome tags
and their nested references for seven *historically* zero-curated Overworld
mineshaft variants; does not stage any biome changes.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

EXPECTED_SHA1="6a14e1d8201f068ca87ef8333e471c5378955906"
EXPECTED_FILE="YungsBetterMineshafts-1.21.1-NeoForge-5.1.1.jar"
TARGETS=("bettermineshafts:mineshaft_oak",
         "bettermineshafts:mineshaft_spruce_snowy",
         "bettermineshafts:mineshaft_acacia",
         "bettermineshafts:mineshaft_desert",
         "bettermineshafts:mineshaft_mesa",
         "bettermineshafts:mineshaft_mushroom",
         "bettermineshafts:mineshaft_red_desert")
ROOT=Path(__file__).resolve().parents[1]

def digest(path):
    h=hashlib.sha1()
    with path.open("rb") as src:
        for block in iter(lambda:src.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def parse_json(z,n):
    with z.open(n) as f:return json.load(f)

def values(obj):
    val=obj.get("values",[])
    return [x if isinstance(x,str) else x.get("id","") for x in val
            if isinstance(x,(str,dict))]

def inspect(path):
    actual=digest(path)
    if actual!=EXPECTED_SHA1:raise RuntimeError("Unexpected native JAR SHA1 "+actual)
    roster=json.loads((ROOT/"docs/audits/CURRENT_BIOME_ROSTER.json").read_text(encoding="utf-8"))
    curated={ns+":"+s for ns,entries in roster.items() for s in entries}
    with zipfile.ZipFile(path) as z:
        allnames=z.namelist()
        tags={}
        for n in allnames:
            if n.startswith("data/") and "/tags/worldgen/biome/" in n and n.endswith(".json"):
                try:
                    obj=parse_json(z,n)
                    ref=n.split("/")[1]+":"+n.split("/tags/worldgen/biome/")[1][:-5]
                    tags[ref]={"source":n,"values":values(obj),"replace":obj.get("replace",False)}
                except (ValueError,KeyError) as e:
                    raise RuntimeError("Invalid native tag: "+n) from e
        defs={}
        for n in allnames:
            if n.startswith("data/") and "/worldgen/structure/" in n and n.endswith(".json"):
                j=parse_json(z,n)
                key=n.split("/")[1]+":"+n.split("/worldgen/structure/")[1][:-5]
                defs[key]={"source":n,"biomes":j.get("biomes"),"type":j.get("type")}
        sets={}
        for n in allnames:
            if n.startswith("data/") and "/worldgen/structure_set/" in n and n.endswith(".json"):
                j=parse_json(z,n)
                k=n.split("/")[1]+":"+n.split("/worldgen/structure_set/")[1][:-5]
                sets[k]=j

    out={}
    for id in TARGETS:
        d=defs.get(id)
        selected=d.get("biomes") if d else None
        targets=[selected] if isinstance(selected,str) else selected if isinstance(selected,list) else []
        direct_tags={}
        visited=set()
        stack=[x[1:] for x in targets if isinstance(x,str) and x.startswith("#")]
        while stack:
            tag=stack.pop()
            if tag in visited:continue
            visited.add(tag)
            row=tags.get(tag)
            if row:
                direct_tags[tag]=row
                for v in row["values"]:
                    if v.startswith("#"):stack.append(v[1:])
        resolved={v for row in direct_tags.values() for v in row["values"] if not v.startswith("#")}
        resolved.update(x for x in targets if not x.startswith("#"))
        out[id]={
            "native_structure_definition":d,
            "source_tag_keys_seen":sorted(visited),
            "resolved_in_jar_tag_entries":sorted(resolved),
            "native_direct_curated_overlap":sorted(resolved&curated),
            "unresolved_nested_native_tags":sorted(visited-set(direct_tags)),
            "native_set_memberships":[k for k,v in sets.items()
                if any(x.get("structure")==id for x in v.get("structures",[])
                       if isinstance(x,dict))],
            "minecraft_tag_sources_may_be_external":True,
            "AO_Paxi_effective_biome_tags_checked":False,
            "naturally_generated_in_current_profile":False,
        }
    return {
        "source":"SHA1_VERIFIED_PR50_CURSEFORGE_YUNGS_BETTER_MINESHAFTS",
        "curseforge_project_id":1015096,
        "curseforge_file_id":5812193,
        "sha1":actual,
        "native_biome_tag_count":len(tags),
        "native_structure_definition_count":len(defs),
        "native_structure_set_count":len(sets),
        "target_results":out,
        "full_native_tag_keys":sorted(tags),
        "no_worldgen_or_gameplay_files_changed":True,
        "natural_generation_verified":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--jar",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    output=inspect(args.jar)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("SOURCE JAR SHA1:",output["sha1"])
    print("NATIVE BIOME TAGS:",output["native_biome_tag_count"])
    for k,v in output["target_results"].items():
        print(k,"selector=",v["native_structure_definition"],
              "native overlaps=",v["native_direct_curated_overlap"],
              "unresolved native references=",v["unresolved_nested_native_tags"])
    print("EVIDENCE:",args.out.as_posix())

if __name__=="__main__":main()
