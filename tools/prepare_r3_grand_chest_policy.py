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
R2 = ROOT / 'docs/handoffs/loot-update-20261015/grand-treasure-r2-historical.json'
HASH = re.compile(r'^[0-9a-f]{64}$')

def table_resource(table: str) -> str:
    namespace, path = table.split(':', 1)
    return f'data/{namespace}/loot_table/{path}.json'

def produce(source_audit, r2_mappings):
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
            'replaces_structure_wide_borrowing': borrowed,
            'old_r2_bonus_source': old['source_resource'],
            'source_approval': 'NEEDS_INSTALLED_JAR_REVALIDATION',
            'best_pool_category_approval': 'NEEDS_MANUAL_REVIEW',
            'lootr_multiplayer_approval': 'NOT_RUN',
            'bonus_is_additive': 'NEEDS_RUNTIME_PROOF',
        })
    # A valid reviewed candidate never repeats or modifies the base chest.
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
