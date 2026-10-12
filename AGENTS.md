# Ambient Odyssey — agent/dev instructions (current)

The historical multi-page handoff is preserved at [pre-cleanup AGENTS](docs/archive/history/AGENTS_pre_organization_2026-10-10.md). **Start with [Current State](docs/status/CURRENT_STATE.md), [Agent Workflow](docs/status/AGENT_WORKFLOW.md) and [Repository Map](docs/maintainers/REPO_MAP.md).**

## Scope of the current project

- **Active modpack source:** `experimental/v0.4h-q1-ftb-field-manual-20261010`: MC 1.21.1, NeoForge 21.1.252, 331 exact CF projects, 50 Questlog Q1 quests and 32 FTB Manual pages.
- **Housekeeping source:** `maintenance/repo-organization-20261010`; this branch reorganizes human documentation and archives older workflows. No mod, worldgen, Questlog or FTB content behavior should change here.
- **Release evidence:** [run 38080830259](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259) successful for ZIP/static checks. Full 331-mod Minecraft client and dedicated-server experience is **not runtime-tested**.
- **Preserve:** `main`, `structure/test6`, rollback branches and known working package candidates. Never overwrite the original locked Tan's Huge Trees ZIP or `Ambient-Odyssey-v0.2.10.zip`.

## Working rules

1. Read the [current TODO](TODO.md) and source specs before edits. Avoid treating old Test6 handoff docs as the latest constraints.
2. Keep the established root Python compiler/validator imports and the entire `release_030` tree stable unless a separate feature branch migrates them with comprehensive regression tests.
3. Make new content in `release_030`, new helper tools under `tools/` and tests under `tests/`; avoid further top-level clutter.
4. Preserve stable quest IDs and chapter definitions. Questlog v3.4.1 provides `/ql edit_mode` for permission-2 operators. No genuine AO GUI or player-progress QA has been completed.
5. Run packaged source/JSON/Questlog/FTB/worldgen validators and the actual ZIP preflight; don't call static PASS a playable release.
6. Do not assume a fictional modded item, entity, recipe, structure or dimension is available. Confirm installed 1.21.1 IDs before wiring quest triggers.
7. Keep user-facing change reports honest about what is built, source-validated, runtime-tested, or still blocked.

For all earlier history see [full previous agent notes](docs/archive/history/AGENTS_pre_organization_2026-10-10.md), rather than stacking more outdated "LATEST" banners here.

## Communication preference

Always prefer short, simple answers in project reports and status updates. Lead with results and the next action. State test results and remaining blockers clearly. Expand only when requested or needed for accuracy.
