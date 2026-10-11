#!/usr/bin/env python3
"""Classify original Apotheotic Additions boss/miniboss definitions for AO migration.

Read-only report, never auto-import old Forge boss JSON as modern Apotheosis data.
Supply a newline-separated list of actual mod IDs from the AO tested mod list.
"""
from __future__ import annotations
import argparse, collections, json, pathlib

def inspect(source, installed):
    buckets = {}
    for group in ("bosses", "minibosses"):
        entries = []
        for file in sorted((source/group).rglob("*.json")):
            try:
                j=json.loads(file.read_text(encoding="utf-8-sig"))
                entity=j.get("entity","")
                required={e.get("modid") for e in j.get("conditions",[])
                          if isinstance(e,dict) and e.get("type") in ("forge:mod_loaded","neoforge:mod_loaded")
                          and e.get("modid")}
                if isinstance(entity,str) and ":" in entity:
                    ns=entity.split(":",1)[0]
                    if ns!="minecraft": required.add(ns)
                missing=sorted(required-installed)
                entries.append({"source":str(file.relative_to(source)),
                                "entity":entity,
                                "requires":sorted(required),
                                "missing_required_mods":missing,
                                "rarity_span":[j.get("min_rarity"),j.get("max_rarity")],
                                "legacy_stats":sorted((j.get("stats") or {}).keys()),
                                "ready_for_direct_import":False})
            except (ValueError,OSError) as e:
                entries.append({"source":str(file.relative_to(source)), "error":str(e),"ready_for_direct_import":False})
        buckets[group]=entries
    summary={key:{"entries":len(v),"present_dependency_candidates":sum(not x.get("missing_required_mods") and "error" not in x for x in v),
                  "missing_mod_dependencies":sum(bool(x.get("missing_required_mods")) for x in v)}
             for key,v in buckets.items()}
    return {"summary":summary,"items":buckets,
            "warning":"Enhanced vanilla/mod mobs and spawn profiles; these files do not imply this many new entity classes. Modern 1.21.1 invader/elite schema conversion and actual entity registry verification required."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("source",type=pathlib.Path)
    p.add_argument("modids",type=pathlib.Path)
    p.add_argument("output",type=pathlib.Path)
    args=p.parse_args()
    installed={l.strip() for l in args.modids.read_text().splitlines()
               if l.strip() and not l.startswith("#")}
    report=inspect(args.source,installed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report["summary"],indent=2))
if __name__=="__main__":main()
