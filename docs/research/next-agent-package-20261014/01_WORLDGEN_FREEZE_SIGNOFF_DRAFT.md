# Worldgen freeze sign-off: DRAFT, **NOT SIGNED OFF**

**Date:** 14 October 2026 · **Scope:** every planned Tier 6 to 9 boss of the boss-balancing handoff · **Evidence:** static only. **No arena has been verified in game.**

**Pregeneration plan (owner): Overworld first; Nether, End and modded dimensions later.** Only the Phase 1 rows below block the first pregeneration.

## 1. Where this stands

- Inventory: **34 rows** (`BOSS_ARENA_INVENTORY_T6_T9.csv`): 25 with an arena whose structure id exists in the current jars but is not verified in game, 5 with an arena not yet identified, 3 summoned by a ritual (no arena; jar inspected), **none blocked**, 1 waiting for an owner decision.
- **Phase 1 (Overworld, or dimension still unknown): 16 rows.** Later (Nether, End, modded dimension): 9. Ritual-summoned (not worldgen-dependent): 3. Bosses with no arena identified yet: 6.
- Arena structure ids checked against the **current** jar scan: **30**; present: **30**.
- Installed versions match the scanned jars for every source mod. **Remnant Bosses 2.7.0 and Eternal Starlight 0.9.1 were uploaded and inspected directly** (`evidence/remnant_bosses_2.7.0_inspection.md`, `evidence/eternalstarlight_0.9.1_inspection.md`), because the scan was stale or missing for them.
- In-game check prepared: `AOA-arena-locate-datapack.zip`: `/function aoa:start` = 87 read-only Overworld searches (phase 1), `/function aoa:start_other` = 28 Nether and End searches (later), with vanilla controls. **Not run yet.**
- **Repairs made: none.** No arena has been *proven* broken or missing, and this task allows repairing only proven problems.

## 2. Owner decisions applied on 14 October 2026

