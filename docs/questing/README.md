# Ambient Odyssey — Quest Content Mapping Project

**Planning iteration:** 10 October 2026 · **Current active branch:** `structure/test6` · **Minecraft:** 1.21.1 NeoForge · **Status:** initial narrative and content audit, not in-game authored quests.

## Writing pass v0.2 — 10 October 2026

**Quest copy now exists, beyond the original content map.** This is still a planned, not installed, questbook.

| Added file | Current content |
|---|---|
| [WRITTEN_QUEST_DRAFTS_V0_2.md](WRITTEN_QUEST_DRAFTS_V0_2.md) | **50 fully written Questlog-style narrative drafts** across early tiers and selected optional branches; original titles, descriptions, objectives, hints and verification concerns |
| [WRITTEN_QUEST_DRAFTS_V0_2.json](WRITTEN_QUEST_DRAFTS_V0_2.json) | Machine-readable versions of the same 50 records, using the **pre-existing quest seed IDs** so later revisions don't discard the content map |
| [FTB_FIELD_MANUAL_DRAFT_PAGES_V0_2.md](FTB_FIELD_MANUAL_DRAFT_PAGES_V0_2.md) | **14 original educational article drafts** for beginner play, JEI, combat/Curios, Waystones/Lootr, Apotheosis, Relics, Iron's Spells, Ars, PasterDream and Enigmatic Legacy |
| [VERSION_PINNED_CONTENT_LEADS_2026-10-10.md](VERSION_PINNED_CONTENT_LEADS_2026-10-10.md) | Upstream **NeoPasterDream 0.9.6** documented garden puzzles/Cold Domain/Aaroncos and **Enigmatic Legacy Plus 1.1.2** named item research, with exact-version uncertainty tagged |
| [POST_EXPANSION_RECONCILIATION_PROTOCOL.md](POST_EXPANSION_RECONCILIATION_PROTOCOL.md) | Procedure for updating quests after mod additions/updates and preserving published IDs, player progress, reward claims and natural achievement feasibility |

**Status:** prose is *draft_copy*. Questlog objective JSON, FTB SNBT pages, tested triggers, approved rewards and release installation still **do not exist** for these drafts. The modpack's future content expansion must be reconciled against real item/structure/boss registries before implementing them.

## Depth review v0.3 — 10 October 2026

**Triple-pass quest-size and mod-complexity audit completed from the current available source inventory; exact final client JAR registry reconciliation remains pending after the content expansion.** This audit keeps the existing 474 seed IDs and 50 written drafts unchanged.

| File | Contents |
|---|---|
| [QUEST_DEPTH_REVIEW_REPORT_2026-10-10.md](QUEST_DEPTH_REVIEW_REPORT_2026-10-10.md) | Narrative of three checks (mod priority, actual deep mod systems, quest technical feasibility), changes and version-pinned source links |
| [MOD_DEPTH_REAUDIT_2026-10-10.csv](MOD_DEPTH_REAUDIT_2026-10-10.csv) | **265-record** follow-up with depth decisions and editor targets; names and source evidence are still provisional |
| [QUEST_DEPTH_SUPPLEMENT_V0_3.csv](QUEST_DEPTH_SUPPLEMENT_V0_3.csv) | **250 additional system-specific quest ideas** across 19 chapter/subject tracks. Includes PasterDream flower puzzles, Starlight native systems, Bumblezone's peaceful Bee Queen, End Remastered eye-source paths, Opposing Force post-Nether/Post-End spawns and more. **Overlaps with existing seeds must be merged.** |
| [QUEST_CAMPAIGN_ARCHITECTURE.md](QUEST_CAMPAIGN_ARCHITECTURE.md) | Updated optional-campaign depth ranges reflecting complex content rather than mod name or visual size |

**Planning quantity:** 474 broad seed beats + 250 supplementary leads, **not 724 unique or completed quests**. Still 50 written Questlog narrative drafts and 14 written FTB manual articles. None of the new leads have live quest JSON, item/structure IDs, approved rewards or successful multiplayer gameplay validation. The source roster is expected to change after the planned modpack content expansion.

## Current outputs

| File | Scope | State |
|---|---|---|
| [QUEST_CAMPAIGN_ARCHITECTURE.md](QUEST_CAMPAIGN_ARCHITECTURE.md) | Player experience, nine-tier main storyline, independent optional campaigns, beginner-first writing rules and FTB field manual | First blueprint |
| [MOD_QUEST_COVERAGE_MATRIX.csv](MOD_QUEST_COVERAGE_MATRIX.csv) | **265 provisional named mod/extension entries** from historical JAR evidence and active source-lock metadata, with quest priority, chapter placement, sample hook and evidence | Initial classification; **not** an exact current-manifest 1:1 mod list |
| [QUEST_CONTENT_SEEDS.csv](QUEST_CONTENT_SEEDS.csv) | **474 specifically described quest beats, 46 chapter concepts**: 430 gameplay/adventure beats and 44 FTB-reference topic beats | Idea seeds, **NOT implemented JSON, configured tasks or tested rewards** |
| [INVENTORY_METHOD_AND_GAPS.md](INVENTORY_METHOD_AND_GAPS.md) | Source reconciliation, duplicate IDs and mod/JAR verification limits | Read before converting anything |
| [QUEST_AUTHORING_VALIDATION_PLAN.md](QUEST_AUTHORING_VALIDATION_PLAN.md) | Progressive generation plan and acceptance tests for exactly working Questlog quests | Planned work |

