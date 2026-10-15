#!/usr/bin/env python3
"""Prepare (never deploy) a per-chest R3 Grand Treasure native-pool candidate.

Reads the historical R2 mapping and its installed-JAR source audit, replacing
the old structure-wide winner with each triggering chest's own audited
candidate. Does not claim that this candidate is the best appropriate reward:
that requires installed native pool review and multiplayer confirmation.

python tools/prepare_r3_grand_chest_policy.py --out build/r3-grand-candidates.json \
    --review build/r3-grand-candidate-review.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/handoffs/loot-update-20261015/chest-source-audit.json'
R2 = ROOT / 'docs/handoffs/loot-update-20261015/grand-treasure-candidates.json'
HASH = re.compile(r'^[0-9a-f]{64}$')
KAYRA_EVIDENCE = ROOT/'docs/handoffs/loot-update-20261015/KEEP_KAYRA_PINNED_SOURCE_POOL_EVIDENCE_20261015.json'
CATEGORY_CHOICES = ROOT/'docs/handoffs/loot-update-20261015/R3_KEEP_KAYRA_SOURCE_GROUNDED_CATEGORY_CHOICES.json'
OTHER_EVIDENCE = ROOT/'docs/handoffs/loot-update-20261015/R3_LAST_THREE_PINNED_NATIVE_SOURCE_VERIFICATION_20261015.json'
OTHER_CHOICES = ROOT/'docs/handoffs/loot-update-20261015/R3_LAST_THREE_NATIVE_CATEGORY_POOL_PROPOSALS_20261015.json'

def table_resource(table: str) -> str:
    namespace, path = table.split(':', 1)
    return f'data/{namespace}/loot_table/{path}.json'

def produce(source_audit, r2_mappings):
    evidence=json.loads(KAYRA_EVIDENCE.read_text(encoding='utf-8'))
    choices=json.loads(CATEGORY_CHOICES.read_text(encoding='utf-8'))
    if (evidence.get('status')!='PINNED_PUBLISHED_JAR_SOURCE_HASHES_MATCH_PREVIOUS_AO_AUDIT_NOT_RUNTIME_ACCEPTED'
        or choices.get('jar_sha256')!=evidence.get('mod_jar_sha256')
        or choices.get('status')!='SOURCE_GROUNDED_CHEST_CATEGORY_SUGGESTIONS_NOT_RUNTIME_APPROVED'):
        raise ValueError('Pinned upstream native evidence cannot establish the category proposal')
    other_evidence=json.loads(OTHER_EVIDENCE.read_text(encoding='utf-8'))
    other_choices=json.loads(OTHER_CHOICES.read_text(encoding='utf-8'))
    if (other_evidence.get('status')!='THREE_PINNED_MOD_JAR_SOURCE_TABLE_HASHES_MATCHED_PRIOR_AO_AUDIT_STATIC_ONLY'
        or other_choices.get('status')!='THREE_THEMATIC_NATIVE_POOL_PROPOSALS_SOURCE_VERIFIED_NOT_RUNTIME_APPROVED'
        or other_choices.get('source')!='docs/handoffs/loot-update-20261015/R3_LAST_THREE_PINNED_NATIVE_SOURCE_VERIFICATION_20261015.json'):
        raise ValueError('Missing genuine upstream source evidence for final-three category choices')
    pool_tables={v['table']:v for v in evidence['review']}
    other_tables={v['table']:v for v in other_evidence['selected_and_other_native_pools']}
    reviewed_choices={}
    for c in choices['candidate_pool_revisions']+other_choices['candidate_pool_revisions']:
        k=(c['structure'],c['table'])
        if k in reviewed_choices:raise ValueError('Duplicate source-grounded category pool suggestion for '+str(k))
        if c.get('approval_status')!='REVIEW_ONLY_NEEDS_EFFECTIVE_DATAPACK_AND_LOOTR_TEST' or c.get('source_verified') is not True:
            raise ValueError('Source-grounded pool incorrectly marked gameplay approved or not source verified: '+str(k))
        if c['native_source']!=table_resource(c['table']):
            raise ValueError('Native pool proposal is not from its own chest table: '+str(k))
        if c['table'] in pool_tables:
            table=pool_tables[c['table']]
            source_hash=table['sha256']
            selected=next((v for v in table['pools'] if v['index']==c['pool_index']),None)
            entries=selected['items'] if selected is not None else []
        else:
            table=other_tables.get(c['table'])
            source_hash=table['native_source_sha256'] if table else None
            selected=next((v for v in table['all_pools'] if v['index']==c['pool_index']),None) if table else None
            entries=selected['entries'] if selected is not None else []
        if source_hash!=c['native_source_sha256'] or not entries or any(v['type'] not in ('minecraft:item','minecraft:empty') for v in entries):
            raise ValueError('Missing or unsafe genuine native chest category pool evidence: '+str(k))
        reviewed_choices[k]=c
    indexed = {}
    for row in source_audit:
        key = (row['structure'], row['table'])
        if key in indexed:
            raise ValueError(f'Duplicate source-audit chest context: {key}')
        indexed[key] = row
    seen = set()
    proposed = []
    review = []
    for old in r2_mappings:
        key = (old['structure'], old['table'])
        if key in seen:
            raise ValueError(f'Duplicate existing R2 Grand Treasure context: {key}')
        seen.add(key)
        src = indexed.get(key)
        if src is None or src.get('status') != 'CANDIDATE_SOURCE_VERIFIED':
            raise ValueError(f'No audited original native candidate for {key}')
        desired = table_resource(old['table'])
        if src.get('resource') != desired:
            raise ValueError(f'Candidate is not the triggering chest original loot table: {key}')
        if src.get('tier') != old.get('tier') or not 3 <= src['tier'] <= 9:
            raise ValueError(f'Tier differs from R2 or is below T3: {key}')
        if old.get('chance') != 0.05:
            raise ValueError(f'The owner-approved 5% chance differs: {key}')
        selected = src.get('selected_pool')
        if not isinstance(selected, int) or isinstance(selected, bool) or selected < 0 or selected >= src.get('pool_count', 0):
            raise ValueError(f'Pool index not verified against table count: {key}')
        expected_hash = src.get('source_sha256','')
        if not HASH.fullmatch(expected_hash):
            raise ValueError(f'Expected source SHA missing: {key}')
        choice=reviewed_choices.get(key)
        if choice:
            if choice['native_source_sha256']!=expected_hash or choice['native_source']!=desired:
                raise ValueError('Category selection differs from actual chest source hash: '+key[1])
            selected=choice['pool_index']
        proposed.append({
            'structure': old['structure'],
            'tier': old['tier'],
            'table': old['table'],
            'source_resource': desired,
            'source_sha256': expected_hash,
            'pool_index': selected,
            'chance': 0.05,
        })
        borrowed = old['source_resource'] != desired
        review.append({
            'structure': old['structure'],
            'chest_table': old['table'],
            'chest_category': old['table'].split('/')[-1],
            'native_source': desired,
            'native_pool_index': selected,
            'native_table_source_hash': expected_hash,
            'native_provider_from_prior_audit': src.get('provider'),
            'pool_selection_basis': 'PINNED_NATIVE_JAR_CATEGORY_TREASURE_CANDIDATE' if choice else 'PREVIOUS_GENERIC_RESOURCE_SCORE_NOT_YET_APPROVED',
            'category_selection_reason': choice['reason'] if choice else 'Same-table generic-value candidate; manual category-fit review required',
            'replaces_structure_wide_borrowing': borrowed,
            'old_r2_bonus_source': old['source_resource'],
            'source_approval': 'NEEDS_INSTALLED_JAR_REVALIDATION',
            'best_pool_category_approval': 'NEEDS_MANUAL_REVIEW',
            'lootr_multiplayer_approval': 'NOT_RUN',
            'bonus_is_additive': 'NEEDS_RUNTIME_PROOF',
        })
    # A valid reviewed candidate never repeats or modifies the base chest.
    if not set(reviewed_choices).issubset(seen):
        raise ValueError('Category-specific choice does not belong to current Grand candidate context set')
    if len(proposed) != len(r2_mappings):
        raise ValueError('Lost or duplicated chest contexts')
    if any(r['source_resource'] != table_resource(r['table']) for r in proposed):
        raise ValueError('Candidate unexpectedly borrows from another table')
    return proposed, review

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit', type=Path, default=AUDIT)
    parser.add_argument('--r2', type=Path, default=R2)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--review', type=Path, required=True)
    args = parser.parse_args()
    if args.out.resolve() == args.review.resolve() or args.out.exists() or args.review.exists():
        raise ValueError('Output files must be different and must not already exist')
    audit = json.loads(args.audit.read_text(encoding='utf-8'))
    r2 = json.loads(args.r2.read_text(encoding='utf-8'))
    proposed, reviews = produce(audit, r2)
    body = {
        'status': 'R3_CANDIDATES_ONLY_NOT_APPROVED_OR_COMPILED',
        'owner_rule': '5% per T3+ eligible chest, exactly one extra appropriate native-pool roll; never replace base loot',
        'r2_grand_context_count': len(r2),
        'r3_candidate_context_count': len(proposed),
        'r2_cross_table_contexts_corrected': sum(r['replaces_structure_wide_borrowing'] for r in reviews),
        'candidates': reviews,
        'not_proof': [
            'The old source audit cannot prove effective currently installed table hash or Paxi precedence.',
            'Pool category fit and best-pool selection require native item and weight examination.',
            'This report cannot establish Lootr individualized rolls or additive Java behavior.',
            'No R2 JAR, compiled policy, or live profile was updated.',
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.review.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(proposed,indent=2)+'\n',encoding='utf-8')
    args.review.write_text(json.dumps(body,indent=2)+'\n',encoding='utf-8')
    print(f'Prepared {len(proposed)} chest-specific source candidates; '
          f'{body["r2_cross_table_contexts_corrected"]} sources changed versus R2. '
          'All are pending review, not enabled.')

if __name__ == '__main__':
    main()
