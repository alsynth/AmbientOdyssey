#!/usr/bin/env python3
"""Structure Test 6 static regression gates (scope: WDA major split + Mushroom Village).

Reads the built import archive only. PASS here is a static source/export result;
it says nothing about natural generation, density or terrain fit.
Usage: python3 validate_structure_test6.py --archive build/<import>.zip [--report out.json]
"""
import argparse, json, re, sys, zipfile

DP = 'overrides/config/paxi/datapacks/'
SD = DP + 'ao_structure_density/data/'
END_MEMBERS = {'dungeons_arise:aviary', 'dungeons_arise:heavenly_rider',
               'dungeons_arise:heavenly_conqueror', 'dungeons_arise:heavenly_challenger'}
MV = 'dungeons_arise:mushroom_village'
# Test 5 audit1 native values that must not drift
NATIVE_MAJOR = {'salt': 88371663, 'separation': 45, 'spacing': 50, 'frequency': 0.7105263157894737}
BATHHOUSE = {'spacing': 112, 'separation': 48, 'salt': 1984010502, 'frequency': 0.5}


def run(archive):
    z = zipfile.ZipFile(archive)
    names = set(z.namelist())
    J = lambda p: json.loads(z.read(p))
    checks = []

    def check(name, ok, detail=''):
        checks.append({'check': name, 'passed': bool(ok), 'detail': detail})

    major = J(SD + 'dungeons_arise/worldgen/structure_set/major_structures.json')
    minor = J(SD + 'dungeons_arise/worldgen/structure_set/minor_structures.json')
    ow = J(SD + 'ambient_odyssey/worldgen/structure_set/wda_major_overworld.json')
    mv = J(SD + 'ambient_odyssey/worldgen/structure_set/wda_mushroom_village.json')
    bath = J(SD + 'ambient_odyssey/worldgen/structure_set/wda_bathhouse.json')
    land = J(SD + 'ambient_odyssey/worldgen/structure_set/wda_ordinary_land.json')

    major_ids = {s['structure'] for s in major['structures']}
    ow_ids = {s['structure'] for s in ow['structures']}
    check('Native major set is End-only (aviary + 3 Heavenly)', major_ids == END_MEMBERS, sorted(major_ids))
    check('Native major grid/salt/frequency unchanged (End rate preserved)',
          all(major['placement'][k] == v for k, v in NATIVE_MAJOR.items()), major['placement'])
    check('Overworld major owner: 50/45, frequency 0.80',
          ow['placement']['spacing'] == 50 and ow['placement']['separation'] == 45
          and ow['placement']['frequency'] == 0.8, ow['placement'])
    check('Overworld major owner has 20 members and no End member',
          len(ow_ids) == 20 and not (ow_ids & END_MEMBERS), len(ow_ids))
    check('Overworld/End major members disjoint, none duplicated', not (ow_ids & major_ids)
          and len(ow['structures']) == len(ow_ids), '')
    check('Mushroom Village absent from both major sets', MV not in ow_ids and MV not in major_ids, '')
    check('Mushroom Village has exactly one dedicated owner',
          [s['structure'] for s in mv['structures']] == [MV], mv['placement'])
    check('Mushroom Village grid is rare-style (frequency <= 0.5, bounds valid)',
          mv['placement']['frequency'] <= 0.5 and 0 <= mv['placement']['separation'] < mv['placement']['spacing'],
          mv['placement'])

    # every owner of every structure across all AO + native density sets
    owners = {}
    for n in names:
        if n.startswith(SD) and '/worldgen/structure_set/' in n and '/tags/' not in n and n.endswith('.json'):
            sid = re.sub(r'^.*data/([^/]+)/worldgen/structure_set/(.*)\.json$', r'\1:\2', n)
            for s in J(n)['structures']:
                owners.setdefault(s['structure'], []).append(sid)
    check('Mushroom Village has one placement owner in the density pack',
          owners.get(MV) == ['ambient_odyssey:wda_mushroom_village'], owners.get(MV))
    wda_ids = ow_ids | major_ids | {MV}
    dup = {k: v for k, v in owners.items() if k in wda_ids and len(v) > 1}
    check('No WDA major structure has two owners in the density pack', not dup, dup)

    salts = {}
    for n in names:
        if n.startswith(SD) and '/worldgen/structure_set/' in n and '/tags/' not in n and n.endswith('.json'):
            salts.setdefault(J(n)['placement'].get('salt'), []).append(n.split('/')[-1])
    check('New owner salts unique within density pack',
          len(salts[ow['placement']['salt']]) == 1 and len(salts[mv['placement']['salt']]) == 1,
          [ow['placement']['salt'], mv['placement']['salt']])

    check('Bathhouse unchanged (112/48, 0.5)', all(bath['placement'][k] == v for k, v in BATHHOUSE.items()), bath['placement'])
    check('Ordinary WDA set unchanged (28/14, salt 1984010501, 5 members)',
          land['placement']['spacing'] == 28 and land['placement']['separation'] == 14
          and land['placement']['salt'] == 1984010501 and len(land['structures']) == 5, '')

    tag = J(DP + 'ao_compatibility/data/dungeons_arise/tags/worldgen/biome/has_structure/mushroom_village_biomes.json')
    check('Mushroom Village biome tag replaces native with Mushroom Fields only',
          tag == {'replace': True, 'values': ['minecraft:mushroom_fields']}, tag)

    avoid = J(SD + 'ambient_odyssey/tags/worldgen/structure_set/large_land_avoid.json')
    check('large_land_avoid points at the Overworld major owner, not the End-only native set',
          'ambient_odyssey:wda_major_overworld' in avoid['values'] and 'dungeons_arise:major_structures' not in avoid['values'], avoid['values'])
    check('minor_structures exclusion follows the Overworld major owner',
          minor['placement']['exclusion_zone']['other_set'] == 'ambient_odyssey:wda_major_overworld', minor['placement']['exclusion_zone'])
    check('Exclusion target set exists', SD + 'ambient_odyssey/worldgen/structure_set/wda_major_overworld.json' in names, '')

    raw = z.read('overrides/config/cristellib/dungeons_arise/structure_toggle_config.json5').decode()
    tog = json.loads(raw[raw.index('{'):])['major_structures']
    off = {k for k, v in tog.items() if v is False}
    want_off = {i.split(':')[1] for i in ow_ids | {MV}} | {'small_blimp', 'coliseum', 'merchant_campsite',
                'illager_campsite', 'greenwood_pub', 'illager_windmill', 'mushroom_house'}
    check('Cristel native toggles off for Overworld majors, Mushroom Village, Blimp, Coliseum, ordinary houses',
          want_off <= off, sorted(want_off - off))
    check('Cristel native toggles keep End members enabled',
          all(tog[i.split(':')[1]] is True for i in END_MEMBERS), {i: tog.get(i.split(':')[1]) for i in END_MEMBERS})
    rawp = z.read('overrides/config/cristellib/dungeons_arise/structure_placement_config.json5').decode()
    pl = json.loads(rawp[rawp.index('{'):])['major_structures']
    check('Cristel native major placement unchanged for End (0.7105)', abs(pl['frequency'] - NATIVE_MAJOR['frequency']) < 1e-12, pl)

    # Heavenly Overworld clones + Farmers untouched
    for h in ('challenger', 'conqueror', 'rider'):
        p = SD + f'ambient_odyssey/worldgen/structure_set/heavenly_{h}_overworld.json'
        check(f'Heavenly {h} Overworld clone set present', p in names, '')
    farm = [n for n in names if n.startswith(SD + 'farmers_structures/worldgen/structure_set/')]
    check('Farmers: all 20 sets present, salts 1984020000..19 unchanged',
          len(farm) == 20 and sorted(J(n)['placement']['salt'] for n in farm) == list(range(1984020000, 1984020020)), len(farm))

    # ---- Part 2: nine installed mods, selectors, Black Spiral decision ----
    import csv, hashlib
    from pathlib import Path
    ROOT = Path(__file__).resolve().parent
    R = ROOT / 'release_030'
    manifest = json.loads(z.read('manifest.json'))
    lock = json.loads((R / 'release-lock.json').read_text())
    t6 = {v['projectId']: v['id'] for k, v in lock['additions'].items() if k.startswith('test6-')}
    mf = {f['projectID']: f['fileID'] for f in manifest['files']}
    check('Manifest pins exactly the nine Test 6 projects, no duplicate projects',
          len(t6) == 9 and all(mf.get(p) == f for p, f in t6.items()) and len(mf) == len(manifest['files']) == 265 and 284876 not in mf,
          {'pins': len(t6), 'total': len(manifest['files'])})
    expect = {1015146: 5812546, 1015149: 5812553, 783522: 7078283, 1620396: 8983496, 698309: 8082824,
              297680: 6584803, 1010066: 8837992, 949158: 6344382, 979809: 9101011}
    check('Pins match current selections (Structory v1.0.14 working in user world; AAA 2.3.3)', t6 == expect, t6)
    check('Dimensional Doors and its stale config exports are absent (removed after creative-tab failure)',
          284876 not in mf and not any(n in names for n in (
              'overrides/config/dimdoors-config.json5',
              'overrides/config/cristellib/dimdoors/structure_placement_config.json5',
              'overrides/config/cristellib/dimdoors/structure_toggle_config.json5')),
          'retired mod and configs')
    next_pins = {1618019: 9099710, 1490601: 7853647, 1605714: 8703116, 1101111: 8365016}
    check('Four exact-file prefreeze client/content additions match source lock and export',
          all(mf.get(project) == file for project, file in next_pins.items()) and
          all(lock['additions'][key]['projectId'] == project and lock['additions'][key]['id'] == file
              for key, project, file in (
                ('next-better-inventory', 1618019, 9099710),
                ('next-shadow-drop', 1490601, 7853647),
                ('next-borderless-window', 1605714, 8703116),
                ('next-irons-jewelry', 1101111, 8365016))),
          next_pins)
    check('Recommended RAM 10 GiB in manifest', manifest['minecraft'].get('recommendedRam') == 10240,
          manifest['minecraft'].get('recommendedRam'))
    check('Jewelry v2.0.2 avoids Iron Lib downgrade for other Iron mods',
          mf.get(1101111) == 8365016 and len(mf) == 265,
          {'jewelry_file': mf.get(1101111), 'manifest_total': len(mf)})
    shaders = {678384: 5743914, 627557: 8884654}
    check('Two official shader projects pinned (loader-agnostic, no binary redistribution)',
          all(mf.get(p) == fid for p, fid in shaders.items()) and
          all(e.get('contentType') == 'shaders' for k, e in lock['additions'].items()
              if k.startswith('shader-')) and
          len([k for k in lock['additions'] if k.startswith('shader-')]) == 2,
          shaders)
    # A clean install must not greet first-time users with the accessibility narrator.
    defaults = z.read('overrides/config/defaultoptions/options.txt').decode()
    check('Default Options narrator off, canonical hotkey and first-launch accessibility prompt disabled',
          'narrator:0' in defaults and 'narratorHotKey:false' in defaults and
          'onboardAccessibility:false' in defaults and
          'menuBackgroundBlurriness:0' in defaults and 'narratorHotkey:false' not in defaults,
          'Narrator and shader menu defaults')
    requested_test8 = {
        834427: 9063977, # Hybrid Aquatic
        1015115: 5924487, # YUNGs Ocean Monuments
        1717003: 9108729, # Better Shipwrecks
        1197859: 6539516, # FTB Ocean Mobs
        450659: 5937999, # Small Ships
        1331880: 6918744, # Aquatic Creepers
        536254: 8931374, # Aquamirae
        1123977: 9070553, # Fragmentum
        714177: 8332463, # Deeper Oceans
        841262: 7939973, # Oceans Delight
        1644371: 8614631, # Solo Quests
    }
    check('11 user-approved ocean/dependency/solo quest files are pinned for combined testing',
          len(mf) == 265 and all(mf.get(pid) == fid for pid, fid in requested_test8.items()),
          {'expected_projects':262,'tested_new_pins':len(requested_test8)})
    check('Solo Quests disables voluntary team completion sync on fresh worlds',
          'teamSyncEnabled = false' in z.read('overrides/defaultconfigs/ftb_solo_quests-server.toml').decode(),
          'new-world default serverconfig')
    check('WDA and IDAS shared grids no longer select lighthouses; two rare independent grids exist',
          all(
            not any(x.get('structure') == structure for x in json.loads(z.read(base))['structures'])
            for base,structure in (
               ('overrides/config/paxi/datapacks/ao_structure_density/data/dungeons_arise/worldgen/structure_set/minor_structures.json','dungeons_arise:lighthouse'),
               ('overrides/config/paxi/datapacks/ao_structure_density/data/idas/worldgen/structure_set/idas_small.json','idas:abandoned_lighthouse')
            )
          ) and all(
            n in names for n in (
              'overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/wda_lighthouse_rare.json',
              'overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/idas_lighthouse_rare.json'
            )
          ), 'rarity grids')
    p_biome='overrides/config/paxi/datapacks/ao_biome_replacement/data/ambient_odyssey/biolith/biome_placement.json'
    biome_payload=json.loads(z.read(p_biome))
    check('Four new curated surface biomes and stony shoreline replacements are present',
          all(any(e.get('biome')==id for e in biome_payload['replacements']) for id in (
             'biomeswevegone:baobab_savanna','biomeswevegone:tropical_rainforest',
             'biomesoplenty:dryland','biomeswevegone:dacite_shore')) and
          any(e.get('target')=='minecraft:stony_shore' and e.get('biome')=='biomeswevegone:dacite_shore'
              for e in biome_payload['replacements']),len(biome_payload['replacements']))
    check('Defer Beyond the Ocean and explicitly excluded Tide 2, Sea Myths, Create Deep Seas, Upgrade Aquatic',
          all(key not in lock['additions'] for key in (
              'beyond-the-ocean','tide-2','sea-myths','create-deep-seas','upgrade-aquatic')),
          'not staged in source lock')
    safety_pins = {883374:9063597,1145462:6880789,401229:7782196,488090:7318664}
    check('Crash recovery: My Picture Frame no longer installed, four APIs and flight projects pinned',
          1582023 not in mf and all(mf.get(project)==file for project,file in safety_pins.items()) and
          all(lock['remove_projects'].get('my-picture-frame')==1582023 for _ in range(1)),
          {'new_projects':safety_pins,'picture_frame_excluded':1582023 not in mf})
    flight_paxi='overrides/config/paxi/datapacks/ao_flight_balance/'
    basic_recipe=J(flight_paxi+'data/flight_rings/recipe/basic_ring.json')
    advanced_recipe=J(flight_paxi+'data/flight_rings/recipe/advanced_ring.json')
    check('Flight Rings recipes are overridden with Nether/late-game gates',
          basic_recipe['result']['id']=='flight_rings:basic_ring' and
          advanced_recipe['result']['id']=='flight_rings:advanced_ring' and
          basic_recipe['key']['B']['item']=='minecraft:blaze_rod' and
          advanced_recipe['key']['N']['item']=='minecraft:nether_star' and
          advanced_recipe['key']['A']['item']=='flight_rings:basic_ring', 'Paxi recipe overrides')
    check('Private test only: vendor-supplied Better Bastions and NeoReefRedux jars intact',
          all(x in names for x in (
           'overrides/mods/betterbastions-1.0.0+neoforge-1.21.1.jar',
           'overrides/mods/neoreefredux-1.0.jar')),'Third-party JAR overrides: NOT CurseForge moderation-ready')
    check('User-supplied Ambient Odyssey artwork included for manual CurseForge icon selection',
          'overrides/Ambient-Odyssey-Icon.png' in names,'Root instance image is not guaranteed to set profile avatar')
    # Test 8.3: source-backed collision mitigation and 1.21.1 recipe codec correction.
    create_windmill=J(SD+'create_structures_arise/worldgen/structure_set/windmill.json')
    check('Independent Create: Structures Arise windmill salt, original 90/10 spacing maintained',
          create_windmill['structures']==[{'structure':'create_structures_arise:windmill','weight':1}]
          and all(create_windmill['placement'][k]==v for k,v in (
              ('type','minecraft:random_spread'),('spacing',90),('separation',10),
              ('salt',1543892757))) and create_windmill['placement']['salt'] != 353987075,
          create_windmill['placement'])
    for title,srcitem,outitem in (
        ('basic','flight_rings:basic_ring','minecraft:gold_ingot'),
        ('advanced','flight_rings:advanced_ring','minecraft:netherite_ingot')
    ):
        recipe=J(DP+'ao_flight_balance/data/flight_rings/recipe/smelt_'+title+'_ring.json')
        check('Flight Rings '+title+' smelting recipe compatible with MC 1.21.1',
              recipe['type']=='minecraft:smelting' and
              recipe['ingredient']=={'item':srcitem} and
              recipe['result']=={'id':outitem,'count':1}, recipe)
    skull_fix=J(DP+'ao_worldgen_final_fixes/data/additionalstructures/tags/worldgen/biome/has_structure/skeleton_skull.json')
    check('Additional Structures 1.21.1 skeleton-skull tag preserves native biomes and makes Pale Garden optional',
          skull_fix == {'replace':True,'values':['#c:is_badlands','#c:is_wasteland',
                  {'id':'minecraft:pale_garden','required':False}]},
          skull_fix)
    approved = json.loads((R / 'approved-structure-additions.json').read_text())
    jars = json.loads((R / 'evidence/test6-addon-jars.json').read_text())
    # Structory v1.0.17 was SHA-audited but fails on NeoForge 1.21.1; its
    # replacement v1.0.14 loaded in a user world but lacks independent JAR SHA.
    # Verify the eight previously audited binaries against historical evidence.
    former_structory = next(m for m in approved['mods'] if m['projectID'] == 783522)['historic_invalid_file']['sha256']
    historical = {j['sha256'] for j in jars if j['sha256'] == former_structory}
    remaining = [m['sha256'] for m in approved['mods'] if m['projectID'] != 783522]
    check('Eight unchanged addon binary hashes match historical evidence; replacement Structory SHA pending',
          len(jars) == 9 and len(historical) == 1 and len(remaining) == 8 and
          sorted(remaining) == sorted(j['sha256'] for j in jars if j['sha256'] not in historical) and
          next(m for m in approved['mods'] if m['projectID'] == 783522)['fileID'] == 7078283,
          {'historical_binaries': len(jars), 'current_sha_verified': len(remaining)})
    check('No third-party JAR bundled in the export', not any(n.startswith('overrides/mods/') for n in names), '')

    roster = json.loads((R / 'biome-roster.json').read_text())
    curated = {f'{ns}:{n}' for ns, ns_names in roster.items() for n in ns_names} | {'streamsreflowing:stream'}
    nether = {'regions_unexplored:infernal_holt', 'regions_unexplored:blackstone_basin'}
    comp = json.loads((R / 'structure-compatibility.json').read_text())
    derived = [k for k, v in comp['provenance'].items() if isinstance(v, dict) and str(v.get('reason', '')).startswith('Test 6: ')]
    tag_ids = [k for k in derived if k in comp['biome_tags']]
    bad, nethers, missing = [], [], []
    for tid in tag_ids:
        ns, name = tid.split(':', 1)
        path = DP + f'ao_compatibility/data/{ns}/tags/worldgen/biome/{name}.json'
        if path not in names: missing.append(tid); continue
        d = J(path)
        if d.get('replace') is not False or not set(d['values']) <= curated: bad.append(tid)
        if set(d['values']) & nether: nethers.append(tid)
    check('Derived selector tags are exported, additive (replace false) and use only roster IDs', len(tag_ids) > 30 and not bad and not missing, {'tags': len(tag_ids), 'bad': bad, 'missing': missing})
    check('No Nether donor leaked into any derived Overworld selector', not nethers, nethers)

    import gzip
    snap = json.loads(gzip.decompress((R / 'evidence/jar-resource-index-test6.json.gz').read_bytes()))
    struct_ids = [k for k in derived if k in comp['structures']]
    bad_s = []
    for sid in struct_ids:
        native = snap['resources']['worldgen/structure'][sid][-1]['data']
        mine = comp['structures'][sid]
        if {k: v for k, v in mine.items() if k != 'biomes'} != {k: v for k, v in native.items() if k != 'biomes'}:
            bad_s.append(sid)
        if mine['biomes']['type'] != 'neoforge:or' or mine['biomes']['values'][0] != native['biomes']: bad_s.append(sid)
    check('Structure-level selector overrides keep every non-biome field and the native selector', len(struct_ids) == 4 and not bad_s, struct_ids)

    own = [n for n in names if n.startswith(SD) and re.search(r'/(additionalstructures|create_structures_arise|create_easy_structures|explorify|structory_towers|archaion|yungsbridges|yungsextras)/', n)]
    check('Addon structure sets keep their shipped placement (no AO placement override)', not own, own)

    dis = J(SD + 'integrated_api/tags/worldgen/structure/disabled_structures.json')
    vals = {v if isinstance(v, str) else v.get('id') for v in dis['values']}
    check('Integrated API disabled list still holds Small Blimp and Coliseum', {'dungeons_arise:small_blimp', 'dungeons_arise:coliseum'} <= vals, sorted(vals))
    check('Black Spiral is NOT disabled (user decision 9 Oct 2026; runtime Nether check pending)', 'explorify:black_spiral' not in vals, 'enabled by decision')

    reg = list(csv.DictReader((ROOT / 'STRUCTURE_REGISTRY_CATALOG.csv').open()))
    sel = {'additionalstructures': 100, 'create_structures_arise': 24, 'create_easy_structures': 16, 'explorify': 15, 'structory_towers': 13, 'archaion': 1}
    got = {n: sum(1 for r in reg if r['structure_id'].split(':')[0] == n and int(r['curated_ow_test5_count']) > 0) for n in sel}
    check('Curated-biome eligibility floors per addon (regression guard)', all(got[n] >= f for n, f in sel.items()), got)
    return {'status': 'PASS (Test 6 scoped static gates; runtime pending)' if all(c['passed'] for c in checks)
            else 'FAIL', 'gameplay_tested': False, 'check_count': len(checks), 'checks': checks}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', required=True)
    ap.add_argument('--report')
    a = ap.parse_args()
    r = run(a.archive)
    if a.report:
        open(a.report, 'w').write(json.dumps(r, indent=2) + '\n')
    for c in r['checks']:
        if not c['passed']:
            print('FAIL:', c['check'], c['detail'])
    print(r['status'], r['check_count'], 'checks')
    sys.exit(0 if r['status'].startswith('PASS') else 1)
