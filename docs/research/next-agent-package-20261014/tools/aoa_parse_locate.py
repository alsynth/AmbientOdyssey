#!/usr/bin/env python3
"""Turn a latest.log containing AOA| lines into per-structure locate verdicts.

  python tools/aoa_parse_locate.py latest.log [--csv out.csv]

Verdicts: LOCATED (nearest distance), NOT FOUND (in N searches; NOT proof of absence), CONTROL FAILED (the vanilla control was not found, so no verdict can be trusted for that
dimension), NO RESULT (planned but never printed: the function did not run), INCOMPLETE (the run stopped before AOA|DONE).
"""
from __future__ import annotations
import argparse, collections, csv, re, sys
from pathlib import Path

CONTROL_IDS = {"minecraft:village_plains", "minecraft:mineshaft", "minecraft:fortress", "minecraft:end_city"}
LINE = re.compile(r"AOA\|LOCATE\|([a-z0-9_.-]+:[a-z0-9_./-]+)\|([a-z_]+)\|origin=(-?\d+),(-?\d+)\|found=(\d+)\|dist=(-?\d+)")


def parse(text: str) -> dict:
    res = collections.defaultdict(list); plan = None; done = False; version = None
    for raw in text.splitlines():
        if "AOA|" not in raw: continue
        line = raw[raw.index("AOA|"):].strip()
        m = LINE.match(line)
        if m: res[(m.group(1), m.group(2))].append((int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))); continue
        if line.startswith("AOA|PLAN|"): plan = int(line.split("|")[2])
        elif line.startswith("AOA|DONE"): done = True
        elif line.startswith("AOA|VERSION|"): version = line.split("|")[2]
    return {"results": res, "plan": plan, "done": done, "version": version}


def verdicts(p: dict) -> list[dict]:
    res = p["results"]; out = []
    ctrl_ok = {}
    has_control = {d for (s, d) in res if s in CONTROL_IDS}          # a dimension with no control search at all (Eternal Starlight) gets a weaker verdict, not a failed control
    for (s, d), v in res.items():
        if s in CONTROL_IDS: ctrl_ok[d] = ctrl_ok.get(d, False) or any(x[2] for x in v)
    for (s, d), v in sorted(res.items()):
        hits = [x for x in v if x[2]]
        if s in CONTROL_IDS:
            verdict = "CONTROL OK" if hits else "CONTROL FAILED"
        elif hits: verdict = "LOCATED"
        elif d not in has_control: verdict = f"NOT FOUND in {len(v)} searches (no control exists for this dimension: weaker)"
        elif not ctrl_ok.get(d, False): verdict = "CONTROL FAILED (no verdict)"
        else: verdict = f"NOT FOUND in {len(v)} searches"
        out.append({"structure": s, "dimension": d, "searches": len(v), "found_in": len(hits), "nearest_blocks": min((x[3] for x in hits), default=""), "verdict": verdict})
    if not p["done"]: out.append({"structure": "(run)", "dimension": "", "searches": sum(len(v) for v in res.values()), "found_in": "", "nearest_blocks": "", "verdict": f"INCOMPLETE: no AOA|DONE line (plan {p['plan']})"})
    elif p["plan"] is not None and sum(len(v) for v in res.values()) < p["plan"]:
        out.append({"structure": "(run)", "dimension": "", "searches": sum(len(v) for v in res.values()), "found_in": "", "nearest_blocks": "", "verdict": f"NO RESULT for {p['plan'] - sum(len(v) for v in res.values())} planned searches"})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("log", type=Path); ap.add_argument("--csv", type=Path)
    a = ap.parse_args(argv)
    p = parse(a.log.read_text(encoding="utf-8", errors="replace"))
    v = verdicts(p)
    print(f"{'structure':44} {'dim':11} {'found/searches':>14} {'nearest':>8}  verdict")
    for r in v: print(f"{r['structure']:44} {r['dimension']:11} {str(r['found_in'])+'/'+str(r['searches']):>14} {str(r['nearest_blocks']):>8}  {r['verdict']}")
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(v[0]), lineterminator="\n"); w.writeheader(); w.writerows(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
