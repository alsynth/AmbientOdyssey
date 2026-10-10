#!/usr/bin/env python3
"""Native-source static proof for Test8.10 (no Minecraft runtime semantics implied)."""
import hashlib,json,io,zipfile,urllib.request,urllib.parse,gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DAT=ROOT/'release_030/overrides/config/paxi/datapacks/ao_worldgen_final_fixes/data'
def require(cond,message):
    assert cond,message
    print('PASS',message)
def load(p):return json.loads(p.read_text())
def getjar(fid,name,sha):
    path=ROOT/'build/cache/native810'/name
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==sha:
        return zipfile.ZipFile(io.BytesIO(path.read_bytes()))
    req=urllib.request.Request(f'https://mediafilez.forgecdn.net/files/{fid//1000}/{fid%1000:03d}/'+urllib.parse.quote(name),headers={'User-Agent':'AmbientOdyssey-NativeSourceValidator/1.0'})
    with urllib.request.urlopen(req,timeout=90) as f:blob=f.read(26000000)
    require(hashlib.sha256(blob).hexdigest()==sha,'Graveyard 1.21.1 binary SHA256 matches source inventory')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(blob)
    return zipfile.ZipFile(io.BytesIO(blob))
def main():
    j=load(ROOT/'release_030/release-lock.json')
    require(j['version']=='0.3.8-worldgen-prefreeze-test1.10','Test8.10 exact release lock')
    with getjar(8213402,'graveyard-2.6.2 NeoForge 1.21.1.jar','69dd4501da1fcc596d8ab7e09f32259ad1beee7e031fd5ab2d9c6cff4a8c8b2b') as zip:
        src=json.loads(zip.read('data/graveyard/worldgen/template_pool/large_walled_graveyard/crypt_pool.json'))
        root=load(DAT/'graveyard/worldgen/template_pool/large_walled_graveyard/small_crypt_pool.json')
        require(src==root,'Graveyard missing pool is exact unmodified native source JSON from misnamed crypt_pool.json')
        require(src['name']=='graveyard:large_walled_graveyard/small_crypt_pool','Native Graveyard crypt pool declares exact missing ID')
        target=src['elements'][0]['element']['location']
        require(target=='graveyard:large_graveyard/small_crypt_pool/small_crypt','Missing crypt pool retains exact source geometry')
        require('data/graveyard/structure/large_graveyard/small_crypt_pool/small_crypt.nbt' in zip.namelist(),'Actual small crypt NBT is present')
    srcpath=ROOT/'release_030/evidence/jar-resource-index-test6.json.gz'
    idx=json.loads(gzip.decompress(srcpath.read_bytes()))
    vill=load(DAT/'kaisyn/worldgen/template_pool/village/meadow_swiss/villagers.json')
    src=idx['resources']['worldgen/template_pool']['kaisyn:village/jungle_tribal/villagers'][0]['data']
    require(vill['name']=='kaisyn:village/meadow_swiss/villagers','Meadow Swiss exact absent pool ID')
    require(vill['fallback']==src['fallback']=='minecraft:empty','Meadow villagers fallback unchanged')
    require(len(vill['elements'])==len(src['elements'])==3,'Meadow villager choices mirror native T&T villager mixture')
    require([v['weight'] for v in vill['elements']]==[v['weight'] for v in src['elements']]==[1,1,10],'Meadow villager relative spawn weights mirror native T&T')
    require(all(v['element']['element_type']=='minecraft:legacy_single_pool_element' and v['element']['location'].startswith('minecraft:village/plains/villagers/') for v in vill['elements']),'Meadow villager templates use known vanilla plains assets')
    require(all(v['element']['processors']=='minecraft:empty' for v in vill['elements']),'Meadow villager processors remain normal')
    print('TEST8.10: static native references consistent; not a game launch/visual placement proof.')
if __name__=='__main__':main()
