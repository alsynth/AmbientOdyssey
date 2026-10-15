"""Reproducible, narrowly scoped native balance overlay. Never edits live instances."""
import csv, hashlib, json, re, subprocess, tomllib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OV=ROOT/'release_030/overrides'
REPORT=ROOT/'docs/handoffs/integration-20261015'
BASE='b29a757'

def original(rel):
    return subprocess.check_output(['git','show',BASE+':release_030/overrides/'+rel],cwd=ROOT)

def build():
    ledger=[]
    def record(rel,key,before,after,tier,reason,target=None):
        ledger.append(dict(path=rel,key=key,before=before,after=after,boss_category=tier,
          uncapped_target=after if target is None else target,route=reason,status='SOURCE IMPLEMENTED',
          runtime_verified=False,ability_damage_verified=False))
    def save(rel,data):
        p=OV/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data,encoding='utf-8',newline='\n')
    # DD candidate is NOT a verified 497-zone rollout. Remove two provisional arena tiers.
    dd=json.loads((ROOT/'experiments/structure-difficulty-v4/candidate/config/dungeon_difficulty/difficulty_v2.json').read_text())
    held={'cataclysm:frosted_prison','cataclysm:sunken_city'}
    for world in dd['dimensions']:
        world['zones']=[z for z in world['zones'] if z['zone_matches']['structure'] not in held]
        assert world['world_matches']['dimension']=='minecraft:overworld' or not world['zones']
    with (ROOT/'experiments/structure-difficulty-v4/DD_CONSOLIDATED_OWNER_TIER_PLAN_20261015.csv').open(encoding='utf-8-sig') as f:
        decisions={r['structure_id']:r for r in csv.DictReader(f)}
    for world in dd['dimensions']:
        for zone in world['zones']:
            row=decisions.get(zone['zone_matches']['structure'],{})
            tier=row.get('selected_structure_tier')
            if tier in {'2','3','4','5','6'} and row.get('decision')!='UNREVIEWED':
                zone['difficulty']['name']='ao_tier_'+tier
    zones=[z for w in dd['dimensions'] for z in w['zones']]
    assert len(zones)==23
    assert all(z['difficulty']['name'] in {'ao_tier_'+str(t) for t in range(2,7)} for z in zones)
    save('config/dungeon_difficulty/difficulty_v2.json',json.dumps(dd,indent=2)+'\n')
    (REPORT/'dd-effective-zones.json').write_text(json.dumps({'status':'SOURCE IMPLEMENTED; REGISTRY/PRECEDENCE RUNTIME CHECK PENDING','zones':zones,'held_arena_tiers':sorted(held),'other_497_candidates':'REVIEW LATER until exact dimension, effective provider and tier proven'},indent=2)+'\n')
    # Native Cataclysm combat multipliers, never fixed/projectile/percent-HP damage.
    rel='config/cataclysm-common.toml';s=original(rel).decode()
    tiers={'ignited_revenant':6,'kobolediator':6,'ender_golem':7,'ender_guardian':7,
           'netherite_monstrosity':7,'ancient_remnant':7,'ignis':8,'maledictus':8,'leviathan':8,'scylla':9}
    for boss,tier in sorted(tiers.items(),key=lambda x:x[1]):
        attack={6:5,7:6,8:10,9:10}[tier]
        section='mobs.'+boss+'.combat_config'
        for key,value in [('health_multiplier',10.0),('attack_multiplier',float(attack))]:
            pattern=r'(\['+re.escape(section)+r'\][\s\S]*?\b'+key+r'\s*=\s*)([0-9.]+)'
            match=re.search(pattern,s);assert match,(boss,key)
            before=float(match[2]);s=s[:match.start(2)]+str(value)+s[match.end(2):]
            record(rel,section+'.'+key,before,value,tier,'Native per-boss combat_config; 1024 HP ceiling accepted; fixed abilities unchanged')
    tomllib.loads(s);save(rel,s)
    # BOMD native absolute fields. Lich only exposes missile damage, which is not ordinary attack.
    rel='config/bosses_of_mass_destruction.json5';obj=json.loads(original(rel))
    for boss,tier in [('lichConfig',5),('gauntletConfig',5),('voidBlossomConfig',5),('obsidilithConfig',9)]:
        for key,scale in [('health',7 if tier==5 else 10),('attack',4 if tier==5 else 10)]:
            if key not in obj[boss]: continue
            before=obj[boss][key];target=before*scale;after=min(target,1024) if key=='health' else target
            obj[boss][key]=after;record(rel,boss+'.'+key,before,after,tier,'Native absolute field; requested HP recorded separately from cap',target)
    save(rel,json.dumps(obj,indent=2)+'\n')
    # Species-wide dragon keys would also buff surface dragons: deliberately untouched.
    rel='config/iceandfire/iaf-common.json';obj=json.loads(original(rel))
    before=obj['hydra']['maxHealth'];obj['hydra']['maxHealth']=min(before*10,1024)
    record(rel,'hydra.maxHealth',before,obj['hydra']['maxHealth'],7,'Hydra-specific native HP; no native ordinary attack key; shared dragon keys excluded',before*10)
    save(rel,json.dumps(obj,indent=2)+'\n')
    # Bosses Rise == Block Factory. SERVER file belongs in defaultconfigs for new worlds.
    rel='config/block_factorys_bosses-server.toml';s=original(rel).decode();parsed=tomllib.loads(s)
    for group,suffix,mult in [('Boss Health','Health',10),('Base Boss Damages','Damage',10)]:
        for key,before in parsed[group].items():
            target=before*mult;after=min(target,1024) if suffix=='Health' else target
            s,n=re.subn(r'("'+re.escape(key)+r'"\s*=\s*)[0-9.]+',lambda m:m[1]+str(float(after)),s);assert n==1
            record(rel,group+'.'+key,before,after,8,'Native SERVER config; copy to defaultconfigs for newly created worlds',target)
    save(rel,s);save('defaultconfigs/block_factorys_bosses-server.toml',s)
    # Remnant ordinary attacks (phase-specific) only; preserve skill and phase thresholds.
    for boss,tier in [('ossukage',7),('kotsukage',7),('umbrakar',8)]:
        rel='config/remnant/bosses/'+boss+'.json';obj=json.loads(original(rel))
        for key,before in list(obj.items()):
            if key in {'max_health','max_health_phase_1'} or key.startswith('attack_damage'):
                hp=key.startswith('max_health');target=before*(10 if hp or tier==8 else 6);after=min(target,1024) if hp else target
                obj[key]=after;record(rel,key,before,after,tier,'Native per-boss JSON, ordinary phase attack; skill values unchanged',target)
        save(rel,json.dumps(obj,indent=2)+'\n')
    # Iron's normal Dead King prepareAttributes(): 500 HP / 10 melee in exact 3.16.3 JAR.
    rel='config/irons_spellbooks-server.toml';s=original(rel).decode()
    for key,target in [('additionalHealth',4500.0),('additionalAttackDamage',50.0)]:
        pattern=r'(\["Boss Config"\."Dead King"\][\s\S]*?\b'+key+r'\s*=\s*)([0-9.]+)'
        m=re.search(pattern,s);assert m;s=s[:m.start(2)]+str(target)+s[m.end(2):]
        record(rel,'Dead King.'+key,float(m[2]),target,6,'T7 combat x10/x6; native additive SERVER fields; ominous resets may override HP; spell power unchanged')
    # Reviewed last: Tyros' additive fields preserve soul mode and native participant scaling.
    for key,target in [('additionalHealth',9000.0),('additionalAttackDamage',180.0)]:
        pattern=r'(\["Boss Config"\.Tyros\][\s\S]*?\b'+key+r'\s*=\s*)([0-9.]+)'
        m=re.search(pattern,s);assert m;s=s[:m.start(2)]+str(target)+s[m.end(2):]
        record(rel,'Tyros.'+key,float(m[2]),target,9,'Native additive SERVER fields, 1000 HP/20 melee baseline; Stronger Fire Boss soul-mode untouched; HP capped')
    save(rel,s);save('defaultconfigs/irons_spellbooks-server.toml',s)
    # Remove inactive configs, template overrides and held Sky Arena DD refs from future source.
    removed=[]
    for rel in ['config/sky_arena.json','config/skyarena-common.toml','config/cristellib/skyarena/structure_placement_config.json5','config/cristellib/skyarena/structure_toggle_config.json5']:
        removed.append(rel)
        p=OV/rel
        if p.exists():p.unlink()
    (REPORT/'native-balance-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
    (REPORT/'removed-source-paths.json').write_text(json.dumps(removed,indent=2)+'\n')
    print(json.dumps({'native_field_changes':len(ledger),'dd_zones':len(zones),'removed_skyarena_configs':len(removed),'runtime_verified':False}))

if __name__=='__main__':build()
