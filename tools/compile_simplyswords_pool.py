"""Enumerate the full installed Simply Swords sword pool for the campaign boss reward.

Read-only on the JAR. A pool ID must be:
  1. registered unconditionally: string literal in net/sweenus/simplyswords/registry/ItemsRegistry.class
     (compat items for absent mods, e.g. Mythic Metals / Gobber / Eldritch End, are excluded automatically);
  2. classified as a sword by the mod itself: member of #simplyswords:swords or #c:swords (nested tags resolved);
  3. backed by an item model and an en_us item name in the JAR.
Nothing is excluded by judgement; owner-review candidates are listed separately.

  python tools/compile_simplyswords_pool.py --jar <simplyswords-neoforge-1.70.2-1.21.1.jar> [--check]
"""
import argparse, hashlib, json, re, struct, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR_SHA256 = '5e75bd66ea489079d60c9c1ed98762550fbc0bee88cd7af399f17bbeb56608c3'  # R4 pin, simplyswords-neoforge-1.70.2-1.21.1.jar
POOL = ROOT / 'addons/ao-campaign/src/main/resources/ao_sword_pool.json'
EVIDENCE = ROOT / 'docs/handoffs/simplyswords-full-pool-20261015/SIMPLYSWORDS_POOL_EVIDENCE.json'
REGISTRY = 'net/sweenus/simplyswords/registry/ItemsRegistry.class'
NON_BLADE = ('spear', 'glaive', 'halberd', 'scythe', 'chakram', 'greathammer', 'greataxe')


def class_strings(data):
    """String literals (CONSTANT_String targets) of a Java class file."""
    if data[:4] != b'\xca\xfe\xba\xbe': raise ValueError('not a class file')
    count = struct.unpack('>H', data[8:10])[0]; i = 10; k = 1; utf = {}; refs = []
    while k < count:
        t = data[i]
        if t == 1:
            n = struct.unpack('>H', data[i + 1:i + 3])[0]; utf[k] = data[i + 3:i + 3 + n].decode('utf-8'); i += 3 + n
        elif t in (3, 4, 9, 10, 11, 12, 17, 18): i += 5
        elif t in (5, 6): i += 9; k += 1
        elif t in (7, 16, 19, 20): i += 3
        elif t == 8: refs.append(struct.unpack('>H', data[i + 1:i + 3])[0]); i += 3
        elif t == 15: i += 4
        else: raise ValueError('unknown constant tag %d' % t)
        k += 1
    return [utf[r] for r in refs]


def tag(z, names, ns, path, seen):
    member = 'data/%s/tags/item/%s.json' % (ns, path)
    if member not in names: return set()
    out = set()
    for v in json.loads(z.read(member))['values']:
        vid = v if isinstance(v, str) else v['id']
        if vid.startswith('#'):
            key = tuple(vid[1:].split(':', 1))
            if key not in seen: seen.add(key); out |= tag(z, names, key[0], key[1], seen)
        else: out.add(vid)
    return out


def build(jar):
    data = Path(jar).read_bytes()
    if hashlib.sha256(data).hexdigest() != JAR_SHA256: raise ValueError('Not the R4-pinned Simply Swords JAR')
    z = zipfile.ZipFile(jar); names = set(z.namelist())
    registered = {'simplyswords:' + s for s in class_strings(z.read(REGISTRY))
                  if re.fullmatch(r'[a-z0-9_]+', s) and s != 'simplyswords'}
    swords_tag = tag(z, names, 'simplyswords', 'swords', set())
    c_swords = tag(z, names, 'c', 'swords', set())
    uniques = tag(z, names, 'simplyswords', 'uniques', set())
    lootable = tag(z, names, 'simplyswords', 'lootable_uniques', set())
    lang = json.loads(z.read('assets/simplyswords/lang/en_us.json'))
    rows = []
    for i in sorted((swords_tag | c_swords) & registered):
        p = i.split(':', 1)[1]
        row = {'id': i, 'name': lang.get('item.simplyswords.' + p), 'registered_literal': True,
               'in_simplyswords_swords': i in swords_tag, 'in_c_swords': i in c_swords,
               'item_model': 'assets/simplyswords/models/item/%s.json' % p in names,
               'lang_key': ('item.simplyswords.' + p) in lang, 'unique': i in uniques,
               'native_lootable_unique': i in lootable}
        if not (row['item_model'] and row['lang_key']): raise ValueError('Unverifiable sword ID ' + i)
        rows.append(row)
    pool = [r['id'] for r in rows]
    candidates = {
        'non_blade_weapon_types_tagged_as_swords_by_mod': [i for i in pool if not i in uniques and i.rsplit('_', 1)[-1] in NON_BLADE],
        'novelty_item': [i for i in pool if i == 'simplyswords:sword_on_a_stick'],
        'uniques_not_in_native_lootable_uniques': sorted(set(pool) & uniques - lootable),
    }
    evidence = {
        'jar': Path(jar).name, 'jar_sha256': JAR_SHA256,
        'rule': 'registered in ItemsRegistry AND in #simplyswords:swords or #c:swords AND item model AND en_us name',
        'counts': {'pool': len(pool), 'uniques_in_pool': sum(r['unique'] for r in rows),
                   'registered_literals': len(registered), 'simplyswords_swords_tag': len(swords_tag)},
        'registered_not_swords': sorted(registered - swords_tag - c_swords),
        'tagged_swords_not_registered_count': len(swords_tag - registered),
        'previous_58_uniques_not_registered': sorted(uniques - registered),
        'owner_review_exclusion_candidates': candidates,
        'rows': rows,
    }
    pool_doc = {
        'purpose': 'Separate guaranteed boss reward: one uniformly random sword from this full installed Simply Swords sword pool per eligible boss kill. Independent of the affixed item and Regalia rolls; native drops untouched. Supersedes the unique-only list for this reward (ao_loot_policy.json unique_weapons is kept byte-identical for the R5 toolchain and the test probe).',
        'source_jar': Path(jar).name, 'source_jar_sha256': JAR_SHA256,
        'selection': 'uniform', 'count': len(pool), 'ids': pool,
        'owner_exclusions_applied': [],
    }
    return pool_doc, evidence


def dump(obj): return (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--jar', required=True); ap.add_argument('--check', action='store_true')
    a = ap.parse_args(); pool, evidence = build(a.jar)
    if a.check:
        ok = POOL.read_bytes() == dump(pool) and EVIDENCE.read_bytes() == dump(evidence)
        print('PASS' if ok else 'STALE'); sys.exit(0 if ok else 1)
    POOL.write_bytes(dump(pool)); EVIDENCE.parent.mkdir(parents=True, exist_ok=True); EVIDENCE.write_bytes(dump(evidence))
    print(json.dumps(evidence['counts']), 'candidates:', {k: len(v) for k, v in evidence['owner_review_exclusion_candidates'].items()})


if __name__ == '__main__':
    main()
