#!/usr/bin/env python3
"""Add the Test 6 addon JARs to the current resource index (keeps the 196 prior snapshots).
Usage: python3 audit_test6_addons.py --jars DIR   (DIR holds only the audited addon JARs)
Writes release_030/evidence/jar-resource-index-test6.json.gz and test6-addon-jars.json."""
import argparse, gzip, json
from pathlib import Path
from audit_jars_031 import inventory

ROOT = Path(__file__).resolve().parent
EV = ROOT / 'release_030/evidence'


def main(jars):
    base = json.loads(gzip.decompress((EV / 'jar-resource-index-test5.json.gz').read_bytes()))
    local = inventory(jars)
    known = {r['sha256'] for r in base['jars']}
    fresh = [r for r in local['jars'] if r['sha256'] not in known]
    names = {r['file'] for r in fresh}
    res = {c: dict(t) for c, t in base['resources'].items()}
    for cat, table in local['resources'].items():
        for ident, rows in table.items():
            sel = [r for r in rows if r['jar'] in names]
            if sel:
                res.setdefault(cat, {}).setdefault(ident, []).extend(sel)
    snap = {'jars': base['jars'] + fresh, 'resources': res,
            'optional_resources': base['optional_resources'] + [r for r in local['optional_resources'] if r['jar'] in names],
            'parse_errors': base['parse_errors'] + [r for r in local['parse_errors'] if r['jar'] in names],
            'provenance': {**base.get('provenance', {}), 'test6': f'{len(fresh)} approved addon JARs added to the 196-JAR index'}}
    raw = (json.dumps(snap, sort_keys=True, indent=2) + '\n').encode()
    (EV / 'jar-resource-index-test6.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    (EV / 'test6-addon-jars.json').write_text(json.dumps(
        [{'file': r['file'], 'sha256': r['sha256'], 'bytes': r['bytes'], 'counts': r['counts']} for r in fresh], indent=2) + '\n')
    print(json.dumps({'indexed_jars': len(snap['jars']), 'new': len(fresh), 'parse_errors': len(local['parse_errors'])}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--jars', type=Path, required=True)
    main(ap.parse_args().jars)
