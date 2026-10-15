#!/usr/bin/env python3
"""Turn a Minecraft latest.log from the AOT edit test into per-boss verdicts. Standard library only.

  python tools/aot_parse_log.py "<instance>/logs/latest.log" --csv aot_results.csv

Verdict logic (all values come from AOT| lines the datapack prints):
  CONTROL  index 0 (vanilla zombie) must scale ~4x on max health and per-hit damage, otherwise the run is INVALID.
  HP       WORKS    : max_health attribute after the +300% modifier is 3.5-4.5x the baseline AND current health reached it
           CAPPED   : attribute rose to the vanilla 1024 limit and health followed (route works; headroom limited to 1024)
           MAX-ONLY : attribute scaled but current health did not follow (code resets/caps health)
           FAILS    : attribute did not scale          NO-ATTR: boss has no max_health attribute
  DAMAGE   WORKS    : mean hit in phase B is 3.3-4.7x phase A (needs >=2 hits in each phase)
           SCALES   : mean hit >=2x and >=40% of B hits exceed 1.5x the largest A hit (scales; attack mix distorts the ratio)
           PARTIAL  : mean hit grew 1.25-3.3x, or only some hits grew (mixed attacks; fixed-damage attacks present)
           FIXED    : mean hit within 0.8-1.25x     NO-ATTR: boss has no attack_damage attribute (hits may still scale if code uses another source)
           NO-DATA  : fewer than 2 hits in a phase (boss did not attack: check manually)
"""
from __future__ import annotations

import argparse
import csv
import re
import statistics
import sys
from collections import defaultdict
import collections
from pathlib import Path

LINE = re.compile(r"AOT\|(.*)$")


def parse_lines(text: str):
    for raw in text.splitlines():
        m = LINE.search(raw)
        if m: yield m.group(1).strip()


def kv(parts):
    out = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            try: out[k] = int(v)
            except ValueError: out[k] = v
    return out


def collect(text: str) -> dict:
    bosses = defaultdict(lambda: {"id": "?", "status": [], "hits": {"1": [], "2": []}, "cnt": {}, "base": None, "mod": None})
    meta = {"all_done": False, "stopped": False}
    cur = None                                                     # ENV / NBT diagnostic lines carry no index: they belong to the latest boss slot
    for line in parse_lines(text):
        p = line.split("|")
        tag = p[0]
        if tag == "BASE" or tag == "MOD":
            i = int(p[1]); cur = i; b = bosses[i]; b["id"] = p[2]; b["base" if tag == "BASE" else "mod"] = kv(p[3:])
        elif tag == "BOSS":
            i = int(p[1]); cur = i
            if p[3] == "START" and i in bosses: del bosses[i]       # the slot was started again (interrupted first attempt): the latest attempt wins
            b = bosses[i]; b["id"] = p[2]; b["status"].append(p[3])
        elif tag == "ENV" and cur is not None:
            bosses[cur].setdefault("env", []).append("|".join(p[1:]))
        elif tag == "NBT" and cur is not None and len(p) >= 2:
            bosses[cur].setdefault("nbt", {})[p[1]] = "|".join(p[2:])
        elif tag == "HIT":
            i, ph, d = int(p[1]), p[2], int(p[3])
            if ph in ("1", "2"): bosses[i]["hits"][ph].append(d / 10.0)
        elif tag == "END":
            i = int(p[1]); bosses[i]["cnt"][p[2]] = kv(p[3:])
        elif tag == "PLAYER": meta["player"] = kv(p[1:])
        elif tag == "SELFTEST": meta["selftest"] = kv(p[1:])
        elif tag == "SELFTEST_FAILED": meta["selftest_failed"] = True
        elif tag == "CHAIN": meta["chain"] = kv(p[2:] ) | {"name": p[1]}
        elif tag == "ALL_DONE": meta["all_done"] = True
        elif tag == "STOPPED": meta["stopped"] = True
    return {"bosses": dict(bosses), "meta": meta}


def mean(xs): return sum(xs) / len(xs) if xs else 0.0


ATTR_RE = re.compile(r'\{base:([^,]+),id:"([^"]+)"(?:,modifiers:\[(.*?)\])?\}')
MOD_RE = re.compile(r'\{amount:([^,}]+),id:"([^"]+)",operation:"([^"]+)"\}')


def attribute_modifiers(nbt_text: str) -> dict:
    """{attribute short name: (base, [(modifier id, amount, operation), ...])} from the SNBT of an entity's `attributes` list."""
    out = {}
    for m in ATTR_RE.finditer(nbt_text or ""):
        name = m.group(2).split(":", 1)[-1].replace("generic.", "").replace("player.", "")
        out[name] = (m.group(1), MOD_RE.findall(m.group(3) or ""))
    return out


