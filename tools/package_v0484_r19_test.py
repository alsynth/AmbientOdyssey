"""Integrate the exact user-supplied r19 candidate into the tested v0483 UI pack."""
import argparse,hashlib,io,json,tomllib
from pathlib import Path
from zipfile import ZipFile
from package_v048_ui_fix import archive
BASE_SHA='e5806a9aba3a5287cd4a3ab374494880b20bdcdbb64f983b57086b74b9d83a5d'
R19_SHA='5baeb9321dcabdad2664f159a089e6e7265f7b14072ccf1bb5cdf3ffec1df6e4'
R8_SHA='05639f00c2905db6f28cac5de6e4076d1f873ffcf80dcad24b48aa19e05af13a'
JAR='overrides/mods/ao-apotheotic-port-prototype-0.4.8-prototype.jar'
NOTES='overrides/AO_TEST_NOTES/'
def build(a):
 assert hashlib.sha256(a.base.read_bytes()).hexdigest()==BASE_SHA
 blob=a.jar.read_bytes();assert hashlib.sha256(blob).hexdigest()==R19_SHA
 with ZipFile(io.BytesIO(blob)) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  meta=tomllib.loads(z.read('META-INF/neoforge.mods.toml').decode())['mods'][0]
  assert meta['modId']=='ao_apotheotic_port' and meta['version']=='0.4.8-prototype'
  resources=0
  for n in z.namelist():
   if n.endswith('.json'):json.loads(z.read(n));resources+=1
 with ZipFile(a.base) as z:
  assert z.testzip() is None
  original={n:z.read(n) for n in z.namelist()}
 assert hashlib.sha256(original[JAR]).hexdigest()==R8_SHA
 full=dict(original);full[JAR]=blob
 manifest=json.loads(full['manifest.json']);assert len(manifest['files'])==329
 assert {1023913,1657433}.isdisjoint(f['projectID'] for f in manifest['files'])
 manifest['name']='Ambient Odyssey v0.4.8.4 - R19 Full Pack TEST'
 manifest['version']='0.4.8.4-r19-full-pack-test'
 full['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
 with ZipFile(a.kit) as z:
  assert hashlib.sha256(z.read(JAR)).hexdigest()==R19_SHA
  full[NOTES+'GEM_PORT_MANUAL_TEST_CHECKLIST.md']=z.read('MANUAL_TEST_CHECKLIST.md')
  for n in list(full):
   if n.startswith(NOTES+'OPTIONAL_QA_DATAPACK/'):del full[n]
  for n in z.namelist():
   if n.startswith('QA_DATAPACK/') and not n.endswith('/'):
    full[NOTES+'OPTIONAL_QA_DATAPACK/'+n[len('QA_DATAPACK/'):]]=z.read(n)
 old=full.pop(NOTES+'R8_FULL_PACK_CHECKS.txt',None)
 if old:full[NOTES+'HISTORICAL_R8_FULL_PACK_CHECKS.txt']=old
 full[NOTES+'READ_FIRST.txt']=b"Import as a NEW CurseForge profile and use a throwaway world.\nExact r19 Apotheotic prototype: matching owner report passed all 30 native GameTests.\nLatest Q above right armor / E below left tool slots, trim, tooltip and startup fixes retained.\nWhaleborne and Wet Sand retained. Subtle Effects and its exclusive patch remain removed.\nFollow GEM_PORT_MANUAL_TEST_CHECKLIST.md; save logs/latest.log.\nOptional QA datapack is reference material and not automatically enabled.\nHistorical notes describe prior JARs. Multiplayer and full gameplay need manual tests.\n"
 if a.report:full[NOTES+'R19_FULL_PACK_CHECKS.txt']=a.report.read_bytes()
 for n,b in original.items():
  if n not in {JAR,'manifest.json'} and not n.startswith(NOTES):assert full[n]==b,n
 assert manifest['files']==json.loads(original['manifest.json'])['files']
 assert not any(n.startswith('overrides/mods/') and 'probe' in n and n.endswith('.jar') for n in full)
 sha=archive(a.output,full)
 report={'base_sha256':BASE_SHA,'r19_jar_sha256':R19_SHA,'output_sha256':sha,'curseforge_pins_unchanged':329,'other_bundled_jars_ui_quests_recipes_worldgen_unchanged':True,'jar_json_resources_parsed':resources}
 a.output.with_suffix('.inputs.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['base','jar','kit','output']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--report',type=Path)
 build(p.parse_args())
