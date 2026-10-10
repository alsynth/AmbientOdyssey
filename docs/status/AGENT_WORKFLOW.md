## 2026-10-10 first-test kit update

Active *preparation* branch: `experimental/v0.4h-test-session-kit-20261010` (full pack still 331 CF refs). The compiled **modpack has not changed** since successful full ZIP run `38077302870`. A small separate read-only snapshot/field-sheet kit passed `38078378067`, tested 11 offline fixtures and released artifact `11678754683` with no JARs. Need user to **actually import a separate CurseForge instance**, capture Questlog icon screenshots, inspect outstanding 23 inaccessible/parse-failed exact JAR metadata, run full client and separately built server, then judge launch readiness. See `docs/testing/V04H_TEST_SESSION_FIELD_SHEET.md`. Do not mark these gameplay gates complete yet.


## 0.4h installed JAR/server readiness hardening — 10 October 2026

**Source-only developer tooling, not a gameplay acceptance pass.** Based on the **331-ref Questlog v0.4h candidate**, GitHub CI `38075828894` had **PASS** for all source, ZIP and deterministic repeat gates. Exact archive SHA-256s: PRIVATE `c611dd21ba6c3206881d47ca44b9ec13f239a019eb9d8c4a2384688a3df11784`; reference-only `514140b2b4b361b43a916cc5caff5b478c903633de8d4e448244b74afa93243e`. These hashes are historical for that exact successfully built source, not a claim about future changes.

Follow-on integration branch: `experimental/v0.4h-launch-readiness-20261010`. New `tools/audit_installed_jars_v04.py` reads top-level NeoForge and Fabric metadata in a CurseForge-imported profile and compares optional dedicated-server JAR lists. It flags duplicate mod IDs, unreadable metadata and unresolved declared dependencies **without claiming full dependency closure, bytecode compatibility, accurate sidedness or runtime tests**. Synthetic unit tests passed on CI run `38077150490`. The original 23 restricted/broken JAR audit cases are *still unverified* until actual installed files can be scanned. See `docs/testing/V04H_INSTALLED_JAR_AND_SERVER_PREFLIGHT.md`. Preserve prior 331-ref and 330-ref artifacts.

## v0.4 experimental Mine Cells candidate — 10 October 2026

**Current candidate:** `experimental/v0.4-complete-20261010`, source lock `0.4.0-experimental-minecells`, **318 CF references**. Supersedes older contradictory current-status paragraphs below; those are retained as historical evidence. User explicitly authorized continuing broad expansion and fixes before worldgen freeze. `structure/test6`, the existing content branches and `main` remain untouched.

Merged latest active source, all 0.4a–e content/worldgen repair waves and Mine Cells preflight. Added exact Mine Cells/Connector/FFAPI pins with existing NeoForge owo, required Iceberg/JamLib, narrow bridge validation, source-backed Traveloptics JSON/Fungi tag repairs and new-profile 12/6 distance defaults. **Actual isolated four-mod dedicated-server smoke PASS:** fresh world, all five Mine Cells dimensions force-loaded, save, stop, restart and stop. **Full AO v0.4 client/server, portal/boss/player tests NOT TESTED.** Dependency binary gaps explicitly recorded; no stable release promotion.

Read [changelog](../../V04_CHANGELOG.md), [test results and known issues](../../V04_TEST_RESULTS.md), [grouped checklist](../../V04_TESTING_CHECKLIST.md) and `docs/testing/v04-evidence/`. Build with `python build_release_030.py --private-modrinth --output build/Ambient-Odyssey-v0.4-Experimental-MineCells-PRIVATE.zip`; validate with `python tools/validate_v04_release.py <zip> --private`. Reference-only export omits NeoReefRedux. No automatic claim of public distribution approval.

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
