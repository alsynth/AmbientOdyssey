# Quest authoring, validation and release plan

**Status:** planned pipeline, NOT executed. `QUEST_CONTENT_SEEDS.csv` is descriptive content mapping, not complete Questlog JSON.

## Work batches in ascending risk

| Batch | Deliverable | Rough scope | Minimum verification |
|---|---|---:|---|
| Q0 | Reconcile actual Test8.3 installed mod IDs, compile accurate resource registries, test Questlog/FTB installation on cloned instance | Data/build tools | Exact runtime, no missing dependencies |
| Q1 | Create first 12–15 beginner Questlog quests and 8–12 FTB reference pages | Beginner tutorial | 2 inexperienced testers; JEI and item IDs accurate, rewards not doubled |
| Q2 | Tier 0–2 main campaign through enchanted diamond + two A-grade supports | 25–40 quests | Equipment milestones achievable from different weapon/magic options |
| Q3 | Explorer's Atlas: 2 vanilla + 2 modded biome/structure triggers and initial journal | 8–20 quests | Natural entry (not `/locate`), stable progress, multiple modded biomes |
| Q4 | Two pilot optional chapters: Frozen Seas / Aquamirae and first Alex's Caves expedition | 12–30 quests | Exact 1.21.1 entity/structure IDs, boss reward/credit |
| Q5 | **NeoPasterDream 0.9.6 full source/content audit** then Dreamseeker campaign prototype | 20–45 validated quests | Every realm/item/puzzle/encounter exists and works in this version; unfinished bits skipped |
| Q6 | **Enigmatic Legacy Plus normal vs cursed independent routes** | 16–35 validated quests | One uncursed player and one voluntary cursed player can each finish own optional path |
| Q7 | Main realm campaigns: Aether, Twilight Forest, Eternal Starlight, Undergarden, Deeper and Darker, Bumblezone | 100–180 quests | Boss order, portal mechanisms and multiplayer progression evidence |
| Q8 | Magic and equipment mastery sidequests, with comprehensive FTB manuals | 60–120 Questlog + 80+ FTB pages | Spell/artifact/loot version accuracy, Origin compatibility and budget |
| Q9 | Complete AO boss atlas, endgame calibration, missing medium-size content, long-term website integration | 100–200 quests | Tier 2–8 balance, rewards and player group tests |

**Numbers are scheduling bands, not precommitted quest count or proof 1000 quests is better than 600.** It is reasonable for the eventual registry to exceed 1000 content entries, but fewer meaningful quests are preferable to repetitive/fake progression.

## Content source registry (proposal)

A future authoring table/JSON record should contain:
- `id`, `chapter_id`, `pack_version_min`, `difficulty_tier`, `lane` and `source_mod_ids`.
- `title`, `description`, `objective_hint`, `spoiler_level`, `category`, `icon_source`.
- `unlock_conditions`, `requirements`, `completed_conditions`, `optional`, `repeatable`, `failure_policy`.
- `questlog_objective_json` **only after real IDs verified**; `ftb_reference_pages` for detailed learning; `reward` and `reward_once_key`.
- `required_gear_band`, `optional_origin_constraint` (usually none), `known_issues`, `test_case`, `status`.
- `reward_policy`: cosmetic, lore, a few useful resources, balanced alternate gear, XP in moderation; not a source of endless endgame affix/gem equipment.
- `validation_state`: `idea`, `identifier_verified`, `logic_implemented`, `static_validated`, `runtime_singleplayer`, `runtime_dedicated_2player`, `released`.

## Questlog objective mechanics: constraints discovered

