#!/usr/bin/env python3
"""Audit authentic When Dungeons Arise 2.1.68 Keep Kayra native loot resources.

Read-only. Uses the EXACT pinned 1.21.1 NeoForge mod JAR.
Requires source-table hashes in docs/handoffs/loot-update-20261015/
chest-source-audit.json to match the actual JAR. Does not automatically approve
Grand Treasure pools or replace native loot.

Usage: python tools/verify_keep_kayra_native_loot.py --jar /path/DungeonsArise-1.21.1-2.1.68-release.jar --out build/keep-kayra-native-source-evidence.json
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/handoffs/loot-update-20261015/chest-source-audit.json'
STRUCTURE='dungeons_arise:keep_kayra'
EXPECTED_JAR='DungeonsArise-1.21.1-2.1.68-release.jar'

def sha(b):return hashlib.sha256(b).hexdigest()

def pool_summary(pool,index,selected):
    records=[]
    for e in pool.get('entries',[]):
        records.append({
            'type':e.get('type'),'id':e.get('name'),'weight':e.get('weight',1),
            'quality':e.get('quality',0),
            'functions':[v.get('function','UNKNOWN') for v in e.get('functions',[])],
            'conditions':[v.get('condition','UNKNOWN') for v in e.get('conditions',[])],
            'has_children':bool(e.get('children')),
        })
    return {
      'index':index,'previously_auto_selected':selected==index,
      'native_rolls':pool.get('rolls'),'native_bonus_rolls':pool.get('bonus_rolls'),
      'pool_functions':[v.get('function','UNKNOWN') for v in pool.get('functions',[])],
      'pool_conditions':[v.get('condition','UNKNOWN') for v in pool.get('conditions',[])],
      'entry_count':len(records),'entries':records,
    }

def inspect_jar(path):
    if path.name != EXPECTED_JAR:
        raise ValueError('Require exact pinned NeoForge mod JAR filename: '+EXPECTED_JAR)
    rows=json.loads(AUDIT.read_text(encoding='utf-8'))
    kayra=[r for r in rows if r['structure']==STRUCTURE and 'resource' in r]
    if len(kayra)!=6:
        raise ValueError('Historical Keep Kayra chest audit must include six native tables; found '+str(len(kayra)))
    names=set()
    output=[]
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise ValueError('Upstream JAR failed CRC check')
        for row in kayra:
            res=row['resource']
            if res in names:raise ValueError('Duplicate Keep Kayra resource')
            names.add(res)
            if not res.startswith('data/dungeons_arise/loot_table/chests/keep_kayra/'):
                raise ValueError('Unexpected source path')
            if res not in z.namelist():
                raise ValueError('Native resource absent: '+res)
            raw=z.read(res);dig=sha(raw)
            if dig!=row['source_sha256']:
                raise ValueError('Native source HASH MISMATCH: '+res+' expected '+row['source_sha256']+' got '+dig)
            table=json.loads(raw)
            pools=table.get('pools')
            if not isinstance(pools,list) or len(pools)!=row['pool_count']:
                raise ValueError('Native source pool count mismatch: '+res)
            idx=row.get('selected_pool')
            if idx is not None and (not isinstance(idx,int) or not 0<=idx<len(pools)):
                raise ValueError('Previously audited pool index out of range: '+res)
            output.append({
                'chest_table':row['table'],
                'native_resource':res,
                'raw_source_sha256':dig,
                'prior_audit_status':row['status'],
                'selected_candidate_pool_index':idx,
                'table_level_functions':[fn.get('function','UNKNOWN') for fn in table.get('functions',[])],
                'pools':[pool_summary(p,j,idx) for j,p in enumerate(pools)]
            })
    return {
        'status':'PINNED_UPSTREAM_JAR_SOURCE_HASH_VERIFIED_NOT_GAMEPLAY_TESTED',
        'pinned_mod':EXPECTED_JAR,
        'pinned_jar_sha256':sha(path.read_bytes()),
        'verified_chest_table_count':len(output),
        'chests':output,
        'scope_limits':[
            'Hashes prove these native table resources match prior audit, not full datapack/Paxi effective precedence.',
            'Pool entries and weights below are native source descriptions, not approved new Grand Treasure rewards.',
            'No native treasure table has been overwritten; original Lootr and affix chances still need runtime checks.'
        ]
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():raise ValueError('Never overwrite existing source evidence')
    result=inspect_jar(args.jar)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('AO_NATIVE_KAYRA_JSON_BEGIN')
    print(json.dumps(result,separators=(',',':'),ensure_ascii=False))
    print('AO_NATIVE_KAYRA_JSON_END')
    print('Source tables verified:', result['verified_chest_table_count'])
if __name__=='__main__':main()
