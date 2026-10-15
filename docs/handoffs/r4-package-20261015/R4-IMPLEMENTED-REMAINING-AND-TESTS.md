# R4 implementation batch — 15 October 2026

## Added in source and the full R4 ZIP

Seven owner-selected Dungeon Difficulty zones, based on actual registered structures and biome intersection with the normal world preset:

| Structure | Tier |
|---|---:|
| dungeons_arise:abandoned_temple |4|
| dungeons_arise:kisegi_sanctuary |4|
| dungeons_arise_seven_seas:corsair_corvette |4|
| iceandfire:mausoleum |4|
| adventuredungeons:underground_camp |2|
| dungeons_arise:bandit_village |2|
| dungeons_arise:mining_complex |3|

Total scoped zones:30 (previous23 retained). Same approved T2–T6 attribute budgets and vanilla-hostile matchers. No new T0/T1, non-Overworld/Pasterdream rollout, Mechanical Nest blanket zone, Frosted Prison or Sunken City. Boss categories/combat exceptions are unchanged. Mining System remains held: registered ID, but zero normal-Overworld eligible biomes in this exact resource stack.

The consolidated497-row plan now marks the seven source implementations explicitly. A separate112-row evidence queue records what remains:78 candidates still need source/placement/content review,25 had no normal Overworld biome match,1 had ambiguous normal-dimension matches,8 already active in this queried subset (including the pre-existing Dungeon Crawl). This subset is not the entire497-row plan, and biome eligibility does not prove natural placement.

A historical R1 reconstruction script now refuses to overwrite this later recorded expansion. Current source packaging uses tools/package_master_integration.py. The exact seven-row before/after and native evidence are under docs/handoffs/dd-native-batch-r4-20261015/.

## Exact R4 package

Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip
154493674 bytes.
SHA256:31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d
Gameplay source:9a2af79d787486eadb1de26d7cf0535807402686.
337 CurseForge references,10 bundled custom JARs,340 expected production JARs,153 journal entries,30 scoped DD zones. Import as a NEW CurseForge profile; app downloads official referenced mods.

All production JARs and official pins are byte-identical to R3 RECONCILED. The ONLY changed archive members are manifest.json, the DD config and AO_TEST_NOTES/MASTER_INTEGRATION.txt. The package receipt's dirty-source flag is true because the non-packaged remaining-candidate-queue.csv was being recorded; no additional runtime payload change was present. Complete member hashes and byte-exact PR50 rollback receipt are provided.

## Verification status

PASS: current105-test Python suite, test-probe compilation, actual R4 ZIP CRC/unique entries/JSON/JSON5/TOML/custom-JAR/source-policy/DD membership checks. Actual R4 validator counts1021 JSON,188 JSON5,289 TOML; shader preprocessor JSON-named files excluded from plain JSON lint.

Exact R3 RECONCILED engine baseline PASS: production startup, world join/save-exit0,600 boss reward factory samples,13 curated Regalia and57 native unique items (one optional tag record absent),600 Bonus Chest samples,153 native quest parse and synthetic DD controls. No custom gem-grant or obsolete Rage Glove filter test was used. R3 native results are not automatically transferred to R4.

The exact R4 production-engine run PASS: startup/world join/save-exit0;30/30 scoped structures registered;34/34 synthetic DD cases PASS, covering all30 sites plus exclusion controls;600 native boss reward factory samples PASS;13 curated Regalia/57 native unique items validated;600 native Bonus Chest samples and153 native Questlog entries PASS. This is not natural generation, combat, party credit or Lootr certification. The new test-only probe exercises every one of the30 DD sites, not only one per tier, with exclusion controls. Probe JAR never belongs in the production ZIP.

## Not finished

Natural structure placement, real spawners/fights, elite stacking, ability scaling, respawn, boss contribution fairness, dedicated-server startup, two-player Lootr/reopen/restart, shaders/performance and Chunky acceptance remain open.13 Regalia is not the broad90% goal;T2/T3 boss identities and unimplemented native combat routes remain unresolved. T2 Scrap/Treasure increases have no approved exact amounts. T9 extra rarity odds remain deferred. No new source-only/engine fixture evidence is owner acceptance or a live installation.

## Exact owner tests and rollback

1. Import this R4 ZIP as a new profile; create a disposable NORMAL AO/FTF world with cheats. Confirm MC1.21.1 / NeoForge21.1.252. Save seed and logs.
2. Run one bounded `/locate structure <ID>` at a time using the seven IDs above. Visit a real generated site; record complete rooms, mob spawner behavior and normal loot. Synthetic bounding boxes do not prove this.
3. Observe ordinary eligible mobs inside and outside each structure. Record max health/attack/armor before and after save/restart, and separately assess Brutal/Apotheosis stacking. Existing DD budgets remain unchanged; T4 ordinary targets:+200%HP,+80%attack,+8armor, T3:+150%,+60%,+5; T2:+100%,+40%,+3.
4. Repeat prior R3 boss rewards/unique-only/native gems, journal/mastery and new-world Solo Quests tests. A normal fight, two-player credit and Lootr persistent individual loot are still required.
5. Do not pregen production until normal worldgen/server acceptance. Preserve pre-test save backups. Return to the untouched previous profile plus its matching pre-test save to roll back; never downgrade this generated world in place. Companion Rollback ZIP is a byte-exact PR50 changed-payload restoration kit with added-path removals, not a CurseForge import or world backup. R3/R2 archives remain immutable.

## Final verification references

R4-STATIC-VERIFICATION.json and R4-DELTA-FROM-R3.json audit the actual archive. Native INPUT_SNAPSHOT.json binds production inputs to the exact R4 ZIP hash; RESULT.json, MASTER_NATIVE_OBSERVATIONS.json, BOSS_REWARD_NATIVE_OBSERVATIONS.json and PR45_ORDINARY_RULE_TESTS.json hold actual engine results.105 Python tests PASS. Dedicated-server and two-player gameplay remain NOT TESTED. Known inherited mod book/recipe/tag/advancement diagnostics remain; no error-free log or performance improvement is claimed.
