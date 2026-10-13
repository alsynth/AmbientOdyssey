"""Read-only installed-resource reconciliation and reproducible AO difficulty lab.

Presence is never generation proof. No instance or JAR is modified.
"""
import argparse, collections, copy, csv, hashlib, json, re, zipfile, tomllib, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT/'docs/balance/AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv'
RESOURCE = re.compile(r'^data/([^/]+)/(worldgen/structure|worldgen/structure_set|worldgen/template_pool|tags/worldgen/biome|dimension|loot_table|trial_spawner|twilight/biome_terrain_data)/(.*)\.json$')
NBT = re.compile(r'^data/([^/]+)/structures?/(.*)\.nbt$')
DIMENSIONS = {'Overworld':'minecraft:overworld','Nether':'minecraft:the_nether','The End':'minecraft:the_end','Twilight Forest':'twilightforest:twilight_forest','Aether':'aether:the_aether','Eternal Starlight':'eternal_starlight:starlight'}
VANILLA_NETHER = {'nether_wastes','soul_sand_valley','crimson_forest','warped_forest','basalt_deltas'}
VANILLA_END = {'the_end','small_end_islands','end_midlands','end_highlands','end_barrens'}
# Explicit ordinary entity IDs; no mod-wide patterns, named bosses or summons.
MOBS = ['zombie','husk','drowned','zombie_villager','skeleton','stray','wither_skeleton','bogged','spider','cave_spider','pillager','vindicator','witch','silverfish','endermite','blaze','piglin_brute']
BUDGETS = {0:(0,0,0),1:(0,0,0),2:(.10,.05,.5),3:(.20,.10,1),4:(.30,.15,1.5),5:(.40,.20,2),6:(.50,.25,2.5)}

def sha(data): return hashlib.sha256(data).hexdigest()
def write_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def read_resource_json(data):
    # Minecraft's parser accepts comments; strip only outside quoted strings.
    text=data.decode('utf-8-sig')
    try:return json.loads(text)
    except json.JSONDecodeError:pass
    out=[];i=0;quoted=False;escaped=False
    while i<len(text):
        ch=text[i]
        if quoted:
            out.append(ch)
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch=='"':quoted=False
            i+=1;continue
        if ch=='"':quoted=True;out.append(ch);i+=1;continue
        if text[i:i+2]=='//':
            while i<len(text) and text[i] not in '\r\n':i+=1
            continue
        if text[i:i+2]=='/*':
            end=text.find('*/',i+2)
            if end<0:raise ValueError('Unclosed JSON comment')
            out.append(' ');i=end+2;continue
        out.append(ch);i+=1
    return json.loads(''.join(out))

def nbt_string_links(data,key):
    # Exact serialized TAG_String name/value markers; discovery leads, not
    # proof that a jigsaw block is selected or that its connector can attach.
    marker=b'\x08'+len(key).to_bytes(2,'big')+key.encode();result=set();start=0
    while True:
        pos=data.find(marker,start)
        if pos<0:break
        pos+=len(marker);length=int.from_bytes(data[pos:pos+2],'big');value=data[pos+2:pos+2+length]
        try:
            text=value.decode('utf-8')
            if re.fullmatch(r'[a-z0-9_.-]+:[a-z0-9_./-]+',text):result.add(text)
        except UnicodeDecodeError:pass
        start=pos+2+length
    return sorted(result)

