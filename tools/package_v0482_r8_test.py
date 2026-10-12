"""Replace only the Apotheotic prototype and test notes in the verified UI pack."""
import argparse
import hashlib
import io
import json
import tomllib
from pathlib import Path
from zipfile import ZipFile
from package_v048_ui_fix import archive

BASE_SHA = 'bc581d63cffec94b219b8a59053acbb4506591b8db2abea2779ac4c1f7395e16'
R8_SHA = '05639f00c2905db6f28cac5de6e4076d1f873ffcf80dcad24b48aa19e05af13a'
OLD_SHA = 'ddec6b79655bc5ff45979e88ef62df7c440646e6d48d6804e3e1476faba32f52'
JAR = 'ao-apotheotic-port-prototype-0.4.8-prototype.jar'
NOTES = 'overrides/AO_TEST_NOTES/'


def main(a):
    assert hashlib.sha256(a.base.read_bytes()).hexdigest() == BASE_SHA
    data = a.jar.read_bytes()
    assert hashlib.sha256(data).hexdigest() == R8_SHA
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        meta = tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode('utf-8'))
        assert any(m['modId'] == 'ao_apotheotic_port' and m['version'] == '0.4.8-prototype' for m in meta['mods'])
        resource_count = 0
        for name in z.namelist():
            if name.endswith('.json'):
                json.loads(z.read(name))
                resource_count += 1
    with ZipFile(a.base) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        original = {n: z.read(n) for n in z.namelist()}
    jarpath = 'overrides/mods/' + JAR
    assert hashlib.sha256(original[jarpath]).hexdigest() == OLD_SHA
    full = dict(original)
    full[jarpath] = data
    manifest = json.loads(full['manifest.json'])
    assert len(manifest['files']) == len({f['projectID'] for f in manifest['files']}) == 331
    assert any(f['projectID'] == 1272075 and f['fileID'] == 8914201 for f in manifest['files'])
    manifest['name'] = 'Ambient Odyssey v0.4.8.2 - R8 Full Pack TEST'
    manifest['version'] = '0.4.8.2-r8-full-pack-test'
    full['manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode('utf-8')
    with ZipFile(a.kit) as z:
        assert hashlib.sha256(z.read(jarpath)).hexdigest() == R8_SHA
        full[NOTES+'GEM_PORT_MANUAL_TEST_CHECKLIST.md'] = z.read('MANUAL_TEST_CHECKLIST.md')
        for name in list(full):
            if name.startswith(NOTES+'OPTIONAL_QA_DATAPACK/'):
                del full[name]
        for name in z.namelist():
            if name.startswith('QA_DATAPACK/') and not name.endswith('/'):
                full[NOTES+'OPTIONAL_QA_DATAPACK/'+name[len('QA_DATAPACK/'):]] = z.read(name)
    old = full.pop(NOTES+'GEM_LOG_FINDINGS.txt', None)
    if old:
        full[NOTES+'HISTORICAL_PRE_R8_GEM_LOG_FINDINGS.txt'] = old
    full[NOTES+'READ_FIRST.txt'] = b'''Import this full ZIP as a NEW CurseForge profile.
It includes the exact r8 Apotheotic prototype, Whaleborne, Wet Sand,
armor trims, Questlog placement and the latest tooltip/startup fixes.
The matching r8 build report passed all 30 native GameTests.
Use a throwaway world and GEM_PORT_MANUAL_TEST_CHECKLIST.md for manual checks.
Save normally and retain logs/latest.log. Multiplayer and gameplay need manual testing.
Optional QA datapack files are reference material, not automatically enabled.
Historical pre-r8 findings describe the older JAR, not this build.
'''
    if a.log_report:
        full[NOTES+'R8_FULL_PACK_CHECKS.txt'] = a.log_report.read_bytes()
    for name, payload in original.items():
        if name not in {'manifest.json', jarpath} and not name.startswith(NOTES):
            assert full[name] == payload, name
    assert manifest['files'] == json.loads(original['manifest.json'])['files']
    assert sum(n.startswith('overrides/mods/ao-apotheotic-port-') and n.endswith('.jar') for n in full) == 1
    for name in full:
        assert not name.startswith('/') and '..' not in name.split('/') and '\\' not in name
        assert not (name.startswith('overrides/mods/') and 'probe' in name and name.endswith('.jar'))
    output_sha = archive(a.output, full)
    report = {'base_sha256': BASE_SHA, 'r8_jar_sha256': R8_SHA, 'output_sha256': output_sha,
              'curseforge_pins_unchanged': 331, 'other_bundled_jars_unchanged': True,
              'ui_quests_recipes_worldgen_unchanged': True, 'r8_jar_json_resources_parsed': resource_count}
    a.output.with_suffix('.inputs.json').write_bytes((json.dumps(report, indent=2)+'\n').encode('utf-8'))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['base', 'jar', 'kit', 'output']:
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--log-report', type=Path)
    main(p.parse_args())
