#!/usr/bin/env python3
"""Turn pinned native NBT read-only index into prioritized invalid-item owner list.

Input is historical Test6 JAR coverage (~65/72), not current 330-ref complete.
This NEVER patches structure NBT or substitutes unrelated items.
"""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'build/invalid-items-worldgen-089.json'
OUTPUT=ROOT/'build/v042-invalid-item-native-owner-triage.json'

def classify(report):
    items=[]
    for src in report["records"]:
        for template in src.get("hits",[]):
            for hit in template.get("items",[]):
                item=hit["item"]
                v=str(hit.get("count",""))
                m=re.search(r"(?<![0-9])-?[0-9]+",v)
                amount=int(m.group()) if m else None
                path=hit["path"]
                if item=='minecraft:air' and amount==0 and path.endswith("/buyB"):
                    priority="empty_optional_trade"
                elif item=='minecraft:air' and amount==0:
                    priority="zero_count_placeholder"
                elif amount is not None and amount>0:
                    priority="positive_count_invalid"
                else:
                    priority="unknown_context_requires_source"
                items.append({"jar":src["jar"],"template":template["template"],
                              "path":path,"item":item,"count":amount,"priority":priority})
    ranking={"positive_count_invalid":0,"unknown_context_requires_source":1,
             "zero_count_placeholder":2,"empty_optional_trade":3}
    items.sort(key=lambda a:(ranking[a["priority"]],a["jar"],a["template"],a["path"]))
    groups={}
    for hit in items:
        k=hit["priority"];groups[k]=groups.get(k,0)+1
    return {"scope":"historical test6 native source index ONLY, not full v0.4.2 330 refs",
            "coverage_complete":False,
            "source_jars_scanned":report["summary"]["scanned"],
            "source_jars_unreadable":report["summary"]["unreadable"],
            "unindexed_current_filenames":report["summary"].get("current_resolved_filenames_outside_historical_index"),
            "group_counts":groups,"prioritized_sources":items,
            "separate_runtime_code_offender":{
              "owner":"Dungeon Crawl 2.3.17 RandomMonster.VILLAGER_OFFERS",
              "source":"neoforge/1.21 RandomMonster.java static offer buyB air Count=0",
              "mitigation":"Experimental exact-zero optional buyB removal Mixin in addon v0.1.2",
              "runtime_verified":False,
              "included_in_native_structure_nbt_scan":False},
            "note":"Only source-prioritize; never blanket-replace minecraft:air, nor alter valid empty slots or chest contents."}

def main():
    source=json.loads(SOURCE.read_text())
    report=classify(source)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(report,indent=2)+"\n")
    print("INVALID_ITEM_COVERAGE",json.dumps({k:report[k] for k in
      ("coverage_complete","source_jars_scanned","source_jars_unreadable","unindexed_current_filenames","group_counts")}))
    for hit in report["prioritized_sources"][:80]:
        if hit["priority"] in ("positive_count_invalid","unknown_context_requires_source"):
            print("NATIVE_ITEM_OWNER",json.dumps(hit)[:700])
if __name__=="__main__":main()