def inventory(instance, vanilla):
    resources=collections.defaultdict(list); templates={}; roster=[]; errors=[]; builtins=[]
    def add(provider, name, data):
        m=RESOURCE.match(name)
        if m:
            try: obj=read_resource_json(data)
            except (ValueError,UnicodeDecodeError) as e:
                errors.append({'provider':provider,'path':name,'error':str(e)});return
            resources[(m[2],m[1]+':'+m[3])].append({'provider':provider,'path':name,'sha256':sha(data),'data':obj})
        n=NBT.match(name)
        if n:
            try:raw=zlib.decompressobj(31).decompress(data) if data[:2]==b'\x1f\x8b' else data
            except zlib.error:raw=b''
            templates.setdefault(n[1]+':'+n[2],[]).append({'provider':provider,'path':name,'sha256':sha(data),'pool_reference_leads':nbt_string_links(raw,'pool'),'loot_reference_leads':nbt_string_links(raw,'LootTable')})
    for jar in sorted((instance/'mods').glob('*.jar')) + [vanilla]:
        before=jar.stat();data=jar.read_bytes();entry={'jar':jar.name,'sha256':sha(data),'bytes':len(data),'metadata':{}}
        after=jar.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise RuntimeError('JAR changed during scan: '+jar.name)
        try:
            with zipfile.ZipFile(jar) as z:
                for meta in ('META-INF/neoforge.mods.toml','META-INF/mods.toml','fabric.mod.json'):
                    if meta in z.namelist(): entry['metadata'][meta]=z.read(meta).decode('utf-8')
                for n in z.namelist():
                    if RESOURCE.match(n) or NBT.match(n): add(jar.name,n,z.read(n))
                    elif '/data/' in n and n.endswith(('.json','.nbt')):
                        # Optional built-in packs are not assumed enabled.
                        builtins.append({'provider':jar.name,'path':n})
        except (OSError,zipfile.BadZipFile) as e: errors.append({'provider':jar.name,'error':str(e)})
        roster.append(entry)
    for folder in (instance/'config/paxi/datapacks',instance/'global_packs/required_data',instance/'datapacks'):
        if not folder.exists(): continue
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.suffix=='.json' and '/data/' in path.as_posix():
                add('local:'+path.relative_to(instance).as_posix().split('/data/')[0], 'data/'+path.as_posix().split('/data/',1)[1],path.read_bytes())
            elif path.is_file() and path.suffix=='.zip':
                with zipfile.ZipFile(path) as z:
                    for n in z.namelist():
                        if RESOURCE.match(n) or NBT.match(n):add('local:'+path.relative_to(instance).as_posix(),n,z.read(n))
    return resources,templates,roster,errors,builtins

def unique(resources, kind, ident):
    values=resources.get((kind,ident),[])
    return values[0]['data'] if values and len({v['sha256'] for v in values})==1 else None

def biome_members(resources, value, seen=None):
    seen=set() if seen is None else seen
    if isinstance(value,list):
        result=set(); unresolved=False
        for v in value:
            a,b=biome_members(resources,v,seen.copy());result|=a;unresolved|=b
        return result,unresolved
    if isinstance(value,dict):
        ident=value.get('id','')
        if value.get('required') is False and ident.startswith('#') and ('tags/worldgen/biome',ident[1:]) not in resources:return set(),False
        value=ident
    if not isinstance(value,str):return set(),True
    if not value.startswith('#'):return {value},False
    key=value[1:]
    if key in seen:return set(),True
    seen.add(key); providers=resources.get(('tags/worldgen/biome',key),[])
    if not providers:return set(),True
    # Tags merge unless replaced; ambiguous replace precedence is held.
    if len(providers)>1 and any(x['data'].get('replace',False) for x in providers):return set(),True
    return biome_members(resources,[v for p in providers for v in p['data'].get('values',[])],seen)

def biome_dimension(biome):
    ns,name=biome.split(':',1) if ':' in biome else ('minecraft',biome)
    if ns=='minecraft':
        return 'minecraft:the_nether' if name in VANILLA_NETHER else 'minecraft:the_end' if name in VANILLA_END else 'minecraft:overworld'
    # Custom dimensions' explicit biome source is handled separately.
    return None

