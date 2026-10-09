#!/usr/bin/env python3
"""Derive curated-donor additions for the Test 6 addon biome tags (offline, deterministic).

For every provider biome tag shipped by the Test 6 addon JARs, find literal vanilla biome
leaves (and #minecraft:is_savanna) and add the curated donors that stand in for that vanilla
biome in this pack. Replacement donors come from Biolith placement (CURRENT_BIOLITH_PLACEMENT)
where a vanilla target is replaced; the remaining vanilla leaves use the same climate/landform
classes as compile_compatibility_031.py. Desert, badlands, End, Nether and mushroom leaves get
NO donors (the curated roster has no analogue; zero eligibility there is intentional).

Usage: python3 derive_test6_selectors.py [--write]   (default: preview only)
"""
import argparse, gzip, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = ROOT / 'release_030'
EV = R / 'evidence'

# Climate/landform classes (kept identical to compile_compatibility_031.py groups)
CLASS = {
    'plains': ['regions_unexplored:flower_fields', 'regions_unexplored:grassland', 'regions_unexplored:orchard',
               'regions_unexplored:rocky_meadow', 'biomeswevegone:prairie', 'biomeswevegone:sakura_grove',
               'biomesoplenty:highland', 'biomesoplenty:pumpkin_patch', 'natures_spirit:alpine_clearings',
               'natures_spirit:floral_ridges'],
    'taiga': ['regions_unexplored:ashen_woodland', 'regions_unexplored:cold_deciduous_forest',
              'regions_unexplored:frozen_pine_taiga', 'regions_unexplored:redwoods',
              'biomeswevegone:frosted_coniferous_forest', 'biomeswevegone:maple_taiga',
              'biomeswevegone:redwood_thicket', 'biomesoplenty:auroral_garden', 'biomesoplenty:ominous_woods',
              'natures_spirit:windswept_sugi_forest'],
    'snowy': ['regions_unexplored:cold_deciduous_forest', 'regions_unexplored:frozen_pine_taiga',
              'regions_unexplored:icy_heights', 'regions_unexplored:spires',
              'biomeswevegone:frosted_coniferous_forest', 'biomeswevegone:shattered_glacier',
              'biomesoplenty:auroral_garden', 'biomesoplenty:snowblossom_grove'],
    'mountain': ['regions_unexplored:icy_heights', 'regions_unexplored:rocky_meadow', 'regions_unexplored:spires',
                 'biomeswevegone:crag_gardens', 'biomeswevegone:shattered_glacier', 'biomesoplenty:highland',
                 'biomesoplenty:volcano', 'natures_spirit:alpine_clearings', 'natures_spirit:floral_ridges',
                 'natures_spirit:windswept_sugi_forest'],
    'swamp': ['regions_unexplored:fen', 'regions_unexplored:marsh', 'biomeswevegone:bayou', 'biomesoplenty:hot_springs'],
    'beach': ['regions_unexplored:grassy_beach'],
    'river': ['regions_unexplored:muddy_river', 'streamsreflowing:stream'],
    'ocean': ['regions_unexplored:hyacinth_deeps', 'regions_unexplored:rocky_reef', 'biomeswevegone:lush_stacks'],
    'cherry': ['biomeswevegone:sakura_grove', 'biomesoplenty:snowblossom_grove'],
    'dark_forest': ['biomeswevegone:ebony_woods', 'biomeswevegone:weeping_witch_forest', 'biomesoplenty:ominous_woods'],
}
CLASS['hill'] = CLASS['mountain'] + ['regions_unexplored:rocky_meadow', 'biomesoplenty:highland',
                                      'natures_spirit:alpine_clearings']
