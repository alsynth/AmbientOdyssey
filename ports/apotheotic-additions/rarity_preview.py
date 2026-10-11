#!/usr/bin/env python3
"""Strict design-only migration of Apotheotic Additions 1.20.1 rarity definitions.
Never emit these JSON files to an active datapack: original custom materials, tier
weights, affix pools, recipes and chance semantics require real migration.
"""
from __future__ import annotations
import argparse, json, pathlib

TIERS=("haven","frontier","ascent","summit","pinnacle")
SUPPORTED={"stat","ability","socket"}

def preview(name, legacy):
    reasons=[]
    rules=[]
    for entry in legacy.get("rules",[]):
        kind=entry.get("type")
        chance=entry.get("chance",1)
        if kind not in SUPPORTED or chance!=1.0:
            reasons.append("manual rules migration required: "+json.dumps(entry,sort_keys=True))
            continue
        if kind=="socket":rules.append({"type":"apotheosis:socket","min":1,"max":1})
        else:rules.append({"type":"apotheosis:affix","affix_type":kind})
    material=legacy.get("material")
    if not isinstance(material,str) or material.startswith("apotheotic_additions:"):
        reasons.append("rarity crafting material not registered in 1.21.1: "+str(material))
    reasons += [
        "original single rarity weight/quality must be mapped to five world progression tiers",
        "custom rarity must have valid affix pools for every enabled loot category",
        "validate appearance, reforging, drops, translations, economy and loot modifiers",
    ]
    json_target={
        "type":"apotheosis:rarity",
        "color":legacy["color"],
        "material":material,
        "sort_index":min(2000,300+int(legacy.get("ordinal",0))*50),
        "weights":{tier:{"weight":0} for tier in TIERS},
        "rules":rules,
    }
    return {"id":"apotheotic_additions:"+name,"source_rules":len(legacy.get("rules",[])),
            "translated_rules":len(rules),"candidate_only_do_not_load":json_target,
            "blocking_reasons":reasons}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("source",type=pathlib.Path)
    p.add_argument("output",type=pathlib.Path)
    args=p.parse_args()
    entries={}
    for key in ("artifact","heirloom","esoteric"):
        f=args.source/"rarities"/(key+".json")
        if not f.is_file():p.error("Missing upstream rarity: "+str(f))
        entries[key]=preview(key,json.loads(f.read_text(encoding="utf-8")))
    assert all(len(v["blocking_reasons"])>0 for v in entries.values())
    report={"port_ready":False,"rarities":entries,
            "policy":"Esoteric is intended to remain unobtainable. Never inject these zero-weight placeholders into active AO datapacks."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("Rarity schema candidates:", ", ".join(entries), "— all blocked pending actual port.")
if __name__=="__main__":main()
