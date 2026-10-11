#!/usr/bin/env python3
"""Private in-run Spark protobuf flame tree summarizer for four USER-shared URLs.

Downloads raw profiles only into runner memory. Emits numeric/top class method
aggregates, never original profile, UUIDs, player names, world data or JVM args.
"""
import importlib.util
import json
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

CODES=("m2Eglp00fO","ohcUJyadut","Gj6d4N6Igg","lhhJO6dLBL")
OUT=Path("build/v041_spark_hotspots_sanitized.json")
MAX_PROF=35_000_000

def download(url,timeout=45):
    request=urllib.request.Request(url,headers={"User-Agent":"AmbientOdyssey-SanitizedSparkProfiler/1.0"})
    with urllib.request.urlopen(request,timeout=timeout) as f:
        value=f.read(MAX_PROF+1)
        if len(value)>MAX_PROF:raise ValueError("Spark profile exceeds size cap")
        return value

def source_schema(tmp):
    from grpc_tools import protoc
    schema_url="https://raw.githubusercontent.com/lucko/spark-viewer/master/proto/spark.proto"
    path=Path(tmp)/"spark.proto"
    path.write_bytes(download(schema_url))
    assert b"message SamplerData " in path.read_bytes()
    result=protoc.main(["protoc","-I"+str(tmp),"--python_out="+str(tmp),str(path)])
    if result!=0:raise RuntimeError("Could not compile public spark sampler schema")
    sys.path.insert(0,str(tmp))
    import spark_pb2
    return spark_pb2

def candidate_sources(node,root_time):
    exclusive=[]
    paths=[]
    def visit(n,depth):
        subtotal=sum(c.time for c in n.children)
        self_ms=max(0.0,n.time-subtotal)
        cls=n.className if hasattr(n,"className") else ""
        method=n.methodName if hasattr(n,"methodName") else ""
        if cls and self_ms>0:
            # Keep only Java identifiers; do not accidentally echo arbitrary
            # comments/player strings from profiler metadata.
            signature=re.sub(r"[^a-zA-Z0-9_.$/-]","",cls)[:145]
            meth=re.sub(r"[^a-zA-Z0-9_$<>]","",method)[:65]
            exclusive.append((self_ms,signature,meth))
        if depth<7:
            for c in n.children:visit(c,depth+1)
    for root in node.children:visit(root,0)
    sums={}
    for count,cls,method in exclusive:
        key=cls+"#"+method
        sums[key]=sums.get(key,0)+count
    return [{"class_method":name,"exclusive_weight":round(weight,2),
             "estimated_thread_percent":round(100*weight/max(root_time,1e-8),2)}
            for name,weight in sorted(sums.items(),key=lambda x:x[1],reverse=True)[:40]]

def scan(spark_pb2,code):
    payload=None
    attempts=[]
    for host in ("https://spark-usercontent.lucko.me/","https://bytebin.lucko.me/"):
        try:
            payload=download(host+code)
            if payload:break
        except Exception as exc: attempts.append(type(exc).__name__)
    if not payload:raise RuntimeError("Cannot access raw Spark payload: "+",".join(attempts))
    report=spark_pb2.SamplerData()
    report.ParseFromString(payload)
    if not report.threads:raise RuntimeError("Spark profile parsed with no threads")
    out={
        "code":code,"sampler_threads":len(report.threads),
        "sample_interval_ms":report.metadata.interval,
        "recorded_ticks":report.metadata.numberOfTicks,
        "aggregator_type":report.metadata.dataAggregator.type,
        "threads":[],"status":"RAW_PROFILER_PROCESSED_EPHEMERALLY",
    }
    best=sorted(report.threads,key=lambda x:x.time,reverse=True)
    for t in best:
        name=t.name
        if "Server thread" not in name and "Render thread" not in name and "Worker" not in name and "ForkJoinPool" not in name:
            continue
        if len(out["threads"])>=14:break
        typ=("server" if "Server thread" in name else
            "render" if "Render thread" in name else
            "worldgen_worker" if "Worker" in name else "fork_join_worker")
        top=candidate_sources(t,t.time)
        out["threads"].append({
            "thread_class":typ,
            "root_weight":round(t.time,2),
            "root_children":len(t.children),
            "top_methods":top[:24],
        })
    return out

def main():
    with tempfile.TemporaryDirectory() as tmp:
        schema=source_schema(tmp)
        profiles=[]
        for code in CODES:
            try:
                entry=scan(schema,code)
                profiles.append(entry)
                print("SPARK_RAW_PARSED",code,"threads",entry["sampler_threads"],
                      "included",len(entry["threads"]),"ticks",entry["recorded_ticks"])
                for t in entry["threads"]:
                    if t["thread_class"]=="server":
                        print("SPARK_SERVER_METHODS",code,json.dumps(t["top_methods"][:14])[:2600])
            except Exception as exc:
                print("SPARK_RAW_PROBE_FAILURE",code,type(exc).__name__)
                profiles.append({"code":code,"status":"FAILED","error_type":type(exc).__name__})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({
        "source":"user-supplied public Spark links",
        "privacy":"raw profile bytes kept ephemeral and never uploaded",
        "model":"exclusive sampled weights from spark profiler protobuf; approximations, not measured milliseconds",
        "profiles":profiles
    },indent=2)+"\n")
    print("SUMMARY_REPORT_SAVED",str(OUT))

if __name__=="__main__":main()
