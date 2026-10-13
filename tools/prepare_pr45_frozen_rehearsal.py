"""Prepare another rehearsal from a frozen snapshot without rereading the live profile."""
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def prepare(source: Path, target: Path, rollback: bool):
    source = source.resolve(); target = target.resolve()
    source.relative_to((ROOT / 'build').resolve()); target.relative_to((ROOT / 'build').resolve())
    if target.exists(): raise RuntimeError('Refusing to replace an existing rehearsal')
    snapshot = json.loads((source / 'PR45_SNAPSHOT.json').read_text(encoding='utf-8'))
    for name, expected in snapshot['jar_hashes'].items():
        if hashlib.sha256((source / 'mods' / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Frozen JAR hash changed: ' + name)
    target.mkdir(parents=True)
    for name in ('config', 'defaultconfigs', 'resourcepacks', 'shaderpacks', 'kubejs', 'scripts', 'pr45-rollback'):
        if (source / name).is_dir(): shutil.copytree(source / name, target / name)
    (target / 'mods').mkdir()
    for name in snapshot['jar_hashes']: shutil.copy2(source / 'mods' / name, target / 'mods' / name)
    if (source / 'options.txt').exists(): shutil.copy2(source / 'options.txt', target / 'options.txt')
    shutil.copytree(source / 'saves/pr45-original-save-copy', target / 'saves/pr45-original-save-copy')
    overlay = ROOT / 'experiments/structure-difficulty-v3' / ('rollback' if rollback else 'candidate') / 'config/dungeon_difficulty/difficulty_v2.json'
    shutil.copy2(overlay, target / 'config/dungeon_difficulty/difficulty_v2.json')
    checks = json.loads((source / 'PR45_CHECK_INPUT.json').read_text(encoding='utf-8'))
    checks['run_ordinary_tests'] = not rollback
    structures = set(checks['structure_ids']); entities = set(checks['arena_entity_ids'])
    resources = {(r['kind'], r['id']): r for r in checks['resource_checks']}
    holds = []
    for name in snapshot['added_since_pr45']:
        with zipfile.ZipFile(source / 'mods' / name) as archive:
            for path in archive.namelist():
                parts = path.split('/')
                if len(parts) < 5 or parts[0] != 'data' or parts[2] != 'worldgen' or not path.endswith('.json'): continue
                kind = 'worldgen/' + parts[3]
                if parts[3] not in ('structure', 'structure_set', 'template_pool'): continue
                identifier = parts[1] + ':' + '/'.join(parts[4:])[:-5]
                data = archive.read(path)
                provider = {'provider': name, 'sha256': hashlib.sha256(data).hexdigest()}
                row = resources.setdefault((kind, identifier), {'kind': kind, 'id': identifier, 'providers': []})
                if provider not in row['providers']: row['providers'].append(provider)
                if parts[3] == 'structure':
                    structures.add(identifier)
                    holds.append({'id': identifier, 'provider': name, 'tier': None, 'status': 'SOURCE_VERIFIED_HOLD_UNASSIGNED; NBT/natural encounter audit pending'})
                    definition = json.loads(data)
                    for group in definition.get('spawn_overrides', {}).values():
                        entities.update(r['type'] for r in group.get('spawns', []))
    checks['structure_ids'] = sorted(structures); checks['arena_entity_ids'] = sorted(entities)
    # Read-only T3/T5 feasibility evidence; no loot override is installed.
    for name in snapshot['jar_hashes']:
        if not name.startswith('DungeonsArise-'): continue
        with zipfile.ZipFile(source / 'mods' / name) as archive:
            for path in archive.namelist():
                if not path.endswith('.json') or not path.startswith(('data/dungeons_arise/loot_table/chests/illager_fort/', 'data/dungeons_arise/loot_table/chests/foundry/')): continue
                identifier = 'dungeons_arise:' + path.split('/loot_table/', 1)[1][:-5]
                resources[('loot_table', identifier)] = {'kind': 'loot_table', 'id': identifier, 'providers': [{'provider': name, 'sha256': hashlib.sha256(archive.read(path)).hexdigest()}]}
    checks['resource_checks'] = list(resources.values())
    snapshot['runtime_overlay'] = 'ORIGINAL_ROLLBACK_CONFIG' if rollback else 'PR45_CANDIDATE_CONFIG'
    snapshot['actual_overlay_sha256'] = hashlib.sha256(overlay.read_bytes()).hexdigest()
    snapshot['frozen_source'] = source.name
    for name, data in [('PR45_CHECK_INPUT.json', checks), ('PR45_SNAPSHOT.json', snapshot), ('NEW_STRUCTURE_HOLDS.json', holds)]:
        (target / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'target': target.name, 'physical_jars': len(snapshot['jar_hashes']), 'rollback': rollback, 'additional_structure_holds': holds}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True); p.add_argument('--target', type=Path, required=True)
    p.add_argument('--rollback', action='store_true')
    a = p.parse_args(); prepare(a.source, a.target, a.rollback)
