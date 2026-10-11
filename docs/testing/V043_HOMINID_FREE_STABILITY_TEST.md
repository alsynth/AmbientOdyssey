# Ambient Odyssey v0.4.3 — Hominid-Free Stability Private Test

**User decisions, 11 October 2026.** This is the next PRIVATE test branch, not an approved main/rollback merge. Starting point is the exact successful GitHub Actions v0.4.2 combined ZIP from run 38152215903, SHA256 `d4f928aec66c9dceea275b71db299a871cdac1ba9d07c83f91bb20c2a9b32be3`. The build asserts that exact SHA and copies all unrelated entries byte-for-byte.

## Changes approved

1. **Remove Hominid 1.3.4 entirely**, CurseForge project `1221597`, plus its `hominid-common.toml` override. The user found its replacements displace correctly equipped and level-buffed dungeon zombies. Remove its custom AO Mixin source, Mixin registration, and REQUIRED NeoForge dependency. The worldgen addon advances `0.1.3-experimental → 0.1.4-experimental` and must retain Tan tree scheduling, Dungeon Crawl pending spawner NBT/zero-count optional payment fixes, and Dungeon Difficulty guarded retry. Native Gradle compilation and JAR assertions required.
2. **Questlog beside Settings:** move Q to the same row, **right of** native Better Inventory gear with a 2px gap. Reuse existing atlas and badge, dynamic click hitbox matching render, and fall back to the user-accepted above/below position on narrow screens. Bridge `0.1.3 → 0.1.4`.
3. **Concrete Subtle Effects × End Remastered mismatch:** last `latest(20261011-163613).log` shows `NoSuchMethodError JsonEye.getID()` from `subtle_effects`/fzzy config. Add *only* official CurseForge patch project `1657433`, file `8673508` (subtleendremcompat 1.0.0, MC 1.21.1 NeoForge), which specifically bridges this changed return type. Its release says tested with Subtle Effects 1.14.3; AO ships 1.14.0, so this is **source-reasonable but NOT actual runtime-verified** for this exact pairing. Keep both existing content mods.
4. All other **329 unchanged** third-party pins and one newly pinned patch = **330 total** after removing Hominid. Preserve all curated worldgen, six Dungeon Difficulty zones and native config path, proven amulet and spellstone, 15 source-converted Mine Cells recipes, existing Questlog Q1/FTB pages, Streams/Mine Cells patch, Luki/IDAS repairs, gamerules, and TREK/Create rarity.

## Intentionally NOT changed in this user-requested stability build

- Routine `minecraft:air`, obsolete `forge:` attribute and infrequent POI/sound warnings, unless there is evidence they break gameplay, save content or materially harm performance. No blanket NBT replacements.
- Goblin-Tuned prices, Apotheosis automatic trims, broad loot balance or six-dungeon tier assignment: all deferred to the future loot/difficulty pass per user.
- Approved gamerules already tested by the user; Mine Cells basic functionality already user-tested. No rework or extra microsessions.
- No generic CPU/FPS miracle claims. The logs show server stalls; controlled Spark/pregeneration checks remain important. A PasterDream/Screenshot Viewer reload burst and Better Advancements file-watcher exception appeared in the latest log, but the source/test does not prove recurring impact, so do not remove these mods blindly.
- Current worldgen logs do not show repeated Hominid removed-zombie warnings in newer sessions, yet the user specifically observed Hominid replacing intended dungeon enemies. **User gameplay preference overrides log cleanliness.**
- The old Hominid save may contain its entities/items and is NOT a reliable compatibility test of removal. **Back up any world; use a fresh throwaway save or clean copied world**. Preserve older v0.4.2 ZIP as rollback.

## Focused acceptance in ONE real playtest

- Verify 0.4.3 launches, creates/saves/rejoins a **fresh test world**, with Hominid absent from installed mods and no missing required Mixin target.
- In WDA Keep Kayra / Plague Asylum and Dungeon Crawl: zombie/skeleton spawners still produce their expected named/armored vanilla mob versions; `dd_scaled` and effective max HP match the six pilot configurations without unwanted Hominid replacement.
- Q tab visually appears **to the right of Settings**, not overlapping other tabs at the usual GUI scale. Click, exit, reopen; badge and shortcut remain functional. Check compact resolution fallback if convenient.
- Check Subtle Effects and End Remastered both initialize without `JsonEye.getID` / `NoSuchMethodError` under normal play **and after config reload if practical**.
- Ensure native Mine Cells Create/Farmer's Delight recipes and Dungeon Crawl spawners operate normally after fresh generation/restart if encountered. Existing user-confirmed Mine Cells functionality does not require repeating full portal campaign.
- Save `latest.log` from new run to assess new or worsening fatal issues and significant client/server stalls. Do not prioritize harmless warnings just because they remain in the log.

## Gate

GitHub CI: native Gradle compile of two fresh AO addons, no Hominid dependency/mixin, selected source safety validators, exact starting ZIP SHA check, manifest entry/remove swap, JSON/Paxi/rule preservation, all other ZIP entries byte-equal, CRC and exact 330 unique refs, standalone inner CurseForge `manifest.json` at root, and profiler static preflight. **CI is NOT a Minecraft client/server test.**
