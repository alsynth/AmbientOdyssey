"""Activate a bounded owner-selected DD batch only after real registry/biome evidence.

The evidence proves registered IDs and normal-preset biome eligibility, not that
natural placement, spawners or fights were tested. No category-default mass rollout.
"""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R3_SHA='5debe094c047162f0b30f2dd76e2ab85201310c480b64333eca89a4f4376ac99'
BATCH=(
    'dungeons_arise:abandoned_temple', 'dungeons_arise:kisegi_sanctuary',
    'dungeons_arise_seven_seas:corsair_corvette', 'iceandfire:mausoleum',
    'adventuredungeons:underground_camp', 'dungeons_arise:bandit_village',
    'dungeons_arise:mining_system', 'dungeons_arise:mining_complex',
)
OUT=ROOT/'docs/handoffs/dd-native-batch-r4-20261015'


def eligibility(plan,evidence,protected):
    sid=plan['structure_id']
    if sid in protected or sid=='dungeons_arise:mechanical_nest' or sid.startswith(('pasterdream:','neopasterdream:')):
        return 'EXCLUDED_OWNER_EXCEPTION'
    if plan['decision'] not in {'KEEP','CHANGE'} or plan['selected_structure_tier'] not in {'2','3','4','5','6'}:
        return 'HOLD_OWNER_TIER_NOT_APPROVED'
    if evidence is None or not evidence.get('registered'):
        return 'HOLD_ID_NOT_REGISTERED'
    dims=evidence.get('normal_preset_biome_overlap',{})
    if not dims.get('minecraft:overworld'):
        return 'HOLD_NO_NORMAL_OVERWORLD_BIOME_MATCH'
    if any(v for k,v in dims.items() if k!='minecraft:overworld'):
        return 'HOLD_AMBIGUOUS_NORMAL_DIMENSION'
    return 'NATIVE_REGISTRY_AND_OVERWORLD_BIOME_ELIGIBLE'


def run(runtime,apply=False):
    ledger=OUT/'rollout.json'
    if apply and ledger.exists() and json.loads(ledger.read_text()).get('applied'):
        raise ValueError('Batch already applied; preserve the original before/after rollout evidence')
    snapshot=json.loads((runtime/'INPUT_SNAPSHOT.json').read_text(encoding='utf-8'))
    if snapshot['pack_sha256']!=R3_SHA:
        raise ValueError('Evidence must be from the exact R3 RECONCILED package')
    if json.loads((runtime/'RESULT.json').read_text())['overall_probe']!='PASS':
        raise ValueError('Native evidence run did not pass; inspect failure rather than promoting zones')
    observations=json.loads((runtime/'DD_EXPANSION_REGISTRY_OBSERVATIONS.json').read_text())
    rows=list(csv.DictReader((ROOT/'experiments/structure-difficulty-v4/DD_CONSOLIDATED_OWNER_TIER_PLAN_20261015.csv').open(encoding='utf-8-sig')))
    plan={r['structure_id']:r for r in rows}
    actual={r['structure_id']:r for r in observations['candidates']}
    protected={r['structure_id'] for r in csv.DictReader((ROOT/'docs/balance/DD_OWNER_PROTECTED_26_SPAWNER_STRUCTURES_20261014.csv').open(encoding='utf-8-sig'))}
    path=ROOT/'release_030/overrides/config/dungeon_difficulty/difficulty_v2.json'
    before=path.read_bytes();config=json.loads(before);new=copy.deepcopy(config)
    world=next(w for w in new['dimensions'] if w['world_matches']['dimension']=='minecraft:overworld')
    existing={z['zone_matches']['structure'] for z in world['zones']}
    review=[];added=[]
    for sid in BATCH:
        row=plan[sid];obs=actual.get(sid);status=eligibility(row,obs,protected)
        record={'structure_id':sid,'selected_tier':int(row['selected_structure_tier']),
                'status':status,'owner_plan_row':row,'native_evidence':obs,
                'natural_generation_tested':False,'combat_tested':False}
        if sid in existing:record['status']='ALREADY_PRESENT'
        elif status=='NATIVE_REGISTRY_AND_OVERWORLD_BIOME_ELIGIBLE':
            world['zones'].append({'zone_matches':{'biome':None,'structure':sid},
                                   'difficulty':{'name':'ao_tier_'+row['selected_structure_tier'],'level':1}})
            added.append(record)
        review.append(record)
    # Existing budgets, matchers and every other dimension stay byte-semantically unchanged.
    assert new['difficulty_types']==config['difficulty_types']
    result={'evidence_package_sha256':R3_SHA,'source_config_before_sha256':hashlib.sha256(before).hexdigest(),
            'source_config_after_sha256':None,'applied':apply,'baseline_zone_count':len(existing),
            'effective_zone_count':len(world['zones']),'added':added,'review':review,
            'scope':'Real registered IDs + normal preset biome eligibility; natural generation, mob spawners, gameplay and multiplayer NOT TESTED'}
    if apply:
        raw=(json.dumps(new,indent=2)+'\n').encode();path.write_bytes(raw)
        result['source_config_after_sha256']=hashlib.sha256(raw).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/('rollout.json' if apply else 'candidate-review.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'apply':apply,'added':len(added),'zones':len(world['zones']),
                      'held':[(r['structure_id'],r['status']) for r in review if r not in added]},indent=2))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--apply',action='store_true')
    a=p.parse_args();run(a.runtime,a.apply)
