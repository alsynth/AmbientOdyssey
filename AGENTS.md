# Ambient Odyssey — agent/dev instructions (current)

See [live 11 October development state](docs/status/V042_ACTIVE_DEV_20261011.md). The historical multi-page handoff is preserved at [pre-cleanup AGENTS](docs/archive/history/AGENTS_pre_organization_2026-10-10.md). **Start with [Current State](docs/status/CURRENT_STATE.md), [Agent Workflow](docs/status/AGENT_WORKFLOW.md) and [Repository Map](docs/maintainers/REPO_MAP.md).**

## Scope of the current project

- **Current experimental source (11 Oct):** `experimental/v042-quest-log-error-stabilization-20261011` is the validated 329-ref TREK/Create + deliberate FTB Manual test build. `experimental/v042-hominid-spawn-lifecycle-preflight-20261011` is an isolated additional Hominid 0.1.1 lifecycle *prototype*, not user-accepted. This branch `research/v042-history-regression-reconciliation-20261011` adds Curios amulet-slot compatibility and source-history regression checks. Minecraft 1.21.1 / NeoForge 21.1.252, 50 Questlog Q1 quests, 32 acknowledgment-based FTB Manual pages. The older 331-reference 0.4h source remains **historical**, not this pack's manifest.
- **Housekeeping source:** `maintenance/repo-organization-20261010`; this branch reorganizes human documentation and archives older workflows. No mod, worldgen, Questlog or FTB content behavior should change here.
- **Current release evidence:** [Trek/FTB Manual combined CI 38142477885](https://github.com/alsynth/AmbientOdyssey/actions/runs/38142477885) passed full private 329-reference ZIP preflight. User visually accepted TREK/Create structure density but no significant performance improvement measured. [Hominid v0.1.1 isolated prototype CI 38143106039](https://github.com/alsynth/AmbientOdyssey/actions/runs/38143106039) compiled. Neither the 329-ref revised quests nor the Hominid prototype has full Minecraft client/server acceptance.
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
