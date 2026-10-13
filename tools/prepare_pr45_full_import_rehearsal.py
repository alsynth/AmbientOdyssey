"""Materialize a private import for native rehearsal using hash-verified cached downloads."""
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def digest(p, algorithm='sha256'): return hashlib.new(algorithm, p.read_bytes()).hexdigest()
def prepare(pack, frozen, celestisynth, target):
    target = target.resolve(); target.relative_to((ROOT / 'build').resolve())
    if target.exists(): raise RuntimeError('Refusing to overwrite a rehearsal')
    with zipfile.ZipFile(pack) as archive:
        if archive.testzip(): raise RuntimeError('Archive CRC failure')
        inputs = json.loads(archive.read('overrides/AO_TEST_NOTES/FULL_IMPORT_INPUTS.json'))
        if inputs['expected_physical_mod_jars'] != 338: raise RuntimeError('Unexpected roster')
        target.mkdir(parents=True)
        for name in archive.namelist():
            if not name.startswith('overrides/') or name.endswith('/'): continue
            out = (target / name[len('overrides/'):]).resolve(); out.relative_to(target)
            out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(archive.read(name))
    for folder in ('resourcepacks', 'shaderpacks'):
        if (frozen / folder).is_dir(): shutil.copytree(frozen / folder, target / folder, dirs_exist_ok=True)
    for row in inputs['roster']:
        if row['kind'] != 'mod': continue
        source = celestisynth if row['projectID'] == 1672331 else frozen / 'mods' / row['name']
        if digest(source, 'sha1') != row['sha1']: raise RuntimeError('Cached download hash mismatch: ' + row['name'])
        shutil.copy2(source, target / 'mods' / row['name'])
    jars = {p.name: digest(p) for p in (target / 'mods').glob('*.jar')}
    if len(jars) != 338: raise RuntimeError('Incorrect materialized physical roster')
    for name, value in inputs['bundled_hashes'].items():
        if jars[name] != value: raise RuntimeError('Bundled mod mismatch')
    snapshot = json.loads((frozen / 'PR45_SNAPSHOT.json').read_text())
    snapshot.update({'jar_hashes': jars, 'physical_jars': len(jars), 'archive_sha256': digest(pack),
                     'runtime_overlay': 'EXACT_FULL_IMPORT', 'instrumentation_mod_included': False,
                     'client_runtime': 'NOT_RUN', 'added_since_pr45': snapshot['added_since_pr45'] + [celestisynth.name]})
    shutil.copytree(frozen / 'saves/pr45-original-save-copy', target / 'saves/pr45-original-save-copy')
    checks = json.loads((ROOT / 'docs/balance/pr45-acceptance-evidence/RUNTIME_CHECK_INPUT.json').read_text())
    with zipfile.ZipFile(celestisynth) as z:
        lang = json.loads(z.read('assets/celestisynth/lang/en_us.json'))
        checks['arena_entity_ids'] = sorted(set(checks['arena_entity_ids']) | {'celestisynth:' + k.split('.', 2)[2] for k in lang if k.startswith('entity.celestisynth.')})
    for name, data in [('PR45_SNAPSHOT.json', snapshot), ('PR45_CHECK_INPUT.json', checks)]:
        (target / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'physical_mods': len(jars), 'archive_sha256': digest(pack), 'client_runtime': 'NOT_RUN'}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('pack', 'frozen', 'celestisynth', 'target'): p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args(); prepare(a.pack, a.frozen, a.celestisynth, a.target)
