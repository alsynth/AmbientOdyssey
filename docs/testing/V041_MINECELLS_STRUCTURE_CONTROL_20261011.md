# Mine Cells: structure-placement control after missing dungeon (11 October 2026)

**Status: user-confirmed successful Mine Cells runtime test on 328-mod control; individual conflict source unresolved.**
Source: `experimental/v0.4.1-trek-sixfix-minecells-quests-20261010`.
This separate, import-only experiment leaves all 331-ref original source files unchanged and produces a 328-reference CurseForge profile for a controlled A/B test.

## New user evidence

- First Mine Cells transfer: two disconnected dungeon rooms and suffocation in wall.
- Next test: floors connected but no discoverable exit/progression.
- Hydrology isolation version: fresh world and `minecells:prison` produces only dark hardstone/brick terrain, **no visible dungeon rooms**.
- Latest log `latest(20261010-222142).log` contains 8167 lines; Mine Cells 2.0.3 is loaded through Sinytra, server enters `minecells:prison`, Structures Essentials emits duplicated-salt diagnostics, Streams Reflowing still precomputes prison watersheds with **0 segments / 0 lakes**. **No Mine Cells structure placement exception is logged**, and no indication the structure actually generated. Tan's Huge Trees scans the dimension without logged tree placement.
- Import shows `Mine Cells` with NeoForge 21.1.252, Minecraft 1.21.1. The included Noisiumed is v3.0.6 and Structure Essentials is v5.0.
- The log has unrelated errors (invalid air item NBT, Traveloptics entity tags, Iron's Jewelry loot, Bumblezone trades). Do not pretend these indicate the dungeon root cause.
- The prison design in Mine Cells source `PrisonGridGenerator` calls `addFloor(..., 3)` and places a `minecells:better_prison/promenade` exit; the empty dimension is genuinely not expected.
- Duplicated Mine Cells salts **are native intentional shared placement data**; do not randomize them.

## Control-pack changes

Remove **only from the derived CurseForge import manifest**:
- CurseForge 832882 — Structure Essentials: spacing, structure overlap and placement mixins; unrelated structure behavior may change without it.
- CurseForge 1430156 — Noisiumed: chunk/terrain generation optimizations.
- CurseForge 1581408 — Streams Reflowing: hooks into Mine Cells dimensions even after no_streams tag.
Retain all other 328 project pins, the exact Mine Cells bridge, Trek, six-fix patches, FTB Quests and associated configs. The unused Structure Essentials config file can remain as harmless text. Do not apply the prior no_streams tag. **All three are suspected cross-mod interference, not demonstrated culprits.**

This is a grouped isolation test only. If it solves generation, reintroduce each removed mod separately to identify the specific conflict. If it still fails, next test should be Mine Cells on the minimal connector runtime with full dungeon generation check, NOT merely a successful dimension forceload.

## Acceptance gate for a FRESH world

1. Import as **new CurseForge instance**: do not update/overlay an existing mod folder (an old JAR left behind invalidates the experiment).
2. Create a **fresh disposable world** and enter a newly spawned Mine Cells Prison doorway. Do not reuse affected chunks.
3. Confirm safe arrival in constructed rooms, multiple rooms and stairs, lower levels, and an actual **Promenade** doorway. Mine Cells is not accepted until all are confirmed.
4. If it fails, in the Mine Cells dimension run `/locate structure minecells:prison` if supported; note any result/error and screenshot the area. Send full `latest.log`.
5. Keep working v0.4.1 or rollback profile untouched; do not move an important save into the experimental build without backup.

Worldgen performance in this control may differ because two worldgen optimizers and a river generator were removed; this is NOT a proposed permanent optimization configuration.

## 11 October 2026 — USER RUNTIME SUCCESS (important baseline)

**User result:** "the control test worked, it seems to work perfectly." The clean import from this **328-reference structure-control build** restored Mine Cells dungeon generation and apparent traversability after the preceding full **331-reference builds** produced suffocation/disconnected rooms, missing progression or plain prison terrain.

**Log evidence:** `latest(20261010-232036).log` (user's control-test client log):
- The log explicitly identifies the instance as `Ambient Odyssey 0.4.1 - Mine Cells Structure Control TEST`, loaded Mine Cells 2.0.3 through Sinytra and had **no** Structure Essentials, Noisiumed or Streams Reflowing mod entries.
- The user entered `minecells:prison` at 01:13:05 and `minecells:promenade` at 01:16:29. These are confirmed dimension transitions, alongside the user's gameplay success report.
- **Tan's Huge Trees still scanned the Prison at 01:13:06 and Promenade at 01:16:29 while the dungeon worked**. Therefore THT's blanket feature registration is **not sufficient** to cause the failure. Optional biome exclusions for performance remain reasonable but must not be presented as a confirmed dungeon repair.
- No logged Mine Cells jigsaw/placement exception was found. Startup included unrelated warnings / missing textures. The FreeTerraForged shutdown counter reported **5.13 real chunks/sec**, but differs from earlier worlds/session workloads and is **not** an apples-to-apples benchmark.

**Causal conclusion:** The excluded set of **three mods as a group** accounts for the experimental difference; one or several may be responsible, including interactions. **No individual culprit has been proven.** DO NOT reintroduce all three in the main pack or switch back to the 331-mod guarded version and call Mine Cells fixed.

**Development decision:** Treat this 328-reference control as the *user-validated Mine Cells provisional baseline*. Preserve the tested CurseForge ZIP, its generation workflow and branch. All future feature and optimization work may build on this control recipe, keeping these three absent pending evidence for safe reintegration. Retain the intact 331-reference prior release and rollback branch independently.

**Source triage (not proof):** Noisiumed 3.0.6 source primarily targets noise/density/NoiseBasedChunkGenerator code while Mine Cells' prison uses `FlatLevelSource`. Structure Essentials targets general structure placement/search and exposes no documented per-dimension bypass for every mixin. Streams Reflowing actively ran chunk/dimension watershed work in broken full-pack logs, and the earlier biome-only `no_streams` tag did not produce an acceptable dungeon. Those facts help prioritize future code-level investigation, but cannot establish which removal restored functionality.
