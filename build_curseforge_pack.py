#!/usr/bin/env python3
"""Build locked Ambient Odyssey test exports without network resolution."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile
from compile_worldgen_031 import compile_pools
from compile_structure_density_031 import compile_density
from compile_compatibility_031 import compile_compatibility

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'release_030'

def check_path(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError(f'Unsafe archive path: {name}')

def validate(archive, lock, baseline, patches):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None, 'ZIP CRC failure'
        names = z.namelist()
        assert len(names) == len(set(names)), 'Duplicate ZIP paths'
        for name in names: check_path(name)
        assert 'manifest.json' in names and any(n.startswith('overrides/') for n in names)
        assert not any(n.startswith('overrides/mods/') for n in names), 'Bundled third-party mod JAR'
        for name in lock.get('remove_override_paths', []):
            assert name not in names, f'Removed override still present: {name}'
        m = json.loads(z.read('manifest.json'))
        assert m['minecraft']['version'] == '1.21.1'
        assert m['minecraft']['modLoaders'] == [{'id': 'neoforge-21.1.252', 'primary': True}]
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
        for path in [
            compat + 'data/minecraft/tags/worldgen/biome/is_forest.json',
            compat + 'data/minecraft/tags/worldgen/biome/is_plains.json',
            compat + 'data/minecraft/tags/worldgen/biome/is_mountain.json',
            compat + 'data/c/tags/worldgen/biome/is_overworld.json',
            compat + 'data/forge/tags/worldgen/biome/is_forest.json',
            compat + 'data/block_factorys_bosses/tags/worldgen/biome/dragon_tower.json',
            compat + 'data/dungeons_arise/tags/worldgen/biome/has_structure/small_prairie_house_biomes.json',
        ]:
            assert path in names, path
    return m

def build(patches=False, output=None):
    compile_pools()
    compile_density()
    compile_compatibility()
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
        assert {'1.21.1', 'NeoForge'}.issubset(e['gameVersions']), slug
        pid, fid = e['projectId'], e['id']
        if pid in files and files[pid] != fid: raise ValueError(f'Unapproved update: {slug}')
        files[pid] = fid
    manifest['version'] = lock['version'] + ('-integrated-patches' if patches and not lock.get('default_integrated_patches', False) else '')
    manifest['name'] = 'Ambient Odyssey ' + manifest['version']
    manifest['overrides'] = 'overrides'
    manifest['files'] = [{'projectID': pid, 'fileID': fid, 'required': True} for pid, fid in sorted(files.items())]
    for p in sorted((RELEASE / 'overrides').rglob('*')):
        if p.is_file(): entries['overrides/' + p.relative_to(RELEASE / 'overrides').as_posix()] = p.read_bytes()
    for name in ['CHANGELOG.md', 'TESTING-0.3.1.md', 'STRUCTURE-DENSITY-TEST1.md',
                 'BIOME-COMPATIBILITY-TEST2.md']:
        p = ROOT / name
        if p.exists(): entries['overrides/' + name] = p.read_bytes()
    for name in list(entries):
        if name.startswith('overrides/') and ('BUILD_NOTES' in name or 'build_notes' in name): del entries[name]
    for name in lock.get('remove_override_paths', []):
        check_path(name)
        entries.pop(name, None)
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
    validate(output, lock, baseline, patches)
    print(f'{output}: {len(files)} locked projects, {output.stat().st_size:,} bytes, SHA256 {hashlib.sha256(output.read_bytes()).hexdigest()}')
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrated-patches', action='store_true')
    parser.add_argument('--output')
    args = parser.parse_args()
    build(args.integrated_patches, args.output)
