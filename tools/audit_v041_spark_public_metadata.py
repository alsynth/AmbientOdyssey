#!/usr/bin/env python3
"""Public Spark link metadata probe. Keeps raw response PRIVATE and ephemeral.

Never publish original profiles, player names, server details, username/UUID,
world seed, IP or raw JVM arguments to a public GitHub artifact.
"""
import json
import re
import ssl
from pathlib import Path
from urllib.request import Request, urlopen

CODES=("m2Eglp00fO","ohcUJyadut","Gj6d4N6Igg","lhhJO6dLBL")
OUT=Path("build/spark_public_metadata_sanitized.json")
ALLOW=re.compile(r"(?:^|_)(?:mspt|tps|tick|cpu|memory|heap|gc|usage|average|mean|median|minimum|maximum|min|max|p50|p95|p99|duration|start|end|percentile|percent|sample|period|uptime)(?:$|_)",re.I)

def metrics(obj,path="",depth=0):
    if depth>=11:return {}
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            if not isinstance(k,str):continue
            if k not in {"platformStatistics","mspt","tps","cpu","memory","gc","heap","statistics","timings"} and depth<2:
                # The API has extra private machine and identity fields; omit
                # everything except known aggregates and safe timing categories.
                continue
            safe=re.sub(r"[^A-Za-z0-9_-]","",k)[:60]
            if not safe:continue
            if isinstance(v,(int,float)) and ALLOW.search(safe):
                out[safe]=v
            elif isinstance(v,dict):
                nested=metrics(v,path+"/"+safe,depth+1)
                if nested:out[safe]=nested
            elif isinstance(v,list) and safe in {"tps","mspt","statistics"}:
                samples=[x for x in v if isinstance(x,(int,float))]
                if samples:out[safe]=samples[:40]
    return out

def main():
    reports=[]
    for code in CODES:
        entry={"spark_code":code,"retrieved":False,"profile_parsed":False,"performance_metrics":{}}
        try:
            url="https://spark.lucko.me/"+code+"?raw=1"
            req=Request(url,headers={"User-Agent":"AmbientOdyssey-PublicProfiler-Preflight/1.0","Accept":"application/json"})
            with urlopen(req,timeout=22) as response:
                raw=response.read(5_000_001)
            if len(raw)>5_000_000:raise ValueError("metadata exceeds size cap")
            obj=json.loads(raw)
            entry["retrieved"]=True
            # Data is often wrapped: metadata.platformStatistics is canonical.
            containers=[obj]
            if isinstance(obj,dict):
                for key in ("metadata","platformStatistics","statistics"):
                    if isinstance(obj.get(key),dict):containers.append(obj[key])
                if isinstance(obj.get("metadata"),dict):
                    for key in ("platformStatistics","statistics"):
                        if isinstance(obj["metadata"].get(key),dict):
                            containers.append(obj["metadata"][key])
            candidates=[]
            for c in containers:
                if isinstance(c,dict):
                    allowed={"platformStatistics","mspt","tps","cpu","memory","gc","heap","statistics","timings"}
                    filtered={k:v for k,v in c.items() if k in allowed}
                    d=metrics(filtered)
                    if d:candidates.append(d)
            entry["performance_metrics"]=candidates[:4]
            entry["profile_parsed"]=bool(candidates)
        except Exception as exc:
            entry["retrieval_error_type"]=type(exc).__name__
        reports.append(entry)
        print("SPARK",code,"retrieved",entry["retrieved"],"metrics",bool(entry["performance_metrics"]),
              "error",entry.get("retrieval_error_type","none"))
    result={"evidence":"PUBLIC_PROFILE_METADATA_ONLY_NO_HOTPATH_ATTRIBUTION","raw_profile_published":False,
            "profile_links":["https://spark.lucko.me/"+code for code in CODES],
            "profiles":reports,
            "limitations":["No flamegraph or sampled method tree processed; do not attribute lag to mods.",
                           "Only sanitized numerical metadata is published; original profile stays remote."]}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("SANITIZED_REPORT",json.dumps(result["profiles"],ensure_ascii=True)[:2800])

if __name__=="__main__":main()
