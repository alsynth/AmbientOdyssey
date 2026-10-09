#!/usr/bin/env python3
"""Write the per-structure eligibility catalogue from the offline JAR snapshot."""
import argparse,csv,collections,gzip,json
from pathlib import Path
from audit_jars_031 import load_json,overlay_tags,resolve_tag,resource_id,resolve_selector
ROOT=Path(__file__).resolve().parent;R=ROOT/'release_030'

def main(test4=None):
 idx=R/'evidence/jar-resource-index-test6.json.gz'
 snapshot=json.loads(gzip.decompress((idx if idx.exists() else R/'evidence/jar-resource-index-test5.json.gz').read_bytes()));native=snapshot['resources']
 roster=json.loads((R/'biome-roster.json').read_text());curated=sorted(ns+':'+n for ns,names in roster.items() for n in names)
 nether={'regions_unexplored:blackstone_basin','regions_unexplored:infernal_holt'};ow=set(curated)-nether
 extras=['ars_nouveau:archwood_forest','streamsreflowing:stream','quark:glimmering_weald','terrablender:deferred_placeholder']+sorted(id for id in native['worldgen/biome'] if id.startswith('alexscaves:'))
 biome_columns=curated+extras
 after_tags=overlay_tags(native['tags/worldgen/biome'],R/'overrides')
 before_tags=overlay_tags(native['tags/worldgen/biome'],test4) if test4 else json.loads(gzip.decompress((R/'evidence/test4-biome-tag-graph.json.gz').read_bytes()))
 if not test4:
  new_jars=set(json.loads((R/'evidence/jar-audit-coverage-test5.json').read_text()).get('newly_recovered_logged_jars',[]))
  t6=R/'evidence/test6-addon-jars.json'
  if t6.exists():new_jars|={r['file'] for r in json.loads(t6.read_text())}
  for id,rows in native['tags/worldgen/biome'].items():
   additions=[row for row in rows if row['jar'] in new_jars]
   if additions:before_tags.setdefault(id,[]).extend(additions)
 effective={k:{id:rows[-1]['data'] for id,rows in native[k].items()} for k in ['worldgen/structure','worldgen/structure_set']}
 for p in sorted((R/'overrides/config/paxi/datapacks').glob('*/data/**/*.json')):
  rel='data/'+p.as_posix().split('/data/',1)[1]
  for cat in effective:
   id=resource_id(rel,cat)
   if id:effective[cat][id]=load_json(p.read_bytes());break
 def selector(obj,tags):
  sel=obj['biomes']
  return resolve_selector(sel,tags,set(native['worldgen/biome'])|set(biome_columns))
 memberships=collections.defaultdict(list)
 for id,obj in effective['worldgen/structure_set'].items():
  for x in obj['structures']:memberships[x['structure']].append(id)
 routes=json.loads((R/'evidence/code-generated-placement-routes.json').read_text())
 active_routes=[row for row in routes if row['enabled']]
 for row in active_routes:
  if row['structure_set_id'] not in memberships[row['structure_id']]:memberships[row['structure_id']].append(row['structure_set_id'])
 providers=collections.defaultdict(lambda:{'native':0,'changed_eligibility':0,'no_curated_ow_after':0,'vanilla_only_direct':0})
 catalogue=[];matrix=[]
 for id,obj in sorted(effective['worldgen/structure'].items()):
  rows=native['worldgen/structure'].get(id,[])
  baseline=rows[-1]['data'] if rows else obj
  before,unknown_before=selector(baseline,before_tags);after,unknown_after=selector(obj,after_tags)
  native_leaves,native_unknown=selector(baseline,native['tags/worldgen/biome'])
  before_cur=before&ow;after_cur=after&ow
  selector_text=obj['biomes'];known_dim=[]
  if after_cur or 'ars_nouveau:archwood_forest' in after or any(x in after for x in ['minecraft:plains','minecraft:forest','minecraft:river','minecraft:snowy_plains']):known_dim.append('Overworld')
  if after&nether or any(k in after for k in ['minecraft:nether_wastes','minecraft:crimson_forest','minecraft:warped_forest','minecraft:soul_sand_valley','minecraft:basalt_deltas']):known_dim.append('Nether')
  if any(k.startswith('betterend:') or k in {'minecraft:the_end','minecraft:end_midlands','minecraft:end_highlands','minecraft:end_barrens','minecraft:small_end_islands'} for k in after):known_dim.append('End')
  for prefix,dimension in [('aether:','Aether'),('the_bumblezone:','Bumblezone'),('undergarden:','Undergarden'),('deeperdarker:','Otherside'),('afterdark:','Afterdark'),('ihfr_fo:','ihfr_fo')]:
   if any(k.startswith(prefix) for k in after):known_dim.append(dimension)
  height=obj.get('start_height',{});absolute=height.get('absolute') if isinstance(height,dict) else None
  if id.startswith(('skyvillages:','sky_whale_ship:')) or 'heavenly_' in id or absolute is not None and absolute>=150:category='sky'
  elif obj.get('step') in {'underground_structures','underground_decoration'} or absolute is not None and absolute<0:category='underground'
  elif ('ocean' in str(selector_text) or 'sunken_' in id or 'shipwreck' in id) and not (after_cur-{'regions_unexplored:hyacinth_deeps','regions_unexplored:rocky_reef','biomeswevegone:lush_stacks'}):category='ocean/river'
  else:category='surface/other'
  vanilla_only=bool(native_leaves) and not native_unknown and all(k.startswith('minecraft:') for k in native_leaves)
  ns=id.split(':')[0];p=providers[ns]
  if rows:p['native']+=1
  if before_cur!=after_cur:p['changed_eligibility']+=1
  if not after_cur:p['no_curated_ow_after']+=1
  if vanilla_only:p['vanilla_only_direct']+=1
  row={'structure_id':id,'native_jar':' | '.join(r['jar'] for r in rows) or 'AO native-template clone',
       'native_resource':' | '.join(r['path'] for r in rows),'biome_selector':selector_text if isinstance(selector_text,str) else json.dumps(selector_text),
       'category_inferred_from_definition':category,'dimension_evidence':' | '.join(known_dim) or 'Other/undetermined',
       'placement_step':obj.get('step',''),'start_height':json.dumps(height,separators=(',',':')),
       'terrain_adaptation':obj.get('terrain_adaptation',obj.get('adapt_noise','')),
       'effective_structure_sets':' | '.join(sorted(memberships[id])),
       'curated_ow_before_test4_count':len(before_cur),'curated_ow_test5_count':len(after_cur),
       'added_curated_ow_biomes':' | '.join(sorted(after_cur-before_cur)),
       'removed_curated_ow_biomes':' | '.join(sorted(before_cur-after_cur)),
       'native_direct_graph_vanilla_only':vanilla_only,
       'unresolved_native_tags':' | '.join(sorted(native_unknown)),
       'unresolved_effective_tags':' | '.join(sorted(unknown_after)),
       'resolved_curated_ow_biomes':' | '.join(sorted(after_cur))}
  catalogue.append(row);matrix.append({'structure_id':id,**{b:int(b in after) for b in biome_columns},'unresolved_tag_count':len(unknown_after)})
 with (ROOT/'STRUCTURE_REGISTRY_CATALOG.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(catalogue[0]));w.writeheader();w.writerows(catalogue)
 with (ROOT/'STRUCTURE_BIOME_MATRIX.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(matrix[0]));w.writeheader();w.writerows(matrix)
 duplicates=[{'structure_id':id,'effective_sets':sets} for id,sets in sorted(memberships.items()) if len(sets)>1]
 (R/'evidence/duplicate-placement-membership-test5.json').write_text(json.dumps(duplicates,indent=2)+'\n')
 set_rows=[];salt_groups=collections.defaultdict(list)
 moog=load_json((R/'overrides/config/moogs_structures.json').read_bytes())
 for id,obj in sorted(effective['worldgen/structure_set'].items()):
  ns,name=id.split(':',1);placement=dict(obj['placement']);config_path=R/'overrides/config/cristellib'/ns/'structure_placement_config.json5'
  if config_path.exists():
   cfg=load_json(config_path.read_bytes());entry=cfg
   for part in name.split('/'):
    entry=entry.get(part,{}) if isinstance(entry,dict) else {}
   if isinstance(entry,dict):placement.update({k:v for k,v in entry.items() if not isinstance(v,dict)})
  eligible=set();unknown=set()
  for member in obj['structures']:
   if member['structure'] in effective['worldgen/structure']:
    leaves,missing=selector(effective['worldgen/structure'][member['structure']],after_tags)
    eligible|=leaves&ow;unknown|=missing
  code_entries=[route for route in active_routes if route['structure_set_id']==id]
  for route in code_entries:
   if route['structure_id'] in effective['worldgen/structure']:
    leaves,missing=selector(effective['worldgen/structure'][route['structure_id']],after_tags)
    eligible|=leaves&ow;unknown|=missing
  code_note='; code adds '+str(len(code_entries))+' CTOV entries' if code_entries else ''
  row={'structure_set_id':id,'placement_type':placement.get('type'),'spacing':placement.get('spacing'),
       'separation':placement.get('separation'),'salt':placement.get('salt'),'frequency':placement.get('frequency',1),
       'moog_per_set_multiplier':moog['frequency']['per_structure'].get(id,''),'placement_json':json.dumps(placement,separators=(',',':')),
       'members':' | '.join(f"{x['structure']} (weight {x['weight']})" for x in obj['structures'])+code_note,
       'curated_ow_membership_count':len(eligible),'unresolved_selector_tags':' | '.join(sorted(unknown)),
       'cristel_config_present':config_path.exists(),'library_execution_verified':False}
  set_rows.append(row)
  if placement.get('salt') is not None:salt_groups[placement['salt']].append({'set':id,'placement':placement,'curated_ow_biomes':sorted(eligible)})
 for id in sorted({route['structure_set_id'] for route in active_routes}-set(effective['worldgen/structure_set'])):
  code_entries=[route for route in active_routes if route['structure_set_id']==id]
  set_rows.append({'structure_set_id':id,'placement_type':'Base-game definition not captured; code augments existing set',
   'members':' | '.join(f"{x['structure_id']} (weight {x['weight']}, code route)" for x in code_entries),
   'library_execution_verified':False})
 with (ROOT/'STRUCTURE_SET_CATALOG.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(set_rows[0]));w.writeheader();w.writerows(set_rows)
 collisions=[{'salt':salt,'sets':entries} for salt,entries in sorted(salt_groups.items()) if len(entries)>1]
 (R/'evidence/shared-placement-salts-test5.json').write_text(json.dumps(collisions,indent=2)+'\n')
 summary={'provider_summary':dict(providers),'inspected_jars':len(snapshot['jars']),'native_structures':len(native['worldgen/structure']),
          'native_structure_sets':len(native['worldgen/structure_set']),'catalogue_rows':len(catalogue),'curated_biomes':len(curated),
          'curated_ow_biomes':len(ow),'matrix_biome_columns':len(biome_columns),'remaining_native_duplicate_structures':len(duplicates),
          'effective_structure_sets':len(set_rows),'shared_salt_groups':len(collisions)}
 (R/'evidence/structure-audit-summary-test5.json').write_text(json.dumps(summary,indent=2)+'\n')
 table='\n'.join(f"| `{ns}` | {v['native']} | {v['changed_eligibility']} | {v['no_curated_ow_after']} |" for ns,v in sorted(providers.items()))
 from report_continuation_031 import audit_report
 report=audit_report(snapshot,summary,table)
 (ROOT/'STRUCTURE_BIOME_AUDIT.md').write_text(report)
 print(json.dumps({k:v for k,v in summary.items() if k!='provider_summary'}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--test4-overrides');a=p.parse_args();main(a.test4_overrides)
