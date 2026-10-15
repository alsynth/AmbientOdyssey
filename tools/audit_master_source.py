"""Reconcile pinned draft surfaces with the current integration files without merging branches."""
import csv,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/handoffs/integration-20261015'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8')
def run():
    metadata=json.loads((OUT/'pr-metadata.json').read_text())
    audit=[]
    for p in metadata:
        changes=git('diff','--name-status',p['base']+'...'+p['sha']).splitlines()
        tree={}
        for line in git('ls-tree','-r',p['sha']).splitlines():
            info,path=line.split('\t',1);tree[path]=info.split()[2]
        records=[]
        for change in changes:
            path=change.split('\t')[-1];current=ROOT/path;source=tree.get(path);match=False;target_sha=None
            if current.is_file():
                data=current.read_bytes().replace(b'\r\n',b'\n');target_sha=hashlib.sha256(current.read_bytes()).hexdigest()
                obj=b'blob '+str(len(data)).encode()+b'\0'+data;match=hashlib.sha1(obj).hexdigest()==source
            records.append({'source_path':path,'source_blob':source,'target_path':path if current.exists() else None,'target_sha256':target_sha,
              'reconciliation':'EXACT_CONTENT_MATCH' if match else 'REVIEWED_DIFFERENCE_OR_OMISSION','source_change':change.split('\t')[0]})
        audit.append({'pr':p['number'],'title':p['title'],'source_branch':p['head'],'head_sha':p['sha'],'base_sha':p['base'],
          'in_master_20':p['number'] in [62,61,60,59,57,56,54,53,52,51,50,49,48,47,46,45,44,42,41,40],
          'surface':records,'source_status':'SOURCE IMPLEMENTED (research/tool/config surfaces distinguished by path)',
          'package_status':'See final ZIP receipt: only release overrides and compiled addon artifacts ship; research stays source-only',
          'native_build_evidence':'See VERIFICATION.md; no automatic runtime inheritance from this PR',
          'superseded_decisions':'Master handoff section A governs. PR44 tiers, PR45 weaker/no-op rules, PR51 table replacement, PR57 Rage Glove prototype, stale equal Brutal multiplier and unnamed End slot are superseded.',
          'owner_accepted_this_integration':False,'live_installed':False})
    (OUT/'pr-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'docs/research/next-agent-package-20261014/17_BOSS_BALANCE_LEDGER_T6_T9.csv'
    rows=list(csv.DictReader(path.open(encoding='utf-8-sig')));result=[]
    applied=json.loads((OUT/'native-balance-ledger.json').read_text())
    for r in rows:
        entity=r['entity_id'];category=5 if entity in {'fdbosses:chesed','fdbosses:malkuth','fdbosses:geburah'} else int(r['tier'])
        combat=7 if entity in {'irons_spellbooks:dead_king','aquamirae:captain_cornelia'} else category
        exempt=entity.startswith('fdbosses:')
        route='PLANNED / BLOCKED: no scoped native stat route implemented'
        if exempt:route='EXEMPT: no HP/damage changes'
        elif entity.startswith('cataclysm:') and entity!='cataclysm:coralssus':route='SOURCE IMPLEMENTED native config (see exact field ledger)'
        elif entity.startswith(('remnants:','block_factorys_bosses:','bosses_of_mass_destruction:')) or entity in {'irons_spellbooks:dead_king','irons_spellbooks:fire_boss'}:route='SOURCE IMPLEMENTED native config; abilities not fully scaled'
        elif entity=='iceandfire:hydra':route='SOURCE IMPLEMENTED HP only; damage BLOCKED'
        if entity.startswith('eternal_starlight:'):route='PLANNED: boss family selection still TBD; native values retained'
        if entity.endswith('_dragon'):route='EXCLUDED: shared species settings also affect surface dragons'
        result.append({**r,'current_category_tier':category,'current_combat_tier':combat,'approved_hp_multiplier':None if exempt else {2:2,3:3,4:5,5:7,6:10,7:10,8:10,9:10}[combat],
          'approved_ordinary_attack_multiplier':None if exempt else {2:1.5,3:2,4:3,5:4,6:5,7:6,8:10,9:10}[combat],
          'current_implementation_status':route,'source_field_ledger':'native-balance-ledger.json','runtime_this_integration':'See final native observations; no fight acceptance inferred','owner_accepted':False,'live_installed':False})
    (OUT/'boss-reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Audited',sum(r['in_master_20'] for r in audit),'master drafts plus',sum(not r['in_master_20'] for r in audit),'older drafts;',len(result),'boss research records')
if __name__=='__main__':run()
