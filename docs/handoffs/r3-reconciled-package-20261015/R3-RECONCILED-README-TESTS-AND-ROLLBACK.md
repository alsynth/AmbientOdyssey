# Ambient Odyssey R3 â€” private import and test instructions

15 October 2026. Source: 7ea67e72ba3bea0877cc1910f29335a0d82f5603.

Import: Ambient-Odyssey-MASTER-INTEGRATION-R3-RECONCILED-PRIVATE-20261015.zip
Size: 154493498 bytes.
SHA256: 5debe094c047162f0b30f2dd76e2ab85201310c480b64333eca89a4f4376ac99

This is a full CurseForge import, not an update kit. Minecraft 1.21.1, NeoForge 21.1.252, 337 pinned CurseForge references and 10 bundled custom JARs. Expected installed inventory: 340 production JARs. CurseForge downloads the referenced mods during import; this ZIP is not an offline collection of all mod downloads.

## What is included

All currently implemented integration source: 23 scoped Dungeon Difficulty zones, native boss config balancing and approved exemptions, starter/trade/ring integrations, rarity and Sigil changes, existing quests/manual/UI/worldgen fixes, and rebuilt campaign 0.3.2. R3 adds additive per-kill affixed equipment, curated Regalia and Simply Swords UNIQUE-only bonuses for mapped bosses, independent T6â€“T8 extra affix chances, the draft 5% native-pool Grand Treasure modifier, and restoration of native gem progression. Obsolete bespoke gem quest rewards and automatic Pinnacle unlock wording have been removed while preserving quest IDs. Rage Glove experimental modifier remains inactive.

This packages implemented code, not every design goal. Current policy has 32 boss IDs, 13 curated Regalia IDs, 58 unique-weapon tag records (optional entries validated at runtime), and 14 source-derived Grand chest candidates. Wider Regalia coverage, some boss mapping/combat routes and remaining chest coverage and Lootr acceptance remain incomplete. T2 Scrap/Treasure increase has no approved numeric amount and is omitted. T9 rare-extra rates remain deferred. Grand/Lootr behavior and party attribution are unaccepted. Refer to the complete source handoff and R3 intake/status ledger for the full exceptions.

## Verification

PASS: clean compilation/build of starter 0.2.0, Sigils 0.1.1 and campaign 0.3.2 against cached dependencies. Gradle has no Java test sources; these builds are not native GameTests.
PASS: actual import CRC, unique archive members, 10 custom-JAR integrity, current campaign classes/policy/modifier list, 337 unique pins, SkyArena exclusion, 23 DD zones, 153 quest files, exact native config/defaultconfig pairing.
PASS: 1021 JSON, 188 JSON5 and 289 TOML files. 24 shader preprocessor sources with JSON filenames excluded from plain JSON lint.
PASS: two exact Bonus Chest affix-only exemptions and seven approved World Tier rarity weight edits; native gem injector untouched.
Python suite: 99 tests, all PASS after updating obsolete historical source expectations to the approved 52-quest base and intentional Hominid exclusion.
Dependency metadata: 340 production JARs, no direct issues/duplicate top-level mod IDs. Some embedded/bridge dependencies and metadata coverage remain warnings. No dedicated-server compatibility claim.
NOT RUN: R3 Minecraft launch, natural generation/fights, loot statistics, two-player Lootr, dedicated server, save/restart, ability scaling, shaders/performance. Older R1 runtime evidence does not validate this R3 package.

## Test this exact ZIP

