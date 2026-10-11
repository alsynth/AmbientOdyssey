#!/usr/bin/env python3
"""Translate exact Mine Cells 2.0.3 Fabric compatibility recipes to 1.21.1 NeoForge.

Only the 15 native recipe IDs currently disabled by ao_v041_runtime_fixes.
Original JSON is read from the pinned SHA256 JAR, not guessed or copied from
another release. Original items, chance values and item amounts are preserved.
The three absent Brewin' & Chewin' recipes and Patchouli guide remain disabled.
"""
from __future__ import annotations
import argparse, hashlib, io, json, copy
from pathlib import Path
from zipfile import ZipFile
try:
    from tools.audit_v042_native_recipes import source
except ModuleNotFoundError:
    from audit_v042_native_recipes import source

ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/"release_030/release-lock.json").read_text())
PIN=LOCK['additions']['content-040-minecells-minecells']
assert (PIN['projectId'],PIN['id'],PIN['sha256'])==(
  618790,7033510,"194b2318ec65896422f70bfc30983eb062c912c85295945c85599f64524e2481")
BASE=ROOT/'release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes/data/minecells/recipe'

def full_id(raw):
    assert isinstance(raw,str) and raw,raw
    return raw if ':' in raw else 'minecraft:'+raw

def convert(raw):
    native=copy.deepcopy(raw)
    expected_mod=('create' if native['type'].startswith('create:')
                  else 'farmersdelight' if native['type']=="farmersdelight:cutting"
                  else None)
    assert expected_mod in ('create','farmersdelight'),native.get('type')
    assert native.get('fabric:load_conditions')==[
      {"condition":"fabric:all_mods_loaded","values":[expected_mod]}]
    del native['fabric:load_conditions']
    native['neoforge:conditions']=[{"type":"neoforge:mod_loaded","modid":expected_mod}]
    if expected_mod=='create':
        if 'processingTime' in native:
            assert 'processing_time' not in native
            native['processing_time']=native.pop('processingTime')
        assert native['type'] in ('create:crushing','create:cutting','create:filling','create:haunting')
        for result in native['results']:
            assert 'item' in result and 'id' not in result
            result['id']=full_id(result.pop('item'))
        for ingredient in native['ingredients']:
            items=ingredient if isinstance(ingredient,list) else [ingredient]
            for element in items:
                if 'item' in element:
                    element['item']=full_id(element['item'])
                if 'fluid' in element:
                    assert native['type']=='create:filling'
                    assert element['amount']==81000,"Only known Fabric one-bucket recipe permitted"
                    element['type']='neoforge:single'
                    element['amount']=1000
        assert 'processingTime' not in native
    else:
        assert native['type']=='farmersdelight:cutting'
        assert native['tool']=={"type":"farmersdelight:tool","tag":"c:tools/axes"}
        native['tool']=[{"type":"farmersdelight:item_ability","action":"axe_strip"},
                        {"tag":"minecraft:axes"}]
        for ingredient in native['ingredients']:
            if 'item' in ingredient:ingredient['item']=full_id(ingredient['item'])
        native['result']=[
          {"item":{"id":full_id(item['item']),"count":item.get("count",1)},
           **({"chance":item['chance']} if "chance" in item else {})}
          for item in native['result']
        ]
        if isinstance(native.get('sound'),str):
            native['sound']={"sound_id":full_id(native['sound'])}
    return native

def validate(native,out):
    # Preserve author recipe outputs and random chance precisely.
    assert native['type']==out['type']
    assert len(native['ingredients'])==len(out['ingredients'])
    original_results=native['results'] if native['type'].startswith('create:') else native['result']
    migrated_results=out['results'] if native['type'].startswith('create:') else out['result']
    assert len(original_results)==len(migrated_results)
    for before,after in zip(original_results,migrated_results):
        if native['type'].startswith('create:'):
            assert full_id(before['item'])==after['id']
            assert before.get('count',1)==after.get('count',1)
            assert before.get('chance',1)==after.get('chance',1)
        else:
            assert full_id(before['item'])==after['item']['id']
            assert before.get('count',1)==after['item']['count']
            assert before.get('chance',1)==after.get('chance',1)
    assert 'fabric:load_conditions' not in out
    assert out['neoforge:conditions'][0]['type']=='neoforge:mod_loaded'
    assert all(':' in v['id'] for v in migrated_results if 'id' in v)

def main(check):
    raw=source(PIN)
    assert hashlib.sha256(raw).hexdigest()==PIN['sha256']
    records=[]
    with ZipFile(io.BytesIO(raw)) as jar:
        for path in sorted(BASE.glob("**/*.json")):
            rel=path.relative_to(BASE).as_posix()
            nativepath='data/minecells/recipe/'+rel
            raw_native=jar.read(nativepath)
            old=json.loads(raw_native)
            obj=convert(old)
            validate(old,obj)
            encoded=(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode()
            if check:
                assert path.read_bytes()==encoded,("stale recipe",str(path))
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(encoded)
            records.append({"id":"minecells:"+rel[:-5],"native_source":nativepath,
                            "original_sha256":hashlib.sha256(raw_native).hexdigest(),
                            "override_sha256":hashlib.sha256(encoded).hexdigest(),
                            "codec":old['type']})
    assert len(records)==15,len(records)
    report={"source_mod_pin":{"projectID":PIN['projectId'],"fileID":PIN['id'],
                              "sha256":PIN['sha256']},
            "migration_count":len(records),"runtime_tested":False,
            "left_disabled":["brewinandchewin:hamburger_with_cheese",
                             "brewinandchewin:pizza_from_dough",
                             "brewinandchewin:toast_with_cheese",
                             "dimdungeons:recipe_item_guidebook"],
            "records":records}
    report_path=ROOT/'build/v042-minecells-recipe-migration.json'
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print("PASS",len(records),"SHA-pinned original author recipes migrated to NeoForge codecs, 4 still disabled; NOT runtime-tested")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    main(parser.parse_args().check)
