"""Build a reproducible, TEST-ONLY Minecraft 1.21.1 Paxi datapack ZIP.

FAIL CLOSED unless:
- all four structure definitions exactly match a pinned v4.4.4 native-JAR
  evidence snapshot, differing ONLY in 'biomes',
- private tags retain original selectors and use only AO curated biome IDs,
- no extra files enter the distributable ZIP,
- an independent PR50-vs-PR56 Paxi source audit reports zero gating issues.

This does not install files into any release, world or Paxi directory and
does not certify live resource precedence or natural generation.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"experiments/structure-biome-compatibility/firewatch-structure-only-draft"
EVIDENCE=ROOT/"docs/balance/DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json"
CURATED=ROOT/"docs/audits/CURRENT_BIOME_ROSTER.json"
SUFFIXES=("birch","cherry","forest","savanna")
EXPECTED_JAR_SHA1="249a5bdd0e8622b8a11f88758e6f5fd5fda036a3"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect(source_audit):
    audit=json.loads(source_audit.read_text(encoding="utf-8"))
    if audit.get("detected_gates") or not audit.get("source_changes_safe_to_apply"):
        raise ValueError("Paxi source audit is not clean; refuse candidate packaging")
    if audit.get("source_pr50_branch_compared") is not True:
        raise ValueError("Exact PR50 source comparison missing")
    cmp=audit.get("comparison") or {}
    if cmp.get("target_resource_differences"):
        raise ValueError("PR50 versus PR56 target Paxi resources differ; refuse package")
    if audit.get("current",{}).get("target_resources"):
        raise ValueError("Preexisting Paxi overrides detected for targeted structure/collections")

    provenance=json.loads(EVIDENCE.read_text(encoding="utf-8"))
    if provenance.get("sha1")!=EXPECTED_JAR_SHA1 or provenance.get("native_structure_json_count")!=96:
        raise ValueError("Pinned source provenance corrupted")
    roster=json.loads(CURATED.read_text(encoding="utf-8"))
    available={namespace+":"+n for namespace,values in roster.items() for n in values}
    data={}
    mcmeta=INPUT/"pack.mcmeta"
    config=json.loads(mcmeta.read_text(encoding="utf-8"))
    if config["pack"]["pack_format"]!=48 or "DRAFT" not in config["pack"]["description"]:
        raise ValueError("Wrong Minecraft 1.21.1 datapack format or missing test warning")
    data["pack.mcmeta"]=mcmeta.read_bytes()
    native=provenance["four_original_native_structure_json"]
    for name in SUFFIXES:
        orig=native[name]
        rel=f"data/nova_structures/worldgen/structure/firewatch_tower_{name}.json"
        src=INPUT/rel
        obj=json.loads(src.read_text(encoding="utf-8"))
        expected=dict(orig,biomes=f"#ambient_odyssey:firewatch_compatible/{name}")
        if obj!=expected:
            raise ValueError(f"Unsafe fields changed for {name}: native JAR comparison failed")
        data[rel]=src.read_bytes()

        rel=f"data/ambient_odyssey/tags/worldgen/biome/firewatch_compatible/{name}.json"
        src=INPUT/rel
        tag=json.loads(src.read_text(encoding="utf-8"))
        previous=orig["biomes"]
        if isinstance(previous,list):
            if len(previous)!=1:
                raise ValueError("Multi-biome source anchor needs a manual review: "+name)
            previous=previous[0]
        values=tag["values"]
        if tag.get("replace",False) or values[0]!=previous:
            raise ValueError("Lost original source biome eligibility: "+name)
        if len(values)!=len(set(values)) or not values[1:] or not set(values[1:]).issubset(available):
            raise ValueError("Uncurated, empty, or duplicate candidate biome IDs: "+name)
        data[rel]=src.read_bytes()

    if len(data)!=9 or any("/worldgen/structure_set/" in x for x in data):
        raise ValueError("Unexpected ZIP member set")
    return data,provenance,audit

def build(out,manifest_out,source_audit):
    files,source,audit=inspect(source_audit)
    out.parent.mkdir(parents=True,exist_ok=True)
    manifest_out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for filename,blob in sorted(files.items()):
            info=zipfile.ZipInfo(filename,date_time=(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            archive.writestr(info,blob,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(out) as verify:
        if verify.testzip() is not None or set(verify.namelist())!=set(files):
            raise ValueError("ZIP CRC or member validation failed")
        if any(verify.read(p)!=b for p,b in files.items()):
            raise ValueError("ZIP member bytes differ from audited source")
    report={
        "purpose":"ISOLATED_DISPOSABLE_WORLD_TEST_ONLY",
        "active_modpack_or_Paxi_changed":False,
        "live_natural_generation_verified":False,
        "live_Paxi_resource_precedence_verified":False,
        "requires_real_Minecraft_and_multiplayer_acceptance":True,
        "native_DNT_pinned_jar_sha1":source["sha1"],
        "curseforge_project_id":source["curseforge_project_id"],
        "curseforge_file_id":source["curseforge_file_id"],
        "repo_Paxi_PR50_vs_PR56_source_comparison_passed":True,
        "zip_name":out.name,
        "zip_sha256":sha(out.read_bytes()),
        "files":{n:sha(blob) for n,blob in sorted(files.items())},
        "notes":"Standalone datapack, not a CurseForge modpack import. Not installed into release.",
    }
    manifest_out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--paxi-report",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    args=p.parse_args()
    report=build(args.out,args.manifest,args.paxi_report)
    print("ZIP:",args.out.as_posix())
    print("SHA256:",report["zip_sha256"])
    print("Validated members:",len(report["files"]))
    print("MANIFEST:",args.manifest.as_posix())
    print("NO LIVE PROFILE CHANGED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
