"""Recheck pinned draft surfaces, active source payload and plan queues against a ZIP.

Different bytes are a review flag, never proof that an obsolete change should be merged.
This audit deliberately makes no native-runtime or completed-design claim.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MASTER = {62,61,60,59,57,56,54,53,52,51,50,49,48,47,46,45,44,42,41,40}


def normalized(data):
    return data.replace(b'\r\n', b'\n')


def audit(package):
    with zipfile.ZipFile(package) as z:
        payload = {n:z.read(n) for n in z.namelist() if not n.endswith('/')}
    metadata = json.loads((ROOT/'docs/handoffs/integration-20261015/pr-metadata.json').read_text(encoding='utf-8'))
    drafts = []
    for pr in metadata:
        reference = subprocess.check_output(['git','rev-parse','origin/'+pr['head']],cwd=ROOT,text=True).strip()
        diff = subprocess.check_output(['git','diff','--name-only',pr['base']+'...'+pr['sha']],cwd=ROOT,text=True)
        tree = subprocess.check_output(['git','ls-tree','-r',pr['sha']],cwd=ROOT,text=True)
        blobs = {line.split('\t',1)[1]:line.split('\t',1)[0].split()[2] for line in tree.splitlines()}
        surfaces = []
        for name in diff.splitlines():
            p = ROOT/name
            current = normalized(p.read_bytes()) if p.is_file() else None
            blob = hashlib.sha1(b'blob '+str(len(current)).encode()+b'\0'+current).hexdigest() if current is not None else None
            surfaces.append({'path':name,'draft_blob':blobs.get(name),'current_matches_draft':blob==blobs.get(name) if blob else False,
                             'source_present':p.is_file(), 'interpretation':'Exact-content test only; supersession/omission requires decision ledger'})
        drafts.append({'pr':pr['number'],'master_20':pr['number'] in MASTER,'branch':pr['head'],'audited_sha':pr['sha'],
                       'refreshed_remote_sha':reference,'head_drift':reference!=pr['sha'],'surfaces':surfaces})
    source_payload = []
    for folder, prefix in [('release_030/overrides','overrides'),('release_030/experimental_overlays/v050/overrides','overrides')]:
        base = ROOT/folder
        for p in sorted(base.rglob('*')):
            if not p.is_file(): continue
            member = prefix+'/'+p.relative_to(base).as_posix()
            actual = payload.get(member)
            source_payload.append({'source':p.relative_to(ROOT).as_posix(),'member':member,
                                   'status':'EXACT_NORMALIZED' if actual is not None and normalized(actual)==normalized(p.read_bytes()) else 'ABSENT' if actual is None else 'DIFFERENT_FROM_REPO_SOURCE'})
    resource_checks = []
    for addon in ('ao-starter-chest','ao-augmenting-sigils','ao-campaign'):
        jars = [n for n in payload if n.startswith('overrides/mods/'+addon+'-') and n.endswith('.jar')]
        if len(jars)!=1: raise ValueError('Expected one packaged addon: '+addon)
        with zipfile.ZipFile(io.BytesIO(payload[jars[0]])) as j:
            base = ROOT/'addons'/addon/'src/main/resources'
            for p in base.rglob('*'):
                if not p.is_file():continue
                rel=p.relative_to(base).as_posix()
                resource_checks.append({'addon':addon,'resource':rel,'exact':rel in j.namelist() and j.read(rel)==p.read_bytes()})
    campaign = next(n for n in payload if n.startswith('overrides/mods/ao-campaign-'))
    with zipfile.ZipFile(io.BytesIO(payload[campaign])) as j: policy=json.loads(j.read('ao_loot_policy.json'))
    plan=list(csv.DictReader((ROOT/'experiments/structure-difficulty-v4/DD_CONSOLIDATED_OWNER_TIER_PLAN_20261015.csv').open(encoding='utf-8-sig')))
    return {'package':package.name,'package_sha256':hashlib.sha256(package.read_bytes()).hexdigest(),
            'runtime_verified':False,'draft_count':len(drafts),'master_draft_count':sum(p['master_20'] for p in drafts),
            'draft_head_drift':[p['pr'] for p in drafts if p['head_drift']], 'drafts':drafts,
            'source_payload':source_payload,'addon_resource_checks':resource_checks,
            'addon_resource_mismatches':[x for x in resource_checks if not x['exact']],
            'policy_counts':{k:len(policy[k]) for k in ('bosses','regalia','unique_weapons','grand_treasure')},
            'boss_tier_counts':dict(collections.Counter(policy['bosses'].values())),
            'dd_plan_rows':len(plan),'dd_implementation_gates':dict(collections.Counter(r['implementation_gate'] for r in plan)),
            'dd_plan_note':'497 candidates are not 497 approved/runtime-ready zones; scope gates remain binding'}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('zip',type=Path);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();result=audit(a.zip)
    a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('drafts','source_payload','addon_resource_checks')},indent=2))
