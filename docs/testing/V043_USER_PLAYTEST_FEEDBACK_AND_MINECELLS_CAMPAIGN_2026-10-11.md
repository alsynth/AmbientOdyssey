# AO v0.4.3 user playtest feedback — 11 October 2026

**Status:** user-reported runtime findings; proposed changes NOT BUILT and NOT included in the v0.4.3 successful artifact. Preserve that tested ZIP and rollback.

## Confirmed user observations

- Startup and remaining features in the short v0.4.3 checklist appear to work fine.
- Questlog Q tab still displays in its old/wrong location (screenshot provided in conversation); user requires Q immediately on the **other side/right of** Settings gear on the same row. Source 0.1.4 intends settings-right via `SETTINGS_X=198`, but runtime screenshot contradicts the intended outcome. Audit effective GUI position, Better Inventory's native positioning, mod/version collision, whether a different Q-button owner is being seen, fallback logic, and renderer/widget bounds. Do not claim fixed from reading Java source. Preserve badge/click and multiple GUI-scale support.
- **Dragon Tower** from Block Factory's Bosses should be **slightly rarer**. Current CristelLib placement at `release_030/overrides/config/cristellib/block_factorys_bosses/structure_placement_config.json5` is spacing 96, separation 48. Candidate spacing 104 with separation held, subject to effective-placement and pack override validation (theoretical attempt-cell density about 15% lower). Keep other bosses unchanged.
- **Normal/CTOV villages** should generate less often while retaining biome eligibility, structures and varieties. Existing `ctov-common.toml` village size weights 10/4/1 control relative selection, not necessarily absolute overall worldgen frequency. Verify CTOV structure-set placement, CristelLib or worldgen override before changing values: avoid pretending weight changes definitely lower global spawn density. Outposts unaffected.
- Major freezes/performance issues occur primarily around `/locate` and teleportation into **unloaded chunks**. General gameplay performance otherwise acceptable. Treat as worldgen/structure-search cold-load spikes. Diagnose with Spark, chunkgen timing and isolated loaded-vs-unloaded reproduction; do not broadly cut mods or assume a constant FPS regression.

## Campaign concept — Mine Cells opening arc

- Start players in Overworld mainland, not inside the Fabric dimension. Supply the **buffed starter chest** and a nearby, accessible Mine Cells doorway/portal, preserving mod-native dimension rules.
- Players enter Mine Cells as **Act I / tutorial expedition**; explore and loot up to the first boss dungeon/arena, then receive a quest/story incentive to temporarily return to Overworld and gear through AO exploration.
- Re-enter Mine Cells to challenge the boss when prepared. Keep portal return, unlock/progression state, loot persistence, death/respawn and multiplayer synchronization in scope. Prefer quest/story nudges and native portals rather than scripts forcing dimension progression.
- **Open question:** can beds set respawn and be slept in within relevant Mine Cells dimensions on this exact 2.0.3 Fabric/Connector stack? Minecraft vanilla beds in non-overworld dimensions normally explode and do NOT set spawn unless the dimension explicitly permits them; DO NOT assume Mine Cells enables beds. Test in disposable copy after backing up, and avoid blindly right-clicking bed near valuable builds. Safe fallback: stable Overworld spawn bed outside portal, return shortcuts and later optional safe native respawn mechanics if supported. Do not directly patch Mine Cells internals unless unavoidable.
- Check whether exact Mine Cells 2.0.3 doorway placement/unlock and boss-door behavior permits the described *leave, gear, return* loop before locking the campaign design. Legacy Mine Cells versions allow Overworld placeable doorways; exact 2.0.3 behavior needs runtime verification.

## Proposed next grouped patch/test

- Fix and visibly verify Questlog Q placement.
- Reduce Dragon Tower and CTOV village actual generation slightly, maintaining unrelated structure placement.
- Recheck cold /locate and unloaded-chunk teleports with profiler; tag as deferred performance investigation unless crashes or world corruption.
- Campaign design is **future quest-content direction**, not a feature implemented in this patch; a focused optional portal/bed/respawn check will resolve its only blocking uncertainty.
