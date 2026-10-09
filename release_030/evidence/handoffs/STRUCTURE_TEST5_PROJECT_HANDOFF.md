# Ambient Odyssey — Development Handoff
**Date:** 8 October 2026  
**Minecraft:** 1.21.1 / NeoForge 21.1.252  
**Current baseline:** v0.3.1 Structure Test 4  
**Next target:** Structure Test 5 — corrected biome eligibility and structure generation

## Project state

Ambient Odyssey is a large exploration/RPG modpack for 5–7 players. Current development is focused on world generation, biome distribution, structures and generation performance.

The existing worldgen setup is promising, but structure distribution still needs major improvements before finalizing the server world.

**Important:** Structure Test 4 is the latest prepared test build, but has not been tested. The editable source archive predates several Test 3 and Test 4 changes. The source and generated builds must be reconciled.

## Available source files

- `Ambient-Odyssey-v0.3.1-sources (3).zip` — main editable source archive.
- `Ambient-Odyssey-v0.3.1-structure-test4.zip` — latest CurseForge import build.
- `TODO.md` — full development backlog.
- `AO_Structure_Biome_Audit_Test4.md` — initial static structure audit.
- `STRUCTURE-DENSITY-TEST1.md` — original frequency changes.
- `BIOME-COMPATIBILITY-TEST2.md` — first biome compatibility pass.
- `AO_structure_test2_benchmark_audit.md` — locate benchmark.
- `latest(20261008-154804).log` — latest benchmark/runtime log.
- `mods1.zip`, `mods2.zip`, `mods3.zip` — complete uploaded installed mod collection.

Seven individual JARs were also uploaded: When Dungeons Arise, IDAS, Integrated API, Dungeon Crawl, Sky Villages, Sky Whale Ship and Moog's Structure Lib.

### Source locations

The main source archive contains:

- `release_030/structure-density.json`
- `release_030/biome-roster.json`
- `release_030/overrides/config/`
- `compile_structure_density_031.py`
- `compile_compatibility_031.py`
- `compile_worldgen_031.py`
- `build_release_030.py`
- `build_curseforge_pack.py`

**All fixes must be committed to editable source inputs, not only the generated CurseForge ZIP.**

## Current user requirements

### Remove entirely

- WDA Small Blimp.
- WDA Coliseum.

These should not naturally generate in new chunks.

### Reduce

- WDA Bathhouse frequency substantially, but retain the structure.
- Unnatural large-structure overlap.
- Disproportionately dense structure generation in vanilla biomes relative to modded biomes.
- Flying structures clustering over oceans when they should appear over land.

### Increase

- Dungeon Crawl dungeons.
- Ordinary medium houses and smaller buildings, particularly IDAS variants.
- Ruins, farmsteads, landmarks and mid-sized dungeons.
- Flying structures, especially the WDA Heavenly Challenger/Conqueror/Rider and compatible land-based sky structures.
- Overall appropriate structure eligibility in curated modded biomes.

Preserve the rarity and importance of major boss encounters, especially high-end castles and boss landmarks.

## Known Test 4 implementation problems

### 1. Small Blimp survives in an AO placement set

Test 4 disabled the native Small Blimp toggle and removed its dedicated extra set, but the inherited `extra_wda_land_and_sky` set still contains `dungeons_arise:small_blimp`.

Required:
- Remove it from all AO sets.
- Keep the native toggle disabled.
- Verify Integrated API's `disabled_structures` tag behavior in installed version 1.9.0 and add an additional safeguard if appropriate.

Apply equivalent complete disabling for Coliseum.

### 2. Duplicate placement membership

Several AO structure sets duplicate structures that also belong to native structure sets.

Investigate the actual mechanics and whether this creates effective additional generation, unintended suppression or misleading `/locate` behavior.

Prefer independently configurable, single-owner placement where practical. Do not rewrite the entire structure system until the installed definitions have been inspected.

### 3. Heavenly ship placement

Test 4 added one set containing three Heavenly structures:

`ambient_odyssey:extra_wda_heavenly_ships`

Settings:
- Spacing: 42 chunks.
- Separation: 22 chunks.
- Salt: 1984010124.

The three structures share placement candidates. This does not give each ship an independent frequency.

The additional set may not preserve native placement safeguards. Verify actual structure IDs, dimension eligibility, biome selectors and native placement settings.

Design appropriately rare but independently manageable ship placement, with strong land-biome coverage. Do not unintentionally multiply End generation.

### 4. Medium-house weighting

Mushroom House and Greenwood Pub were given increased weights in a mixed WDA placement set. This raises their relative selection probability without necessarily increasing total placement opportunities.

Ordinary buildings should receive an appropriate frequency system rather than merely competing more heavily with major structures.

### 5. Dungeon Crawl

Test 4 attempted to increase Dungeon Crawl frequency using spacing 22 and separation 9.

Verify these changes actually target its effective registered placement settings, then inspect its native biome selector.

## Modded-biome compatibility

