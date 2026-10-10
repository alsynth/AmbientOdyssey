# Ambient Odyssey — Test8.6 actual runtime log (user test)

**Date:** 10 October 2026. **Source:** private user-uploaded `latest(20261010-042806).log` (7957 lines), not committed in full because it includes user environment paths, account metadata, and other private data. **Pack:** Ambient Odyssey `0.3.8-worldgen-prefreeze-test1.6`; Minecraft 1.21.1, NeoForge 21.1.252, Java 21.0.9. No new gameplay/QoL changes made based on this log. This is evidence and next-step guidance, **not full worldgen sign-off**.

## Definitively observed
- Client launched; integrated server started **06:14:45**; user entered new world **06:16:41** and exited **06:27:46**; server stopped; **all dimensions saved** ~06:27:48 and client shutdown normally. **No fatal crash**.
- `ao_worldgen_final_fixes` was detected as a new datapack and automatically loaded (06:14:21).
- Both official CurseForge additions **Better Bastions** and **Luki's Woodland Mansions**, plus `neoreefredux-1.0.jar`, were found in mod list.
- `/locate structure archaion:ancient_keep` succeeded at 06:19:57, reporting **[288, ~, -640]**. **No** `No starting jigsaw archaion:arena_mainhall` warning or `misc_room` EOF. This is a positive log-level check, *not proof of correct arena/hall/rooms geometry*.
- `/locate structure farmers_structures:cooks` succeeded at 06:24:32, reporting **[0, ~, -896]**. **No** `minecraft:cook_additions_*` or `minecraft:cook_end_1_pool` unresolved warnings during this log. No `create_easy_structures:undergroundtrain_station` unresolved warning either. Counts are not directly comparable to earlier routes and may reflect fewer affected structures.
- Lithostitched emitted **214** missing template-pool references: **212 `minecraft:` blank** and **2 `minecraft:angler_additions_3_pool`** (both logged at **[87,72,-1297]**). New angler namespace error suggests the same Farmers Structures namespace defect as repaired cook pools, but must inspect the **exact native source pool, connectors and provenance before an alias**. Do not automatically create `minecraft:` blank catch-all.
- The integrated server reported **11** `Can't keep up` warnings, worst **20,217 ms**; other delays included 11,283 and 7,521 ms. This was a new-world exploration test, **not a controlled benchmark**. This log has no complete FTF shutdown chunks/sec report. Per user instruction, performance tuning stays after worldgen.
- **9** POI data mismatch errors (coordinates include underground and surface positions) and scattered `WorldGenRegion` block entity warnings remain, with possible structure ownership uncertain. Further owners/seed-based reproduction required before patch.
- Remaining secondary datapack/loot problems: invalid `redeco:hammer`, `traveloptics:blood_echo`, repeated `minecraft:air` itemstacks, Ice & Fire dread banner pattern, `traveloptics:can_cast_reversal` missing `#forge:tools`; not direct evidence of broken worldgen placement but need later content/loot audit.

## Test8.6 focused outcome
**Log-level progress** for three source-backed repairs. Cannot claim full fix until naturally generated / fresh-chunk Ancient Keep and Farmers cooking house are physically inspected, and a Create Easy underground T-junction behaves sensibly. Relative missing-pool warning count from previous run is **not normalized by chunks generated or structures visited**. Test8.6 branch and existing pack remain unchanged by this evidence note.

## Still-open worldgen gates
1. Attribute exact 212 blank `minecraft:` pool references to owner NBTs, decide whether deliberately terminal or assembly-breaking. Do not add a generic malformed pool alias.
2. Source-audit `farmers_structures:angler_additions_3_pool` versus `minecraft:angler_additions_3_pool`, and any other angler/farmer houses. Repair only exact mismatch and test assembly.
3. Verify Archaion root room correctness in newly-generated structure, not just `/locate`.
4. Reproduce and investigate Repurposed Structures city required `fat_tower_top` and Dungeon Crawl spawner issues if they reappear.
5. Finish representative ocean, Nether, End and large YUNG's Bridges natural spawn/placement acceptance.
6. Post-worldgen content/QoL wave may consider **optional Bonus Chest loot table** (keeps Minecraft Create World Bonus Chest ON/OFF setting), documented in [QoL audit](../audits/QOL_VISUAL_RENDERING_BACKLOG_2026-10-10.md). **Easy Anvils was declined and removed from the candidate list.** No Bonus Chest modification yet.

