"""Trace Eternal Nether's new structures through native pools and NBT without assigning tiers."""
import argparse, hashlib, json, zipfile
from collections import deque
from pathlib import Path
from audit_encounter_nbt_041 import load_nbt, examine, plain, palette_names

EXPECTED = '9680efb45ec51250da820b8d525ab739fe0210458651ea87f13c3de9b2691a93'
def identifier(path, kind):
    bits = path.split('/'); return bits[1] + ':' + path.split('/' + kind + '/', 1)[1].rsplit('.', 1)[0]
def values(tree, key):
    if isinstance(tree, dict):
        for k, v in tree.items():
            if k == key and isinstance(v, str): yield v
            yield from values(v, key)
    elif isinstance(tree, list):
        for item in tree: yield from values(item, key)
def audit(jar, output):
    if hashlib.sha256(jar.read_bytes()).hexdigest() != EXPECTED: raise RuntimeError('Unexpected Eternal Nether JAR')
    pools = {}; definitions = {}; templates = {}; features = {}; errors = []
    with zipfile.ZipFile(jar) as archive:
        for name in archive.namelist():
            if '/worldgen/template_pool/' in name and name.endswith('.json'):
                pools[identifier(name, 'worldgen/template_pool')] = json.loads(archive.read(name))
            elif '/worldgen/configured_feature/' in name and name.endswith('.json'):
                features[identifier(name, 'worldgen/configured_feature')] = json.loads(archive.read(name))
            elif '/worldgen/structure/' in name and name.endswith('.json'):
                definitions[identifier(name, 'worldgen/structure')] = json.loads(archive.read(name))
            elif '/structure/' in name and name.endswith('.nbt'):
                try:
                    root = load_nbt(archive.read(name)); tree = plain(root)
                    row = examine(jar.name, name, root)
                    palette = palette_names(root)
                    connectors = sorted({str(b.get('nbt', {}).get('pool')) for b in root.get('blocks', []) if int(b['state']) < len(palette) and palette[int(b['state'])] == 'minecraft:jigsaw' and b.get('nbt', {}).get('pool')})
                    embedded = sorted({str(e.get('nbt', {}).get('id')) for e in root.get('entities', []) if e.get('nbt', {}).get('id')})
                    row.update({'jigsaw_pool_refs': connectors, 'embedded_entity_ids': embedded, 'loot_table_refs': sorted(set(values(tree, 'LootTable'))), 'size': [int(n) for n in root.get('size', [])]})
                    templates[identifier(name, 'structure')] = row
                except Exception as e: errors.append({'path': name, 'error': str(e)})
    structures = []
    for id_, definition in definitions.items():
        queue = deque([definition['start_pool']]); reached_pools = set(); reached_templates = set(); reached_features = set(); unresolved_pools = set(); unresolved_templates = set()
        while queue:
            pool_id = queue.popleft()
            if pool_id in reached_pools or pool_id == 'minecraft:empty': continue
            reached_pools.add(pool_id)
            pool = pools.get(pool_id)
            if pool is None: unresolved_pools.add(pool_id); continue
            queue.append(pool.get('fallback', 'minecraft:empty'))
            reached_features.update(values(pool.get('elements', []), 'feature'))
            for location in values(pool.get('elements', []), 'location'):
                if location in reached_templates: continue
                reached_templates.add(location); template = templates.get(location)
                if template is None: unresolved_templates.add(location); continue
                queue.extend(template['jigsaw_pool_refs'])
        rows = [templates[t] for t in reached_templates if t in templates]
        structures.append({'structure_id': id_, 'tier': None, 'status': 'SOURCE_VERIFIED_GRAPH; HOLD_UNASSIGNED; NOT_NATURAL_GENERATION_OR_COMBAT_TESTED',
                           'definition': definition, 'reachable_pools': sorted(reached_pools), 'reachable_templates': sorted(reached_templates),
                           'configured_features': {f: features.get(f) for f in sorted(reached_features)},
                           'unresolved_feature_refs': sorted(reached_features - features.keys()),
                           'unresolved_pool_refs': sorted(unresolved_pools), 'unresolved_template_refs': sorted(unresolved_templates),
                           'spawner_blocks': sum(r['mob_spawners'] for r in rows), 'trial_spawners': sum(r['trial_spawners'] for r in rows),
                           'vaults': sum(r['vaults'] for r in rows), 'equipment_indicators': sum(r['equipped_mob_or_spawner_indicators'] for r in rows),
                           'spawner_entity_ids': sorted({v for r in rows for v in r['spawner_entity_ids'].split(' | ') if v}),
                           'embedded_entity_ids': sorted({v for r in rows for v in r['embedded_entity_ids']}),
                           'loot_table_refs': sorted({v for r in rows for v in r['loot_table_refs']})})
    report = {'jar': jar.name, 'sha256': EXPECTED, 'templates_decoded': len(templates), 'template_errors': errors,
              'pool_count': len(pools), 'structure_count': len(definitions), 'structures': structures,
              'templates': templates, 'native_code_spawns_audited': False, 'runtime_generation_tested': False,
              'pool_graph_limit': 'Syntactic native resource reachability, not proof of weighted selection, processors, assembly, boss initialization or loot execution.'}
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('templates_decoded', 'template_errors', 'pool_count', 'structure_count')}, indent=2))
    print(json.dumps([{k: r[k] for k in ('structure_id', 'spawner_blocks', 'trial_spawners', 'equipment_indicators', 'spawner_entity_ids', 'embedded_entity_ids', 'unresolved_pool_refs', 'unresolved_template_refs')} for r in structures], indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--jar', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); audit(a.jar, a.output)
