"""Exact delta from the verified r8 import: optional ring bridge and approved mod removal."""
import argparse,hashlib,json,io,tomllib
from pathlib import Path
from zipfile import ZipFile
from package_v048_ui_fix import archive
BASE_SHA='6b8ebe241ace59469098650aadf5f143a7fa1e16d1514488449dd69e3522363b'
REMOVED={1023913,1657433}
def build(base,jar,output):
 assert hashlib.sha256(base.read_bytes()).hexdigest()==BASE_SHA
 with ZipFile(base) as z:
  assert z.testzip() is None
  original={n:z.read(n) for n in z.namelist()}
 full=dict(original); manifest=json.loads(full['manifest.json'])
 before={f['projectID']:f['fileID'] for f in manifest['files']}
 assert before[1023913]==7768631 and before[1657433]==8673508
 manifest['files']=[f for f in manifest['files'] if f['projectID'] not in REMOVED]
 manifest['name']='Ambient Odyssey v0.4.8.3 - Ring Inventory TEST'
 manifest['version']='0.4.8.3-ring-inventory-test'
 assert len(manifest['files'])==329
 full['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
 removed_paths=[]
 for n in list(full):
  if n.startswith('overrides/config/') and ('subtle_effects' in n.lower() or 'subtleeffects' in n.lower() or 'subtleendremcompat' in n.lower()):
   removed_paths.append(n); del full[n]
 blob=jar.read_bytes()
 with ZipFile(io.BytesIO(blob)) as z:
  assert z.testzip() is None
  assert tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode())['mods'][0]['modId']=='aoenigmaticbridge'
  assert not any('QA' in n or 'Probe' in n for n in z.namelist())
 full['overrides/mods/'+jar.name]=blob
 full['overrides/AO_TEST_NOTES/RING_INVENTORY_CHECKLIST.txt']=b"Use a NEW profile and throwaway world.\nWithout the equipped Seven Curses ring: no E tab.\nEquip it in Curios: E tab above Settings opens the original Ender Chest.\nCheck normal/hover appearance, scales 2/3/4, Q/Settings/Curios/backpacks.\nCheck carried items, save/reload, disabled ring-access config and multiplayer.\nSubtle Effects and its End Remastered patch removed; Fzzy Config retained.\nRetest the previously crashing mob interaction.\n"
 for n,b in original.items():
  if n!='manifest.json' and n not in removed_paths: assert full[n]==b,n
 after={f['projectID']:f['fileID'] for f in manifest['files']}
 assert after=={k:v for k,v in before.items() if k not in REMOVED}
 assert not any('subtle' in n.lower() and n.startswith('overrides/mods/') for n in full)
 sha=archive(output,full)
 report={'base_sha256':BASE_SHA,'output_sha256':sha,'bridge_sha256':hashlib.sha256(blob).hexdigest(),'removed_projects':sorted(REMOVED),'curseforge_pins':329,'remaining_pins_and_original_payload_unchanged':True,'removed_config_paths':removed_paths}
 output.with_suffix('.inputs.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['base','jar','output']: p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();build(a.base,a.jar,a.output)