def declared_dimensions(resources):
    result=collections.defaultdict(set)
    for (kind,ident),providers in resources.items():
        if kind!='dimension':continue
        obj=unique(resources,kind,ident)
        if obj is None:continue
        source=obj.get('generator',{}).get('biome_source',{})
        vals=[]
        if source.get('type')=='twilightforest:twilight_biomes':
            terrain=unique(resources,'twilight/biome_terrain_data',source.get('terrain_data',''))
            if terrain:
                for entry in terrain.get('biome_landscape',[]):
                    vals.append(entry.get('key_biome'))
                    vals.extend(entry.get('biome_layers',{}).values())
        if isinstance(source.get('biome'),str):vals.append(source['biome'])
        for e in source.get('biomes',[]):
            if isinstance(e,dict) and isinstance(e.get('biome'),str):vals.append(e['biome'])
        for b in vals:
            if isinstance(b,str):result[b].add(ident)
    return result

def reachable(resources,templates,structure):
    obj=unique(resources,'worldgen/structure',structure)
    if not obj:return [],[],True
    pools=set();found=set();pending=[obj.get('start_pool')];unresolved=not isinstance(obj.get('start_pool'),str)
    while pending:
        pool=pending.pop()
        if not isinstance(pool,str) or pool in pools:continue
        pools.add(pool)
        if pool=='minecraft:empty':continue
        data=unique(resources,'worldgen/template_pool',pool)
        if data is None:unresolved=True;continue
        pending.append(data.get('fallback'))
        def walk(v):
            if isinstance(v,dict):
                if isinstance(v.get('location'),str):found.add(v['location'])
                for a in v.values():walk(a)
            elif isinstance(v,list):
                for a in v:walk(a)
        before=set(found);walk(data.get('elements',[]))
        for template in found-before:
            providers=templates.get(template,[])
            if len({p['sha256'] for p in providers})>1:unresolved=True
            for provider in providers:pending.extend(provider.get('pool_reference_leads',[]))
    # Includes serialized pool-reference leads, not proven connector selection.
    return sorted(pools), sorted(x for x in found if x in templates), unresolved

