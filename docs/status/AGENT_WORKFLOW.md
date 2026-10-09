# Ambient Odyssey — Agent Repository Workflow

The **repository is the canonical handoff**, not a conversation, external ZIP or someone's memory.

## Every new agent must do the following

1. Identify repository `alsynth/AmbientOdyssey`, active branch, commit SHA, and current [project state](CURRENT_STATE.md).
2. Read root `AGENTS.md`, `docs/handoff/START_HERE.md`, the Test 6 implementation brief, post-handoff decisions, `TODO.md`, and relevant audits. These files establish settled choices and stop conditions.
3. Rebuild before edits, run the appropriate source/runtime regression gates, and report failures **before** modifying anything.
4. Work against **editable `release_030/` inputs** (source-of-truth); compile derived Paxi packs and regenerate audits rather than manually patching only generated outputs.
5. Commit source changes, generated outputs, gate code, validation results, changed audit catalogues, status and changelog **together**, ideally via a PR. Don't overwrite the stable baseline in `main`.
6. Keep major structure/boss rarity, preserve End WDA behavior, Farmers tuning and curated biome decisions. Work on Test 7 only after Test 6 acceptance.
7. Verify final CurseForge import has `manifest.json` at ZIP root; run a second clean build and hash comparison. Minecraft runtime testing is separate from static checks.
8. Clearly label **Implemented / Static verified / Runtime verified / Not tested / Blocked** and cite commit IDs, source paths and artifact hashes.

## Working with external agents

A patch from another agent is **not implemented until committed** and its generated assets and regressions are checked. Attach or commit the patch under `docs/patches/` if useful for traceability. Agents should prefer repository files over out-of-band text. Never ask users to share access tokens in chat; use authorized GitHub integrations or have the user apply and push a prepared patch.

## What to update at the end of each task

- `docs/status/CURRENT_STATE.md` — latest working branch, implemented vs pending, blockers, evidence.
- `TODO.md` — mark only genuinely completed steps.
- Relevant `docs/audits/` and CSV catalogues, if changed.
- Code/source plus *recompiled* generated assets and validator additions.
- Changelog and optional PR description with exact steps, hashes, known limitations.

### Known blockers

Eight selected new structure mods remain pending integration and loader/dependency verification. Full runtime acceptance and Test 7 are pending. See `docs/handoff/05_MOD_DOWNLOADS_AND_BLOCKERS.md`.
