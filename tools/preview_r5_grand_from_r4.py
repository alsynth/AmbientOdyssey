#!/usr/bin/env python3
"""Preview exactly five R4 -> R5 Grand Treasure pool-index changes.

The output is REVIEW ONLY and must not be used as a packaged campaign policy
without separate owner/category acceptance, installed-JAR/Paxi effective-source
verification, native behavior and dedicated two-player Lootr tests.

Usage:
 python tools/preview_r5_grand_from_r4.py --out build/r5-grand/ao_loot_policy.REVIEW_ONLY.json
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'addons/ao-campaign/src/main/resources/ao_loot_policy.json'
PROPOSALS=ROOT/'docs/handoffs/r5-grand-from-r4-20261015/REVIEW_ONLY_FIVE_POOL_DIFF.json'
SHA=re.compile(r'^[0-9a-f]{64}$')

def key(x):
    return (x['structure'],x['table'])

def transform(base,proposal):
    if proposal.get('status')!='R5_ONLY_FIVE_REVIEW_POOL_CHANGES_NOT_APPROVED_NOT_PACKAGED':
        raise ValueError('Not a review-only R4 delta')
    if proposal.get('source_release_sha256')!='31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d':
        raise ValueError('Not based on pinned published R4 import')
    rows=base.get('grand_treasure')
    if not isinstance(rows,list) or len(rows)!=14 or len({key(v) for v in rows})!=14:
        raise ValueError('Expected exactly fourteen unique R4 Grand contexts')
    if len(base.get('regalia',[]))!=13 or len(base.get('unique_weapons',[]))!=58:
        raise ValueError('Unexpected R4 addon policy roster. Reconcile before preview.')
    changes=proposal.get('changes')
    if not isinstance(changes,list) or len(changes)!=5 or len({key(v) for v in changes})!=5:
        raise ValueError('Expected exactly five different R4-native pool proposals')
    if proposal.get('scope',{}).get('changed_pool_indices')!=5:
        raise ValueError('Invalid proposal scope')
    indexed={key(r):r for r in rows}
    proposed=copy.deepcopy(base)
    new_indexed={key(r):r for r in proposed['grand_treasure']}
    receipt=[]
    for c in changes:
        k=key(c);old=indexed.get(k)
        if old is None:
            raise ValueError('Proposal adds an unauthorized chest: '+str(k))
        for field in ('tier','source_resource','source_sha256','chance'):
            if c.get(field)!=old[field]:
                raise ValueError('Proposal changes preserved R4 field '+field+': '+str(k))
        ns,resource_path=c['table'].split(':',1)
        if c['source_resource']!=f'data/{ns}/loot_table/{resource_path}.json':
            raise ValueError('Cross-table source forbidden in this reviewed preview')
        if not SHA.fullmatch(c['source_sha256']):
            raise ValueError('Invalid original native resource hash')
        if not c.get('source_evidence')=='SOURCE_HASH_VERIFIED_FROM_PINNED_UPSTREAM_JAR':
            raise ValueError('No original native JAR evidence')
        if c.get('approval')!='SOURCE_VERIFIED_CATEGORY_REVIEW_ONLY' or c.get('runtime_tested') is not False:
            raise ValueError('Cannot auto-promote an unaccepted gameplay candidate')
        if type(c.get('original_pool_index')) is not int or old['pool_index']!=c['original_pool_index']:
            raise ValueError('R4 selected index differs; refuses stale/rebased proposal')
        if type(c.get('proposed_pool_index')) is not int or c['proposed_pool_index']<0 or old['pool_index']==c['proposed_pool_index']:
            raise ValueError('Incorrect or no-op native pool index')
        new_indexed[k]['pool_index']=c['proposed_pool_index']
        receipt.append({'table':c['table'],'old_pool':old['pool_index'],
                        'review_only_candidate_pool':c['proposed_pool_index'],
                        'native_table_sha256':old['source_sha256'],
                        'reason':c['reason'],'gameplay_accepted':False})
    # NEVER widen scope or rewrite original probabilities, table keys, bosses,
    # Regalia, uniques, affix rates or gem/party policies.
    for before,after in zip(rows,proposed['grand_treasure']):
        differing={v for v in set(before)|set(after) if before.get(v)!=after.get(v)}
        if differing not in (set(),{'pool_index'}):
            raise ValueError('Unexpected policy drift '+str(key(before)))
    for name in base:
        if name!='grand_treasure' and proposed[name]!=base[name]:
            raise ValueError('Unexpected non-Grand loot policy drift')
    if sum(a['pool_index']!=b['pool_index'] for a,b in zip(rows,proposed['grand_treasure']))!=5:
        raise ValueError('Exactly five changes required')
    receipt.sort(key=lambda v:v['table'])
    return proposed,receipt

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,default=BASE)
    parser.add_argument('--proposals',type=Path,default=PROPOSALS)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():
        raise ValueError('Never overwrite existing preview')
    if not args.out.resolve().is_relative_to((ROOT/'build').resolve()):
        raise ValueError('Preview path must be under project build/')
    base_bytes=args.base.read_bytes()
    proposals_bytes=args.proposals.read_bytes()
    proposals=json.loads(proposals_bytes)
    # Pin the exact R4 campaign source file, not merely its 13/58 roster sizes.
    blob=hashlib.sha1(b'blob '+str(len(base_bytes)).encode()+b'\x00'+base_bytes).hexdigest()
    if proposals.get('source_policy_git_blob_sha1')!=blob:
        raise ValueError('R4 campaign policy bytes differ from the exact pinned GitHub blob; re-review changes')
    proposed,changes=transform(json.loads(base_bytes),proposals)
    result={'status':'REVIEW_ONLY_NOT_A_COMPILED_RELEASE',
            'r4_source_policy_sha256':hashlib.sha256(base_bytes).hexdigest(),
            'proposal_sha256':hashlib.sha256(proposals_bytes).hexdigest(),
            'changed_pools':changes,
            'grand_contexts':len(proposed['grand_treasure']),
            'untouched_non_grand_sections':[k for k in proposed if k!='grand_treasure'],
            'must_still_verify':['matching installed JARs and Paxi effective resource winner',
                                 'manual chest category and bonus pool review',
                                 'native loot additions and probability invariance',
                                 'two-player Lootr/reopen/restart semantics'],
            'policy':proposed}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('R4-based review-only Grand preview generated: 5 of 14 source pool indices proposed for change. Nothing packaged.')

if __name__=='__main__':
    main()
