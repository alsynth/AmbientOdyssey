# Ambient Odyssey 0.3.1-structure-test1 — placement changes

This is the first frequency test. Biome/terrain eligibility and overlap rules still decide which candidates succeed. Ratios below describe generation attempts, not measured building counts.

## Included changes

- Integrated Patches 1.2.0, Integrated Mowzie's Mobs 1.3.2, Integrated Bosses of Mass Destruction 1.0.0, and required Amendments 2.1.10.
- Companions! and Modern Companions removed, including their imported configs.
- Alex's Mobs seal fishing rewards disabled through an empty loot table.
- FTF preset, biome replacement ratios, climate settings, Tan trees, Streams Reflowing and existing overlap settings carried forward.
- Wildlife, missing NPC/piece pools, IDAS obsolete BYG eligibility tags, other spawn problems and overlaps deferred. Traveloptics and Cataclysm Spellbooks defects are also deferred.

## Main targets

| Group | First-pass change |
|---|---|
| Apotheosis towers | 26/18 → 12/6 spacing/separation; candidate density ×4.69 |
| Houses, farms, villages and landmarks | Most selected groups about ×2–3 |
| Moog Voyager selected land buildings/details | ×2.5; selected larger buildings ×3 |
| Moog Soaring floating structures | ×3 |
| Moog Overworld desert/jungle/badlands temples | ×2 |
| Integrated Lich tower | Inherited profile 100/50 → 28/14; addon default 32/16, so ×1.31 relative to the addon default |

## Exact native placement settings

Spacing and separation are in chunks. The old values are from the previous exported profile. Existing salts are retained.

