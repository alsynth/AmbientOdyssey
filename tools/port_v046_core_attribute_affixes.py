"""Convert the first, explicitly bounded native attribute-affix batch.

Preserves min/steps/step directly: Placebo 9.9.2 still accepts that strict
codec. Records every other attribute affix as pending instead of discarding it.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

UPSTREAM_SHA = '822ecf6993ceaada1504e8dd10a8fea727a6235d'
CATEGORIES = {
    'sword': 'apotheosis:melee_weapon', 'heavy_weapon': 'apotheosis:melee_weapon',
    'trident': 'apotheosis:trident', 'bow': 'apotheosis:bow', 'crossbow': 'apotheosis:bow',
    'pickaxe': 'apotheosis:breaker', 'shovel': 'apotheosis:breaker',
    'helmet': 'apotheosis:helmet', 'chestplate': 'apotheosis:chestplate',
    'leggings': 'apotheosis:leggings', 'boots': 'apotheosis:boots', 'shield': 'apotheosis:shield',
}
OPERATIONS = {'ADDITION': 'add_value', 'MULTIPLY_BASE': 'add_multiplied_base', 'MULTIPLY_TOTAL': 'add_multiplied_total'}
RARITIES = {f'apotheotic_additions:{name}': f'ao_apotheotic_port:{name}' for name in ('artifact', 'heirloom', 'esoteric')}


def convert(source, destination):
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == UPSTREAM_SHA, 'Use the pinned, audited upstream revision'
    data_root = source / 'data/apotheotic_additions'
    language_source = json.loads((source / 'assets/apotheotic_additions/lang/en_us.json').read_text(encoding='utf-8'))
    language_file = destination / 'assets/ao_apotheotic_port/lang/en_us.json'
    language = json.loads(language_file.read_text(encoding='utf-8'))
    rows = []
    for path in sorted((data_root / 'affixes').rglob('*.json')):
        old = json.loads(path.read_text(encoding='utf-8'))
        if old.get('type') != 'apotheosis:attribute':
            continue
        relative = path.relative_to(data_root / 'affixes').as_posix()
        reasons = []
        namespace = old['attribute'].split(':', 1)[0]
        if namespace not in ('minecraft', 'attributeslib'):
            reasons.append('requires external attribute integration')
        if not set(old['types']) <= CATEGORIES.keys():
            reasons.append('requires external or unmapped loot categories')
        if not set(old['values']) <= RARITIES.keys():
            reasons.append('requires stock/Ancient rarity mapping decision')
        if old.get('conditions'):
            reasons.append('requires legacy condition/dependency migration')
        if old['operation'] not in OPERATIONS:
            reasons.append('unknown modifier operation')
        for curve in old['values'].values():
            if set(curve) != {'min', 'steps', 'step'} or not isinstance(curve['steps'], int) or curve['steps'] <= 0:
                reasons.append('unverified stepped curve')
                break
        canonical_source = json.dumps(old, sort_keys=True, separators=(',', ':')).encode('utf-8')
        row = {'source': 'affixes/' + relative, 'source_json_sha256': hashlib.sha256(canonical_source).hexdigest(),
               'status': 'pending' if reasons else 'ported_core_attribute', 'pending_reasons': reasons,
               'original_attribute': old['attribute'], 'original_categories': old['types'], 'original_rarities': list(old['values'])}
        if reasons:
            rows.append(row)
            continue
        attribute = old['attribute'].replace('attributeslib:', 'apothic_attributes:', 1)
        new = {'type': 'apotheosis:attribute', 'attribute': attribute, 'operation': OPERATIONS[old['operation']],
               'categories': sorted({CATEGORIES[name] for name in old['types']}),
               'definition': {'affix_type': 'stat', 'exclusive_set': [], 'weights': {'weight': 1, 'quality': 0}},
               'values': {RARITIES[key]: value for key, value in old['values'].items()}}
        target = destination / 'data/ao_apotheotic_port/affixes' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(new, indent=2) + '\n', encoding='utf-8')
        identifier = 'ao_apotheotic_port:' + relative.removesuffix('.json')
        row.update({'ported_id': identifier, 'ported_attribute': attribute, 'categories': new['categories'], 'values': new['values']})
        for suffix in ('', '.suffix'):
            key = 'affix.apotheotic_additions:' + relative.removesuffix('.json') + suffix
            assert key in language_source, 'Missing original affix name: ' + key
            language['affix.' + identifier + suffix] = language_source[key]
        rows.append(row)
    active = [row for row in rows if row['status'] == 'ported_core_attribute']
    assert len(rows) == 118 and len(active) == 25, 'Upstream/core batch inventory drift'
    language_file.write_text(json.dumps(language, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    report = {'upstream': 'https://github.com/Bryce792/ApotheoticAdditions', 'upstream_commit': revision,
              'license': 'AFL-3.0', 'ported_count': len(active), 'pending_count': len(rows) - len(active),
              'port_complete': False, 'ready_to_install': False, 'attribute_affixes': rows}
    output = destination / 'assets/ao_apotheotic_port/core-attribute-port-manifest.json'
    output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return {key: report[key] for key in ('ported_count', 'pending_count', 'port_complete', 'ready_to_install')}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(convert(args.source, args.destination)))