The provisional coverage-row count resembles the current approximate CurseForge project-ref count **by coincidence and must not be presented as proof of exact mod-list reconciliation**. Row entries include historical repins, client-logged JAR names, integrations, shaders and explicit libraries. A clean **Test8.3 full runtime mod list** and project-ID data remain necessary to verify every mod. Some historical labels were merged/split manually to avoid losing large addons such as Deep Aether, Seven Seas, More Relics, WDA expansions and dedicated libraries.

## Priorities (provisional)

- **A:** Major, multi-stage Questlog campaign / mechanically substantial dimension / main boss or pivotal gear system.
- **B:** Substantial optional Questlog chapters with meaningful discoveries, fights or items.
- **C:** One-to-few Questlog sidequests / short experiences; typically linked into themed multi-mod anthologies.
- **D:** FTB Quests teaching page(s), rather than a duplicated story progression.
- **E:** Explorer's Journal or biome-region anthologies; no standalone linear chapter needed.
- **I:** Technical integration of content already covered by its parent Questlog chapter.
- **X:** Library, renderer, performance, technical mod, cosmetic: no player-facing quest.
- **?:** Feature verification needed before assigning priority.

### Why Questlog *and* FTB

Questlog is the **Adventure Journal** and plays through discovery, preparation, boss encounters, dimension campaigns and optional character routes. FTB Quests is the **Field Manual** explaining mechanics: JEI recipes, spell schools, Ars glyph composition, Apotheosis enchantment/affix/gem systems, Curios slots, travel tools, advanced crafting and accessibility. Players should not need to complete 100 micro-tasks to learn a recipe. Only one engine owns any given completion reward.

## Mod-specific checkpoints before authoring

- **NeoPasterDream:** Historical pack JAR `pasterdream-0.9.6.jar`; upstream [v0.9.6 changelog](https://www.curseforge.com/minecraft/mc-mods/neopasterdream/files/8639119) explicitly adds Cold Domain and overhauls **Aaroncos** boss mechanics (including a dangerous ultimate) and earlier dream systems. The [current CurseForge description](https://www.curseforge.com/minecraft/mc-mods/neopasterdream) is updated for later versions including 0.10 prereleases and may overstate what 0.9.6 ships. Treat unproven realm/biome/story hooks as **verification first**; do not give players an impossible task.
- **Enigmatic Legacy Plus:** A **normal relic route** and **voluntary cursed route** (Ring of Seven Curses) must never gate each other or the main campaign. The latter may be irreversible and has significant drawbacks; explain consequences before unlock. Current source evidence recorded `enigmaticlegacyplus-1.21.1-1.1.2.jar`; check exact Curios slots, items, condition states, recipes and ring curse toggles.
- **Twilight Forest / Aether / Eternal Starlight / Undergarden:** Major campaigns but inspect exact 1.21.1 port progression, bosses and completion status.
- **Cataclysm / BOMD / Mowzie / Remnant / FD bosses / Ice and Fire:** Use AO-calibrated boss tiers; early discovery may coexist with much-later victories.
- **Worldgen structure mods:** Avoid entire chapters for each minor tower and ruined house. Register major structures for the Explorer's Journal and build a curated anthology with legitimate combat/location goals.
- **Magic / Apotheosis / Relics:** Many complex systems benefit from FTB Field Manual pages alongside a much smaller Questlog mastery track.
- **Create/food/storage:** Optional cameos and technical FTB explanations, not required stops on the adventurer's main path.
- **Upcoming Origins:** Treat class/background/perk branches as future content only once selected backend is tested; Questlog's built-in Origins objective currently targets IAFEnvoy and should not be assumed to detect NeoOrigins.
- **Release/source:** Current `release_030/release-lock.json` has 51 source additions/repins beyond the base manifest plus removals; archive snapshot and audited list are older than Test8.2. Status markers differ intentionally.

## Content standards for a thousand-quest future

Each published quest needs a stable ID, verified actual mod resource ID, exact trigger semantics, owner engine, priority/lane, whether repeatable, prerequisite visibility, player/team behavior, localization text, icon ownership, reward accounting, difficulty band, version-added tag and rollback plan. A future generator should check dependency loops, missing tags, nonexistent items/bosses, reward duplication and impossible irreversible requirements.

**Keep the early journal small:** tutorial and first expedition visible first; optional chapters appear on discovery and never trigger hundreds of toasts. Locked discovery journal tracking and per-player persistence must not create hundreds of active 1-second location polling objectives in Questlog without performance evidence.

## Inspiration, not direct copying

Design patterns were researched from [Cisco's RPG Questlines](https://ciscos-rpg.fandom.com/wiki/Quests), [Integrated Minecraft](https://www.curseforge.com/minecraft/modpacks/integrated-minecraft), and [Prominence II](https://www.curseforge.com/minecraft/modpacks/prominence-2-hasturian-era). The **quest copy, reward tables, artwork and progression** should be original to Ambient Odyssey and verified against its mod version/pack balance.

## Release independence

No Questlog JAR was installed, no FTB Quests chapters modified, no existing player quest state changed, and no active Test8.2/Test8.3 source/release altered by this mapping task.
