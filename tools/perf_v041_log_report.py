#!/usr/bin/env python3
"""Ambient Odyssey 0.4.1 read-only client/dedicated log performance summary.

Does not expose player names, UUIDs, coordinates, server hostnames or local paths.
'Can't keep up' WARNINGS are isolated pauses, NOT a complete MSPT distribution.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from statistics import median

STALL = re.compile(r"Can't keep up!.*?\bRunning\s+(\d+)ms(?:\s+or\s+(\d+)\s+ticks behind)?",re.I)
STAMP = re.compile(r"^\[(\d{2}[A-Za-z]{3}\d{4}\s+\d{2}:\d{2}:\d{2}\.\d{3})\]")
TRACKER = {
    "chunks_generated": re.compile(r"Total Chunks Generated\s*:\s*(\d+)",re.I),
    "thread_time_ms": re.compile(r"Total Thread Time Spent\s*:\s*(\d+)\s*ms",re.I),
    "thread_ms_per_chunk": re.compile(r"Thread Time Per Chunk\s*:\s*([\d.,]+)\s*ms",re.I),
    "real_chunks_per_second": re.compile(r"Real Chunks Per Second\s*:\s*([\d.,]+)",re.I),
    "parallel_efficiency_percent": re.compile(r"Parallel Efficiency\s*:\s*([\d.,]+)\s*%",re.I),
    "wall_clock_ms": re.compile(r"Wall Clock Time\s*:\s*(\d+)\s*ms",re.I),
    "peak_threads": re.compile(r"Peak Threads In Use\s*:\s*(\d+)",re.I),
}
ISSUES = {
    "unsafe_entity_thread_warnings": "trying to add an entity from offthread",
    "invalid_air_messages": "Item must not be minecraft:air",
    "dungeon_crawl_spawner_warnings": "Failed to fetch a mob spawner",
    "mansion_missing_pool_warnings": "mansions:mansion/bottom_back_left",
    "missing_texture_reports": "Missing textures in model",
    "unknown_legacy_attribute": "Ignoring unknown attribute 'forge:",
}
def p95(values):
    """Nearest-rank p95; used only on stall WARNINGS, never presented as p95 MSPT."""
    if not values:return None
    values=sorted(values)
    import math
    return values[max(0,math.ceil(0.95*len(values))-1)]

def decimal(text):
    value=text.strip().replace(" ","")
    if "," in value and "." in value:
        value=value.replace(",","")
    elif "," in value:
        value=value.replace(",",".")
    return float(value)

def read_stamp(line):
    m=STAMP.search(line)
    if not m:return None
    try:return datetime.strptime(m.group(1),"%d%b%Y %H:%M:%S.%f")
    except ValueError:return None

def summarize(text):
    lines=text.splitlines()
    stalls=[]
    ftf={}
    counts=dict.fromkeys(ISSUES,0)
    errors=warnings=0
    first=last=None
    for line in lines:
        stamp=read_stamp(line)
        if stamp is not None:
            if first is None:first=stamp
            last=stamp
        if "/ERROR]" in line:errors+=1
        if "/WARN]" in line:warnings+=1
        m=STALL.search(line)
        if m:stalls.append(int(m.group(1)))
        for key,phrase in ISSUES.items():
            if phrase.lower() in line.lower():counts[key]+=1
        for key,rx in TRACKER.items():
            m=rx.search(line)
            if m:
                ftf[key]=int(m.group(1)) if key in {"chunks_generated","thread_time_ms","wall_clock_ms","peak_threads"} else decimal(m.group(1))
    result={
        "evidence_level":"HISTORICAL_LOG_ONLY_NOT_CAUSAL_OR_RUNTIME_PATCH_PASS",
        "line_count":len(lines),
        "session_elapsed_seconds":round((last-first).total_seconds(),2) if first and last and last>=first else None,
        "total_warn_lines":warnings,
        "total_error_lines":errors,
        "lag_warning_events":{
            "count":len(stalls),"worst_ms":max(stalls,default=None),
            "median_warning_ms":median(stalls) if stalls else None,
            "p95_warning_ms_nearest_rank":p95(stalls),
            "all_ms_sorted":sorted(stalls,reverse=True)
        },
        "ftf_shutdown_tracker":ftf,
        "issue_message_counts":counts,
        "limitations":[
            "Warn-event durations are NOT observed tick MSPT or server TPS; collect Spark MSPT separately.",
            "FreeTerraForged counters describe all generated chunks during its report window, not a controlled route.",
            "Counts are messages, not distinct root causes or guaranteed mod ownership.",
            "No hardware, seed, player name, coordinates, raw log snippets or absolute file paths are exported.",
            "Compare only matching builds, hardware, world states, seeds, routes, graphics settings and player count."
        ]
    }
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("logs",nargs="+",type=Path)
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    reports=[]
    for path in a.logs:
        res=summarize(path.read_text(encoding="utf-8",errors="replace"))
        res["log_label"]=path.name
        reports.append(res)
    obj={"reports":reports,"runtime_pass":False,"notes":"Historical client logs; not a new performance run."}
    data=json.dumps(obj,indent=2,ensure_ascii=False)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(data,encoding="utf-8")
        print("Wrote redacted aggregate report",a.out)
    else:print(data,end="")

if __name__=="__main__":
    main()
