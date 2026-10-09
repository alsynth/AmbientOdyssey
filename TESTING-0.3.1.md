# Ambient Odyssey 0.3.1 worldgen test — historical Test 2 notes

These notes describe Test 2 and earlier biome tuning. For the current export, use `STRUCTURE_TEST5_INSTALL.md`, `STRUCTURE_TEST5_CHANGELOG.md` and `STRUCTURE_TEST5_VALIDATION.md`. Test 5's static build is complete independently of later gameplay acceptance.

Current full export: **0.3.1-structure-test2**. The user verified the earlier 0.3.1 biome replacement run. This revision carries the structure-test1 placement increases and adds biome eligibility compatibility for the active modded biome roster, plus the Enigmatic Legacy+ Curios bridge. It includes the three Integrated addons and Amendments, removes both companion mods, and disables seal fishing rewards. It has not been launched here; static export checks are recorded separately.

## Structure test first

Import `Ambient-Odyssey-v0.3.1-structure-test2.zip` as a new CurseForge profile. The export contains the mod additions and removals, so use this full ZIP rather than the earlier small worldgen update. Existing profiles retain their installed companion JARs until removed manually.

Create a NEW world using the same seed and **Ambient Odyssey 0.3.1** FTF preset as your comparison world. The continent scale, rivers, biome ratios, tree settings and climate settings are carried forward. Check a recorded inland route for Apotheosis towers, villages, houses/farms, large landmarks and sky structures. Note biome IDs and coordinates where areas remain empty. Start with a short route; a full locate survey is not required for this first density check.

Most selected groups now request about two to three times as many placement attempts, and Apotheosis towers request about 4.69 times as many. The new compatibility datapack extends the common selector tags used by those providers to the active curated biomes; direct vanilla-only selectors receive a small set of explicit additions. Actual placement remains dependent on terrain acceptance and existing exclusions. `STRUCTURE-DENSITY-TEST1.md` and `BIOME-COMPATIBILITY-TEST2.md` list the exact changes. Wildlife, missing structure pieces/NPCs and overlaps remain separate audits; Traveloptics and Cataclysm Spellbooks issues remain deferred too.

## Compatibility test

The `ao_compatibility` datapack is loaded through Paxi. It adds the current modded biome IDs to the common `minecraft`, `c`, and `forge` climate/landform tags that structure definitions already read. It does not change structure spacing, structure weights or the Biolith replacement pools. The test question is whether the same structure groups that appear in vanilla biomes now become eligible in their curated climate equivalents.

The datapack also overlays Curios item tags. Enigmatic Legacy+ 1.1.2 already tags its standard coloured and named amulets, but the overlay repeats them, adds the fork's registered `enigmaticlegacyplus:the_necklace`, and adds `enigmaticlegacyplus:darkest_scroll`. If a particular item still refuses the slot, use F3+H and record its exact item ID; that ID will distinguish another fork item from a Curios slot problem.

## Install and start

For the small worldgen update ZIP, extract its contents into your existing 0.3.0.2 instance folder (the folder containing `mods` and `config`). This adds Biolith 3.0.14 and the worldgen settings without replacing your mod list or Streams Reflowing settings. Keep your current donor mod versions. The update expects the selected BWG 2.6.2, BOP 21.1.0.14, RU 0.6.2 and Nature's Spirit 2.2.5.

The earlier full 0.3.1 test ZIP was the locked base build with Biolith added and optional Integrated Patches. The current structure-test2 export includes Integrated Patches, Integrated Mowzie's Mobs, Integrated Bosses of Mass Destruction and Amendments by default.

1. Fully restart Minecraft after installing the update.
2. Create a NEW world. In the World tab, keep World Type **Default**, open **Customize**, and choose **Ambient Odyssey 0.3.1** under Your Presets. Apply the preset with **Done**. This uses FTF's own world-creation export path to generate its complete terrain datapack.
3. Check that the preset shows continent scale **6500** and river count **15**. It is based on FTF 1.0.0's built-in 4000-scale, 10-river `modernDefaultWithRivers` template. Other terrain, cave, river-width/depth, lake, island and land/ocean settings are retained from that template.
4. Keep shaders off for the first worldgen comparison. Use a known seed and consistent render/simulation distances.
5. Explore a few separate inland climate areas and record the F3 **Biome:** line, seed and coordinates. Region names alone do not identify the actual biome. Short local spawn sampling cannot establish world-wide percentages.