def reconcile(rows,resources,templates,nbt_rows,disabled=None,builtin_ids=None):
    dimmap=declared_dimensions(resources); result=[]
    disabled=disabled or {}
    builtin_ids=builtin_ids or set()
    for tag,dimension in [('minecraft:is_overworld','minecraft:overworld'),('minecraft:is_nether','minecraft:the_nether'),('minecraft:is_end','minecraft:the_end'),('c:is_overworld','minecraft:overworld'),('c:is_nether','minecraft:the_nether'),('c:is_end','minecraft:the_end'),('c:in_overworld','minecraft:overworld'),('c:in_nether','minecraft:the_nether'),('c:in_end','minecraft:the_end')]:
        members,unknown=biome_members(resources,'#'+tag)
        if not unknown:
            for b in members:dimmap[b].add(dimension)
    nbt_index={(r['jar'],r['structure_nbt']):r for r in nbt_rows}
    set_ids=collections.defaultdict(list)
    for (kind,ident),providers in resources.items():
        if kind=='worldgen/structure_set':
            for p in providers:
                for s in p['data'].get('structures',[]):
                    if isinstance(s,dict):set_ids[s.get('structure','')].append(ident)
    for row in rows:
        r=dict(row);ident=r['registry_id'];providers=resources.get(('worldgen/structure',ident),[])
        obj=unique(resources,'worldgen/structure',ident)
        archived=any(s in r['tier_source'].lower() for s in ('superseded','archived'))
        status='archived' if archived else 'absent_root_resource' if not providers else 'overridden_precedence_unresolved' if obj is None else 'installed_resource_candidate'
        if not archived and ident in disabled:status='inactive_native_replacement'
        biomes,unresolved=biome_members(resources,obj.get('biomes') if obj else None)
        dims=set()
        for b in biomes:
            if biome_dimension(b):dims.add(biome_dimension(b))
            dims |= dimmap.get(b,set())
            if not biome_dimension(b) and not dimmap.get(b):unresolved=True
        requested=DIMENSIONS.get(r['dim'].split(' /')[0])
        dimension=next(iter(dims)) if len(dims)==1 and not unresolved else ''
        pools,nbts,pool_unknown=reachable(resources,templates,ident)
        indicators=collections.Counter();mechanic_paths=[];spawn_entities=set()
        for template in nbts:
            for t in templates[template]:
                n=nbt_index.get((t['provider'],t['path']))
                if n:
                    for k in ('mob_spawners','trial_spawners','vaults','equipped_mob_or_spawner_indicators'):indicators[k]+=int(n[k])
                    mechanic_paths.append(t['provider']+'!'+t['path'])
                    spawn_entities.update(x for x in n.get('spawner_entity_ids','').split(' | ') if x)
        approved=r['tier_source'].startswith(('V2 approved','Explicit user decision'))
        tier=int(r['tier']) if r['tier'].isdigit() else None
        reasons=[]
        if archived: reasons.append('archived')
        if not approved:reasons.append('tier_not_approved_for_0_6')
        if tier is None or tier>6:reasons.append('outside_0_6')
        if status!='installed_resource_candidate':reasons.append(status)
        if not dimension:reasons.append('dimension_unresolved')
        elif requested is not None and dimension!=requested:reasons.append('catalogue_dimension_conflict')
        if not set_ids.get(ident):reasons.append('no_root_structure_set_reference')
        if ident in builtin_ids:reasons.append('optional_builtin_override_activation_unresolved')
        if ident in ('skyarena:sky_arena','skyarena:ice_arena'):reasons.append('native_wave_scaler_requires_separate_budget')
        r.update(installed_status=status,replacement_evidence=disabled.get(ident,''),providers=' | '.join(p['provider'] for p in providers),resource_hashes=' | '.join(p['sha256'] for p in providers),biome_reference=json.dumps(obj.get('biomes') if obj else None),resolved_biomes=' | '.join(sorted(biomes)),dimension_evidence=' | '.join(sorted(dims)),implementation_dimension=dimension,structure_sets=' | '.join(sorted(set(set_ids.get(ident,[])))),start_pool_templates=' | '.join(nbts),template_spawners=indicators['mob_spawners'],template_trial_spawners=indicators['trial_spawners'],template_vaults=indicators['vaults'],equipment_indicators=indicators['equipped_mob_or_spawner_indicators'],mechanic_evidence=' | '.join(mechanic_paths),pool_scan_incomplete=str(pool_unknown),runtime_generation='NOT_TESTED',implementation='hold' if reasons else 'preserve_natural' if tier<2 else 'attribute_pilot',hold_reasons=' | '.join(reasons))
        compatible=spawn_entities & {'minecraft:'+name for name in MOBS}
        if r['implementation']=='attribute_pilot' and not compatible:
            r['implementation']='hold';r['hold_reasons']='compatible_ordinary_encounter_unproven'
        r.update(template_spawner_entity_ids=' | '.join(sorted(spawn_entities)),dd_compatible_template_entities=' | '.join(sorted(compatible)),encounter_control_status='NOT_FULLY_TUNED: attribute-only pilot; equipment/composition/loot/native mechanics unchanged' if r['implementation']=='attribute_pilot' else 'NO_CHANGE',ordinary_mob_coverage='POOL_GRAPH_TEMPLATE_LEAD_ONLY' if compatible else 'UNPROVEN: no compatible spawn entity in traversed pool-reference leads',catalogue_dimension_reconciliation='Original dimension preserved; native explicit biome-source dimension used for implementation' if requested is None and dimension else 'No technical relabeling applied')
        result.append(r)
    # Different approved tiers for the same dimension/ID must never silently win.
    groups=collections.defaultdict(list)
    for r in result:
        if r['implementation']!='hold':groups[(r['implementation_dimension'],r['registry_id'])].append(r)
    for group in groups.values():
        if len({r['tier'] for r in group})>1:
            for r in group:r.update(implementation='hold',hold_reasons='conflicting_approved_tiers')
    return result

