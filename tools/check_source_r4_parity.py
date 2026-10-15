"""Compare editable source and/or a rebuilt import against the exact published R4 ZIP.

Read-only. Classifies every differing member as:
  eol_only       bytes equal after CRLF->LF (build-checkout line endings)
  mod_rewritten  listed in release_030/MOD_REWRITTEN_CONFIGS.json
  real           anything else (exit code 1)

  python tools/check_source_r4_parity.py --r4 <R4.zip> [--rebuild <rebuilt.zip>] [--report out.json]
"""
import argparse, hashlib, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R4_SHA256 = '31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d'
SRC = ROOT / 'release_030/overrides'


def ignored():
    data = json.loads((ROOT / 'release_030/MOD_REWRITTEN_CONFIGS.json').read_text(encoding='utf-8'))
    return {f['path'] for f in data['files']}


def classify(rel, a, b, skip):
    if a == b: return 'equal'
    if a.replace(b'\r\n', b'\n') == b.replace(b'\r\n', b'\n'): return 'eol_only'
    if rel in skip: return 'mod_rewritten'
    return 'real'


def source_parity(r4, skip):
    out = {}
    for p in sorted(SRC.rglob('*')):
        if not p.is_file(): continue
        rel = p.relative_to(SRC).as_posix()
        name = 'overrides/' + rel
        if name in r4: out[rel] = classify(rel, p.read_bytes(), r4[name], skip)
    return out


def rebuild_parity(r4, rebuilt, skip):
    out = {}
    for name in sorted(set(r4) | set(rebuilt)):
        rel = name[len('overrides/'):] if name.startswith('overrides/') else name
        if name not in rebuilt: out[name] = 'only_r4'
        elif name not in r4: out[name] = 'only_rebuild'
        else: out[name] = classify(rel, rebuilt[name], r4[name], skip)
    return out


def read(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist() if not n.endswith('/')}


def summary(result):
    counts = {}
    for v in result.values(): counts[v] = counts.get(v, 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--r4', required=True, type=Path)
    ap.add_argument('--rebuild', type=Path)
    ap.add_argument('--report', type=Path)
    a = ap.parse_args()
    if hashlib.sha256(a.r4.read_bytes()).hexdigest() != R4_SHA256:
        sys.exit('Not the published R4 ZIP')
    skip = ignored(); r4 = read(a.r4)
    report = {'r4_sha256': R4_SHA256, 'source': summary(src := source_parity(r4, skip)),
              'source_real': sorted(k for k, v in src.items() if v == 'real'),
              'source_mod_rewritten': sorted(k for k, v in src.items() if v == 'mod_rewritten')}
    bad = bool(report['source_real'])
    if a.rebuild:
        reb = rebuild_parity(r4, read(a.rebuild), skip)
        report['rebuild'] = summary(reb)
        report['rebuild_not_equal'] = {k: v for k, v in reb.items() if v != 'equal'}
        bad |= any(v in ('real', 'only_r4', 'only_rebuild') for v in reb.values())
    text = json.dumps(report, indent=2) + '\n'
    if a.report: a.report.write_text(text, encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in report.items() if k in ('source', 'source_real', 'rebuild')}, indent=2))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
