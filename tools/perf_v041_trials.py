#!/usr/bin/env python3
"""Aggregate user-entered Ambient Odyssey v0.4.1 parallel performance trials.

CSV measurements are observations only; never infer speedups from unmatched
versions, worldgen states, profiles, or fewer than three comparable trials.
No raw seeds, server identifiers, paths or user notes are included in JSON.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import csv
import json
from pathlib import Path
from statistics import median

METRICS=("avg_fps","fps_1pct_low","avg_mspt","p95_mspt","tps","chunks_generated")
CONTROL_FIELDS=("build_sha256","seed","route_id","dimension","terrain_state",
                "players","shaders","render_distance","simulation_distance","ram_mib")
KNOWN_SCENARIOS={"idle","new_chunks","warm_chunks","combat","shader_scene","server_2p","server_5p"}
def number(value):
    text=str(value or "").strip()
    if not text:return None
    value=float(text.replace(",","."))
    if value < 0:raise ValueError("Negative metric")
    return value

def report(rows):
    grouped=defaultdict(list)
    invalid=[]
    skipped=0
    for i,entry in enumerate(rows,2):
        if entry.get("status","").upper()!="MEASURED":
            skipped+=1
            continue
        scenario=entry.get("scenario","").strip()
        variant=entry.get("variant","").strip()
        if not scenario in KNOWN_SCENARIOS or not variant:
            invalid.append("row %s: invalid scenario or absent variant" % i)
            continue
        if not entry.get("build_sha256") or not entry.get("route_id") or not entry.get("seed"):
            invalid.append("row %s: exact ZIP SHA, route and seed required for measurable trial" % i)
            continue
        readings={}
        try:
            for name in METRICS:
                readings[name]=number(entry.get(name))
        except ValueError:
            invalid.append("row %s: invalid numerical metric" % i)
            continue
        if all(value is None for value in readings.values()):
            invalid.append("row %s: no actual measured values" % i)
            continue
        grouped[(scenario,variant)].append((entry,readings))
    summaries=[]
    for (scenario,variant),records in sorted(grouped.items()):
        controls={k:{entry.get(k,"").strip() for entry,_ in records} for k in CONTROL_FIELDS}
        changed={key:len(v) for key,v in controls.items() if len(v)>1}
        stats={name:median(v) if (v:=[read[name] for _,read in records if read[name] is not None]) else None
               for name in METRICS}
        incomplete={name:sum(read[name] is not None for _,read in records) for name in METRICS}
        notes=[]
        if len(records)<3:notes.append("PROVISIONAL: fewer than 3 completed trials")
        if changed:notes.append("NONCOMPARABLE: controls changed within group: "+", ".join(sorted(changed)))
        if scenario=="new_chunks":
            notes.append("Do not compare cold generation to a previously explored route.")
        if scenario=="warm_chunks":
            notes.append("Ensure this is exactly the prior cold-route playback.")
        summaries.append({
            "scenario":scenario,"variant":variant,"measured_trials":len(records),
            "medians":stats,"sample_counts":incomplete,
            "controlled":len(changed)==0,
            "eligible_for_comparison":len(records)>=3 and not changed,
            "quality_notes":notes,
        })
    return {
        "evidence_level":"USER_RECORDED_MEASUREMENTS_NOT_CAUSAL_PROOF",
        "measured_rows":sum(x["measured_trials"] for x in summaries),
        "unmeasured_template_rows":skipped,
        "invalid_rows":invalid,
        "groups":summaries,
        "cross_variant_conclusions":"NOT COMPUTED: require hardware, save state, seed/route and profile matching first",
        "limitations":[
            "Spark sampling can change performance; compare with and without active profiler separately.",
            "Server stall warnings do not determine p95 MSPT.",
            "Median FPS alone hides stutter: record 1% low FPS and frame times independently.",
            "Performance improvements require identical modpack content except isolated measured changes.",
        ],
    }
def main():
    p=argparse.ArgumentParser()
    p.add_argument("csv",type=Path)
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    with a.csv.open(encoding="utf-8-sig",newline="") as f:
        data=report(list(csv.DictReader(f)))
    text=json.dumps(data,indent=2)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(text,encoding="utf-8")
        print("Wrote non-identifying measurements summary:",a.out)
    else:print(text,end="")
    if data["invalid_rows"]:raise SystemExit(2)

if __name__=="__main__":
    main()
