# Ambient Odyssey — Questlog vs FTB Quests Evaluation

**Research date:** 10 October 2026. **Scope:** Minecraft 1.21.1, NeoForge 21.1.252, 5–7-player AO pack. **Status:** RESEARCH / CANDIDATE ONLY. **No Questlog mod, JSON quests, manifest pins or production configs have been installed/modified.**

## Verdict

**Questlog is a credible immersion-focused alternative for *narrative / expedition / boss / character* quests, but should NOT currently replace AO's planned giant FTB Quests mod progression book.** Strongest initial experiment is *FTB Quests as extensive reference/progression tree + Questlog as optional smaller story/adventure/character journal* on isolated test profiles. If dual-book UX feels redundant or triggers/persistence conflict, revert to FTB-only and borrow UI design principles. Do not prematurely author hundreds of quests in two competing formats. User has NOT approved a replacement or hybrid installation.

| Requirement | FTB Quests (currently staged in AO) | Questlog 3.4.1 | Recommendation |
|---|---|---|---|
| Long, broad modded questbook with dozens of chapters/hundreds of nodes | Mature graph chapters, dependencies, specialized extensible tasks, configurable rewards | Flat chapter journal and linked/triggered quests; no equivalent authored spatial progression tree | **FTB stronger foundation** for pack-wide catalogue |
| Immersive private-MMORPG quest presentation | Supports rich quest text, visible node maps, chapter artwork, rewards | Oblivion-style inventory-accessible readable log, conditional toast/popup, notification badge, per-quest style, hover images/animations, clickable quest links | **Questlog excels** for guided adventuring and character identity |
| Curated boss and dungeon quest lines | Native FTB tasks and commands | Entity kill/approach, visit structure/position, objective AND/OR/NOT, prerequisite quest_complete, failure triggers | Both viable; Questlog nicer as quest *narrative*, exact boss IDs and AO-tier gating need QA |
| Discovery journal | FTB 1.21.1 Visit Biome + Find Structure, chapters and other tasks | Exact-ID `visit_biome`, `visit_structure`, `visit_dimension`, plus quest-driven completions; no biome/structure tags in these specific types | Questlog works for curated handful; **not automatically a dynamic complete all-biomes/structures index or percent calculator** |
| Multiplayer independent progress | Base FTB is normally team-based; AO has **FTB Solo Quests 1.1.2** staged but only dedicated-server behavior to verify, not known-good integrated/LAN | Questlog server saves per-player UUID `<uuid>.questlog.dat` in world playerdata using temp+backup, and explicit player quest managers. `global` quests also exist, meaning global behavior needs clarification/test | Questlog likely simpler for private quests, **still run 2-player server persistence test** |
| Authoring | Rich in-game FTB editor plus SNBT, established reward/task addons and KubeJS ecosystem | 3.x in-game editor with presets (`/ql edit_mode`); JSON in `config/questlog/quests/`, chapters in `config/questlog/chapters/`, commands `/ql reload`, `/ql open`, `/ql trigger` | Both authorable; avoid a large migration before creator workflow tested |
| Rewards | Item, XP, commands, extensible reward systems, many advanced tasks and economy | Item, experience, command, loot table, **player choice** (3.0.0), **weighted random** (3.4.0); auto-claim supported | Both practical; no assumed automatic migration, command permissions audit required |
| Origin-based quests | FTB advancement/commands could bridge | `questlog:origin` objective exists (3.0.0), **but NeoForge source imports `com.iafenvoy.origins` and checks mod ID `origins`**, NOT CyberDay **NeoOrigins** | CRITICAL: if AO chooses NeoOrigins backend, Questlog Origin objective should be assumed **incompatible without explicit bridge/fix/test** |
| Performance at AO scale | Mature, still needs real AO testing | 1.21.1 source creates event listener per visit objective; each active `visit_structure` checks position/structure ~20 ticks per player; `visit_biome` similar. Many separate unfinished objectives could add overhead. Exact number/cost not benchmarked | Test 10/50/200 active objective definitions on 5–7 players before using it as entire book |
| Visual customizability | FTB themes, chapters and icons | Resource-pack-friendly parchment/panels, badge art, hover pictures, panels and colors | Questlog high thematic fit |

## Exact candidate / dependencies