LEAF_CLASS = {
    'meadow': 'plains', 'cherry_grove': 'cherry', 'dark_forest': 'dark_forest',
    'taiga': 'taiga', 'old_growth_pine_taiga': 'taiga', 'old_growth_spruce_taiga': 'taiga',
    'snowy_taiga': 'snowy', 'snowy_plains': 'snowy', 'ice_spikes': 'snowy', 'snowy_slopes': 'snowy',
    'snowy_beach': 'snowy', 'grove': 'snowy', 'frozen_peaks': 'mountain', 'jagged_peaks': 'mountain',
    'stony_peaks': 'mountain', 'windswept_hills': 'hill', 'windswept_forest': 'hill',
    'windswept_gravelly_hills': 'hill', 'swamp': 'swamp', 'mangrove_swamp': 'swamp', 'river': 'river',
    'frozen_river': 'river', 'beach': 'beach', 'stony_shore': 'beach', 'ocean': 'ocean',
    'deep_ocean': 'ocean', 'cold_ocean': 'ocean', 'lukewarm_ocean': 'ocean', 'warm_ocean': 'ocean',
}
# Vanilla tags used inside provider tags that the common compat layer does not fill
SAVANNA = ['biomeswevegone:prairie', 'regions_unexplored:grassland', 'natures_spirit:floral_ridges']
TAG_CLASS_DONORS = {'minecraft:is_savanna': SAVANNA,
                    'minecraft:has_structure/village_savanna': SAVANNA,
                    'minecraft:has_structure/village_taiga': CLASS['taiga'],
                    'minecraft:has_structure/village_snowy': CLASS['snowy']}
NONE_OK = {'desert', 'badlands', 'eroded_badlands', 'wooded_badlands', 'mushroom_fields', 'the_end',
           'end_highlands', 'end_midlands', 'end_barrens', 'small_end_islands', 'nether_wastes',
           'crimson_forest', 'warped_forest', 'soul_sand_valley', 'basalt_deltas', 'deep_dark',
           'dripstone_caves', 'lush_caves'}


def biolith_donors():
    d = json.loads((ROOT / 'docs/audits/CURRENT_BIOLITH_PLACEMENT.json').read_text())
    out = {}
    for r in d['replacements']:
        out.setdefault(r['target'].split(':', 1)[1], []).append(r['biome'])
    return out


def derive():
    # village_plains = plains/meadow: Biolith plains donors plus the plains class
    TAG_CLASS_DONORS['minecraft:has_structure/village_plains'] = sorted(set(CLASS['plains'] + biolith_donors()['plains']))
    idx = EV / 'jar-resource-index-test6.json.gz'
    snap = json.loads(gzip.decompress(idx.read_bytes()))
    new_jars = {r['file'] for r in json.loads((EV / 'test6-addon-jars.json').read_text())}
    roster = json.loads((R / 'biome-roster.json').read_text())
    curated = {f'{ns}:{n}' for ns, names in roster.items() for n in names} | {'streamsreflowing:stream'}
    bio = biolith_donors()
    result, provenance, unmapped = {}, {}, {}
    for tag, rows in sorted(snap['resources']['tags/worldgen/biome'].items()):
        ns = tag.split(':', 1)[0]
        if ns in ('minecraft', 'c', 'forge', 'neoforge'):
            continue                                   # common layer handles these
        mine = [r for r in rows if r['jar'] in new_jars]
        if not mine:
            continue
        existing, donors, notes = set(), [], []
        for row in mine:
            for v in row['data'].get('values', []):
                v = v['id'] if isinstance(v, dict) else v
                if v.startswith('#'):
                    if v.lstrip('#') in TAG_CLASS_DONORS:
                        donors += TAG_CLASS_DONORS[v.lstrip('#')]; notes.append(v)
                    continue
                existing.add(v)
                leaf = v.split(':', 1)[1] if ':' in v else v
                if v.startswith(('minecraft:',)) or ':' not in v:
                    if leaf in bio:
                        donors += bio[leaf]; notes.append(v)
                    elif leaf in LEAF_CLASS:
                        donors += CLASS[LEAF_CLASS[leaf]]; notes.append(v)
                    elif leaf not in NONE_OK and leaf not in ('plains', 'forest'):
                        unmapped.setdefault(tag, set()).add(leaf)
        donors = sorted({d for d in donors if d in curated and d not in existing})
        if donors:
            result[tag] = {'replace': False, 'values': donors}
            provenance[tag] = {'reason': 'Test 6: curated analogues for vanilla biome leaves: ' + ', '.join(sorted(set(notes))),
                               'source_paths': [{'jar': mine[0]['jar'], 'path': mine[0]['path']}]}
    # Bridges: rivers also include the Streams Reflowing channel biome (common tags only add RU Muddy River)
    t = 'yungsbridges:has_structure/bridge'
    result[t] = {'replace': False, 'values': ['streamsreflowing:stream']}
    provenance[t] = {'reason': 'Test 6: YUNG\'s Bridges span rivers; Streams Reflowing channels use their own biome ID',
                     'source_paths': [{'jar': 'YungsBridges-1.21.1-NeoForge-5.1.1.jar',
                                       'path': 'data/yungsbridges/tags/worldgen/biome/has_structure/bridge.json'}]}
    return result, provenance, {k: sorted(v) for k, v in unmapped.items()}


