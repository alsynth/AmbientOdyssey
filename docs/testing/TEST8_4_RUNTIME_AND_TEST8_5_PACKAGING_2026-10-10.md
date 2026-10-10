# Ambient Odyssey — Test8.4 actual runtime and Test8.5 complete roster packaging

**Date:** 10 October 2026. **Source branch:** `worldgen/test8.5-mod-roster` (based on Test8.4's source, *not merged* into `structure/test6`). **Minecraft:** 1.21.1, NeoForge 21.1.252, Java 21. Build outputs are private test candidates, not public CurseForge moderation submissions.

## User's actual Test8.4 report and log

User reported **no visible worldgen problems** after deliberately pushing fast chunk loading; benchmark expected poor. Uploaded client log `latest(20261010-034122).log` has **8,665 lines**, world launch and normal clean save/exit, no game crash. User's Test8.4 `mods` listing includes **both** `betterbastions-1.0.0+neoforge-1.21.1.jar` and `neoreefredux-1.0.jar`, confirming they were manually present in that instance, but the earlier CurseForge source export had neither built into its manifest/overrides.

### FreeTerraForged perf report (NOT an apples-to-apples benchmark)
| Metric | Test8.3 | Test8.4 |
|---|---:|---:|
| Chunks | 7524 | 4567 |
| FTF real chunks/sec | 8.25 | 6.68 |
| FTF CPU time/chunk | 123.03 ms | 182.43 ms |
| Peak threads | 14 | 16 |
| Parallel efficiency | 7.2% | 7.6% |
| Integrated server `Can't keep up` | 12 | 10 |

Test8.4 generated 4567 chunks during **683,480 ms** FTF wall clock, with 833,165 ms summed thread time and 10 server lag warnings. Worst was about **25.2 sec**, then ~20.3 sec. User purposely pushed chunk loading hard; **do not ascribe rate difference to mountains, Streams Reflowing or mods without controlled seed/cold-cache A/B**. Performance tuning is deliberately deferred until worldgen is accepted.

### Remaining technically observable generation defects

- **Archaion repair is partial:** the two previously broken empty-NBT `misc_room` / `misc_room_x` EOF errors from Test8.3 are no longer in this run. However Test8.4 had exactly one new `No starting jigsaw archaion:arena_mainhall found in start pool archaion:ancient_keep/main_path` while using `/locate` (around 05:37:43). **Do not sign off Ancient Keep assembly yet.** It might involve upstream root pool `main_path`, malformed start-jigsaw selector, or author asset mismatch. Inspect real 1.21.1 JAR templates before patching.
- **Lithostitched missing jigsaw pool refs:** **1065** total: **1000** `minecraft:` blank, **23** `create_easy_structures:undergroundtrain_station`, **42** `minecraft:cook_*_pool` distributed among five named cook pools. Nonfatal runtime warnings but structure components may be missing; still need authoritative source attribution/repairs.
- **Traveloptics** `tags/entity_type/element_fire.json` failed parsing (`Unterminated array`, line 11 column 6), affecting `traveloptics:element_fire` mob tag. Also `traveloptics:can_cast_reversal` references missing, trade offer `traveloptics:celestial_shard` missing. Repair only from valid source assets.
- **Missing ItemStacks in generated loot:** repeated unknown registry refs including `meadow:alpine_salt` and `create:crushed_iron_ore`. Investigate applicable loot and data providers. Dungeon Crawl has a block entity creation-order warning.
- **Pre-existing content:** BetterEnd Patchouli guidebook skipped, 89 missing models, recurrent tag/animation warnings. Do not conflate rendering/animation warnings with worldgen crashes.
- Chunk-gen profiling remains an unresolved release goal, after worldgen freeze.

### User-requested mandatory mod roster for next builds
| Mod | Authority | Packaging |
| --- | --- | --- |
| Better Bastions | CurseForge project **1713723**, file **8988949**, 1.21.1 NeoForge | Mandatory `release_030/release-lock.json` `additions`; CurseForge installs automatically. |
| Luki's Woodland Mansions | CurseForge project **1385782**, file **7227735**, 1.21–1.21.4 compatible on NeoForge | Mandatory `release_030/release-lock.json` `additions`; CurseForge installs automatically. |
| NeoReefRedux 1.0 | Modrinth project **5bMVdkpO**, version **PVzfioBU**, GPL-3.0-or-later, SHA1 **10160406202fd3dadd295e130b380466436e0981**, SHA512 in release lock | `python build_release_030.py --private-modrinth` downloads/pins the 80,519-byte JAR automatically and injects `overrides/mods/neoreefredux-1.0.jar`, strictly checked against both hashes; **private test only**. Public CurseForge pack requires legal/moderation approval for external asset inclusion. |

**Why Luki Woodland:** Its mansion was separated from Luki's Grand Capitals. Test8.4 has Luki Ancient Cities and Luki Grand Capitals but *not* Luki Woodland Mansions.

## Verified Test8.5 private ZIP
- GitHub Actions [private packaging workflow](https://github.com/alsynth/AmbientOdyssey/actions/runs/38021804642) **passed** `validate_worldgen_test84.py`, downloaded the pinned Modrinth version and checked hashes, built the archive, validated 2 CurseForge manifest pins, verified ZIP CRC/root manifest and uploaded exact importer.
- `Ambient-Odyssey-Test8.5-Private-All-Three.zip`: **69,819,810 bytes**, **1,098 members**, SHA256 **`cb81c691aeab690bb13a84545b27ff82422ac4fd4b116a2ca5cd97af3550f99c`**.
- Release lock version `0.3.8-worldgen-prefreeze-test1.5`; 2 new CurseForge references expected vs Test8.4.
- This is **not runtime tested yet**, and does **not** establish Archaion, traveloptics or all structure pools are fixed.
- Preserve successful Test8.4 profile. Next test: import the ZIP as a separate profile and verify all three in Mods/Log, woodland mansion normal placement, no duplicate datapack/mansion overwrites.

## Freeze decision

User's visual acceptance is a strong green signal for terrain/biomes. But leave full worldgen freeze open until Ancient Keep root jigsaw, Create Easy and cook pools, ocean/Nether/End tests, and required mod additions are verified in actual Minecraft. Continue to defer active performance changes.
