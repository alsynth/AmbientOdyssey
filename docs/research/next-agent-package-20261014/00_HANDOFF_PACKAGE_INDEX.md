# Boss balancing: package index and owner decision ledger (14 October 2026)

For the agent taking over the boss-balancing work. This file replaces the chat: every decision the owner made is listed here, then the files to read, then what is **not** done. Read it first.
Reference you already have: the boss-balancing handoff (tiers 1 to 9, deliverables, scope control) and PRs #44, #50, #53, #56, issues #43 and #55.

## 1. Owner decisions (binding unless marked otherwise)
**Tiers and roster**
- Tier 9: **Tyros, Scylla and Obsidilith** (Obsidilith is the third; the End slot is closed).
- **Ignis, Maledictus and Leviathan are Tier 8** (the older Tier 7 placement is superseded).
- **Geburah: TBD**, leave for later (the owner's final word; an earlier remark had said Tier 6). Its arena is an End structure.
- **Mother of Maze is not a boss** (an ordinary mob). Removed.
- **Ancient Remnant:** the entity `cataclysm:ancient_remnant` is fine; it only needs a special interaction to appear; its stats should edit like the other Cataclysm bosses (health was measured: 450, capped at 1024; damage needs the interaction).
- All Cataclysm bosses are assumed to be configurable the same way.
- **Bosses'Rise is the same jar as Block Factory's Bosses** (fact, not a decision): `block_factorys_bosses-2.1.2`.
- **Remnant Bosses 2.7.0 was inspected directly (fact):** Ossukage, Kotsukage and Umbrakar are summoned by a ritual at a crafted altar, need **no arena**, and every stat and ability damage is a native config key in `config/remnant/bosses/`. Not worldgen-dependent, but Umbrakar's ritual needs an echo shard and sculk, so the Overworld must generate an Ancient City.
- **Eternal Starlight 0.9.1 was inspected directly (fact):** its boss structures exist only in its own dimension; **The Gatekeeper's arena is the Overworld portal ruins (phase 1)**, which very likely gate entry to the whole dimension, and AO loosened their spacing from 36/30 to 45/32. Natively configurable (Gatekeeper 175 HP, Starlight Golem 200, Permafrost 120, Lunar Monstrosity 200). Boss respawn is on (30 min cooldown). Tangled is an ordinary mob.

**Worldgen**
- **Pregeneration starts with the Overworld only**; Nether, End and modded dimensions come later.
- Anything that changes world generation must be final before that pregeneration.

**Brutal Bosses**
- `globalBossSpawnChance` **30 to 70** and `minDistance` **100 to 30** (ready file `brutalbosses.json`, comments and line endings kept). Baked at generation: do before pregeneration.
- Coverage (about 12% of AO chest tables) is **accepted**; the dummy boss dilution is **accepted**; Dungeon Difficulty also scaling these bosses is **accepted**. Do not edit boss files or spawn tables.
- Set `damageMultiplier` and `healthMultiplier` to the **same** value. The factor is **not decided** (x3 is only a placeholder). Owner check: both at 10 gave a 1000 HP zombie boss with damage scaled too.

**Scylla and boss editability**
- Scylla's **wave is let go** (no lever exists; not necessarily a damage spell).
- Boss health is capped at **1024**. Options for tougher bosses: armor (AO uses the formula `a / (a + armor)`), resistance and absorption effects, or a **damage-scaling addon that the owner will do later** (it touches no worldgen and can be added after pregeneration).
- Apotheosis tuning and the Sky Arena entries are **out of scope**. The Origins idea is **scrapped**.

**Economy**
- The economy to work on first is **loot and reward**. Boss rewards are authored per encounter, never rolled from ordinary chests.

## 2. Still open (do not decide for the owner)
- The roster's unnamed "comparable strong Tier 6 boss" slot stays open (Geburah is TBD and does not fill it) and must not be invented.
- Eternal Starlight: which bosses are the Tier 6 family (**TBD, the owner says it can wait**), and the boss respawn setting (30 minutes today; when a boss dies its spawner block can spawn it again and each kill rolls the loot table; config only, changeable after pregeneration).
- Reward pacing numbers (nothing approved), what to do while the Apotheotic port is a prototype (Artifact, Heirloom and Esoteric have zero natural drop weights), and which Tier 7 Nether boss carries the Rage Glove (proposal: Netherite Monstrosity).
- The Brutal Bosses global factor.

## 3. Files to hand over, in reading order
**Essential**
1. `00_HANDOFF_PACKAGE_INDEX` (this file)
2. `01_WORLDGEN_FREEZE_SIGNOFF_DRAFT.md`: status of every Tier 6 to 9 boss site, the findings that could block pregeneration, what is needed to sign off. **Not signed off.**
3. `02_BOSS_ARENA_INVENTORY_T6_T9.csv`: the machine-readable version (34 rows, every claim labelled by evidence).
4. `03_ARENA_CHECK_GUIDE.md` and `04_ENCOUNTER_RESULTS_TEMPLATE.csv`: how the owner verifies the arenas in game.
5. `05_BRUTAL_BOSSES_FINDINGS.md` and `06_brutalbosses.json`.
6. `07_AOT_CONFIGURABILITY.csv` and `08_AOT_merged_results.csv`: for each tested boss, which route changes its health and damage, with the measured numbers.
7. `09_AOT_SCYLLA_FIELD_GUIDE.md`, `10_AOT_SCYLLA_ABILITY_TEST.md`, `11_AOT_FOCUS_DOSSIER.md`: Scylla, Tyros and Obsidilith in detail.
8. `12_BOSS_REWARD_ROUTING_BASELINE.md`: where the reward work stands.
9. `13_V05_BOSS_DUNGEON_LOOT_CAPABILITY_CATALOGUE.md` and `14_V05_CAPABILITY_MATRIX.csv`: what each boss mod allows (health, damage, loot, spawn).
10. `15_REMNANT_BOSSES_2.7.0_INSPECTION.md` and `16_ETERNAL_STARLIGHT_0.9.1_INSPECTION.md`: what the two jars contain and the live boss values.

11. **The handoff's own deliverable documents (built 14 Oct, none applies a balance value):** `17_BOSS_BALANCE_LEDGER_T6_T9.csv`, `18_PROGRESSION_CONSISTENCY_REPORT.md`, `19_COMPATIBILITY_EVIDENCE.md`, `20_TEST_BUILD_AND_ROLLBACK.md`, `21_REMAINING_BLOCKERS_AND_OWNER_DECISIONS.md`, and the folder `rollback-baseline/` (39 byte-exact boss config files with SHA-256 hashes).

**Tools (only if they will verify or measure)**
- `tools/AOA-arena-locate-datapack.zip` and `tools/aoa_parse_locate.py` (arena check), `tools/AOT-edit-test-datapack.zip`, `tools/AOT-edit-test-guide.md` and `tools/aot_parse_log.py` (boss stat measurements).

**Do not hand over:** raw game logs, per-run result files, the Origins material, the `jar-scan` data (it is in the repository if needed), and older copies of any file above.

## 3b. Handoff deliverables against this package
| Handoff deliverable | File | State |
|---|---|---|
| 1. Implementation package | none | **not started**: no balance value applied (waits on a player-power reference per tier) |
| 2. Boss-by-boss ledger | 17 | **built**: 35 rows, baselines, edit routes, live config keys; the changed-values columns are empty |
| 3. Progression consistency report | 18 | **draft** of the native ordering; no target model yet |
| 4. Compatibility evidence | 19 | **built** (static); Apotheosis affix interactions, party wipes and performance not assessed |
| 5. Test build and rollback | 20 + `rollback-baseline/` | rollback baseline **exists**; no experimental build yet |
| 6. Blockers and owner decisions | 21 (+ 01) | **built** |

## 4. What is and is not done
| Area | State |
|---|---|
| Boss and arena inventory | done (static evidence only) |
| Arena verification in game | **not run**; datapack and guide ready |
| Remnant Bosses 2.7.0 | **inspected**; no arena needed |
| Eternal Starlight 0.9.1 | **inspected**; no blocked rows remain |
| Worldgen blocker repairs | **none made** (nothing proven broken) |
| Worldgen freeze sign-off | **draft, not signed off** |
| Boss stat editing | measured for 55 bosses (5 of the Tier 6 to 9 bosses never measured, 4 interaction-locked for damage); **no balance values applied** |
| Brutal Bosses changes | decided, to be implemented by the owner's agent |
| Loot and reward | baseline written; no numbers approved; nothing implemented |
| Damage-scaling addon | not built (deferred by the owner) |