Earlier AO compatibility work generated approximately 87 biome-tag files covering 41 distinct modded biome IDs.

The runtime reported 103 Overworld biome entries, including 50 non-vanilla entries. Some additional entries are cave biomes and should not receive normal surface buildings.

Generic `minecraft`, `c` and `forge` biome tags alone are insufficient to establish compatibility with every structure mod.

Audit, for every significant structure mod:

1. Actual `worldgen/structure` JSON and its `biomes` selector.
2. Referenced `tags/worldgen/biome` values and nested tags.
3. Resolved inclusion of curated AO biomes.
4. `worldgen/structure_set` placement settings.
5. Exclusion zones and dimension restrictions.
6. Config toggles and library-generated placement behavior.

Prioritize WDA, IDAS, Dungeon Crawl, Integrated Villages/API, Sky Villages, Sky Whale Ship, Moog's, Iron's Spellbooks, Repurposed Structures, Seven Seas, Cataclysm and other substantial structure providers.

Do not assume a structure is vanilla-only just because AO does not explicitly patch its namespace.

### Known invalid biome tags

The latest runtime log reports missing references:

- `idas:has_structure/byg_redwood_biomes` → `byg:redwood_thicket`
- `idas:has_structure/bygmohogany_biomes` → `byg:tropical_rainforest`
- `aether_villages:collections/ancient_aether_biomes` → missing Ancient Aether biome tag.
- `aether_villages:collections/aether_redux_biomes` → missing Aether Redux biomes.

Check the actual JAR definitions before overriding these. Empty optional collections with `replace: true` may be appropriate when those providers are absent, provided the references are not required elsewhere.

## Structure assembly problems

The runtime log contains missing jigsaw/template-pool references, including:

- WDA Foundry: `dungeons_arise:underworld/foundry/foundry_corridor_gears`
- IDAS Dread Citadel: `idas:dread_citadel/dread_citadel12`, `dread_citadel5`
- Integrated Villages: `cabin_village/villager_random`, `cabin_village/house/fisherman_lecturn`
- Other IDAS and CTOV pool references.

Determine which are genuine broken structure pieces versus harmless legacy references.

Do not invent empty template pools purely to silence warnings.

## Performance findings

Structure Test 2 locate benchmark:

- 164 completed searches.
- 22 distinct structure IDs.
- Median search: 3,122 milliseconds.
- Mean: 8,552 milliseconds.
- Worst: 141,631 milliseconds.
- 36 searches exceeded 10 seconds.
- Nine ModernFix watchdog incidents.

These are `/locate` search costs, not direct estimates of ordinary chunk-generation performance.

The log reports Streams Reflowing using slow terrain height sampling because ReTerraForged terrain data was unavailable during preparation. Investigate this separately, preserving the current worldgen stack unless an alternative is demonstrably better.

Structure Essentials also warned about duplicate structure-set salts. Shared salts are not automatically bugs; prioritize collisions between eligible sets in the same dimension and region.

## Other independent TODO investigations

- RAR-Compat appears to clear an Artifacts equipment-slot tag.
- Traveloptics has unresolved entity/item tags and model/resource errors.
- Some Cataclysm Spellbooks recipes reference unregistered items.
- Wildlife spawn compatibility and unwanted insects need a later controlled audit.
- Tan's Huge Trees is overly dense in Prairie/open-field biomes.
- Future FTF/Biolith tuning includes biome repetition, snowy peaks, coasts and climate-group size.
- Preserve the existing Integrated Stronghold arrangement and current agreed worldgen decisions.
- Keep unrelated QoL/content additions out of the current structure compatibility test.

## Implementation workflow for ChatGPT Work

1. Open and compare the original source ZIP, Structure Test 4 ZIP and uploaded JARs.
2. Build an exact inventory of native structure definitions, tags and structure sets.
3. Produce a structure-to-biome eligibility matrix, distinguishing verified failures from hypotheses.
4. Repair invalid structure references, native toggles and biome selectors where evidence supports changes.
5. Reconcile all Test 3/4 changes into the editable source configuration and compilers.
6. Apply targeted placement redesign for medium houses, Dungeon Crawl and flying structures.
7. Regenerate Paxi datapacks and CurseForge export using the source build scripts.
8. Validate JSON, tags, referenced structure IDs, archive CRC and CurseForge root `manifest.json`.
9. Create the updated source ZIP, importable Structure Test 5 ZIP, changelog, audit report and updated TODO.
10. Record all issues that still require Minecraft runtime testing.

**Do not mark a static check as a passed gameplay test.**

## Required deliverables

- `Ambient-Odyssey-v0.3.1-structure-test5.zip`
- `Ambient-Odyssey-v0.3.1-sources-test5.zip`
- Updated `TODO.md`
- `STRUCTURE_BIOME_AUDIT.md`
- `STRUCTURE_TEST5_CHANGELOG.md`
- `STRUCTURE_TEST5_VALIDATION.md`

Test 4 remains the baseline until Test 5 has passed static verification. No gameplay test is requested before those deliverables exist.
