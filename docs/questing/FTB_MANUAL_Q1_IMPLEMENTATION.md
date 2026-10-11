# Ambient Odyssey — FTB Field Manual Q1 integrated reference pages

**State:** `experimental/v0.4h-q1-ftb-field-manual-20261010`, based on the validated **331-ref Questlog Q1** branch.

## What is authored

**32 browseable FTB Quests reference pages in three task-free, reward-free chapters:**

- **Field Manual — Systems (15 pages):** 14 existing detailed original articles plus a landing page. JEI, shields, combat supports, Lootr, maps/Waystones, Apotheosis, Relics, Iron's Spellbooks, Ars, dungeon tiers, Dreamscape and cursed-versus-uncursed Enigmatic routes.
- **Tips & Tricks (9 pages):** eight authored topics including 65 earlier tips, a practical opening checklist, expeditions, combat, magic, multiplayer, troubleshooting, and concise discoveries.
- **Controls & Keybinds (8 pages):** seven topics including JEI R/U, inventory moves, F3 diagnostics, map defaults, mod-specific bindings and conflict recovery; new welcome page warns about untested defaults.

The source articles reside under `docs/questing/`; the **actual FTB chapter SNBT** resides in `release_030/overrides/config/ftbquests/quests/chapters/` and new translation keys are added to the existing `lang/en_us.snbt`. Stable deterministic **uppercase 16-character hex IDs** avoid colliding with the shipped WDA chapter and its pre-existing quests.

The original `when_dungeons_arise.snbt`, chapter groups, reward tables, global FTB Quests `data.snbt` and FTB Solo Quests configuration are preserved. All manual pages have `tasks: [ ]` and `rewards: [ ]`, with **zero prerequisites**; FTB Quests may visually mark them completed automatically, which is acceptable for reference content. **No character progression, material rewards, cursed-ring activation or repeatable XP** originates from the manual.

## Why this is separate from Questlog

Questlog Q1 owns 50 exploration/story entries across 13 chapters. These FTB pages explain mechanisms, shortcuts and tactics rather than duplicating Questlog achievements. A guide about JEI is not a claim that JEI interaction was automatically detected; a guide about Relics is not a claim that exact item effects or attribute caps were gameplay-verified.

A few pages include preexisting draft statements referring to features as proposed; the current editor should prioritize correcting them **after installed-mod and keyboard testing**. The keybind cheatsheet explicitly distinguishes AO-distributed suggested bindings from actual, user-rebound controls. Do not force final keybind assignments without observed input conflicts.

## How to verify in-game

1. On a **new disposable profile**, import the separate **Q1+Manual experimental private ZIP** rather than overwriting an existing Q1 or old Test 5/6 profile.
2. Open FTB Quests. The existing **When Dungeons Arise** chapter must remain intact, including the special chests/advancements and original rewards.
3. Locate three new manual chapters and page titles; open representative pages (JEI, Apotheosis, Keybinds). Confirm readable text, no missing translation keys, tabs or duplicated overlay.
4. Open Questlog separately. No double quests/rewards; manual should remain accessible without completing the 50 Q1 Adventure Journal nodes.
5. Restart client and dedicated server, load both FTB and Questlog with two players, inspect errors and screen scaling. This is *not* established by static CI.
6. Log page clipping/wrapping issues, outdated keybinding suggestions, or text which doesn't match the exact modpack version.

## Validation limits

`tools/validate_v04_ftb_manual.py` checks source syntax balances, unique hex IDs, chapter/page counts, no tasks/rewards, and the presence of localized titles/descriptions. It is **not** the full FTB runtime SNBT parser. CI source/ZIP checks plus repeated rebuilds still cannot establish GUI rendering, team-based FTB progress, quests auto-marking, multiplayer or content truth.

Further work once a client can load this content: contextual icons/screenshots, link pages from the Q1 journal, real 1.21.1 keybinding screenshots, full modded recipe examples (verified by JEI), gear and boss dossiers, and optional archaeology pages with concrete reward provenance.

## Q1 copy correction

After the first successful static packaging run, the published manual text was corrected to treat Questlog as already installed rather than a future mod. It describes the trial screen-anchored inventory icon and default grave/backtick control accurately while still requiring visual/keybind acceptance. Two other legacy research placeholders were revised so the manual does not promise an unavailable automated Explorer's Journal or future JEI recipe exception catalogue.

## 11 October 2026 — reference-page task correction

The generated chapter SNBT previously had **32 `checkmark` tasks** despite the documentation describing task-free reference pages. These looked like ordinary FTB quests and reasonably caused confusion with Questlog's authored adventure quests. Source SNBT now uses `tasks: [ ]` for all 32 manual pages with `rewards: [ ]` unchanged. FTB Quests may mark empty-task pages completed; this is acceptable for information-only articles but still requires in-game UI testing. The inherited WDA authored FTB quests and Questlog's 50 independent quest definitions were not touched.
