#!/usr/bin/env python3
"""R3 Grand Treasure experimental policy staging, with explicit per-chest gates.

Does NOT touch the compiled addon, historical R2 policy, or active modpack.
Do not infer that a 5% bonus or Lootr persistence was runtime-tested here.

1. Run the installed-JAR native source audit with --candidates pointing to the
   committed R3 per-chest preview.
2. Run this with --mode draft to obtain EMPTY human-review checkboxes.
3. Review original native pools, source hashes/weights/functions, and category
   fit, then deliberately complete the review file.
4. Use --mode stage to write an isolated campaign policy under build/.

Only AFTER an isolated experimental policy passes its gates may a separate
R3 addon build use that staged policy as input; packaging remains independent.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/handoffs/loot-update-20261015'
CANDIDATES=DOC/'R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json'
BASE_POLICY=ROOT/'addons/ao-campaign/src/main/resources/ao_loot_policy.json'
DRAFT_FORMAT='AO_R3_GRAND_CHEST_REVIEW_1'
ALLOWED_CHANCE=0.05

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def key(row):
    return row['structure']+'|'+row['table']

def table_resource(table):
    ns, name=table.split(':',1)
    return 'data/'+ns+'/loot_table/'+name+'.json'

def mappings(rows):
    if not isinstance(rows,list) or not rows:
        raise ValueError('Grand candidates must be a nonempty JSON list')
    result={}
    for item in rows:
        name=key(item)
        if name in result:
            raise ValueError('Duplicate candidate: '+name)
        if set(item)!={'structure','tier','table','source_resource','source_sha256','pool_index','chance'}:
            raise ValueError('Unexpected candidate fields: '+name)
        if item['tier']<3 or type(item['tier']) is not int or item['chance']!=ALLOWED_CHANCE:
            raise ValueError('Wrong tier/chance: '+name)
        if item['source_resource']!=table_resource(item['table']):
            raise ValueError('Source is not the current chest table: '+name)
        if type(item['pool_index']) is not int or item['pool_index']<0:
            raise ValueError('Invalid pool index: '+name)
        if not isinstance(item['source_sha256'],str) or len(item['source_sha256'])!=64 or any(c not in '0123456789abcdef' for c in item['source_sha256']):
            raise ValueError('Invalid resource SHA: '+name)
        result[name]=item
    return result

def audit_index(candidates, candidate_bytes, audit):
    if audit.get('status')!='STATIC_JAR_EVIDENCE_ONLY_NOT_RUNTIME_ACCEPTED':
        raise ValueError('Native JAR audit missing static-only status')
    if audit.get('candidate_input_sha256')!=sha(candidate_bytes):
        raise ValueError('Native JAR audit was produced from another candidate file')
    if audit.get('grand_context_count')!=len(candidates):
        raise ValueError('Audit chest count does not match candidate set')
    checked={}
    for item in audit.get('grand',[]):
        k=item['structure']+'|'+item['trigger_table']
        if k in checked:raise ValueError('Duplicate native-JAR audit row: '+k)
        checked[k]=item
    if set(checked)!=set(candidates):
        raise ValueError('Native-JAR audit rows differ from candidate context set')
    return checked

def draft(candidates,candidate_bytes,audit,audit_bytes):
    checked=audit_index(candidates,candidate_bytes,audit)
    return {
        'format':DRAFT_FORMAT,
        'status':'DRAFT_NOT_APPROVED',
        'candidate_sha256':sha(candidate_bytes),
        'audit_sha256':sha(audit_bytes),
        'decisions':[{
            'structure':v['structure'],
            'table':v['table'],
            'source_sha256':v['source_sha256'],
            'pool_index':v['pool_index'],
            'static_audit_blockers':checked[k]['blockers'],
            'reviewed_category_fit':False,
            'reviewed_native_entries_weights_conditions_functions':False,
            'approved_for_experimental_build':False,
            'reviewer_rationale':'',
        } for k,v in candidates.items()]
    }

def stage(candidates,candidate_bytes,audit,audit_bytes,decisions,base):
    reviewed=audit_index(candidates,candidate_bytes,audit)
    if decisions.get('format')!=DRAFT_FORMAT:
        raise ValueError('Unknown approval format')
    if decisions.get('candidate_sha256')!=sha(candidate_bytes):
        raise ValueError('Review references a different candidate SHA')
    if decisions.get('audit_sha256')!=sha(audit_bytes):
        raise ValueError('Review references a different installed-JAR audit SHA')
    rows=decisions.get('decisions',[])
    if not isinstance(rows,list):
        raise ValueError('Review decisions must be a list')
    by_key={}
    for v in rows:
        k=key(v)
        if k in by_key:raise ValueError('Duplicate approval row: '+k)
        by_key[k]=v
    if set(by_key)!=set(candidates):
        raise ValueError('Review approval context set differs from candidates')
    if not isinstance(base.get('grand_treasure'),list) or not base['grand_treasure']:
        raise ValueError('Invalid existing R2 campaign policy')
    base_keys={key(r) for r in base['grand_treasure']}
    if base_keys!=set(candidates) or len(base['grand_treasure'])!=len(candidates):
        raise ValueError('Different existing campaign chest contexts: no widening without owner review')
    for k,v in candidates.items():
        a=reviewed[k]
        if a.get('static_status')!='SOURCE_STATIC_VERIFIED_NOT_RUNTIME_APPROVED' or a.get('blockers'):
            raise ValueError('Installed JAR source check did not pass: '+k)
        if a.get('selected_native_source')!=v['source_resource'] or not a.get('same_table'):
            raise ValueError('Native audit resolved another source: '+k)
        if a.get('expected_source_sha256')!=v['source_sha256'] or a.get('actual_source_sha256_matches') is not True:
            raise ValueError('Native loot resource SHA not verified: '+k)
        if a.get('pool_index')!=v['pool_index'] or len(a.get('source_jar_candidates',[]))!=1:
            raise ValueError('Missing unique native provider/pool identity: '+k)
        if a.get('potential_paxi_overrides'):
            raise ValueError('Effective Paxi precedence cannot be proven: '+k)
        pools=a.get('native_all_pools_for_human_comparison',[])
        if v['pool_index']>=len(pools) or pools[v['pool_index']]['pool_index']!=v['pool_index']:
            raise ValueError('No original native pool evidence: '+k)
        selected=pools[v['pool_index']]
        # A single native pool may still contain functions, which require
        # specific human review. Never accept recursive/structural entries.
        if not selected.get('entries') or any(e.get('type') not in ('minecraft:item','minecraft:empty') or e.get('has_children') for e in selected['entries']):
            raise ValueError('Unsafe composite/empty pool: '+k)
        decision=by_key[k]
        if decision.get('source_sha256')!=v['source_sha256'] or decision.get('pool_index')!=v['pool_index']:
            raise ValueError('Review refers to another source pool: '+k)
        if decision.get('reviewed_category_fit') is not True or decision.get('reviewed_native_entries_weights_conditions_functions') is not True or decision.get('approved_for_experimental_build') is not True:
            raise ValueError('Manual source/category approval incomplete: '+k)
        reason=decision.get('reviewer_rationale','')
        if not isinstance(reason,str) or len(reason.strip())<24:
            raise ValueError('Explain each approval and category fit in at least 24 characters: '+k)
    result=copy.deepcopy(base)
    result['grand_treasure']=list(candidates.values())
    if {k:v for k,v in result.items() if k!='grand_treasure'}!={k:v for k,v in base.items() if k!='grand_treasure'}:
        raise ValueError('Unexpected non-Grand campaign policy changes')
    receipt={
        'status':'STAGED_EXPERIMENTAL_SOURCE_REVIEW_ONLY_NOT_COMPILED_NOT_RUNTIME_TESTED',
        'candidate_sha256':sha(candidate_bytes),
        'installed_jar_audit_sha256':sha(audit_bytes),
        'approved_context_count':len(candidates),
        'cross_table_borrowing_count':0,
        'native_loot_tables_overridden':0,
        'unchanged_non_grand_policy':True,
        'native_lootr_multiplayer_tested':False,
        'minecraft_runtime_tested':False,
        'instructions':'Use separate experimental addon source input and rebuild; do not overwrite R2 JAR or declare release accepted.'
    }
    return result,receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=('draft','stage'),required=True)
    p.add_argument('--candidates',type=Path,default=CANDIDATES)
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--approvals',type=Path)
    p.add_argument('--base-policy',type=Path,default=BASE_POLICY)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    # Deliberately restrict output to project-local build, never production source.
    if not args.out.resolve().is_relative_to((ROOT/'build').resolve()):
        raise ValueError('Output must be under the isolated project build/ directory')
    if args.out.exists() or (args.report and args.report.exists()):
        raise ValueError('Never overwrite a prior policy or report')
    c_bytes=args.candidates.read_bytes();a_bytes=args.audit.read_bytes()
    candidates=mappings(json.loads(c_bytes));audit=json.loads(a_bytes)
    if args.mode=='draft':
        if args.report or args.approvals:raise ValueError('Draft needs --out only')
        output=draft(candidates,c_bytes,audit,a_bytes)
    else:
        if not args.approvals or not args.report or args.report.resolve()==args.out.resolve():
            raise ValueError('Stage needs separate --approvals and --report')
        approval=read_json(args.approvals)
        base=read_json(args.base_policy)
        output,receipt=stage(candidates,c_bytes,audit,a_bytes,approval,base)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    if args.report:
        receipt['staged_policy_sha256']=sha(args.out.read_bytes())
        args.report.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(f'{args.mode.upper()} prepared: {args.out}. No R2 policy or live addon changed.')

if __name__=='__main__':
    main()
