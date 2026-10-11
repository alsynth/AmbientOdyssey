#!/usr/bin/env python3
"""Inspect exact pinned native JAR recipes to replace disabled AO 0.4.1 recipes.

Read only, SHA256 on Mine Cells, no new recipes or overrides are written.
Output native metadata (no full source NBT redistributed). The source raw
JSONs are printed with limits in PRIVATE CI logs for engineering attribution.
"""
import hashlib, io, json, re, urllib.request
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/'release_030/release-lock.json').read_text())
MODS={
 'minecells':'content-040-minecells-minecells',
 'brewinandchewin':'content-040f-brewin-and-chewin',
 'dimdungeons':'content-040g-dimensional-dungeons'
}
def source(jar):
    fid=int(jar['id'])
    urls=[
      f"https://mediafilez.forgecdn.net/files/{fid//1000}/{fid%1000:03d}/"+quote(jar['fileName']),
      f"https://edge.forgecdn.net/files/{fid//1000}/{fid%1000:03d}/"+quote(jar['fileName'])
    ]
    errors=[]
    for url in urls:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'AmbientOdyssey-RecipeSourceAudit/0.4.2'})
            with urllib.request.urlopen(req,timeout=75) as conn:data=conn.read(30_000_001)
            assert len(data)<=30_000_000
            with ZipFile(io.BytesIO(data)) as z:assert z.testzip() is None
            return data
        except Exception as e:errors.append(type(e).__name__)
    raise RuntimeError(f'Pinned JAR unavailable {jar["fileName"]}: {errors}')
def main():
    root=ROOT/'release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes/data'
    targets=sorted(root.glob('*/recipe/**/*.json'))
    assert len(targets)==19,len(targets)
    report={'count':len(targets),'sources':{},'recipes':[],'classification':{},'notes':[
      'Output only metadata. Original JAR JSON is consulted but not redistributed.',
      'A disabled recipe might be malformed due missing recipe serializer or absent dependency.',
      'No recipe should be enabled until native registry and required compat mod are confirmed.'
    ]}
    for mod,slug in MODS.items():
        jar=LOCK['additions'][slug];raw=source(jar)
        if 'sha256' in jar:assert hashlib.sha256(raw).hexdigest()==jar['sha256']
        report['sources'][mod]={'projectID':jar['projectId'],'fileID':jar['id'],
                                'sha256':hashlib.sha256(raw).hexdigest(),'filename':jar['fileName']}
        with ZipFile(io.BytesIO(raw)) as z:
            names=set(z.namelist())
            for p in targets:
                if p.parts[-1]=='pack.mcmeta' or p.parts[p.parts.index('data')+1]!=mod:continue
                rel=p.relative_to(root).as_posix()
                # Namespace/recipe/compat/foo is same inside native data directory.
                paths=[f'data/{rel}',f'data/{rel}'.replace('/recipe/','/recipes/')]
                candidates=[x for x in paths if x in names]
                entry={'id':mod+':'+rel.split('/recipe/')[1].removesuffix('.json'),
                       'native_paths':candidates}
                if candidates:
                    blob=z.read(candidates[0])
                    obj=json.loads(blob)
                    entry.update({'native_sha256':hashlib.sha256(blob).hexdigest(),
                        'native_type':obj.get('type'), 'native_keys':sorted(obj.keys()),
                        'body':obj})
                    print('RECIPE_NATIVE',entry['id'],json.dumps(obj,ensure_ascii=False)[:3600])
                else:
                    entry['native_absent']=True
                    print('RECIPE_ABSENT',entry['id'],'PATHS',paths)
                report['recipes'].append(entry)
    report['native_found']=sum(not x.get('native_absent',False) for x in report['recipes'])
    assert len(report['recipes'])==19,len(report['recipes'])
    out=ROOT/'build/v042-native-recipe-source-audit.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('RECIPE_AUDIT',report['native_found'],'of 19 native JSON found')
if __name__=='__main__':main()
