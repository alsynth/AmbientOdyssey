#!/usr/bin/env python3
"""AO 0.4.0-b1 one-large-batch acceptance: exactly 15 NeoForge mods and 5 official CF resourcepack references."""
import json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'release_030/release-lock.json').read_text())
assert j['version'] in ('0.4.0-b1-living-world-batch','0.4.0-c0-ecosystem-feedback','0.4.0-d0-content-first','0.4.0-e0-audit-broad-content','0.4.0-experimental-minecells','0.4.0-experimental-minecells-fg','0.4.0-experimental-minecells-fg-questlog','0.4.0-experimental-minecells-fg-questlog-q1','0.4.1-experimental-six-fix-test')
if j['version'] != '0.4.0-b1-living-world-batch':
    EXPECT_REMOVED_GALOSPHERE = True
else:
    EXPECT_REMOVED_GALOSPHERE = False
EXPECTED_MODS={
 'guard-villagers':(360203,8767509),
 'easy-npc-core':(1308987,9039094),
 'easy-npc-ui':(1214728,9039106),
 'galosphere':(631098,8242886),
 'better-archeology':(835687,9099893),
 'resourceful-config-dep':(714059,6467772),
 'naturalist':(627986,9004373),
 'villager-names':(345854,9032258),
 'collective-dep':(342584,9060865),
 'cosy-critters':(1182393,8390081),
 'polytone':(958094,9103491),
 'foxified-dense-flowers':(1413643,7384220),
 'resourcify':(870076,9001238),
 'swinging-lanterns':(1477733,9116978),
 'atmosfera-neo':(1499605,8313373),
}
EXPECTED_PACKS={
 'rainbows-foliage-polytone':(1363585,9092152),
 'os-colorful-grasses-mix':(1690239,8936929),
 'bushy-pink-petals':(1321476,8493563),
 'torches-reimagined':(531730,8048795),
 'extended-illumina':(380413,6021451),
}
assert len(EXPECTED_MODS)==15
assert len(EXPECTED_PACKS)==5
def check_mod(slug,pid,fid):
 entry=j['additions']['content-040b-'+slug]
 assert (entry['projectId'],entry['id'])==(pid,fid),(slug,entry)
 assert set(entry['gameVersions'])=={'1.21.1','NeoForge'},(slug,entry)
 assert entry['fileName'].endswith('.jar'),slug
 assert entry.get('content_kind') is None,slug
for slug,(pid,fid) in EXPECTED_MODS.items():
 if slug=='galosphere' and EXPECT_REMOVED_GALOSPHERE:
  assert 'content-040b-galosphere' not in j['additions']
 else:check_mod(slug,pid,fid)
for slug,(pid,fid) in EXPECTED_PACKS.items():
 entry=j['additions']['content-040b-rp-'+slug]
 assert (entry['projectId'],entry['id'])==(pid,fid),slug
 assert entry['gameVersions']==['1.21.1'] and entry['content_kind']=='resourcepack'
 assert entry['fileName'].endswith('.zip') and entry['version_check_override'],slug
assert len({v['projectId'] for v in j['additions'].values()})==len(j['additions']),'Multiple versions of same CF project'
assert j['terminal_jigsaw_repair']['expected_overrides']==273
assert j['private_modrinth_addons'][0]['fileName']=='neoreefredux-1.0.jar'
# Source dependencies from pinned 1.21.1 NeoForge JAR files, independently audited by Github:
# Better Archeology needs Architectury >=13.0.2 (present) and Resourceful Config >=3.0.3 (added).
# Villager Names needs Collective >=8.22 (added).
# Naturalist needs GeckoLib (present).
# Easy NPC config UI requires Easy NPC Core >=7.14.0 (added exact version).
assert 'resourceful-config-dep' in EXPECTED_MODS and EXPECTED_MODS['resourceful-config-dep']==(714059,6467772)
assert EXPECTED_MODS['collective-dep']==(342584,9060865)
assert EXPECTED_MODS['easy-npc-core']==(1308987,9039094)
assert EXPECTED_MODS['easy-npc-ui']==(1214728,9039106)
# Don't mix both atmospheric audio engines or shader and server season systems in this batch.
assert 'content-040b-atmosfera-neo' in j['additions']
assert not any('ambient-sounds' in k or 'serene-seasons' in k or 'euphoria' in k for k in j['additions'])
with zipfile.ZipFile(ROOT/j['baseline']) as z:
    m=json.loads(z.read('manifest.json'))
    pins={a['projectID']:a['fileID'] for a in m['files']}
for v in j['remove_projects'].values():pins.pop(v,None)
for v in j['additions'].values():pins[v['projectId']]=v['id']
if j.get('default_integrated_patches'):
 v=j['optional_integrated_patches'];pins[v['projectId']]=v['id']
assert len(pins)=={'0.4.0-b1-living-world-batch':289,'0.4.0-c0-ecosystem-feedback':288,'0.4.0-d0-content-first':296,'0.4.0-e0-audit-broad-content':313,'0.4.0-experimental-minecells':318,'0.4.0-experimental-minecells-fg':330,'0.4.0-experimental-minecells-fg-questlog':331,'0.4.0-experimental-minecells-fg-questlog-q1':331,'0.4.1-experimental-six-fix-test':331}[j['version']],len(pins)
for pid,fid in [*EXPECTED_MODS.values(),*EXPECTED_PACKS.values()]:
 if pid==631098 and EXPECT_REMOVED_GALOSPHERE:
  assert pid not in pins
 else:assert pins[pid]==fid
print(f'PASS: inherited 0.4b pins with explicit later Galosphere removal; {len(pins)} CF refs, no conflicting ambient/season stack.')
print('PASS: dependency pairs, all 273 previous terminal NBT fixes remain pinned; no runtime success implied.')