def diagnostics(bosses: dict) -> str:
    rows = [(i, b) for i, b in sorted(bosses.items()) if b.get("env") or b.get("nbt")]
    if not rows: return ""
    L = ["", "DIAGNOSTICS (environment and attribute modifiers present at spawn, before the AOT test modifiers)"]
    for i, b in rows:
        base = b["base"] or {}
        L.append(f"  slot {i} {b['id']}: baseline max health {base.get('max100', 0) / 100:g}, attack {base.get('atk100', 0) / 100:g}")
        if b.get("env"): L.append("    env: " + "; ".join(b["env"]))
        nbt = b.get("nbt", {})
        attrs = attribute_modifiers(nbt.get("attributes", "") or nbt.get("Attributes", ""))
        if not nbt.get("attributes") and not nbt.get("Attributes"): L.append("    attributes NBT: (nothing printed: neither key exists on this entity)")
        for want in ("max_health", "attack_damage", "armor", "movement_speed"):
            if want in attrs:
                bs, mods = attrs[want]
                L.append(f"    {want}: base {bs}" + (" | modifiers: " + ", ".join(f"{mid} {amt} {op}" for amt, mid, op in mods) if mods else " | no modifiers"))
        for k in ("ActiveEffects", "neoforge:attachments", "Tags"):
            if nbt.get(k): L.append(f"    {k}: {nbt[k][:200]}")
    L.append("")
    L.append("HIT SIZES per slot, rounded (how many hits of each size; phase A = no AOT modifier, phase B = attack attribute x4). A size that is the same in A and B is NOT scaled by the attack attribute.")
    for i, b in rows:
        for ph, label in (("1", "A"), ("2", "B")):
            h = b["hits"][ph]
            if h:
                c = collections.Counter(round(x) for x in h)
                L.append(f"  slot {i} {label} ({len(h)} hits): " + ", ".join(f"{v}x{n}" for v, n in sorted(c.items(), reverse=True)[:14]))
    ids = collections.defaultdict(list)
    for i, b in rows:
        if b["base"]: ids[b["id"]].append((b["base"]["max100"] / 100, b["base"]["atk100"] / 100))
    for eid, vals in ids.items():
        if len(vals) > 1:
            L.append(f"  {eid} baselines over {len(vals)} spawns: " + ", ".join(f"{h:g}/{a:g}" for h, a in vals) + (" -> STABLE" if len(set(vals)) == 1 else " -> VARIES between spawns"))
    return "\n".join(L)


HP_CAP = 1024.0   # vanilla max_health attribute limit; modifiers cannot push a boss above this


def hp_verdict(b):
    base, mod = b["base"], b["mod"]
    if not base or not mod: return "NO-DATA", ""
    if not base.get("hasmax"): return "NO-ATTR", ""
    if base["max100"] <= 0: return "NO-DATA", ""
    ratio = mod["max100"] / base["max100"]
    note = f"max {base['max100']/100:g} -> {mod['max100']/100:g} (x{ratio:.2f}); hp after {mod['hp100']/100:g}"
    followed = mod["hp100"] >= 0.9 * mod["max100"]
    if abs(mod["max100"] / 100 - HP_CAP) < 0.5 and ratio < 3.5:   # pushed up to the cap, health followed: the route works
        return ("CAPPED" if followed else "MAX-ONLY"), note + f"; capped at {HP_CAP:g} (needs x4 = {base['max100']/25:g})"
    if 3.5 <= ratio <= 4.5:
        return ("WORKS" if followed else "MAX-ONLY"), note
    return "FAILS", note


def dmg_verdict(b):
    base, mod = b["base"], b["mod"]
    a, c = b["hits"]["1"], b["hits"]["2"]
    attr = ""
    if base and mod and base.get("hasatk") and base["atk100"] > 0:
        attr = f"atk attr {base['atk100']/100:g} -> {mod['atk100']/100:g}"
    elif base and not base.get("hasatk"):
        attr = "no attack_damage attribute"
    if len(a) < 2 or len(c) < 2:
        return "NO-DATA", f"hits A={len(a)} B={len(c)}; {attr}".strip("; ")
    ratio = mean(c) / mean(a)
    grew = sum(1 for x in c if x > 1.5 * max(a)) / len(c)
    low = " (low sample)" if min(len(a), len(c)) < 5 else ""
    note = f"mean hit {mean(a):.1f} -> {mean(c):.1f} (x{ratio:.2f}), hits {len(a)}/{len(c)}, {grew:.0%} of B hits exceed 1.5x A max; {attr}{low}"
    if 3.3 <= ratio <= 4.7 and grew >= 0.6: return "WORKS", note
    if ratio >= 2.0 and grew >= 0.4: return "SCALES", note          # clearly scales; attack mix distorts the exact ratio
    if ratio >= 1.25 or grew >= 0.1: return "PARTIAL", note         # only some attacks scale
    return "FIXED", note


