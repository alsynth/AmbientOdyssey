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

def weight(node):
    return float(node.time) if node.time else float(sum(node.times))

def candidate_sources(thread):
    """Unflatten spark's childrenRefs into its actual call tree.

    spark-viewer Preprocessing.unflatten uses ThreadNode.children as a flat
    backing array and childrenRefs to traverse. The protobuf does not have
    actual nested children until those refs are resolved. Weight is the sum
    of repeated times (source viewer Preprocessing.calculateTotalTimes).
    """
    flat=thread.children
    root=weight(thread)
    if root<=0:
        root=sum(weight(flat[i]) for i in thread.childrenRefs)
    counts={}
    stack=list(thread.childrenRefs)
    visited=set()
    while stack:
        idx=stack.pop()
        if idx in visited:continue
        visited.add(idx)
        if not (0<=idx<len(flat)):continue
        node=flat[idx]
        kids=[k for k in node.childrenRefs if 0<=k<len(flat)]
        exclusive=max(0.0,weight(node)-sum(weight(flat[k]) for k in kids))
        cls=node.className
        if cls and exclusive>0:
            cls=re.sub(r"[^a-zA-Z0-9_.$/-]","",cls)[:145]
            method=re.sub(r"[^a-zA-Z0-9_$<>]","",node.methodName)[:65]
            key=cls+"#"+method
            counts[key]=counts.get(key,0.0)+exclusive
        stack.extend(kids)
    top=sorted(counts.items(),key=lambda q:q[1],reverse=True)[:40]
    return [
        {"class_method":name,"exclusive_weight":round(v,2),
         "estimated_thread_percent":round(100*v/max(root,1e-8),2)}
        for name,v in top
    ],root,len(visited)

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
        top,root_weight,visited=candidate_sources(t)
        if typ=="server":
            print("SPARK_SERVER_TREE",code,"weight",round(root_weight,1),
                  "flat_nodes",len(t.children),"refs",len(t.childrenRefs),"visited",visited)
        out["threads"].append({
            "thread_class":typ,
            "root_weight":round(root_weight,2),
            "root_children":len(t.childrenRefs),
            "flattened_node_count":len(t.children),
            "visited_node_count":visited,
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
                shown={"server":0,"worldgen_worker":0,"fork_join_worker":0,"render":0}
                for t in entry["threads"]:
                    cls=t["thread_class"]
                    limit={"server":1,"render":1,"worldgen_worker":2,"fork_join_worker":1}[cls]
                    if shown[cls]<limit:
                        shown[cls]+=1
                        print("SPARK_THREAD_METHODS",code,cls,"root",t["root_weight"],json.dumps(t["top_methods"][:12])[:3000])
            except Exception as exc:
                print("SPARK_RAW_PROBE_FAILURE",code,type(exc).__name__,str(exc)[:130])
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
