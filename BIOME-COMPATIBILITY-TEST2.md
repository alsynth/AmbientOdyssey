# Ambient Odyssey 0.3.1-structure-test2 — biome eligibility

This is a compatibility test layered on top of the first structure-frequency pass. The field report showed many structures in vanilla biomes and very few in modded biomes. The installed structure definitions explain that pattern: many selectors reference tags such as `minecraft:is_forest`, `minecraft:is_mountain`, `c:is_plains`, `c:is_snowy`, `c:is_ocean`, or direct vanilla biome IDs. Several active biome providers did not contribute their current IDs to those selectors.

## What the test adds

- `config/paxi/datapacks/ao_compatibility` extends the common `minecraft`, `c`, and `forge` biome tags for the current curated Overworld roster. The classifications cover forests, taigas/conifers, jungles, plains, hills/mountains, snowy and icy areas, swamps, oceans, beaches, rivers, lush areas, floral areas and hot/cold climate groups.
- Direct vanilla-only lists receive focused additions for Bosses' Rise dragon towers and yeti hideouts, Bosses of Mass Destruction's cold collection, Dungeons Arise's small prairie and giant mushroom landmarks, and Ice and Fire mausoleums.
- Curios receives a tag overlay for Enigmatic Legacy+ 1.1.2. The active coloured and named amulets are explicitly listed, `enigmaticlegacyplus:the_necklace` is assigned to `curios:amulet`, and `enigmaticlegacyplus:darkest_scroll` is assigned to `curios:scroll`.

The patch leaves spacing/separation, structure weights, terrain acceptance and Biolith pool ratios alone. It also leaves the providers' original tag entries in place, so vanilla-biome behavior is retained while curated equivalents gain the same selector coverage.

## Fresh-world checks

Use the same seed, preset and route as the structure-test1 comparison, then record the F3 biome ID at every structure or empty area. Sample at least one open field, forest, Sakura Grove/Prairie, cold forest or mountain, swamp/coast, and an ocean route. Compare the number and types of structures in a similar generated distance rather than comparing a single close cluster.

Pay special attention to Apotheosis towers, Dungeons Arise houses/landmarks, villages and farms, Moog sky structures, MTR/Integrated Villages collections, IDAS collections, Iron's Spellbooks towers and the Bosses' Rise dragon/yeti structures. The first acceptance signal is that these groups appear in matching curated climate categories; frequency and collision tuning follows after eligibility is confirmed.

For the Curios check, open the Curios screen and test one coloured Enigmatic Amulet, one named amulet, `The Necklace`, and `Darkest Scroll`. If any item is still rejected, record the exact F3+H item ID and the slot name shown by Curios. A standard coloured amulet should now be accepted by the amulet slot.

## Limits

This datapack is specific to the locked Ambient Odyssey profile and its active 1.21.1 mod versions. Runtime generation is still required to confirm that a selector, terrain test, spacing rule and structure piece all succeed together. Wildlife selectors also consume some common biome tags, so the separate wildlife audit should record any spawn-rate changes before this compatibility layer is treated as final.
