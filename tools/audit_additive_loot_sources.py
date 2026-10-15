"""Read exact installed resources and jigsaw/NBT reachability before enabling loot additions."""
import csv,gzip,hashlib,io,json,zipfile
from pathlib import Path
import nbtlib,json5
ROOT=Path(__file__).resolve().parents[1]
MODS=ROOT/'build/master-final-smoke/mods';OUT=ROOT/'docs/handoffs/loot-update-20261015'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 resources={};owners={};archives=[]
 for p in sorted(MODS.glob('*.jar')):
  z=zipfile.ZipFile(p);archives.append(z)
  for n in z.namelist():
   if n.startswith('data/') and ('/worldgen/structure/' in n or '/worldgen/template_pool/' in n or '/loot_table/' in n or ('/structure/' in n and n.endswith('.nbt'))):
    resources[n]=(z,n);owners[n]=p.name
 # Effective Paxi overlays use the reviewed source. Do not guess between colliding loot definitions.
 for p in sorted((ROOT/'release_030/overrides/config/paxi/datapacks').glob('*/data/**/*')):
  if p.is_file():
   n='data/'+p.as_posix().split('/data/',1)[1];resources[n]=(None,p);owners[n]=p.as_posix().split('/datapacks/',1)[1].split('/')[0]
 def data(n):
  z,p=resources[n];return z.read(p) if z else p.read_bytes()
 def resource(id,kind,ext='.json'):
  ns,path=id.split(':',1);return f'data/{ns}/{kind}/{path}{ext}'
 def refs(obj,key):
  result=[]
  if isinstance(obj,dict):
   for k,v in obj.items():
    if k==key and isinstance(v,str):result.append(v)
    result+=refs(v,key)
  elif isinstance(obj,list):
   for v in obj:result+=refs(v,key)
  return result
 dd=json.loads((ROOT/'release_030/overrides/config/dungeon_difficulty/difficulty_v2.json').read_text())
 rows=[];mappings=[]
 for world in dd['dimensions']:
  for zone in world['zones']:
   sid=zone['zone_matches']['structure'];tier=int(zone['difficulty']['name'][-1]);sr=resource(sid,'worldgen/structure')
   if sr not in resources:continue
   structure=json5.loads(data(sr).decode('utf-8-sig'));start=structure.get('start_pool');pools=set();templates=set();missing=[]
   def pool(pid):
    if pid in pools or pid=='minecraft:empty':return
    pools.add(pid);path=resource(pid,'worldgen/template_pool')
    if path not in resources:missing.append(path);return
    obj=json5.loads(data(path).decode('utf-8-sig'))
    for t in refs(obj,'location'):templates.add(t)
    fallback=obj.get('fallback');
    if fallback:pool(fallback)
   if start:pool(start)
   seen=set();tables={}
   while templates-seen:
    tid=next(iter(templates-seen));seen.add(tid);nr=resource(tid,'structure','.nbt')
    if nr not in resources:missing.append(nr);continue
    raw=data(nr)
    try:nbt=nbtlib.File.parse(io.BytesIO(gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw))
    except Exception as e:missing.append(nr+': '+str(e));continue
    for block in nbt.get('blocks',[]):
     tag=block.get('nbt',{})
     palette=nbt.get('palette',[]);state=int(block.get('state',0));container=str(palette[state].get('Name','')) if state<len(palette) else ''
     for k in ('LootTable','loot_table'):
      if k in tag and container in {'minecraft:chest','minecraft:trapped_chest','lootr:lootr_chest'}:tables.setdefault(str(tag[k]),[]).append(nr)
     if 'pool' in tag and ':' in str(tag['pool']):pool(str(tag['pool']))
   # Choose a single existing native pool with non-gating, valuable native entries.
   for table,nbts in sorted(tables.items()):
    tr=resource(table,'loot_table');r={'structure':sid,'tier':tier,'dimension':world['world_matches']['dimension'],'table':table,'template_evidence':sorted(set(nbts)),
      'structure_resource':sr,'structure_sha256':sha(data(sr)),'status':'BLOCKED','reason':'No suitable verified native pool selected'}
    if tr in resources:
     raw=data(tr);obj=json.loads(raw);r.update(provider=owners[tr],resource=tr,source_sha256=sha(raw),pool_count=len(obj.get('pools',[])))
     candidates=[]
     for i,poolobj in enumerate(obj.get('pools',[])):
      entries=poolobj.get('entries',[])
      # Strictly native non-recursive basic treasure only. No trophies, affix/gem factories or tags.
      values=refs(entries,'name')
      safe=all(e.get('type') in {'minecraft:item','minecraft:empty'} for e in entries)
      allowed={'minecraft:diamond','minecraft:emerald','minecraft:gold_ingot','minecraft:iron_ingot','minecraft:lapis_lazuli','minecraft:redstone','minecraft:enchanted_book','minecraft:golden_apple','minecraft:book','minecraft:experience_bottle','minecraft:amethyst_shard','minecraft:copper_ingot','minecraft:quartz'}
      prices={'minecraft:diamond':8,'minecraft:emerald':4,'minecraft:enchanted_book':8,'minecraft:golden_apple':8,'minecraft:gold_ingot':2,'minecraft:iron_ingot':1,'minecraft:experience_bottle':2}
      weights=sum(e.get('weight',1) for e in entries)
      score=sum(e.get('weight',1)*prices.get(e.get('name'),.1) for e in entries)/max(weights,1)
      valuable=any(v in {'minecraft:diamond','minecraft:emerald','minecraft:enchanted_book','minecraft:golden_apple'} for v in values)
      if safe and values and set(values)<=allowed and valuable and not poolobj.get('conditions'):candidates.append((score,i))
     if tier>=3 and candidates and not table.startswith(('minecraft:','minecells:')) and len(set(tables[table])):
      score,index=max(candidates);r.update(status='CANDIDATE_SOURCE_VERIFIED',reason='Reachable native chest; single valuable basic native pool; no trophy/recursive entries',selected_pool=index)
      mappings.append({'structure':sid,'tier':tier,'table':table,'source_resource':tr,'source_sha256':sha(raw),'pool_index':index,'chance':0.05,'selection_score':score})
    rows.append(r)
 # Each structure uses its best VERIFIED general treasure pool, shared by its eligible chest contexts.
 for sid in {m['structure'] for m in mappings}:
  candidates=[m for m in mappings if m['structure']==sid];best=max(candidates,key=lambda m:m['selection_score'])
  for m in candidates:
   for key in ['source_resource','source_sha256','pool_index','selection_score']:m[key]=best[key]
 (OUT/'chest-source-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
 (OUT/'grand-treasure-candidates.json').write_text(json.dumps(mappings,indent=2)+'\n')
 ss=next(MODS.glob('simplyswords*'));z=zipfile.ZipFile(ss);tag=json.loads(z.read('data/simplyswords/tags/item/uniques.json'))
 (OUT/'simplyswords-native-uniques.json').write_text(json.dumps({'jar':ss.name,'jar_sha256':sha(ss.read_bytes()),'tag':'simplyswords:uniques','values':tag['values'],'owner_override':'Only unique weapons, received in current chat'},indent=2)+'\n')
 print('Chest contexts',len(rows),'safe candidate contexts',len(mappings),'native unique IDs',len(tag['values']))
if __name__=='__main__':main()
