"""Copy a read-only installed profile into a new workspace-only test runtime."""
import argparse,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(instance,target,save,allow_added_mods=False):
    target=target.resolve();target.relative_to((ROOT/'build').resolve())
    if target.exists():raise RuntimeError('Refusing to overwrite an existing test runtime')
    expected=json.loads((ROOT/'docs/balance/v3-evidence/INSTALLED_JARS.json').read_text(encoding='utf-8'))
    pins={r['jar']:r['sha256'] for r in expected if r['jar']!='minecraft_1.21.1_client.jar'}
    current={p.name:digest(p) for p in (instance/'mods').glob('*.jar')}
    added=sorted(current.keys()-pins.keys());removed=sorted(pins.keys()-current.keys());changed=sorted(k for k in pins.keys()&current.keys() if pins[k]!=current[k])
    if removed or changed or (added and not allow_added_mods):raise RuntimeError('Current physical JAR roster differs from PR45; reconcile first')
    target.mkdir(parents=True)
    for name in ('mods','config','defaultconfigs','resourcepacks','shaderpacks','kubejs','scripts'):
        source=instance/name
        if source.is_dir():shutil.copytree(source,target/name)
    for name in ('options.txt',):
        if (instance/name).exists():shutil.copy2(instance/name,target/name)
    original=instance/'config/dungeon_difficulty/difficulty_v2.json'
    if original.read_bytes()!=(ROOT/'experiments/structure-difficulty-v3/rollback/config/dungeon_difficulty/difficulty_v2.json').read_bytes():raise RuntimeError('Live DD differs from recorded rollback')
    backup=target/'pr45-rollback/config/dungeon_difficulty/difficulty_v2.json';backup.parent.mkdir(parents=True)
    backup.write_bytes(original.read_bytes())
    candidate=ROOT/'experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json'
    (target/'config/dungeon_difficulty/difficulty_v2.json').write_bytes(candidate.read_bytes())
    source_save=instance/'saves'/save
    if not source_save.is_dir() or source_save.parent!=(instance/'saves'):raise RuntimeError('Invalid source save')
    before={p.relative_to(source_save).as_posix():(p.stat().st_size,p.stat().st_mtime_ns) for p in source_save.rglob('*') if p.is_file() and p.name!='session.lock'}
    shutil.copytree(source_save,target/'saves/pr45-original-save-copy',ignore=shutil.ignore_patterns('session.lock'))
    after={p.relative_to(source_save).as_posix():(p.stat().st_size,p.stat().st_mtime_ns) for p in source_save.rglob('*') if p.is_file() and p.name!='session.lock'}
    if before!=after:raise RuntimeError('Source save changed during copy; do not use this snapshot')
    copied={p.name:digest(p) for p in (target/'mods').glob('*.jar')}
    if copied!=current:raise RuntimeError('Copied JAR hashes differ')
    report={'status':'STATIC_PASS_SNAPSHOT_ONLY','source_instance':instance.name,'physical_jars':len(copied),'jar_hashes':copied,'added_since_pr45':added,'exact_pr45_roster':not added,'candidate_sha256':digest(candidate),'rollback_sha256':digest(backup),'copied_save':save,'copied_save_files':len(before),'save_unchanged_during_copy':True,'client_runtime':'NOT_RUN','dedicated_server':'NOT_RUN','multiplayer':'NOT_RUN','instrumentation_mod_included':False}
    (target/'PR45_SNAPSHOT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='jar_hashes'},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--instance',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--save',required=True);p.add_argument('--allow-added-mods',action='store_true',help='Retain added JARs as a separately labelled runtime context; original pins must still match');a=p.parse_args();prepare(a.instance,a.target,a.save,a.allow_added_mods)