- Official CurseForge project: **1202066**. Latest exact **NeoForge 1.21.1 Questlog 3.4.1 file 8952784**, uploaded **23 Sep 2026**. URL https://www.curseforge.com/minecraft/mc-mods/questlog/files/8952784
- Source branch `1.21.1`, version `3.4.1`, build against NeoForge **21.1.228**, Minecraft `[1.21.1,1.21.2)`; current AO loader **21.1.252** newer but compatibility not play-tested. Source: https://github.com/infernalstudios/Questlog/blob/1.21.1/gradle.properties
- Optional/runtime dependencies: `neoforge/build.gradle` includes **Cloth Config 15.0.140** and **Triggers** as bundled `jarJar`; Modrinth additionally labels Cloth Config required. Need inspect exact distributed JAR `META-INF` and verify dependency closure in the actual test profile; do not infer from Gradle compile dependencies alone. https://github.com/infernalstudios/Questlog/blob/1.21.1/neoforge/build.gradle ; https://modrinth.com/mod/questlog/version/3.0.0-1.21.1-neoforge
- Questlog is client+server and **ships NO predefined quests**. Existing README still says *datapack-driven*, but **since v2.0.0 content lives in `config/questlog/`**, not a vanilla datapack. Do not copy outdated 1.x folder instructions or assume KubeJS exports FTB SNBT directly.
- 3.1.0 renamed `requirements` to `prerequisites` (old definitions intended to work); 3.3.x/3.4.x improve editor/config and fix important progress resets.
- Source released under Apache-2.0, note custom art licensing/packaging as appropriate.

## Verified mechanics from 1.21.1 official source/docs

