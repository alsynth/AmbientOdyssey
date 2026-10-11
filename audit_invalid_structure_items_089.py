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

# This is a historical Test6 SHA inventory, not an index of all v0.4.1 JARs.
# A successful scan therefore never proves that the complete 329-ref pack is clean.
INDEX_SCOPE = 'historical Test6 pinned native JAR index; newer 0.4.x additions may be absent'

from audit_remaining_jigsaw_nbt_086 import indexed_jars, manifest_pairs, resolve, fetch

ROOT=Path(__file__).resolve().parent
BAD={'minecraft:air','redeco:hammer','traveloptics:blood_echo','meadow:alpine_salt','create:crushed_iron_ore','biomesoplenty:rose_quartz_shard'}
CANDIDATES={item.encode('utf-8') for item in BAD}

def is_structure_nbt_path(path):
    """Accept only vanilla/current and legacy native structure NBT paths."""
    parts=path.split('/')
    return (len(parts)>=4 and parts[0]=='data' and parts[-1].endswith('.nbt')
            and parts[2] in ('structure','structures'))

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
                if not is_structure_nbt_path(path):continue
                raw=archive.read(path)
                try: buf=gzip.decompress(raw)
                except (OSError,EOFError): buf=raw
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
    # Any JAR absent from this historical index remains unaudited. Report it,
    # rather than silently treating the scan as full-pack verification.
    not_in_index=sorted(set(mapped)-set(index))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as exe:
        for record in exe.map(inspect,eligible):
            found.append(record)
            if record.get('hits'):
                print('INVALID_ITEM_SOURCE',json.dumps(record,ensure_ascii=False)[:23000],flush=True)
            elif record.get('error'):
                print('SOURCE_UNREADABLE',record['jar'],record['error'],flush=True)
    dest=ROOT/'build/invalid-items-worldgen-089.json'
    dest.parent.mkdir(exist_ok=True)
    summary={'scanned':len(found),'with_hits':sum(bool(r.get('hits')) for r in found),
             'total_item_matches':sum(sum(p.get('total_matches',0) for p in r.get('hits',[])) for r in found),
             'unreadable':sum(bool(r.get('error')) for r in found),
             'current_manifest_refs':len(pairs),'resolved_filenames':len(mapped),
             'historical_index_jars':len(index),
             'current_resolved_filenames_outside_historical_index':len(not_in_index),
             'coverage_complete':False,'report':str(dest)}
    report={'index_scope':INDEX_SCOPE,'targets':sorted(BAD),
            'summary':summary,'records':found,
            'current_files_not_in_historical_index':not_in_index,
            'historical_candidates_without_current_filename_mapping':sorted(set(candidates)-set(mapped)),
            'note':'Read-only provenance scan. Missing/unreadable JARs and source-defined loot or runtime-generated stacks are NOT cleared by a zero-hit result.'}
    dest.write_text(json.dumps(report,indent=2)+'\n')
    print('SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__':main()
