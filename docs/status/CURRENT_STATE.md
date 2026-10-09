# Ambient Odyssey — Current Project State

**Last reviewed:** 2026-10-09. **Authoritative repository:** `alsynth/AmbientOdyssey`. **Minecraft:** 1.21.1. **Loader:** NeoForge 21.1.252.

> START HERE for *any* new agent or conversation. This file is a status ledger, not proof of gameplay testing. Read [AGENTS.md](../../AGENTS.md), then [the Test 6 handoff](../handoff/START_HERE.md).

## Branches and evidence levels

- **`main`**: preserved Test 5 Audit1 source with cross-platform compilation and byte-identity repairs. Treat as the rollback source of truth. 238/238 scoped tests were previously run in a local check; in-game acceptance remains pending.
- **`structure/test6`**: Test 6 development branch. It has been merged with the repaired main baseline. Do not merge untested Test 6 work to main.
- **Claude's WDA major split/Mushroom Village patch**: supplied as `test6-wda-major-mushroom-village.patch` in a separate handoff on 2026-10-09. Its review against Audit1 applied cleanly; local patched-source build succeeded, its 24 new scoped gates passed, and the expanded legacy validator returned 242 checks. **Until the source commit is present on this branch, it is REVIEWED LOCALLY / NOT IN GITHUB**. Check branch history and file presence, not this note alone.

## Current Test 6 decisions

1. Raise WDA **Overworld** major candidate-grid frequency to **0.80** without raising the original End-only WDA set. Keep End set on native spacing 50, separation 45, salt 88371663, frequency 27/38.
2. Give **Mushroom Village** exactly one rare, dedicated owner, restricted to `minecraft:mushroom_fields`.
3. Keep Bathhouse at 112/48, 0.5; do not reintroduce Small Blimp or Coliseum. Preserve ordinary WDA and prior Test 5 fixes.
4. Preserve Audit1 Farmers Structures tuning (20 sets) and repairs. **Do not apply tuning a second time.**
5. Eight approved structure-mod additions remain **pending downloads, exact-version/dependency checks and source integration**. See `APPROVED_STRUCTURE_ADDITIONS.csv` and [blockers](../handoff/05_MOD_DOWNLOADS_AND_BLOCKERS.md).
6. Test 7 terrain/biome choices are documented planning **not authorized for Test 6**. Do not install them yet.

## Build and test (from repository root)

```powershell
py --version
py build_release_030.py
py validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/continuation-regression.json
# Only after the Claude WDA patch is actually committed:
py validate_structure_test6.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/wda-test6-regression.json
```

The output ZIP currently retains a Test 5 Audit1 filename even after Test 6 edits; **do not mistake that for a final Test 6 release**. Create properly named deliverables only at release validation.

Build from editable `release_030/` inputs and compiler scripts; generated `overrides/config/paxi/datapacks/` are outputs. Preserve original config line endings as needed for historical hashes. Required Tan's pack at `release_030/overrides/config/tanshugetrees/custom_packs/#main.zip` is a 73,500,294-byte **normal Git blob**, not an LFS pointer. Do not commit third-party unmodified mod JARs.

## Evidence labels

- **Implemented** means present in a specific Git commit, not merely provided in a chat/patch.
- **Statically verified** means explicit tool/validator execution. Always record counts and SHA-256 for the exact built artifact.
- **Runtime verified** means actual Minecraft client/server behavior was observed and logged.
- **Not tested** includes fresh-world structure density, overlap, biome selectors, registry loads, chunk generation and performance for Test 6.
- **Blocked** means required mod files/dependencies are missing or incompatible.

## Before an agent starts

Read `AGENTS.md`, this ledger, `docs/handoff/START_HERE.md`, `docs/handoff/01_TEST6_IMPLEMENTATION_BRIEF.md`, `docs/handoff/02_POST_HANDOFF_DECISIONS.md`, `TODO.md` and audit reports. Confirm which branch/commit you checked out, validate baseline before edits, work on a branch, and update this ledger with each PR. Do not use ChatGPT/Claude conversations as the only record of decisions.

## Received addon patches — 9 October 2026 (under review)

Claude supplied `test6-addon-audit.patch` (binary audit report) and `test6-install-addons.patch` (nine-project install/selector candidate). **Neither patch is implemented on GitHub yet**. A local reconstruction applied WDA → audit → installation patches cleanly, and independently obtained an identical two-pass ZIP hash `1383d71ec7178490ddf5b056c29c34fc14cd9ce0d48a972294ca799cf71ccec8`, with 247 continuation + 35 Test 6 scoped checks passing. These are not Minecraft runtime checks; source JAR binaries were not provided with these two patches.

**DECISION RESOLVED 9 Oct:** The user explicitly confirms **Explorify Black Spiral enabled provisionally** and **Structory: Towers v1.0.17 (CF 783522:8396885)**, superseding the former exclusion and older pin. Integration is authorized on `structure/test6` (not `main`); runtime Nether and cross-version loader compatibility remain UNVERIFIED. See [patch review](../reviews/TEST6_ADDON_PATCH_REVIEW_2026-10-09.md). **The source patches still need an actual successful commit/push** before they can be called implemented.

**Portability note:** `audit_jars_031.overlay_tags` has a path-splitting bug for checkouts under directories whose names include `/data/` (e.g., `/mnt/data/`); this can falsely fail `ambient_odyssey:sky_land_and_river`. Run from a neutral directory such as `/tmp/` until path handling is corrected.

## Test 6 source candidate — approved Claude patch stack imported

The three original Claude patches are retained at `docs/patches/` and applied on `structure/test6`. They include the WDA split, Mushroom Fields-only Village and 8 structure add-ons + AAA Particles. The user expressly approved Explorify Black Spiral enabled provisionally and Structory: Towers v1.0.17 (CF 783522:8396885) on 9 Oct. No Test 7 modifications. See `docs/status/TEST6_CANDIDATE_IMPORT.json` for **this checkout's** verified ZIP hash and every-file cross-platform equivalence; the earlier Linux reference ZIP SHA is not by itself proof of a Windows discrepancy. Canonical CTOV Waystone NBT is now checked semantically and pinned byte-for-byte to avoid platform zlib differences.

**Static check result:** 247 continuation + 35 Test 6; 246-project CurseForge manifest. **NOT RUNTIME TESTED:** Minecraft client/server startup, complete mod dependency closure, Nether Black Spiral collisions, Structory Towers version override, actual structure spawn density, terrain compatibility and performance. Do not merge `main` or publish a release until acceptance. Latest section supersedes earlier 'patches pending' language, only after GitHub push is confirmed.
