"""Build a complete private CurseForge import from the reconciled frozen profile."""
import argparse, hashlib, html, json, zipfile
from pathlib import Path
from package_v048_ui_fix import archive

ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = '8643e31b8f086dfde6c9729643ac5b77c692edb38ac000e7186a767b996c67a9'
CELESTI_SHA = '03225d0ac3789f8cd1df90df1793f080ab36c4c1143a4f15b622f88bb41bd9de'

def digest(path, algorithm='sha256'): return hashlib.new(algorithm, path.read_bytes()).hexdigest()
def build(base, metadata, frozen, celestisynth, output):
    if digest(base) != BASE_SHA: raise RuntimeError('Unexpected complete v049 export')
    if digest(celestisynth) != CELESTI_SHA: raise RuntimeError('Unexpected Celestisynth artifact')
    snapshot = json.loads((frozen / 'PR45_SNAPSHOT.json').read_text(encoding='utf-8'))
    if len(snapshot['jar_hashes']) != 337: raise RuntimeError('Requires frozen reconciled 337-JAR context')
    profile = json.loads(metadata.read_text(encoding='utf-8-sig'))
    with zipfile.ZipFile(base) as z:
        if z.testzip() or len(z.namelist()) != len(set(z.namelist())): raise RuntimeError('Invalid base ZIP')
        original = {n: z.read(n) for n in z.namelist() if not n.endswith('/')}
    files = dict(original)
    unsafe = lambda n: n.startswith(('/', '\\')) or '..' in Path(n).parts or any(t in n.lower() for t in ('/saves/', '/logs/', '/crash-reports/', 'servers.dat', 'session.lock', 'minecraftinstance.json', 'accounts.json'))
    if any(unsafe(n) for n in files): raise RuntimeError('Personal/runtime content in export')
    bundled = {Path(n).name: n for n in files if n.startswith('overrides/mods/') and n.endswith('.jar')}
    if len(bundled) != 7 or any('probe' in n for n in bundled): raise RuntimeError('Unexpected bundled mods')
    for name, expected in snapshot['jar_hashes'].items():
        if digest(frozen / 'mods' / name) != expected: raise RuntimeError('Frozen mod hash drift: ' + name)
    for name, path in bundled.items():
        if hashlib.sha256(files[path]).hexdigest() != snapshot['jar_hashes'][name]: raise RuntimeError('Bundled mod differs: ' + name)
    resource_hashes = {digest(p, 'sha1') for folder in ('resourcepacks', 'shaderpacks') for p in (frozen / folder).rglob('*') if p.is_file()}
    pins = {}; roster = []; mapped = set()
    for addon in profile['installedAddons']:
        name = addon['fileNameOnDisk']; native = addon['installedFile']
        hashes = {r['type']: r['value'].lower() for r in native['hashes']}
        if name in snapshot['jar_hashes']:
            if digest(frozen / 'mods' / name, 'sha1') != hashes.get(1): raise RuntimeError('CF hash does not match installed mod: ' + name)
            mapped.add(name); kind = 'mod'
        elif hashes.get(1) in resource_hashes: kind = 'resource_or_shader_pack'
        else: raise RuntimeError('Unresolved installed addon: ' + name)
        project = addon['addonID']; file_id = native['id']
        if project in pins: raise RuntimeError('Duplicate project')
        pins[project] = file_id
        roster.append({'projectID': project, 'fileID': file_id, 'name': name, 'kind': kind, 'sha1': hashes[1]})
    if mapped | bundled.keys() != snapshot['jar_hashes'].keys(): raise RuntimeError('Incomplete physical mod mapping')
    if 1672331 in pins: raise RuntimeError('Celestisynth already represented')
    pins[1672331] = 8867800
    roster.append({'projectID': 1672331, 'fileID': 8867800, 'name': celestisynth.name, 'kind': 'mod', 'sha1': digest(celestisynth, 'sha1'), 'sha256': CELESTI_SHA})
    manifest = json.loads(files['manifest.json'])
    if manifest['minecraft']['version'] != '1.21.1' or manifest['minecraft']['modLoaders'] != [{'id': 'neoforge-21.1.252', 'primary': True}]: raise RuntimeError('Unexpected loader')
    old_pins = {r['projectID']: r['fileID'] for r in manifest['files']}
    manifest['name'] = 'Ambient Odyssey v0.4.9.1 - Structure Difficulty + Celestisynth TEST'
    manifest['version'] = '0.4.9.1-pr45-celestisynth-test'
    manifest['files'] = [{'projectID': p, 'fileID': f, 'required': True} for p, f in sorted(pins.items())]
    manifest['manifestType'] = 'minecraftModpack'; manifest['manifestVersion'] = 1; manifest['overrides'] = 'overrides'
    files['manifest.json'] = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode()
    changed = {'manifest.json', 'modlist.html'}
    for name in ('particular-common.toml', 'alexsmobs.toml'):
        target = 'overrides/config/' + name
        expected = (ROOT / 'docs/performance/v049-followup' / name).read_bytes()
        candidate = (ROOT / 'release_030' / target).read_bytes()
        if files[target] not in (expected, candidate): raise RuntimeError('Unexpected visual/ecology config: ' + name)
        files['overrides/AO_TEST_NOTES/rollback/' + name] = files[target]
        files[target] = candidate; changed.add(target)
    dd = 'overrides/config/dungeon_difficulty/difficulty_v2.json'
    rollback = (ROOT / 'experiments/structure-difficulty-v3/rollback/config/dungeon_difficulty/difficulty_v2.json').read_bytes()
    if json.loads(files[dd]) != json.loads(rollback): raise RuntimeError('Unexpected base difficulty config')
    files['overrides/AO_TEST_NOTES/rollback/dungeon_difficulty/difficulty_v2.json'] = rollback
    files[dd] = (ROOT / 'experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json').read_bytes(); changed.add(dd)
    for name in ('armoredfoes-server.toml', 'fantasticwings-server.toml', 'overflowingbars-client.toml', 'skeletonaifix-server.toml'):
        files['overrides/config/' + name] = (frozen / 'config' / name).read_bytes()
    files['modlist.html'] = ('<!doctype html><meta charset="utf-8"><title>Ambient Odyssey experimental roster</title><ul>' + ''.join('<li>' + html.escape(r['name']) + ' — CF ' + str(r['projectID']) + ':' + str(r['fileID']) + '</li>' for r in roster) + '</ul>').encode()
    report = {'kind': 'FULL_PRIVATE_CURSEFORGE_EXPERIMENTAL_IMPORT', 'base_sha256': BASE_SHA,
              'cf_download_pins': len(pins), 'cf_mod_pins': sum(r['kind'] == 'mod' for r in roster),
              'resource_shader_pins': sum(r['kind'] != 'mod' for r in roster), 'bundled_custom_mods': len(bundled),
              'expected_physical_mod_jars': len(snapshot['jar_hashes']) + 1,
              'added_vs_export': [r for r in roster if r['projectID'] not in old_pins],
              'updated_vs_export': [r for r in roster if r['projectID'] in old_pins and r['fileID'] != old_pins[r['projectID']]],
              'roster': roster, 'candidate_sha256': hashlib.sha256(files[dd]).hexdigest(),
              'bundled_hashes': {n: snapshot['jar_hashes'][n] for n in sorted(bundled)},
              'original_quest_manual_worldgen_and_other_payload_preserved': True,
              'saves_accounts_logs_test_probes_included': False,
              'curseforge_ui_import_tested': False, 'celestisynth_runtime_tested': False, 'full_acceptance_complete': False}
    notes = '''Import this ZIP as a NEW profile in CurseForge: My Modpacks > Create Custom Profile > Import.
The importer downloads the exact official mods and resource/shader packs from the manifest.
Seven inherited private custom mods are included in overrides/mods. No previous profile is needed.
Minecraft 1.21.1, NeoForge 21.1.252; recommended client memory 10 GB on the owner's 32 GB machine.
Includes the reconciled five additions, four previously local Ars integrations, Remnant Bosses 2.7.0,
Celestisynth 1.3.9, existing client performance settings, visual/ecology tuning and the 53-rule DD pilot.
Celestisynth dependencies were statically verified. The prior 337-mod client and controlled DD rules passed;
this 338-mod import is experimental until its own loading/combat/dimension tests finish.
Elite stacking cap/exclusion remains unresolved. Natural encounters, dedicated server and multiplayer remain pending.
The inherited Simply More stun/target-dummy crash and requested flashing fixes are not repaired in this build.
No new loot/quest gates or automatic tier assignments for Eternal Nether are enabled.
The unchanged 52 quests and 32-page manual remain. Original difficulty and two performance configs are
under AO_TEST_NOTES/rollback; close Minecraft before restoring them to their corresponding config paths.
No worlds, accounts, server lists, logs or test probes are shipped.
'''
    files['overrides/AO_TEST_NOTES/READ_FIRST_STRUCTURE_CELESTISYNTH.txt'] = notes.encode()
    files['overrides/AO_TEST_NOTES/FULL_IMPORT_INPUTS.json'] = (json.dumps(report, indent=2) + '\n').encode()
    for n, data in original.items():
        if n not in changed and files[n] != data: raise RuntimeError('Unintended payload delta: ' + n)
    quests = [n for n in files if n.startswith('overrides/config/questlog/quests/') and n.endswith('.json')]
    if len(quests) != 52: raise RuntimeError('Quest count changed: ' + str(len(quests)))
    if any(unsafe(n) for n in files): raise RuntimeError('Unsafe output content')
    report['output_sha256'] = archive(output, files)
    output.with_suffix('.inputs.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('roster', 'added_vs_export', 'updated_vs_export', 'bundled_hashes')}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('base', 'metadata', 'frozen', 'celestisynth', 'output'): p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args(); build(a.base, a.metadata, a.frozen, a.celestisynth, a.output)