def config_for(rows):
    c=json.loads((ROOT/'experiments/ao-balance-lab/config/dungeon_difficulty_v2.json').read_text())
    base=copy.deepcopy(c['difficulty_types'][0]);c['difficulty_types']=[];c['dimensions']=[]
    for tier,(health,damage,armor) in BUDGETS.items():
        t=copy.deepcopy(base);t['name']='ao_tier_'+str(tier)
        e=t['entities'][0];e['entity_matches']['type']='~^minecraft:(?:'+'|'.join(MOBS)+')$'
        for a,value in zip(e['attributes'],(health,damage,armor)):a.update(value=value,offset=0,randomness=0)
        t['entities']=[] if tier<2 else [e]
        c['difficulty_types'].append(t)
    bydim=collections.defaultdict(dict)
    for r in rows:
        if r['implementation']=='hold':continue
        bydim[r['implementation_dimension']][r['registry_id']]=int(r['tier'])
    for dimension,ids in sorted(bydim.items()):
        # Specific structure rules only; no blanket dimension/biome difficulty.
        c['dimensions'].append({'world_matches':{'dimension':dimension},'zones':[{'zone_matches':{'biome':None,'structure':ident},'difficulty':{'name':'ao_tier_'+str(tier),'level':1}} for ident,tier in sorted(ids.items())],'zone_specifiers':[],'entities':[]})
    return c