def structure_overrides():
    """Structures whose `biomes` is a literal list/id or a vanilla structure tag, not a provider tag."""
    snap = json.loads(gzip.decompress((EV / 'jar-resource-index-test6.json.gz').read_bytes()))
    bio = biolith_donors()
    plan = {
        'create_easy_structures:foresttracks': sorted(set(bio['forest'] + bio['flower_forest'])),
        'create_structures_arise:createdesertwell': sorted(set(CLASS['plains'] + bio['plains'])),
        'create_structures_arise:createwitchhut': sorted(CLASS['swamp']),
    }
    for sid, rows in snap['resources']['worldgen/structure'].items():   # vanilla pillager-outpost tag users
        if rows[-1]['data'].get('biomes') == '#minecraft:has_structure/pillager_outpost' and sid.split(':')[0] == 'structory_towers':
            plan[sid] = sorted(set(CLASS['plains'] + CLASS['taiga'] + CLASS['snowy'] + SAVANNA + CLASS['mountain']))
    out, prov = {}, {}
    for sid, donors in sorted(plan.items()):
        row = snap['resources']['worldgen/structure'][sid][-1]
        data = json.loads(json.dumps(row['data']))
        data['biomes'] = {'type': 'neoforge:or', 'values': [data['biomes'], donors]}
        out[sid] = data
        prov[sid] = {'reason': 'Test 6: literal/vanilla-tag selector extended with curated donors (all other fields unchanged)',
                     'source_paths': [{'jar': row['jar'], 'path': row['path']}]}
    return out, prov


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    res, prov, unm = derive()
    print(len(res), 'tags would receive donors;', sum(len(v['values']) for v in res.values()), 'additions')
    for t, v in res.items():
        print(' ', t.ljust(58), len(v['values']))
    if unm:
        print('Unmapped vanilla leaves (left without donors):', json.dumps(unm))
    if a.write:
        p = R / 'structure-compatibility.json'
        c = json.loads(p.read_text())
        for k in [k for k, v in c['provenance'].items() if isinstance(v, dict) and str(v.get('reason', '')).startswith('Test 6: ')]:
            c['biome_tags'].pop(k, None); c['structures'].pop(k, None); c['provenance'].pop(k, None)
        for t in res:
            if t in c['biome_tags']:
                raise SystemExit('refusing to overwrite a non-Test-6 patch for ' + t)
        sres, sprov = structure_overrides()
        c['biome_tags'].update(res); c['structures'].update(sres); c['provenance'].update(prov); c['provenance'].update(sprov)
        print(len(sres), 'structure overrides:', ', '.join(sres))
        p.write_text(json.dumps(c, indent=2) + '\n')
        print('written to', p)