1. CurseForge: Create Custom Profile / Import, select this ZIP and choose a NEW profile. Confirm Minecraft 1.21.1 and NeoForge 21.1.252. Let all referenced downloads finish. Keep existing profiles untouched. Record installed JAR count and latest.log.
2. Launch with Java 21. Create a disposable NORMAL AO/FTF world with cheats and Bonus Chest ON, not a flat world. Save seed. Run `/datapack list enabled`. Open journal/manual and verify stable quests and gem information. Native Apotheosis progression must remain authoritative.
3. Open the world-created Bonus Chest. Confirm vanilla content plus one spellstone, one genuine added affixed item, added torches/meat. Native gems may drop normally. Check logs for AO_BOSS_BONUS_BLOCKED, AO_REGALIA_SKIPPED and AO_UNIQUE_SKIPPED; optional absent unique IDs alone are expected diagnostics.
4. For a direct boss-loot smoke in this disposable world, use `/summon irons_spellbooks:dead_king ~ ~ ~`, attack it as a player, and finish the fight with player damage. Avoid relying solely on `/kill`, which may not carry player credit. Count one added affixed item, one Regalia and one unique weapon separate from native drops. Repeat the kill: bonuses must remain available. Dead King uses T6 loot classification; additional ancient/artifact rolls are independent chances, not guaranteed. Repeat using a natural arena encounter; the summoned fixture does not prove that fight works.
5. Fight representative naturally generated bosses and record HP/ordinary damage/phase or scripted ability damage separately. Chesed, Malkuth and Geburah retain original combat stats and T5 loot. Cornelia T6 loot is included but her missing verified combat-scaling route remains a blocker. Shared surface dragons and Mechanical Nest ordinary mobs remain excluded from blanket scaling.
6. Visit genuine mapped T3+ dungeon chests. Record structure/table/coordinates and results across many fresh chests; Grand chance is only 5%, so a few misses prove nothing. Grand output should be one bonus draw from the mapped native pool, with native contents retained. Test T0â€“T2 and unrelated shared-table chests as negative controls. A `/loot` command outside a structure is not a positive Grand test.
7. On a fresh disposable dedicated server, have two players open the SAME Lootr chest. Record each inventory, reopen/relog, restart and reopen again. Existing personal loot must not reroll. Repeat per-kill boss rewards and player credit checks. Do not copy the client mods folder blindly to a server; server sidedness/startup remains a separate acceptance gate.
8. Verify new-world serverconfig copies of Iron's Spellbooks and Block Factory match shipped defaults, DD ordinary-mob behavior inside/outside T2â€“T6 structures, Goblin prices, Flight Ring recipes, Sigil costs, held-item mastery once-only behavior, Q/E UI, Mine Cells return and Simply More stun/flash suppression.
9. Save, exit completely and relaunch. Preserve latest.log, crash reports and seed/coordinates. Return PASS/FAIL per case and the package SHA256. Do not pregenerate a production world until natural worldgen and server tests are accepted.

## Rollback

Use a separate profile and disposable saves for this test. To return to your previous client, open its untouched profile. There is no current server package to migrate; rebuild server separately after acceptance. Never downgrade a generated world in place. Restore the pre-test save backup together with its matching full profile/version.

The companion R3 Rollback ZIP contains byte-exact PR50 originals for changed/removed members and ROLLBACK-RECEIPT.json listing newly added paths to remove. It is NOT a CurseForge import and does NOT restore worlds. For an exact PR50 return, import the original full PR50 ZIP into a separate profile and use its matching pre-test save. Original 39-config rollback baseline remains in Git. Stable/main unchanged.

R3 audit additions: restored new-world FTB Solo Quests teamSyncEnabled=false; added four source-verified crafted Eternal Starlight Regalia (Dagger of Hunger, Chain of Souls, Soulit Spectator, Etheric Eye). See R3-DRAFT-AND-PLAN-AUDIT.md and R3-PLAN-COVERAGE.json. On a new dedicated world inspect world/serverconfig/ftb_solo_quests-server.toml and test two same-team players earning FTB quest progress independently. Existing saves require checking their existing serverconfig; a shipped default does not change them.

Latest integrated owner correction: all14 Grand mappings now take one selected valuable native pool from their own triggering chest table; the former8 cross-table choices are gone. Installed-source hashes and selected pool types pass, and no mapped Paxi table override was found. Preserve the5% independent chance, native contents/weights/functions, and test real Lootr behavior. See R3-RECONCILED-DRAFT-AND-PLAN-AUDIT.md, R3-RECONCILED-NATIVE-SOURCE-AUDIT.json and R3-RECONCILED-PLAN-COVERAGE.json.

Additional concurrent source-only updates through4b21f0c were merged after archive creation: review-only candidate generator/ledgers, configurable native audit input and6 new synthetic tests. The new preview tool now reads the preserved historical R2 mapping, so it cannot mislabel active R3 mappings as R2. These tools/docs do not alter the packaged runtime payload; final suite99/99 PASS. Package gameplay source7ea67e7 remains the receipt basis.

Final review-only commit d49d7bc merged;99/99 Python tests PASS. Shared branch kept intact; reconciled build saved on experimental/master-integration-r3-reconciled-20261015 to avoid concurrent upload races.