| Config family | Set | Old spacing/separation | New spacing/separation | Candidate density ratio |
|---|---|---|---|---|
| apotheosis | `towers` | 26/18 | 12/6 | ×4.694 |
| vanilla_structures | `villages` | 34/8 | 24/7 | ×2.007 |
| vanilla_structures | `pillager_outposts` | 32/8 | 24/6; frequency 0.2 → 0.3 | ×2.667 |
| vanilla_structures | `igloos` | 32/8 | 24/6 | ×1.778 |
| vanilla_structures | `swamp_huts` | 32/8 | 24/6 | ×1.778 |
| vanilla_structures | `woodland_mansions` | 80/20 | 48/16 | ×2.778 |
| vanilla_structures | `trail_ruins` | 34/8 | 24/6 | ×2.007 |
| towns_and_towers | `other` | 32/16 | 22/10 | ×2.116 |
| towns_and_towers | `towers` | 48/12 | 32/10; frequency 0.2 → 0.3 | ×3.375 |
| towns_and_towers | `towns` | 51/12 | 30/10 | ×2.89 |
| idas | `idas_common` | 21/12 | 15/8 | ×1.96 |
| idas | `idas_small` | 26/20 | 18/12 | ×2.086 |
| dungeons_arise | `minor_structures` | 45/40 | 28/18 | ×2.583 |
| integrated_villages | `air_villages` | 115/90 | 65/45 | ×3.13 |
| mr_lukis_grandcapitals | `villages` | 50/35 | 32/20 | ×2.441 |
| biomeswevegone | `aspen_manors` | 50/35 | 32/20 | ×2.441 |
| biomeswevegone | `bog_trial` | 40/30 | 28/18 | ×2.041 |
| biomeswevegone | `prairie_houses` | 25/20 | 16/10 | ×2.441 |
| biomeswevegone | `villages` | 34/8 | 24/6 | ×2.007 |
| create_rustic_structures | `rustic_barn` | 32/16 | 20/10 | ×2.56 |
| create_rustic_structures | `rustic_smithy` | 24/12 | 16/8 | ×2.25 |
| create_rustic_structures | `rustic_well` | 16/8 | 12/6 | ×1.778 |
| create_rustic_structures | `rustic_windmill` | 24/12 | 16/8 | ×2.25 |
| structory | `mid_rare_ruin` | 30/16 | 21/11 | ×2.041 |
| structory | `old_manor` | 42/16 | 29/11 | ×2.098 |
| structory | `outcast_villager` | 44/14 | 31/10 | ×2.015 |
| structory | `ruin` | 30/10 | 21/7 | ×2.041 |
| structory | `ruin_quiet` | 23/10 | 16/7 | ×2.066 |
| formationsoverworld | `rare` | 50/40 | 30/22 | ×2.778 |
| formationsoverworld | `uncommon` | 15/8 | 12/6 | ×1.562 |
| archaeology_ruins | `adoberuins` | 30/20 | 21/14 | ×2.041 |
| archaeology_ruins | `mudblacksmithruin` | 35/30 | 24/21 | ×2.127 |
| archaeology_ruins | `mudpotterruin` | 35/25 | 24/18 | ×2.127 |
| archaeology_ruins | `mudschoolruin` | 40/30 | 28/21 | ×2.041 |
| archaeology_ruins | `ruined_desert_pyramid` | 35/25 | 24/18 | ×2.127 |
| archaeology_ruins | `ruinedjungletemple` | 25/20 | 18/14 | ×1.929 |
| archaeology_ruins | `smallmudruin` | 20/14 | 14/10 | ×2.041 |
| adventuredungeons | `ruins_desert` | 30/10 | 20/7 | ×2.25 |
| adventuredungeons | `ruins_snow` | 30/10 | 20/7 | ×2.25 |
| adventuredungeons | `ruins_standard` | 30/10 | 20/7 | ×2.25 |
| farmers_structures | `cacaos_with_all` | 65/31 | 46/22 | ×1.997 |
| farmers_structures | `cooks_moss_with_all` | 16/14 | 11/10 | ×2.116 |
| farmers_structures | `cooks_with_all` | 40/32 | 28/22 | ×2.041 |
| farmers_structures | `honey_cake_farms_with_all` | 64/29 | 45/20 | ×2.023 |
| farmers_structures | `ratatouilles_with_all` | 44/29 | 31/20 | ×2.015 |
| farmers_structures | `shepherd_farms_with_all` | 141/121 | 99/85 | ×2.028 |
| irons_spellbooks | `evoker_fort` | 85/50 | 50/28 | ×2.89 |
| irons_spellbooks | `mangrove_hut` | 25/18 | 18/11 | ×1.929 |
| irons_spellbooks | `mountain_tower` | 45/33 | 28/18 | ×2.583 |
| ars_nouveau | `wilden_den_set` | 36/10 | 24/7 | ×2.25 |
| enigmaticlegacyplus | `spellstone_hut` | 32/11 | 22/8 | ×2.116 |
| friendsandfoes | `iceologer_cabin` | 40/10 | 28/7 | ×2.041 |
| friendsandfoes | `illusioner_shack` | 40/10 | 28/7 | ×2.041 |
| friendsandfoes | `illusioner_training_grounds` | 40/10 | 28/7 | ×2.041 |
| graveyard | `altar_structure` | 30/24 | 22/18 | ×1.86 |
| graveyard | `haunted_house_structure` | 20/18 | 15/14 | ×1.778 |
| graveyard | `large_graveyard_structure` | 25/20 | 19/15 | ×1.731 |
| graveyard | `lich_prison_structure` | 120/100 | 90/75 | ×1.778 |
| graveyard | `medium_graveyard_structure` | 18/16 | 14/12 | ×1.653 |
| graveyard | `ruins_structure` | 16/12 | 12/9 | ×1.778 |
| graveyard | `small_desert_graveyard_structure` | 32/28 | 24/21 | ×1.778 |
| graveyard | `small_graveyard_structure` | 20/18 | 15/14 | ×1.778 |
| iceandfire | `cyclops_cave` | 16/6 | 14/5 | ×1.306 |
| iceandfire | `dragon_roost` | 15/6 | 13/5 | ×1.331 |
| iceandfire | `gorgon_temple` | 32/12 | 27/10 | ×1.405 |
| iceandfire | `graveyard` | 28/14 | 24/12 | ×1.361 |
| iceandfire | `hydra_cave` | 16/6 | 14/5 | ×1.306 |
| iceandfire | `mausoleum` | 32/12 | 27/10 | ×1.405 |
| mowziesmobs | `frostmaw_spawns` | 25/8 | 18/6 | ×1.929 |
| mowziesmobs | `monasteries` | 25/8 | 18/6 | ×1.929 |
| mowziesmobs | `umvuthana_groves` | 25/8 | 18/6 | ×1.929 |
| bosses_of_mass_destruction | `lich_tower` | 100/50 | 28/14 | ×12.755 |
| cataclysm | `abandoned_structures` | 30/20 | 22/14 | ×1.86 |
| cataclysm | `acropolis` | 80/50 | 50/30 | ×2.56 |
| cataclysm | `cursed_pyramid` | 80/50 | 50/30 | ×2.56 |
| cataclysm | `desert_structures` | 30/20 | 22/14 | ×1.86 |
| cataclysm | `frosted_prison` | 80/50 | 50/30 | ×2.56 |
| integrated_cataclysm | `cursed_pyramid` | 80/50 | 50/30 | ×2.56 |
| integrated_cataclysm | `frosted_prison` | 80/50 | 50/30 | ×2.56 |
| integrated_cataclysm | `small_integrated_cataclysm` | 50/30 | 32/18 | ×2.441 |
| block_factorys_bosses | `dragon_tower` | 96/24 | 60/16 | ×2.56 |
| block_factorys_bosses | `sandworm_nest` | 45/30 | 32/20 | ×1.978 |
| block_factorys_bosses | `yeti_hideout` | 30/25 | 22/16 | ×1.86 |
| fdbosses | `chesed_arena` | 100/50 | 65/32 | ×2.367 |
| repurposed_structures | `fortresses_overworld` | 50/25 | 32/16 | ×2.441 |
| repurposed_structures | `igloos_overworld` | 36/18 | 23/12 | ×2.45 |
| repurposed_structures | `mansions_mangrove` | 120/50 | 78/32 | ×2.367 |
| repurposed_structures | `mansions_overworld` | 225/110 | 146/72 | ×2.375 |
| repurposed_structures | `outposts_overworld` | 49/24 | 32/16 | ×2.345 |
| repurposed_structures | `pyramids_mushroom` | 35/15 | 23/10 | ×2.316 |
| repurposed_structures | `pyramids_overworld` | 52/29 | 34/19 | ×2.339 |
| repurposed_structures | `temples_overworld` | 51/29 | 33/19 | ×2.388 |
| repurposed_structures | `villages_mushroom` | 35/15 | 23/10 | ×2.316 |
| repurposed_structures | `villages_overworld` | 50/25 | 32/16 | ×2.441 |
| repurposed_structures | `witch_huts_overworld` | 53/26 | 34/17 | ×2.43 |
| mr_dungeons_andtaverns | `desert_ruins` | 80/12 | 52/8 | ×2.367 |
| mr_dungeons_andtaverns | `firewatch_towers` | 50/15 | 32/10 | ×2.441 |
| mr_dungeons_andtaverns | `illager_camp` | 50/32 | 32/21 | ×2.441 |
| mr_dungeons_andtaverns | `illager_hideout` | 200/12 | 130/8 | ×2.367 |
| mr_dungeons_andtaverns | `jungle_ruins` | 80/12 | 52/8 | ×2.367 |
| mr_dungeons_andtaverns | `mangrove_witch_hut` | 32/8 | 21/5 | ×2.322 |
| mr_dungeons_andtaverns | `minecraft:woodland_mansions` | 80/20 | 52/13 | ×2.367 |
| mr_dungeons_andtaverns | `remnants` | 120/30 | 78/20 | ×2.367 |
| mr_dungeons_andtaverns | `ruin_town` | 72/30 | 47/20 | ×2.347 |
| mr_dungeons_andtaverns | `shrine_tower` | 600/312 | 390/203 | ×2.367 |
| mr_dungeons_andtaverns | `shrines` | 50/26 | 32/17 | ×2.441 |
| mr_dungeons_andtaverns | `stray_fort` | 100/16 | 65/10 | ×2.367 |
| mr_dungeons_andtaverns | `swamp_structure` | 80/20 | 52/13 | ×2.367 |
| mr_dungeons_andtaverns | `taverns` | 40/15 | 26/10 | ×2.367 |
| mr_dungeons_andtaverns | `villages_birch` | 34/8 | 22/5 | ×2.388 |
| mr_dungeons_andtaverns | `villages_jungle` | 34/8 | 22/5 | ×2.388 |
| mr_dungeons_andtaverns | `villages_swamp` | 34/8 | 22/5 | ×2.388 |
| mr_dungeons_andtaverns | `wells` | 40/15 | 26/10 | ×2.367 |
| mr_dungeons_andtaverns | `wild_ruin` | 27/18 | 18/12 | ×2.25 |
| philipsruins | `ancient_ruins` | 60/30 | 39/20 | ×2.367 |
| philipsruins | `ancient_towers` | 50/40 | 32/26 | ×2.441 |
| philipsruins | `field_stone_ruins` | 75/35 | 49/23 | ×2.343 |
| philipsruins | `field_stone_ruins_rocks` | 40/27 | 26/18 | ×2.367 |
| philipsruins | `level_one_ruins` | 75/40 | 49/26 | ×2.343 |
| philipsruins | `level_two_ruins` | 80/50 | 52/32 | ×2.367 |
| philipsruins | `level_three_ruins` | 85/45 | 55/29 | ×2.388 |
| philipsruins | `pumpkin_ruins` | 50/40 | 32/26 | ×2.441 |
| philipsruins | `rare_ruin` | 360/130 | 234/84 | ×2.367 |
| eternal_starlight | `portal_ruins_cold` | 36/30 | 25/21 | ×2.074 |
| eternal_starlight | `portal_ruins_common` | 36/30 | 25/21 | ×2.074 |
| eternal_starlight | `portal_ruins_desert` | 36/30 | 25/21 | ×2.074 |
| eternal_starlight | `portal_ruins_forest` | 36/30 | 25/21 | ×2.074 |
| eternal_starlight | `portal_ruins_jungle` | 36/30 | 25/21 | ×2.074 |
| floating_islands | `dungeon_islands` | 90/70 | 55/35 | ×2.678 |
| floating_islands | `peaceful_islands` | 60/40 | 38/24 | ×2.493 |
| floating_islands | `villager_islands` | 100/90 | 60/42 | ×2.778 |
| skyvillages | `skyvillage` | 70/65 | 44/32 | ×2.531 |
| sky_whale_ship | `frozen_whale` | 220/40 | 132/24 | ×2.778 |
| sky_whale_ship | `whale` | 190/35 | 114/21 | ×2.778 |
| sky_whale_ship | `whalearena` | 183/35 | 110/21 | ×2.768 |
| sky_whale_ship | `whalelight` | 171/35 | 103/21 | ×2.756 |
| sky_whale_ship | `whaleship` | 178/35 | 107/21 | ×2.767 |
| skyarena | `ice_arena` | 75/50 | 49/32 | ×2.343 |
| skyarena | `sky_arena` | 75/50 | 49/32 | ×2.343 |
| totw_modded | `overworld` | 45/25 | 26/14 | ×2.996 |

