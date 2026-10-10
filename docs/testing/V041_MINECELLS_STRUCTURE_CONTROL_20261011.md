# Mine Cells: structure-placement control after missing dungeon (11 October 2026)

**Status: investigation, NOT FIXED or gameplay-certified.**
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
