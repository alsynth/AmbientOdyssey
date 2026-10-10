#!/usr/bin/env python3
"""Diagnose resource-source ownership of invalid NBT item stacks from actual installed JARs.

Standalone read-only audit. Uses exact CurseForge file refs + saved installed SHA256
inventory. Never mutates user packs or structure files.
"""
import concurrent.futures
import gzip
import io
import json
import hashlib
from pathlib import Path
import zipfile
import nbtlib

from audit_remaining_jigsaw_nbt_086 import indexed_jars, manifest_pairs, resolve, native_jar, fetch

ROOT=Path(__file__).resolve().parent
BAD={'minecraft:air','redeco:hammer','traveloptics:blood_echo','meadow:alpine_salt','create:crushed_iron_ore'}
CANDIDATES={'minecraft:air'.encode(),b'redeco:hammer',b'traveloptics:blood_echo',b'meadow:alpine_salt',b'create:crushed_iron_ore'}

def recursive_hits(node,path='',in_items=False,depth=0):
    if depth>24:return
    if isinstance(node,dict):
        if 'id' in node and str(node['id']) in BAD and (in_items or 'Count' in node or 'count' in node):
            yield {'path':path,'item':str(node['id']),'count':str(node.get('Count',node.get('count','')))}
        for k,v in node.items():
            key=str(k)
            yield from recursive_hits(v,path+'/'+key,in_items or key in ('Items','items','inventory','Inventory','HandItems','ArmorItems'),depth+1)
    elif isinstance(node,(list,tuple)):
        for i,v in enumerate(node):
            yield from recursive_hits(v,path+'/'+str(i),in_items,depth+1)

def scan(entry,fid,name):
    native=native_jar(entry)
    # helper native_jar here expects entry dict from 087, not 086; use direct download in place.
    raise NotImplementedError

def inspect(item):
    entry,fid,name=item
    key=str(fid)
    from urllib.parse import quote
    url=f"https://mediafilez.forgecdn.net/files/{int(key[:-3])}/{int(key[-3:]):03d}/"+quote(name)
    try:
        jarbytes=fetch(url,limit=85_000_000,timeout=90)
        assert hashlib.sha256(jarbytes).hexdigest()==entry['sha256'], 'source JAR SHA mismatch'
        examined=0
        found=[]
        with zipfile.ZipFile(io.BytesIO(jarbytes)) as archive:
            for path in archive.namelist():
                if not path.endswith('.nbt') or not path.startswith('data/') or '/structure/' not in path:continue
                raw=archive.read(path)
                try: buf=gzip.decompress(raw)
                except Exception: continue
                examined+=1
                if not any(s in buf for s in CANDIDATES):continue
                try:
                    nbt=nbtlib.File.parse(io.BytesIO(buf))
                    hits=list(recursive_hits(nbt))
                    if hits:found.append({'template':path,'items':hits[:75],'total_matches':len(hits)})
                except Exception as e:
                    found.append({'template':path,'read_error':str(e)[:200]})
        return {'jar':name,'count':examined,'hits':found}
    except Exception as e:
        return {'jar':name,'error':type(e).__name__+":"+str(e)[:220]}
def main():
    index=indexed_jars()
    candidates={name:item for name,item in index.items() if item.get('counts',{}).get('worldgen/template_pool',0)>0 or item.get('counts',{}).get('worldgen/structure',0)>0}
    pairs=manifest_pairs()
    mapped={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as exe:
        for pid,fid,name,error in exe.map(resolve,pairs.items()):
            if name:mapped[name]=(pid,fid)
    eligible=[(entry,mapped[name][1],name) for name,entry in candidates.items() if name in mapped]
    print('SOURCE_CANDIDATES',len(candidates),'MAPPED',len(eligible),flush=True)
    found=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as exe:
        for record in exe.map(inspect,eligible):
            found.append(record)
            if record.get('hits'):
                print('INVALID_ITEM_SOURCE',json.dumps(record,ensure_ascii=False)[:23000],flush=True)
            elif record.get('error'):
                print('SOURCE_UNREADABLE',record['jar'],record['error'],flush=True)
    dest=ROOT/'build/invalid-items-worldgen-089.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps({'scanned':len(found),'records':found,'unmapped':sorted(set(candidates)-set(mapped))},indent=2))
    print('SUMMARY',json.dumps({'scanned':len(found),'with_hits':sum(bool(r.get('hits')) for r in found),'total_item_matches':sum(sum(p.get('total_matches',0) for p in r.get('hits',[])) for r in found),'unreadable':sum(bool(r.get('error')) for r in found),'report':str(dest)}),flush=True)
if __name__=='__main__':main()