## Scoped Moog multipliers

These refer to structure-set IDs. The MSL universal multiplier remains 1 and no whole-mod multiplier is added. This avoids increasing Nether, underwater or ordinary ground tree sets by accident. MSL scales spacing/separation by 1/sqrt(frequency). Native Cristel Moog spacing configs are not also reduced.

| Structure set | Frequency multiplier |
|---|---|
| `mss:arena` | ×3.0 |
| `mss:birch_river` | ×3.0 |
| `mss:calcite_house` | ×3.0 |
| `mss:castle_ruin` | ×3.0 |
| `mss:castle_tower` | ×3.0 |
| `mss:cherry_river` | ×3.0 |
| `mss:desert_pyramid` | ×3.0 |
| `mss:desert_well` | ×3.0 |
| `mss:diorite_house` | ×3.0 |
| `mss:frozen_pond` | ×3.0 |
| `mss:jungle` | ×3.0 |
| `mss:large_tower` | ×3.0 |
| `mss:leaf_hollow` | ×3.0 |
| `mss:mangrove` | ×3.0 |
| `mss:muddy_water_hole` | ×3.0 |
| `mss:mushroom` | ×3.0 |
| `mss:nether_portal` | ×3.0 |
| `mss:palm_island` | ×3.0 |
| `mss:red_sand` | ×3.0 |
| `mss:small_deepslate_house` | ×3.0 |
| `mss:small_oak_house` | ×3.0 |
| `mss:small_pond` | ×3.0 |
| `mss:small_tower` | ×3.0 |
| `mss:spruce_huts` | ×3.0 |
| `mss:taiga` | ×3.0 |
| `mss:trees` | ×3.0 |
| `mss:volcano` | ×3.0 |
| `mss:white_house` | ×3.0 |
| `mtr:badlands_temple` | ×2.0 |
| `mtr:desert_temple` | ×2.0 |
| `mtr:jungle_temple` | ×2.0 |
| `mvs:azelea_house` | ×3.0 |
| `mvs:barn` | ×3.0 |
| `mvs:beach_bar` | ×2.5 |
| `mvs:bee_dome` | ×2.5 |
| `mvs:bench` | ×2.5 |
| `mvs:campsite` | ×2.5 |
| `mvs:cart` | ×2.5 |
| `mvs:cartographer_tower` | ×3.0 |
| `mvs:castle_ruins` | ×3.0 |
| `mvs:cathedral` | ×3.0 |
| `mvs:deepslate_house` | ×2.5 |
| `mvs:desert_house` | ×2.5 |
| `mvs:desert_pump` | ×2.5 |
| `mvs:diorite_and_deepslate_house` | ×2.5 |
| `mvs:diorite_tower` | ×3.0 |
| `mvs:fire_camp` | ×2.5 |
| `mvs:floating_islands` | ×2.5 |
| `mvs:fox_hut` | ×2.5 |
| `mvs:gallows` | ×2.5 |
| `mvs:haystack` | ×2.5 |
| `mvs:horse_campsite` | ×2.5 |
| `mvs:horse_pen` | ×2.5 |
| `mvs:house` | ×3.0 |
| `mvs:jungle_tower` | ×3.0 |
| `mvs:lamp_chest` | ×2.5 |
| `mvs:large_cart_1` | ×2.5 |
| `mvs:large_cart_2` | ×2.5 |
| `mvs:large_floating_island` | ×2.5 |
| `mvs:lecturn_garden` | ×2.5 |
| `mvs:lil_house` | ×2.5 |
| `mvs:log_ruin` | ×2.5 |
| `mvs:medium_bamboo_cart` | ×2.5 |
| `mvs:medium_igloo_1` | ×2.5 |
| `mvs:medium_igloo_2` | ×2.5 |
| `mvs:medium_oak_lantern` | ×2.5 |
| `mvs:mud_brick_house_1` | ×2.5 |
| `mvs:mushroom_well` | ×2.5 |
| `mvs:other_wells` | ×2.5 |
| `mvs:out_house` | ×2.5 |
| `mvs:paths` | ×2.5 |
| `mvs:pile` | ×2.5 |
| `mvs:railway` | ×2.5 |
| `mvs:rare_well` | ×2.5 |
| `mvs:red_tower` | ×3.0 |
| `mvs:ruined_beacon` | ×2.5 |
| `mvs:shed` | ×2.5 |
| `mvs:small_acacia_lantern` | ×2.5 |
| `mvs:small_bamboo_lantern` | ×2.5 |
| `mvs:small_birch_lantern` | ×2.5 |
| `mvs:small_campfire_lantern` | ×2.5 |
| `mvs:small_cherry_lantern` | ×2.5 |
| `mvs:small_dark_oak_lantern` | ×2.5 |
| `mvs:small_igloo` | ×2.5 |
| `mvs:small_jungle_lantern` | ×2.5 |
| `mvs:small_mangrove_lantern` | ×2.5 |
| `mvs:small_oak_lantern` | ×2.5 |
| `mvs:small_pillager_tower` | ×2.5 |
| `mvs:small_ruin` | ×2.5 |
| `mvs:small_spruce_lantern` | ×2.5 |
| `mvs:small_swamp_house` | ×2.5 |
| `mvs:small_tower_well` | ×2.5 |
| `mvs:snowy_dog_hut` | ×2.5 |
| `mvs:stalls` | ×2.5 |
| `mvs:statue_ruins` | ×2.5 |
| `mvs:stone_fountain` | ×2.5 |
| `mvs:stone_pillars` | ×2.5 |
| `mvs:sunzi_gate` | ×2.5 |
| `mvs:tall_house` | ×3.0 |
| `mvs:villager_statue` | ×2.5 |
| `mvs:wheat_grain_bin` | ×2.5 |
| `mvs:windmill` | ×3.0 |
| `mvs:wooden_wheat_farm` | ×2.5 |

