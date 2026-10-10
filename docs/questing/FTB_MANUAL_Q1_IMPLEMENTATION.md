# Ambient Odyssey — First FTB Field Manual installed-content wave

**Experimental candidate:** `experimental/v0.4h-questbook-manual-20261010`; no changes to the exact **331 CurseForge mod/project pins**, 50 Questlog Q1 quests, 13 Questlog chapters or WDA gameplay quest definitions. The release-lock label is deliberately suffixed `-q1-manual` so this ZIP cannot be confused with the older validated Q1 ZIP.

## What is now installed

The original FTB reference Markdown was converted to **29 user-visible localized SNBT articles in 3 new FTB chapters**, under `release_030/overrides/config/ftbquests/quests/chapters/`:

| FTB chapter | Pages | What players can look up |
|---|---:|---|
| Ambient Odyssey — Field Manual | 14 | Questlog vs FTB, JEI, shield/defense, slots, Lootr, maps, Apotheosis, Relics, two spell systems, dungeons, NeoPasterDream, Enigmatic Legacy |
| Ambient Odyssey — Tips & Tricks | 8 | Early expedition skills, inventory, combat, exploration, magic, multiplayer, troubleshooting and quick facts |
| Ambient Odyssey — Controls & Keybinds | 7 | Keybind landing page, inventory, JEI, waypoints, combat/voice, advanced debug and resolving conflicts |

Original text: `docs/questing/FTB_FIELD_MANUAL_DRAFT_PAGES_V0_2.md`, `FTB_TIPS_AND_TRICKS_V0_3.md`, `FTB_KEYBIND_CHEATSHEET_V0_3.md`.

**Each article is a single optional checkmark task with zero rewards, no prerequisites, and disabled completion toasts.** Clicking the checkmark acknowledges that a page was read; it is not supposed to prove a dungeon was completed or give a Questlog reward. Every page is always accessible without completing other pages. FTB remains an **educational manual**, Questlog remains the story/progression journal.

The original WDA `when_dungeons_arise.snbt` file was **not touched**. Existing `en_us.snbt` entries were preserved and only `chapter.*`, `quest.*`, `task.*` localization strings for the new pages were appended. FTB source on 1.21.1 supports `optional`, `disable_toast` and `checkmark` tasks.

## Limits intentionally kept

- The keybind pages distinguish user-remapped controls, historical DefaultOptions/KeybindOverrides configurations, and mod defaults. `keybindoverrides-client.toml` has `applyOverrides = false` so **do not assume every existing player has identical binds**. 
- Examples for NeoPasterDream, Enigmatic, magic and progression are provisional until verified in an actual fully imported client with exact installed registries.
- No economy-changing items, XP, currency or loot were added in FTB. No required beginner tasks, duplicated Questlog rewards, altered WDA checkpoints or auto-completed blanket progress.
- This is **written, source-validated educational content**, NOT a successful Minecraft GUI or multiplayer test. Questbook appearance, text wrapping, checkmark interaction, locale availability, per-player FTB Solo Quests, persistence and fit with Questlog's icon need a fresh-profile run.
- Existing 50 Questlog Q1 JSON quests remain experimental and must be tested for real completion/rewards.

## Static acceptance

Run `python tools/validate_v04_ftb_manual.py` with Python 3.11+ and `nbtlib==2.0.4` to parse real SNBT and fail on missing localization, duplicate IDs, task/reward mistakes or missing WDA strings. Independently run all original content/worldgen and Q1 Questlog validators and build new private and reference-only ZIPs with deterministic SHA comparison.

## First in-game check

1. Import this manual candidate into a **new experimental profile**, not the stable 331-ref Q1 profile. Java 21 and shaders off initially.
2. Open FTB Quests and verify the three chapters appear **alongside** the original WDA chapter.
3. Browse a long manual page, a tips page and a keybind table: look for cut-off lines, broken colors, missing icons, blank translations or scrolling issues.
4. Click one optional `mark as read` checkmark. Confirm zero rewards or side effects; restart/rejoin and verify its behavior.
5. Open Questlog and test the Q1 opener and existing configured inventory icon again. Verify there is no reward or state crossover from FTB.
6. Repeat on a separate two-player dedicated server; do not infer this from SNBT validity.

The older successful [50-quest Q1 pack artifact](https://github.com/alsynth/AmbientOdyssey/actions/runs/38079305682/artifacts/11678969415) remains the immediate rollback for any manual UI problem.
