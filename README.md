# Ambient Odyssey — Minecraft Modpack Development

**Minecraft:** 1.21.1  |  **Loader:** NeoForge 21.1.252  |  **Target:** 5–7-player, exploration-first RPG modpack

This repository contains the editable **Structure Test 5 Audit1** source and the full external-agent handoff needed to implement **Structure Test 6**. It is **not** a claim that Structure Test 6 is complete.

## Start here

1. Read [`AGENTS.md`](AGENTS.md) (also applies to non-Codex agents).
2. Read [`docs/handoff/START_HERE.md`](docs/handoff/START_HERE.md), then [`docs/handoff/01_TEST6_IMPLEMENTATION_BRIEF.md`](docs/handoff/01_TEST6_IMPLEMENTATION_BRIEF.md) and [`docs/handoff/02_POST_HANDOFF_DECISIONS.md`](docs/handoff/02_POST_HANDOFF_DECISIONS.md).
3. Read [`docs/handoff/04_BUILD_AND_VERIFY.md`](docs/handoff/04_BUILD_AND_VERIFY.md), [`TODO.md`](TODO.md) and supporting reports under [`docs/audits/`](docs/audits/).
4. Reproduce the current baseline using Python and the existing build/validator, without modifying source files.
5. Make any changes in the editable inputs first, then compile generated datapacks and validate again.

## Source of truth

- **Active editable source:** this Git repository, initially extracted from `Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip` without modifying its existing members. Build scripts and `release_030/` remain at the repository root.
- **Current state:** Test 5 Audit1 statically validated; no complete in-game acceptance test.
- **Next target:** Structure Test 6; eight selected structure mods, WDA tuning, biome compatibility and associated repairs.
- **Later target:** Test 7 biome/terrain changes, documented but **not authorized for Test 6**.

## Large Tan's Huge Trees asset

The original `release_030/overrides/config/tanshugetrees/custom_packs/#main.zip` is 73,500,294 bytes (SHA-256 `0c20b47a6377230e10c53fe36f30efa6c14fd8576928640e7c8af8580122ab89`). It is intentionally committed as a **normal Git blob** to avoid Git LFS download restrictions in external agent environments. GitHub warns above 50 MB, but the file is below its 100 MB hard limit. Verify this file exists as a full ZIP, not a 133-byte LFS pointer, before building.

## Tests and distribution

CurseForge import ZIPs and source snapshots should be published as **GitHub Releases assets**, not committed repeatedly. Each release should include source/import archives, a changelog, validation report and SHA-256 checksums. Verify `manifest.json` at the **root** of the exact CurseForge import.

Do not report in-game validation unless Minecraft was actually run. Inspect the 9 October runtime log and other reports for existing evidence, not as substitutes for Test 6 acceptance.

## External dependencies

Download **official CurseForge mod files** by their exact approved project/file identities where possible, and inspect loader compatibility, dependency metadata and actual registry assets before integrating. Never invent a compatible substitute or redistribute unmodified third-party JAR files in this repository. See the approved-additions catalogue and Test 6 instructions for the exact requirements.

## Git workflow

Use branches such as `structure/test6` for work; submit pull requests to `main` and preserve the initial Test 5 Audit1 baseline in git history. Do not treat regenerated reports as proof of runtime behavior.
