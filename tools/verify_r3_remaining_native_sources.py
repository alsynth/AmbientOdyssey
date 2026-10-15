#!/usr/bin/env python3
"""Read-only source verification for the last 3 R3 Grand Treasure contexts.

Use exact published NeoForge JARs:
- adventuredungeons-neoforge-1.21-1.3.1.jar (Modrinth BOyaLHWk)
- irons_spellbooks-1.21.1-3.16.3.jar (Modrinth slKLosTb)
No installation, bytecode execution, native override or automatic approval.
"""
import argparse
import json
import zipfile
from pathlib import Path
from verify_keep_kayra_native_loot import pool_summary,sha

ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=ROOT/'docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json'
NAMES={
  'adventuredungeons':'adventuredungeons-neoforge-1.21-1.3.1.jar',
  'irons_spellbooks':'irons_spellbooks-1.21.1-3.16.3.jar',
}

def inspect(sources):
    for ns,name in NAMES.items():
        if ns not in sources or sources[ns].name!=name:
            raise ValueError('Unpinned or missing source file for '+ns)
    candidates=json.loads(CANDIDATES.read_text(encoding='utf-8'))
    remaining=[r for r in candidates if r['structure'].split(':')[0] in NAMES]
    if len(remaining)!=3:raise ValueError('Expected exactly three remaining R3 Grand contexts')
    result=[]
    hashes={}
    for namespace,jar in sources.items():
        with zipfile.ZipFile(jar) as z:
            if z.testzip():raise ValueError('Native JAR CRC failure: '+jar.name)
            hashes[namespace]=sha(jar.read_bytes())
            for r in remaining:
                if r['structure'].split(':')[0]!=namespace:continue
                ns,table=r['table'].split(':',1)
                source=f'data/{ns}/loot_table/{table}.json'
                if source !=r['source_resource'] or source not in z.namelist():
                    raise ValueError('Missing or cross-table source '+source)
                raw=z.read(source);actual=sha(raw)
                if actual!=r['source_sha256']:
                    raise ValueError('Source hash mismatch '+source+' actual='+actual+' expected='+r['source_sha256'])
                obj=json.loads(raw);pools=obj.get('pools',[])
                index=r['pool_index']
                if not isinstance(index,int) or not 0<=index<len(pools):
                    raise ValueError('Invalid pool index '+r['table'])
                selected=pools[index]
                if selected.get('conditions') or any(e.get('type') not in {'minecraft:item','minecraft:empty'} for e in selected.get('entries',[])):
                    raise ValueError('Selected source pool has unsafe/more complex conditions: '+r['table'])
                result.append({
                    'structure':r['structure'],'table':r['table'],'tier':r['tier'],
                    'source_resource':source,'source_sha256':actual,
                    'selected_pool_index':index,
                    'all_pools':[pool_summary(p,i,index) for i,p in enumerate(pools)],
                    'static_sha_verified':True,
                    'effective_datapack_winner':'NOT_TESTED',
                    'lootr_additive_runtime':'NOT_TESTED',
                    'category_best_pool_review':'PENDING',
                })
    if len(result)!=3:raise ValueError('Expected three independently verified pools')
    return {'status':'THREE_NATIVE_SOURCE_HASHES_VERIFIED_NOT_RUNTIME_APPROVED',
            'verified_count':len(result),'jar_sha256':hashes,'tables':result,
            'limitations':['Original native resources match historical AO audit but active Paxi/datapack precedence remains untested.',
                           'Native pool selection and no-replacement Lootr behavior need an integrated runtime test.',
                           'No external mod files are committed or modified.']}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--adventure-jar',type=Path,required=True)
    p.add_argument('--irons-jar',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise ValueError('Do not overwrite recorded evidence')
    result=inspect({'adventuredungeons':a.adventure_jar,'irons_spellbooks':a.irons_jar})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print('AO_LAST_THREE_NATIVE_SUMMARY_BEGIN')
    for r in result['tables']:
        compact={'table':r['table'],'selected_pool_index':r['selected_pool_index'],
                 'native_source_sha256':r['source_sha256'],
                 'all_pools':[{'index':pool['index'],'rolls':pool['native_rolls'],
                         'entries':[{'item':x['id'],'weight':x['weight'],'type':x['type']} for x in pool['entries']]}
                         for pool in r['all_pools']]}
        print(json.dumps(compact,separators=(',',':')))
    print('AO_LAST_THREE_NATIVE_SUMMARY_END')
    print('Verified final three native source tables')
if __name__=='__main__':main()
