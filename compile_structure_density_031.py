#!/usr/bin/env python3
"""Compile the editable AO Structure Test 5 placement plan deterministically."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'release_030'


def read_config(path):
    # These generated placement files use quoted JSON keys plus comments.
    text = re.sub(r'/\*.*?\*/|//[^\n]*', '', path.read_text(), flags=re.S)
    return json.loads(re.sub(r',\s*([}\]])', r'\1', text))


def compile_density():
    plan_path = RELEASE / 'structure-density.json'
    if not plan_path.exists():
        return
    plan = json.loads(plan_path.read_text())
    config_root = RELEASE / 'overrides/config'
    count = 0
    for file in plan['placement_configs']:
        path = config_root / file['path']
        config = read_config(path)
        for key, change in file['sets'].items():
            assert key in config, (file['path'], key)
            new = change['after']
            assert 0 <= new['separation'] < new['spacing'], (file['path'], key)
            if 'frequency' in new:
                assert 0 < new['frequency'] <= 1, (file['path'], key)
            config[key].update(new)
            count += 1
        path.write_text('/* Ambient Odyssey: Structure Test 5 placement. */\n' +
                        json.dumps(config, indent=2) + '\n')
    moog_path = config_root / 'moogs_structures.json'
    moog = json.loads(moog_path.read_text())
    moog['frequency'] = plan['moogs_frequency']
    moog_path.write_text(json.dumps(moog, indent=2) + '\n')
    sets_root = config_root / 'paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set'
    # This pack is compiler-owned. Delete obsolete sets/definitions so Test 3/4
    # grids cannot survive a source edit or a second compilation.
    pack = config_root / 'paxi/datapacks/ao_structure_density'
    if (pack / 'data').exists():
        shutil.rmtree(pack / 'data')
    sets_root.mkdir(parents=True, exist_ok=True)
    for entry in plan['extra_sets']:
        namespace, name = entry['id'].split(':', 1)
        assert namespace == 'ambient_odyssey' and re.fullmatch(r'[a-z0-9_]+', name)
        placement = entry['placement']
        assert 0 <= placement['separation'] < placement['spacing'], entry['id']
        payload = {'structures': entry['structures'], 'placement': placement}
        (sets_root / (name + '.json')).write_text(json.dumps(payload, indent=2) + '\n')
    for category, entries in plan.get('resources', {}).items():
        assert category in {'worldgen/structure', 'worldgen/structure_set',
                            'tags/worldgen/structure', 'tags/worldgen/structure_set'}
        for identifier, payload in entries.items():
            namespace, name = identifier.split(':', 1)
            assert re.fullmatch(r'[a-z0-9_/.-]+', name) and '..' not in name
            path = pack / 'data' / namespace / category / (name + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2) + '\n')
    for file in plan.get('toggle_configs', []):
        path = config_root / file['path']
        config = read_config(path)
        for key, enabled in file['values'].items():
            parts = key.split('/')
            target = config
            for part in parts[:-1]:
                target = target[part]
            assert parts[-1] in target, key
            target[parts[-1]] = enabled
        path.write_text('/* Ambient Odyssey: Structure Test 5 toggles. */\n' +
                        json.dumps(config, indent=2) + '\n')
    (pack / 'pack.mcmeta').write_text(json.dumps({'pack': {'pack_format': 48,
        'description': 'Ambient Odyssey: Structure Test 5 independent placement and safeguards'}}, indent=2) + '\n')
    print(f'Structure density: {count} placement entries, '
          f'{len(plan["moogs_frequency"]["per_structure"])} Moog set multipliers')
    return plan


if __name__ == '__main__':
    compile_density()
