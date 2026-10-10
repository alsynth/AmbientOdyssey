# Questlog administration and overview — Ambient Odyssey

Applies to **Questlog 3.4.1** on Minecraft 1.21.1 NeoForge in Ambient Odyssey v0.4h; source: [Questlog 1.21.1 commands](https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/commands/QuestlogCommands.java) and [official command reference](https://github.com/infernalstudios/Questlog/blob/1.21.1/docs/questlog/commands.mdx).

## In-game admin/editor

1. Log into a **disposable test world** with Minecraft operator permissions **level 2 or higher**.
2. Run `/ql edit_mode true` or `/ql edit_mode` (toggle). The Questlog 3.4.1 source registers that subcommand even though some published command-reference pages omit it.
3. Open the Questlog UI using its inventory icon or default grave/backtick shortcut. Questlog includes dedicated quest and chapter editing screens. The editor offers entries and tabs for objectives, prerequisites, rewards and settings.
4. Use `/ql edit_mode false` when finished; `/ql reload` reloads files and synchronizes to currently online players. Confirm an edit appears only after backing up and inspecting affected JSON, and test actual save/reload behavior on a copied profile.

**This is not a web admin panel and not a unified dashboard of every player's progress.** The GUI is for editing/browsing quests; no external progress database or cross-player table is installed in AO.

## Useful operator commands

| Command | Purpose |
| --- | --- |
| `/ql edit_mode true` | Enable in-game editor for yourself |
| `/ql edit_mode false` | Leave edit mode |
| `/ql reload` | Reload chapter and quest config and synchronize |
| `/ql open` | Open own journal |
| `/ql open questlog:first_pages` | Open the First Pages chapter |
| `/ql progress complete questlog:ao_first_pages_01_welcome_to_ambient_odyssey` | Force-complete one specified quest on the test character |
| `/ql progress reset questlog:ao_first_pages_01_welcome_to_ambient_odyssey` | Reset that quest |
| `/ql trigger all` | Fulfill all prerequisites on test player |
| `/ql progress reset all` | **Destructively resets** all quest progress on the target player |

Operators can specify player targets according to the official command syntax; avoid `@a` on a shared world. The source also exposes `/ql reset_all_progress_and_reload`, a particularly destructive command that should never be used on real server data.

## Source-of-truth overview

| Content | Location |
| --- | --- |
| 50 Questlog quest definition files | `release_030/overrides/config/questlog/quests/*.json` |
| 13 Questlog chapter files | `release_030/overrides/config/questlog/chapters/*.json` |
| Searchable quest IDs, chapter, source, task types, reward counts | [Q1 installed index](QUESTLOG_Q1_INSTALLED_INDEX.json) |
| Quest construction and limitations | [Q1 implementation](QUESTLOG_Q1_IMPLEMENTATION.md) |
| First gameplay acceptance tests | [Q1 runtime checklist](QUESTLOG_Q1_RUNTIME_TESTS.md) |
| 32 FTB reference entries, distinct from adventure quests | [FTB manual installed index](FTB_MANUAL_IMPLEMENTED_INDEX.json) |

The files above live in **pack source** and are copied into a CurseForge instance at `config/questlog/` on import. A live player's progress is stored separately in the **world's** player data, not in the tracked quest definition JSON. Never treat Git changes as immediately applied to an existing world: take backups, reload on a disposable instance, and verify multiplayer persistence.

## Recommended admin workflow

- View the Q1 JSON index to audit all quests and stable IDs; enable edit mode for visual inspection.
- Change quest JSON in a feature branch, not in a permanent server world. Avoid changing quest IDs or deleting existing files when players have saves.
- Run `python tools/validate_v04_quest_campaign.py` before distribution to check IDs, chapters, reward ceilings, dependencies and cycles.
- Test one `read` objective, shield/provisions progression, one optional exploration task, manual chapters, then two distinct players/restarts. Collect logs/screenshots before fixing unverified behavior.
- If you need cross-player completion summaries later, a **separate read-only reporting tool** could parse backed-up world Questlog progress. It does not exist in this repository yet.

*All actual in-game editor appearance and save behavior remains untested in the complete 331-mod pack.*
