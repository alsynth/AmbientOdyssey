# AO v0.4.1 — Invalid item stack provenance coverage (11 Oct 2026)

Source branch: `experimental/v041-invalid-item-source-coverage-20261011`.
Base: `experimental/v041-worldgen-safety-patch-20261011` commit `4099a92`.
This is a **diagnostic patch**. It does not replace loot, modify any NBT, or certify the full 329-reference pack.

## Why another audit step is needed

The 11 October client log recorded ~540 messages about invalid `minecraft:air` item stacks and missing registry IDs, including `redeco:hammer` and `biomesoplenty:rose_quartz_shard`. The earlier `audit_invalid_structure_items_089.py` searched for `minecraft:air`, `redeco:hammer`, `traveloptics:blood_echo`, `meadow:alpine_salt`, and `create:crushed_iron_ore`; it omitted the Biomes O' Plenty ID and recognized only singular `data/<namespace>/structure/...` structure paths.

More importantly, the scanner takes its SHA-verified resource inventory from the older Test6 JAR index. This is **not a complete inventory of all mods introduced in 0.4.1**. A zero-hit scan is not evidence that all 329 pack references or runtime-generated loot are clean.

## Implemented

- Add `biomesoplenty:rose_quartz_shard` to the native item candidates, deriving byte candidates from one authoritative list.
- Recognize both singular current `structure` and older plural `structures` NBT template directories, without opening unrelated NBT/loot tables. Accept gzip-compressed and uncompressed NBT data, still parsed as NBT.
- Record historical-index coverage explicitly: candidate count, current resolved CF filenames absent from the old inventory, unreadable JARs, unmapped historical files, and a forced `coverage_complete: false` flag.
- Retain per-template source paths, item NBT paths, count values, and SHA-256 verification of indexed native JARs. No automatic item replacement.
- Add offline source regression tests; the regression workflow performs no remote download and is independent of the slower pinned-native-audit job.

## How to use evidence safely

The **original** native-attribution workflow on `experimental/v041-worldgen-safety-patch-20261011` remains the running historical scan. This patch does not interrupt it.

On a later thorough full-pack investigation, first obtain the **exact currently installed JAR list and hashes**, including newer 0.4 mods, and audit likely source structures/loot alongside the older pinned JARs. Correlate any found template with source SHA and in-game event. Do not replace all `minecraft:air` tags or invent substitute loot items without a confirmed owner and codec-safe transformation.

## Remaining blockers

1. Historical 089 scanner may still be incomplete if CFWidget metadata cannot resolve archived file names, if a pinned binary cannot be read, or if culprit item data is generated at runtime.
2. Dungeon Crawl's block entity lifecycle remains unresolved.
3. Tan/Hominid worldgen addon is compiled but requires live test; a static Mixin build does not prove runtime invocation.
4. Worldgen chunk-stall diagnosis needs fresh Spark server-thread plus worker samples on matching profiles.
