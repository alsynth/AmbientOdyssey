#!/usr/bin/env python3
"""Read-only 1.20.1 Apotheotic Additions -> Apotheosis 8.9 schema migration probe.

Does not automatically enable any legacy affixes in an AO data pack.
It deliberately fails closed when custom rarity registry entries do not exist.
Usage: python port_schema_probe.py /path/to/upstream/data/apotheotic_additions output.json
"""
from __future__ import annotations
import argparse, collections, json, pathlib

OLD_CATEGORY = {
    "helmet":"apotheosis:helmet",
    "chestplate":"apotheosis:chestplate",
    "leggings":"apotheosis:leggings",
    "boots":"apotheosis:boots",
    "shield":"apotheosis:shield",
    "sword":"apotheosis:melee_weapon",
    "heavy_weapon":"apotheosis:melee_weapon",
    "trident":"apotheosis:trident",
    "pickaxe":"apotheosis:breaker",
    "shovel":"apotheosis:breaker",
    "bow":"apotheosis:bow",
    "crossbow":"apotheosis:bow",
}
VANILLA_OPERATIONS = {
    "ADDITION": "add_value",
    "MULTIPLY_BASE": "add_multiplied_base",
    "MULTIPLY_TOTAL": "add_multiplied_total",
}
REQUIRED_MODERN_KEYS = {"type", "attribute", "categories", "definition", "operation", "values"}

def inspect(legacy: dict) -> dict:
    if legacy.get("type") != "apotheosis:attribute":
        return {"status":"unsupported_type", "type":legacy.get("type")}
    reasons=[]
    types=legacy.get("types", [])
    categories=[OLD_CATEGORY[t] for t in types if t in OLD_CATEGORY]
    unknown=sorted(set(types)-set(OLD_CATEGORY))
    if unknown:reasons.append("unmapped legacy categories: "+",".join(unknown))
    old_operation=legacy.get("operation")
    if old_operation not in VANILLA_OPERATIONS:
        reasons.append("unknown legacy operation: "+str(old_operation))
    values=legacy.get("values",{})
    custom=sorted(x for x in values if x.startswith("apotheotic_additions:"))
    if custom:
        reasons.append("legacy custom rarity IDs require migration to verified native port namespace: "+",".join(custom))
    for rarity,v in values.items():
        if isinstance(v,dict) and ("steps" in v or "step" in v):
            # Placebo 9.9.2's strict codec still accepts min/steps/step. Retain it.
            if not isinstance(v.get("steps"), int) or v.get("steps", 0) <= 0:
                reasons.append("invalid legacy stepped roll: "+rarity)
    reasons.append("new Apotheosis affix definition weights/exclusive_set require balancing review")
    preview={
        "type":"apotheosis:attribute",
        "attribute":legacy.get("attribute"),
        "operation":VANILLA_OPERATIONS.get(old_operation),
        "categories":categories,
        "definition":{"affix_type":"stat","exclusive_set":[],"weights":{"quality":0.0,"weight":0}},
        "values":values,
    }
    return {"status":"blocked_pending_registry_and_schema_port","reasons":reasons,
            "preview_only_not_loadable":preview,"modern_required_fields_present":set(preview)>=REQUIRED_MODERN_KEYS}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("source",type=pathlib.Path)
    p.add_argument("output",type=pathlib.Path)
    args=p.parse_args()
    if not args.source.is_dir():p.error("Source must be upstream apotheotic_additions data directory")
    stats=collections.Counter()
    examples=[]
    for path in sorted((args.source/"affixes").rglob("*.json")):
        try:
            old=json.loads(path.read_text(encoding="utf-8"))
            result=inspect(old)
            stats[result["status"]]+=1
            if len(examples)<12:
                examples.append({"relative_path":str(path.relative_to(args.source)),**result})
        except (OSError,ValueError) as e:
            stats["unreadable"]+=1
            if len(examples)<12:examples.append({"relative_path":str(path),"error":str(e)})
    payload={"port_complete":False,"ready_to_install":False,"type_counts":dict(stats),"examples":examples,
            "note":"Preview transformation only. Never ship this output as an active datapack."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2,default=str)+"\n",encoding="utf-8")
    print(json.dumps({"type_counts":dict(stats),"port_complete":False,"report":str(args.output)}))
if __name__=="__main__":main()
