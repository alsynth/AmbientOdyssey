"""Exact r19 delta: tested client performance candidate; no terrain/loot/quest changes."""
import argparse,hashlib,json
from pathlib import Path
from zipfile import ZipFile
from package_v048_ui_fix import archive
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='10fe2562ac0f584dbdc1372ff2542b2224a939cf67f5b7fd116934cec4511fd1'
REMOVED={502561,532127,638111}
ADDED={915902:8884680,448233:9100286}
CONFIGS=['streamsreflowing-client.toml','entityculling.json','euphoria_patcher/settings.toml','oculus.properties']
def build(base,output):
 assert hashlib.sha256(base.read_bytes()).hexdigest()==BASE_SHA
 with ZipFile(base) as z:assert z.testzip() is None;original={n:z.read(n) for n in z.namelist()}
 full=dict(original);m=json.loads(full['manifest.json']);old={f['projectID']:f['fileID'] for f in m['files']}
 assert len(old)==329 and REMOVED<=old.keys()
 m['files']=[f for f in m['files'] if f['projectID'] not in REMOVED]+[{'projectID':k,'fileID':v,'required':True} for k,v in ADDED.items()]
 m['name']='Ambient Odyssey v0.4.9 - Client Performance TEST';m['version']='0.4.9-client-performance-test'
 assert len(m['files'])==len({f['projectID'] for f in m['files']})==328
 full['manifest.json']=(json.dumps(m,indent=2)+'\n').encode()
 removed_paths={'overrides/config/equipmentcompare.toml','overrides/config/legendarytooltips.toml'}
 for n in removed_paths:full.pop(n,None)
 modified=set()
 for n in CONFIGS:
  target='overrides/config/'+n;full[target]=(ROOT/'release_030'/target).read_bytes();modified.add(target)
 for p in (ROOT/'release_030/overrides/shaderpacks').glob('AO *.txt'):
  full['overrides/shaderpacks/'+p.name]=p.read_bytes()
 full['overrides/AO_TEST_NOTES/PERFORMANCE_READ_FIRST.txt']=b"Import this test as a NEW CurseForge profile.\nBalanced shaders are selected by default. Shader menu offers AO Performance / AO Balanced / AO Quality.\nShaders are generated locally by the original Euphoria Patcher from the original Complementary download.\nFor weaker hardware select AO Performance or disable shaders.\nClient tick culling is OFF. Streams particle work is reduced; terrain unchanged.\nDisabled Equipment Compare/Legendary Tooltips and exclusive Prism are removed; Iceberg retained.\nUse r19 rollback for comparisons. No broad FPS improvement is certified by startup tests.\n"
 for n,b in original.items():
  if n!='manifest.json' and n not in removed_paths|modified:assert full[n]==b,n
 assert {f['projectID']:f['fileID'] for f in m['files']}=={**{k:v for k,v in old.items() if k not in REMOVED},**ADDED}
 assert not any(n.startswith('overrides/mods/') and 'probe' in n for n in full)
 sha=archive(output,full);r={'base_sha256':BASE_SHA,'output_sha256':sha,'cf_pins':328,'removed_projects':sorted(REMOVED),'added_projects':ADDED,'r19_other_bundled_jars_worldgen_quests_loot_unchanged':True}
 output.with_suffix('.inputs.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.base,a.output)
