#!/usr/bin/env python3
"""Validate the Test 5 audit revision from its reproducible offline evidence."""
import argparse,copy,csv,gzip,hashlib,json,re,zipfile
from pathlib import Path
from audit_jars_031 import load_json,overlay_tags,resolve_tag,resolve_selector
from nbt_audit_031 import NbtReader,plain,template_details,migrate_waystone_jigsaw
from validate_structure_test5 import validate as original_gates

ROOT=Path(__file__).resolve().parent
R=ROOT/'release_030';E=R/'evidence';O=R/'overrides'

def validate(archive=None):
    report=original_gates(archive=archive)
    checks=report['checks']
    def check(name,condition,detail):
        checks.append({'check':name,'passed':bool(condition),'detail':detail})
        if not condition:raise AssertionError(name+': '+str(detail))
    snapshot=json.loads(gzip.decompress((E/'jar-resource-index-test5.json.gz').read_bytes()))
    native=snapshot['resources'];density=json.loads((R/'structure-density.json').read_text())
    repairs=json.loads((R/'structure-repairs.json').read_text())
    compat=json.loads((R/'structure-compatibility.json').read_text())
    coverage=json.loads((E/'jar-audit-coverage-test5.json').read_text())
    check('Expanded audit coverage reconciles 177 + 19 and 60 - 19',len(snapshot['jars'])==196 and len(coverage['unretrieved_logged_jars'])==41 and len(coverage['newly_recovered_logged_jars'])==19,{'audited':196,'missing':41})
    check('No duplicate audited binaries',len({row['sha256'] for row in snapshot['jars']})==196,'SHA-256 deduplication')
    proof=json.loads((E/'baseline-reproduction.json').read_text())
    check('Untouched Test 5 reproduced and original catalogues regenerated',proof['import_archive_sha256']==proof['fresh_rebuild_sha256'] and all(proof['original_catalogue_regeneration'].values()) and proof['scoped_static_checks']==76,proof['fresh_rebuild_sha256'])
    # Cristel modifies native JSON, so the extraction toggles must agree even
    # if its generated runtime pack is above the AO datapack at runtime.
    for id,obj in density['resources']['worldgen/structure_set'].items():
        if not id.startswith(('dungeons_arise:','idas:')):continue
        ns,name=id.split(':',1);cfg=load_json((O/'config/cristellib'/ns/'structure_toggle_config.json5').read_bytes())
        original=native['worldgen/structure_set'][id][-1]['data']
        removed={x['structure'] for x in original['structures']}-{x['structure'] for x in obj['structures']}
        def enabled(structure):
            value=cfg[name]
            for part in structure.split(':')[1].split('/'):value=value[part]
            return value
        check('Cristel extraction toggles '+id,all(not enabled(x) for x in removed),sorted(removed))
        place=load_json((O/'config/cristellib'/ns/'structure_placement_config.json5').read_bytes())[name]
        check('Cristel native placement fields agree '+id,all(place[k]==obj['placement'].get(k,1) for k in ['spacing','separation','frequency']),'spacing/separation/frequency')
    farm_native={id:rows[-1]['data'] for id,rows in native['worldgen/structure_set'].items() if id.startswith('farmers_structures:')}
    farm_cfg=load_json((O/'config/cristellib/farmers_structures/structure_placement_config.json5').read_bytes())
    salts=[]
    for id,original in sorted(farm_native.items()):
        obj=density['resources']['worldgen/structure_set'][id];p=obj['placement'];name=id.split(':')[1]
        unchanged={k:v for k,v in original['placement'].items() if k not in {'spacing','separation','salt'}}
        preserved={k:v for k,v in p.items() if k not in {'spacing','separation','salt'}}
        check('Farmers placement and restrictions '+name,
              obj['structures']==original['structures'] and unchanged==preserved and
              0<=p['separation']<p['spacing']<original['placement']['spacing'] and
              all(p[k]==farm_cfg[name][k] for k in ['spacing','separation','salt']) and
              -2147483648<=p['salt']<=2147483647,
              {'native_spacing':original['placement']['spacing'],'candidate_spacing':p['spacing']})
        salts.append(p['salt'])
        for member in obj['structures']:
            check('Farmers native dimension/height definition unchanged '+member['structure'],member['structure'] not in compat['structures'] and member['structure'] not in density['resources']['worldgen/structure'],'No structure definition or biome-tag edits in this pass')
    other_salts={obj['placement'].get('salt') for id,rows in native['worldgen/structure_set'].items() if not id.startswith('farmers_structures:') for obj in [rows[-1]['data']]}
    check('All 20 Farmers salts unique and independent',len(salts)==20 and len(set(salts))==20 and not set(salts)&other_salts,salts)
    pool_evidence=json.loads((E/'pool-repair-continuation-evidence.json').read_text())
    pool_map={(row['pool'],row['template']):row for row in pool_evidence}
    locations=set()
    baseline={e['pool'] for e in json.loads((E/'pool-repair-evidence.json').read_text())}
    for id,obj in repairs['template_pools'].items():
        if id in baseline:continue
        for entry in obj['elements']:
            element=entry['element'];location=element.get('location')
            if location:locations.add((id,'data/'+location.replace(':','/structure/')+'.nbt'))
            else:check('D&T genuine empty choice '+id,element=={'element_type':'minecraft:empty_pool_element'},entry['weight'])
    check('Every new pool template has actual source provenance',locations==set(pool_map),'52 template provenance rows')
    migration=repairs['template_migrations']['ctov:village/waystone/sand'];raw=(R/migration['source']).read_bytes()
    emitted=(O/'config/paxi/datapacks/ao_structure_repairs/data/ctov/structure/village/waystone/sand.nbt').read_bytes()
    check('Waystone migration deterministic from exact native input',hashlib.sha256(raw).hexdigest()==migration['source_sha256'] and gzip.decompress(emitted)==gzip.decompress(migrate_waystone_jigsaw(raw)) and hashlib.sha256(emitted).hexdigest()=='40620134589628ae5e6752bbc231aa4ce75dd6a5d910d9a3e1abb4143ce4ff7c','Native Waystones desert template')
    before=template_details(raw);after=template_details(emitted)
    check('Waystone geometry/palette/entities retained',before['size']==after['size'] and before['palette_ids']==after['palette_ids'] and before['entities']==after['entities'] and [j['pos'] for j in before['jigsaws']]==[j['pos'] for j in after['jigsaws']],'Only legacy connector NBT and orientation schema migrated')
    check('Waystone connector matches CTOV parent target',all(j['nbt']['name']=='minecraft:building_entrance' and j['nbt']['pool']=='minecraft:empty' for j in after['jigsaws']),'Parent Christmas town center target confirmed in original CTOV NBT')
    basement=repairs['template_pools']['minecraft:illager_mansion/illager_mansion_room_basement']
    check('Mansion basement rooms preserved with real empty choice',len(basement['elements'])==50 and basement['elements'][0]=={'weight':20,'element':{'element_type':'minecraft:empty_pool_element'}} and len([row for row in pool_evidence if row['pool']==basement['name']])==49,'49 present NBT rooms and native processors; all native weights retained')
    recipe_evidence=json.loads((E/'catspell-absent-items.json').read_text())
    check('Exactly 11 proven absent-item recipes gated',len(recipe_evidence['affected_recipes'])==11 and all(repairs['recipes'][row['recipe']]['neoforge:conditions']==[{'type':'neoforge:false'}] and row['absent_items'] for row in recipe_evidence['affected_recipes']),'Native recipe payloads retained; no invented registry keys')
    tags=repairs['additional_resources']['tags/entity_type']
    check('Traveloptics fire tag strict JSON and replacement semantics',tags['traveloptics:element_fire']['replace'] is True and 'irons_spellbooks:pyromancer' in tags['traveloptics:element_fire']['values'],'Missing comma repaired')
    for id in ['traveloptics:aerial_collapse_dr','traveloptics:spectral_blink_blacklist','traveloptics:spectral_shift_blacklist']:
        values=tags[id]['values']
        check('Actual Ancient Ancient Remnant namespace '+id,'cataclysm:ancient_ancient_remnant' not in values and {'id':'cataclysm_spellbooks:ancient_ancient_remnant','required':False} in values,'CSEntityRegistry registration verified')
    client=O/'config/paxi/resourcepacks/ao_resource_repairs'
    check('Client repair pack format and model payloads',json.loads((client/'pack.mcmeta').read_text())['pack']['pack_format']==34 and all(json.loads((client/name).read_text())==payload for name,payload in repairs['client_models'].items()),len(repairs['client_models']))
    model_proof=json.loads((E/'traveloptics-repair-evidence.json').read_text())
    check('Every client model has native resource evidence',len(repairs['client_models'])==33 and set(repairs['client_models'])=={row['path'] for row in model_proof['model_patches']} and all(len(row['native_sha256'])==64 and row['changes'] for row in model_proof['model_patches']),'33 native model hashes and recorded changes')
    for row in recipe_evidence['affected_recipes']:
        id=row['recipe'];payload=repairs['recipes'][id]
        check('Disabled recipe native payload retained '+id,{k:v for k,v in payload.items() if k!='neoforge:conditions'}==native['recipe'][id][-1]['data'],row['absent_items'])
    alias='cataclysm_spellbooks:archaeology/cursed_pyramid_prison_modifier'
    source='cataclysm_spellbooks:archaeology/cursed_pyramid_modifier'
    global_entries=next(row['data']['entries'] for row in native['loot_modifiers']['neoforge:global_loot_modifiers'] if row['jar'].startswith('cataclysm_spellbooks-'))
    check('Loot alias matches the real native payload without duplicate registration',repairs['additional_resources']['loot_modifiers'][alias]==native['loot_modifiers'][source][-1]['data'] and global_entries.count(alias)==1 and source not in global_entries,'Native global list references only the missing alias, not both resources')
    patches=json.loads((E/'continuation-biome-patches.json').read_text())
    check('Curated CTOV/Rustic eligibility changes preserve non-biome fields',len(patches)==36 and all({k:v for k,v in compat['structures'][row['structure']].items() if k!='biomes'}=={k:v for k,v in native['worldgen/structure'][row['structure']][-1]['data'].items() if k!='biomes'} for row in patches),'32 CTOV + 4 Rustic definitions')
    staged=json.loads((R/'approved-structure-additions.json').read_text())
    locked=json.loads((R/'release-lock.json').read_text())
    HEX=re.compile(r'[0-9a-f]{64}')
    check('Nine Test 6 mods recorded as installed with supplied-binary SHA-256, audited, dependencies verified',len(staged['mods'])==9 and staged['manifest_mutation'] is True and all(row['enabled'] is True and row['binary_audited'] is True and row['dependencies_verified'] is True and HEX.fullmatch(row['sha256'] or '') and row['status']=='INSTALLED_STATIC_AUDITED' for row in staged['mods']),'Static audit only; no runtime test')
    staged_ids={row['projectID'] for row in staged['mods']}
    reference=json.loads((E/'test4-baseline.json').read_text())['manifest']
    current_ids={row['projectID'] for row in reference['files']}
    check('Test 6 mods are new projects pinned in the lock with matching file IDs',not staged_ids&current_ids and {row['projectID']:row['fileID'] for row in staged['mods']}=={v['projectId']:v['id'] for k,v in locked['additions'].items() if k.startswith('test6-')},'No unselected substitution')
    check('Archaion dependency AAA Particles is pinned',979809 in staged_ids and 1620396 in staged_ids,'aaa_particles >= 2.2.3 satisfied by 2.3.3')
    check('Born in Chaos removal retained in locked sources',locked['remove_projects']['born-in-chaos']==686437 and 686437 not in current_ids,'Project 686437 excluded')
    screen=list(csv.DictReader((ROOT/'INSTALLED_MOD_STRUCTURE_SCREENING.csv').open()))
    future=list(csv.DictReader((ROOT/'FUTURE_MOD_STRUCTURE_SCREENING.csv').open()))
    check('Screening coverage and its scopes preserved',len(screen)==196 and sum(row['current_binary_class_screen']=='True' for row in screen)==26 and len(future)==166 and all('no binary audit' in row['evidence_scope'] for row in future),'196 resource rows; 26 current binary screens; 166 description-only candidates')
    if archive:
        with zipfile.ZipFile(archive) as z:
            manifest=json.loads(z.read('manifest.json'))
            check('Export includes the nine Test 6 projects and excludes Born in Chaos',staged_ids<={row['projectID'] for row in manifest['files']} and 686437 not in {row['projectID'] for row in manifest['files']},'9 Test 6 projects present; Born in Chaos absent')
            embedded=['README-0.3.1.md','MOD_STRUCTURE_SCREENING.md','MISSING_JARS.txt','APPROVED_ADDITION_JARS.txt','APPROVED_STRUCTURE_ADDITIONS.csv','FARMERS_STRUCTURE_CATALOG.csv','CODE_GENERATED_PLACEMENT_ROUTES.csv']
            check('Continuation reports embedded exactly',all(z.read('overrides/'+name)==(ROOT/name).read_bytes() for name in embedded),embedded)
    check('Curated donor roster unchanged',(R/'biome-roster.json').read_bytes()==(E/'baseline-test5/biome-roster.json').read_bytes(),'40 Overworld + 2 Nether')
    report['status']='PASS (expanded scoped static gates; runtime pending)'
    report['counts'].update({'farmers_variants':20,'new_recipe_gates':11,'client_model_repairs':len(repairs['client_models']),'code_generated_ctov_routes':74})
    report['limitations'] += ['Nine Test 6 mods are installed in the manifest after a static binary audit of user-supplied JARs only; no registry load, natural generation, density, clipping or performance test has been run. Explorify Black Spiral is left enabled by user decision pending a fresh-Nether check.',
                              'Cristel spacing/separation/frequency/member-removal code is inspected; live pack priority and non-native exclusion retention are not runtime-certified.',
                              'Native resource collisions remain enumerated; recorded snapshot precedence is not a game-launch result.']
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive');p.add_argument('--report');a=p.parse_args();result=validate(a.archive)
    if a.report:Path(a.report).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(result['checks']),**result['counts']}))