## Additional sets for mixed groups

Original mixed groups remain active. Three additional groups contain selected land/sky structures copied from the exact pinned JARs, preserving their original weights, definitions and biome eligibility. Placement fields are copied; only spacing, separation and a new unique salt change. No biome tags or structure definitions are overridden by this density pack.

### `ambient_odyssey:extra_wda_land_and_sky`

Source: `dungeons_arise:major_structures`, CurseForge file 7150870. Extra grid: 28/18 chunks.

Included: `dungeons_arise:bandit_village`, `dungeons_arise:ceryneian_hind`, `dungeons_arise:coliseum`, `dungeons_arise:illager_campsite`, `dungeons_arise:illager_fort`, `dungeons_arise:illager_windmill`, `dungeons_arise:merchant_campsite`, `dungeons_arise:monastery`, `dungeons_arise:mushroom_house`, `dungeons_arise:mushroom_village`, `dungeons_arise:small_blimp`, `dungeons_arise:greenwood_pub`, `dungeons_arise:bandit_towers`, `dungeons_arise:thornborn_towers`, `dungeons_arise:shiraz_palace`, `dungeons_arise:keep_kayra`, `dungeons_arise:mechanical_nest`.

### `ambient_odyssey:extra_idas_landmarks`

Source: `idas:idas_rare`, CurseForge file 8232359. Extra grid: 32/14 chunks.

