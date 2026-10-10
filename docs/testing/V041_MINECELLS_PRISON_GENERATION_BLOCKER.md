# Mine Cells Prison generation failure — test evidence (2026-10-10)

## Observed on six-fix test (CONFIRMED, user runtime)
- The portal interface worked and dimension switching to `minecells:prison` succeeded in Minecraft 1.21.1 / NeoForge 21.1.252 with Mine Cells 2.0.3 via Sinytra Connector.
- On arrival the player was suffocating inside blocks **outside the dungeon**.
- Spectator examination revealed **two separate, nonconnecting rooms**, without a traversable route or exits.
- Log shows active world-generation hooks **inside** `minecells:prison`:
  - 23:10:16.227 Streams Reflowing uses dimension-specific watershed processing for the prison; its reported network output was `segs=0 lakes=0` in the sampled plates, so causality is NOT established.
  - 23:10:16.262 Tan's Huge Trees processes `minecells:prison` regions (and completes); do not assume this necessarily placed trees.
  - 23:05:09 Structure Essentials reports several Mine Cells structure sets share native salt `2043237655`. This may be intentional for coordinated placements. Do NOT randomize the salts as a generic warning cleanup.
- The log does **not** list FastNoise/zfastnoise or Sparse Structures as installed.

## Relevant upstream reports
- https://github.com/mim1q/MineCells/issues/58 — hardstone encasement/unreachable rooms, likely cross-mod structure-placement interference.
- https://github.com/mim1q/MineCells/issues/104 — portal wall spawn from Sparse Structures in older modpacks; **not installed here**, so do not apply its workaround blindly.
- https://github.com/mim1q/MineCells/issues/189 — **1.21.1 NeoForge + Sinytra + Mine Cells 2.0.3** and exactly **disconnected jigsaw pieces** with FastNoise; disabling FastNoise solved that separate setup, but FastNoise is **not present** in this log. This indicates generator/mixin conflicts are plausible, not proven here.

## Reproduction / safe diagnostic test
1. Back up the world. Existing generated chunks will not magically repair after a configuration change.
2. Check vanilla Fabric 1.21.1 + Mine Cells 2.0.3 + its minimum native dependencies on a fresh world; record dungeon spawn, paths and exit.
3. Check NeoForge 21.1.252 + Sinytra Connector + Forgified Fabric API + Cardinal Components + owo-lib + Mine Cells on a fresh world; use exact installed versions.
4. If the minimal bridge succeeds, reintroduce AO worldgen changes in groups; prioritize terrain/structure-related mods and mixins: Structure Essentials, Streams Reflowing, Tan's Huge Trees, Noisiumed, biome/structure/jigsaw remappers. Inspect any mod known to alter jigsaw placement.
5. Test the same seed, or multiple fresh seeds/portals, with and without each suspect. Capture coordinates and output logs, document whether dungeon start, complete room connections, progression and exit work.
6. If failing even on the minimal bridge stack, escalate to the Mine Cells / Connector compatibility path or leave Mine Cells as experimental, NOT accepted. Avoid hacks that merely teleport the player into one of the orphaned rooms.
7. Check that Trek and DnT worldgen in the Overworld still works independently; never fix this by disabling global structure generation.

**Acceptance gate:** new dungeon generates a navigable, connected full path; arrival safely inside its entry; no block suffocation; route to exit works. Static validators cannot establish this.

**Current status:** portal UI and transport confirmed; Mine Cells procedural dungeon **BROKEN / UNRESOLVED**; no runtime fix is claimed.

## Follow-up observed 11 October 2026
- **User runtime:** Mine Cells rooms/floors now connect, but no discoverable way to progress to the next destination. This is an improvement over separate pieces, **not** a successful progression test. The mod developer describes a Prisoners' Quarters **doorway to the Promenade of the Condemned**; a staircase or further downward floor is not by itself the acceptance condition. See https://mim1q.dev/minecells/progression-guide/.
- The newly uploaded `latest(20261010-220044).log` has only 95 lines of **clean client/world shutdown**, not world-entry, portal or jigsaw placement logs. It cannot identify the generation culprit. The FreeTerraForged shutdown report shows **2,385 chunks**, **233.40 ms/thread/chunk**, **2.41 real chunks/sec** and **4.7% parallel efficiency** over **991,305 ms wall time**. This is a performance concern, but not an A/B benchmark nor evidence that FTF broke Mine Cells.
- Confirmed Mine Cells upstream five biome resource IDs from `mim1q/MineCells` worldgen source: `black_bridge`, `insufferable_crypt`, `prison`, `promenade`, `ramparts`.
- **New isolated preflight candidate:** add those five biomes to the documented `#streamsreflowing:no_streams` datapack tag, through the compiler-owned `ao_compatibility` pack. Streams Reflowing documents this opt-out: https://modrinth.com/mod/streams-reflowing/version/Gev9Gbnm. This changes only hydrology eligibility in those special biomes, not Mine Cells placements, jigsaw pools or shared salts. **It is not a proven repair for missing exits.**
- To test: **back up the save and use a new world or genuinely new Mine Cells generation area**. Compare with old build using a fresh prison entrance; confirm safe spawn, navigable connected route and the Promenade doorway. If still missing, isolate additional worldgen/jigsaw mixin participants, beginning with Structure Essentials and other code touching jigsaw placement. Do not delete saved dimension data without a backup.
