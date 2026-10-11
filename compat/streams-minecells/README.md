# AO Mine Cells × Streams Reflowing compatibility experiment

**Target** Minecraft 1.21.1 · NeoForge 21.1.252 · Mine Cells 2.0.3 via Sinytra Connector · Streams Reflowing **2.14.4**.

Status (11 October 2026): **USER-VALIDATED SINGLEPLAYER COMPATIBILITY**. The player confirmed all three post-fix acceptance checks:
1. Mine Cells Prison dungeon generates connected rooms, functioning floors/stairs and a reachable Promenade exit.
2. Streams Reflowing rivers generate normally in the Overworld.
3. Mine Cells dungeon generation continues working after restarting and generating another dungeon.

This is a direct user gameplay verification, not an automated test. **Dedicated-server/multiplayer behavior is NOT YET TESTED.** Preserve the independently user-validated 328-mod Mine Cells control build as a rollback.

## What the code does
- Prevents Streams' `ChunkStepDefer.defer` from intercepting vanilla chunk generation in **any `minecells:*` dimension**. Outside Mine Cells the original deferral is unchanged.
- Prevents Streams' river-footprint and river-start vetoes from discarding Mine Cells' own structure implementations. Other structures are unaffected.
- Does not disable Streams or change its Overworld features.
- Does not distribute or modify Streams Reflowing's copyrighted binary.

These hooks were verified by disassembling the exact pinned Streams **2.14.4 NeoForge** JAR. Do not upgrade Streams without re-auditing targets.

## Validated singleplayer checks and outstanding server checks
1. Import the confirmed 328-mod Mine Cells control **as a separate instance**, then add Streams Reflowing **2.14.4** and the compiled `ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar` to `mods/`.
2. Use the exact pinned Connector, FFAPI, CCA, and Mine Cells versions of the working control. Preserve the control ZIP, branch, and original test world.
3. Start singleplayer. Verify both mods plus addon appear in the startup log.
4. Spawn a fresh Mine Cells Prison portal and enter it. Check spawn safety, connected rooms, stairs and floors, and real exit doorway. Enter the Promenade too. Prefer at least two fresh seeds/dungeon starts.
5. Check Overworld streams and near-stream structure generation still work. Check dedicated-server generation separately before promotion.
6. If failure persists: check logs for `MixinApplyError`, `InjectionError`, `ChunkStepDefer`, structure start vetoes, and region stalls. Revert ONLY the addon and Streams to the known-good 328-mod control.

**Acceptance:** user-validated in singleplayer for the three checks above. Dedicated-server/multiplayer compatibility remains unverified. Do not claim server compatibility or change Streams 2.14.4 without re-auditing its bytecode. The two bypasses are deployed together; it is not established which individual bypass is necessary. Streams may still precompute Mine Cells watersheds without affecting verified gameplay.
