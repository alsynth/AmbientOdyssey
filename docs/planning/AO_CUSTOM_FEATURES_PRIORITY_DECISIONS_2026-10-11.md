# Ambient Odyssey — Custom Feature Priorities (User decisions, 11 Oct 2026)

**Authority:** Latest user's explicit roadmap decisions. Supersedes exploratory suggestions for guilds/discovery/balance scope. **Planning only, no gameplay source changed by this file.** Baseline is the successful v0.4.4 pre-performance candidate, itself an experiment, and no old rollback should be overwritten.

## Phase 1 — most interesting bespoke projects, BEFORE performance

1. **Buffed starter Bonus Chest — top priority.** Datapack override of `minecraft:chests/spawn_bonus_chest`, a meaningful starter gear/supply pool, and per-player Lootr conversion verification. Prior policy says valuable rewards are fine but per-player Lootr conversion is a hypothesis until tested. Coordinate with the new early Questlog food/torch rewards and 5–7 player economy; keep opt-in Bonus Chest. Avoid claiming each player gets an independent instance until tested on actual server.
2. **Apotheotic/Apothic Additions source port feasibility and scoped implementation** for 1.21.1 NeoForge; check exact upstream project/version/license, current Apotheosis/Apothic libraries, APIs, and alternative native addon availability. No blind binary repack or claim that a port is finished.
3. **Random armor trims on Apotheosis rarity armor generated in dungeon chests or mob drops.** Prefer narrow loot/item-generation hook to preserve generated affixes, gem sockets and durability; decide compatible trim registries & randomness, test with Lootr and inventory/JEI. Implement separate from broad loot rebalance.
4. **Goblin-Tuned trade pricing/scarcity** while RETAINING powerful tuned attributes, not removing them. Investigate native Goblin Traders configs/trade tables, then narrow hook only if necessary. Final economic numbers can be refined during post-performance balance, but any necessary technical addon belongs here.
5. **Wet Sands compatibility/port review and narrow prototype** only if an actual remaining missing feature is confirmed; don't port if it is already functional through existing compatibility.
6. **Foundation-only boss/dungeon hooks** where existing native Dungeon Difficulty configs/datapacks cannot express approved tier design. Do not conduct the full tier-by-tier combat balance pass before performance. No unverified Mixin explosion.

These are scoped as proposals for the first development wave, not confirmation of feasibility. Prioritize data packs/scripts over custom Java when reliable; consolidate minimal Java hooks where appropriate. Check exact 1.21.1 NeoForge versions, licenses, dependencies and multiplayer side. Do not expand mod roster indiscriminately.


## Added traversal-wear request — 11 October 2026

- **YES: stronger player-traffic path erosion.** Frequently walked paths should become more visibly worn and develop more noticeably than lightly traveled ground. Specifically target the existing TRMT/Desire Paths-style walked-trail system, **not** FreeTerraForged terrain sculpting, rivers or an indiscriminate global erosion increase.
- **Timing:** include a targeted config/API audit and cheap native tuning during the upcoming custom integrations wave if practical; otherwise finish as a bounded world/visual gameplay tuning item alongside performance, **before final server/world settings are locked**. Avoid a major new terrain-generation rewrite.
- **Tuning objective:** make a noticeable difference between occasional footsteps, repeated player use, and established routes, preserving grass/vegetation in low-traffic areas. Avoid instant full-width dirt highways, excessive farmland damage, permanent unwanted paths inside player buildings, or extra TPS cost. Verify real mod version and available config fields before setting numbers; use a small patch only if native options cannot achieve desired results.
- **Acceptance:** revisit a frequently walked route versus a control route in a disposable survival world, compare before/after wear, regrowth/reversal if supported, and test multiplayer/server impact. Record any chunk updates or save footprint. No existing gameplay change is implied by this planning note.

## Phase 2 — performance and server readiness

After the bespoke changes that touch registries/content are stable, run a true exploration-oriented performance pass (normal walking, sailing, combat, new chunks and cached chunks, 5–7 player server). Fix keybinding/performance-side configuration collisions where necessary; test native worldgen settings; select final seed, finalize structure placement, and PREGENERATE an agreed, bounded Overworld radius with Chunky before server opening. Admin `/locate` or teleport-to-unloaded-chunks are not representative primary benchmarks. Keep world pregen AFTER biome/structure generation settings finalized.

## Phase 3 — rest of approved creative systems AFTER performance

- **YES: Rumors, treasure maps and clue chains**, anchored to truly reachable, curated existing structures; integrate optional Questlog, loot and NPC dialogue. Avoid coordinate spoilers and arbitrary loot farming.
- **YES: Explorer's Journal** with persistent per-player discovery history and selectable checklists, but **first audit current overlap**: Xaero's map/waypoints, Traveler's Titles/other travel title mods if actually pinned, Questlog structure/biome objective tracking, FTB Quest reference/manual, and Explorer's Journals if present. These overlapping features do NOT automatically establish a unified discovery journal. Prefer integration or extension over a redundant mod.
- **MAYBE: A separate discovery mod** only if current mods fail to provide useful journal coverage. Do not automatically install another tracker.
- **YES: Boss danger identification / reconnaissance**, ideally mapping found structure/boss ID to broad AO difficulty tier and gear-readiness hints; needs finalized tiers and real ID verification.
- **YES but LOW priority: Biome field guide, archaeology discoveries and other previously approved optional exploration extras**, after performance and core balancing, as value warrants.
- **YES, CAN WAIT: Ambient Odyssey custom main menu/logo**, including removal of BetterEnd popup and Aquamirae menu branding. Cosmetic phase.
- **Mine Cells opening arc: ONLY through Questlog progression,** with Overworld starter chest and native portal/return loop. No custom engine-level Mine Cells starting campaign or mandatory forced entry; portal before boss can be used for narrative returning to Overworld, pending runtime check.
- **Full boss/dungeon difficulty tier tuning and loot economy** follows performance, building on foundational hooks without major mod rewrites.

## Explicitly DECLINED / REMOVE FROM FORWARD ROADMAP

- NO Explorer's Guild / guild board / guild contracts.
- NO Discovered -> Conquered -> Mastered system.
- NO custom FTB Ocean Mobs loot work (unless separately requested in future).

## Source reminders

Latest decision favors **interesting custom projects -> performance -> remaining approved custom experiences**, not 'implement every brainstorm before performance'. Do not treat the current v0.4.4 package as proof of live functionality for its new quests and jigsaw repair; build new experimental branches and retain rollback.
