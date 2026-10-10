#!/usr/bin/env python3
"""Exact v0.4 packaging/bridge regressions; no Minecraft runtime claim."""
import argparse
import copy
import gzip
import io
import json
import sys
import zipfile
from hashlib import sha256
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_release_030 import validate_connector_stack

PINS = {618790: 7033510, 890127: 8654089, 889079: 8726480,
        532610: 6785734, 520110: 6375480, 623764: 5988164, 1202066: 8952784}

def verify(archive, private=False):
    lock = json.loads((ROOT / 'release_030/release-lock.json').read_text())
    with zipfile.ZipFile(ROOT / lock['baseline']) as z:
        baseline = {x['projectID']: x['fileID'] for x in json.loads(z.read('manifest.json'))['files']}
    validate_connector_stack(lock, baseline)
    # Fail closed when dependencies, file identity, or loader truth are changed.
    for mutate in ('missing_connector', 'wrong_minecells', 'false_loader', 'extra_fabric'):
        bad = copy.deepcopy(lock)
        if mutate == 'missing_connector':
            del bad['additions']['content-040-minecells-connector']
        elif mutate == 'wrong_minecells':
            bad['additions']['content-040-minecells-minecells']['id'] += 1
        elif mutate == 'false_loader':
            bad['additions']['content-040-minecells-minecells']['gameVersions'] = ['1.21.1', 'NeoForge']
        else:
            bad['additions']['fabric-api'] = {'projectId': 306612, 'id': 1}
        try:
            validate_connector_stack(bad, baseline)
        except AssertionError:
            pass
        else:
            raise AssertionError('Bridge regression not rejected: ' + mutate)
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        assert z.testzip() is None and len(names) == len(set(names))
        for name in names:
            p = PurePosixPath(name)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in name, name
        m = json.loads(z.read('manifest.json'))
        assert m['version'] == '0.4.0-experimental-minecells-fg-questlog-q1-manual'
        assert m['minecraft']['modLoaders'] == [{'id': 'neoforge-21.1.252', 'primary': True}]
        refs = {e['projectID']: e['fileID'] for e in m['files']}
        assert len(refs) == len(m['files']) == 331
        assert all(refs.get(pid) == fid for pid, fid in PINS.items())
        assert 306612 not in refs and 284876 not in refs and 631098 not in refs
        jars = {n for n in names if n.startswith('overrides/mods/') and n.endswith('.jar')}
        expected = {'overrides/mods/' + e['fileName'] for e in lock.get('private_modrinth_addons', [])}
        assert jars == (expected if private else set())
        if private:
            for e in lock['private_modrinth_addons']:
                from hashlib import sha1, sha512
                b = z.read('overrides/mods/' + e['fileName'])
                assert len(b) == e['size'] and sha1(b).hexdigest() == e['sha1'] and sha512(b).hexdigest() == e['sha512']
        json_count = 0
        for n in names:
            # Minecraft data/resource packs require JSON. Mod configs may use
            # comment-tolerant codecs even with a .json suffix; do not conflate them.
            if n == 'manifest.json' or ('/paxi/' in n and (n.endswith('.json') or n.endswith('/pack.mcmeta'))):
                json.loads(z.read(n))
                json_count += 1
        import nbtlib
        prefix = 'overrides/config/paxi/datapacks/ao_worldgen_final_fixes/data/'
        owners = ('adventuredungeons', 'block_factorys_bosses', 'irons_spellbooks', 'create_easy_structures')
        patched = [n for n in names if n.startswith(prefix) and n.endswith('.nbt') and n[len(prefix):].split('/')[0] in owners]
        assert len(patched) == 273
        for n in patched:
            d = nbtlib.File.parse(io.BytesIO(gzip.decompress(z.read(n))))
            for block in d['blocks']:
                if str(d['palette'][int(block['state'])]['Name']) == 'minecraft:jigsaw':
                    assert str(block.get('nbt', {}).get('pool', '')) != 'minecraft:', n
        rule = z.read('overrides/config/paxi/datapacks/ao_server_rules/data/ambient_odyssey/function/server_rules.mcfunction').decode()
        assert 'gamerule playersSleepingPercentage 30' in rule
        technical = 'overrides/config/paxi/datapacks/ao_technical_fixes/'
        fire = json.loads(z.read(technical + 'data/traveloptics/tags/entity_type/element_fire.json'))
        assert 'cataclysm:ignited_revenant' in fire['values'] and 'irons_spellbooks:pyromancer' in fire['values']
        for tag in ('inky_cap', 'morel', 'truffle'):
            bridge = json.loads(z.read(technical + 'data/forge/tags/item/mushrooms/' + tag + '.json'))
            assert bridge == {'replace': False, 'values': ['#c:mushrooms/' + tag]}
        import tomllib
        quest_config = tomllib.loads(z.read('overrides/config/questlog-client.toml').decode('utf-8'))
        button = quest_config['button']
        assert button['enabled'] and button['showBadge'] and not button['relativeToInventory']
        assert (button['x'], button['y']) == (38, 38)
        pilot_prefix='overrides/config/questlog/'
        pilot_quests=[n for n in names if n.startswith(pilot_prefix+'quests/') and n.endswith('.json')]
        pilot_chapters=[n for n in names if n.startswith(pilot_prefix+'chapters/') and n.endswith('.json')]
        assert len(pilot_quests)==50 and len(pilot_chapters)==13, 'Pilot quest campaign missing'
        from tools.validate_v04_quest_campaign import validate as validate_q1
        assert validate_q1()==50
        for n in pilot_quests+pilot_chapters:
            json.loads(z.read(n))
        # Separate three-chapter no-reward FTB Field Manual (14 + 8 + 7).
        from tools.validate_v04_ftb_manual import run as validate_manual
        assert validate_manual()==29
        from tools.validate_v04_ftb_manual import parse_ftb_text
        manual_chapters=['ao_field_manual','ao_tips_tricks','ao_keybinds']
        for slug in manual_chapters:
            path='overrides/config/ftbquests/quests/chapters/'+slug+'.snbt'
            assert path in names
            parse_ftb_text(z.read(path).decode('utf-8'))
        loc='overrides/config/ftbquests/quests/lang/en_us.snbt'
        assert loc in names
        parse_ftb_text(z.read(loc).decode('utf-8'))
        assert 'overrides/config/ftbquests/quests/chapters/when_dungeons_arise.snbt' in names
        options = z.read('overrides/config/defaultoptions/options.txt').decode().splitlines()
        assert 'renderDistance:12' in options and 'simulationDistance:6' in options
    return {'archive': Path(archive).name, 'sha256': sha256(Path(archive).read_bytes()).hexdigest(),
            'bytes': Path(archive).stat().st_size, 'entries': len(names), 'manifest_refs': len(refs),
            'parsed_json': json_count, 'parsed_repaired_nbt': len(patched),
            'negative_bridge_tests': 4, 'private_neoreef': private, 'runtime_claim': False}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive', type=Path)
    p.add_argument('--private', action='store_true')
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    result = verify(a.archive, a.private)
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
