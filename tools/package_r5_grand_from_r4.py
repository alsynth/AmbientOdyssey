#!/usr/bin/env python3
"""Package a NEW experimental R5 import from the exact original R4 release ZIP.

Only changes:
  1. original R4 campaign JAR replaced with the hash-verified, five-pool
     human-reviewed R5 experimental resource-only campaign variant
  2. importer manifest version/name updated to PRIVATE EXPERIMENTAL R5
All other ZIP members, 337 official CurseForge references, and nine custom
JARs must remain unmodified. Does NOT claim Minecraft/Lootr runtime acceptance.

Use only after patch_r5_grand_from_r4.py has generated the new campaign JAR
and its provenance receipt. Never repack an already generated R5 ZIP.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

R4_SHA="31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d"
CAMPAIGN_SHA="802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7"
CAMPAIGN_PATH="overrides/mods/ao-campaign-0.3.2-experimental.jar"

def sha(b):return hashlib.sha256(b).hexdigest()

def read_members(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or z.testzip():
            raise ValueError('ZIP CRC failure or duplicate member name')
        return {n:z.read(n) for n in names if not n.endswith('/')}

def write_zip(path,files):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,data in sorted(files.items()):
            # Never permit traversal, malformed names or unexpected directory roots.
            if (name.startswith('/') or '\\' in name or '..' in name.split('/') or
                name.startswith('./') or not name or name.endswith('/')):
                raise ValueError('Unsafe member name: '+name)
            info=zipfile.ZipInfo(name,(2026,10,15,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,data)

def build(r4_path,addon_path,patch_receipt_path,out,*,expected_base=R4_SHA,
          expected_campaign=CAMPAIGN_SHA,expected_pins=337,expected_jar_count=10):
    r4_path,addon_path,patch_receipt_path,out=map(Path,(r4_path,addon_path,patch_receipt_path,out))
    rollback=out.with_name(out.stem+'-Rollback.zip')
    report=Path(str(out)+'.report.json')
    if out.exists() or rollback.exists() or report.exists():
        raise ValueError('Never overwrite an existing import, rollback or receipt')
    if sha(r4_path.read_bytes())!=expected_base:
        raise ValueError('R4 base ZIP SHA256 does not match the pinned published release')
    original=read_members(r4_path)
    if CAMPAIGN_PATH not in original or sha(original[CAMPAIGN_PATH])!=expected_campaign:
        raise ValueError('Original R4 compiled campaign JAR differs from the pinned release')
    manifest=json.loads(original['manifest.json'])
    pins=manifest['files']
    if len(pins)!=expected_pins or len({(f['projectID'],f['fileID']) for f in pins})!=expected_pins:
        raise ValueError('Original official CurseForge reference pins missing or duplicated')
    jars={n for n in original if n.startswith('overrides/mods/') and n.endswith('.jar')}
    if len(jars)!=expected_jar_count:
        raise ValueError('Unexpected R4 custom mod JAR count')
    receipt=json.loads(patch_receipt_path.read_text(encoding='utf-8'))
    changed=receipt.get('changed_grand_pool_indices',[])
    if (receipt.get('status')!='R5_GRAND_RESOURCE_ONLY_EXPERIMENTAL_JAR_NOT_RUNTIME_TESTED'
        or receipt.get('basis_release_sha256')!=expected_base
        or receipt.get('basis_campaign_jar_sha256')!=expected_campaign
        or receipt.get('only_modified_jar_member')!='ao_loot_policy.json'
        or receipt.get('minecraft_runtime_tested') is not False
        or receipt.get('lootr_multiplayer_tested') is not False
        or len(changed)!=5 or len({r[0] for r in changed})!=5):
        raise ValueError('Unverified R4-source Grand campaign patch receipt')
    patched=addon_path.read_bytes()
    if sha(patched)!=receipt.get('patched_campaign_jar_sha256'):
        raise ValueError('Patched campaign JAR hash differs from reviewed receipt')
    if patched==original[CAMPAIGN_PATH]:
        raise ValueError('No-op addon replacement')
    new=dict(original)
    new[CAMPAIGN_PATH]=patched
    updated=dict(manifest)
    updated['name']='Ambient Odyssey - R5 Grand Treasure PRIVATE EXPERIMENTAL TEST'
    updated['version']='0.5.5-master-integration-r5-grand-experimental'
    if updated['files']!=pins:raise ValueError('Official mod reference roster changed')
    new['manifest.json']=(json.dumps(updated,indent=2,ensure_ascii=False)+'\n').encode()
    changed_members=[n for n in new if original.get(n)!=new[n]]
    if set(changed_members)!={'manifest.json',CAMPAIGN_PATH}:
        raise ValueError('Unexpected R4 import changes beyond campaign addon and manifest')
    if {n for n in new if n.startswith('overrides/mods/') and n.endswith('.jar')}!=jars:
        raise ValueError('Addon filename roster drift')
    if any(original[n]!=new[n] for n in new if n not in changed_members):
        raise ValueError('Unrelated original R4 data modified')
    rollback_entries={
        'manifest.json':original['manifest.json'],
        CAMPAIGN_PATH:original[CAMPAIGN_PATH],
        'ROLLBACK-RECEIPT.json':(json.dumps({
            'warning':'This is an incremental file receipt, NOT a standalone CurseForge import or world rollback.',
            'base_r4_sha256':expected_base,
            'restore_original_profile':'Reimport exact immutable R4 into a NEW profile; never overwrite existing world or mix generated chunks.',
            'changed_members':sorted(changed_members)
        },indent=2)+'\n').encode()
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    try:
        write_zip(out,new)
        write_zip(rollback,rollback_entries)
        if read_members(out)!=new or read_members(rollback)!=rollback_entries:
            raise ValueError('Round-trip import or rollback ZIP validation failed')
        summary={
            'status':'R5_PRIVATE_EXPERIMENTAL_STATIC_IMPORT_NOT_GAMEPLAY_TESTED',
            'source_r4_sha256':expected_base,
            'source_r4_campaign_jar_sha256':expected_campaign,
            'r5_import_sha256':sha(out.read_bytes()),
            'rollback_sha256':sha(rollback.read_bytes()),
            'r5_campaign_jar_sha256':sha(patched),
            'cf_references':len(pins),
            'custom_addon_jar_count':len(jars),
            'changed_members':sorted(changed_members),
            'grand_five_pool_indices_only':changed,
            'minecraft_runtime_tested':False,
            'lootr_two_player_tested':False,
            'native_loot_preservation_runtime_tested':False,
            'warning':'Never use as a production server/client release without in-game and dedicated multiplayer validation.'
        }
        report.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
        return summary
    except Exception:
        for p in (out,rollback,report):
            if p.exists():p.unlink()
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ('r4','addon','patch-receipt','output'):
        p.add_argument('--'+x,type=Path,required=True)
    args=p.parse_args()
    result=build(args.r4,args.addon,args.patch_receipt,args.output)
    print('R5 separate PRIVATE EXPERIMENTAL import packaged, static-only; sha256 '+result['r5_import_sha256'])

if __name__=='__main__':main()
