#!/usr/bin/env python3
"""AO 0.4.0-a *trial-only* mod-pin and frozen-worldgen provenance checks."""
import gzip,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LOCK=json.loads((ROOT/'release_030/release-lock.json').read_text())
EXPECTED={
  'content-040a-controlling':(250398,6368976,'Controlling-neoforge-1.21.1-19.0.5.jar'),
  'content-040a-ftb-xmod-compat':(889915,8909889,'ftb-xmod-compat-neoforge-21.1.12.jar'),
}
assert LOCK['version']=='0.4.0-a0-qol-quest-trial'
for slug,(project,fid,filename) in EXPECTED.items():
    p=LOCK['additions'][slug]
    assert p['projectId']==project and p['id']==fid and p['fileName']==filename,p
    assert set(('1.21.1','NeoForge')).issubset(set(p['gameVersions']))
assert len({v['projectId'] for v in LOCK['additions'].values()})==len(LOCK['additions'])
assert LOCK['minecraft']['version']=='1.21.1' if 'minecraft' in LOCK else True
assert LOCK['terminal_jigsaw_repair']['expected_overrides']==273
with zipfile.ZipFile(ROOT/LOCK['baseline']) as z:
    base=json.loads(z.read('manifest.json'))
    pins={i['projectID']:i['fileID'] for i in base['files']}
for k in LOCK['remove_projects'].values():pins.pop(k,None)
for a in LOCK['additions'].values():pins[a['projectId']]=a['id']
if LOCK.get('default_integrated_patches',False):
    a=LOCK['optional_integrated_patches']
    pins[a['projectId']]=a['id']
assert len(pins)==269,len(pins)
assert pins[250398]==6368976 and pins[889915]==8909889
assert pins[1713723]==8988949 and pins[1385782]==7227735
index=json.loads(gzip.decompress((ROOT/'release_030/evidence/jar-resource-index-test6.json.gz').read_bytes()))
names=' '.join(a['file'] for a in index['jars']).lower()
for key in ('searchables','ftb','jei'):
    assert key in names,key
print('PASS: +2 exact NeoForge 1.21.1 releases, 269 CF projects, baseline deps remain, 273 native pool repairs.')
print('No Minecraft runtime was run; no new content mod or resource pack is included in this first test.')
