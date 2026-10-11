#!/usr/bin/env python3
"""AO v0.4.1 private Trek/Common + Create/non-farming rarity experiment.

Exact SHA-pinned upstream 1.21.1 JAR registry JSON is the sole input. Generate
an isolated Paxi datapack without changing native biome eligibility, weights,
loot, template pools, structures, salt or boss logic.

NOT A RUNTIME TEST. Effect applies only to newly generated chunks and must be
A/B tested against the unmodified 329-ref engineering pack on equal seeds.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile
try:
    from tools.audit_v041_native_trek_create import ROOT,LOCK,download
except ModuleNotFoundError:
    from audit_v041_native_trek_create import ROOT,LOCK,download

PACK=ROOT/"release_030/overrides/config/paxi/datapacks/ao_v041_trek_create_rarity_test"
DATA=PACK/"data"
REPORT=ROOT/"build/v041_trek_create_rarity_report.json"
# Pinned exact source JARs: audited 2026-10-11 in CI 38138907870.
PINS={
    "trek-structure-expansion":"5ea0837a4b1ef02cc702d7e7e49a245f4857591696183b9d2fe56c574cbfc022",
    "test6-create-structures-arise":"a98c1853a4a3ab2b845f19617b8ed6aed682aa77e818c13bae4ab95ebff8bd6e",
    "test6-create-easy-structures":"8d5949114e9dd506c4a8598f789e63678fdf6b2b90f40a8e6ef2babc6f56029f",
}
# Trek "very_common" stays unchanged to avoid overloading small ruins.
# Its huge, very_rare sites and monster-room grids are unchanged.
TREK_OVERWORLD={
    "common":(24,21),
    "medium":(30,26),
    "rare":(48,44),
}
# Keep farming and food production sites, even if nominally "Create" structures.
CREATE_ARISE_FARM={"windmill","honey_pit","chocolate_pit"}
CREATE_EASY_FARM={"windmill"}
CREATE_RATIO=1.30  # 1/1.30^2 ~ 59.2% native random-spread grid density.
ROOT_KEYS={"structures","placement"}
MODS={
    "trek-structure-expansion":("data/trek/worldgen/structure_set/",None),
    "test6-create-structures-arise":("data/create_structures_arise/worldgen/structure_set/",CREATE_ARISE_FARM),
    "test6-create-easy-structures":("data/create_easy_structures/worldgen/structure_set/",CREATE_EASY_FARM),
}

def render(slug, blob):
    prefix,keep=MODS[slug]
    outputs={}
    audit=[]
    native_count=0
    with ZipFile(io.BytesIO(blob)) as z:
        for name in sorted(z.namelist()):
            if not name.startswith(prefix) or not name.endswith(".json"):continue
            native_count+=1
            native=json.loads(z.read(name))
            assert set(native)>=ROOT_KEYS, (slug,name)
            placement=native["placement"]
            if placement.get("type")!="minecraft:random_spread":continue
            spacing=placement.get("spacing")
            separation=placement.get("separation")
            assert isinstance(spacing,int) and isinstance(separation,int) and 0<=separation<spacing,(name,placement)
            stem=Path(name).stem
            if slug=="trek-structure-expansion":
                if name!=prefix+"overworld/"+stem+".json" or stem not in TREK_OVERWORLD:continue
                expected,new=TREK_OVERWORLD[stem]
                assert spacing==expected,(name,spacing,expected)
                # A common/medium boost shouldn't explode the number of small sites.
                assert len(native["structures"])>=10,(name,len(native["structures"]))
            else:
                # No farming windmills, food pits or unlisted rarer boss constraints touched.
                if stem in keep:continue
                new=max(spacing+1,round(spacing*CREATE_RATIO))
                assert new>spacing and separation<new
            patched=dict(native)
            patched["placement"]=dict(placement,spacing=new)
            assert patched["structures"]==native["structures"]
            assert {k:v for k,v in patched.items() if k!="placement"}=={k:v for k,v in native.items() if k!="placement"}
            assert {k:v for k,v in patched["placement"].items() if k!="spacing"}=={k:v for k,v in placement.items() if k!="spacing"}
            target=PACK/name
            encoded=(json.dumps(patched,indent=2,ensure_ascii=False)+"\n").encode()
            outputs[target]=encoded
            audit.append({
                "native":name,"original_spacing":spacing,"new_spacing":new,
                "separation":separation,"salt":placement.get("salt"),
                "structure_count":len(native["structures"]),
                "theoretical_grid_ratio":round((spacing/new)**2,3),
                "native_sha256":hashlib.sha256(z.read(name)).hexdigest(),
                "override_sha256":hashlib.sha256(encoded).hexdigest(),
            })
    return native_count,outputs,audit

def prepare(check=False):
    generated={}
    report={"name":"Trek/Create density experimental","runtime_verified":False,
            "claims":"candidate structure grid rates only; actual success also depends on biome and exclusion filters",
            "changes":{},"source_pins":{}}
    total=0
    for slug in MODS:
        item=LOCK["additions"][slug]
        raw=download(item)
        actual=hashlib.sha256(raw).hexdigest()
        assert actual==PINS[slug],(slug,actual)
        native_count,outputs,changes=render(slug,raw)
        if slug=="trek-structure-expansion":assert len(changes)==3,(slug,len(changes))
        if slug=="test6-create-structures-arise":assert len(changes)==25,(slug,len(changes))
        if slug=="test6-create-easy-structures":assert len(changes)==15,(slug,len(changes))
        total+=len(changes)
        generated.update(outputs)
        report["changes"][slug]={"native_structure_sets":native_count,"changed":changes}
        report["source_pins"][slug]={"projectID":item["projectId"],"fileID":item["id"],"sha256":actual}
        print("RARITY",slug,"native",native_count,"changed",len(changes))
    # 3 Trek + 25 Create Arise + 15 Create Easy sets; untouched other mods.
    assert total==43,total
    generated[PACK/"pack.mcmeta"]=(json.dumps({"pack":{"pack_format":48,
          "description":"AO private experiment: Trek common/medium/rare slightly more frequent; non-farming Create structures less frequent"}},indent=2)+"\n").encode()
    paths={p.relative_to(PACK).as_posix() for p in generated}
    assert len(paths)==44
    if check:
        actual={p.relative_to(PACK).as_posix() for p in PACK.rglob("*") if p.is_file()}
        assert actual==paths,(len(actual),len(paths),sorted(actual^paths)[:15])
        for p,expected in generated.items():
            assert p.read_bytes()==expected,("stale or edited rarity source",p)
    else:
        for p,data in generated.items():
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(data)
    report["total_changed_structure_sets"]=total
    report["untouched"]=["TREK End/Nether/monster rooms/very_common/very_rare",
                         "Create windmills, Create honey/chocolate food production pits",
                         "all native structure weights, biome tags, jigsaw pools, loot tables and salts",
                         "Farmers Structures (independent mod), Minecraft structures unrelated to Create/Trek"]
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print("PASS native-sourced candidate",total,"overrides","mode",("check" if check else "generate"))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    prepare(args.check)
