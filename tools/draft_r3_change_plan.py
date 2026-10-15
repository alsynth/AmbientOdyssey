#!/usr/bin/env python3
"""Draft an explicit R2 -> R3 overlay change plan; requires human review.

Creates empty reasons on PURPOSE so the packager refuses the draft until
every change has been explained and approved. Only local/R2 ZIP files needed.
"""
import argparse
import json
from pathlib import Path
import package_r3_from_r2 as pack

def draft(base, overlay, output, removed=()):
    base,overlay,output=map(Path,(base,overlay,output))
    if output.exists():
        raise ValueError('Draft plan already exists; never silently overwrite')
    if pack.sha(base.read_bytes())!=pack.R2_SHA:
        raise ValueError('Only the exact verified private R2 import is accepted')
    before=pack.read_archive(base)
    changes=[]
    newpaths=set()
    for candidate in sorted(overlay.rglob('*')):
        if not candidate.is_file():
            continue
        if not candidate.resolve().is_relative_to(overlay.resolve()):
            raise ValueError('Unsafe overlay symlink: '+str(candidate))
        name=candidate.relative_to(overlay).as_posix()
        if not pack.safe_name(name) or not name.startswith('overrides/'):
            raise ValueError('Overlay must mirror overrides/ layout: '+name)
        after=candidate.read_bytes()
        old=before.get(name)
        if old == after:
            continue
        change={'action':'replace' if old is not None else 'add','path':name,'new_sha256':pack.sha(after),'reason':''}
        if old is not None:
            change['old_sha256']=pack.sha(old)
        changes.append(change)
        newpaths.add(name)
    for name in sorted(set(removed)):
        if name in newpaths or not pack.safe_name(name) or not name.startswith('overrides/') or name not in before:
            raise ValueError('Removal not an eligible original R2 member: '+name)
        changes.append({'action':'remove','path':name,'old_sha256':pack.sha(before[name]),'reason':''})
    if not changes:
        raise ValueError('No content changes to package')
    plan={'format':'ao-r2-to-r3-1','reason':'','changes':changes}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    return len(changes)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('base','overlay','out'):parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--remove',action='append',default=[],help='Explicit R2 ZIP path to remove (e.g. old addon JAR)')
    args=parser.parse_args()
    number=draft(args.base,args.overlay,args.out,args.remove)
    print(f'Wrote {number} proposed changes to {args.out}. REVIEW each path and fill in overall and per-change reasons before building.')

if __name__=='__main__':main()