- Third Tier 9 boss: **Obsidilith** (`bosses_of_mass_destruction:obsidilith`; End arena, so not a phase 1 item).
- **Ignis, Maledictus and Leviathan are Tier 8** (the older Tier 7 placement is superseded).
- **Mother of Maze is not a boss** (an ordinary mob): removed from the inventory.
- **Geburah: TBD**, leave for later (owner's final word; an earlier remark had said Tier 6). Its arena is an End structure in the Test 5 and v3 catalogues.
- **Ancient Remnant:** the entity `cataclysm:ancient_remnant` is fine; it only needs a special interaction to appear, and its stats should edit like the other Cataclysm bosses (health was measured at 450; damage needs the interaction).
- **Pregeneration starts with the Overworld only.**

## 3. Phase 1: boss sites in or possibly in the Overworld

| # | Tier | Boss | Mod | Arena | Dimension | Spawn mechanism | Status |
|---:|---|---|---|---|---|---|---|
| 1 | 6 | Dead King | Iron's Spells | irons_spellbooks:catacombs (INFERRED) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 5 | 6 | Kobolediator | Cataclysm | cataclysm:kobolediator_shrine (ROSTER) | Overworld | GENERATION | STATIC ONLY: structure id present, not verified in game |
| 6 | 6 | Eternal Starlight: The Gatekeeper | Eternal Starlight | eternal_starlight:portal_ruins_common; eternal_starlight:portal_ruins_cold; eternal_starlight:portal_ruins_desert; eternal_starlight:portal_ruins_forest; eternal_starlight:portal_ruins_jungle (JAR) | Overworld | GENERATION | STATIC ONLY: structure id present, not verified in game |
| 11 | 6 | Underground dragons (fire, ice, lightning) | Ice and Fire | iceandfire:fire_dragon_cave; iceandfire:ice_dragon_cave; iceandfire:lightning_dragon_cave (INFERRED) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 13 | 7 | Ancient Remnant | Cataclysm | cataclysm:cursed_pyramid (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 16 | 7 | Ice and Fire Hydra | Ice and Fire | iceandfire:hydra_cave (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 19 | 7 | Chesed | F.D. Bosses | fdbosses:chesed_arena (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 20 | 7 | Malkuth | F.D. Bosses | fdbosses:malkuth_arena (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 23 | 8 | Maledictus | Cataclysm | cataclysm:frosted_prison (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 24 | 8 | The Leviathan | Cataclysm | cataclysm:sunken_city (ROSTER) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 25 | 8 | Bosses'Rise: Sandworm | Bosses'Rise (jar block_factorys_bosses) | block_factorys_bosses:sandworm_nest (INFERRED) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 26 | 8 | Bosses'Rise: Yeti | Bosses'Rise (jar block_factorys_bosses) | block_factorys_bosses:yeti_hideout (INFERRED) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 27 | 8 | Bosses'Rise: Infernal Dragon | Bosses'Rise (jar block_factorys_bosses) | block_factorys_bosses:dragon_tower (INFERRED) | Overworld | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 29 | 8 | Bosses'Rise: Kraken | Bosses'Rise (jar block_factorys_bosses) | block_factorys_bosses:kraken_ship (INFERRED) | Overworld / ocean | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 31 | 8 | Last of Deepslate | Archaion | archaion:ancient_keep (INFERRED) | UNKNOWN (structure is in neither the Test 5 nor the v3 catalogue) | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 33 | 9 | Scylla | Cataclysm | cataclysm:acropolis (ROSTER) | Other/undetermined | GENERATION | STATIC ONLY: structure id present, not verified in game |

## 4. Later: Nether, End and modded dimensions (not in a hurry)

| # | Tier | Boss | Mod | Arena | Dimension | Spawn mechanism | Status |
|---:|---|---|---|---|---|---|---|
| 7 | 6 | Eternal Starlight: Starlight Golem | Eternal Starlight | eternal_starlight:golem_forge (JAR) | Eternal Starlight dimension (eternal_starlight:starlight) | GENERATION | STATIC ONLY: structure id present, not verified in game |
| 8 | 6 | Eternal Starlight: Permafrost | Eternal Starlight | eternal_starlight:golem_forge (JAR) | Eternal Starlight dimension (eternal_starlight:starlight) | GENERATION | STATIC ONLY: structure id present, not verified in game |
| 9 | 6 | Eternal Starlight: Lunar Monstrosity | Eternal Starlight | eternal_starlight:cursed_garden (INFERRED) | Eternal Starlight dimension (eternal_starlight:starlight) | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 12 | 7 | Netherite Monstrosity | Cataclysm | cataclysm:soul_black_smith (INFERRED) | Nether | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 14 | 7 | Ender Guardian | Cataclysm | cataclysm:ruined_citadel (ROSTER) | The End | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 21 | TBD | Geburah | F.D. Bosses | fdbosses:geburah_arena (ROSTER) | The End | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 22 | 8 | Ignis | Cataclysm | cataclysm:burning_arena (ROSTER) | Nether | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 28 | 8 | Bosses'Rise: Underworld Knight | Bosses'Rise (jar block_factorys_bosses) | block_factorys_bosses:underworld_arena (INFERRED) | Nether | UNKNOWN | STATIC ONLY: structure id present, not verified in game |
| 34 | 9 | Obsidilith | Bosses of Mass Destruction | bosses_of_mass_destruction:obsidilith_arena (OWNER) | The End | UNKNOWN | STATIC ONLY: structure id present, not verified in game |

## 5. Summoned by a ritual: no arena, not worldgen-dependent

| # | Tier | Boss | Mod | Arena | Dimension | Spawn mechanism | Status |
|---:|---|---|---|---|---|---|---|
| 17 | 7 | Ossukage | Remnant Bosses | - (NONE:) | - | RITUAL | NO ARENA NEEDED: ritual summon (jar inspected) |
| 18 | 7 | Kotsukage | Remnant Bosses | - (NONE:) | - | RITUAL | NO ARENA NEEDED: ritual summon (jar inspected) |
| 30 | 8 | Umbrakar | Remnant Bosses | - (NONE:) | - | RITUAL | NO ARENA NEEDED: ritual summon (jar inspected) |

Remnant Bosses 2.7.0 contains **no worldgen data at all**. Each boss is summoned at a crafted Ancient Altar with an activation item and four pedestal offerings, and every stat and ability damage is a native config key (`config/remnant/bosses/`). The materials still come from the world: Ossukage needs a Nether Star, Kotsukage a wither skeleton skull and Nether blocks, **Umbrakar an echo shard and sculk (Ancient City / Deep Dark, Overworld) and end stone (the End)**.

## 5b. Bosses with no arena identified

| # | Tier | Boss | Mod | Arena | Dimension | Spawn mechanism | Status |
|---:|---|---|---|---|---|---|---|
| 2 | 6 | Comparable strong T6 boss (unnamed) | unselected | - (UNASSIGNED) | - | n/a | DECISION NEEDED |
| 3 | 6 | Ignited Revenant | Cataclysm | - (UNKNOWN) | - | UNKNOWN | ARENA UNKNOWN |
| 4 | 6 | Coralssus | Cataclysm | - (UNKNOWN) | - | GENERATION | ARENA UNKNOWN |
| 10 | 6 | Captain Cornelia | Aquamirae | - (UNKNOWN) | - | UNKNOWN | ARENA UNKNOWN |
| 15 | 7 | Ender Golem | Cataclysm | - (UNKNOWN) | - | UNKNOWN | ARENA UNKNOWN |
| 32 | 9 | Tyros | Iron's Spells | - (UNKNOWN) | - | UNKNOWN | ARENA UNKNOWN |

Arena basis: ROSTER = named by the owner's roster; INFERRED = matched by name or template, to be confirmed; OWNER DECISION = chosen by the owner; UNKNOWN = no arena identified. Spawn mechanism is GENERATION only where the jar ships a single-mob template for that boss; everything else is UNKNOWN until jar code or an in-game encounter says otherwise.

## 6. Findings that could become worldgen blockers (to be decided by the in-game check)

1. **Original and Integrated variants of the same arena (63 collisions).** Cataclysm (3.33) and `integrated_cataclysm` (1.0.6) both define the structures, sets and template pools of ancient_factory, burning_arena, cursed_pyramid, frosted_prison, ruined_citadel, soul_black_smith and sunken_city; BOMD and IBOMD do the same for obsidilith_arena, lich_tower and gauntlet_arena. The Test 5 snapshot picks the Integrated variant, the handoff says to keep the Integrated arenas, but **runtime precedence has never been verified.** Cheap check: `/datapack list enabled` and read the order of `mod/integrated_cataclysm` against `mod/cataclysm` (the later one wins).
2. **Scylla (Tier 9):** `cataclysm:acropolis` exists in the jar and a `cataclysm:scylla` template places her, but the Acropolis is **missing from the v3 structure catalogue**, its dimension is undetermined and it counted **0 curated Overworld biomes** in Test 5 (zero can also mean an unresolved tag). If `/locate` cannot find it from any origin, this is the most serious phase 1 blocker.
3. **Low eligibility:** `cataclysm:frosted_prison` (Maledictus) and `fdbosses:malkuth_arena` each counted only **1** curated Overworld biome in Test 5, and Malkuth's spacing is 100/80 (rare).
4. **Last of Deepslate:** `archaion:ancient_keep` is in neither catalogue (Archaion is a new addition), so its dimension and biome rules are unknown. `start` searches the Overworld, `start_other` the Nether and End.
5. **Eternal Starlight 0.9.1 (read from the jar):** its boss structures (`golem_forge` with the Starlight Golem and Permafrost, `cursed_garden`) generate **only in its own dimension**, so they are not part of the Overworld pregeneration. **The Gatekeeper's arena is the five `portal_ruins_*` structures, which generate in the Overworld** (phase 1). They are very likely the entrance to the whole dimension (portal block `starlight_portal`; not verified in game), so every Eternal Starlight boss depends on them, **and AO loosened their spacing from 36/30 to 45/32.** The Lunar Monstrosity's arena is an inference (its spawner block is in no template). **Remnant Bosses 2.7.0 is resolved**: ritual-summoned, no arena (section 5).
5a. **Eternal Starlight boss respawn is on:** `enableBossRespawn` true, `bossRespawnCooldown` 36000 ticks (30 minutes). From the class constants (not run in game): when a boss dies, its **spawner block** gets that cooldown and can produce the boss again, and every kill rolls the boss loot table, so each respawn is another reward roll. Config only: it does not affect worldgen and can be changed after pregeneration.
5b. **Umbrakar's ritual depends on the Overworld generating an Ancient City** (echo shard, sculk). `/function aoa:start` therefore also searches `minecraft:ancient_city`.
6. **Arenas not identified:** Tyros (`irons_spellbooks:fire_boss`; only Nether candidates exist), Captain Cornelia, Ender Golem, Ignited Revenant and Coralssus (templates exist, the placing structure is unknown).
7. **Never measured in any AOT run (5):** `cataclysm:ender_golem`, `cataclysm:ignited_revenant`, `cataclysm:coralssus`, `cataclysm:kobolediator`, `iceandfire:hydra`. **Measured for health but interaction-locked for damage (4):** `eternal_starlight:the_gatekeeper` (175), `eternal_starlight:starlight_golem` (200), `cataclysm:ancient_remnant` (450, capped when raised) and `block_factorys_bosses:yeti` (250).
8. **Bosses'Rise is the same jar as Block Factory's Bosses** (`block_factorys_bosses-2.1.2`, display name Bosses'Rise). The roster note 'do not conflate' is wrong; the five Tier 8 bosses are Sandworm, Yeti, Infernal Dragon, Underworld Knight and Kraken.
9. **Test 5 data is historical:** dimension, biome counts and placement come from the Test 5 scan and AO's later configs may differ.

## 7. Still to decide

- The roster's unnamed 'comparable strong Tier 6 boss' stays open (Geburah is TBD and does not fill it); it must not be invented.
- **Which Eternal Starlight bosses are the Tier 6 family?** TBD; the owner says it can wait (Eternal Starlight is not in the first pregeneration, except the Gatekeeper's Overworld ruins). The inventory lists the four real bosses (Gatekeeper 175 HP, Starlight Golem 200, Permafrost 120, Lunar Monstrosity 200); Tangled is an ordinary mob.
- **Eternal Starlight boss respawn (open, not urgent):** keep the 30-minute respawn, lengthen it, or disable it. It is a reward-economy question and a config change that can be made after pregeneration.
- Brutal Bosses: spawn chance 70, spacing 30, boss files and spawn tables are baked at generation (see `BRUTAL_BOSSES_FINDINGS.md`, section 13); they must be final before the Overworld pregeneration.

## 8. What is needed to sign off Phase 1 (Overworld)

1. `/datapack list enabled` and send the output (collision precedence, finding 1).
2. Run `/function aoa:start` in the **final AO world preset** and send the log (`ARENA_CHECK_GUIDE.md`). Every `NOT FOUND` then needs the manual registry check in the guide.
3. Walk to each located Overworld arena and record how the boss appears (guide, section 3).
4. Optionally upload `L_Ender's Cataclysm 1.21.1-3.33.jar` and `irons_spellbooks-1.21.1-3.16.3.jar`: they would close the unknown arenas (Tyros, Ender Golem, Ignited Revenant, Coralssus) by static analysis. No other jar is needed.
5. Repair **only** what steps 1 to 4 prove broken (missing structure registration, template references, generation-dependent spawners), then re-run.
6. Sign off: every phase 1 row is either LOCATED with a recorded encounter, or listed as a known limitation. Phase 2 (`start_other`) follows later.

