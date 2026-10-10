#!/usr/bin/env python3
"""0.4c user feedback source and next multi-change-build invariant checks. No actual Minecraft runtime."""
from pathlib import Path
import json, re, zipfile
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'release_030'
LOCK=json.loads((BASE/'release-lock.json').read_text())
assert LOCK['version'] in ('0.4.0-c0-ecosystem-feedback','0.4.0-d0-content-first')
assert 'content-040b-galosphere' not in LOCK['additions']
assert all(x.get('projectId')!=631098 for x in LOCK['additions'].values())
assert LOCK['terminal_jigsaw_repair']['expected_overrides']==273
with zipfile.ZipFile(ROOT/LOCK['baseline']) as z:
 m=json.loads(z.read('manifest.json'))
 refs={x['projectID']:x['fileID'] for x in m['files']}
for x in LOCK['remove_projects'].values(): refs.pop(x,None)
for x in LOCK['additions'].values():refs[x['projectId']]=x['id']
if LOCK.get('default_integrated_patches'):
 x=LOCK['optional_integrated_patches'];refs[x['projectId']]=x['id']
assert len(refs)==(295 if LOCK['version']=='0.4.0-d0-content-first' else 288),len(refs)
assert 631098 not in refs
assert refs[835687]==9099893 and refs[714059]==6467772
assert refs[250398]==6368976 and refs[889915]==8909889
root=BASE/'overrides/config/paxi/datapacks/ao_server_rules'
m=json.loads((root/'pack.mcmeta').read_text())
assert m['pack']['pack_format']==48
f=json.loads((root/'data/minecraft/tags/function/load.json').read_text())
assert f=={'values':['ambient_odyssey:server_rules']}
func=(root/'data/ambient_odyssey/function/server_rules.mcfunction').read_text()
cmds=[s.strip() for s in func.splitlines() if s.strip() and not s.startswith('#')]
assert cmds==['gamerule playersSleepingPercentage 30','gamerule doFireTick false','gamerule mobGriefing false'],cmds
audio=(BASE/'overrides/config/waves-common.toml').read_text()
assert 'waveVolume = 0.25' in audio
assert re.search(r'^waveBreakingSoundChance = 120$',audio,re.M)
defaults=(BASE/'overrides/config/defaultoptions/options.txt').read_text()
assert 'soundCategory_weather:0.2' in defaults and 'soundCategory_block:0.4' in defaults and 'soundCategory_ambient:1.0' in defaults
alex=(BASE/'overrides/config/alexsmobs.toml').read_text()
for k in ['gorillaSpawnWeight','flySpawnWeight','cockroachSpawnWeight']:
 assert k+' = 0' in alex,k
print('PASS: inherited 0.4c pack source invariants, Galosphere absent, Better Archaeology present, rules load by Paxi, source-validated audio defaults, Alexs pests disabled, original 273 NBT source patch maintained.')
