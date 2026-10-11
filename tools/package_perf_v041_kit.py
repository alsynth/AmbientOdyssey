#!/usr/bin/env python3
"""Package self-contained AO v0.4.1 performance test kit, not a modpack ZIP."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
CONTENTS={
    "README.md":"docs/performance/V041_PARALLEL_PERFORMANCE_TESTS_20261011.md",
    "benchmark_template.csv":"docs/performance/V041_PARALLEL_BENCHMARK_TEMPLATE.csv",
    "tools/perf_v041_log_report.py":"tools/perf_v041_log_report.py",
    "tools/perf_v041_trials.py":"tools/perf_v041_trials.py",
}
def build(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(path,"w") as z:
        for inside,source in sorted(CONTENTS.items()):
            blob=(ROOT/source).read_bytes()
            i=ZipInfo(inside,date_time=(2026,10,11,0,0,0))
            i.compress_type=ZIP_DEFLATED
            i.external_attr=0o644<<16
            z.writestr(i,blob)
    verify(path)
    print(f"Prepared performance-only kit: {path.name}; SHA256={hashlib.sha256(path.read_bytes()).hexdigest()}")
def verify(path):
    with ZipFile(path) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(names))
        assert set(names)==set(CONTENTS),"Unexpected contents"
        assert not any(n.lower().endswith(('.jar','.nbt','.log','.sparkprofile')) for n in names),"Raw/private data present"
        assert "manifest.json" not in names,"Do not mistake benchmark kit for CurseForge ZIP"
        for inside,source in CONTENTS.items():
            assert z.read(inside)==(ROOT/source).read_bytes(),inside
    print("PASS: self-contained no-mod no-log benchmark kit, source-matched file bytes")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=ROOT/"build/AO-v041-PERF-TEST-KIT.zip")
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    verify(args.output) if args.verify else build(args.output)
