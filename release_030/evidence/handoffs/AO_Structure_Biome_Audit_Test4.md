# Ambient Odyssey — structure spawning eligibility audit

**Source:** actual `Ambient-Odyssey-v0.3.1-structure-test4.zip` overrides, not the installed mod JARs.

## Key limitation

The CurseForge export has **no mod JARs**. It contains Cristel Lib spacing/toggle configuration and custom datapacks, but not the mods’ built-in `data/<namespace>/worldgen/structure/*.json` and biome tags. Thus **strictly vanilla-only spawning cannot be certified or ruled out for each mod from this ZIP alone**. `structure_placement_config` contains spacing/separation, not biome eligibility.

## Quantitative findings

- Cristel Lib structure namespaces: **62**.
- Custom biome-tag files: **87**.
- Distinct modded biome IDs referenced in these tags: **41**.
- Custom structure-set definitions: **4**.
- Mod-owned biome tag namespaces explicitly patched: **block_factorys_bosses, bosses_of_mass_destruction, dungeons_arise, iceandfire**.

## Mod-by-mod first-pass audit

| Structure namespace | Spacing config | Native biome selector in export | Explicit AO namespace biome patch | Follow-up |
|---|---|---|---|---|
| `adventuredungeons` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `block_factorys_bosses` | Yes | **Not included** | Yes | **High — inspect mod JAR** |
| `bosses_of_mass_destruction` | Yes | **Not included** | Yes | **High — inspect mod JAR** |
| `cataclysm` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `dungeoncrawl` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `dungeons_arise` | Yes | **Not included** | Yes | **High — inspect mod JAR** |
| `dungeons_arise_seven_seas` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `floating_islands` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `formationsoverworld` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `iceandfire` | Yes | **Not included** | Yes | **High — inspect mod JAR** |
| `idas` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `integrated_cataclysm` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `integrated_stronghold` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `integrated_villages` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `irons_spellbooks` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mes` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mns` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mowziesmobs` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mr_dungeons_andtaverns` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mr_lukis_grandcapitals` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mss` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `mvs` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `philipsruins` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `repurposed_structures` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `sky_whale_ship` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `skyvillages` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `structory` | Yes | **Not included** | No | **High — inspect mod JAR** |
| `aether` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `aether_villages` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `alexscaves` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `apotheosis` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `archaeology_ruins` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `ars_nouveau` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `betterend` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `betterfortresses` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `biomeswevegone` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `create_rustic_structures` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `deep_aether` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `deeperdarker` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `dimdoors` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `echoes_of_the_end__structures_` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `end_villager_outpost` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `enigmaticlegacyplus` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `eternal_starlight` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `explore_ruins_aether` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `farmers_structures` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `fdbosses` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `friendsandfoes` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `graveyard` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `illagerwarship` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `incendium` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `netherman` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `pasterdream` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `skyarena` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `supplementaries` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `terralith` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `the_bumblezone` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `tombstone` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `totw_modded` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `twilightforest` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `undergarden` | Yes | **Not included** | No | Inspect JAR if overworld structures |
| `underwater_village` | Yes | **Not included** | No | Inspect JAR if overworld structures |

## AO biome tag coverage (number of modded biome IDs in each AO tag)

| Tag | Count |
|---|---:|
| `beach` | 1 |
| `climate_cold` | 10 |
| `climate_hot` | 7 |
| `extreme_hills` | 10 |
| `flower_forests` | 4 |
| `forest` | 16 |
| `in_overworld` | 41 |
| `is_beach` | 1 |
| `is_birch_forest` | 4 |
| `is_cherry` | 2 |
| `is_cold` | 10 |
| `is_cold/overworld` | 10 |
| `is_coniferous` | 10 |
| `is_dark_forest` | 3 |
| `is_dense_vegetation/overworld` | 23 |
| `is_dry/overworld` | 14 |
| `is_floral` | 4 |
| `is_flower_forest` | 4 |
| `is_forest` | 16 |
| `is_hill` | 10 |
| `is_hills` | 10 |
| `is_hot` | 7 |
| `is_hot/overworld` | 7 |
| `is_icy` | 4 |
| `is_jungle` | 3 |
| `is_lush` | 4 |
| `is_mountain` | 10 |
| `is_ocean` | 3 |
| `is_overworld` | 41 |
| `is_peak` | 10 |
| `is_plains` | 10 |
| `is_river` | 1 |
| `is_snowy` | 10 |
| `is_sparse_vegetation/overworld` | 16 |
| `is_swamp` | 4 |
| `is_taiga` | 10 |
| `is_tree/coniferous` | 10 |
| `is_wet/overworld` | 9 |
| `mountain` | 10 |
| `mountain_peak` | 10 |
| `mountain_slope` | 10 |
| `ocean` | 3 |
| `river` | 1 |
| `shallow_ocean` | 3 |
| `swamp` | 4 |
| `taiga` | 10 |

## High-priority structural problems and cautions

1. **Only a few structure mods receive their own namespace-specific biome-tag patches.** Generic `c`, `forge`, and `minecraft` tags help only when the original mod structure definitions reference those exact tags. This is a coverage gap, **not proof** that each unpatched mod is vanilla-only.
2. **Sky Villages and Sky Whale Ship have no mod-specific AO biome tags.** Their water preference must be verified against built-in structure biome definitions before changing frequency.
3. **WDA Heavenly ships:** The Test 4 custom set lists three structure IDs, but the exported pack does not include the original structure registries, so IDs and eligibility cannot yet be validated against the installed WDA JAR.
4. **IDAS houses:** `mason_house` and many other houses are enabled in `idas_common`, but this is not a biome selector. A per-house frequency boost requires verifying its registered structure ID and applicable biome selector, not only increasing the common set.
5. **Dungeon Crawl:** Test 4 spacing is changed, but eligibility remains unverified.
6. **Placement search benchmarks** are not a reliable measurement of biome eligibility or ordinary chunk-generation throughput.

## Required second-pass evidence

Provide a copy of the *installed* `mods` folder (or a ZIP containing only the structure-mod JARs) for v0.3.1, or a generated Minecraft registry/datapack dump. Inspect each JAR’s `data/*/worldgen/structure/*.json`, `data/*/tags/worldgen/biome/**/*.json`, and `data/*/worldgen/structure_set/*.json`, then cross-reference each biome selector with the curated biome roster. **No new gameplay test needed before this static audit.**

## Structure set files present in Test 4

- `overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/extra_idas_landmarks.json`
- `overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/extra_integrated_land_villages.json`
- `overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/extra_wda_land_and_sky.json`
- `overrides/config/paxi/datapacks/ao_structure_density/data/ambient_odyssey/worldgen/structure_set/extra_wda_heavenly_ships.json`
