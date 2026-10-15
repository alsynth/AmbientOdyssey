# Implementation progress — 15 October 2026

**Canonical next-agent overview:** [Claude master handoff](../handoffs/CLAUDE_CANONICAL_MASTER_HANDOFF_20261015.md). This file remains the batch implementation ledger, while the handoff reconciles R4 release, post-R4 R5 prep, owner overrides and stale historical docs.

This is the current working ledger for `experimental/master-integration-r3-reconciled-20261015` / draft PR64. Stable/main is unchanged. Each completed batch must update this file and its evidence in GitHub; a source implementation is not automatically packaged or runtime accepted.

## Previous published package (retained rollback/test baseline)

R3 RECONCILED, campaign0.3.2: `Ambient-Odyssey-MASTER-INTEGRATION-R3-RECONCILED-PRIVATE-20261015.zip`.
SHA256 `5debe094c047162f0b30f2dd76e2ab85201310c480b64333eca89a4f4376ac99`.
[Private release](https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-288bd4f89b923343564e), [draft PR64](https://github.com/alsynth/AmbientOdyssey/pull/64), [complete audit](../handoffs/r3-reconciled-package-20261015/R3-RECONCILED-DRAFT-AND-PLAN-AUDIT.md).

Implemented and packaged: scoped23-zone DD baseline;51 native boss field edits with explicit exceptions; additive starter/trades/rings; native rarity/Sigil/UI integrations;32 mapped boss reward IDs,13 curated Regalia and native unique-only weapons;14 chest-specific Grand mappings; restored native gems and Solo Quests new-world default. Build/static checks and100 Python tests passed for that source checkpoint. Runtime evidence below must be read separately.

## Current completed batch: R4

Full private R4 ZIP: `Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip`.
SHA256 `31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d`.
[Implemented/remaining/test details](../handoffs/r4-package-20261015/R4-IMPLEMENTED-REMAINING-AND-TESTS.md).
Seven source-backed owner-selected zones implemented and packaged; total30. Actual R4 engine startup/world join/save-exit0 PASS,30 registered zones,34 synthetic DD cases PASS,600 reward factory samples PASS,13 Regalia and57 native uniques.105 Python tests PASS. None is natural combat, server or multiplayer acceptance.

## Current batch

| Work | Source | Package | Verification |
|---|---|---|---|
| Update obsolete test probe to current boss/Grand policy | Implemented; test-only code | Never ship probe JAR | Build PASS; exact R3 engine run PASS (exit0) |
| Native boss rewards and required item/unique registries |600 synthetic reward-factory samples prepared | Production R3 unchanged | Native factory PASS on R3 and R4:600 samples each,13 Regalia,57 native uniques; no natural-kill/party claim |
| DD candidate dimension evidence | Query actual structure registry and normal-preset biome overlap | Seven zones implemented in source; R4 full ZIP built and static/native-fixture verified | 112 candidate observations collected from actual registries; biome eligibility is not natural-generation proof |
| Next source-backed DD zone batch | Seven added: Abandoned TempleT4, KisegiT4, Corsair CorvetteT4, MausoleumT4, Underground CampT2, Bandit VillageT2, Mining ComplexT3 | R4 full ZIP built and static/native-fixture verified | Registry and normal Overworld biome checks PASS; Mining System held (zero normal Overworld biome matches) |

## Still incomplete

- Broader Regalia curation:497 catalogue rows,421 previously unscored; do not auto-approve them. Native-only exclusions and native boss trophies remain protected.
- T2/T3 boss identities and several native combat routes remain unresolved. Cornelia and Last of Deepslate combat changes are not implemented; Hydra ordinary damage and fixed ability damage remain open. Do not duplicate the separate later reinforcement addon.
- DD expansion beyond30 zones requires registered IDs, Overworld eligibility, effective resource/config checks and owner tier authority. T0/T1, Mechanical Nest blanket scaling, Pasterdream and non-Overworld rollout remain excluded/held.
- Grand coverage beyond14 mappings, native statistics, Lootr independent two-player generation, reopen/restart behavior and category reward quality remain unaccepted.
- T2 Scrap/Treasure increases need approved source-specific amounts. T9 rare extra odds deferred. No invented rates.
- Boss party credit/contribution fairness, delivery/respawn/restart behavior and natural combat acceptance remain unfinished.
- Dedicated-server startup/sidedness, normal-world generation, natural encounters, multiplayer, shaders/performance and staged Chunky acceptance remain open.
- Quest Atlas, custom menu and optional realm campaigns remain approved later work.

## Rollback and evidence rules

Keep previous ZIPs and rollback receipts immutable. Use new disposable profiles/worlds only. No active client/server installation or owner acceptance is inferred from a draft. New generation-affecting changes require a new package and updated rollback inventory. Record exact source/package hashes, test commands/results and blockers for every completed batch.

## Current batch evidence

[Native evidence and rollout](../handoffs/dd-native-batch-r4-20261015/rollout.json). Production R3 engine startup/world join/save exit0 and600 boss reward factory fixtures PASS; these are not natural fights or multiplayer. The new source DD total is30, retaining the23-zone baseline and unchanged attribute budgets/matchers. R4 passed archive checks and its own engine run:34/34 synthetic cases cover all30 scoped sites plus exclusions.105 Python tests pass. The test-only probe is never shipped.

Remaining source queue:78 native-eligible candidates await source/placement/content review;25 queried candidates have no normal Overworld biome match and1 has ambiguous normal dimensions. See [112-row remaining queue](../handoffs/dd-native-batch-r4-20261015/remaining-candidate-queue.csv). Current R4 rollout is30 zones, not497. Source plan marks the seven implemented rows. Historical R1 generator is guarded against reverting the expansion.

## Current preparation after R4: guarded R5 Grand Treasure candidate (15 October 2026)

No R5 gameplay import has been built or uploaded. R4 remains the latest private released ZIP and source/binary acceptance baseline. The R4 campaign (0.3.2, SHA256 `802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7`) already has **14 chest-specific Grand Treasure sources**. Compared with the newly source-verified native chest-content study, there are **exactly five remaining prospective pool-index changes**: Keep Kayra library and keep treasure 2→1, Adventure Dungeons Murky 0→2, and Iron's Spellbooks hidden trough 3→1/generic magic treasure 6→1. All preserve original native source-resource hashes, Tier 3+ chest contexts, bonus probability 5%, native drops and other R4 systems. These choices are **review-only**, not approved for shipping.

R4-based, fail-closed tools now committed to PR #64: `tools/preview_r5_grand_from_r4.py`, `tools/patch_r5_grand_from_r4.py` and `tools/package_r5_grand_from_r4.py`. Source-preview pins the exact Git blob of R4's JSON policy; JAR patching pins the actual published R4 ZIP SHA256 and 0.3.2 compiled addon SHA, requires individual native-source/Paxi/category review, and changes only `ao_loot_policy.json` inside a copy of that JAR. The full-import packager preserves all 337 CF refs, 10 custom JAR names, 30 DD zones and other R4 content; creates separate rollback and digest reports. No unrelated Java compilation or original-release changes.

**Synthetic CI:** [30/30 tests PASS](https://github.com/alsynth/AmbientOdyssey/actions/runs/38753512071), including blocked unsafe approvals, invalid R4 source hashes and unchanged original content. CI generated review-only candidate JSON and five DENIED-by-default review forms; they are NOT Minecraft runtime certification. Actual 338-JAR local installed-profile audit and Paxi winner, owner per-pool category approval and two-player Lootr acceptance are still required; only then should Claude produce a *separate* R5 private test import and record its real SHA256. Complete [Claude execution instructions](../handoffs/r5-grand-from-r4-20261015/CLAUDE_R4_TO_R5_LOCAL_EXECUTION.md). Do not confuse the older PR #63/R2-based R3 staging files with this R4-based work.

## Current-state reconciliation (15 October 2026)

Local 338-JAR profile is pre-R4 (v0.4.9.1); R4 ZIP hash verified; one packaged conflict found (ao_campaign_gates Pinnacle override). Report: [R4_CURRENT_STATE_RECONCILIATION_20261015.md](R4_CURRENT_STATE_RECONCILIATION_20261015.md). Read-only; no gameplay files changed.
