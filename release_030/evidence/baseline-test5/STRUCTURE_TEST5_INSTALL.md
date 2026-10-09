# Ambient Odyssey — Structure Test 5 installation and later acceptance

Import `Ambient-Odyssey-v0.3.1-structure-test5.zip` as a new CurseForge profile. It is a full import export with a root `manifest.json`, Minecraft 1.21.1, NeoForge 21.1.252 and the same 237 locked mod project/file pairs as Test 4. The ZIP contains overrides and manifest pins, not third-party mod JARs; the launcher downloads the pinned mods.

The static package and reproducible source build are complete without a gameplay prerequisite. Read `STRUCTURE_TEST5_VALIDATION.md` for the scoped checks and remaining JAR coverage limits.

For a later clean comparison, create a fresh world, retain the previous seed/settings, choose Default world type and select **Ambient Odyssey 0.3.1** in FreeTerraForged's Customize presets. The retained preset has continent scale 6500 and river count 15. Existing generated chunks keep their old structures.

Check `/datapack list enabled` and the new log for `ao_compatibility`, `ao_structure_density`, `ao_structure_repairs` and `ao_biome_replacement`. Restart when changing worldgen inputs. The earlier Test 1/2 notes are historical; the Test 5 changelog specifies current ownership and selectors.

## Later observations to record

1. Record seed, FTF preset, biome IDs, coordinates, render/simulation distances and a repeatable inland route. Measure ordinary generation separately from locate searches.
2. Check ordinary houses, WDA medium sites, villages and Dungeon Crawl in Prairie, Flower Fields, Sakura and appropriate forest/cool biomes. Check Bathhouse remains possible but rarer, and no Small Blimp or Coliseum naturally generates.
3. Check Sky Villages over land and rivers. Its selector includes `minecraft:river`, `minecraft:frozen_river`, `regions_unexplored:muddy_river` and `streamsreflowing:stream`. Record the biome underneath a visible stream; channels can occupy a land biome. Ocean biomes are excluded from this village tag.
4. Check the new Overworld Heavenly variants and original End variants. The Overworld command IDs changed because they are separate registered copies:

   ```mcfunction
   /locate structure ambient_odyssey:heavenly_challenger_overworld
   /locate structure ambient_odyssey:heavenly_conqueror_overworld
   /locate structure ambient_odyssey:heavenly_rider_overworld
   ```

   Original `dungeons_arise:heavenly_*` IDs now serve the End-only branch. A locate command measures search cost and nearest candidates; it is not an area-normalized density test.
5. Inspect Foundry gears, Mechanical Nest decorations and Cabin villager/lectern assemblies. Preserve template, pool, biome and coordinate evidence for remaining IDAS/CTOV errors.
6. Check Artifacts belts/hands/general slot behavior and record the exact item ID if an item is rejected. Keep the existing Enigmatic overlay checks available.
7. Record overlap, clipping and rare boss-landmark frequency. Candidate exclusions are directed and cannot certify all cross-mod bounding boxes.

Trees, wildlife, biome sizes and climate remain at Test 4 settings. Tan tuning is staged separately in `TANS_OPEN_FIELD_TUNING_PLAN.md`. The full unretrieved-JAR inventory and remaining static tasks are in TODO and the audit evidence.
