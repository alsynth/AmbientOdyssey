# Claude Code: R4 -> R5 Grand Treasure, minimum-effort verified local steps
15 October 2026 | PR #64 | Experimental preparation, not a published R5 package

## Correct baseline (CRITICAL)
Start on **experimental/master-integration-r3-reconciled-20261015**, PR **#64**, NOT the older experimental/master-integration-20261015 / PR #63 branch.

- Latest full private R4 import: Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip
- Exact R4 SHA256: 31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d
- Compiled R4 campaign addon: overrides/mods/ao-campaign-0.3.2-experimental.jar
- Exact R4 addon SHA256: 802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7
- R4 has 337 official CurseForge file refs, 10 bundled custom addon JARs, **30 DD zones, 13 curated Regalia and 58 native simply-swords unique IDs, 14 already chest-specific Grand Treasure sources, 153 quests**.
- The R4 packaging receipt records a dirty working-tree build source. Treat the actual **published ZIP byte hashes**, not the current source checkout alone, as the immutable executable input.
- R4 native startup/world join/save-exit evidence is valid for R4 only. No natural fights, Lootr multiplayer, production R5 build or R5 gameplay tests have yet passed.

## What changed since R4 (ONLY five native source-pool indices)
The newer PR #63 source-verified loot review showed that R4's 14-chest Grand policy is already category-specific, with only FIVE review-only improvements remaining:

| Native chest context | R4 pool index | Proposed pool index | Native treasure content |
|---|---:|---:|---|
| Keep Kayra library treasure | 2 | 1 | Native enchanted-book/equipment pool, rare Netherite Helmet |
| Keep Kayra keep treasure | 2 | 1 | Native enchanted-book/equipment pool, rare Netherite Boots |
| Adventure Dungeons Murky reward | 0 | 2 | Native armor trim templates and music discs |
| Iron's Spellbooks hidden trough | 3 | 1 | Native randomized spell scroll/blank rune |
| Iron's Spellbooks generic magic treasure | 6 | 1 | Native randomized spell scroll |

Original published upstream WDA/Adventure Dungeons/Iron's native table SHA256 values for all fourteen contexts were verified in GitHub Actions; see historical PR #63 evidence. This does **not** establish effective Paxi precedence in the currently uploaded 338-mod local pack, item function safety, boss trophies or Lootr two-player behavior. Owner approved the category-specific rule, **not automatic approval of all five exact index choices**.

**Committed machine-readable source:** docs/handoffs/r5-grand-from-r4-20261015/REVIEW_ONLY_FIVE_POOL_DIFF.json

## The code you can run using the complete local installed modpack

### 1. Generate a review-only R4-derived policy
Run at repository root with Python 3.11+:

    python tools/preview_r5_grand_from_r4.py --out build/r5-grand/ao_loot_policy.REVIEW_ONLY.json

The generator verifies exact Git blob of the R4 source policy and limits differences to five pool indices. It leaves bosses/Regalia/Sigils/gems/unique weapons/14 chest trigger IDs/5% probabilities unchanged.

### 2. Extract the 14 candidate rows for a REAL local source audit
The auditor expects a raw JSON list of chest entries rather than the wrapper preview:

    python -c "import json,pathlib; src=pathlib.Path('build/r5-grand/ao_loot_policy.REVIEW_ONLY.json'); dst=pathlib.Path('build/r5-grand/grand-native-candidates.json'); dst.write_text(json.dumps(json.loads(src.read_text())['policy']['grand_treasure'],indent=2)+'\n')"

Inspect the complete uploaded/installed AO mod directory, not merely ZIP manifest references. Adjust the following paths to where Claude Code can actually read the 338 JARs and configs:

    python tools/audit_r3_native_reward_sources.py --mods "<ACTUAL AO PROFILE>/mods" --paxi "<ACTUAL AO PROFILE>/config/paxi/datapacks" --candidates build/r5-grand/grand-native-candidates.json --out build/r5-grand/installed-jar-source-audit.json

If the Paxi datapacks directory is absent, inspect the profile layout; do not invent a path. The auditor now FAILS on an explicitly provided nonexistent Paxi directory instead of silently treating it as proof there are no overrides. For every proposed source require the exact native resource SHA, pool-index existence, entry-functions/weights review, no unresolved datapack-source collisions. The published upstream native JAR hashes recorded for the three mods can be cross-checked with the actual installed JAR binaries as an independent check.

