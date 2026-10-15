"""Validate the actual private import, with explicit inherited pins and custom JARs."""
import argparse, hashlib, io, json, re, tomllib, zipfile
from pathlib import Path
import json5

ROOT=Path(__file__).resolve().parents[1]
def validate(path):
    errors=[];warnings=[];counts={'json':0,'json5':0,'toml':0};jars={};shader_sources=[]
    with zipfile.ZipFile(path) as z:
        names=z.namelist();assert z.testzip() is None and len(names)==len(set(names))
        manifest=json.loads(z.read('manifest.json'));pins=manifest['files'];assert len(pins)==337
        assert len({r['projectID'] for r in pins})==337
        assert not any(r['projectID'] in {1141465,1023913,1657433} for r in pins)
        for n in names:
            try:
                if '/shaderpacks/' in n and '/shaders/' in n and n.endswith('.json'):
                    shader_sources.append(n);continue # Shader preprocessor syntax, not plain JSON.
                if n.endswith(('.json','.mcmeta')):
                    data=z.read(n).decode('utf-8-sig')
                    try:json.loads(data);counts['json']+=1
                    except json.JSONDecodeError:json5.loads(data);counts['json5']+=1
                elif n.endswith('.json5'):json5.loads(z.read(n).decode('utf-8-sig'));counts['json5']+=1
                elif n.endswith('.toml'):tomllib.loads(z.read(n).decode('utf-8-sig'));counts['toml']+=1
                if n.startswith('overrides/mods/') and n.endswith('.jar'):
                    data=z.read(n);jars[n]=hashlib.sha256(data).hexdigest()
                    with zipfile.ZipFile(io.BytesIO(data)) as j:
                        if j.testzip() is not None:errors.append('JAR CRC '+n)
                        if 'ao-campaign-' in n:
                            glm=json.loads(j.read('data/neoforge/loot_modifiers/global_loot_modifiers.json'));assert glm['entries']==['ao_campaign:grand_treasure'] and not glm.get('replace')
                            assert not any('rage_glove' in e for e in glm['entries'])
                            for need in ('dev/ambientodyssey/campaign/BossRewards.class','dev/ambientodyssey/campaign/GrandTreasure.class','ao_loot_policy.json'):assert need in j.namelist(),need
                            assert 'ao-campaign-0.3.1-experimental' in n,n
                            pol=json.loads(j.read('ao_loot_policy.json'));assert pol['regalia'] and len(pol['unique_weapons'])>=50 and pol['grand_treasure']
                        if 'ao-starter-chest-' in n:assert 'data/minecraft/loot_table/chests/spawn_bonus_chest.json' not in j.namelist()
            except Exception as exc:errors.append({'path':n,'error':str(exc)})
        assert len(jars)==10 and not any('probe' in n for n in jars)
        assert not any(n.endswith('gem_loot_injection.json') and 'ao_starter_apotheosis_exemptions' in n for n in names),'gem suppression must be gone'
        assert sum('ao-campaign-' in n for n in jars)==1
        solo=tomllib.loads(z.read('overrides/defaultconfigs/ftb_solo_quests-server.toml').decode())
        assert solo['teamSyncEnabled'] is False,'FTB Solo Quests must not enable optional team sync'
        dd=json.loads(z.read('overrides/config/dungeon_difficulty/difficulty_v2.json'))
        zones=[v for d in dd['dimensions'] for v in d['zones']];assert len(zones)==23
        assert all(v['difficulty']['name'] not in {'ao_tier_0','ao_tier_1'} for v in zones)
        assert all('mechanical_nest' not in v['zone_matches']['structure'] for v in zones)
        brutal=json5.loads(z.read('overrides/config/brutalbosses.json').decode())
        assert all(brutal[k][k]==v for k,v in {'damageMultiplier':3,'healthMultiplier':4,'globalBossSpawnChance':70,'minDistance':30}.items())
        for n in ['irons_spellbooks-server.toml','block_factorys_bosses-server.toml']:
            assert z.read('overrides/config/'+n)==z.read('overrides/defaultconfigs/'+n)
        campaign=[n for n in names if n.startswith('overrides/config/questlog/quests/') and n.endswith('.json')]
        assert len(campaign)==153
        # Multiple datapacks may intentionally override resources; report every collision.
        resources={}
        for n in names:
            if '/datapacks/' in n and '/data/' in n:
                key=n.split('/data/',1)[1];resources.setdefault(key,[]).append(n)
        collisions={k:v for k,v in resources.items() if len(v)>1}
        warnings.append('Paxi winner precedence requires engine observations; collisions are not automatically errors')
    return {'status':'STATIC VERIFIED' if not errors else 'STATIC CHECKS FAILED','counts':counts,'errors':errors,'warnings':warnings,
      'custom_jars':jars,'paxi_resource_collisions':collisions,'shader_preprocessor_sources_not_json_linted':shader_sources,'cf_references':337,'dd_zones':23,'quest_files':153,
      'minecraft_runtime_tested_by_this_validator':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('zip',type=Path);p.add_argument('--report',type=Path,required=True);a=p.parse_args();r=validate(a.zip)
    a.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['custom_jars','paxi_resource_collisions']},indent=2));raise SystemExit(bool(r['errors']))
