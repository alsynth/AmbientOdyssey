#!/usr/bin/env python3
"""Create a RESOURCE-ONLY Grand Treasure R3 campaign addon from verified R2.

No Java compile or official CurseForge JAR downloads required when ONLY the
Grand Treasure policy entries change and the compiled R2 Java stays identical.
This is a static experimental binary transformation, NOT a runtime acceptance.

Requires the exact R2 ZIP, a staged experimental policy and its source-reviewed
staging receipt. Output only a new copy of the campaign JAR, suitable for
overrides/mods/ in a separately assembled R3 private test ZIP.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R2_SHA='db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617'
MEMBER='ao_loot_policy.json'
EXPECTED_GRAND_CONTEXTS=14

def sha(data):return hashlib.sha256(data).hexdigest()

def archive_members(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if z.testzip() is not None:raise ValueError('Corrupted archive member')
        entries=[i for i in z.infolist() if not i.is_dir()]
        if len(set(i.filename for i in entries))!=len(entries):
            raise ValueError('Duplicate JAR member paths')
        return [(i,z.read(i)) for i in entries]

def patch_jar(jar_bytes,policy_bytes,stage_receipt):
    if stage_receipt.get('status')!='STAGED_EXPERIMENTAL_SOURCE_REVIEW_ONLY_NOT_COMPILED_NOT_RUNTIME_TESTED':
        raise ValueError('Staging receipt does not prove reviewed experimental policy')
    if stage_receipt.get('staged_policy_sha256')!=sha(policy_bytes):
        raise ValueError('Staged policy hash differs from source-reviewed receipt')
    prior=archive_members(jar_bytes)
    members={i.filename:b for i,b in prior}
    if MEMBER not in members:
        raise ValueError('Compiled R2 campaign JAR has no loot policy resource')
    for name in ('dev/ambientodyssey/campaign/GrandTreasure.class',
                 'dev/ambientodyssey/campaign/BossRewards.class',
                 'META-INF/neoforge.mods.toml'):
        if name not in members:raise ValueError('R2 campaign JAR is missing required compiled class/metadata: '+name)
    # Resource replacements invalidate Java JAR signatures: forbid this path
    # for any signed binary; a proper rebuild must handle that case.
    if any(i.filename.upper().startswith('META-INF/') and i.filename.upper().endswith(('.SF','.RSA','.DSA','.EC')) for i,_ in prior):
        raise ValueError('Signed JAR: cannot patch resources without invalidating signatures')
    metadata=members['META-INF/neoforge.mods.toml'].decode('utf-8')
    if 'modId="ao_campaign"' not in metadata or 'version="0.3.0-experimental"' not in metadata:
        raise ValueError('Unexpected compiled R2 addon identity/version')
    original=json.loads(members[MEMBER])
    new=json.loads(policy_bytes)
    original_rest={k:v for k,v in original.items() if k!='grand_treasure'}
    new_rest={k:v for k,v in new.items() if k!='grand_treasure'}
    if original_rest!=new_rest:
        raise ValueError('Policy patch changes non-Grand boss/Regalia/gem/unique properties')
    old_rows=original.get('grand_treasure',[]);new_rows=new.get('grand_treasure',[])
    if len(old_rows)!=EXPECTED_GRAND_CONTEXTS or len(new_rows)!=EXPECTED_GRAND_CONTEXTS:
        raise ValueError('Campaign context count differs from pinned R2/owner mapping')
    old_keys={(r['structure'],r['table']) for r in old_rows}
    new_keys={(r['structure'],r['table']) for r in new_rows}
    if len(old_keys)!=EXPECTED_GRAND_CONTEXTS or new_keys!=old_keys:
        raise ValueError('Grand Treasure trigger structure/table context set changed')
    for r in new_rows:
        namespace,tablepath=r['table'].split(':',1)
        if r['source_resource']!=f'data/{namespace}/loot_table/{tablepath}.json':
            raise ValueError('Unverified cross-chest Grand source: '+r['table'])
        if r['tier']<3 or r['chance']!=0.05:
            raise ValueError('Grand bonus tier/chance changed')
        if set(r)!={'structure','table','tier','source_resource','source_sha256','pool_index','chance'}:
            raise ValueError('Unexpected Grand policy key')
    if old_rows==new_rows:
        raise ValueError('No actual Grand Treasure resource change')
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as jar:
        for info,body in prior:
            jar.writestr(info,policy_bytes if info.filename==MEMBER else body)
    result=out.getvalue()
    modified=dict((i.filename,b) for i,b in archive_members(result))
    if set(members)!=set(modified):
        raise ValueError('Output JAR changed member set')
    if any(modified[k]!=v for k,v in members.items() if k!=MEMBER):
        raise ValueError('Output JAR modified unrelated resources or bytecode')
    if modified[MEMBER]!=policy_bytes:
        raise ValueError('Output JAR policy changed unexpectedly')
    return result,{
        'status':'R3_CAMPAIGN_RESOURCE_ONLY_PATCH_NOT_RUNTIME_TESTED',
        'r2_campaign_jar_sha256':sha(jar_bytes),
        'r3_campaign_jar_sha256':sha(result),
        'r2_policy_sha256':sha(members[MEMBER]),
        'r3_policy_sha256':sha(policy_bytes),
        'original_member_count':len(prior),
        'unmodified_jar_member_count':len(prior)-1,
        'original_grand_contexts':len(old_rows),
        'r3_grand_contexts':len(new_rows),
        'changed_grand_source_contexts':sum(any(
            next(v for v in old_rows if (v['structure'],v['table'])==(r['structure'],r['table']))[field]!=r[field]
            for field in ('source_resource','source_sha256','pool_index')) for r in new_rows),
        'all_compiled_classes_byte_identical':True,
        'minecraft_runtime_tested':False,
        'lootr_multiplayer_tested':False,
        'native_original_loot_replacement_tested':False,
        'warning':'Resource change only. Verify native reward source hashes and real Lootr behavior in dedicated multiplayer.'
    }

def extract_r2_campaign(r2_path):
    if sha(r2_path.read_bytes())!=R2_SHA:
        raise ValueError('Full R2 input ZIP does not match exact private-release SHA256')
    with zipfile.ZipFile(r2_path) as z:
        if z.testzip() is not None:raise ValueError('R2 outer ZIP CRC failure')
        jars=[n for n in z.namelist() if n.startswith('overrides/mods/ao-campaign-') and n.endswith('.jar')]
        if len(jars)!=1:raise ValueError('Expected exactly one campaign JAR in R2')
        if not jars[0].endswith('ao-campaign-0.3.0-experimental.jar'):
            raise ValueError('Unexpected R2 campaign addon filename')
        return jars[0],z.read(jars[0])

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--r2',type=Path,required=True)
    p.add_argument('--policy',type=Path,required=True)
    p.add_argument('--staging-receipt',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True,
                   help='Receipt JSON outside overrides/, e.g. build/r3-reports/campaign-policy-patch.json')
    p.add_argument('--out',type=Path,required=True,
                   help='New file in build/r3-overlay/overrides/mods/ao-campaign-0.3.0-experimental.jar')
    args=p.parse_args()
    report=args.report
    if args.out.exists() or report.exists():
        raise ValueError('Refusing to overwrite JAR or receipt')
    if not args.out.resolve().is_relative_to((ROOT/'build').resolve()) or not report.resolve().is_relative_to((ROOT/'build').resolve()):
        raise ValueError('Both output and report must be inside project build/')
    if 'overrides' in report.resolve().parts or report.resolve()==args.out.resolve():
        raise ValueError('Receipt cannot be inside the import overrides tree or overwrite the JAR')
    name,binary=extract_r2_campaign(args.r2)
    if args.out.name!=Path(name).name:
        raise ValueError('Preserve R2 addon filename so R3 replaces it, not duplicates it')
    policy_bytes=args.policy.read_bytes()
    staged=json.loads(args.staging_receipt.read_text(encoding='utf-8'))
    patched,receipt=patch_jar(binary,policy_bytes,staged)
    receipt['r2_zip_sha256']=R2_SHA
    receipt['addon_path_in_import']=name
    args.out.parent.mkdir(parents=True,exist_ok=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(patched)
    report.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('R3 campaign addon policy-only patch prepared; bytecode unchanged; runtime not tested: '+str(args.out))

if __name__=='__main__':main()
