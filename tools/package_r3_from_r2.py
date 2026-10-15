#!/usr/bin/env python3
"""Create an auditable R3 private CurseForge import from the exact R2 ZIP.

All intended additions, replacements and removals must be explicitly enumerated.
Not evidence of in-game, Lootr, boss or multiplayer correctness.

python tools/package_r3_from_r2.py --base build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip --overlay build/r3-overlay --plan build/r3-plan.json --output build/Ambient-Odyssey-R3-PRIVATE.zip
"""
import argparse
import hashlib
import io
import json
import re
import tomllib
import zipfile
from pathlib import Path, PurePosixPath

R2_SHA = 'db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617'
R2_COUNT = 337
R2_JARS = 10

def sha(b):
    return hashlib.sha256(b).hexdigest()

def safe_name(name):
    p = PurePosixPath(name)
    return isinstance(name, str) and name != '' and '\\' not in name and not p.is_absolute() and all(s not in ('', '.', '..') for s in name.split('/')) and str(p) == name

def read_archive(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if z.testzip() or len(set(names)) != len(names) or not all(safe_name(n.rstrip('/')) for n in names):
            raise ValueError('Archive CRC, duplicate member, or unsafe archive path')
        return {n:z.read(n) for n in names if not n.endswith('/')}

def addon_ids(data):
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        if jar.testzip() is not None:
            raise ValueError('Corrupt nested JAR')
        paths = jar.namelist()
        ids=set()
        for name in ('META-INF/neoforge.mods.toml', 'META-INF/mods.toml'):
            if name in paths:
                obj=tomllib.loads(jar.read(name).decode('utf-8-sig'))
                ids |= {x['modId'] for x in obj.get('mods',[]) if x.get('modId')}
        if not ids and 'fabric.mod.json' in paths:
            modid=json.loads(jar.read('fabric.mod.json')).get('id')
            if modid:ids.add(modid)
        for name in paths:
            match=re.fullmatch(r'data/([^/]+)/loot_tables?/.*',name)
            if match and match.group(1) not in ids:
                raise ValueError('Custom addon JAR shadows a foreign/native loot table: '+name)
            if name == 'data/neoforge/loot_modifiers/global_loot_modifiers.json':
                j=json.loads(jar.read(name))
                if j.get('replace') is not False or len(j.get('entries',[]))!=len(set(j.get('entries',[]))):
                    raise ValueError('Custom addon loot modifier list must explicitly append and contain no duplicate entries')
        return ids

def guarded_resource(name,data):
    if not name.startswith('overrides/'):
        raise ValueError('Only overrides/ payload entries can be patched; manifest is managed internally')
    # Even a newly added file can shadow a JAR's native loot table.
    if re.search(r'/data/(?!ao_[a-z0-9_]+/)[^/]+/loot_tables?/', name):
        raise ValueError('Native loot-table override forbidden: ' + name)
    if name.endswith('/global_loot_modifiers.json'):
        obj=json.loads(data)
        entries=obj.get('entries',[])
        if obj.get('replace') is not False or not isinstance(entries,list) or len(entries)!=len(set(entries)):
            raise ValueError('Global loot modifiers must be add-only with unique entries')
    if '/data/apotheosis/loot_modifiers/' in name:
        raise ValueError('Changing native Apotheosis modifiers needs a separate explicit review')

def build(base, overlay, plan_file, output, *, expected_base_sha=R2_SHA, expected_pins=R2_COUNT, expected_jars=R2_JARS):
    base, overlay, plan_file, output=map(Path,(base,overlay,plan_file,output))
    rollback=output.with_name(output.stem+'-Rollback.zip')
    report=Path(str(output)+'.report.json')
    if any(p.exists() for p in (output,rollback,report)):
        raise ValueError('Output, rollback or report already exists: never overwrite existing build artifacts')
    if not base.is_file() or sha(base.read_bytes())!=expected_base_sha:
        raise ValueError('R2 base SHA256 mismatch; never bypass the pinned input')
    native=read_archive(base)
    manifest=json.loads(native['manifest.json'])
    pins=manifest['files']
    if len(pins)!=expected_pins or len({(f['projectID'],f['fileID']) for f in pins})!=expected_pins:
        raise ValueError('Incorrect or duplicate CurseForge roster')
    plan=json.loads(plan_file.read_text(encoding='utf-8'))
    if plan.get('format')!='ao-r2-to-r3-1' or not plan.get('reason') or not plan.get('changes'):
        raise ValueError('Plan must contain format, non-empty reason and explicit changes')
    if set(plan)-{'format','reason','changes'}:
        raise ValueError('Unknown plan keys')
    changed=dict(native)
    receipt=[]; names=set()
    for record in plan['changes']:
        if set(record)-{'action','path','old_sha256','new_sha256','reason'}:
            raise ValueError('Unknown change fields')
        name=record['path']; action=record['action']
        if not safe_name(name) or name in names or action not in ('add','replace','remove'):
            raise ValueError('Invalid or duplicate plan change')
        names.add(name)
        if not record.get('reason'):
            raise ValueError('Every change requires an explanatory reason')
        if not name.startswith('overrides/'):
            raise ValueError('Only override members can change')
        old=native.get(name)
        if action=='add' and (old is not None or 'old_sha256' in record):
            raise ValueError('Add cannot overwrite existing member or carry old SHA')
        if action in ('replace','remove') and (old is None or record.get('old_sha256')!=sha(old)):
            raise ValueError('Replacement/removal requires original member and correct old_sha256')
        if action=='remove':
            if 'new_sha256' in record:
                raise ValueError('Remove cannot carry new SHA')
            if re.search(r'/data/[^/]+/loot_tables?/',name):
                raise ValueError('Removing native loot table blocked')
            del changed[name]
            new=None
        else:
            if not re.fullmatch('[0-9a-f]{64}',record.get('new_sha256','')):
                raise ValueError('New SHA256 required')
            disk=(overlay/name).resolve()
            if not disk.is_relative_to(overlay.resolve()) or not disk.is_file():
                raise ValueError('Missing/unsafe overlay file: '+name)
            new=disk.read_bytes()
            if sha(new)!=record['new_sha256']:
                raise ValueError('Overlay file does not match declared new SHA256: '+name)
            if name.endswith('.jar'):
                addon_ids(new)
            else:
                guarded_resource(name,new)
            if action=='replace' and new==old:
                raise ValueError('No-op replacement rejected')
            changed[name]=new
        receipt.append({'action':action,'path':name,'reason':record['reason'],
                        'before_sha256':sha(old) if old is not None else None,
                        'after_sha256':sha(new) if new is not None else None})
    # Distinct filenames alone do not mean distinct mod IDs.
    modids={}; jars={}
    for name,data in changed.items():
        if name.startswith('overrides/mods/') and name.endswith('.jar'):
            jars[name]=sha(data)
            for modid in addon_ids(data):
                if modid in modids:
                    raise ValueError('Duplicate bundled addon mod ID '+modid+' in '+name+' and '+modids[modid])
                modids[modid]=name
    if len(jars)!=expected_jars:
        raise ValueError(f'Wrong bundled JAR count: {len(jars)} != {expected_jars}; additions require an explicitly reviewed roster change')
    original_unchanged={n for n in native if n not in names and n!='manifest.json'}
    if any(changed[n]!=native[n] for n in original_unchanged):
        raise ValueError('Original unrelated data drift')
    manifest['name']='Ambient Odyssey - R3 PRIVATE EXPERIMENTAL UNTESTED'
    manifest['version']='0.5.3-master-integration-r3-experimental'
    if manifest['files']!=pins:
        raise ValueError('CurseForge file pins were changed')
    changed['manifest.json']=(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode()
    receipt.insert(0,{'action':'replace','path':'manifest.json','reason':'Identify R3; CF pins unchanged',
                      'before_sha256':sha(native['manifest.json']), 'after_sha256':sha(changed['manifest.json'])})
    rollback_content={x['path']:native[x['path']] for x in receipt if x['path'] in native}
    rollback_content['ROLLBACK-RECEIPT.json']=(json.dumps({'base_r2_sha256':expected_base_sha,
        'added_paths_to_delete':[x['path'] for x in receipt if x['action']=='add'],
        'instructions':'Receipt only; never unpack onto an active save/profile. Reimport exact R2 separately.'},indent=2)+'\n').encode()
    def write_zip(path,files):
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,data in sorted(files.items()):
                if not safe_name(name):raise ValueError('Unsafe output name')
                info=zipfile.ZipInfo(name,(2026,10,15,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                z.writestr(info,data)
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        write_zip(output,changed)
        write_zip(rollback,rollback_content)
        if read_archive(output)!=changed or read_archive(rollback)!=rollback_content:
            raise ValueError('Round-trip ZIP validation failed')
        report_data={'status':'STATIC_PACKAGE_CREATED_NOT_RUNTIME_TESTED','r2_base_sha256':expected_base_sha,
                     'r3_sha256':sha(output.read_bytes()),'rollback_sha256':sha(rollback.read_bytes()),
                     'cf_references':len(pins),'custom_jars':jars,'changes':receipt,
                     'original_member_count':len(native),'new_member_count':len(changed),
                     'base_unchanged_member_count':len(original_unchanged),
                     'minecraft_runtime_tested':False,'lootr_multiplayer_tested':False,
                     'warning':'No claims of additive-only Java behavior; source and in-game loot tests are still mandatory.'}
        report.write_text(json.dumps(report_data,indent=2)+'\n')
        return report_data
    except Exception:
        for p in (output,rollback,report):
            if p.exists():p.unlink()
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for a in ('base','overlay','plan','output'):p.add_argument('--'+a,type=Path,required=True)
    a=p.parse_args()
    result=build(a.base,a.overlay,a.plan,a.output)
    print(json.dumps({k:result[k] for k in ('status','r3_sha256','rollback_sha256','cf_references')},indent=2))

if __name__=='__main__':main()
