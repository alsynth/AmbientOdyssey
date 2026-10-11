"""Preserve the first five attribute-only gems, with all nine original tiers."""
import argparse
import hashlib
import json
from pathlib import Path
from port_v046_core_attribute_affixes import CATEGORIES, OPERATIONS, UPSTREAM_SHA
import subprocess


def convert(source, destination):
    assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == UPSTREAM_SHA
    rows = []
    language_file = destination / 'assets/ao_apotheotic_port/lang/en_us.json'
    language = json.loads(language_file.read_text(encoding='utf-8'))
    upstream_language = json.loads((source / 'assets/apotheotic_additions/lang/en_us.json').read_text(encoding='utf-8'))
    tiers = ['common', 'uncommon', 'rare', 'epic', 'mythic', 'ancient', 'artifact', 'heirloom', 'esoteric']
    for path in sorted((source / 'data/apotheotic_additions/gems').rglob('*.json')):
        old = json.loads(path.read_text(encoding='utf-8'))
        reasons = []
        if old.get('conditions'): reasons.append('legacy conditions need integration')
        for bonus in old['bonuses']:
            if bonus['type'] != 'apotheosis:attribute': reasons.append('non-attribute bonus needs native implementation')
            elif bonus['attribute'].split(':')[0] not in ('minecraft', 'attributeslib'): reasons.append('external attribute dependency')
            if not set(bonus.get('gem_class', {}).get('types', ['unmapped'])) <= CATEGORIES.keys(): reasons.append('external category dependency')
        relative = path.relative_to(source / 'data/apotheotic_additions/gems').as_posix()
        row = {'source': relative, 'source_json_sha256': hashlib.sha256(json.dumps(old, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
               'status': 'pending' if reasons else 'ported_attribute_gem', 'pending_reasons': sorted(set(reasons)), 'original': old}
        if not reasons:
            minimum = tiers.index(old.get('min_rarity', 'common').split(':')[-1])
            bonuses = []
            for bonus in old['bonuses']:
                bonuses.append({'type': 'ao_apotheotic_port:legacy_attribute',
                    'attribute': bonus['attribute'].replace('attributeslib:', 'apothic_attributes:', 1),
                    'operation': OPERATIONS[bonus['operation']],
                    'gem_class': {'key': bonus['gem_class']['key'], 'types': sorted({CATEGORIES[c] for c in bonus['gem_class']['types']})},
                    'legacy_values': {k.split(':')[-1]: v for k, v in bonus['values'].items()}})
            new = {'type': 'apotheosis:gem', 'weights': {'weight': 0},
                   'min_purity': ['cracked', 'chipped', 'flawed', 'normal', 'flawless', 'perfect'][min(5, minimum)],
                   'unique': old.get('unique', False), 'bonuses': bonuses}
            target = destination / 'data/ao_apotheotic_port/gems' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(new, indent=2) + '\n', encoding='utf-8')
            row['ported_id'] = 'ao_apotheotic_port:' + relative.removesuffix('.json')
            original_key = 'item.apotheosis.gem.apotheotic_additions:' + relative.removesuffix('.json')
            language['item.apotheosis.gem.' + row['ported_id']] = upstream_language[original_key]
        rows.append(row)
    report = {'upstream_commit': UPSTREAM_SHA, 'port_complete': False, 'ready_to_install': False,
              'ported_count': sum(r['status'] == 'ported_attribute_gem' for r in rows), 'gems': rows}
    assert report['ported_count'] == 5 and len(rows) == 71
    target = destination / 'assets/ao_apotheotic_port/core-gem-port-manifest.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    language_file.write_text(json.dumps(language, indent=2) + '\n', encoding='utf-8')
    print('Preserved five gems; 66 pending; all natural weights zero')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    convert(args.source, args.destination)

