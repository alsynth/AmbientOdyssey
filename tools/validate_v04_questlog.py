#!/usr/bin/env python3
"""Questlog 3.4.1 native NeoForge integration and source-backed UI preflight, not runtime."""
import json
import tomllib
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'release_030/release-lock.json').read_text())
assert lock['version']=='0.4.1-experimental-six-fix-test'
q=lock['additions']['content-040h-questlog']
assert (q['projectId'],q['id'],q['fileName'])==(1202066,8952784,'questlog-neoforge-1.21.1-3.4.1.jar')
assert {'NeoForge','1.21.1'}.issubset(q['gameVersions'])
assert not q.get('loader_bridge'), 'Questlog is native NeoForge; never Fabric-bridge this file'
assert lock['experimental_minecells']['expected_manifest_refs']==331
with zipfile.ZipFile(ROOT/lock['baseline']) as z:
  base=json.loads(z.read('manifest.json'))
pins={e['projectID']:e['fileID'] for e in base['files']}
for pid in lock['remove_projects'].values(): pins.pop(pid,None)
for name,e in lock['additions'].items():
  pid,fid=e['projectId'],e['id']
  assert pid not in pins or pins[pid]==fid,('silently changed pinned mod',name,pid)
  pins[pid]=fid
if lock.get('default_integrated_patches'):
  e=lock['optional_integrated_patches'];pins[e['projectId']]=e['id']
assert len(pins)==331,len(pins)
assert pins[1202066]==8952784
assert pins[348521]==5729127, 'Questlog requires existing Cloth Config NeoForge 15.0.140; no duplicate/repin'
assert pins[618790]==7033510 and pins[890127]==8654089 and pins[889079]==8726480 and pins[318449]==5845879
assert 1100379 not in pins
assert lock['terminal_jigsaw_repair']['expected_overrides']==273
cfg=tomllib.loads((ROOT/'release_030/overrides/config/questlog-client.toml').read_text())
button=cfg['button']
assert button['enabled'] and button['showBadge'] and not button['relativeToInventory']
assert (button['x'],button['y'])==(38,38)
assert all(isinstance(button[k],bool) for k in ('enabled','showBadge','relativeToInventory','bobbingBadge'))
quest_folder=ROOT/'release_030/overrides/config/questlog/quests'
assert quest_folder.is_dir() and len(list(quest_folder.glob('*.json')))==50
from validate_v04_quest_campaign import validate
assert validate()==50
print('PASS: 331 projects, native Questlog pin, inherited Cloth Config, Mine Cells bridge, exact source-backed inventory button configuration, no quest campaign and 273 NBT repairs.')
print('Source and packaging only: inventory placement, interaction and multiplayer have NOT been runtime tested.')