- Current Questlog 3.4.x uses `config/questlog/quests/*.json` and `config/questlog/chapters/*.json`, not the original outdated README claim of ordinary datapack quests.
- Use `prerequisites` for current canonical version; older documentation sometimes still shows `requirements`; create a 3.4.1-generated specimen in the editor and validate version-specific serialization.
- `visit_structure` checks a player inside a registered **structure piece**, not generic proximity to a building guessed from its name; not every generated structure/feature has such an ID. `visit_biome` and `visit_structure` don't accept biome/structure tags per official docs.
- `entity_kill` needs a *correct* mob ID and attribution: if a boss is killed by another player, summon/minion or weapon effect, per-player completion may differ. Test group damage credit and fallback quest logic rather than using fabricated goals.
- `origin` objective uses the IAFEnvoy Origins mod API in NeoForge source, not presumed CyberDay NeoOrigins.
- Several hundred active polling `visit_structure`/biome tasks could be expensive; only activate relevant quests and benchmark real server TPS. Source-level suspicion is NOT a measured regression.
- Questlog's player data uses `<UUID>.questlog.dat` in world playerdata with a backup; save migration, player respawn and simultaneous FTB Solo Quests still need live tests.
- Avoid reward duplication when Questlog + FTB manual both track one tutorial. Cosmetic achievements can be recorded silently with vanilla advancements; one engine gives the tangible reward.
- Each quest needs a *failure-safe*: if a boss is absent in the exact mod version, automatically hide or omit the quest at build time, don't allow permanently unfinishable journal entries.

## Static validator design

Build a generator and CI check that:
1. Checks unique quest IDs, chapter existence and no dependency cycles.
2. Validates every referenced item/entity/structure/biome/dimension against a captured 1.21.1 registry dump; flag unresolvable IDs.
3. Flags physically unobtainable loot / command-only items / recipes disabled by Paxi or KubeJS.
4. Warns of mandatory quests requiring one Origin, one irreversible curse, a rare random structure with no alternative, or a route declared optional.
5. Verifies no duplicate rewards or infinite repeats that generate unique boss drops, currency or XP.
6. Verifies chapters are not dumped into the visible initial journal all at once.
7. Verifies localization and resource pack icons (permissions, missing textures, fallback).
8. Performs offline JSON schema parse and Questlog 3.4.1 structure checks, then *separate* runtime acceptance. Do not fake successful gameplay.

## First concrete pilot outlines

**Quest 1 — The First Pages:** `questlog:read` to acknowledge short explanation (test whether read requirement must be explicitly completed), or a safe follow-up with `item_obtain minecraft:crafting_table`. Reward a modest starter utility once. FTB page demonstrates JEI.

**Quest 2 — Your First Distant Landmark:** `questlog:visit_structure` bound to an actually registered, common AO structure ID confirmed from a fresh generated world. On completion, unlock an optional preparation note but no giant loot reward.

**Quest 3 — Prepared for Tier 2:** Item and equipment predicates must check *full armor enchantments* plus **two compatible A-grade combat supports**. Questlog's `item_equip` only explicitly documents mainhand/offhand/head/chest/legs/feet, NOT arbitrary Curios slots; design a reliable advancement/command/Curios bridge before marking this objective automated. **Do not substitute mere possession of one item as proof of the full gear condition.**

**Quest 4 — Frozen Seas, first encounter:** `visit_biome` for an exact installed Aquamirae frozen ocean, `visit_structure` for a verified Ice Maze ID, otherwise explicit custom action only after confirmed integration. Separate finishing Cornelia later so low-tier explorers can safely discover her place.

**Quest 5 — Optional Seven Curses:** Do not grant curse by quest reward or by a click-to-complete tutorial. Detect actual ring-equipped cursed state with a suitable reliable predicate, gated behind an explicit warning and user choice. The normal Enigmatic route must stay completable without it.

## Beginner QA

- New to Minecraft, never played mods: can find **how to use JEI, inventory, shield, waypoint and manual**.
- New to AO but has played Minecraft: can skip repetitive movement/crafting explanation and enter the first dungeon quest quickly.
- 2 players with different goals: personal Boss and Origin quests don't unexpectedly synchronize.
- A player who discovers an endgame ruin very early: gets a *warning* but no forced abandonment or impossible quest.
- A player who wants only to explore/farm/build: can ignore the optional boss, curse, magic and tech chapters without spoiling the main story.

## Later site integration

Publish static guide pages generated from the same content registry, including mod/version, quest descriptions, gear requirements, verified mob/structure names, tips, and non-spoiler alternative paths. Player progress sync requires explicit opt-in and should not expose UUID/coordinates by default.

**Current state:** no generated quest JSON, no Questlog installed or tested, no modlist or release altered.