def analyse(text: str):
    d = collect(text); rows = []
    for i in sorted(d["bosses"]):
        b = d["bosses"][i]
        if "NO_ENTITY" in b["status"]:
            rows.append((i, b["id"], "NO-ENTITY", "NO-ENTITY", "boss id did not summon (wrong id or mod missing)")); continue
        hv, hn = hp_verdict(b); dv, dn = dmg_verdict(b)
        extra = "; boss gone after phase A" if "GONE_AFTER_A" in b["status"] else ""
        rows.append((i, b["id"], hv, dv, (hn + " | " + dn + extra).strip(" |")))
    ctrl = next((r for r in rows if r[0] == 0), None)
    valid = bool(ctrl and ctrl[2] == "WORKS" and ctrl[3] == "WORKS")
    return rows, valid, d["meta"]


def mod_summary(rows):
    """Group sampled bosses by mod namespace and say whether the samples agree."""
    grp_hp = {"WORKS": "OK", "CAPPED": "OK"}
    grp_dm = {"WORKS": "OK", "SCALES": "OK"}
    by = defaultdict(list)
    for i, bid, hv, dv, _ in rows:
        if i == 0 or hv == "NO-ENTITY": continue
        by[bid.split(":")[0]].append((hv, dv))
    out = {}
    for ns, vs in sorted(by.items()):
        hp = {grp_hp.get(h, h) for h, _ in vs if h != "NO-DATA"}; dm = {grp_dm.get(d, d) for _, d in vs if d != "NO-DATA"}
        agree = len(hp) <= 1 and len(dm) <= 1
        out[ns] = f"{len(vs)} sampled; HP {'/'.join(sorted(hp)) or 'NO-DATA'}, DAMAGE {'/'.join(sorted(dm)) or 'NO-DATA'} -> " + ("consistent" if agree else "INCONSISTENT")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log", type=Path); ap.add_argument("--csv", type=Path)
    a = ap.parse_args(argv)
    rows, valid, meta = analyse(a.log.read_text(encoding="utf-8", errors="replace"))
    if not rows: print("No AOT| lines found. Did the datapack run, and is this the right latest.log?"); return 2
    print(f"{'#':>2} {'boss':42} {'HP':9} {'DAMAGE':9}  details")
    for i, bid, hv, dv, note in rows: print(f"{i:>2} {bid:42} {hv:9} {dv:9}  {note}")
    d = diagnostics(collect(a.log.read_text(encoding="utf-8", errors="replace"))["bosses"])
    if d: print(d)
    ch = meta.get("chain")
    if ch: print(f"\nCHAIN: {ch['name']} (phase_ticks {ch.get('phase_ticks')}, i.e. {ch.get('phase_ticks', 0) / 20:g} s per phase)")
    st = meta.get("selftest")
    if st:
        print(f"\nSELF-TEST: max health {st.get('max')}, damage counted {st.get('dmg10', 0)/10:g} (expected 50), health after healing {st.get('hp')} -> " + ("PASSED" if st.get("ok") == 1 else "FAILED: the run did not start; an item/mod is blocking healing, max health or damage counting"))
    pl = meta.get("player")
    if pl:
        ok = pl.get("max", 0) >= 100
        print(f"\nPLAYER: max health {pl.get('max')}, health {pl.get('hp')} -> " + ("ok" if ok else "WARNING: max health did not hold; an item or mod resets it, so hits may be cancelled/uncounted. Remove health/immortality items and rerun."))
    print("\nPER-MOD CONSISTENCY (samples only; INCONSISTENT means test the rest of that mod):")
    for ns, summary in mod_summary(rows).items(): print(f"  {ns:18} {summary}")
    print("\nCONTROL (vanilla zombie) VALID:" , "yes" if valid else "NO - results are not trustworthy")
    print("run finished:", "yes" if meta["all_done"] else "no (stopped early or still running)")
    if a.csv:
        with a.csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n"); w.writerow(["idx", "boss", "hp_verdict", "damage_verdict", "details"]); w.writerows(rows)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
