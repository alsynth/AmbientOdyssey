# Simply Swords full sword pool — 15 October 2026

**Result:** The boss reward now draws one uniformly random sword from **133** verified Simply Swords swords, instead of the 58-entry unique list. It's a separate roll from the affixed item and the Regalia. Status: **SOURCE IMPLEMENTED + STATIC TEST PASS + javac compile PASS**. Not packaged, not engine-tested, not multiplayer-tested.

## Source JAR
`simplyswords-neoforge-1.70.2-1.21.1.jar`, SHA256 `5e75bd66…08c3`. This is the R4 pin, the same JAR used for the existing 58, read from the installed profile with Python `zipfile`.

## How each ID was verified (`tools/compile_simplyswords_pool.py`)
A pool ID must pass all four checks; the tool fails if one can't be verified:
1. It's a string literal in `net/sweenus/simplyswords/registry/ItemsRegistry.class`, which registers 140 IDs with no mod-presence checks.
2. The mod classifies it as a sword: `#simplyswords:swords` or `#c:swords`, nested tags resolved. This is the JAR's own definition, not a name guess.
3. It has an item model, `assets/simplyswords/models/item/<id>.json`.
4. It has an en_us name, `item.simplyswords.<id>`.

The previous 58 were verified by the same JAR tag (`#simplyswords:uniques`) plus a runtime registry and tag check, which `swordPoolIds()` keeps (registry + sword tag).

## Counts
| Group | Count |
|---|---:|
| **Pool** | **133** |
| Material weapons (15 types × iron/gold/diamond/netherite/runic) + `sword_on_a_stick` | 76 |
| Uniques | 57 |
| Previous 58 uniques not registered | 1: `dreadtide` (compat item, matches the R4 engine fixture's "57 registered") |
| Registered but not swords (left out) | 7: `runic_tablet`, `runefused_gem`, `netherfused_gem`, `empowered_remnant`, `contained_remnant`, `tampered_remnant`, `runic_forge` |
| Tagged swords not registered (compat for absent Mythic Metals / Gobber / Eldritch End) | 318 |

No creative-only or test items were found.

## Owner-review exclusion candidates (nothing excluded)
1. **Non-blade weapon types that the mod tags as swords (35):** spear, glaive, halberd, scythe, chakram, greathammer and greataxe, each in iron/gold/diamond/netherite/runic. The owner said "every sword" but also asked to tell swords apart from spears, glaives and hammers. The mod itself calls these swords.
2. **Novelty item (1):** `sword_on_a_stick`.
3. **Uniques the mod doesn't put in chest loot (17)**, not in `#simplyswords:lootable_uniques`. Most are upgrade or transformation forms: `awakened_lichblade`, `waking_lichblade`, `ionbound_stormscale`, `righteous_relic`, `tainted_relic`, `decaying_relic`, `the_devourer`, `harbinger`, `sunfire`, `soulstalker`, `dreadwhisper`, `enigma`, `gloampiercer`, `magiblade`, `magiscythe`, `magispear`, `wraithmaw`. Dropping them could skip the mod's own progression.
4. **Not Simply Swords:** `simplymore-forge-1.3.0_alpha.jar` (Simply More) adds weapons under its own namespace. They're not included; the owner can decide whether "Simply Swords" covers it.

The full row-by-row evidence is in `SIMPLYSWORDS_POOL_EVIDENCE.json`.

## Code changes
- `addons/ao-campaign/src/main/resources/ao_sword_pool.json`: 133 IDs, `selection: uniform`, `owner_exclusions_applied: []`.
- `BossRewards.java`:
  - New `swordPoolIds()` loads that file and keeps an ID only if it's registered and carries `#simplyswords:swords` or `#c:swords`.
  - `createBonus()` now uses it in place of `uniqueIds()`.
  - Boss mapping, eligibility (`tier()`), the affixed item, Regalia, rare extra rates, kill credit and native drops are unchanged.
  - `uniqueIds()` is kept for the test probe.
- `ao_loot_policy.json` is **byte-identical to R4**. The R5 preview and patch tools pin its Git blob and the 58-entry list, and the handoff says not to mix R5 with this change.
- Campaign version bumped to **0.3.3-experimental** (`build.gradle`, `neoforge.mods.toml`), so it can't be confused with R4's 0.3.2. R4's packager is hard-coded to 0.3.2 and will refuse this source until packaging is approved and updated.

## Tests
- `tests/test_simplyswords_full_pool.py`, 7/7 PASS:
  - Every ID resolves in the pinned-JAR evidence.
  - All 57 registered old uniques are in the pool.
  - No non-weapons, and no exclusions applied.
  - Every eligible boss reaches `createBonus`, which uses `swordPoolIds()`.
  - The roll stays independent of Regalia and the affixed item.
  - The R4 policy is untouched.
  - The pool re-derives byte-identically from the JAR when the JAR is present.
- Compile: `javac --release 21` of all campaign sources against R4-pinned NeoForge 21.1.252 (patched client + universal), the Minecraft 1.21.1 classes and libraries from the CurseForge install, and the Apotheosis 8.9.0 / Placebo 9.9.2 / ApothicAttributes 2.11.0 JARs: exit 0, 0 errors. The unchanged branch compiles the same way, as a control. Gradle `--offline` failed: Apotheosis artifacts aren't cached.

## Rollback
`git revert <this commit>`. That restores the unique-only roll and version 0.3.2, and removes the pool, tool, test and docs. R4 is unaffected.

## Remaining
- Owner: decide on the exclusion candidates above and confirm uniform weighting.
- Build: real Gradle/moddev build of 0.3.3 and update the packager. Not done; packaging wasn't requested.
- Engine test: native registry/tag check of all 133 in a real run (as done for the 57 uniques), and kill-loop drop sampling.
- Multiplayer: credited-player pickup and repeat kills.
