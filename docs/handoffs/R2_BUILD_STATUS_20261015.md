# R2 build status — what is done, what is not (15 Oct 2026)

**No R2 ZIP exists yet.** The sandbox that did this work cannot reach the NeoForge/Apotheosis Maven hosts, CurseForge, or the private PR50/R1 base ZIP and draft release, so the Java could not be compiled and nothing could be packaged. Everything below is source-side and ready for `python tools/build_r2.py` on a machine that has those inputs.

## Done in this pass
| Item | File | Status |
|---|---|---|
| Unique-tag normalisation (string + `{"id","required"}` records); optional IDs preserved in `unique_weapons_optional` | `tools/compile_additive_loot_policy.py` | Fixed, ran OK: 32 boss IDs, 58 unique weapons, 9 Regalia, 14 Grand contexts |
| `ao_loot_policy.json` generated (required at runtime by `BossRewards`) | `addons/ao-campaign/src/main/resources/` | Generated |
| Packager targets campaign **0.3.0**, refuses stale/missing JARs, checks classes, policy, modifier list, metadata version; new R2 name/version/notes | `tools/package_master_integration.py` | Edited, not run |
| Validator expects exactly `["ao_campaign:grand_treasure"]` (no Rage Glove, `replace:false`), classes, policy, one campaign JAR, no gem suppression pack file | `tools/validate_master_integration.py` | Edited, not run |
| Tests updated + new loot-contract and no-gem-grant tests | `tests/test_master_integration.py` | 6/6 pass |
| Obsolete gem-suppression file removed from economy packager | `tools/package_ao_loot_economy_pilot.py` | Edited |
| Log-probe points at 0.3.0 | `tools/log-probe/build.gradle` | Edited |
| Journal: removed dead `artifact/heirloom/esoteric_reward` milestones; the 3 quests keep stable IDs but are now honest native-gem read notes; Pinnacle wording removed | `tools/compile_ao_v050_campaign.py`, overlay quests, mapping CSV | Regenerated (101 new quests, 86 read-only) |
| `GrandTreasure`: rejection/cache now reset on resource reload (blocker 12), synchronized | `GrandTreasure.java` | Edited, uncompiled |
| `BossRewards`: Remnant `remnant_bosses:` alias, one-time diagnostics for skipped Regalia/unique IDs | `BossRewards.java` | Edited, uncompiled |
| One-command build | `tools/build_r2.py` | New, not run |

Java files parse with no syntax errors (checked with `javax.tools`; 100 diagnostics, all missing-symbol from absent NeoForge/Apotheosis jars). **API correctness against NeoForge 21.1.252 / Apotheosis 8.9.0 is unverified**; the highest-risk assumptions are `LootController.createRandomLootItem(GenContext, LootRarity)`, `LootRarity.random(GenContext)`, `GenContext.forPlayerAtPos`, and `LootTable.DIRECT_CODEC` parsing with `RegistryOps`.

## Exception ledger (genuinely undecided, not hidden)
1. **T2 Scrap/Treasure boost** — per-source amounts unapproved; not implemented.
2. **Regalia breadth** — only 9 IDs are in the policy (7 low-risk Artifacts + Abyssal Tiara + Tempest Trident). The ~90%-of-suitable-≤T5 goal needs registry validation against the installed JARs; 421 catalogue rows remain unscored. Annihilator unapproved.
3. **Grand "best pool"** — the 14 mappings come from a scoring heuristic, not owner review. Several Keep Kayra / Irons tables borrow a sibling table's pool.
4. **Boss mapping gaps** — T2/T3 identities, Eternal Starlight family, underground vs surface dragons, Mechanical Nest boss, and T9 rare-extra odds are unmapped/deferred. Policy has a Twilight Forest hydra at T4 and Iron's/I&F hydra at T7; confirm both are intended.
5. **Obsidilith** is rewarded in any dimension by `BossRewards` (the journal milestone is End-only). Decide whether to match.
6. **Party credit** — one set per credited killer is an unreviewed assumption.
7. `RageGloveGate.java` stays registered but inactive (not in the global modifier list). `BossGems.java` is unreferenced.

## Run on your machine
```
python tools/build_r2.py --base <PR50 zip> --out build/Ambient-Odyssey-MASTER-INTEGRATION-R2-ALL-DECIDED-PRIVATE-20261015.zip
```
Needs the pinned dependency/custom-JAR inputs the existing packager already reads. Expect the first Gradle compile to surface API mismatches in the two new classes; fix and re-run.

## Continuation prompt for Codex
"Fetch the R2 branch, record its HEAD and the ZIP SHA256, then run the section 14 tests from CLAUDE_COMPLETE_IMPORT_ZIP_HANDOFF_20261015.md in order. Mark every result PASS/FAIL/NOT RUN. Do not reuse R1 evidence."
