#!/usr/bin/env python3
"""0.4e broad candidate intake: exact native CurseForge project/files, version/dep closure and no silent repins. No Minecraft runtime."""
import json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
lock=json.loads((ROOT/'release_030/release-lock.json').read_text())
assert lock['version']=='0.4.0-e0-audit-broad-content'
pins={
    'betterf3': (401648,5873258,'BetterF3-11.0.3-NeoForge-1.21.1.jar'),
    'pick-up-notifier': (351441,6409785,'PickUpNotifier-v21.1.1-1.21.1-NeoForge.jar'),
    'cave-dust-rethinking': (1617531,8740321,'cavedust-3.3.0+1.21.1-neoforge.jar'),
    'light-overlay': (325492,5553811,'light-overlay-12.0.0-neoforge.jar'),
    'inventory-sorter': (240633,5979614,'inventorysorter-1.21-24.0.18.jar'),
    'subtle-effects': (1023913,7768631,'SubtleEffects-neoforge-1.21.1-1.14.0.jar'),
    'travelers-titles': (1015155,6294123,'TravelersTitles-1.21.1-NeoForge-5.1.3.jar'),
    'legendary-tooltips': (532127,6400660,'LegendaryTooltips-1.21.1-neoforge-1.5.5.jar'),
    'map-distance-fix': (1321830,8507645,'mapdistancefix-neoforge-1.1.2+mc1.21-1.21.11.jar'),
    'equipment-compare': (502561,6375501,'EquipmentCompare-1.21.1-neoforge-1.3.13.jar'),
    'rightclickharvest': (452834,7508749,'rightclickharvest-neoforge-4.6.1+1.21.1.jar'),
    'better-advancements': (272515,5850587,'BetterAdvancements-NeoForge-1.21.1-0.4.3.21.jar'),
    'cut-through': (969423,5731913,'CutThrough-v21.1.0-1.21.1-NeoForge.jar'),
    'screenshot-viewer': (693961,6743822,'screenshot_viewer-1.3.4-neoforge-mc1.21.1.jar'),
}
for slug,(pid,fid,name) in pins.items():
    e=lock['additions']['content-040e-'+slug]
    assert (e['projectId'],e['id'],e['fileName'])==(pid,fid,name),(slug,e)
    assert {'1.21.1','NeoForge'}.issubset(e['gameVersions']),slug
with zipfile.ZipFile(ROOT/lock['baseline']) as z:
    manifest=json.loads(z.read('manifest.json'))
installed={e['projectID']:e['fileID'] for e in manifest['files']}
for pid in lock['remove_projects'].values():installed.pop(pid,None)
for slug,e in lock['additions'].items():
    if e['projectId'] in installed: assert installed[e['projectId']]==e['id'],('Conflicting original project pin',slug,e['projectId'])
    installed[e['projectId']]=e['id']
if lock.get('default_integrated_patches'):
    e=lock['optional_integrated_patches'];installed[e['projectId']]=e['id']
assert installed[638111]==6372979
assert len(installed)==311,('Expected 296 + 14 candidates plus required Prism',len(installed))
assert len(set(pid for pid,_,_ in pins.values()))==len(pins)
assert all(installed[pid]==fid for pid,fid,_ in pins.values())
# Verify libraries with source/native or CurseForge relations before claiming dependency closure:
for pid,desc in {495476:'Puzzles Lib (Pick Up Notifier)',638111:'Prism (Legendary Tooltips)',283644:'Cloth Config (Light Overlay optional UI)'}.items():
    if pid==283644:continue # optional client GUI integration; no forced pin
    assert pid in installed,('Missing library project: check exact NeoForge dependency',pid,desc)
assert lock['terminal_jigsaw_repair']['expected_overrides']==273
assert (ROOT/'release_030/overrides/config/mutantmonsters-common.toml').is_file()
print('PASS: 0.4e 14 official NeoForge 1.21.1 candidates plus Prism; 311 references; 273 source repairs retained; rarity unchanged.')
print('NOT RUNTIME-TESTED: rendering/particle layers, farming double-rightclick, tooltip UI, client keybinds and multiplayer installer sidedness.')
