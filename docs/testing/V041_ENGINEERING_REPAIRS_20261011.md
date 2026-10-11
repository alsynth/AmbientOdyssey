# Ambient Odyssey v0.4.1 — engineering repairs and precise remaining blockers

**11 October 2026.** Experimental source branch: `experimental/v041-engineering-repairs-20261011` based on the separately CI-validated source-coverage branch. The earlier user-tested 328-reference Mine Cells control and 329-reference Streams-compatible build are preserved. Changes here do NOT represent Minecraft gameplay signoff.

## Source and runtime evidence

The user-uploaded client `latest(20261011-014807).log` contains 9,449 log lines. It was from the earlier 328-reference Mine Cells control with Questlog manually installed, **without Streams Reflowing** and before the three newest bundled AO addons. It is not a runtime test of this branch.

| Observation | Actual count / evidence | Engineering decision |
| --- | --- | --- |
| Invalid `minecraft:air` stack logging | 540 messages | Exact source JAR audit; do not rewrite optional trade `buyB`, empty display/filter stacks or equipment in bulk |
| Unknown registry item keys | 6 messages (`redeco:hammer` x2, `biomesoplenty:rose_quartz_shard` x4) | Source-match only; old Test6 binary index isn't complete 0.4.1 coverage |
| Legacy attribute warnings | 572 (`forge:entity_gravity` 367; `forge:step_height_addition` 111; `forge:swim_speed` 89; `obscure_api:regeneration` 5) | Attribute migration needs actual source template and 1.21 registry semantics before editing entities |
| Dungeon Crawl missing spawner | 1 error | Preceded by TWO `WorldGenRegion: Tried to access a block entity before it was created` warnings at same position. Native method calls `LevelAccessor.setBlock(SPAWNER)` then immediately `getBlockEntity`. The lifecycle bug is evidenced, but safe persistence of an alternative block-entity setup is not established |
| Offthread entity creation | 3 Cupboard warnings | Native Hominid / Tan Tree targeted fixes are compiled, not runtime confirmed |
| Server tick stalls | 12, worst **27,486ms** | Real slow cold-generation/teleport and surrounding workload. Source not profiled; no claim Spark background toggling fixes it |
| Luki mansion jigsaw | 4 missing-pool warnings | One missing native pool repair already implemented in earlier branch, still needs new-generation test |

The completed historical pinned JAR scan checked 65 native archives, found 3,397 matching item references in 17 archives, with four source archives unreadable. **Counts of source NBT references are not counts of errors at runtime.** They include many valid empty-slot representations and other mod data.

## Exact IDAS Ancient Mines Create repair

The historical scan located exactly seven `create:crushed_iron_ore` item stack references in:
- `data/idas/structure/ancient_mines/ancient_mines_hall2.nbt` (3)
- `data/idas/structure/ancient_mines/ancient_mines_hall3.nbt` (4)

Current Create 1.21.1 registers `create:crushed_raw_iron`; see [upstream Create item registry](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/src/main/java/com/simibubi/create/AllItems.java) and its [iron crushing recipe](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/src/generated/resources/data/create/recipe/crushing/iron_ore.json).

Script `tools/repair_v041_idas_create_items.py` downloads the **exact manifest-pinned IDAS 1.13.7 JAR**, verifies its SHA against the saved native binary inventory, loads two original NBT structures, changes only seven matching item stacks with `Items` paths, and fails closed on mismatched counts or semantic drift. It emits a distinct private Paxi datapack `ao_idas_create_item_compat` and JSON provenance. The compiled CurseForge test ZIP should contain only those two extra structure NBTs and the datapack metadata.

**Copyright/distribution:** The patched native structure templates are author-owned assets. Private acceptance build only; never send this ZIP as a public CurseForge release without resolving redistribution rights and using an appropriate upstream fix instead.

## Spawner engineering decision

The exact pinned Dungeon Crawl 2.3.17 native JAR SHA256 is `853cd59208f17c25188a419b48d1a9fed3acebf676bb1ddd026fa4e7fb56dad4`. `tools/audit_v041_dungeoncrawl_spawner.py` rechecks its bytecode and records the risky placement/lookup sequence.

A synthetic BE returned by a mixin without persisting it into the chunk is a **false fix**. Writing pending NBT from an async worker or deferring a task into a not-yet-generated chunk may introduce race conditions, duplicate/block entity loss or blocking loads. We have **not deployed** such an unproven patch. Real acceptance requires fresh dungeon generation and seeing configured mob spawners rather than default/empty block entities, followed by save/restart and multiplayer checks.

## Performance experiment, not claimed optimization

`tools/make_v041_spark_profiler_ab.py` creates a second ZIP that changes only `spark/config.json` from `backgroundProfiler: true` to `false`. It asserts the exact 329 pinned references and every other override are identical. Spark is retained so profiles can still be manually started.

The first Spark viewer could not be read in previous work; no CPU samples are being claimed. For meaningful optimization, use comparable warm-idle / cold-chunk / same-route warm-chunk tests with Spark server-thread, chunk-worker, GC, FPS and MSPT data. Avoid retuning FreeTerraForged, scenery or iconic structures without evidence.

## Static workflow gates

- Full three-addon/private pack: `.github/workflows/v041-engineering-idAS-private.yml`
- Fast regession and native bytecode: `.github/workflows/v041-engineering-static-triage.yml`
- Original v0.4.1 worldgen safety source and 329-pin control remain untouched.
- Static passes may establish ZIP integrity and exact substitutions only. Full Minecraft client, save/reload, Mine Cells Prison progression, mansion placement, Dungeon Crawl spawners and 5–7-player performance still require a real runtime test.