**Objective families:** `stat`, block mine/place/interact; entity breed/death/kill/tame/**approach**; item craft/drop/equip/obtain/use with item tags/components; `visit_biome`, `visit_dimension`, `visit_position`, `visit_structure`; advancement, enchant, effect_added, quest_complete, read; logical AND/OR/NOT; Origin objective; unobtainable externally triggered marker. Exact biome/structure visit objectives **do not support tags** in 1.21.1 documentation, whereas FTB 1.21.1 structure task can match structure tags. Sources:
- https://github.com/infernalstudios/Questlog/blob/1.21.1/docs/questlog/objective_types.mdx
- https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/core/quests/objectives/misc/VisitStructureObjective.java

**Quest controls:** configurable prerequisite triggers, completion objectives, failure conditions, chapters, quest sound/toast/popup, conditional descriptions, completion hide, repeatable and global flag. Quest and reward icons use item models or resource-pack textures. Quest description links may target other quests and show static/animated hover images. **No automatic complex branch-node map UI** comparable to FTB's graph verified.

**Quest rewards:** Items including components/enchantments, console-authorized command, XP, loot table, user-choice subset and weighted random. Review / test reward security/anti-abuse and ensure no unbounded repeatable rewards, avoid duplicated payouts on reload.

**Editor:** `/ql edit_mode` + in-game GUI. Quest runtime reload command `/ql reload`. JSON file hot reload; must test while users are online (AO already contains FTB config and Paxi).

**Progress persistence:** current source saves by UUID in `world/playerdata/<UUID>.questlog.dat` with backup file, and 3.4.0 changelog specifically fixes wiped player quest progress when another mod saves during login. *Persistence design exists* but AO dedicated server proof still pending.

**Origin integration caution:** Questlog NeoForge `NeoForgePlatformHelper` imports **IAFEnvoy Origins** `OriginDataHolder`, not NeoOrigins; do not count `questlog:origin` as functional for the CyberDay NeoOrigins candidate until bridging logic is tested. Can use advancement/command prerequisites instead if reliable.

**Runtime scaling caution:** `VisitStructureObjective.onPlayerMove` subscribes to player tick event and checks position roughly once every 20 ticks for each active matching player objective; per-objective repeated structure queries create possible scale cost. `VisitBiomeObjective` also polls every 20 ticks. **No measured FPS/TPS result, only code-level risk.** Other event handlers/task conditions similarly need testing with a large quest roster.

**Important version warning:** GitHub 1.21.1 doc `quest_definition.mdx` still spells `requirements` although 3.1.0 changed canonical to `prerequisites`. Test with an editor-generated 3.4.1 JSON specimen, not blindly copy an older example.

## Fit for Ambient Odyssey (no user approval to install yet)

**Retain FTB Quests:** current broad mechanical skill tree/gear progression, extensive mod guides, crafting/exploration checklist, 8-tier boss atlas, hundreds of quests, rewards and custom task formats, integration with user-staged FTB Solo Quests.

**Potential Questlog use (small/targeted):** first-play introduction for newcomer; short 3–5-step AO protagonist setup and Origin intro; new dimension arrival guide; discovering first dungeon, preparing correct Tier 2 gear, claiming an initial "Expedition Ready" completion; 6–20 curated major boss quest lines; limited NPC interactions and optional expedition contracts; interactive lore/hover map screenshots (but **NO scripted Lost Expedition Stories**, explicit user rejection). Emphasize quests useful to players instead of duplicated fetch tasks.

**Biggest drawbacks of a hybrid:** two separate books and completion systems, duplicate objectives/rewards, progress sync if both show the same quest, HUD noise, possibly more event listeners and extra mod dependencies. Avoid duplicate tasks by using **clear ownership** (FTB progression encyclopaedia, Questlog narrative/mission log). Distinct tabs/keys. Consider all-in-FTB UI polishing if players dislike maintaining two systems.

**Not a wholesale migration:** Questlog has no documented universal FTB SNBT converter and its own save files, objective semantics and reward behavior differ; a custom authoring/transformation tool would require item-by-item verification. Do not delete existing FTB chapters or change `ftbquests/data.snbt` until live acceptance and explicit user decision.

## Controlled prototype / acceptance checklist (NOT EXECUTED)

1. Clone the Test8.2 known-working client and a disposable NeoForge 21.1.252 dedicated server. Keep Test8.3 build work untouched. Add only official Questlog `1202066:8952784` and proven required dependencies on test copies. Confirm local client, server launch, disconnect/reconnect, and clean logs.
2. Author **three quest demonstrations** in 3.4.1 current config JSON using its editor:
   - Beginner welcome/read-once, optional pop-up and linked hover illustration, no forced gameplay lock.
   - Visit **one exact registered modded AO biome or structure**, after verifying its ID in game; check repeated entry doesn't credit twice.
   - Defeat a real minor boss/mob with prerequisite Quest Complete, choice reward and optional failure reset; reward only once, no duplicated payout.
3. Two players: independent quest progress, death, logout/login, world backup/restore, server restart, reload live quest definitions, login with FTB Solo Quests active.
4. **Origin interaction:** test against exact Origins backend chosen later; IAFEnvoy hard-coded check likely won't work if NeoOrigins installed. Try an advancement bridge rather than adding redundant backend.
5. Test UI with Better Inventory and Backpacks, inventory button placement, keybinds (default Grave Accent), FTB Quests, JEI overlays, shaders/resources, on 1920×1080 and lower resolution.
6. Compare 10/50/200 *unfinished* location tasks and ~5 players, record server tick/ms, network log spam, responsiveness, memory and save latency. No successful result claimed until test completed.
7. Brief 20-minute beginner playtest: Does player find relevant Questlog quests more naturally than FTB? Does maintaining *two* interfaces confuse them?
8. Decision: **hybrid acceptable / FTB-only / Questlog-only** after objective test. Only authorize wider authoring or manifest pin after explicit player feedback and performance evidence.

## Sources / audit provenance

- Official mod and release: https://www.curseforge.com/minecraft/mc-mods/questlog ; https://www.curseforge.com/minecraft/mc-mods/questlog/files/8952784
- Exact 1.21.1 source: https://github.com/infernalstudios/Questlog/tree/1.21.1
- Version history: https://github.com/infernalstudios/Questlog/blob/1.21.1/CHANGELOG.md
- Object types: https://github.com/infernalstudios/Questlog/blob/1.21.1/docs/questlog/objective_types.mdx
- Quest definition and styling: https://github.com/infernalstudios/Questlog/blob/1.21.1/docs/questlog/quest_definition.mdx
- Rewards: https://github.com/infernalstudios/Questlog/blob/1.21.1/docs/questlog/reward_types.mdx
- Progress engine: https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/core/ServerPlayerManager.java
- Origins integration: https://github.com/infernalstudios/Questlog/blob/1.21.1/neoforge/src/main/java/org/infernalstudios/questlog/platform/NeoForgePlatformHelper.java
- Existing FTB 1.21.1 author docs: https://docs.feed-the-beast.com/mod-docs/mods/suite/Quests/Developer/Quests/

**Status:** source-based review completed, no binaries inspected/tested locally, no AO modpack changes, no production decision to add or replace FTB Quests.