If the preset is missing, inspect `latest.log` and verify the JSON is in `config/freeterraforged/presets`. If the pools appear inactive, check `/datapack list enabled` for `ao_biome_replacement` and the log for Biolith placement loading. Do not use `/reload` to retune a running world: restart for Biolith rule changes and use fresh worlds for clean comparisons.

## First-pass pools

These percentages describe Biolith's normalized request weights within each targeted vanilla fallback, before the temperature guards below. Spatial noise, other mods' native placements and the seed determine actual area. They are not a promise of 95% curated surface coverage across the entire world.

| Original vanilla result | Vanilla retained | Curated pool, relative weights |
|---|---:|---|
| Plains | 5% | BWG Prairie 40, RU Grassland 35, RU Flower Fields 15, BWG Skyris Vale 10 |
| Sunflower Plains / Flower Forest | 5% | RU Flower Fields 50, BWG Sakura Grove 25, BOP Pumpkin Patch 15, RU Orchard 5, BWG Skyris Vale 5 |
| Forest | 5% | BWG Ebony Woods 30, Redwood Thicket 25, Zelkova Forest 20, RU Maple Forest 15, BWG Weeping Witch Forest 10 |
| Birch Forest / Old Growth Birch Forest | 5% | BWG Zelkova Forest 40, Sakura Grove 35, RU Maple Forest 25 |
| Savanna / Savanna Plateau | 0.5% | BWG Prairie 80, RU Grassland 10, NS Floral Ridges 10 |
| Windswept Savanna | 0.5% | BWG Prairie 75, RU Grassland 10, NS Floral Ridges 15 |
| Jungle / Sparse Jungle / Bamboo Jungle | 0.5% | BWG Crag Gardens 55, Ebony Woods 30, Redwood Thicket 15 |

These are explicit AO assignments. Savanna slots use retained warm open biomes because the curated list has no dedicated dry savanna donor. This deliberately extends some donors beyond their native selector cells; it does not rewrite their native TerraBlender tables.

Temperature guards use Biolith's real `original`, `value` and `all_of` criteria. They apply only when the ORIGINAL result was one of the vanilla targets above. Native curated placements remain intact. Cold non-frozen open slots prefer Alpine Clearings; warm forest slots prefer Ebony Woods; cool forest selections prefer Maple Forest/Maple Taiga/Zelkova; warm selections of Skyris Vale become Prairie. Floral Ridges is limited to warm slots; hot slots become Prairie and temperate windswept slots use Windswept Sugi Forest. These are conservative AO pool rules, not a claim to reproduce every native humidity/erosion constraint.

All 42 curated donors remain enabled. Volcano and Snowblossom Grove stay on their native placements; this first pool pass does not quantify or retune their global frequency. Skyris Vale and Floral Ridges have modest additional pool weights. The requested rarity categories remain tuning targets pending observations.

Desert, badlands, other unlisted vanilla surface biomes, oceans, coasts, rivers and caves are outside this first replacement pass. The patch does not change Nether or End biome rules. Review caves and oceans after the surface-biome test. Increasing continent scale makes features larger and does not independently increase land fraction.

## Edit the ratios

The active file is `config/paxi/datapacks/ao_biome_replacement/data/ambient_odyssey/biolith/biome_placement.json`. Biolith 3.0.14 reads that exact single-file path. It does not use the newer `biome_placement/*.json` layout.

For easier editing, the sources contain `release_030/biome-pools.json`: change `vanilla_percent` or the relative member weights, then run `python3 compile_worldgen_031.py`. Copy the regenerated `ao_biome_replacement` folder into your instance and restart. Climate guards are separately editable in that same authoring file. The authoring file itself is not a runtime mod config.

The compiler solves Biolith's rule: vanilla weight is `1 - max(proportions)`, then all weights normalize together. Setting every member's proportion to 0.95 would not retain 5% vanilla in a multi-member pool.

Global Biolith settings are supplied in `defaultconfigs/biolith/general.json`, the directory selected by Biolith's NeoForge platform helper. The Overworld replacement scale stays at its default 4 for this initial test.

## Quick acceptance checks

- Launch and create the FTF world; save the new log if either step fails.
- Confirm actual vanilla Plains/Forest/Birch/Savanna/Jungle coverage falls in several inland areas, including warm climates.
- Check climate boundaries, biome patch size, rivers and a few existing structures/trees visually.
- Confirm preserved cool, wet, ocean and rare curated biomes remain discoverable, especially RU's two restored retired biomes.
- After this passes, audit cave/ocean generation and collect larger-area measurements before tuning global rarity.
