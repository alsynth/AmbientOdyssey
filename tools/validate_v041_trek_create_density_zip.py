#!/usr/bin/env python3
"""Fail-closed ZIP audit for the private 329-ref Trek/Create A/B variant."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

PACK="overrides/config/paxi/datapacks/ao_v041_trek_create_rarity_test/"
REPORT=Path("build/v041_trek_create_rarity_report.json")

def validate(path):
    report=json.loads(REPORT.read_text())
    assert report["total_changed_structure_sets"]==43
    all_mods=report["changes"]
    assert {mod:len(meta["changed"]) for mod,meta in all_mods.items()}=={
        "trek-structure-expansion":3,
        "test6-create-structures-arise":25,
        "test6-create-easy-structures":15}
    with ZipFile(path) as z:
        assert z.testzip() is None,"bad ZIP checksum"
        names=z.namelist()
        assert len(names)==len(set(names))
        manifest=json.loads(z.read("manifest.json"))
        assert manifest["version"]=="0.4.1-experimental-trek-manual-ack"
        assert len(manifest["files"])==329
        pins={x["projectID"]:x["fileID"] for x in manifest["files"]}
        for p in report["source_pins"].values():
            assert pins[p["projectID"]]==p["fileID"]
        expected=set()
        for name,meta in all_mods.items():
            for row in meta["changed"]:
                loc=PACK+row["native"]
                expected.add(loc)
                encoded=z.read(loc)
                assert hashlib.sha256(encoded).hexdigest()==row["override_sha256"],loc
                obj=json.loads(encoded)
                placement=obj["placement"]
                assert placement["spacing"]==row["new_spacing"]
                assert placement["separation"]==row["separation"]
                assert placement["salt"]==row["salt"]
                assert len(obj["structures"])==row["structure_count"]
                assert 0<=placement["separation"]<placement["spacing"]
                if name=="trek-structure-expansion":
                    assert placement["spacing"]<row["original_spacing"]
                else:
                    assert placement["spacing"]>row["original_spacing"]
        actual={p for p in names if p.startswith(PACK) and p.endswith(".json") and "/worldgen/structure_set/" in p}
        assert actual==expected,(len(actual),len(expected),sorted(actual^expected)[:10])
        assert json.loads(z.read(PACK+"pack.mcmeta"))["pack"]["pack_format"]==48

        import re
        chapters={
            "field_manual":15,
            "tips_and_tricks":9,
            "keybind_cheatsheet":8
        }
        ids=[]
        for chapter,count in chapters.items():
            path="overrides/config/ftbquests/quests/chapters/"+chapter+".snbt"
            text=z.read(path).decode()
            tasks=re.findall(r'tasks: \[\{ id: "([0-9A-F]{16})", type: "checkmark" \}\]',text)
            assert len(tasks)==count,(chapter,len(tasks),count)
            assert "tasks: [ ]" not in text
            ids.extend(tasks)
        assert len(ids)==len(set(ids))==32

        # Farms/food productions and special TREK types must not be overridden.
        assert not any(s.endswith(("/windmill.json","/honey_pit.json","/chocolate_pit.json"))
                       for s in actual)
        assert not any("/trek/worldgen/structure_set/"+frag in s for s in actual
                       for frag in ("end/","nether/","monster_room/","overworld/very_common","overworld/very_rare"))
        rustic="overrides/config/cristellib/create_rustic_structures/structure_placement_config.json5"
        cfg=z.read(rustic).decode()
        import re
        cfg=json.loads(re.sub(r'/\*.*?\*/|//[^\n]*','',cfg,flags=re.S))
        assert cfg["rustic_smithy"]["spacing"]==37 and cfg["rustic_smithy"]["separation"]==24
        assert cfg["rustic_well"]["spacing"]==27 and cfg["rustic_well"]["separation"]==17
        assert cfg["rustic_barn"]["spacing"]==36 and cfg["rustic_windmill"]["spacing"]==32
    print("PASS 329 locked mod refs, 32 deliberate Field Manual checkmarks, 3 TREK structure-set increases, 40 non-farming Create reductions, 2 Rustic reductions, zero farm/End/Nether/rarity boss rewrites")
    print("NOT RUNTIME TESTED — fresh disposable world A/B required; structure frequency not guaranteed by candidate grid spacing")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("archive",type=Path)
    validate(parser.parse_args().archive)
