#!/usr/bin/env python3
"""Source-backed Dungeons & Taverns v4.4.4 curated structure biome vetoes.

Built against the exact installed-era NeoForge version from NovaWostra on Modrinth.
Only structure biome selector is changed. Native sets, weights, terrain adaptation,
loot, large castles, Nether and End are retained byte-exact by the mod itself.
Do NOT use arbitrary empty structure-set JSON: it can fail codec validation.
"""
import argparse
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "release_030/overrides/config/paxi/datapacks/ao_dnt_trek_curation"
DATA = PACK / "data/nova_structures/worldgen/structure"
TAG = PACK / "data/ambient_odyssey/tags/worldgen/biome/dnt_trek_disabled.json"
REPORT = ROOT / "docs/audits/DNT_TREK_CURATION_NATIVE_AUDIT.json"
NATIVE_URL = "https://api.modrinth.com/v2/version/BYUUUeZA"  # exact 1.21.1 NeoForge v4.4.4
NATIVE_PREFIX = "data/nova_structures/worldgen/structure/"
KEEP_SPECIAL = {
    "end_castle", "end_lighthouse", "end_ship", "nether_keep", "nether_port",
    "lone_citadel", "illager_manor", "illager_hideout", "remnant_taiga_castle",
    "witch_villa", "stray_fort", "toxic_lair", "undead_crypt",
    "trident_trial_monument", "shrine_tower", "piglin_donjon",
}
EXCLUDE_EXACT = {"ruin_town", "wild_ruin", "jungle_ruins", "desert_ruins"}
PACK_META = {
    "pack": {
        "pack_format": 48,
        "description": "Ambient Odyssey: trim Dungeons & Taverns settlement/ruin clutter for Trek without altering native big, Nether or End structures",
    }
}
DISABLED_TAG = {"replace": False, "values": []}

def classify(name):
    if name in KEEP_SPECIAL or name.startswith(("end_", "nether_", "piglin_", "skeleton_camp_")):
        return "keep"
    if name.startswith("remnant_"):
        return "remove_remnant"
    if name.startswith("village_"):
        return "remove_village"
    if name in EXCLUDE_EXACT:
        return "remove_routine_ruin"
    return "keep"

def get_native():
    req = urllib.request.Request(NATIVE_URL, headers={"User-Agent":"AmbientOdyssey-SourceAuditor/1.0"})
    with urllib.request.urlopen(req,timeout=45) as f:
        metadata = json.load(f)
    assert metadata["id"] == "BYUUUeZA"
    assert "neoforge" in {x.lower() for x in metadata["loaders"]}, metadata["loaders"]
    assert "1.21.1" in metadata["game_versions"]
    candidates = [file for file in metadata["files"] if file.get("primary", False)]
    assert len(candidates)==1, "Expected one audited native primary jar"
    item = candidates[0]
    assert "v4.4.4" in item["filename"]
    assert item["url"].startswith("https://cdn.modrinth.com/data/")
    req2 = urllib.request.Request(item["url"],headers={"User-Agent":"AmbientOdyssey-SourceAuditor/1.0"})
    with urllib.request.urlopen(req2,timeout=80) as f:
        raw=f.read(35_000_000)
    assert len(raw)<35_000_000, "Unexpected or truncated native jar"
    actual=hashlib.sha512(raw).hexdigest()
    assert actual==item["hashes"]["sha512"], "Native jar SHA512 mismatch"
    return raw, {"modrinth_version":"BYUUUeZA","filename":item["filename"],"sha512":actual,"sha1":hashlib.sha1(raw).hexdigest(),"bytes":len(raw)}

def render(blob, metadata):
    result={}
    seen={}
    with zipfile.ZipFile(io.BytesIO(blob)) as jar:
        for name in sorted(x for x in jar.namelist() if x.startswith(NATIVE_PREFIX) and x.endswith(".json")):
            slug=Path(name).stem
            kind=classify(slug)
            seen[slug]=kind
            if kind=="keep":
                continue
            native=json.loads(jar.read(name))
            assert isinstance(native,dict) and "biomes" in native, name
            updated=dict(native)
            updated["biomes"]="#ambient_odyssey:dnt_trek_disabled"
            assert {k:v for k,v in updated.items() if k!="biomes"} == {k:v for k,v in native.items() if k!="biomes"}
            output=DATA/(slug+".json")
            result[str(output.relative_to(ROOT))]=json.dumps(updated,indent=2,ensure_ascii=False)+"\n"
    assert len(seen)>=90, ("Inadequate native DnT 1.21.1 registry coverage",len(seen))
    for name in KEEP_SPECIAL:
        assert name in seen and seen[name]=="keep",name
    assert sum(x!="keep" for x in seen.values()) >= 26, "Selection unexpectedly empty"
    assert sum(x!="keep" for x in seen.values()) <= 55, "Overbroad selection"
    result[str(PACK.joinpath("pack.mcmeta").relative_to(ROOT))]=json.dumps(PACK_META,indent=2)+"\n"
    result[str(TAG.relative_to(ROOT))]=json.dumps(DISABLED_TAG,indent=2)+"\n"
    report={"schema":"ao_dnt_trek_curation_native_v1","native":metadata,
        "rule":"Disable remnant structures except taiga castle, all DnT village replacements, and ordinary overworld ruins; preserve other DnT structures, sets, spawn weights and Nether/End.",
        "catalogue_structure_count":len(seen),
        "disabled":{k:v for k,v in sorted(seen.items()) if v!="keep"},
        "retained":sorted(k for k,v in seen.items() if v=="keep"),
        "override_file_count":len(result),
        "minecraft_runtime_verified":False}
    result[str(REPORT.relative_to(ROOT))]=json.dumps(report,indent=2)+"\n"
    return result

def run(check=False):
    blob,md=get_native()
    contents=render(blob,md)
    if check:
        for path,text in contents.items():
            p=ROOT/path
            assert p.exists(), ("Missing native-sourced override",path)
            assert p.read_text(encoding="utf-8")==text, ("Stale native-sourced override",path)
        actual={x.relative_to(ROOT).as_posix() for x in DATA.glob("*.json")}
        expected={p for p in contents if p.startswith(DATA.relative_to(ROOT).as_posix()+"/")}
        assert actual==expected, ("Stale DnT patch files",sorted(actual^expected))
        print("PASS_SOURCE_EXACT_DNT_CURATION count=",len(contents),"native=",md["sha512"])
    else:
        for path,contents_text in contents.items():
            p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(contents_text,encoding="utf-8")
        print("GENERATED_SOURCE_EXACT_DNT_CURATION",len(contents),"native=",md["sha512"])

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    run(check=args.check)
