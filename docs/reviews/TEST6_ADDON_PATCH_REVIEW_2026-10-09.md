# Test 6 — Claude addon audit and installation patch review

**Reviewed:** 9 October 2026. **Status:** REVIEWED / NOT MERGED / NOT INSTALLED IN GITHUB. This is an evidence and decision handoff, not release authorization.

## Inputs

1. `test6-wda-major-mushroom-village.patch` — earlier WDA prerequisite; 91,510 bytes; SHA-256 `61fc0ea8165f2e704b74f90827cc1751264388317c05f0a0bfda7eaf445f4a6f`.
2. `test6-addon-audit.patch` — Claude's static binary audit, 1 Markdown report, 6,397 bytes; SHA-256 `2cf87bd5335502b043632770e95c5ad806da17d7f78ffd8c4f6980bc2463dadb`.
3. `test6-install-addons.patch` — nine pinned projects, selector changes and validator, 72 files, including one Git binary patch; 1,383,199 bytes; SHA-256 `efb4e12bcace710c4252a7d1b907ed18c522d0f6e16fe8e164b8ee7f8531368f`.

**Patch application order:** WDA → addon audit → addon installation. In a reconstructed, unpacked Test 5 Audit1 source, these applied cleanly in this order after adding the repository-only `AGENTS.md` and `docs/handoff/02_POST_HANDOFF_DECISIONS.md`. Direct application to the *current* GitHub branch must be checked anew because repository docs changed.

**Provenance:** The addon audit cites hashes of JARs examined in another agent's environment. The original JARs were *not* supplied with these two patches here; the reviewer verified the patch content, **not** those binary hashes or complete runtime dependency compatibility independently. A derived compressed resource index in the patch does not substitute for the nine source JARs.

## Reproduced local test (on isolated reconstruction; not yet on GitHub branch)

- Build: **PASS**, produced CurseForge ZIP with **246** project entries, root `manifest.json`, ZIP CRC pass.
- Rebuilt twice: identical SHA-256 `1383d71ec7178490ddf5b056c29c34fc14cd9ce0d48a972294ca799cf71ccec8` (**69,730,342 bytes**).
- Continuation static regression: **247 checks PASS**.
- Test 6 focused validator: **35 checks PASS**.
- No Minecraft client/server runtime was executed; these are static checks and do **not** prove structures work in-game, JAR dependency closure, or CurseForge actual downloadability.
- Environment caveat: validator `audit_jars_031.overlay_tags` splits paths at the **first `/data/`**; when the repository lives under `/mnt/data/`, that substring collides with the working-directory path and causes a false "sky_land_and_river" tag failure. The same candidate passed in `/tmp/ao_t6_validation`. Fix path handling by using relative paths rather than splitting absolute strings before adopting this as a portable validator.

## High-priority decision/compatibility blockers

**B1 — Explorify Black Spiral is enabled in install patch, conflicting with existing handoff.**
Our repository's prior `AGENTS.md` and `docs/handoff/02_POST_HANDOFF_DECISIONS.md` instruct to **disable** `explorify:black_spiral`. Installation patch rewrites this as "user decision 9 October: left enabled." That reversal is **not confirmed in this ChatGPT conversation**. Do not supersede the earlier requirement or merge this change without explicit user confirmation. The audit identifies `explorify:black_spirals` (40/18, salt 30184232; Nether bastion-biome selector) and a possible Integrated API disable-tag route. Runtime generation remains untested.

**B2 — Structory: Towers pin changed and version gate weakened.**
The original approved pin `783522:7078283` (v1.0.14) becomes `783522:8396885` (`Structory_Towers_26.2_v1.0.17.jar`). The installation patch adds a general `version_check_override` bypass to the CurseForge locked build. This is not the same as proving Forge/NeoForge 1.21.1 compatibility. Modrinth publishes v1.0.17 as compatible with 1.21.x, but CurseForge highlights 26.2; require explicit pin approval, inspection of actual JAR and Minecraft loader test before release. Prefer a narrowly scoped compatibility exception if needed, not a blanket bypass.

**B3 — The install patch asserts additional user decisions that are not independently verified here.**
These include shipping Nether/End content from four providers unchanged, accepting Create: Easy Structures' 16 independent native grids, and AAA Particles 2.3.3. They can be useful candidate settings, but should be confirmed against user decisions/constraints and actual density testing.

**B4 — Static audit vs runtime.**
The patch adds YUNG's Extras, YUNG's Bridges, Structory: Towers, Archaion, Explorify, Additional Structures, Create: Structures Arise, Create: Easy Structures and AAA Particles. It records 205 indexed resource snapshots and 9 new JAR identities, but none of those JARs were provided with this handoff. Archaion's custom placement `archaion:avoid_trial_chambers` and Bridges' placed features need actual modded-world verification. Create Arise needs Create 6.0.10; Archaion requires AAA Particles >=2.2.3. Additional Structures and Easy Structures may substantially affect density.

## Required before import/merge

- Get explicit user confirmation for **Black Spiral behavior** and the **Structory: Towers v1.0.17 pin/override**.
- Preserve the three original patches in `docs/patches/` or another versioned accessible location; do not rely on chat attachments as the sole source.
- Check the patch on the latest `structure/test6` commit, not only an old Audit1 zip. Apply source modifications in order and resolve documentation conflicts rather than overwriting the canonical status ledger.
- Run Python build + both validators, check root manifest and reproducible hashes, regenerate derived reports and update `docs/status/CURRENT_STATE.md`; in-game verification still pending.
- Keep `main` stable until runtime acceptance and reviewed PR. Do not start Test 7.

**Verdict:** The audit and installation patch are valuable, and static local reproduction passed; the **installation patch is held for confirmation** because it explicitly reverses settled pack decisions and changes a file to a cross-version package with an override.