def build(instance, vanilla, output):
    evidence=ROOT/'docs/balance/v3-evidence'
    resources,templates,roster,errors,builtins=inventory(instance,vanilla)
    if not any('modId = "dungeon_difficulty"' in text and 'version = "3.9.2+1.21.1"' in text for item in roster for text in item['metadata'].values()):
        raise RuntimeError('Requires source-inspected Dungeon Difficulty 3.9.2+1.21.1')
    rows=list(csv.DictReader(CAT.open(encoding='utf-8-sig')))
    nbt_path=evidence/'ENCOUNTER_NBT.csv'
    if not nbt_path.exists() or not nbt_path.with_suffix('.errors.json').exists():raise RuntimeError('Complete the encounter NBT census before packaging')
    nbt_rows=list(csv.DictReader(nbt_path.open(encoding='utf-8')))
    disabled={};replacement_configs={}
    for mod,key,ident in [('betteroceanmonuments','Disable Vanilla Ocean Monuments','minecraft:monument'),('betterfortresses','Disable Vanilla Nether Fortresses','minecraft:fortress')]:
        path=instance/('config/'+mod+'-neoforge-1_21.toml')
        if path.exists():
            data=tomllib.loads(path.read_text(encoding='utf-8'));group=next(iter(data.values()))
            replacement_configs[path.name]={'sha256':sha(path.read_bytes()),'data':data}
            if group.get('General',{}).get(key) is True:disabled[ident]=path.name+': '+key+' = true'
    builtin_ids=set()
    for item in builtins:
        name='data/'+item['path'].split('/data/',1)[1];m=RESOURCE.match(name)
        if m and m[2]=='worldgen/structure':builtin_ids.add(m[1]+':'+m[3])
    reconciled=reconcile(rows,resources,templates,nbt_rows,disabled,builtin_ids);c=config_for(reconciled)
    write_json(evidence/'REPLACEMENT_CONFIGS.json',replacement_configs)
    sky_config=instance/'config/sky_arena.json'
    if sky_config.exists():
        sky=json.loads(sky_config.read_text(encoding='utf-8'))
        write_json(evidence/'SKY_ARENA_NATIVE_CONTROLS.json',{'path':'config/sky_arena.json','sha256':sha(sky_config.read_bytes()),'data':sky,'implementation':'PRESERVED; native points/stat/group/reward progression requires a separate wave budget; no DD rule','runtime_tested':False})
    write_csv(evidence/'RECONCILED_CATALOGUE.csv',reconciled)
    write_csv(evidence/'APPROVED_TIER_MAPPING.csv',[r for r in reconciled if r['tier_source'].startswith(('V2 approved','Explicit user decision')) and r['tier'].isdigit() and int(r['tier'])<=6])
    write_csv(evidence/'ENCOUNTER_CONTROL_GAPS.csv',[r for r in reconciled if r['implementation']=='attribute_pilot' or 'compatible_ordinary_encounter_unproven' in r['hold_reasons']])
    write_json(evidence/'INSTALLED_JARS.json',roster)
    write_json(evidence/'RESOURCE_ERRORS.json',errors)
    write_json(evidence/'OPTIONAL_BUILTIN_RESOURCES.json',builtins)
    links=[{'template':ident,'provider':t['provider'],'path':t['path'],'sha256':t['sha256'],'pool_reference_leads':' | '.join(t['pool_reference_leads']),'loot_reference_leads':' | '.join(t['loot_reference_leads']),'confidence':'SERIALIZED_TAG_STRING_LEADS; connector choice and loot reachability unproven'} for ident,ts in sorted(templates.items()) for t in ts if t['pool_reference_leads'] or t['loot_reference_leads']]
    if links:write_csv(evidence/'TEMPLATE_RESOURCE_LINKS.csv',links)
    collisions=[{'kind':kind,'id':ident,'providers':[{k:v for k,v in p.items() if k!='data'} for p in providers]} for (kind,ident),providers in sorted(resources.items()) if len({p['sha256'] for p in providers})>1]
    write_json(evidence/'RESOURCE_COLLISIONS.json',collisions)
    write_json(evidence/'TRIAL_AND_LOOT_RESOURCES.json',[{'kind':kind,'id':ident,'providers':providers} for (kind,ident),providers in sorted(resources.items()) if kind=='trial_spawner'])
    loot=[{'loot_table':ident,'provider':p['provider'],'path':p['path'],'sha256':p['sha256'],'pool_count':len(p['data'].get('pools',[])),'functions':json.dumps(p['data'].get('functions',[])),'container_role':'UNCLASSIFIED; requires reachable-template and economy review'} for (kind,ident),providers in sorted(resources.items()) if kind=='loot_table' for p in providers]
    if loot:write_csv(evidence/'LOOT_TABLE_INDEX.csv',loot)
    profile=json.loads((instance/'minecraftinstance.json').read_text(encoding='utf-8'))
    actual_pins=[{'projectID':a['addonID'],'fileID':a['installedFile']['id'],'jar':a['fileNameOnDisk'],'enabled':a.get('isEnabled',True)} for a in profile.get('installedAddons',[]) if a.get('installedFile') and a.get('fileNameOnDisk')]
    manifest=profile.get('manifest',{});original_pins={(f['projectID'],f['fileID']) for f in manifest.get('files',[])}
    current={(f['projectID'],f['fileID']) for f in actual_pins}
    write_json(evidence/'CURRENT_PROFILE.json',{'name':instance.name,'minecraft':profile.get('gameVersion'),'loader':profile.get('baseModLoader',{}).get('name'),'manifest_version':manifest.get('version'),'manifest_pin_count':len(original_pins),'installed_addons':actual_pins,'changed_or_added_pins':sorted([{'projectID':p,'fileID':f} for p,f in current-original_pins],key=lambda x:x['projectID']),'missing_or_replaced_manifest_pins':sorted([{'projectID':p,'fileID':f} for p,f in original_pins-current],key=lambda x:x['projectID']),'manifest_is_not_current_binary_roster':current!=original_pins})
    remnant={}
    for item in roster:
        for meta,text in item['metadata'].items():
            if meta.endswith('.toml'):
                try:parsed=tomllib.loads(text)
                except tomllib.TOMLDecodeError:continue
                for mod in parsed.get('mods',[]):
                    if mod.get('modId') in ('remnant_bosses','geckolib','jauml'):remnant[mod['modId']]={'jar':item['jar'],'sha256':item['sha256'],'version':mod.get('version'),'dependencies':parsed.get('dependencies',{}).get(mod['modId'],[])}
    comparisons=[]
    for path in sorted((instance/'config/remnant').rglob('*.json')):
        actual=json.loads(path.read_text(encoding='utf-8'));old=ROOT/'release_030/overrides'/path.relative_to(instance)
        olddata=json.loads(old.read_text(encoding='utf-8')) if old.exists() else {}
        comparisons.append({'path':path.relative_to(instance).as_posix(),'sha256':sha(path.read_bytes()),'current':actual,'added_keys':sorted(set(actual)-set(olddata)),'removed_keys':sorted(set(olddata)-set(actual)),'changed_values':{k:{'source':olddata[k],'installed':actual[k]} for k in actual.keys()&olddata.keys() if actual[k]!=olddata[k]}})
    write_json(evidence/'REMNANT_COMPATIBILITY.json',{'installed':remnant,'loader':profile.get('baseModLoader',{}).get('name'),'config_comparison_to_legacy_source':comparisons,'metadata_dependency_check':'NeoForge 21.1.252 >=21.1.219; MC1.21.1; GeckoLib4.9.3 >=4.8.4; jauml2.3.1 >=1.2.0. Static metadata only; dedicated runtime pending.','runtime_tested':False})
    configpath=ROOT/'experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json'
    write_json(configpath,c)
    current_names=sorted(p.name for p in (instance/'mods').glob('*.jar'))
    if current_names!=sorted(item['jar'] for item in roster if item['jar']!=vanilla.name):raise RuntimeError('Installed roster changed during scan; rerun')
    nbt_errors=evidence/'ENCOUNTER_NBT.errors.json'
    mod_templates=sum(1 for ts in templates.values() for t in ts if t['provider']!=vanilla.name and not t['provider'].startswith('local:'))
    decode_errors=len(json.loads(nbt_errors.read_text()))
    report={'instance':instance.name,'source_commit':'b387dc0','catalogue_rows':len(rows),'physical_mod_jars':len(roster)-1,'resource_candidates':dict(collections.Counter(r['installed_status'] for r in reconciled)),'implementation':dict(collections.Counter(r['implementation'] for r in reconciled)),'zones':sum(len(d['zones']) for d in c['dimensions']),'resource_errors':len(errors),'collisions':len(collisions),'root_template_resources':sum(len(ts) for ts in templates.values()),'root_mod_template_resources':mod_templates,'nbt_decoded_templates':mod_templates-decode_errors,'nbt_templates_with_indicators':len(nbt_rows),'nbt_decode_errors':decode_errors,'loot_table_provider_records':len(loot),'runtime_tested':False,'nbt_indicators_do_not_prove_reachability':True,'config_sha256':sha(configpath.read_bytes())}
    write_json(evidence/'SUMMARY.json',report)
    original=instance/'config/dungeon_difficulty/difficulty_v2.json'
    backup=ROOT/'experiments/structure-difficulty-v3/rollback/config/dungeon_difficulty/difficulty_v2.json'
    backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(original.read_bytes())
    report['rollback_sha256']=sha(original.read_bytes());write_json(evidence/'SUMMARY.json',report)
    output.parent.mkdir(parents=True,exist_ok=True)
    files={p.relative_to(ROOT/'experiments/structure-difficulty-v3').as_posix():p.read_bytes() for p in (configpath,backup)}
    files['README.md']=(ROOT/'docs/balance/STRUCTURE_DIFFICULTY_V3_IMPLEMENTATION.md').read_bytes()
    for p in sorted(evidence.iterdir()):
        if p.is_file():files['evidence/'+p.name]=p.read_bytes()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
    write_json(output.with_suffix('.sha256.json'),{'sha256':sha(output.read_bytes()),'kind':'experimental config kit; not a full import','runtime_tested':False})
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--instance',type=Path,required=True);p.add_argument('--vanilla-jar',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.instance,a.vanilla_jar,a.output)
