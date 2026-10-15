"""Generate the owner-approved Pinnacle override: native five epic gear criteria + Captain Cornelia kill.

Owner decision (15 Oct 2026): Pinnacle = the native five epic-or-better gear pieces PLUS a kill of
Captain Cornelia, which replaces the native Ender Dragon kill. Built from the exact native Apotheosis
8.9.0 file by text substitution, so every byte except the dragon criterion (and its requirement key)
is native. No minecraft:impossible.

  python tools/compile_pinnacle_cornelia_gate.py --apotheosis-jar <Apotheosis-1.21.1-8.9.0.jar> [--check]
"""
import argparse, hashlib, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APOTHEOSIS_SHA256 = '23a8b4a21d0d8744f097c77c8a96fcba14c4b95f3b1bb542412f40dab272872e'  # R4 pin
NATIVE_MEMBER = 'data/apotheosis/advancement/progression/pinnacle.json'
NATIVE_SHA256 = 'd456b49dc2bdc49178f7a9c6600e58619e3822dfce9b5154791a2b05a8499f62'
CORNELIA = 'aquamirae:captain_cornelia'
OVERLAY = ROOT / 'release_030/experimental_overlays/v050/overrides/config/paxi'
DATA = OVERLAY / 'datapacks/ao_campaign_gates'
LANG = OVERLAY / 'resourcepacks/ao_campaign_gates_lang'

NATIVE_DRAGON = '''        "kill_ender_dragon": {
            "conditions": {
                "entity": [
                    {
                        "condition": "minecraft:entity_properties",
                        "entity": "this",
                        "predicate": {
                            "type": "minecraft:ender_dragon"
                        }
                    }
                ]
            },
            "trigger": "minecraft:player_killed_entity"
        }'''
CORNELIA_KILL = NATIVE_DRAGON.replace('"kill_ender_dragon"', '"kill_captain_cornelia"').replace('"minecraft:ender_dragon"', '"%s"' % CORNELIA)


def native_bytes(jar):
    if hashlib.sha256(Path(jar).read_bytes()).hexdigest() != APOTHEOSIS_SHA256:
        raise ValueError('Not the R4-pinned Apotheosis 8.9.0 JAR')
    data = zipfile.ZipFile(jar).read(NATIVE_MEMBER)
    if hashlib.sha256(data).hexdigest() != NATIVE_SHA256: raise ValueError('Native Pinnacle advancement changed')
    return data


def build(native):
    text = native.decode('utf-8')
    for old, count in ((NATIVE_DRAGON, 1), ('"kill_ender_dragon"', 2)):
        if text.count(old) != count: raise ValueError('Unexpected native structure for ' + old[:40])
    text = text.replace(NATIVE_DRAGON, CORNELIA_KILL).replace('"kill_ender_dragon"', '"kill_captain_cornelia"')
    out = {
        DATA / 'pack.mcmeta': (json.dumps({'pack': {'pack_format': 48, 'description': 'AO Pinnacle: native epic gear + Captain Cornelia kill'}}) + '\n').encode(),
        DATA / 'data/apotheosis/advancement/progression/pinnacle.json': text.encode('utf-8'),
        LANG / 'pack.mcmeta': (json.dumps({'pack': {'pack_format': 34, 'description': 'AO Pinnacle requirement text'}}, indent=2) + '\n').encode(),
        LANG / 'assets/apotheosis/lang/en_us.json': (json.dumps({
            'advancements.apotheosis.progression.pinnacle.desc': 'Entering the Pinnacle requires defeating the Ghost of Captain Cornelia, and acquiring a full set of Epic gear',
            'advancements.apotheosis.progression.pinnacle.criteria.kill_captain_cornelia': 'Slay the Ghost of Captain Cornelia',
        }, indent=2) + '\n').encode(),
    }
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--apotheosis-jar', required=True); ap.add_argument('--check', action='store_true')
    a = ap.parse_args(); files = build(native_bytes(a.apotheosis_jar))
    if a.check:
        stale = [str(p.relative_to(ROOT)) for p, b in files.items() if not p.is_file() or p.read_bytes() != b]
        print('PASS' if not stale else 'STALE ' + ', '.join(stale)); sys.exit(1 if stale else 0)
    for p, b in files.items(): p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
    print('wrote', len(files), 'files')


if __name__ == '__main__':
    main()
