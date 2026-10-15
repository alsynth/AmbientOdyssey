"""Prepare a NEW isolated exact-roster runtime; never edit the supplied cache/profile."""
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path
from run_full_pack_log_probe import launch
ROOT=Path(__file__).resolve().parents[1]
def prepare(pack,cache,runtime):
    runtime=runtime.resolve();runtime.relative_to((ROOT/'build').resolve())
    if runtime.exists():raise ValueError('Runtime must be new')
    runtime.mkdir(parents=True)
    with zipfile.ZipFile(pack) as z:
        inputs=json.loads(z.read('overrides/AO_TEST_NOTES/FULL_IMPORT_INPUTS.json'))
        for name in z.namelist():
            if name.startswith('overrides/') and not name.endswith('/'):
                dest=(runtime/name.removeprefix('overrides/')).resolve();dest.relative_to(runtime)
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(name))
    for row in inputs['roster']:
        folders=['mods'] if row['kind']=='mod' else ['resourcepacks','shaderpacks']
        found=None
        for folder in folders:
            exact=cache/folder/row['name']
            candidates=[exact] if exact.exists() else list((cache/folder).glob('*.jar' if folder=='mods' else '*.zip'))
            for p in candidates:
                if hashlib.sha1(p.read_bytes()).hexdigest()==row['sha1']:found=p;break
            if found:break
        if not found:raise ValueError('Hash-pinned cache input absent: '+row['name'])
        dest=runtime/found.parent.name/found.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(found,dest)
    jars=sorted((runtime/'mods').glob('*.jar'));assert len(jars)==340,len(jars)
    snapshot={'pack_sha256':hashlib.sha256(pack.read_bytes()).hexdigest(),'production_jars':len(jars),
      'jars':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in jars},'live_profile_modified':False}
    (runtime/'INPUT_SNAPSHOT.json').write_text(json.dumps(snapshot,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pack',type=Path,required=True);p.add_argument('--cache',type=Path,required=True)
    p.add_argument('--install',type=Path,required=True);p.add_argument('--runtime',type=Path,required=True);a=p.parse_args()
    prepare(a.pack,a.cache,a.runtime)
    r=launch(a.install,a.runtime,ROOT/'tools/log-probe/build/libs/ao-fullpack-log-probe-1.0-test-only.jar',shutil.which('java'),'6G',420,campaign_checks=True)
    (a.runtime/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
