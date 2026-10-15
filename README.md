# Ambient Odyssey

**Exploration-first Minecraft 1.21.1 / NeoForge 21.1.252 RPG modpack**, built for 5–7 friends. This repository is the **editable development source**, not a pretested multiplayer release.

> **Latest integration (15 Oct 2026):** R4 PRIVATE experimental import (337 CurseForge references, 10 bundled custom JARs, 30 scoped Dungeon Difficulty zones, 153 Questlog quests, campaign 0.3.2) on draft PR #64. Static and controlled native-engine checks passed; dedicated multiplayer, Lootr, natural boss fights/worldgen and owner acceptance remain open. Newer PR64 R5 Grand work is review/test tooling **not a released R5 ZIP**. **[START HERE — canonical Claude master handoff](docs/handoffs/CLAUDE_CANONICAL_MASTER_HANDOFF_20261015.md)** and [current implementation ledger](docs/status/IMPLEMENTATION_PROGRESS.md). The older v0.4h/Q1 and 331-ref pages are historical evidence, not the latest import.

## Start here

| Need | Go to |
| --- | --- |
| **Current status and recent decisions (Claude handoff)** | [**Canonical master handoff — R4/R5**](docs/handoffs/CLAUDE_CANONICAL_MASTER_HANDOFF_20261015.md) · [current implementation ledger](docs/status/IMPLEMENTATION_PROGRESS.md) |
| **What Claude should build/test next** | [Canonical implementation sequence](docs/handoffs/CLAUDE_CANONICAL_MASTER_HANDOFF_20261015.md#7-do-next-execution-sequence--optimized-for-claude-code-with-the-full-local-modpack) · [legacy TODO](TODO.md) |
| **Find everything in the repo** | [Repository map](docs/maintainers/REPO_MAP.md) · [Documentation index](docs/README.md) |
| **Browse the adventure quests** | [Q1 quest index](docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json) · [Q1 guide](docs/questing/QUESTLOG_Q1_IMPLEMENTATION.md) |
| **Edit Questlog as admin** | [Questlog admin guide](docs/questing/QUESTLOG_ADMIN_GUIDE.md) |
| **Find the in-game Field Manual** | [32-page FTB index](docs/questing/FTB_MANUAL_IMPLEMENTED_INDEX.json) |
| **Import latest full experimental ZIP** | [**R4 PRIVATE draft release**](https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-3d9c2fc62334621d6b59) — import Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip, **not** its rollback archive; R5 remains preparation only |
| **Test installed mods/client/server** | [Test checklist](docs/questing/QUESTLOG_Q1_RUNTIME_TESTS.md) · [Profile preflight](docs/testing/V04H_TEST_SESSION_FIELD_SHEET.md) |

## Source layout

- **`release_030/`** — pinned mod roster, manifest inputs and the actual Minecraft configs, data packs, structures, Questlog JSON and FTB SNBT to ship. Despite the folder name this is the actively used source input.
- **`build_release_030.py`** and legacy `compile_*.py` / `validate_*.py` at repository root — established reproducible build chain. **Do not move them without migrating imports and workflow paths**.
- **`tools/`** and **`tests/`** — recent preflight, authoring and diagnostic validators.
- **`docs/status/`** — short current briefing and actionable agent workflow. Full old status logs are archived.
- **`docs/questing/`** — quest implementation, reference-manual copy, quest inventories and QA.
- **`docs/audits/`, `docs/testing/`, `docs/handoff/`** — research, evidence, tests and older Test6 instructions. Historical documents are **not current requirements** unless revalidated.
- **`.github/workflows/`** — still-active v0.4 build/test workflows. **Historical one-shot workflows** are preserved under `.github/workflows-archive/2026-10-10/` and can be restored manually.

## Safe development rules

1. Branch from the current source candidate; preserve `main`, `structure/test6`, older experimental candidates, and any rollback branch. Repo organization happens on `maintenance/repo-organization-20261010`; **it is not merged into main**.
2. Do not modify `release_030/` mod files or the historically pinned 73.5 MB Tan's Huge Trees ZIP during housekeeping. Keep `Ambient-Odyssey-v0.2.10.zip` at root: the build references it as its baseline.
3. Static/CI PASS means source/package integrity only, never actual full-client, portal, Questlog reward or dedicated-server gameplay.
4. Deliver generated CurseForge exports as GitHub Actions or release assets, not new huge committed ZIPs. Never redistribute optional third-party mod JARs in a public package without permission.
5. After source modifications, run the Q1 quest, FTB manual, content/worldgen and exact ZIP validators listed in [the build guide](docs/maintainers/REPO_MAP.md).

## History and migration

The top-level README and handoff once described **Structure Test 6** as the next step. That work progressed through worldgen Test 8, v0.4 content expansion and Q1 authoring. We preserved old instructions, bootstrap files, and older workflows in the [archive manifest](docs/archive/ARCHIVE_MANIFEST.json); they are not silently deleted.

## Latest full-pack test: v0.4.8.3

Adds Seven Curses Ender Chest access in Better Inventory and removes Subtle Effects plus its dedicated End Remastered patch. Full-roster native equip/layout/click/unequip checks passed; manual edge cases and mob-crash regression remain. [Build and evidence](docs/testing/V0483_RING_INVENTORY_2026-10-12.md).

## Latest diagnostic import: v0.4.8.4 r19

Supplied r19 port integrated on top of the final Q/E UI pack. Full-roster native client/world/save passes, with 60 gems and no observed port parsing failure. Manual gem/server/multiplayer acceptance remains. [Build and evidence](docs/testing/V0484_R19_FULL_PACK_2026-10-12.md).
