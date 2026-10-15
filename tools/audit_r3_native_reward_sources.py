#!/usr/bin/env python3
"""Evidence-only audit of R3 Grand Treasure / Regalia against INSTALLED mod JARs.

Does NOT change loot rules or auto-approve item IDs. Requires local CurseForge
profile mods/ or equivalent exact mod JAR collection, not just an import ZIP.

Usage:
  python tools/audit_r3_native_reward_sources.py --mods "C:\...\Minecraft\Instances\Ambient Odyssey\mods" --out build/r3-rewards-native-audit.json
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import tomllib
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=ROOT/'docs/handoffs/loot-update-20261015/grand-treasure-candidates.json'
CATALOGUE=ROOT/'docs/balance/REGALIA_ITEM_CATALOGUE_EXPANSION_2026-10-13.csv'
RANKING=ROOT/'docs/balance/REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv'
CURRENT_POLICY=ROOT/'docs/handoffs/loot-update-20261015/effective-loot-policy.json'

def digest(data): return hashlib.sha256(data).hexdigest()

def loot_resource(table):
    namespace,location=table.split(':',1)
    return f'data/{namespace}/loot_table/{location}.json'

def load_jar_index(mods):
    archives={}
    mod_sources=defaultdict(set)
    for p in sorted(mods.glob('*.jar')):
        try:
            with zipfile.ZipFile(p) as z:
                paths=set(z.namelist())
                archives[p.name]=paths
                if 'META-INF/neoforge.mods.toml' in paths:
                    obj=tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode('utf-8-sig'))
                    for m in obj.get('mods',[]):
                        if m.get('modId'):mod_sources[m['modId']].add(p.name)
                if 'fabric.mod.json' in paths:
                    modid=json.loads(z.read('fabric.mod.json')).get('id')
                    if modid:mod_sources[modid].add(p.name)
        except (zipfile.BadZipFile,UnicodeDecodeError,ValueError) as exc:
            raise ValueError(f'Installed JAR is unreadable: {p.name}: {exc}') from exc
    if not archives:raise ValueError(f'No JAR files in {mods}')
    return archives,mod_sources

def local_overlays(root,resources):
    if root is None:return {}
    mapping=defaultdict(list)
    for data_dir in root.glob('*/data'):
        for p in data_dir.rglob('*'):
            if p.is_file():
                key='data/'+p.relative_to(data_dir).as_posix()
                if key in resources:
                    mapping[key].append(str(p))
    return dict(mapping)

def summarize_native_pool(pool,index):
    # Preserve actual native entry weights and function IDs for human review;
    # numerical score heuristics do not establish the best room-specific pool.
    return {
        'pool_index':index,
        'native_rolls':pool.get('rolls'),
        'native_bonus_rolls':pool.get('bonus_rolls'),
        'pool_conditions':pool.get('conditions',[]),
        'pool_functions':pool.get('functions',[]),
        'entries':[{
            'type':e.get('type'),'name':e.get('name'),
            'weight':e.get('weight',1),'quality':e.get('quality',0),
            'functions':e.get('functions',[]),
            'conditions':e.get('conditions',[]),
            'has_children':bool(e.get('children')),
        } for e in pool.get('entries',[])],
    }

def grand_check(rows,mods,index,paxi=None):
    required=set()
    for r in rows:
        required.add(r['source_resource'])
        required.add(loot_resource(r['table']))
    resource_owners=defaultdict(list)
    for jar,names in index.items():
        for name in names.intersection(required):
            resource_owners[name].append(jar)
    overlays=local_overlays(paxi,required)
    checked=[]
    for r in rows:
        trigger=loot_resource(r['table'])
        source=r['source_resource']
        owner_files=resource_owners.get(source,[])
        blockers=[]
        if not resource_owners.get(trigger):
            blockers.append('TRIGGER_TABLE_MISSING_FROM_INSTALLED_JARS')
        if len(owner_files)!=1:
            blockers.append('SOURCE_MISSING_OR_AMBIGUOUS_JARS')
        if overlays.get(source) or overlays.get(trigger):
            blockers.append('PAXI_TABLE_OVERRIDE_PRECEDENCE_REQUIRES_RUNTIME_CONFIRMATION')
        pool=None;hash_valid=False;properties={};all_pool_summaries=[]
        if len(owner_files)==1:
            with zipfile.ZipFile(mods/owner_files[0]) as z:
                data=z.read(source)
            hash_valid=digest(data)==r['source_sha256']
            if not hash_valid:blockers.append('SOURCE_SHA256_CHANGED')
            try:
                obj=json.loads(data)
                all_pool_summaries=[summarize_native_pool(p,j) for j,p in enumerate(obj['pools'])]
                i=r['pool_index']
                if not isinstance(i,int) or i<0 or i>=len(obj['pools']):
                    blockers.append('POOL_INDEX_OUT_OF_RANGE')
                else:
                    pool=obj['pools'][i]
                    entries=pool.get('entries',[])
                    # A basic pool may still have native item functions/conditions;
                    # record them for manual review instead of silently removing them.
                    properties={
                        'pool_entry_types':[e.get('type') for e in entries],
                        'pool_entry_names':[e.get('name') for e in entries if 'name' in e],
                        'pool_has_conditions':bool(pool.get('conditions')),
                        'pool_has_functions':bool(pool.get('functions')),
                        'table_has_functions':bool(obj.get('functions')),
                        'pool_original_rolls':pool.get('rolls'),
                        'pool_original_bonus_rolls':pool.get('bonus_rolls'),
                    }
                    if any(t not in ('minecraft:item','minecraft:empty') for t in properties['pool_entry_types']):
                        blockers.append('NON_SIMPLE_POOL_REQUIRES_MANUAL_REVIEW')
                    if pool.get('conditions'):
                        blockers.append('NATIVE_POOL_CONDITIONS_REQUIRES_MANUAL_REVIEW')
            except (ValueError,KeyError,IndexError,TypeError) as exc:
                blockers.append('INVALID_SOURCE_TABLE_OR_POOL: '+str(exc)[:100])
        cross=source!=trigger
        if cross:
            blockers.append('CROSS_TABLE_SOURCE_CHOICE_NEEDS_INDEPENDENT_REVIEW')
        if not r.get('tier',0)>=3 or r.get('chance')!=0.05:
            blockers.append('OWNER_TIER_OR_PROBABILITY_MISMATCH')
        checked.append({
            'structure':r['structure'],'tier':r['tier'],'trigger_table':r['table'],
            'selected_native_source':source,'same_table':not cross,'source_jar_candidates':owner_files,
            'trigger_jar_candidates':resource_owners.get(trigger,[]),
            'expected_source_sha256':r['source_sha256'],'actual_source_sha256_matches':hash_valid,
            'pool_index':r['pool_index'],'source_pool_details':properties,
            'native_all_pools_for_human_comparison':all_pool_summaries,
            'potential_paxi_overrides':sorted(set(overlays.get(trigger,[])+overlays.get(source,[]))),
            'static_status':'BLOCKED' if blockers else 'SOURCE_STATIC_VERIFIED_NOT_RUNTIME_APPROVED',
            'blockers':blockers,
        })
    return checked

def regalia_check(mods,index,mod_sources):
    with CATALOGUE.open(encoding='utf-8-sig',newline='') as file:
        rows=list(csv.DictReader(file))
    with RANKING.open(encoding='utf-8-sig',newline='') as file:
        ranked={r['item_registry_candidate']:r for r in csv.DictReader(file)}
    current=set(json.loads(CURRENT_POLICY.read_text(encoding='utf-8'))['regalia'])
    found=[]
    for r in rows:
        ident=r.get('candidate_registry_id','')
        if ':' not in ident:continue
        ns,item=ident.split(':',1)
        if not ns or not item:continue
        hard_native_only=ns in {'enigmaticlegacy','enigmaticlegacyplus'}
        is_paster=ns in {'pasterdream','neopasterdream'}
        family=(r.get('item_family') or '').lower()
        accessory_terms=('amulet','charm','cloak','accessory','curios','ring','headwear','tiara','necklace','talisman','bracelet')
        confirmed_paster_accessories={'pasterdream:turnback_cloak','pasterdream:ceciliacare_charm',
            'pasterdream:evasion_cloak','pasterdream:counter_ring','pasterdream:ghost_face_head','pasterdream:qym_head'}
        # An ID containing "ring" or "head" need not be an accessory (e.g. a
        # weapon). Do not infer accessory classification from arbitrary substrings.
        accessory=is_paster and (any(t in family for t in accessory_terms) or ident in confirmed_paster_accessories)
        hard_native_only |= accessory or ident=='cataclysm:cursium_chestplate'
        if ns=='simplyswords':
            disposition='SEPARATE_UNIQUE_WEAPON_REWARD'
        elif hard_native_only:
            disposition='NATIVE_ONLY_NO_NEW_REGALIA_REWARD'
        elif is_paster:
            disposition='HOLD_PASTERDREAM_ACCESSORY_STATUS'
        elif ident=='cataclysm:the_annihilator':
            disposition='HOLD_OWNER_NOT_APPROVED'
        else:disposition='ELIGIBILITY_UNREVIEWED'
        jars=sorted(mod_sources.get(ns,[]))
        expected=r.get('installed_jar','')
        if expected in index and expected not in jars:jars.append(expected)
        clues=[]
        for jar in jars:
            paths=index[jar]
            for res in (f'assets/{ns}/models/item/{item}.json',
                        f'assets/{ns}/items/{item}.json',
                        f'data/{ns}/recipe/{item}.json'):
                if res in paths:clues.append({'jar':jar,'resource':res})
        found.append({
            'id':ident,'name':r.get('display_name'),'source_mod':r.get('mod'),
            'installed_jar_in_catalogue':expected,
            'jar_candidates':jars,'resource_clues':clues,
            'resource_clues_are_not_registry_proof':True,
            'registered_item_verified':False,
            'currently_in_r2_reward_pool':ident in current,
            'known_combat_risk_band':ranked.get(ident,{}).get('combat_risk_band','C? — unscored'),
            'owner_disposition':disposition,
        })
    return found

def audit(mods,paxi=None,candidates=CANDIDATES):
    if not mods.is_dir():raise ValueError(f'Installed mods directory does not exist: {mods}')
    if paxi is not None and not paxi.is_dir():
        raise ValueError(f'Provided Paxi datapacks directory does not exist; cannot silently claim no overrides: {paxi}')
    index,mod_sources=load_jar_index(mods)
    rows=json.loads(Path(candidates).read_text(encoding='utf-8'))
    if not isinstance(rows,list) or not rows:
        raise ValueError('Candidate JSON must be a nonempty list of native Grand Treasure chest contexts')
    grand=grand_check(rows,mods,index,paxi)
    regalia=regalia_check(mods,index,mod_sources)
    return {
        'status':'STATIC_JAR_EVIDENCE_ONLY_NOT_RUNTIME_ACCEPTED',
        'installed_jar_count':len(index),'paxi_path':str(paxi) if paxi else None,
        'grand_context_count':len(grand),
        'grand_direct_contexts':sum(r['same_table'] for r in grand),
        'grand_cross_table_contexts':sum(not r['same_table'] for r in grand),
        'grand_blocked_contexts':sum(r['static_status']=='BLOCKED' for r in grand),
        'grand':grand,
        'catalogue_rows_checked':len(regalia),
        'regalia_native_only_count':sum(r['owner_disposition']=='NATIVE_ONLY_NO_NEW_REGALIA_REWARD' for r in regalia),
        'regalia_already_in_r2_reward_pool':sum(r['currently_in_r2_reward_pool'] for r in regalia),
        'regalia_unscored_candidates':sum(r['known_combat_risk_band'].startswith('C?') for r in regalia),
        'regalia_source_evidence_only':regalia,
        'limitations':[
            'Compiled items may lack model/recipe resources; static clues never prove registration or gameplay safety.',
            'Paxi load order, Lootr instancing, native item functions and effective pool semantics require Minecraft runtime tests.',
            'No unknown or unscored Regalia are auto-approved; owner exclusions remain binding.',
            'This tool never edits game files or reward policies.',
        ],
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mods',required=True,type=Path,help='Actual installed profile mods/ directory')
    p.add_argument('--paxi',type=Path,help='Optional active profile config/paxi/datapacks')
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--candidates',type=Path,default=CANDIDATES,
                   help='Candidate JSON to audit (default: historical R2 list; use R3 preview to audit new mapping)')
    args=p.parse_args()
    result=audit(args.mods,args.paxi,args.candidates)
    result['candidate_input_file']=str(args.candidates)
    result['candidate_input_sha256']=digest(args.candidates.read_bytes())
    if args.out.exists():raise ValueError('Refusing to overwrite existing audit output: '+str(args.out))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in {
        'status','installed_jar_count','grand_context_count','grand_direct_contexts',
        'grand_cross_table_contexts','grand_blocked_contexts','catalogue_rows_checked',
        'regalia_native_only_count'}},indent=2))

if __name__=='__main__':main()
