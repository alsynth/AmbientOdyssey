# AO Mine Cells × Streams Reflowing compatibility experiment

**Target** Minecraft 1.21.1 · NeoForge 21.1.252 · Mine Cells 2.0.3 via Sinytra Connector · Streams Reflowing **2.14.4**.

Status (11 October 2026): **initial user runtime feedback positive** — user reports “it seems to have worked” with the code-level addon. Exact test scope (full Prison progression, Promenade exit, repeated fresh dungeon, Overworld streams, dedicated server) was not supplied. Record this as a promising smoke-test result, **not full acceptance**. Keep the user-verified 328-mod Mine Cells control build as rollback.

## What the code does
- Prevents Streams' `ChunkStepDefer.defer` from intercepting vanilla chunk generation in **any `minecells:*` dimension**. Outside Mine Cells the original deferral is unchanged.
- Prevents Streams' river-footprint and river-start vetoes from discarding Mine Cells' own structure implementations. Other structures are unaffected.
- Does not disable Streams or change its Overworld features.
- Does not distribute or modify Streams Reflowing's copyrighted binary.

These hooks were verified by disassembling the exact pinned Streams **2.14.4 NeoForge** JAR. Do not upgrade Streams without re-auditing targets.

## Smoke test (fresh disposable world only)
1. Import the confirmed 328-mod Mine Cells control **as a separate instance**, then add Streams Reflowing **2.14.4** and the compiled `ambientodyssey-streams-minecells-compat-0.1.0-experimental.jar` to `mods/`.
2. Use the exact pinned Connector, FFAPI, CCA, and Mine Cells versions of the working control. Preserve the control ZIP, branch, and original test world.
3. Start singleplayer. Verify both mods plus addon appear in the startup log.
4. Spawn a fresh Mine Cells Prison portal and enter it. Check spawn safety, connected rooms, stairs and floors, and real exit doorway. Enter the Promenade too. Prefer at least two fresh seeds/dungeon starts.
5. Check Overworld streams and near-stream structure generation still work. Check dedicated-server generation separately before promotion.
6. If failure persists: check logs for `MixinApplyError`, `InjectionError`, `ChunkStepDefer`, structure start vetoes, and region stalls. Revert ONLY the addon and Streams to the known-good 328-mod control.

**Explicit limitation**: initial player feedback is positive but comprehensive client/server runtime validation is still pending. These targeted hooks appear promising, but we have not isolated which of the two bypasses is essential, and other Streams hooks may still precompute Mine Cells watersheds. Do not claim full compatibility or promote the addon to the main release before the above checks.
