"""Build a full private log-test import from the exact v045.1 consolidated base."""
import argparse
import hashlib
import io
import json
import tomllib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

BASE_SHA = 'fa775ce9ebc3dec4b6c70e50d5c3bf0dab0117c28bb80c3e6bf7b2cdbe0a8364'
PORT_SHA = 'ddec6b79655bc5ff45979e88ef62df7c440646e6d48d6804e3e1476faba32f52'
WET_SHA = 'fc7e84d341339f5ad88d9485ab6316b86edacfc9c1e9caccef2c562d0f3a5b49'
WHALE_SHA = '29af46632fbc066e2e9e761c1718f67e1e91a6e6f2569f8985fb2ded288bb285'
WHALE_PIN = {'projectID': 1272075, 'fileID': 8914201, 'required': True}

def sha(b): return hashlib.sha256(b).hexdigest()

def read_jar(path, expected, modid, version):
    data = path.read_bytes()
    assert sha(data) == expected, f'Wrong exact JAR: {path.name}'
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        meta = tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode())
        assert any(m['modId'] == modid and m['version'] == version for m in meta['mods'])
    return data

def main(a):
    assert sha(a.base.read_bytes()) == BASE_SHA, 'Use the exact v045.1 armor/Q fixed base'
    port = read_jar(a.port, PORT_SHA, 'ao_apotheotic_port', '0.4.8-prototype')
    wet = read_jar(a.wet_sand, WET_SHA, 'ao_wet_sand', '0.0.1-source-prototype')
    read_jar(a.whaleborne, WHALE_SHA, 'whaleborne', '1.21.1-1.2.5')
    with ZipFile(a.base) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        base = {n: z.read(n) for n in z.namelist()}
    manifest = json.loads(base['manifest.json'])
    assert manifest['version'] == '0.4.5.1-affix-trims-questlog-fix-test'
    assert len(manifest['files']) == 330
    pins = {f['projectID']: f['fileID'] for f in manifest['files']}
    assert len(pins) == 330 and WHALE_PIN['projectID'] not in pins
    for project, file in {283644:8463693, 898963:9006294, 313970:8993983, 306770:7730942}.items():
        assert pins.get(project) == file, 'The user prototype dependency pin changed'
    assert not any(n.startswith('overrides/mods/ao-apotheotic-port-') or n.startswith('overrides/mods/ao-wet-sand-') for n in base)
    new = dict(base)
    manifest['files'].append(WHALE_PIN)
    manifest['version'] = '0.4.8-consolidated-whaleborne-log-test'
    manifest['name'] = 'Ambient Odyssey v0.4.8 - Full Pack Gem and Whaleborne TEST'
    manifest['minecraft']['recommendedRam'] = 10240
    new['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    new['overrides/mods/' + a.port.name] = port
    new['overrides/mods/' + a.wet_sand.name] = wet
    # Whaleborne is an official CurseForge reference, not a bundled third-party JAR.
    notes = 'overrides/AO_TEST_NOTES/'
    new[notes+'GEM_PORT_MANUAL_TEST_CHECKLIST.md'] = (a.kit/'MANUAL_TEST_CHECKLIST.md').read_bytes()
    for p in sorted((a.kit/'QA_DATAPACK').rglob('*')):
        if p.is_file(): new[notes+'OPTIONAL_QA_DATAPACK/'+p.relative_to(a.kit/'QA_DATAPACK').as_posix()] = p.read_bytes()
    readme = '''FULL PRIVATE TEST IMPORT — not a finished Apotheotic Additions release.

Import this ZIP as a NEW CurseForge profile. Do not replace a working profile/save.
It contains the full 330-pin tested-source roster plus official Whaleborne 1.2.5 (331 pins),
the exact supplied Apotheotic port 0.4.8 JAR, latest available Wet Sand prototype,
and the verified armor-trim 0.1.1 / Questlog Q 0.1.5 fixes.

Use a NEW throwaway world. First enter it, wait for data loading, and save/quit normally.
Send logs/latest.log from this profile after that run, or the crash report if loading fails.
Look for Failed parsing gems file ao_apotheotic_port and the first caused-by/mixin error.
Natural prototype gem drops remain disabled; use the supplied manual checklist/commands.
The optional QA datapack is reference material here, NOT auto-enabled in gameplay.

Malkuth arena and Mine Cells portal/progression are user-verified; no new changes to them.
Dungeon Crawl spawners will be checked in the next actual playtest/log. Keybind cleanup is later.
The four unwanted recipe routes remain disabled. No loot/balance/quest overhaul is included.
Wet Sand/full-pack multiplayer and Whaleborne taming/widgets/save persistence still need testing.
'''
    new[notes+'READ_FIRST.txt'] = readme.encode()
    if a.log_report:
        new[notes+'GEM_LOG_FINDINGS.txt'] = a.log_report.read_bytes()
    report = {'base_sha256':BASE_SHA,'port_sha256':PORT_SHA,'wet_sand_sha256':WET_SHA,
              'whaleborne_sha256':WHALE_SHA,'whaleborne_pin':WHALE_PIN,'curseforge_pins':331,
              'prototype_finished':False,'unrelated_base_members_preserved':True}
    new[notes+'BUILD_INPUTS.json'] = (json.dumps(report,indent=2)+'\n').encode()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(a.output,'w',compression=ZIP_DEFLATED) as z:
        for name,data in sorted(new.items()):
            assert not name.startswith('/') and '..' not in name.split('/') and '\\' not in name
            info=ZipInfo(name,(2026,10,12,0,0,0));info.compress_type=ZIP_DEFLATED
            z.writestr(info,data)
    with ZipFile(a.output) as z:
        assert z.testzip() is None and set(z.namelist()) == set(new)
        result=json.loads(z.read('manifest.json'))
        assert result['files'][:-1] == json.loads(base['manifest.json'])['files']
        assert len({f['projectID'] for f in result['files']}) == 331
        for name,data in base.items():
            if name != 'manifest.json': assert z.read(name) == data, name
        for name,data in new.items(): assert z.read(name) == data, name
    report['output_sha256'] = sha(a.output.read_bytes())
    report['output_bytes'] = a.output.stat().st_size
    a.output.with_suffix('.inputs.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    for name in ['base','port','wet-sand','whaleborne','kit','output']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--log-report',type=Path)
    main(p.parse_args())
