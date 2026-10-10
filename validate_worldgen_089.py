#!/usr/bin/env python3
"""Source-backed AO Test8.9 worldgen repair checks, no Minecraft runtime claim."""
from pathlib import Path
import gzip,io,json,zipfile,urllib.parse,urllib.request,hashlib
import nbtlib

ROOT=Path(__file__).resolve().parent
FIX=ROOT/'release_030/overrides/config/paxi/datapacks/ao_worldgen_final_fixes/data'
SOURCES=(
    (8688394,'repurposed_structures-7.5.22+1.21.1-neoforge.jar','64e64109acf7673b969aca9b3cca0bb555777cd7038aa16aa32a1548d753f257'),
    (8657120,'t_and_t-fabric-neoforge-1.13.11.jar','270fc0d1c99e54bc15f43d64bdaac60a90cb896efc357af624988e677136440f'),
)
passed=0
def require(label,ok):
    global passed
    if not ok: raise AssertionError(label)
    passed+=1
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def jar(fid,name,sha):
    cache=ROOT/'build/cache/native89'/name
    if cache.exists() and hashlib.sha256(cache.read_bytes()).hexdigest()==sha:
        return zipfile.ZipFile(io.BytesIO(cache.read_bytes()))
    url=f"https://mediafilez.forgecdn.net/files/{fid//1000}/{fid%1000:03d}/"+urllib.parse.quote(name)
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AmbientOdyssey-Worldgen-SourceValidator/1.0'}),timeout=80) as response:
        raw=response.read(25000000)
    require(name+' exact binary SHA',hashlib.sha256(raw).hexdigest()==sha)
    cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_bytes(raw)
    return zipfile.ZipFile(io.BytesIO(raw))
def jigsaws(data):
    d=nbtlib.File.parse(io.BytesIO(gzip.decompress(data)))
    found=[]
    for b in d['blocks']:
        if str(d['palette'][int(b['state'])]['Name'])=='minecraft:jigsaw':
            tag=b.get('nbt',{})
            found.append((str(tag.get('name','')),str(tag.get('pool','')),str(tag.get('target',''))))
    return d,found
def run():
    require('Test8.9 version and pinned mod roster',load(ROOT/'release_030/release-lock.json')['version']=='0.3.8-worldgen-prefreeze-test1.9')
    with jar(*SOURCES[0]) as z:
        src=json.loads(z.read('data/repurposed_structures/worldgen/structure/city_overworld.json'))
        dst=load(FIX/'repurposed_structures/worldgen/structure/city_overworld.json')
        require('city source 5-level baseline',src['size']==5)
        require('city override only changes level count 5 to 7',dst==dict(src,size=7))
        require('required tower top in boundary bypass unchanged','repurposed_structures:cities/overworld/fat_tower_top' in dst['pools_that_ignore_boundaries'])
        start=json.loads(z.read('data/repurposed_structures/worldgen/template_pool/cities/overworld/start_pool.json'))
        require('original city base room remains start',start['elements'][0]['element']['location']=='repurposed_structures:cities/overworld/base_room')
        top=json.loads(z.read('data/repurposed_structures/worldgen/template_pool/cities/overworld/fat_tower_top.json'))
        require('required city tower top native asset exists and is mapped',top['elements'][0]['element']['location']=='repurposed_structures:cities/overworld/fat_tower_top' and 'data/repurposed_structures/structure/cities/overworld/fat_tower_top.nbt' in z.namelist())
        _,tops=jigsaws(z.read('data/repurposed_structures/structure/cities/overworld/fat_tower_top.nbt'))
        require('native required top has expected minecraft tower-top mating connector',any(n=='minecraft:tower_top' for n,p,t in tops))
    with jar(*SOURCES[1]) as z:
        name='kaisyn:village/beach_lighthouse/villager_lighthouse_master'
        root=load(FIX/'kaisyn/worldgen/template_pool/village/beach_lighthouse/villager_lighthouse_master.json')
        child=load(FIX/'kaisyn/worldgen/template_pool/village/beach_lighthouse/villagers/lighthouse_master.json')
        require('missing root pool recreated under exact referenced ID',root['name']==name and root['fallback']=='minecraft:empty' and len(root['elements'])==1)
        native='kaisyn:village/beach_lighthouse/villagers/lighthouse_master'
        require('root uses exactly author-provided lighthouse master template',root['elements'][0]['element']['location']==native and root['elements'][0]['element']['element_type']=='minecraft:legacy_single_pool_element')
        require('nested self-ref safely terminates without inventing another master',child['name']==native and child['elements']==[{'weight':1,'element':{'element_type':'minecraft:empty_pool_element'}}])
        template='data/kaisyn/structure/village/beach_lighthouse/villagers/lighthouse_master.nbt'
        require('source contains missing lighthouse NPC template',template in z.namelist())
        d,jigs=jigsaws(z.read(template))
        require('lighthouse NPC connector matches main beach lighthouse bottom',any(n=='minecraft:bottom' and p==native and t=='minecraft:bottom' for n,p,t in jigs))
        center='data/kaisyn/structure/village/beach_lighthouse/town_centers/beach_meeting_point_1.nbt'
        _,starts=jigsaws(z.read(center))
        require('source main building requests exact missing root pool with bottom connector',any(n=='minecraft:bottom' and p==name and t=='minecraft:bottom' for n,p,t in starts))
        require('lighthouse pool does not replace any original native pool',not any(x.endswith('/villager_lighthouse_master.json') for x in z.namelist()))
        print('Native lighthouse master structure size:',list(map(int,d.get('size',[]))),'entity count:',len(d.get('entities',[])))
    print(f'PASS {passed}: independent 1.21.1 pinned-JAR Test8.9 worldgen source assertions')
    print('NOT TESTED: random generation, gameplay, server, detailed geometry.')
if __name__=='__main__': run()