### 3. Generate HUMAN review form, denied by default

    python tools/patch_r5_grand_from_r4.py --mode draft --preview build/r5-grand/ao_loot_policy.REVIEW_ONLY.json --out build/r5-grand/R5_GRAND_FIVE_DECISIONS_DRAFT_NOT_APPROVED.json

Do NOT auto-fill. Inspect and record all five pool decisions: installed native source, actual Paxi resource winner, functions/rarity/tier fit and owner category decision. Only after real checks, change status to APPROVED_FOR_EXPERIMENTAL_TEST_ONLY and mark four per-chest checkboxes true, with substantial explanations. These approvals authorize only an experimental test build, NOT production acceptance.

### 4. Create a NEW test addon, changing one JSON resource only
Download/import the exact R4 ZIP from its authenticated private GitHub release. The tested builder requires that R4 input SHA and compiled 0.3.2 addon SHA match the published receipt:

    python tools/patch_r5_grand_from_r4.py --mode patch --r4 "<PATH TO EXACT R4 ZIP>" --preview build/r5-grand/ao_loot_policy.REVIEW_ONLY.json --approval build/r5-grand/R5_GRAND_FIVE_DECISIONS_DRAFT_NOT_APPROVED.json --out build/r5-overlay/overrides/mods/ao-campaign-0.3.2-experimental.jar --receipt build/r5-reports/grand-campaign-patch.json

The output is a NEW JAR file. It retains every compiled Java class, all original JAR resources/metadata, addon ID and filenames; only ao_loot_policy.json differs. The script REFUSES if another bytecode/resource changes, if approval is still draft, if the current R4 ZIP or JAR differs, or if more than five reviewed pool indices change. No NeoForge/Apotheosis build dependencies needed for this mapping-only variant. New Java features still require full Java 21 compilation.

### 5. Generate a separate full R5 PRIVATE TEST import + rollback

    python tools/package_r5_grand_from_r4.py --r4 "<PATH TO EXACT R4 ZIP>" --addon build/r5-overlay/overrides/mods/ao-campaign-0.3.2-experimental.jar --patch-receipt build/r5-reports/grand-campaign-patch.json --output build/Ambient-Odyssey-MASTER-INTEGRATION-R5-GRAND-PRIVATE-EXPERIMENTAL.zip

This produces the full R5 test import, a separate increment-only Rollback.zip (NOT a standalone import) and a .report.json receipt. R4 remains immutable. R5 may differ only in campaign JAR + CurseForge import manifest; all 337 refs, 10 addon filenames, 30 DD zones, configuration bytes, quest files and unrelated mod JARs must stay identical.

Never upload or publish R5 as gameplay-accepted solely on static checks. The review forms and stage/packager synthetic tests are CI gated; see the workflow AO R4 to R5 Grand Delta Preflight.

## Before any R5 release acceptance
Run an isolated fresh-profile R5 import and disposable dedicated multiplayer server; verify normal native loot contents/odds remain and 5% is a single ADDITIONAL native-pool draw, never replacing native drops. Test Keep Kayra five eligible variants and Adventure/Iron's, all T3+ triggers, no T0–T2/Mine Cells, two independent Lootr players, reopen/restart, and randomized spell tiers. Preserve native gem/APOTHEOSIS behavior and the existing R4 DD/quest/boss rewards.

## Current handoff status
- FINISHED: review-only five-delta file; R4-based SHA-gated preview; manual-source-review form; R4 0.3.2 addon JSON-only binary patcher; R4->R5 full import and rollback builder; **30 synthetic CI tests PASS** in https://github.com/alsynth/AmbientOdyssey/actions/runs/38753512071.
- NOT DONE: read Claude's newly uploaded full 338-JAR profile from this GitHub Actions run; manual source/category approval; produce a real R5 JAR/ZIP; dedicated two-player Lootr tests, natural encounters or production acceptance.
- Do NOT merge/rerun the PR #63 R2-based compiler or overwrite PR #64 release artifacts. R2/R3 prep code and R4 have different packaged campaign versions.