Included: `idas:pillager_fortress`, `idas:labyrinth`, `idas:bazaar`, `idas:tinkers_workshop`, `idas:tree_of_wisdom`, `idas:iceandfire/dread_citadel`, `idas:tinkers_citadel`, `idas:ars_nouveau/archmages_tower`, `idas:desert_pyramid`, `idas:collectors_museum`, `idas:windswept_shrine`.

### `ambient_odyssey:extra_integrated_land_villages`

Source: `integrated_villages:regular_villages`, CurseForge file 8161672. Extra grid: 22/14 chunks.

Included: `integrated_villages:tavern_village`, `integrated_villages:mediterranean_village`, `integrated_villages:kutcha_village`, `integrated_villages:oasis_village`, `integrated_villages:mossy_mounds`, `integrated_villages:cabin_village`, `integrated_villages:quark/minka_village`, `integrated_villages:marketstead_village`, `integrated_villages:clockwork_village`, `integrated_villages:sunken_village`.

The WDA extra set excludes boat/ocean structures, mine/underground groups, and variants whose native tags explicitly include End biomes. The IDAS extra set excludes Ancient Mines and Ruins of the Deep. The Integrated Villages extra set excludes the ocean Pirate Village; the swamp Sunken Village is retained. Existing exclusion fields are copied. These added groups still need an in-game overlap/availability check after the density test.

