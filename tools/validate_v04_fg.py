#!/usr/bin/env python3
"""Exact static 0.4f/g reconciliation gates; not gameplay certification."""
import json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'release_030/release-lock.json').read_text())
assert lock['version']=='0.4.1-experimental-six-fix-test'
assert lock['experimental_minecells']['expected_manifest_refs']==331
EXPECTED={
  "content-040f-armor-trim-item-fix": [
    895603,
    5924310,
    "ArmorTrimItemFix-neoforge-1.21.1-1.2.0.jar"
  ],
  "content-040f-shulker-box-tooltip": [
    315811,
    6530833,
    "shulkerboxtooltip-neoforge-5.1.6+1.21.1.jar"
  ],
  "content-040f-crafting-tweaks": [
    233071,
    8697050,
    "craftingtweaks-neoforge-1.21.1-21.1.11.jar"
  ],
  "content-040f-chat-heads": [
    407206,
    7057837,
    "chat_heads-0.14.0-neoforge-1.21.jar"
  ],
  "content-040f-sound-physics": [
    535489,
    7032247,
    "sound-physics-remastered-neoforge-1.21.1-1.5.1.jar"
  ],
  "content-040f-polymorph": [
    388800,
    6794589,
    "polymorph-neoforge-1.1.0+1.21.1.jar"
  ],
  "content-040f-brewin-and-chewin": [
    637808,
    8309583,
    "BrewinAndChewin-neoforge-4.5.0+1.21.1.jar"
  ],
  "content-040g-dimensional-dungeons": [
    352222,
    8828150,
    "dimdungeons-210-neoforge-1.21.1.jar"
  ],
  "content-040g-ancient-remnants": [
    1668579,
    9084406,
    "ancient_remnants-1.5.2+1.21.1-neoforge.jar"
  ],
  "content-040g-tarotcards-remastered": [
    1473837,
    8450385,
    "tarotcards-2.3.5-neoforge-1.21.1.jar"
  ],
  "content-040g-aquaculture-delight": [
    961988,
    6179576,
    "aquaculturedelight-1.2.0-neoforge-1.21.1.jar"
  ],
  "content-040g-end-remastered-additions": [
    1365790,
    9111385,
    "endrem_additions-neoforge-1.2.0.jar"
  ]
}
assert len(EXPECTED)==12
for slug,(pid,fid,filename) in EXPECTED.items():
 e=lock['additions'][slug]
 assert (e['projectId'],e['id'],e['fileName'])==(pid,fid,filename),slug
 assert {'1.21.1','NeoForge'}.issubset(e['gameVersions']),slug
with zipfile.ZipFile(ROOT/lock['baseline']) as z:
 base=json.loads(z.read('manifest.json'))
refs={e['projectID']:e['fileID'] for e in base['files']}
for pid in lock['remove_projects'].values():refs.pop(pid,None)
for slug,e in lock['additions'].items():
 pid,fid=e['projectId'],e['id']
 assert pid not in refs or refs[pid]==fid,('unreviewed repin',slug,pid,fid,refs.get(pid))
 refs[pid]=fid
if lock.get('default_integrated_patches'):
 e=lock['optional_integrated_patches'];refs[e['projectId']]=e['id']
assert len(refs)==331,len(refs)
assert refs[318449]==5845879 and 1100379 not in refs
for pid,fid,_ in EXPECTED.values(): assert refs[pid]==fid
for pid in (618790,890127,889079,532610,520110,623764,841890,638111,1005914,1123977,60028):
 assert pid in refs,('missing prior required project',pid)
assert refs[1023913]==7768631, 'Keep completed Mine Cells Subtle Effects pin, do not silently repin'
assert lock['terminal_jigsaw_repair']['expected_overrides']==273
print('PASS: 331 refs including exact 12 f/g pins; pinned Mine Cells stack, libraries, Subtle Effects and 273 native repairs retained. Static only.')
