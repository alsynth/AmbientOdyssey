#!/usr/bin/env python3
"""Inspect Spark full-profile JSON structural schema, WITHOUT printing metadata/PII.

Only top-level static keys and container type names leave the runner.
Never save or upload original raw profiles to public GitHub artifacts.
"""
import json
from urllib.request import Request,urlopen
from pathlib import Path

CODES=("ohcUJyadut","lhhJO6dLBL")
SAFE={"metadata","platformStatistics","threads","profile","sampler","data","session","mode",
      "samplerData","samplerMetadata","timeline","sources","platform","nodes","root",
      "callTree","statistics","methodLookup","classLookup","samples","aggregator"}
def shape(obj,depth=0):
    if depth>=4:return str(type(obj).__name__)
    if isinstance(obj,dict):
        return {k: shape(v,depth+1) for k,v in obj.items() if k in SAFE}
    if isinstance(obj,list):
        return {"kind":"array","count":len(obj),"first":shape(obj[0],depth+1) if obj else None}
    return type(obj).__name__
def main():
    for code in CODES:
        try:
            url=f"https://spark.lucko.me/{code}?raw=1&full=true"
            with urlopen(Request(url,headers={"User-Agent":"AmbientOdyssey-Spark-Schema-Check"}),timeout=60) as f:
                raw=f.read(25_000_001)
            if len(raw)>25_000_000:raise ValueError("full profile exceeds size cap")
            obj=json.loads(raw)
            print("SPARK_FULL_SCHEMA",code,len(raw),
                  "root_keys",sorted(k for k in obj if k in SAFE) if isinstance(obj,dict) else type(obj).__name__,
                  "shape",json.dumps(shape(obj),separators=(",",":"))[:1300])
        except Exception as e:print("SPARK_SCHEMA_ERROR",code,type(e).__name__)
if __name__=="__main__":main()
