#!/usr/bin/env python3
"""0.4d seven-project content-wave source and dependency-closure gate. No Minecraft runtime."""
import json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
lock=json.loads((ROOT/'release_030/release-lock.json').read_text())
assert lock['version'] in ('0.4.0-d0-content-first','0.4.0-e0-audit-broad-content'), lock['version']
selected={
  'mutant-monsters':(852665,7232511),
  'illager-invasion':(891324,6492670),
  'chipped':(456956,5813117),
  'handcrafted':(538214,6330030),
  'dusty-decorations':(843344,7917189),
  'night-lights':(1199355,8555615),
  'apothic-combat':(986982,6105085),
}
for slug,(pid,fid) in selected.items():
    e=lock['additions']['content-040d-'+slug]
    assert (e['projectId'],e['id'])==(pid,fid),slug
    assert {'1.21.1','NeoForge'}.issubset(e['gameVersions']),slug
with zipfile.ZipFile(ROOT/lock['baseline']) as z:
    m=json.loads(z.read('manifest.json'))
pins={x['projectID']:x['fileID'] for x in m['files']}
for pid in lock['remove_projects'].values():pins.pop(pid,None)
previous=set(pins)
for e in lock['additions'].values():
    old=pins.get(e['projectId'])
    assert old is None or old==e['id'],('Existing baseline project version conflict',e['projectId'],old,e['id'])
    pins[e['projectId']]=e['id']
if lock.get('default_integrated_patches'):
    e=lock['optional_integrated_patches']
    pins[e['projectId']]=e['id']
assert len(pins)==(311 if lock['version']=='0.4.0-e0-audit-broad-content' else 296),(len(pins),'Expected 288 previous +7 content projects +Athena')
for _,(pid,fid) in selected.items():assert pins[pid]==fid
assert pins[841890]==8061947, 'Athena must be the source-verified NeoForge 4.0.6'
# Upstream Mutant Monsters CommonConfig fields map to four snake_case TOML keys.
expected = {'mutant_creeper_spawn_weight', 'mutant_enderman_spawn_weight', 'mutant_skeleton_spawn_weight', 'mutant_zombie_spawn_weight'}
raw = (ROOT/'release_030/overrides/config/mutantmonsters-common.toml').read_text()
lines = [s.strip() for s in raw.splitlines() if s.strip() and not s.lstrip().startswith('#')]
values = {s.split('=',1)[0].strip(): float(s.split('=',1)[1].strip()) for s in lines}
assert set(values)==expected, values
assert all(v==0.01 for v in values.values()), values
assert lock['terminal_jigsaw_repair']['expected_overrides']==273
# Required library projects may be inherited from original AO manifest; never invent
# a replacement pin or claim CurseForge has installed them without verifying identity.
required={
  570073:'Resourceful Lib (Handcrafted, Chipped)',
  841890:'Athena (Chipped)',
  495476:'Puzzles Lib (Illager Invasion, Mutant Monsters)',
  388172:'GeckoLib (Dusty Decorations)',
}
missing={pid:name for pid,name in required.items() if pid not in pins}
if missing:
    raise AssertionError('Dependency closure BLOCKED; identify official 1.21.1 NeoForge pins first: '+str(missing))
print('PASS: 7 new content projects + Athena library; 296 total CF refs, required shared libraries, no baseline repins, 273 native NBT repairs retained.')
print('Minecraft startup, missing runtime-only dependencies, worldgen and entity balance remain unverified.')
