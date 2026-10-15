#!/usr/bin/env python3
"""Verify every R3 Dungeons Arise Grand candidate against exact published 2.1.68 JAR.

Read-only source evidence. No loot table replacement, imports, R3 compilation
or gameplay claims. Requires 1.21.1 NeoForge DungeonsArise 2.1.68.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from verify_keep_kayra_native_loot import EXPECTED_JAR, pool_summary, sha

ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=ROOT/'docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json'

def inspect(path):
    if path.name!=EXPECTED_JAR:raise ValueError('Incorrect Dungeons Arise JAR version or loader')
    candidates=json.loads(CANDIDATES.read_text(encoding='utf-8'))
    rows=[x for x in candidates if x['structure'].startswith('dungeons_arise:')]
    if len(rows)!=11:raise ValueError('Expected precisely 11 source-scoped WDA contexts')
    checked=[]
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise ValueError('Native Dungeons Arise JAR CRC failed')
        for r in rows:
            name=r['source_resource']
            namespace,loc=r['table'].split(':',1)
            if name!=f'data/{namespace}/loot_table/{loc}.json':
                raise ValueError('Proposed pool borrows another source: '+r['table'])
            if name not in z.namelist():raise ValueError('Source table missing: '+name)
            raw=z.read(name)
            if sha(raw)!=r['source_sha256']:raise ValueError('Native table SHA mismatch: '+name)
            pools=json.loads(raw)['pools'];idx=r['pool_index']
            if not isinstance(idx,int) or idx<0 or idx>=len(pools):
                raise ValueError('Native selected pool outside array: '+name)
            selected=pool_summary(pools[idx],idx,idx)
            checks=['minecraft:item','minecraft:empty']
            if not selected['entries'] or any(e['type'] not in checks or e['has_children'] for e in selected['entries']):
                raise ValueError('Proposed pool is non-simple or contains recursive entries: '+name)
            if selected['pool_conditions']:
                raise ValueError('Selected native pool has conditions needing separate review: '+name)
            checked.append({
                'structure':r['structure'],'table':r['table'],'source_sha256':sha(raw),
                'tier':r['tier'],'candidate_pool_index':idx,
                'all_native_pools':[pool_summary(p,i,idx) for i,p in enumerate(pools)],
                'source_integrity':'MATCHED_PINNED_JAR',
                'human_category_approval':'PENDING',
                'effective_paxi_precedence':'NOT_TESTED',
                'lootr_multiplayer':'NOT_TESTED',
            })
    return {
      'status':'ELEVEN_DUNGEONS_ARISE_SOURCE_HASHES_CONFIRMED_NOT_RUNTIME_TESTED',
      'mod_file':EXPECTED_JAR,'jar_sha256':sha(path.read_bytes()),
      'contexts':checked,'count':len(checked),
      'original_loot_unchanged_by_audit':True,
      'candidate_is_not_owner_approval':True,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jar',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():raise ValueError('Refuse to overwrite prior evidence')
    result=inspect(args.jar)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('AO_R3_WDA_SUMMARY_BEGIN')
    for c in result['contexts']:
        selected=c['all_native_pools'][c['candidate_pool_index']]
        compact={'table':c['table'],'pool':selected['index'],
                 'rolls':selected['native_rolls'],
                 'entries':[{'id':e['id'],'weight':e['weight'],'functions':e['functions']} for e in selected['entries']],
                 'all_pools':len(c['all_native_pools'])}
        print(json.dumps(compact,separators=(',',':')))
    print('AO_R3_WDA_SUMMARY_END')
    print('Verified native Dungeons Arise chest contexts:',result['count'])

if __name__=='__main__':main()
