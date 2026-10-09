#!/usr/bin/env python3
"""Re-run Structure Test 5's scoped static gates from its offline audit snapshot.

This deliberately does not certify uninspected JARs or claim a gameplay test.
"""
import argparse,collections,gzip,hashlib,json,sys,zipfile
from pathlib import Path
from audit_jars_031 import load_json,resource_id,overlay_tags,resolve_tag,selector_tag_references

ROOT=Path(__file__).resolve().parent;RELEASE=ROOT/'release_030';OVERRIDES=RELEASE/'overrides'
BUILTIN_SETS={'minecraft:villages','minecraft:nether_complexes','minecraft:nether_fossils',
 'minecraft:buried_treasures','minecraft:desert_pyramids','minecraft:end_cities','minecraft:igloos',
 'minecraft:jungle_temples','minecraft:mineshafts','minecraft:ocean_monuments','minecraft:ocean_ruins',
 'minecraft:pillager_outposts','minecraft:ruined_portals','minecraft:shipwrecks','minecraft:strongholds',
 'minecraft:swamp_huts','minecraft:trail_ruins','minecraft:trial_chambers','minecraft:woodland_mansions','minecraft:ancient_cities'}

def validate(archive=None,test4=None):
 _idx=RELEASE/'evidence/jar-resource-index-test6.json.gz'
 snapshot=json.loads(gzip.decompress((_idx if _idx.exists() else RELEASE/'evidence/jar-resource-index-test5.json.gz').read_bytes()))
 native=snapshot['resources'];plan=json.loads((RELEASE/'structure-density.json').read_text());compat=json.loads((RELEASE/'structure-compatibility.json').read_text())
 reference=json.loads((RELEASE/'evidence/test4-baseline.json').read_text())
 checks=[]
 def check(name,condition,detail):
  checks.append({'check':name,'passed':bool(condition),'detail':detail})
  if not condition:raise AssertionError(name+': '+str(detail))
 # Compiler-owned resources must be strict JSON, irrespective of legacy configs.
 generated=[]
 for pack_name in ['ao_compatibility','ao_structure_density','ao_structure_repairs','ao_biome_replacement']:
  pack=OVERRIDES/'config/paxi/datapacks'/pack_name
  assert json.loads((pack/'pack.mcmeta').read_text())['pack']['pack_format']==48
  for path in pack.rglob('*.json'):
   json.loads(path.read_text());generated.append(path)
 check('Generated JSON and Minecraft 1.21.1 pack formats',True,len(generated))
 effective={c:{id:rows[-1]['data'] for id,rows in native[c].items()} for c in ['worldgen/structure','worldgen/structure_set','worldgen/template_pool']}
 added={c:{} for c in effective}
 for path in sorted((OVERRIDES/'config/paxi/datapacks').glob('*/data/**/*.json')):
  rel='data/'+path.as_posix().split('/data/',1)[1]
  for category in effective:
   id=resource_id(rel,category)
   if id:
    obj=json.loads(path.read_text());effective[category][id]=obj;added[category][id]=obj
    break
 tags=overlay_tags(native['tags/worldgen/biome'],OVERRIDES)
 known_biomes=set(native['worldgen/biome'])
 # All modded biome IDs introduced by the authoring input are present in the
 # actual inspected JSON registry resources. Vanilla IDs are base-game keys.
 introduced=[]
 for id,payload in compat['biome_tags'].items():
  for value in payload['values']:
   key=value.get('id') if isinstance(value,dict) else value
   if not key.startswith(('#','minecraft:')):introduced.append(key)
 check('Added modded biome IDs exist in inspected registry resources',all(k in known_biomes for k in introduced),len(set(introduced)))
 required_tag_refs=[]
 for id,payload in compat['biome_tags'].items():
  for value in payload['values']:
   key=value.get('id') if isinstance(value,dict) else value
   if key.startswith('#') and not (isinstance(value,dict) and value.get('required') is False):required_tag_refs.append(key[1:])
 check('New required nested biome-tag references exist',all(k in tags for k in required_tag_refs),required_tag_refs)
 for id,obj in added['worldgen/structure'].items():
  selector=obj['biomes'];check('Structure selector '+id,not isinstance(selector,str) or not selector.startswith('#') or selector[1:] in tags,selector)
 check('All newly emitted nested structure selector tags exist',all(tag in tags for obj in added['worldgen/structure'].values() for tag in selector_tag_references(obj['biomes'])),'Nested NeoForge holder sets included')
 refs=[]
 for id,obj in added['worldgen/structure_set'].items():
  p=obj['placement'];check('Placement bounds '+id,0<=p['separation']<p['spacing'] and 0<p.get('frequency',1)<=1,p)
  refs += [x['structure'] for x in obj['structures']]
  check('Positive structure weights '+id,all(isinstance(x['weight'],int) and x['weight']>0 for x in obj['structures']),len(obj['structures']))
 check('All emitted structure-set references exist',all(id in effective['worldgen/structure'] for id in refs),len(set(refs)))
 # The only new structure IDs are declared OW-only copies of exact native ship
 # definitions. Validate their provenance rather than claiming they were in a JAR.
 clones=[]
 for id,obj in added['worldgen/structure'].items():
  if id.startswith('ambient_odyssey:'):
   origin='dungeons_arise:'+id.split(':')[1].removesuffix('_overworld')
   original=native['worldgen/structure'][origin][-1]['data']
   check('Native template provenance '+id,{k:v for k,v in obj.items() if k!='biomes'}=={k:v for k,v in original.items() if k!='biomes'},origin)
   clones.append(id)
 disabled={'dungeons_arise:small_blimp','dungeons_arise:coliseum'}
 all_members=collections.defaultdict(list)
 for id,obj in effective['worldgen/structure_set'].items():
  for entry in obj['structures']:all_members[entry['structure']].append(id)
 check('Blimp/Coliseum absent from every inspected effective placement set',not any(all_members[id] for id in disabled),{id:all_members[id] for id in disabled})
 blacklist=plan['resources']['tags/worldgen/structure']['integrated_api:disabled_structures']['values']
 check('Verified Integrated API global generation safeguard',disabled<=set(blacklist),'DisableStructuresMixin HEAD returns false for tagged structures')
 toggles=load_json((OVERRIDES/'config/cristellib/dungeons_arise/structure_toggle_config.json5').read_bytes())
 check('Native Blimp/Coliseum toggles disabled',not toggles['major_structures']['small_blimp'] and not toggles['major_structures']['coliseum'],'both false')
 check('Bathhouse retained on AO owner and removed from native Cristel owner',not toggles['minor_structures']['bathhouse'] and all_members['dungeons_arise:bathhouse']==['ambient_odyssey:wda_bathhouse'],all_members['dungeons_arise:bathhouse'])
 target_members={x['structure'] for row in plan['extra_sets'] for x in row['structures']}
 target_members|={x['structure'] for x in plan['resources']['worldgen/structure_set']['integrated_villages:regular_villages']['structures']} if 'integrated_villages:regular_villages' in plan['resources']['worldgen/structure_set'] else set()
 check('Single placement owner for new ordinary/sky/bathhouse groups',all(len(all_members[id])==1 for id in target_members),{id:all_members[id] for id in sorted(target_members)})
 sets_pack=OVERRIDES/'config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set'
 stale=['extra_wda_land_and_sky','extra_wda_heavenly_ships','extra_idas_landmarks','extra_integrated_land_villages','extra_wda_small_blimp']
 check('Obsolete Test 1–4 placement grids removed',not any((sets_pack/(n+'.json')).exists() for n in stale),stale)
 nether={'regions_unexplored:blackstone_basin','regions_unexplored:infernal_holt'}
 for id in ['c:is_overworld','minecraft:is_overworld','ambient_odyssey:sky_land','ambient_odyssey:sky_land_and_river']:
  leaves,unknown=resolve_tag(id,tags)
  check('No curated Nether leak '+id,not (leaves&nether),sorted(leaves&nether))
 sky,_=resolve_tag('skyvillages:has_structure/skyvillage',tags)
 rivers={'minecraft:river','minecraft:frozen_river','regions_unexplored:muddy_river','streamsreflowing:stream'}
 check('Sky Villages retains explicit river and Streams eligibility',rivers<=sky,sorted(rivers))
 check('Sky Villages has no ocean biome selectors',not any('ocean' in k or k in {'regions_unexplored:hyacinth_deeps','regions_unexplored:rocky_reef','biomeswevegone:lush_stacks'} for k in sky),'land + rivers')
 for id in clones:
  leaves,_=resolve_tag(effective['worldgen/structure'][id]['biomes'][1:],tags)
  check('No End/Nether multiplication '+id,not any(k.startswith(('minecraft:end','minecraft:the_end','betterend:','incendium:')) or k in nether for k in leaves),len(leaves))
 for name in ['heavenly_challenger','heavenly_conqueror','heavenly_rider']:
  id='dungeons_arise:'+name;leaves,_=resolve_tag(effective['worldgen/structure'][id]['biomes'][1:],tags)
  check('Native End branch '+id,leaves=={'minecraft:end_midlands','minecraft:end_highlands'} and all_members[id]==['dungeons_arise:major_structures'],sorted(leaves))
 # All new set salts must be independent from each other and from native sets.
 new_salts=[s['placement']['salt'] for s in plan['extra_sets']]
 check('New AO placement salts are distinct',len(new_salts)==len(set(new_salts)),new_salts)
 native_salts={obj['placement'].get('salt') for id,obj in effective['worldgen/structure_set'].items() if not id.startswith('ambient_odyssey:')}
 check('New AO salts do not collide with inspected native sets',not set(new_salts)&native_salts,sorted(set(new_salts)&native_salts))
 dc=load_json((OVERRIDES/'config/cristellib/dungeoncrawl/structure_placement_config.json5').read_bytes())['dungeons']
 check('Dungeon Crawl effective native placement settings',dc['spacing']==20 and dc['separation']==9 and dc['salt']==1984010530,dc)
 # Resolve custom exclusion tags and check the graph has no new AO cycles.
 st_tags={k:list(v) for k,v in native['tags/worldgen/structure_set'].items()}
 for id,obj in plan['resources']['tags/worldgen/structure_set'].items():st_tags[id]=[{'data':obj}]
 for s in plan['extra_sets']:
  exclusion=s['placement'].get('super_exclusion_zone')
  if exclusion:
   leaves,unknown=resolve_tag(exclusion['other_set'][1:],st_tags)
   check('Exclusion graph '+s['id'],not unknown and all(k in effective['worldgen/structure_set'] or k in BUILTIN_SETS for k in leaves) and s['id'] not in leaves,sorted(leaves))
 repairs=json.loads((RELEASE/'structure-repairs.json').read_text())
 evidence=json.loads((RELEASE/'evidence/pool-repair-evidence.json').read_text())
 baseline_pools={e['pool'] for e in evidence}
 check('Original pool repairs have real native templates and matching connector evidence',baseline_pools<=set(repairs['template_pools']) and len(evidence)==33 and all(obj['elements'] for obj in repairs['template_pools'].values()),'Original 4 pools, 33 native templates retained')
 pool_locations=set()
 for id,obj in repairs['template_pools'].items():
  if id not in baseline_pools:continue
  for element in obj['elements']:
   location=element['element'].get('location')
   if location:
    ns,name=location.split(':',1);pool_locations.add((id,'data/'+ns+'/structure/'+name+'.nbt'))
 check('Every repaired pool template has connector audit provenance',pool_locations=={(e['pool'],e['template']) for e in evidence},len(pool_locations))
 for id in ['artifacts:slot/all','artifacts:slot/belt','artifacts:slot/hands']:
  original=next(row['data'] for row in native['tags/item'][id] if row['jar'].startswith('artifacts-'))
  overlay=compat['item_tags'][id]
  check('Artifacts native slot membership restored '+id,overlay['replace'] is False and set(original['values'])<=set(overlay['values']),len(original['values']))
 recipe=repairs['recipes']['simplymore:matterbane_clean']
 recipe_path=OVERRIDES/'config/paxi/datapacks/ao_structure_repairs/data/simplymore/recipe/matterbane_clean.json'
 check('Simply More recipe syntax repair compiled',json.loads(recipe_path.read_text())==recipe and recipe['ingredients']==[{'item':'simplymore:matterbane'}] and recipe['result']=={'id':'simplymore:matterbane','count':1},'native contents, valid JSON')
 moog=load_json((OVERRIDES/'config/moogs_structures.json').read_bytes())
 check('Integrated Stronghold ownership preserved',moog['presets']['mtr']['replace_stronghold'] is False and 'mtr:stronghold' in moog['disabled_structures'],'MTR stronghold disabled')
 if test4:
  with zipfile.ZipFile(test4) as base:
   drift=[]
   config_paths={'overrides/config/'+x['path'] for x in plan['placement_configs']+plan['toggle_configs']}
   for name in base.namelist():
    if not name.startswith('overrides/') or name.endswith('/'):continue
    rel=name[len('overrides/'):]
    if name in config_paths or '/paxi/datapacks/ao_compatibility/' in name or '/paxi/datapacks/ao_structure_density/' in name:continue
    if not rel.startswith(('config/','defaultconfigs/','resources/','resourcepacks/','kubejs/','options','defaultoptions/')):continue
    path=OVERRIDES/rel
    if not path.exists() or path.read_bytes()!=base.read(name):drift.append(name)
   check('Unrelated Test 4 config/assets preserved',not drift,drift)
 else:
  drift=[]
  for rel,expected in reference['unchanged_override_sha256'].items():
   path=OVERRIDES/rel
   if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:drift.append(rel)
  check('Unrelated Test 4 config/assets preserved',not drift,drift)
 if archive:
  with zipfile.ZipFile(archive) as z:
   names=z.namelist();check('CurseForge ZIP CRC and unique safe paths',z.testzip() is None and len(names)==len(set(names)) and not any(n.startswith('/') or '\\' in n or '..' in Path(n).parts for n in names),len(names))
   check('CurseForge root manifest and no bundled mod JARs','manifest.json' in names and not any(n.startswith('overrides/mods/') for n in names),'manifest.json at archive root')
   manifest=json.loads(z.read('manifest.json'))
   version=json.loads((RELEASE/'release-lock.json').read_text())['version']
   check('Pinned game/loader/version',manifest['minecraft']['version']=='1.21.1' and manifest['minecraft']['modLoaders']==[{'id':'neoforge-21.1.252','primary':True}] and manifest['version']==version,manifest['minecraft'])
   if test4:
    with zipfile.ZipFile(test4) as base:base_manifest=json.loads(base.read('manifest.json'))
   else:base_manifest=reference['manifest']
   _lock=json.loads((RELEASE/'release-lock.json').read_text());_t6={v['projectId']:v['id'] for k,v in _lock['additions'].items() if k.startswith('test6-')}
   _exp=sorted(({f['projectID']:f['fileID'] for f in base_manifest['files']}|_t6).items())
   check('Test 4 baseline pins unchanged and exactly the nine Test 6 additions added',len(_t6)==9 and [(f['projectID'],f['fileID']) for f in manifest['files']]==_exp,len(manifest['files']))
   mismatch=[]
   for path in OVERRIDES.rglob('*'):
    if path.is_file():
     name='overrides/'+path.relative_to(OVERRIDES).as_posix()
     if name not in names or z.read(name)!=path.read_bytes():mismatch.append(name)
   check('Export matches every compiled source override',not mismatch,mismatch)
   documents=['STRUCTURE_TEST5_CHANGELOG.md','STRUCTURE_BIOME_AUDIT.md','STRUCTURE_TEST5_VALIDATION.md','STRUCTURE_TEST5_INSTALL.md','TANS_OPEN_FIELD_TUNING_PLAN.md','TODO.md']
   check('Required Test 5 supporting documents embedded',all('overrides/'+name in names and z.read('overrides/'+name)==(ROOT/name).read_bytes() for name in documents),documents)
 return {'status':'PASS (scoped static gates)', 'gameplay_tested':False,'checks':checks,
  'counts':{'inspected_jars':len(snapshot['jars']),'native_structure_definitions':len(native['worldgen/structure']),
            'native_structure_set_definitions':len(native['worldgen/structure_set']),'generated_json':len(generated),
            'new_declared_structure_clones':len(clones),'independent_sets':len(plan['extra_sets'])},
  'limitations':['mods1.zip and mods3.zip full transfers failed HTTP 403; complete CRC-verified JAR members from their retrieved prefixes were audited.',
                 'Unretrieved tail JARs, registry load, worldgen execution, actual density, clipping and performance remain uncertified.',
                 'Native Minecraft tag definitions are not in the uploaded mod JARs; native graph reports explicitly retain unresolved base-game/optional tags.']}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive');p.add_argument('--test4');p.add_argument('--report');a=p.parse_args()
 report=validate(a.archive,a.test4)
 if a.report:Path(a.report).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'checks':len(report['checks']),**report['counts']}))
