# AO v0.4.2 user test — Dungeon Crawl difficulty attribution (11 Oct 2026)

## Actual uploaded run evidence (private; don't commit raw log)

User tested the exact `Ambient Odyssey v0.4.2 - Spellstone Dungeon Difficulty Combined TEST` profile with NeoForge 21.1.252. The user **confirmed Curios spellstone is fixed**, and reported more buffed skeletons in Keep Kayra, but **no detectable buffs in a newly located Dungeon Crawl dungeon**. Other mobs displayed special health bars, which may be unrelated to Dungeon Difficulty. Do not infer that they were buffed.

Uploaded `latest(20261011-161328).log`: 9,801 lines; session 17:57:55–18:13:15. Loaded `dungeon_difficulty-neoforge-3.9.2+1.21.1.jar`, AO `ao-worldgen-safety-0.1.3-experimental.jar`; AO late-evaluation registration at 17:58:33. There were **zero** recorded native `dd_scaled`/entity-level scale decisions and **zero** AO deferred-retry exceptions. No fatal Minecraft crash. User ran `/locate structure dungeoncrawl:dungeon` at 18:11:47; returned [-2496,~,96] 84 blocks away, then teleported -2495.5,106.74,96.5. **Locating a structure doesn't prove an enemy is inside its exact bounding box**.

Remaining unrelated warnings/errors: 113 `Item must not be minecraft:air` on worldgen workers, several `WorldGenRegion Tried to access a block entity before it was created` (including -2646,-19,30 and -2713,-29,29 near the Dungeon Crawl visit; source owner unconfirmed), 2 `POI data mismatch`, 2 IntegratedAPI missing swamp-village priest pools, 9 server lag warnings (longest 45,201 ms), ModernFix watchdog stack dump 40,001 ms; main server thread blocked loading chunks and one worldgen worker in Biolith biome lookup. This is *not evidence* that Dungeon Difficulty caused that stall. Prior removed-zombie readd warnings and `Failed to fetch a mob spawner` string do not occur in this log, but absence is not equivalent to coverage.

## Source-level verified diagnostic fork

Dungeon Difficulty's `EntityScaling.scale` resolves native `PatternMatching.LocationData.create(world, mob.blockPosition())`, which enumerates **structure starts referenced by the mob's current chunk** and filters by **the start's bounding box containing the exact mob position**. Its `Zone.Filters.structure` must therefore match both the registered `dungeoncrawl:dungeon` ID *and* in-bounds position. If no zone resolves, native mixin records `dd_scaled = 0`, `dd_evaluated_in = minecraft:overworld`. Otherwise `dd_scaled` is positive. AO's late retry still calls this native algorithm; retry cannot force a zone match when bounding boxes/reference coverage are missing.

Dungeon Crawl 2.3.17 is a genuine vanilla `Structure` (`dungeoncrawl:dungeon`, stage UNDERGROUND_STRUCTURES), with many individual pieces. `/locate` works as shown. Its particular piece/start bounding extents at a mob position remain unverified. The mod may spawn ordinary `minecraft:zombie` or `minecraft:skeleton` in spawners; vanilla armor/equipment **does not change entity type eligibility**. They are already whitelisted for AO DD config.

Original Dungeon Difficulty `LivingEntityMixin` serializes `dd_scaled` and `dd_evaluated_in` to entity NBT. **Use these before any additional blind damage/health buffs.**

## Minimum in-game probes, same current v0.4.2 import — no new ZIP needed

1. Stand beside a freshly spawned ordinary skeleton in the *interior of a newly generated Dungeon Crawl*, while cheats enabled. Run:
   - `/data get entity @e[type=minecraft:skeleton,sort=nearest,limit=1] dd_scaled`
   - `/data get entity @e[type=minecraft:skeleton,sort=nearest,limit=1] dd_evaluated_in`
   - `/attribute @e[type=minecraft:skeleton,sort=nearest,limit=1] minecraft:generic.max_health get`
2. Repeat for the buffed skeleton in Keep Kayra, and optionally a normal Overworld skeleton outside structures. Different `dd_scaled` 0 vs >0 isolates zone matching from per-entity attribute bugs. `Health` vs `max_health` differentiates 2-current-HP wounded/low-current-health entities from wrongly calculated maximum.
3. If all Dungeon Crawl skeletons have `dd_scaled=0` and Keep Kayra has 3, next engineering repair should instrument exact structure-reference and bounding-box detection per mob, or apply a **source-identified Dungeon Crawl spawner-origin marker**, never global underground buffs. If DD>0 but max_health unchanged, check attribute modifier ID/operation and whether the relevant attribute exists; do not guess.
4. Ask user to upload **effective** `config/dungeon_difficulty/difficulty_v2.json` from this actual CurseForge instance to confirm the config loader didn't sanitize away the six zones (the user log doesn't print it).
5. Mobs with health bars may be from other elite/healthbar mods; do not equate those with DD scaling without NBT evidence.

## Engineering safety

The already user-validated spellstone Curios patch should remain unchanged. Preserve the exact 330 project pins and all prior recipes, worldgen and UI repairs. Keep additional Dungeon Crawl tuning staged until test yields zone evidence. Any runtime probe addon should be read-only, rate-limited and use a new branch. Never tag all nearby underground hostiles, remove native dungeon gear or rescale already persistently scaled mobs.
