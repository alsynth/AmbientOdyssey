#!/usr/bin/env python3
"""Compile the AO biome-eligibility and Curios compatibility datapack."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'release_030'
DATAPACK = RELEASE / 'overrides/config/paxi/datapacks/ao_compatibility'


def unique(values):
    return sorted(dict.fromkeys(values))


def write_tag(namespace, name, values):
    path = DATAPACK / 'data' / namespace / 'tags/worldgen/biome' / (name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'replace': False, 'values': unique(values)}, indent=2) + '\n', newline='\n')
    return path


def write_item_tag(name, values):
    path = DATAPACK / 'data/curios/tags/item' / (name + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'replace': False, 'values': unique(values)}, indent=2) + '\n', newline='\n')
    return path


def compile_compatibility():
    # All files in this compiler-owned pack are recreated, including optional
    # reference repairs. This removes stale generated additions on rebuild.
    if (DATAPACK / 'data').exists():
        shutil.rmtree(DATAPACK / 'data')
    roster = json.loads((RELEASE / 'biome-roster.json').read_text())
    curated = {f'{ns}:{name}' for ns, names in roster.items() for name in names}
    nether = {
        'regions_unexplored:infernal_holt',
        'regions_unexplored:blackstone_basin',
    }
    overworld = curated - nether

    # These are deliberate AO climate/landform classifications.  They fill the
    # common tags used by the installed structure mods without changing any
    # structure spacing or vanilla biome replacement rules.
    forest = [
        'regions_unexplored:ashen_woodland',
        'regions_unexplored:cold_deciduous_forest',
        'regions_unexplored:maple_forest',
        'regions_unexplored:orchard',
        'regions_unexplored:redwoods',
        'biomeswevegone:ebony_woods',
        'biomeswevegone:frosted_coniferous_forest',
        'biomeswevegone:redwood_thicket',
        'biomeswevegone:sakura_grove',
        'biomeswevegone:skyris_vale',
        'biomeswevegone:weeping_witch_forest',
        'biomeswevegone:zelkova_forest',
        'biomesoplenty:auroral_garden',
        'biomesoplenty:ominous_woods',
        'biomesoplenty:snowblossom_grove',
        'natures_spirit:windswept_sugi_forest',
    ]
    taiga = [
        'regions_unexplored:ashen_woodland',
        'regions_unexplored:cold_deciduous_forest',
        'regions_unexplored:frozen_pine_taiga',
        'regions_unexplored:redwoods',
        'biomeswevegone:frosted_coniferous_forest',
        'biomeswevegone:maple_taiga',
        'biomeswevegone:redwood_thicket',
        'biomesoplenty:auroral_garden',
        'biomesoplenty:ominous_woods',
        'natures_spirit:windswept_sugi_forest',
    ]
    jungle = [
        'biomeswevegone:bayou',
        'biomeswevegone:crag_gardens',
        'biomeswevegone:ebony_woods',
        'biomeswevegone:tropical_rainforest',
    ]
    plains = [
        'regions_unexplored:flower_fields',
        'regions_unexplored:grassland',
        'regions_unexplored:orchard',
        'regions_unexplored:rocky_meadow',
        'biomeswevegone:prairie',
        'biomeswevegone:baobab_savanna',
        'biomeswevegone:sakura_grove',
        'biomesoplenty:dryland',
        'biomesoplenty:highland',
        'biomesoplenty:pumpkin_patch',
        'natures_spirit:alpine_clearings',
        'natures_spirit:floral_ridges',
    ]
    mountain = [
        'regions_unexplored:icy_heights',
        'regions_unexplored:rocky_meadow',
        'regions_unexplored:spires',
        'biomeswevegone:crag_gardens',
        'biomeswevegone:shattered_glacier',
        'biomesoplenty:highland',
        'biomesoplenty:volcano',
        'natures_spirit:alpine_clearings',
        'natures_spirit:floral_ridges',
        'natures_spirit:windswept_sugi_forest',
    ]
    hill = mountain + [
        'regions_unexplored:rocky_meadow',
        'biomesoplenty:highland',
        'natures_spirit:alpine_clearings',
    ]
    snowy = [
        'regions_unexplored:cold_deciduous_forest',
        'regions_unexplored:frozen_pine_taiga',
        'regions_unexplored:icy_heights',
        'regions_unexplored:spires',
        'biomeswevegone:frosted_coniferous_forest',
        'biomeswevegone:shattered_glacier',
        'biomesoplenty:auroral_garden',
        'biomesoplenty:snowblossom_grove',
    ]
    swamp = [
        'regions_unexplored:fen',
        'regions_unexplored:marsh',
        'biomeswevegone:bayou',
        'biomesoplenty:hot_springs',
    ]
    ocean = [
        'regions_unexplored:hyacinth_deeps',
        'regions_unexplored:rocky_reef',
        'biomeswevegone:lush_stacks',
    ]
    beach = ['regions_unexplored:grassy_beach']
    river = ['regions_unexplored:muddy_river']
    lush = [
        'regions_unexplored:marsh',
        'biomeswevegone:bayou',
        'biomeswevegone:crag_gardens',
        'biomesoplenty:hot_springs',
    ]
    icy = [
        'regions_unexplored:icy_heights',
        'regions_unexplored:spires',
        'biomeswevegone:shattered_glacier',
        'biomesoplenty:auroral_garden',
    ]
    hot = [
        'regions_unexplored:ashen_woodland',
        'biomeswevegone:crag_gardens',
        'biomeswevegone:ebony_woods',
        'biomeswevegone:prairie',
        'biomeswevegone:baobab_savanna',
        'biomeswevegone:tropical_rainforest',
        'biomesoplenty:dryland',
        'biomesoplenty:volcano',
        'natures_spirit:floral_ridges',
    ]
    cold = [
        'regions_unexplored:cold_deciduous_forest',
        'regions_unexplored:frozen_pine_taiga',
        'regions_unexplored:icy_heights',
        'regions_unexplored:spires',
        'biomeswevegone:frosted_coniferous_forest',
        'biomeswevegone:maple_taiga',
        'biomeswevegone:skyris_vale',
        'biomeswevegone:weeping_witch_forest',
        'biomeswevegone:zelkova_forest',
        'biomeswevegone:shattered_glacier',
        'biomesoplenty:auroral_garden',
        'biomesoplenty:hot_springs',
        'biomesoplenty:snowblossom_grove',
    ]
    floral = [
        'regions_unexplored:flower_fields',
        'biomeswevegone:sakura_grove',
        'biomesoplenty:pumpkin_patch',
        'natures_spirit:floral_ridges',
    ]
    birch = [
        'regions_unexplored:maple_forest',
        'biomeswevegone:sakura_grove',
        'biomeswevegone:zelkova_forest',
        'biomesoplenty:snowblossom_grove',
    ]
    cherry = [
        'biomeswevegone:sakura_grove',
        'biomesoplenty:snowblossom_grove',
    ]
    dark_forest = [
        'biomeswevegone:ebony_woods',
        'biomeswevegone:weeping_witch_forest',
        'biomesoplenty:ominous_woods',
    ]
    dense = unique(forest + taiga + jungle + swamp + lush)
    wet = unique(swamp + ocean + river + lush)
    dry = unique(plains + hot)
    sparse = unique(mountain + plains)
    coniferous = taiga

    all_groups = {
        'is_overworld': overworld,
        'in_overworld': overworld,
        'is_forest': forest,
        'forest': forest,
        'is_taiga': taiga,
        'taiga': taiga,
        'is_coniferous': coniferous,
        'is_jungle': jungle,
        'is_plains': plains,
        'is_mountain': mountain,
        'mountain': mountain,
        'mountain_peak': mountain,
        'mountain_slope': hill,
        'is_peak': mountain,
        'is_hill': hill,
        'is_hills': hill,
        'extreme_hills': hill,
        'is_snowy': snowy,
        'is_swamp': swamp,
        'swamp': swamp,
        'is_ocean': ocean,
        'ocean': ocean,
        'is_beach': beach,
        'beach': beach,
        'is_river': river,
        'river': river,
        'is_lush': lush,
        'is_icy': icy,
        'is_hot': hot,
        'is_cold': cold,
        'is_hot/overworld': hot,
        'is_cold/overworld': cold,
        'climate_hot': hot,
        'climate_cold': cold,
        'is_floral': floral,
        'is_flower_forest': floral,
        'flower_forests': floral,
        'is_birch_forest': birch,
        'is_cherry': cherry,
        'is_dark_forest': dark_forest,
        'shallow_ocean': ocean,
        'is_dense_vegetation/overworld': dense,
        'is_tree/coniferous': coniferous,
        'is_wet/overworld': wet,
        'is_dry/overworld': dry,
        'is_sparse_vegetation/overworld': sparse,
    }

    # Fail early if an editable classification drifts from the active roster.
    for name, values in all_groups.items():
        assert set(values).issubset(curated), (name, sorted(set(values) - curated))

    minecraft_names = {
        'is_overworld', 'is_forest', 'is_taiga', 'is_coniferous', 'is_jungle',
        'is_plains', 'is_mountain', 'is_hill', 'is_hills', 'is_snowy',
        'is_swamp', 'is_ocean', 'is_beach', 'is_river', 'is_lush', 'is_icy',
        'is_floral', 'is_flower_forest', 'is_birch_forest', 'is_cherry',
        'is_dark_forest',
    }
    forge_names = {
        'is_overworld', 'is_forest', 'is_coniferous', 'is_jungle', 'is_plains',
        'is_mountain', 'is_peak', 'is_hill', 'is_hills', 'is_snowy',
        'is_swamp', 'is_ocean', 'is_beach', 'is_icy',
    }
    for name in minecraft_names:
        write_tag('minecraft', name, all_groups[name])
    for name in forge_names:
        write_tag('forge', name, all_groups[name])
    for name, values in all_groups.items():
        write_tag('c', name, values)

    # A few providers use direct vanilla-only lists rather than the common
    # tags above. These additions are intentionally small and climate-specific.
    direct = {
        ('block_factorys_bosses', 'dragon_tower'): unique(plains + forest + hot),
        ('block_factorys_bosses', 'yeti_hideout'): cold,
        ('bosses_of_mass_destruction', 'collections/cold'): cold,
        ('dungeons_arise', 'has_structure/small_prairie_house_biomes'): plains,
        ('dungeons_arise', 'has_structure/giant_mushroom_biomes'): forest + plains,
        ('iceandfire', 'structure_gen/mausoleum'): cold,
    }
    for (namespace, name), values in direct.items():
        write_tag(namespace, name, values)

    # Enigmatic Legacy+ 1.1.2 registers these fork items but omits the
    # Curios assignments. The standard coloured amulets are repeated here so
    # the overlay remains effective even if the fork's nested tag is skipped.
    write_item_tag('amulet', [
        'enigmaticlegacyplus:enigmatic_amulet_red',
        'enigmaticlegacyplus:enigmatic_amulet_aqua',
        'enigmaticlegacyplus:enigmatic_amulet_violet',
        'enigmaticlegacyplus:enigmatic_amulet_magenta',
        'enigmaticlegacyplus:enigmatic_amulet_green',
        'enigmaticlegacyplus:enigmatic_amulet_black',
        'enigmaticlegacyplus:enigmatic_amulet_blue',
        'enigmaticlegacyplus:unwitnessed_amulet',
        'enigmaticlegacyplus:ascension_amulet',
        'enigmaticlegacyplus:redemption_amulet',
        'enigmaticlegacyplus:eldritch_amulet',
        'enigmaticlegacyplus:the_necklace',
    ])
    write_item_tag('scroll', ['enigmaticlegacyplus:darkest_scroll'])

    patch_path = RELEASE / 'structure-compatibility.json'
    if patch_path.exists():
        patches = json.loads(patch_path.read_text())
        for identifier, data in patches.get('biome_tags', {}).items():
            namespace, name = identifier.split(':', 1)
            path = DATAPACK / 'data' / namespace / 'tags/worldgen/biome' / (name + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            # A patch may share a tag with the initial common compatibility
            # layer. Merge additions, but honor explicit replacement repairs.
            if path.exists() and not data.get('replace', False):
                old = json.loads(path.read_text())
                data = dict(data, values=unique(old['values'] + data['values']))
            path.write_text(json.dumps(data, indent=2) + '\n', newline='\n')
        for identifier, data in patches.get('structures', {}).items():
            namespace, name = identifier.split(':', 1)
            path = DATAPACK / 'data' / namespace / 'worldgen/structure' / (name + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2) + '\n', newline='\n')
        for identifier, data in patches.get('item_tags', {}).items():
            namespace, name = identifier.split(':', 1)
            path = DATAPACK / 'data' / namespace / 'tags/item' / (name + '.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2) + '\n', newline='\n')

    DATAPACK.mkdir(parents=True, exist_ok=True)
    (DATAPACK / 'pack.mcmeta').write_text(json.dumps({
        'pack': {
            'pack_format': 48,
            'description': 'Ambient Odyssey: biome eligibility and Curios compatibility',
        }
    }, indent=2) + '\n', newline='\n')
    print(f'Compatibility: {len(all_groups)} common biome tags, '
          f'{len(direct)} direct structure tags, Curios amulet/scroll bridges')
    return all_groups


if __name__ == '__main__':
    compile_compatibility()
