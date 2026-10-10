# Ambient Odyssey — Test8.9 remaining worldgen defects (source-based follow-up)

**Date:** 10 October 2026. **Baseline:** Test8.8 private successful deterministic pack, inherited unchanged. **Branch:** `worldgen/test8.9-source-triage`. **Minecraft:** 1.21.1 / NeoForge 21.1.252. **Exact current version:** `0.3.8-worldgen-prefreeze-test1.9`.

## Scope

User requested **remaining generation defects** be repaired using the same SHA-pinned source inspection and multi-pass static validation as Test8.8, without mandatory new game tests. Distinguish **source-proven repairs**, **conditional mitigations**, **code-level defects requiring runtime verification**, and **visual/dimension acceptance that no static analysis can replace**. No performance, gameplay/QoL, global structure density or broad mod changes.

## Source-backed changes implemented

### Towns and Towers beach lighthouse: missing master-villager pool

Actual Test8.6 `latest(20261010-042806).log`: twice `Empty or non-existent pool: kaisyn:village/beach_lighthouse/villager_lighthouse_master`. Source: exact installed `t_and_t-fabric-neoforge-1.13.11.jar`, CurseForge project **626761** / file **8657120**, SHA256 `270fc0d1c99e54bc15f43d64bdaac60a90cb896efc357af624988e677136440f`. Native `beach_meeting_point_1.nbt` uses a `minecraft:bottom` connector with the missing pool; native `kaisy[n]/village/beach_lighthouse/villagers/lighthouse_master.nbt` is present, 1×3×1 with the matching `minecraft:bottom` jigsaw and outgoing reference to another absent pool.

**Repair:** Add Paxi pool `kaisyn:village/beach_lighthouse/villager_lighthouse_master` containing the **existing exact native lighthouse-master template**, and a terminating `kaisyn:village/beach_lighthouse/villagers/lighthouse_master` empty pool for that template's internal outgoing jigsaw. No fabricated NPC. **Important:** the source template has **zero embedded entities**. This fixes missing template-pool registration and restores the native template selection, but **does NOT prove a villager or unique trades spawn**; nor does it guarantee visual geometry correctness without a loaded Minecraft world.

### Repurposed Structures Overworld city: intermittent required top failure

Actual Test8.3 log, one event at **(-4360, 93, 3176)**: `Failed to create valid structure with all required pieces`; required `repurposed_structures:cities/overworld/fat_tower_top=1`. Exact installed `repurposed_structures-7.5.22+1.21.1-neoforge.jar`, CF project **368293** / file **8688394**, SHA256 `64e64109acf7673b969aca9b3cca0bb555777cd7038aa16aa32a1548d753f257`:
- Real `fat_tower_top` template pool and native NBT **exist**.
- Real tower connector sequence points at this cap; the city structure already includes the cap among `pools_that_ignore_boundaries`.
- Native Overworld city `size=5` while minimum required chain and optional side rooms/bridges consume jigsaw depth; high terrain variation and city bounding boxes can stop assembly. No definitive evidence that size is *the* cause of the one failed attempt.

**Mitigation:** Override only `repurposed_structures:city_overworld` structure definition, changing **`size: 5 → 7`**. Preserve all other keys, source pool, spawn limits, processors, terrain adaptation, liquid rules and frequency. Native template pool/room weights untouched. This **increases assembly search depth** and may reduce missing required-top cases, but cannot guarantee placement if obstructed by terrain or neighboring structures. No blanket collision bypass or fake required-piece stubs.

## Independently traced, not falsely labelled fixed

### Dungeon Crawl custom spawners

Test8.3 has **explicit** `[Dungeon Crawl/]: Failed to fetch a mob spawner at (-896,36,95)` (twice) and `(-895,36,98)`. Matched author's 1.21 NeoForge GPL source:
[Dungeon Crawl Spawner.java](https://github.com/XYROC/DungeonCrawl/blob/neoforge/1.21/src/main/java/xiroc/dungeoncrawl/dungeon/block/Spawner.java) calls `world.setBlock(pos, Blocks.SPAWNER.defaultBlockState(), 2)`, **then immediately** `world.getBlockEntity(pos)`; fails when the world-generation context has not yet created this entity. The mod's config `custom_spawners=false` would not remove this read: it gates later **extra customization only**, so is **not a valid fix**. A robust actual fix requires a separate tested code patch/mod update that safely handles deferred block-entity creation/serialization. No spawner replacement, disabling whole mod or undocumented binary rewrite was made.

### POI mismatch and WorldGenRegion early block entities

Minecraft emitted 9 `POI data mismatch: already registered` entries in Test8.6 and `WorldGenRegion: Tried to access a block entity before it was created` at two positions. These vanilla/NeoForge logging sites are not enough to link the POI issue to a specific mod or determine if it is persistent/corrupt. The block-entity warning can occur in generic asynchronous generation independently of Dungeon Crawl. The logs contain **no world seed, block-state owner or reproducing trace**. Do not suppress log messages, delete POI chunks, remove village mods or tamper with vanilla registries without attribution.

### Invalid loot and data tags

Test8.6 had 106 `minecraft:air` item stacks, several `redeco:hammer`, `traveloptics:blood_echo`, plus `traveloptics:element_fire` malformed source JSON, and missing `#forge:tools` tag in `traveloptics:can_cast_reversal`. These are **different classes** from structure-piece placement. The original Traveloptics source file is malformed (`Unterminated array at line 11 column 6`); a normal datapack replacement may not suppress parsing of the bad mod-provided file. Avoid bogus tag names, arbitrary replacement loot or silent unique-item deletions. See source-owner audits in branch CI. No fix is claimed without the exact generator/template source.

### Other remaining acceptance gates

- Real visual assembly for Archaion Ancient Keep, Farmers cook houses, Create Easy station termination and Repurposed city;
- underwater/worldgen oceans and rare structures, Nether Better Bastions, End cities, world transitions and **larger YUNG Bridges** in FreeTerraForged + Streams Reflowing;
- dedicated-server worldgen, chunk pregeneration and actual playability;
- any newly uncovered structure/biome conditions (without a reproduction).
These require representative in-game evidence to assert visually correct generation. Static source scanners can check presence and JSON but **cannot** truthfully substitute the generator or terrain collision engine.

## Verification and rollback

- `validate_worldgen_089.py` fetches exact **SHA-pinned source JARs**, verifies the RS override has **only** the size change and the existing tower cap really has a matching connector, and checks lighthouse start-pool/source-native template connector mapping plus the internal safe termination.
- Original **28 Test8.4** biome/terrain and **31 Test8.6** native structure checks remain unchanged in content; Test8.8 **273** binary NBT roundtrip repairs, one native cook/angler pool, all **267 CurseForge pins**, NeoReef SHA and private-only bundling are preserved.
- [Test8.9 build workflow](https://github.com/alsynth/AmbientOdyssey/actions/runs/38026492570) runs checks before and after packaging and builds two complete byte-identical ZIPs. **Wait for its actual conclusion**, do not assume pass merely because script files exist.
- User should keep Test8.6 or Test8.8 as a known-good **runtime rollback**; Test8.9 static success alone does not guarantee Minecraft runtime. No additional Minecraft test requested now.

