# Ambient Odyssey — Test8.6 Native Generation Repair Wave

**Source:** `worldgen/test8.6-generation-repairs` from successful Test8.5 private 3-mod roster. **Date:** 10 October 2026. Minecraft 1.21.1, NeoForge 21.1.252.

## Goal and freeze rules
Address **actual source-backed** structure failures visible in the Test8.3 / Test8.4 logs. User confirmed Test8.5 client launches with Better Bastions, NeoReefRedux, and Luki Woodland Mansions. No further mod additions or performance changes are requested. **Test8.5 is the known-good rollback.** Do not merge experimental worldgen before runtime verification, and do not equate disappearing warnings with correct generated structures.

## Confirmed underlying defects and scoped repairs

### 1. Archaion Ancient Keep: wrong starting jigsaw
Real Test8.4 error: `No starting jigsaw archaion:arena_mainhall found in start pool archaion:ancient_keep/main_path` (around 05:37:43 after /locate).

Binary audit of the **exact installed** `archaion-1.21.1-1.4.4.jar` and upstream 1.21.1 NBT:
- `arena.nbt`: the **`archaion:arena_mainhall`** jigsaw is at local [28,0,0], targeting `archaion:mainhall_arena`.
- `arena_hall.nbt`: complementary `archaion:mainhall_arena` jigsaw at [14,0,43], **not** the required `archaion:arena_mainhall` name.
- Upstream `ancient_keep.json` selects `main_path` as its start pool; that pool has **both** `arena` and `arena_hall` elements. When the incompatible `arena_hall` is selected for the root, the game reports the error.

**Fix:** Override only `archaion:ancient_keep` structure definition to use `start_pool: archaion:ancient_keep/start`. Add a new `start` pool with the **native arena entry including original processor**; retain the native `main_path` pool as the arena→hall expansion path. The earlier Test8.4 `rooms` and `rooms_x` overrides excluding upstream zero-byte misc-room NBTs remain intact. **Runtime assembly and loot remain untested.**

### 2. Farmer's Structures cooking houses: wrong namespace for five sub-pools
Test8.4: 42 unresolved `minecraft:cook_additions_1_pool` through `_4_pool` and `minecraft:cook_end_1_pool` references.

Source evidence: the checked-in installed-binary resource index `release_030/evidence/jar-resource-index-test6.json.gz`, provenance `FarmersStructures-1.0.6-1.21.1_neoforge.jar`, exposes valid `farmers_structures:...` template pools, not matching `minecraft:...` keys. Actual log coordinates show naturally occurring cook houses triggering those dangling references.

**Fix:** Added **five** `minecraft:` namespace alias JSON files, **copied exactly from the original installed-JAR pool records** except for their `name` IDs. Retained native 7, 10, 9, 14 and 31 elements (**71 total**), processor lists, paths, weights and fallback `minecraft:empty`. No structures removed and no invented templates. Verify actual generation of the rooms on a new seed; if a downstream attachment mismatch persists, inspect local jigsaw `target` names rather than editing indiscriminately.

### 3. Create Easy underground train junction: reference to nonexistent pool
Test8.4: 23 unresolved `create_easy_structures:undergroundtrain_station` refs.

Binary audit of `create_easy_structures-0.2a-neoforge-1.21.1.jar`:
- Contains **30** template pools; **no** `undergroundtrain_station` pool.
- `gross_tkreuzung.nbt`, local [8,0,2], refers to missing station pool with jigsaw `name=target=create_easy_structures:einsturz`.
- Although `station_underground.nbt` exists, its jigsaw names are `create_easy_structures:gross_gang`, `create_easy_structures:schiene`, and unnamed chest connectors; it **does not** have a matching `einsturz` connector.
- Inventing an alias pointing at the incompatible station template would not produce a valid join and could cause broken generation.

**Fix:** Define the missing native ID as a valid **one-entry `minecraft:empty_pool_element` termination** with `minecraft:empty` fallback. This prevents a missing-template-pool error and does not substitute incompatible geometry. **This branch currently does not generate a new station from that unsupported junction**: source pack has no matching template to attach. Its other corridors, chests, room pools and existing railway remain unchanged. Future redesign would need a correctly connector-tagged NBT variant, subject to visual testing.

## Still-open, not randomly altered
- Up to **1,000** repeated `minecraft:` blank jigsaw pool warnings in Test8.4, with many around Y 16–31. This is not a legal useful pool ID; must identify exact NBT owner and whether intentionally unused before editing. Separate CI scan of major structure JARs underway.
- Repurposed Structures city `fat_tower_top` required-piece selection failure occurred once in Test8.3 but **not** Test8.4. It may be terrain/space-dependent rather than a missing template; preserve native data pending more evidence.
- Dungeon Crawl block-entity spawner warnings in Test8.3, less evident in Test8.4. Need live spawned dungeon inspection.
- Ocean, Nether, End, river-bridge size, and full integrated-server worldgen all remain open gates. None were modified in this source wave.
- Performance tuning deliberately after worldgen signoff, per user.

## Build verification
GitHub Actions [Test8.6 CI](https://github.com/alsynth/AmbientOdyssey/actions/runs/38022665722) passed:
- 28 original mountain/biome/dragon/roster source checks before and after build.
- **30** new exact installed-JAR provenance/geometry preservation checks before and after build, including all **71** original Farmer pieces.
- Source-only reproducible private CurseForge import builder with checksum-locked NeoReefRedux and mandatory Better Bastions / Luki Woodland Mansions.
- ZIP CRC, root `manifest.json`, duplicate-member guard, 267 pinned CF project IDs, private NeoReef SHA1 and expected 8 new structure repairs.
- `Ambient-Odyssey-v0.3.8-Test8.6-Generation-Repairs-Private.zip` = **69,824,360 bytes**, SHA-256 `24a243753fd3b045869b161e3811f9d6b1b61fbac43822a1c1840e68f21f6f2b`.

**No Test8.6 Minecraft runtime test has occurred.** This is a private test ZIP, not a public CurseForge submission. Original Test4/Test6 validators contain known obsolete data/private asset assumptions; they were not falsely reported as passing.

## Focused user QA on new world
1. Keep the original Test8.5 profile untouched. Import Test8.6 as a separate profile (NeoReef/Better Bastions/Luki all included).
2. On fresh seed, `/locate structure archaion:ancient_keep` then visit at reported X/Z and spectator inspect Y−115-ish for arena with attached main hall and intact 10+7 room options. In new log, expect absence of `No starting jigsaw archaion:arena_mainhall` **only if this structure actually generates**.
3. Find a Farmer's Structures cooking house naturally, verify side rooms and ending pieces physically appear; log should no longer reference the five `minecraft:cook_*` missing pool IDs in fresh chunks. Beware repeated line counts are heavily affected by exploration volume.
4. Inspect Create Easy underground railways, particularly T-junctions near Y0–40. No missing `undergroundtrain_station` warnings; unimplemented `einsturz` station branch now deliberately terminates rather than generating a bogus station.
5. If any structure looks clipped, floating or unfinished, save seed, exact coordinates, F3 biome and screenshots. Save/exit normally and send `latest.log`.

