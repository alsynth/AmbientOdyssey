# Ambient Odyssey

**Exploration-first Minecraft 1.21.1 / NeoForge 21.1.252 RPG modpack**, built for 5–7 friends. This repository is the **editable development source**, not a pretested multiplayer release.

> **Active development handoff:** v0.4h Q1 + FTB Field Manual · **331 pinned CurseForge mod projects** · **50 Questlog adventure quests in 13 chapters** · **32 educational FTB pages in 3 chapters**. The latest content/packaging run [38080830259](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259) passed static checks; full Minecraft client, worldgen gameplay, Questlog interface and multiplayer remain **NOT TESTED**. The source of those built ZIPs is commit `9a5db8ea0ac16b8b55a6929e6819e6b8479178a0` on `experimental/v0.4h-q1-ftb-field-manual-20261010`.

## Start here

| Need | Go to |
| --- | --- |
| **Current state, last successful packages, blocking issues** | [Current project status](docs/status/CURRENT_STATE.md) |
| **What to develop or test next** | [TODO](TODO.md) · [Development handoff](docs/status/AGENT_WORKFLOW.md) |
| **Find everything in the repo** | [Repository map](docs/maintainers/REPO_MAP.md) · [Documentation index](docs/README.md) |
| **Browse the adventure quests** | [Q1 quest index](docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json) · [Q1 guide](docs/questing/QUESTLOG_Q1_IMPLEMENTATION.md) |
| **Edit Questlog as admin** | [Questlog admin guide](docs/questing/QUESTLOG_ADMIN_GUIDE.md) |
| **Find the in-game Field Manual** | [32-page FTB index](docs/questing/FTB_MANUAL_IMPLEMENTED_INDEX.json) |
| **Import latest experimental ZIP** | [Verified build artifact](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259/artifacts/11680318532) (download outer artifact, **import an inner** CurseForge ZIP) |
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