## Providers outside this frequency pass

Ocean/underwater mods, Seven Seas, underground Dungeon Crawl and stronghold/mineshaft systems, and dimension-specific providers retain their earlier placement settings. Mixed-profile content such as NeoPasterDream, Quark features and Remnant Bosses retains its existing settings for the later eligibility/content audit. Ordinary tree/rock decoration frequency is not raised. Adding the Integrated overhauls naturally replaces their original structure definitions, including non-surface content; the frequency edits themselves target the selected surface sets.

## Test

Import the full CurseForge ZIP into a new profile, restart, and create a fresh same-seed world using the existing Ambient Odyssey 0.3.1 FTF preset. Count towers, villages, houses/farms, large landmarks and sky structures along a recorded inland route. Save the new log. The increased candidate density is not a guarantee of an exact nearest-structure distance.

Primary configuration sources:
- https://www.curseforge.com/minecraft/mc-mods/integrated-mowzies-mobs/files/8960804
- https://www.curseforge.com/minecraft/mc-mods/integrated-bosses-of-mass-destruction/files/8895453
- https://www.curseforge.com/minecraft/mc-mods/integrated-patches/files/8995436
- https://www.curseforge.com/minecraft/mc-mods/amendments/files/8825641
- https://github.com/FinnSetchell/MoogsStructureLib/blob/HEAD/src/main/java/com/finndog/moogs_structures/config/MslConfig.java
