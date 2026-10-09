> **Repository state first:** Read [docs/status/CURRENT_STATE.md](docs/status/CURRENT_STATE.md) and [docs/status/AGENT_WORKFLOW.md](docs/status/AGENT_WORKFLOW.md) before making changes. The default branch is the protected-by-process Test 5 Audit1 baseline; `structure/test6` is experimental. Update those documents on every completed change. Work from the repository alone; do not assume conversation history.

# Ambient Odyssey — Agent Entry Point

This repository is the implementation handoff for **Structure Test 6**, based on Minecraft 1.21.1 and NeoForge 21.1.252.

**Do not begin by changing the repository.** Reproduce the checked-in Test 5 Audit1 build and run its validator first. Stop and report if it does not reproduce. Source files are rooted here; no need to unzip another source package.

## Mandatory reading order

1. `docs/handoff/START_HERE.md`
2. `docs/handoff/01_TEST6_IMPLEMENTATION_BRIEF.md`
3. `docs/handoff/02_POST_HANDOFF_DECISIONS.md`
4. `docs/handoff/03_TEST7_BIOME_QUEUE.md` (planning only, do not implement yet)
5. `docs/handoff/04_BUILD_AND_VERIFY.md`
6. `docs/handoff/07_PASTE_INTO_EXTERNAL_AGENT.md`
7. `TODO.md` and `docs/audits/*` reports/catalogues

## Non-negotiable guardrails

- Preserve Audit1 CTOV, IDAS, Cataclysm Spellbooks, biome eligibility, Farmers Structures and other completed source fixes; do not apply tuning twice.
- Eight selected structure additions are pending third-party JAR download, compatibility and dependency verification.
- WDA Overworld major frequency 0.80 is the target while End rarity and Bathhouse rarity are preserved.
- WDA Mushroom Village must be rare and Mushroom Fields-only; Explorify Nether Black Spiral disabled; no WDA Small Blimp or Coliseum.
- Do not add Block Factory's Biomes, FDstructure, incompatible/duplicate mineshafts or deferred Test 7 biomes.
- Do not fake registry IDs, template pools, successful tests, or tool outputs.
- No unmodified third-party mod JARs in git.
- Check SHA and root `manifest.json` for the exact output CurseForge archive.
- Distinguish implemented, statically verified, runtime verified, not tested and blocked.

## Work strategy

Create a `structure/test6` branch and commit independently reviewable changes. Edit canonical inputs, regenerate with project scripts, run static gates, package deterministic outputs, and prepare a fresh-world acceptance checklist. Do not call the work finished without honest validation status.
