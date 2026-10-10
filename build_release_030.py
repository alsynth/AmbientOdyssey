#!/usr/bin/env python3
"""Build locked Ambient Odyssey test exports without network resolution."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile
import urllib.request
from compile_worldgen_031 import compile_pools
from compile_structure_density_031 import compile_density
from compile_compatibility_031 import compile_compatibility
from compile_structure_repairs_031 import compile_repairs

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'release_030'

def check_path(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError(f'Unsafe archive path: {name}')

def validate(archive, lock, baseline, patches, private_modrinth=False):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None, 'ZIP CRC failure'
        names = z.namelist()
        assert len(names) == len(set(names)), 'Duplicate ZIP paths'
        for name in names: check_path(name)
        assert 'manifest.json' in names and any(n.startswith('overrides/') for n in names)

        embedded = {n for n in names if n.startswith('overrides/mods/')}
        expected_private = {'overrides/mods/' + a['fileName'] for a in lock.get('private_modrinth_addons', [])}
        assert embedded == (expected_private if private_modrinth else set()), 'Unexpected or missing private JAR'
        if private_modrinth:
            for addon in lock['private_modrinth_addons']:
                blob = z.read('overrides/mods/' + addon['fileName'])
                assert len(blob) == addon['size'], 'Private binary size mismatch'
                assert hashlib.sha1(blob).hexdigest() == addon['sha1'], 'Private binary SHA1 mismatch'
                assert hashlib.sha512(blob).hexdigest() == addon['sha512'], 'Private binary SHA512 mismatch'
        for name in lock.get('remove_override_paths', []):
            assert name not in names, f'Removed override still present: {name}'
        m = json.loads(z.read('manifest.json'))
        assert m['minecraft']['version'] == '1.21.1'
        assert m['minecraft']['modLoaders'] == [{'id': 'neoforge-21.1.252', 'primary': True}]
        assert m['minecraft'].get('recommendedRam') == int(lock.get('recommended_ram_mb', 8192)), 'Recommended RAM mismatch'
        files = {x['projectID']: x['fileID'] for x in m['files']}
        assert len(files) == len(m['files']), 'Duplicate projects'
        removed = set(lock['remove_projects'].values())
        assert removed.isdisjoint(files)
        for pid, fid in baseline.items():
            if pid not in removed: assert files[pid] == fid, f'Unrelated baseline drift: {pid}'
        for entry in lock['additions'].values(): assert files[entry['projectId']] == entry['id']
        optional = lock['optional_integrated_patches']
        assert (optional['projectId'] in files) == (patches or lock.get('default_integrated_patches', False))
        assert 1285600 not in files, 'Incompatible standalone Create/BWG addon'
        moog = json.loads(z.read('overrides/config/moogs_structures.json'))
        assert moog['presets']['mtr']['replace_stronghold'] is False
        assert 'mtr:stronghold' in moog['disabled_structures']
        plan_path = RELEASE / 'structure-density.json'
        if plan_path.exists():
            plan = json.loads(plan_path.read_text())
            assert moog['frequency'] == plan['moogs_frequency']
            for file in plan['placement_configs']:
                raw = z.read('overrides/config/' + file['path']).decode()
                config = json.loads(raw[raw.index('{'):])
                for key, change in file['sets'].items():
                    for field, expected in change['after'].items():
                        assert config[key][field] == expected, (file['path'], key, field)
                    assert 0 <= config[key]['separation'] < config[key]['spacing']
            for entry in plan['extra_sets']:
                name = entry['id'].split(':', 1)[1]
                path = 'overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/' + name + '.json'
                actual = json.loads(z.read(path))
                assert actual == {'structures': entry['structures'], 'placement': entry['placement']}
            seal = json.loads(z.read('overrides/config/paxi/datapacks/ao_content_overrides/data/alexsmobs/loot_table/gameplay/seal_reward.json'))
            assert seal['pools'] == []
        compat = 'overrides/config/paxi/datapacks/ao_compatibility/'
        assert compat + 'pack.mcmeta' in names
        amulet = json.loads(z.read(compat + 'data/curios/tags/item/amulet.json'))
        assert amulet['replace'] is False
        assert 'enigmaticlegacyplus:the_necklace' in amulet['values']
        assert 'enigmaticlegacyplus:enigmatic_amulet_red' in amulet['values']
        scroll = json.loads(z.read(compat + 'data/curios/tags/item/scroll.json'))
        assert scroll['replace'] is False
        assert 'enigmaticlegacyplus:darkest_scroll' in scroll['values']
    # Check the exact resulting archive, not just prepack source JSON.
    if lock.get('terminal_jigsaw_repair', {}).get('enabled', False):
        import gzip
        with zipfile.ZipFile(archive) as z:
            expected = 'overrides/config/paxi/datapacks/ao_worldgen_final_fixes/data/'
            owners = ('adventuredungeons', 'block_factorys_bosses', 'irons_spellbooks')
            overrides = [n for n in z.namelist() if n.startswith(expected)
                         and n[len(expected):].split('/')[0] in owners and n.endswith('.nbt')]
            assert len(overrides) == 271, f'Wrong native terminal NBT count: {len(overrides)}'
            for n in overrides:
                plain = gzip.decompress(z.read(n))
                assert b'minecraft:empty' in plain, n
                assert b'minecraft:' in plain  # Other normal Minecraft references remain.
    return m

def build(patches=False, output=None, private_modrinth=False):
    compile_pools()
    compile_density()
    compile_compatibility()
    compile_repairs()
    lock = json.loads((RELEASE / 'release-lock.json').read_text())
    baseline_path = ROOT / lock['baseline']
    if not baseline_path.is_file(): raise FileNotFoundError(baseline_path)
    with zipfile.ZipFile(baseline_path) as z:
        manifest = json.loads(z.read('manifest.json'))
        baseline = {e['projectID']: e['fileID'] for e in manifest['files']}
        entries = {n: z.read(n) for n in z.namelist() if not n.endswith('/') and n != 'manifest.json'}
    removed = set(lock['remove_projects'].values())
    files = {pid: fid for pid, fid in baseline.items() if pid not in removed}
    additions = dict(lock['additions'])
    if patches or lock.get('default_integrated_patches', False):
        additions['integrated-patches'] = lock['optional_integrated_patches']
    for slug, e in additions.items():
        # CurseForge shader projects are loader-agnostic resources and are installed
        # to shaderpacks by the app; do not falsely require the 'NeoForge' file tag.
        if e.get('contentType') == 'shaders':
            assert {'1.21.1', 'Iris'}.issubset(e['gameVersions']), slug
        else:
            assert {'1.21.1', 'NeoForge'}.issubset(e['gameVersions']) or e.get('version_check_override'), slug
        pid, fid = e['projectId'], e['id']
        if pid in files and files[pid] != fid: raise ValueError(f'Unapproved update: {slug}')
        files[pid] = fid
    manifest['minecraft']['recommendedRam'] = int(lock.get('recommended_ram_mb', 8192))
    manifest['version'] = lock['version'] + ('-integrated-patches' if patches and not lock.get('default_integrated_patches', False) else '')
    manifest['name'] = 'Ambient Odyssey ' + manifest['version']
    manifest['overrides'] = 'overrides'
    manifest['files'] = [{'projectID': pid, 'fileID': fid, 'required': True} for pid, fid in sorted(files.items())]
    for p in sorted((RELEASE / 'overrides').rglob('*')):
        if p.is_file(): entries['overrides/' + p.relative_to(RELEASE / 'overrides').as_posix()] = p.read_bytes()
    for name in ['CHANGELOG.md', 'TESTING-0.3.1.md', 'STRUCTURE-DENSITY-TEST1.md',
                 'BIOME-COMPATIBILITY-TEST2.md', 'STRUCTURE_TEST5_CHANGELOG.md',
                 'STRUCTURE_BIOME_AUDIT.md', 'STRUCTURE_TEST5_VALIDATION.md',
                 'STRUCTURE_TEST5_INSTALL.md', 'TANS_OPEN_FIELD_TUNING_PLAN.md', 'TODO.md']:
        p = ROOT / name
        if p.exists(): entries['overrides/' + name] = p.read_bytes()
    for name in ['README-0.3.1.md', 'MOD_STRUCTURE_SCREENING.md', 'MISSING_JARS.txt',
                 'APPROVED_ADDITION_JARS.txt', 'APPROVED_STRUCTURE_ADDITIONS.csv',
                 'FARMERS_STRUCTURE_CATALOG.csv', 'CODE_GENERATED_PLACEMENT_ROUTES.csv']:
        p = ROOT / name
        if p.exists(): entries['overrides/' + name] = p.read_bytes()
    for name in list(entries):
        if name.startswith('overrides/') and ('BUILD_NOTES' in name or 'build_notes' in name): del entries[name]
    for name in lock.get('remove_override_paths', []):
        check_path(name)
        entries.pop(name, None)

    # Test8.7: derive PRIVATE resource overrides from exact SHA256-pinned native JARs.
    # This is not a blanket missing-pool alias: only validated terminal NBT
    # references are repaired. Source binaries are never republished here.
    if lock.get('terminal_jigsaw_repair', {}).get('enabled', False):
        from compile_terminal_jigsaws_087 import fix_jigsaws
        terminal_entries, terminal_report = fix_jigsaws()
        assert len(terminal_entries) == lock['terminal_jigsaw_repair']['expected_overrides']
        for name, blob in terminal_entries.items():
            check_path(name)
            if name in entries:
                raise ValueError('Existing resource would be overwritten by terminal repair: '+name)
            entries[name] = blob
        assert sum(terminal_report.values()) == 271
    if private_modrinth:
        for addon in lock.get('private_modrinth_addons', []):
            assert addon['url'].startswith('https://cdn.modrinth.com/data/'), 'Unapproved external mod source'
            assert addon['fileName'] == Path(addon['fileName']).name and addon['fileName'].endswith('.jar')
            req = urllib.request.Request(addon['url'], headers={'User-Agent':'AmbientOdyssey-PrivateTestBuilder/1.0'})
            with urllib.request.urlopen(req, timeout=30) as source:
                blob = source.read(addon['size'] + 1)
            if len(blob) != addon['size'] or hashlib.sha1(blob).hexdigest() != addon['sha1'] or hashlib.sha512(blob).hexdigest() != addon['sha512']:
                raise ValueError('Modrinth source hash differs from pinned file: ' + addon['fileName'])
            entries['overrides/mods/' + addon['fileName']] = blob
    entries['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    output = Path(output) if output else ROOT / 'build' / ('Ambient-Odyssey-v' + manifest['version'] + '.zip')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, data in sorted(entries.items()):
            check_path(name)
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0))
            info.create_system = 3  # deterministic ZIP creator on all platforms
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    validate(output, lock, baseline, patches, private_modrinth)
    print(f'{output}: {len(files)} locked projects, {output.stat().st_size:,} bytes, SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}')
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrated-patches', action='store_true')
    parser.add_argument('--output')
    parser.add_argument('--private-modrinth', action='store_true', help='Embed checksum-locked NeoReefRedux in PRIVATE test builds only')
    args = parser.parse_args()
    build(args.integrated_patches, args.output, args.private_modrinth)
