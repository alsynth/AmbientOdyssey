> **SUPERSEDED / CANCELLED — final owner decision 2026-10-14:** The whole Dungeon Crawl structure is Tier **3**, with **no upper-floor Tier2 or deeper-floor Tier4 split**. This document records a rejected technical option for historical context only. Do not implement the floor resolver or Tier4 zone.

# Dungeon Crawl: Tier 4 overall, Tier 2 upper-floor exception — 14 Oct 2026

Owner: dungeoncrawl:dungeon is **Tier 4 overall**, with the upper floors kept at **Tier 2**. An intermediate **Tier 3** band is suggested (not yet separately approved). Source mod in AO PR50: DungeonCrawl-NeoForge-1.21-2.3.17.jar.

## Verified technical limit
Native Dungeon Difficulty 1.21.1 Config.Zone.Filters has only biome and structure (with dimension match separately). It has no min/max Y, floor ID, vertical-depth or per-instance-height property. Matching structure ID dungeoncrawl:dungeon assigns the same DD tier to every floor. Duplicate same-ID rules do not split floors. Unknown JSON properties may be sanitized.
Source: https://github.com/ZsoltMolnarrr/DungeonDifficulty/blob/1.21.1/common/src/main/java/net/dungeon_difficulty/config/Config.java

## Feasible implementation options
1. Preferred: a small NeoForge addon or compat patch with a structure-instance-relative floor resolver. Find this dungeon's specific worldgen start and floor boundaries from valid native metadata or a reliable local-generation marker; apply Tier 2 near the top and Tier 4 at the bottom (optional Tier 3 between). **Never use absolute world Y** because dungeon elevation and floor count vary.
2. Investigate Difficulty+ 1.21.1 custom level resolver extension (DifficultyPlusAPI.registerLevelResolver), with exact installed DD 3.9.2 compatibility validated. Its level_range randomizes the entire structure's level, NOT per floor. Source: https://github.com/KevzCz/DifficultyPlus/blob/1.21.1/README.md
3. Investigate Dungeon Crawl pinned JAR's own floor-aware spawner/loot generation; editing level-specific templates might help but a blanket Tier 4 native DD structure zone would still scale mobs at the top.

## Safety / gating
- **Do not deploy blanket DD Tier 4 for dungeoncrawl:dungeon** until a Tier 2 upper-floor exemption is proven. Catalogue Tier 4 is a label only.
- Do not infer floor from global Y, which could also affect caves and other structures; calculate position relative to *each dungeon instance*.
- Do not silently adjust actual spawner contents, loot or worldgen or promote a test to runtime-verified.
- Test 3+ dungeons on differing surface heights, varied floor counts, spawner-created mobs, outside same-Y control, multiplayer, restart and old-world compatibility. Ensure no double-scaling or entity stacking with Apotheosis/other mods.
- Keep existing v3 difficulty pilot and rollback files intact: experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json.

**Status: User-approved structure-level Tier 4 and requested upper Tier 2; no floor-split implementation installed or runtime tested.**
