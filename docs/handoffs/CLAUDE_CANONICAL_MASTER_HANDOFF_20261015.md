# AMBIENT ODYSSEY — CANONICAL CLAUDE MASTER HANDOFF
**Snapshot: 15 October 2026, after R4 + PR64 R5-Grand preparation.**
**Project:** Minecraft 1.21.1, NeoForge 21.1.252, exploration/RPG multiplayer (approximately 5–7 players).
**Authority:** Latest explicit owner decisions > this reconciled ledger > actual published R4 binary/receipt for packaged facts > effective installed-profile JAR/config evidence > current PR64 source > older PR63/other draft evidence > historical docs. A document being recent does not make its proposed change shipped.

> START HERE. This file supersedes obsolete “current version”, “next agent” and “ready for release” labels in historical TODO/AGENT_WORKFLOW/CURRENT_STATE, older R2 and PR57 notes. It does NOT replace detailed underlying evidence. Every item has separate SOURCE, PACKAGED, STATIC/ENGINE, OWNER GAMEPLAY and LIVE status.

## 0. Executive summary — what Claude must do
- **Use PR #64** (branch experimental/master-integration-r3-reconciled-20261015) as the **latest consolidated development source**. Do not start from old PR63/R2 handoff, main, Oct10 v0.4h, PR57 or the isolated PR62 DD pilot. Make a NEW child branch for actual implementation.
- **R4 is the last full published private import**, not R5. It is a GitHub draft release, not proof of owner installation, server readiness or worldgen freeze.
- **R4 already implements 30 scoped Dungeon Difficulty zones, 14 same-chest native Grand Treasure mappings at 5%, campaign 0.3.2, 32 boss-reward entity IDs, 13 selected Regalia IDs, 58 Simply Swords unique-tag policy entries, 153 Questlog quests, native gem preservation and the 70/30/x4HP/x3DMG Brutal Bosses setup**. These are the INCLUDED system baselines, not “all remaining work”.
- **R5 Grand work in PR64 is a complete TEST-BUILD TOOLCHAIN, NOT A BUILT R5**. Exactly five source-verified, chest-category-better native pool selections are proposed, and 30 synthetic tests passed; individual approval, actual current profile/Paxi inspection and two-player Lootr are missing.
- **Major remaining implementation:** broaden eligible Regalia (not indiscriminately), implement the owner's newer **full verified Simply Swords sword pool** rather than the older unique-only pool, source-map T2/T3 bosses, finish blocked boss combat routes, expand source-confirmed DD/loot, decide T2 Scrap/Treasure amounts, verify real worldgen/server/party mechanics, then performance and pregen.
- User says **Claude has the complete current installed modpack with 338 JARs, configs and assets**. This is user-provided availability, NOT GitHub artifact verification. Claude must confirm readable local paths. The published R4 manifest documents **337 CurseForge references + 10 bundled custom JARs, expected 340 physical production mod JARs**. These numbers reflect different counting/baselines and may indicate client changes; inventory/diff is essential. Never replace files merely to force counts to match.
- **Do not silently finish by writing more planning docs.** Inspect executable resources/JARs, make verified source changes or explicit blockers, build separate reversible tests and report evidence.

## 1. Exact release/source authority and branching
| Build / branch | Concrete status | Where / why |
|---|---|---|
| **R4 FULL PRIVATE EXPERIMENTAL** | **LATEST full uploaded import; static + narrow native engine fixtures PASS; no multiplayer/natural fight acceptance** | GitHub draft release https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-3d9c2fc62334621d6b59 |
| R4 archive | Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip; 154,493,674 bytes; **SHA256 31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d** | docs/handoffs/r4-package-20261015/package-receipt.json |
| R4 source | PR **#64**, experimental/master-integration-r3-reconciled-20261015; R4 packaged gameplay source **9a2af79d787486eadb1de26d7cf0535807402686** | https://github.com/alsynth/AmbientOdyssey/pull/64 ; branch now also contains later **R5-preparation-only commits**. R4 receipt has dirty-source flag; binary receipt is executable truth. |
| R4 bundled campaign | overrides/mods/ao-campaign-0.3.2-experimental.jar; **SHA256 802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7** | Packaged binary is version 0.3.2; do not apply R2 0.3.0 patcher. |
| R3 RECONCILED | Previous full import, R3 campaign 0.3.2, 23 DD zones, corrected 14 own-table Grand sources, 13 Regalia, Solo Quests default; superseded as launch test baseline by R4 | docs/handoffs/r3-reconciled-package-20261015/, SHA256 5debe094c047162f0b30f2dd76e2ab85201310c480b64333eca89a4f4376ac99 |
| R2 / PR63 | Historical 0.3.0 addon, 23 DD zones, 9 Regalia and old cross-table Grand candidate model; separate **later native-JAR research, five thematic proposals and testing tools** landed on PR63 | https://github.com/alsynth/AmbientOdyssey/pull/63 . Research can be ported selectively; do NOT use PR63 as the R4 binary base. |
| R1 / PR50 / PR57 | Historical reconstructions / prototype binaries and source evidence only; untouched rollback baselines | Do not replay old packaging scripts over R4. |
| **R5 GRAND TEST CANDIDATE** | **NOT created, not released, not installed**. PR64 contains five-delta review, 0.3.2 resource-only addon patcher and full R4->R5 import/rollback builder | docs/handoffs/r5-grand-from-r4-20261015/CLAUDE_R4_TO_R5_LOCAL_EXECUTION.md |
| Main/stable | Do not assume any draft PR merged; do not force merge to stable/main | Continue on isolated branches and releases. |

R4 factual evidence: docs/status/IMPLEMENTATION_PROGRESS.md; docs/handoffs/r4-package-20261015/R4-IMPLEMENTED-REMAINING-AND-TESTS.md; R4-STATIC-VERIFICATION.json; RESULT.json; BOSS_REWARD_NATIVE_OBSERVATIONS.json; DD_EXPANSION_REGISTRY_OBSERVATIONS.json; R4-DELTA-FROM-R3.json. R4 checks: 105 Python tests, 1,021 JSON/188 JSON5/289 TOML static checks, native production client startup/world join/save/exit, 34/34 synthetic DD cases across 30 zones, 600 boss reward factory samples, 600 Bonus Chest samples and 153 quest parses. Native tests verified 13 Regalia and **57 registered** unique weapons of 58 optional candidate/tag records. **No natural structure spawn, real boss kill credit/party, Lootr multiplayer, dedicated-server or performance pass is certified**.

## 2. Status vocabulary REQUIRED in all follow-up deliverables
- **DESIGN APPROVED** = owner's intent accepted; not proof executable IDs or working JAR.
- **RESEARCH / SOURCE EVIDENCE** = JAR byte/registry/loot table verified, but no changed runtime payload.
- **SOURCE IMPLEMENTED** = committed code/config; may not be in current import.
- **PACKAGED R4** = present in exact R4 ZIP, regardless of local user's installation.
- **STATIC VERIFIED** = hashes/schema/test fixtures only; cannot establish gameplay.
- **NATIVE ENGINE FIXTURE PASS** = real Minecraft engine used under controlled/synthetic conditions, **not** normal encounters.
- **OWNER GAMEPLAY ACCEPTED / DEDICATED SERVER PASS / LIVE INSTALLED** = require separate recorded observation. Never infer these.
- **HELD / NOT IMPLEMENTED / DEFERRED** = do not create speculative registry IDs, rates or goals.

## 3. Recent changes by version (do not re-do)
**Oct 10–12 content/worldgen/UI wave — inherited via full import where source/binary confirms:**
- Mine Cells Fabric/NeoForge Connector + dependencies, compatibility bridge and portal/return loop; owner previously verified return. Check latest actual mod/loader configuration. Mine Cells first arc belongs in Questlog; no mandatory custom-engine starting dimension.
- Curated Free TerraForged terrain/biomes, biome/structure eligibility, Paxi repairs, integrations, WDA/Integrated structure fixes including historic 273 jigsaw template repairs. Native source does NOT prove final natural placement or terrain frequency.
- Sources contain AO worldgen safety addon, Tan trees stop-hang workaround research, structure tag/loot/recipe fixes; do not replace old patches blindly.
- Later full client experiments addressed Seven Curses Enigmatic inventory chest icon, Questlog Q/E button positioning, tooltip wheel collisions, BetterEnd popups, and removed crash-prone Subtle Effects; current UI smoke is narrower than owner gameplay acceptance.
- Random trims on Apotheosis affixed loot developed as ao-affix-trims 0.1.1 with native-source/GameTests; runtime chest AND mob-drop coverage needs genuine sampled confirmation.
- Experimental r19/0.4.8 Apotheotic prototype and Wet Sand source prototype bundled; **prototype bundled ≠ fully ported/fully validated**. Preserve their exact versions/hashes; inspect JAR contents and missing feature status rather than treating them as newly requested downloads.
- Performance shader presets (AO Performance/Balanced/Quality), renderer/tooltip/visual ecology candidates and Spark tooling exist; no reliable current R4 shader FPS/MSPT gain proven.

**Oct 13–14 balance/planning integration:**
- PR49 Regalia catalogue/risk ranking covers **497 candidate rows, 421 unscored**, a review/research set, NOT 497 approved source-registered boss drops.
- PR51 starter bonus, Goblin Tuned trade pricing, optional ring recipes, Lootr configuration; PR53 world-tier rarity data edits; PR54 Sigils rarity-cost addon; PR57 experimental campaign and partial boss loot. R2/R3/R4 packages reconcile source changes and intentionally remove older invalid gems / forced Pinnacle unlock / 10% Rage Glove gate.
- PR59 config is final **Brutal Bosses chance 70 / minimum distance 30 / HP x4 / damage x3**; generator-related chance/spacing must be final before irreversible pregeneration.
- PR60 arena/boss roster gate is a source audit, NOT proof missing/present boss structures in installed R4.
- PR61 continuity docs are historical context; PR62 stronger Dungeon Difficulty standalone pilot is NOT a fully active independent 497-zone list.
- PR50 pinned full import is historical source basis. PR64 now owns the consolidated source.
  
**Oct 15 shipped waves:**
- **R1:** full master integration attempt, rollback/test draft. Do not use as baseline over newer builds.
- **R2:** campaign 0.3.0, source-backed bonus boss rewards, native Apotheosis gem restoration, starter/trade/ring fixes, 23 DD zones and original 14 Grand contexts with eight structure-wide borrowed pools. The old cross-table source selection is superseded.
- **R3 RECONCILED:** campaign 0.3.2, 13 curated Regalia (four Eternal Starlight craftable additions), true per-chest own-native Grand source mappings, 14 contexts, FTB Solo Quests server default teamSyncEnabled=false for NEW worlds, other R2 systems unchanged; 100 tests, native R3 later engine fixtures.
- **R4:** 7 approved DD zones added (23→30), all source-registered/normal Overworld climate verified; R4 **only changes manifest, DD config, test notes from R3**. Official mod pins and bundled custom JAR binaries are identical to R3; 105 tests plus R4 engine fixtures as in section 1.
- **Post-R4 / PR64 R5-PREP ONLY:** compared exact 14 R4 Grand mappings with PR63 pinned native loot source evidence: **nine already match** and precisely **five pool indices differ**. Added R4-exact preview, review/approval form, campaign 0.3.2 JSON-only binary patcher, full private R4→R5 packager with rollback and guard tests; **30 synthetic tests PASS** at https://github.com/alsynth/AmbientOdyssey/actions/runs/38753512071. Neither R5 nor these pool changes exists in the published R4 ZIP.

## 4. Feature-by-feature implementation ledger (as of this handoff)
| Area / owner direction | Actually done / where | Missing, risk or test |
|---|---|---|
| **Core pack/roster** | R4 full import; 337 CF refs; 10 custom JARs; expected340 installed; report paths in §1 | User provided Claude 338 JARs; compare SHA inventory, client-only/server-only, added/updated files; no unsupported auto-addition |
| **FTF terrain/curated biomes** | release_030/overrides/config + Paxi datapacks; old worldgen source audits; R4 inherits | Natural normal-world distribution and modded vs vanilla climate check, biome empty structure eligibility, Prairie/Sakura dominance, peaks/stony shores/rare caves, freeze/seed acceptance |
| **WDA/Integrated/other structures** | ao_structure_repairs and source tags; historic 273 jigsaw repairs; approved structure frequency patches; SkyArena removed from R3/R4 | Actual generation and complete arenas, spawners, IDAS houses, Farmers Structures, bridges, dragon caves, structure conflicts. Don't blindly change frequency before sampling |
| **Boss arena roster/pregen gate** | PR60 gate, arena dossiers, NEXT_AGENT_PACKAGE files 00–21 in docs/research, 39 config snapshots in historical handoff | Final /datapack list, structure/portal references, one-off/respawn rules, boss presence, full normal-world checks; no production Chunky |
| **Brutal Bosses** | R4 includes 70/30/x4HP/x3DMG config | Verify active R4 client/server config on the actual pregen world. No stale x4/x4, no edits to boss files, dummyboss or spawn tables |
| **DD T2–T6 attributes** | R4 release_030/overrides/config/dungeon_difficulty/difficulty_v2.json with 30 eligible zones. T2 +100%HP/+40%attack/+3armor; T3 +150/+60/+5; T4 +200/+80/+8; T5 +250/+100/+11; T6 +300/+200/+15 | Test normal mobs spawned in actual structures, stacks with Brutal/Apotheosis, reload/multiplayer; no blanket T0/T1, Mechanical Nest, Pasterdream or non-Overworld |
| **Seven R4 DD additions** | dungeons_arise:abandoned_temple T4; dungeons_arise:kisegi_sanctuary T4; dungeons_arise_seven_seas:corsair_corvette T4; iceandfire:mausoleum T4; adventuredungeons:underground_camp T2; dungeons_arise:bandit_village T2; dungeons_arise:mining_complex T3 | Native 34 synthetic cases pass. Natural placement/real spawns still untested |
| **DD future mapping** | 497-row owner/design plan; R4 112-row native-query queue: 78 need review, 25 no normal Overworld biome intersection, one dimension ambiguous, eight already active in subset | Approve verified structures by tier/placement one batch at a time. Mining System held; no automatic 497-zone expansion |
| **Boss tier/balance routes** | 51 source-backed native boss config field edits and 32 reward IDs; native observation ledgers, R4 included | Not all T2–T9 HP/direct-attack targets achieved. Scripted ability damage, T2/T3 IDs, Cornelia, Last of Deepslate, Coralssus, Ice & Fire Hydra etc routes blocked/partial. HP cap ~1024 and effects/armor interactions matter |
| **Boss tier exceptions** | Latest decision ledger, 51 field records, R4 reward categories | Chesed/Malkuth/Geburah are T5 boss-class/exempt hit-count; Dead King/Cornelia T6 *loot* with T7 *combat* targets; T8 Ignis/Maledictus/Leviathan; T9 Tyros/Scylla/Obsidilith. Verify real values, abilities, separate arena tiers and natural spawn. Old files claiming Geburah TBD or Chesed T7 are superseded |
| **Boss base rewards** | addons/ao-campaign BossRewards.java, campaign0.3.2 JSON: per player-credited mapped kill T2–T9 design of one genuine affixed item, one curated Regalia, one unique-tag Simply Swords weapon; keeps native boss drops. 32 IDs mapped; R4 600 factory samples | No T2/T3 mapped IDs; owner-player credited killer gets one set, NOT one per party member. Natural fights, extra-loot ownership, delayed pickup, repeat, death, contribution fairness are not accepted |
| **NEWER Simply Swords target** | LATEST owner update in docs/handoffs/REGALIA_OWNER_REVIEW_QUEUE_20261015.md: separate **one random sword from ALL verified installed Simply Swords sword IDs**, not only unique-tag items | **NOT IMPLEMENTED IN R4.** Enumerate sword registry/classes from user's installed JAR (exclude non-swords accurately); change/add code as needed; verify compatibility and boss kill loops. Do not silently keep only 57 registered unique weapons |
| **Rarity extra affix boss drops** | R4 campaign policy rare_affix_rates T6 Ancient20%, Artifact2%; T7 Ancient25%, Artifact8%, Heirloom5%; T8 Ancient30%, Artifact15%, Heirloom8%, Esoteric5%; T9 deferred; 600 synthetic factory samples | Explicit native/live drop probability, 5–7 player economy and identity/tier tests remain. High-grade affixed *equipment*, not custom gems |
| **Regalia distribution** | R4 13 concrete item IDs, drawn from Artifacts, Aquamirae and four Eternal Starlight; source at addons/ao-campaign/src/main/resources/ao_loot_policy.json. 497-row catalogue,421 C? | Owner wants roughly **90% of verified eligible useful Regalia accessible by T5**, not 90% of 497 random catalog entries. Source-register/classify/acquisition first, keep boss-only native routes, add broad set gradually; current implementation grossly narrower |
| **Regalia hard exclusions/latest overrides** | Owner queue (read **last sections**): all Enigmatic Legacy + Plus native-only in new Regalia roll; Pasterdream **accessories** native-only, Qym native-only, Cursium native-only, The Annihilator unapproved. Native acquisition preserved | Earlier C4/C3 T2–T5 approvals of Pasterdream accessories, and T6–T7 The Infinitum bonus, are **superseded**. Aquamirae Tiara and Tempest verified in R4 pool; do not invent balancing nerfs. Simply Swords are now separate full-sword drop |
| **Grand Treasure R4** | campaign0.3.2 GrandTreasure.java + ao_loot_policy.json: 14 T3+ same-chest native source mappings, 5% extra draw, original source-table identities. R4 package and R3 reconciled native evidence | The category “best appropriate pool” is not proven for all; 14 of many dungeon sources, no two-player Lootr/reopen/real resource precedence. Maintain strict **additive-only native loot** |
| **Grand R5 candidate five improvements** | PR64 review file docs/handoffs/r5-grand-from-r4-20261015/REVIEW_ONLY_FIVE_POOL_DIFF.json plus exact R4-oriented tools. Proposed: Keep Kayra library treasure 2→1, keep treasure 2→1, Murky chest 0→2, Iron's hidden trough 3→1, generic magic 6→1 | **Source hash verified, choice not owner gameplay accepted**, need effective installed Paxi and loot quality/scroll level review + dedicated Lootr. No built R5 ZIP. Nine remaining R4 mappings unchanged |
| **T2 Scrap/Treasure** | Owner decision says additive native-source boosts starting T2 | **NOT IMPLEMENTED**: exact amounts and source tables not yet approved; do not invent global weights or replace loot tables |
| **Starter optional vanilla Bonus Chest** | addons/ao-starter-chest 0.2.0 built & packaged; native append/source fixture; retains original vanilla loot, chooses one Enigmatic Spellstone, genuine affixed gear (Common55/Uncommon30/Rare15), 32–48 torches,16–48 cooked meat | Independent Lootr/player rolls and one-time/reopen/restart actual gameplay remain missing; inspect Paxi Apotheosis affix exemptions for native-probability side effects |
| **Goblin Tuned, flight accessories** | PR51 integrated goblin trade datapack, ring recipes, Lootr config. Retain powerful 50% Goblin Tuned gear, scarce prices | Source-check exact item trade outputs, actual cost/probability and duplication/JEI in R4, rather than claiming every proposed price is live |
| **Apotheosis rarity/augmenting** | Four Paxi world-tier rarity overlays + seven accepted native weighting edits; Sigils addon 0.1.1 with Common–Mythic1/2; Ancient6/12; Artifact18/36; Heirloom24/48; Esoteric32/64 reroll/upgrade | Actual upgrade/GUI tooltip/rarity drop odds and world-tier gating in current profile to be tested; XP and gem costs intentionally high |
| **Gems** | Restored genuine Apotheosis gem crafting/source and no bespoke AO gem bonus/automatic Pinnacle unlock in R3/R4 | Confirm r19 prototype 60 gems and exact native upgrade in R4; **do not reintroduce AO gem drop/gate** |
| **Affixed armor trims** | Packaged addon ao-affix-trims 0.1.1, source factory/native tests | Real chest/mob drops with random valid trim + retained affixes/gem sockets/durability and Lootr still need in-game samples |
| **Apothic Additions/Wet Sands** | Bundled apotheotic port 0.4.8 PROTOTYPE and wet-sand 0.0.1 SOURCE PROTOTYPE, source/compat studies | No claim full port/gameplay completion; audit required APIs/recipes/3 extra rarity tiers/bosses and available version; avoid duplicate future mods |
| **Mine Cells + other dimensions** | Integration/portal return compatibility patches and Questlog intro; owner return portal verified historically | Test full R4 normal world, no overlap with Streams Reflowing, dimension travel/restart; optional realm campaigns pending |
| **Questlog/FTB** | R4 reports 153 quests (52 base +101 campaign), 20 chapters, FTB reference pages/manual; custom Q/E UI bridge and anti-duplicate rewards; FTB Solo Quests new-world teamSyncEnabled=false | Confirm actual menu/keybind/boss objectives, group vs solo, native completion/rewards/reload in R4; older docs claiming “no Questlog installed”, 50 quests or “Q1 only” are outdated |
| **UI/quality** | Better Inventory integrations, Enigmatic rings, tooltip fixes, anti-flash/stun changes in current integrated baseline | Test Q/E actual layouts, keybind search, BetterEnd popups, fatal flickering/stun and shader UI; custom AO menu/Quest Atlas later |
| **Performance** | Embeddium/NeoOculus/Lithium/FerriteCore/ModernFix/ImmediatelyFast and shader preset work, source-level performance/Streams/culling overlays | Bench actual 1440p FPS/1% lows/MSPT warm vs new chunks, shaders/Euphoria, weaker clients, hosted server/latency and Spark; don't claim numerical gain without apples-to-apples trials |
| **Chunky pregeneration** | Historical small pilot proposed or user-owned; staging advice already in docs/performance | NO full 10k–20k production radius acceptance. Pregen only AFTER worldgen freeze, exact server-side structure/brutal settings and 1k test of CPU/disk/stalls/restarts |
| **Player builds/later RPG** | Owner wants distinct multiplayer builds **without Origins**, quest atlas, optional dimension quests, late superbosses, rumors/treasure maps, menu | Planning/later, not packaged core gameplay; don't block worldgen/pregen for cosmetic or far-endgame content |

## 5. Latest binding owner corrections — do not revive older plans
1. **Brutal Bosses = 70 spawn chance / 30 minimum separation / ×4 health / ×3 damage.** docs/handoffs/BOSS_BALANCE_PACKAGE_INTAKE_20261015.md still incorrectly says x4/x4; historical 00–21 package says x1 or x3 placeholder. **R4 effective source is x4/x3**.
2. **Chesed/Malkuth/Geburah = T5 boss-category and exempt standard HP/direct-attack multiplier** due hit-count. Older boss research lists T7 / Geburah TBD; owner later overrode those.
3. **Dead King / Cornelia** retain T6 category/loot, but aim for T7 combat scaling; unimplemented native Cornelia route remains explicit. Do not promote reward tiers just to match combat.
4. Boss *target multipliers* (not promise of final implemented effect): T2 HP×2/direct DMG×1.5; T3×3/×2; T4×5/×3; T5×7/×4; T6×10/×5; T7×10/×6; T8×10/×10; T9×10/×10. Damage from projectile/skills may not follow attributes; 1024 HP cap observed. Later Claude boss addon is separate — avoid competing scalers.
5. Structure DD only applies to scoped ordinary Overworld hostiles T2–T6 with the approved separate attribute budgets in §4. Structure/arena tier ≠ boss rarity tier.
6. Simply Swords **latest owner change** requests full installed sword item pool as a separate guaranteed bonus; R4 has historical **unique-only** source. This discrepancy is a P1 coding item, not 58 IDs “sufficient”.
7. All **Enigmatic Legacy/Plus bonus Regalia** native-only, **NeoPasterDream accessories** native-only, Qym/Cursium native-only. Earlier “Enigmatic craftables downweight 90%”, “Infinitum T6–T7” and Pasterdream accessory T2–T5 approval statements are obsolete. Native crafting/loot always untouched. Starter spellstone is a separate exception.
8. Grand Treasure = **T3+ eligible chest, independent 5%, one EXTRA draw from a valuable fitting existing native pool per chest category**; prefer own chest table. Do not copy entire native table, duplicate trophy/quest loot, replace Apotheosis affix/gem chances or reroll once-opened Lootr.
9. Tier6/7/8 rare extra *affixed equipment* rates are present in R4 (§4). Gems stay native; no T9 rates fabricated; don't confuse gem grades.
10. T2+ Scrap/Treasure additions lack numeric approval, even though the intent is approved. No invented distribution.
11. Earlier PR57 automated Pinnacle unlocking, bespoke gem quest drops and Rage Glove 10%-Monstrosity special route were superseded/disabled. Do not restore.
12. Block Factory's Bosses and Bosses'Rise refer to the same owner-recognized mod. “Mother of Maze” is ordinary, not a boss. Tyros, Scylla, Obsidilith are T9; Ignis/Maledictus/Leviathan T8; no fabricated third T9 slot. Bosses need native source-backed IDs.
13. Final worldgen should retain owner-approved biome/structure identity, pregen timing and conservative Paxi repairs. Older worldgen notes (Prairie/Sakura, zero Stony Shore, weak mountains, Farmers houses, bridges, Ice&Fire rare caves, snow effects) are TEST OBSERVATIONS, not a license for another unmeasured overhaul.
14. Owner has declined **Origins**, Ocean Loot work, MCA Reborn, Big Globe, Mob Plaque and a mandatory Mine Cells starting dimension; no Explorer's Guild / discovered-conquered-mastered system. Avoid resurrecting rejected mods/ideas.
15. Quest Atlas, custom AO menu, optional dimension quests and distinct builds may follow worldgen. Endgame T9 need not be immediately defeatable.
16. No blanket reroll/replacement of native boss/chest loot; protect native mod-exclusive trophies/recipes/Apotheosis drops.

## 6. Specific files that are stale, contradictory or easy to misread
| File / branch | Why NOT to treat as current truth | Correct destination |
|---|---|---|
| docs/status/CURRENT_STATE.md | Header is newer but body still says “as of 10 October”, 331/329/318 pins, v0484 current, 50 Questlog quests | This file and docs/status/IMPLEMENTATION_PROGRESS.md, PR64 R4 receipts |
| docs/status/AGENT_WORKFLOW.md | “Current source” still names 10 Oct v0.4h, 331 refs, r19; even though newer paragraph mentions PR57 | New canonical handoff, R4 archive and PR64 |
| TODO.md | 158 KB historical mixed checkboxes with multiple “current release” claims (0.4/old phases); checks may refer to older variants | Treat as historical backlog only; do not treat [x] as present in R4 without binary/source comparison |
| docs/questing/QUEST_AUTHORING_VALIDATION_PLAN.md | says Questlog not installed and no quest JSON; accurate when written, false for R4 | R4 153 native quest parse evidence and current source |
| docs/handoffs/WORK_MODE_MASTER_IMPLEMENTATION_HANDOFF_20261015.md | valuable owner decision ledger but drafted before R3/R4, says only future candidate DD and earlier unique-only plan | Use as historical context, not build baseline; latest decisions in §5 |
| docs/handoffs/BOSS_BALANCE_PACKAGE_INTAKE_20261015.md | erroneous x4/x4 Brutal; says Geburah TBD | R4 70/30 x4/x3 source, later T5 protected exception |
| docs/research/next-agent-package-20261014/21_REMAINING_BLOCKERS_AND_OWNER_DECISIONS.md | some owner TBD/old spawn-damage placeholder overridden | Follow latest binding decisions, retain measurement gaps |
| docs/handoffs/REGALIA_OWNER_REVIEW_QUEUE_20261015.md | early rows provisionally approve Pasterdream accessories and The Infinitum; **last owner updates supersede early sections** | Read **bottom latest** and §5 of this handoff |
| docs/handoffs/GRAND_TREASURE_14_SOURCE_REVIEW_R3_20261015.md | upper part describes R2 8 cross-table borrowings; bottom describes R3 reconciled 14 own-table implementation | R4 actual policy + PR64 five-delta queue |
| PR63 docs/handoffs/R3_GRAND_14_OF_14_NATIVE_SOURCE_VERIFICATION_20261015.md | real verified published JAR loot sources/quality proposals; branch and artifact are NOT the latest R4 full integration | Port only the five evidence-backed pool choices via PR64 R4-based tools |
| PR63 tools/stage_r3_grand_policy.py and tools/patch_r3_grand_campaign_jar.py | built for older R2 campaign 0.3.0, not R4 0.3.2 | PR64 tools/preview_r5_grand_from_r4.py, patch_r5_grand_from_r4.py, package_r5_grand_from_r4.py |
| Old PR49 combat ranking | C4/C3 danger score is research, not automatic Tier8/Tier9 or live reward list | Current owner native-only and broad early-utility decisions |
| R3/R4 '57 or 58 Simply Swords uniques' | 58 policy records, 57 registered in engine fixture; newer owner wants full **sword** pool, not unique tag subset | Source full installed sword enumeration before new reward code |
| PR60 “Bosses'Rise missing by name” | name-only pin scan could miss Block Factory mod and user local additions | Inspect actual active mod metadata, not filename guess |
| historical engine test receipts | Client test fixture or flatworld pass is NOT natural combat, server, 2-player Lootr or worldgen freeze | New independent acceptance row/evidence |

Update the top-of-file navigation for CURRENT_STATE, AGENT_WORKFLOW and TODO if they are used for new agents; **do not delete history**. For every old draft, compare source paths to actual R4 member bytes and record a disposition: INCLUDED, PARTIAL, SUPERSEDED, BLOCKED, LATER or NOT APPLICABLE.

## 7. Do-next execution sequence — optimized for Claude Code with the full local modpack
**Stage 0 — inventory/authority (mandatory, lowest owner effort)**
1. Confirm Claude can read the user's complete **mods/** directory with 338 user-supplied JARs and every **config/**, **defaultconfigs/**, **kubejs/** (if present), **Paxi datapack**, quest and shader file; do not infer filesystem access from mere upload. List actual physical JARs, mod IDs, SHA256, source/version/loader and duplicate providers. Cross-compare exact R4 manifest 337 CurseForge refs/10 custom mods/340 expected production count and the new local files/updates; create a DIFF report with safe reuse plan. Avoid uploading individual JARs to GitHub.
2. Fetch PR64 HEAD, create a NEW working branch. Preserve original R4 archive and matching world backups; do not modify GitHub release or commit third-party JARs. Verify Java21, Python3.11+, Gradle and GitHub Desktop CLI/PUSH ability; GitHub Desktop may publish later. Generate branch/commit manifest.
3. Confirm the exact R4 ZIP SHA and campaign addon SHA in §1. If the user's local installed profile differs materially from R4, choose the actual owner-approved input and explicitly report deltas rather than assuming R4 binary matches every installed config.

**Stage 1 — close high-risk pregen gates without starting full pregen**
4. Verify live source/effective datapack precedence, server-type config locations, worldgen structure generation/arena list, SkyArena removed, WDA/Integrated repairs, village/dungeon spacing, boss presence, hostile table IDs and full 30 DD contexts in a **NORMAL FTF** fresh world. Try real natural generation/traversal; synthetic bounding boxes/registries are inadequate alone. Special checks: Mine Cells portal/return, Malkuth completeness, Dragon cave rarity, Farmers, bridges, snow/Euphoria.
5. Verify Brutal 70/30/4/3 before any chunk generation. Then perform a **bounded ~1k Chunky pilot** with Spark/MSPT/IO/disk/join/save/restart measurements. Only after final owner acceptance of worldgen and server config, choose 10k–20k radius. No pregen in production worlds on an unaccepted source variant.

**Stage 2 — current R4 → R5 Grand candidate (smallest reversible gameplay change)**
6. Read docs/handoffs/r5-grand-from-r4-20261015/CLAUDE_R4_TO_R5_LOCAL_EXECUTION.md, and the exact five deltas. The PR64 tools already produce R4-pinned *REVIEW_ONLY* files, verify 0.3.2 JAR identity and create separately packaged R5 test binaries/rollback once **all five owner/category/Paxi/installed-source review decisions are genuine**. Tests 30/30 passed in GitHub; they are synthetic.
7. Review Keep Kayra library/keep treasure enhanced book/equipment native functions, Adventuredungeons Murky trim/music reward, Iron's hidden trough and generic magic scroll randomize_spell; compare item/tier/balance from the user's actual installed JARs. Check full effective Paxi resource winner, not just original mod JAR SHA. Do not auto-click booleans true.
8. If all pass, compile/stage **ONE** separate experimental full R5 ZIP using PR64 tools, retaining 337 ref pins, 10 custom addon JAR names, 30 DD and all other R4 bytes. If a change needs Java behavior beyond JSON pool indices, stop the resource-only route and make a distinct full Java21 addon build/version.
9. Client+dedicated-server: compare original chest output statistically, never replace, test 5% chance vs native chest inheritance, two Lootr players independent, reopening/restart and late join; verify on normal/worldgen structures and separate no-bonus negative contexts. Deliver test receipt and rollback. Do not call R5 “released” simply because packaged.

**Stage 3 — boss/reward correction (requires actual source work, not just R5 JSON)**
10. Fix newer owner **Simply Swords full sword pool** requirement (enumerate true swords, include unique swords, exclude unrelated weapon classes; preserve Regalia/affixed/native separation). Test player-credited bonus, repeated kill, 5–7 player balance and loot ownership. This is **not** achieved by replacing five Grand pool indices.
11. Expand Regalia in reviewed batches from 13 toward 90% of verified eligible *suitable* items by T5 while observing native-only families. Stop on missing ID/unclear acquisition/unique trophy. Do not create a monolithic untested registry of 497.
12. Source-map boss T2/T3 entities; finish blocked native combat fields and isolate fixed scripted damage for Claude's separate boss addon. Verify all category exceptions, caps, multiplayer and repeat behavior.
13. Tier2+ Scrap/Treasure source-specific boosts only after actual values/source table selection are approved; keep native probabilities intact.

**Stage 4 — server readiness and performance**
14. Exercise starter Bonus Chest and Lootr; quest journal + FTB Solo Quests separate personal progress, Q/E, native gems/affix UI/Sigils/armor trims, Mine Cells and dimension portals, Goblin trades, keybinds. Dedicated-server start/stop, no Tan threads hang, consistent player state.
15. Benchmark shaders ON/OFF AO presets + Euphoria, forest/water/boss magic, newly generated vs pregen chunks, teleport and /locate stress (isolated), memory/GC, weaker-PC clients, 5–7-player TPS. No feature pruning without measured evidence.
16. After worldgen freeze and staged 1k pilot, execute the approved long pregeneration on server; retain exact config, seed, radius, disk footprint, timing and restart result.

**Stage 5 — later creative work (do not derail launch blockers)**
17. Wider quest atlas and dimension-optional campaigns, multiplayer RPG differentiation without Origins, rumors/treasure maps/explorer's journal integration, custom AO main menu, polish snow effects after Euphoria, expanded boss arena/superboss tuning later. New features need source registries and no redundant systems.

## 8. Acceptance test matrix (always distinguish synthetic and natural)
- **Import:** exact full ZIP SHA/CRC; no repeated mod IDs; correct version/manifest; official pins/campaign JAR and rollback separate.
- **Startup:** Java21, NeoForge21.1.252, full installed profile, real NORMAL Overworld, save/restart, no fatal mixin/registry errors; known book/tag/advancement diagnostics reviewed, not auto-ignored.
- **Worldgen:** natural representative curated biomes, mountain/coast/river/climate, all seven new DD structure families plus existing major dungeons, complete jigsaws, correct arena spawner/boss placements.
- **DD:** real ordinary mobs T2–T6 inside/outside zones vs synthetic; boss exemptions, Brutal overlaps, elite attributes, reload and restart.
- **Boss:** exact T5 exception fights, Cornelia/Dead King reward vs combat, Cataclysm scripted hits, Ice&Fire dragons/Hydra, T8/T9 later; native and extra loot at repeat kill, no duplication and player credit.
- **Grand:** 14 eligible contexts; proposed five thematic pools, 5% independent *one bonus roll*, correct native pool entry functions, never clear native loot; T0/T1/T2/Bonus Chest/Mine Cells and unrelated villages excluded.
- **Lootr:** two non-op players, one unopened chest; distinct personal loot, reopen/relog/restart/new joiner; no rereward duplication. Preserve Apotheosis affix/gem odds.
- **Starter:** exact original vanilla contents + approved one spellstone, one genuine affix, torches/meat; no reroll on reopen.
- **Regalia/Swords:** every approved ID resolves, native-only excluded, separate full sword family behavior once implemented, no inferred approval from catalog rank; R4 still unique-only.
- **Quests/UI:** 153 valid quests and per-player completion/rewards, normal and optional Enigmatic routes, no forced curse, FTB Solo false new worlds, Q/E placement at GUI scales, JEI/Curios/tooltip.
- **Performance/pregen:** cold/warm FPS 1% lows, MSPT, Spark, shaders, long loads and bounded Chunky; normal save/stop/restart; production only after acceptance.
Record each result as PASS/BLOCKED/NOT RUN with *exact binary hash/seed/config path*, player count, test type and reproduction steps.

## 9. Repo/source navigation: where each partial implementation lives
| Location | Purpose / status |
|---|---|
| docs/status/IMPLEMENTATION_PROGRESS.md | PR64 current R4 packaged/verified/open ledger; append new receipts, do not rewrite old results |
| docs/handoffs/r4-package-20261015/ | Exact R4 contents, native checks, 30 DD, 105 tests, SHA receipts |
| docs/handoffs/r3-reconciled-package-20261015/ | R3 previous baseline and reconciled owner/source decisions |
| docs/handoffs/integration-20261015/native-balance-ledger.json | Native boss 51-field source changes and fallback/unsupported routes |
| release_030/overrides/config/brutalbosses.json | Spawn chance/spacing and HP/damage multiplier 70/30/x4/x3 |
| release_030/overrides/config/dungeon_difficulty/difficulty_v2.json | Active R4 30-scoped zone source |
| docs/handoffs/dd-native-batch-r4-20261015/ | Seven new zones, 112 candidate queue and registry/biome eligibility evidence |
| docs/balance/ (DD_* owner plans) | Tier/structure planning, not all active |
| addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/BossRewards.java | R4 additive credited-player boss reward, historical unique-only |
| addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/GrandTreasure.java | Additive 5% native bonus source logic, review actual loot-list append |
| addons/ao-campaign/src/main/resources/ao_loot_policy.json | Exact R4 source mapping 32 IDs,13 Regalia,58 uniques,14 Grand, rare extra rates |
| docs/handoffs/r5-grand-from-r4-20261015/ | Review-only five pool delta and Claude local execution instructions |
| tools/preview_r5_grand_from_r4.py | Exact R4 source-blob-guarded five-pool preview, not runtime patch |
| tools/patch_r5_grand_from_r4.py | Exact R4 release & campaign0.3.2 hash guard, denied-by-default human approval, resource-only JAR patch |
| tools/package_r5_grand_from_r4.py | Separate full R5 experimental import + incremental rollback builder, not run on actual R4 yet |
| tests/test_preview_r5_grand_from_r4.py; test_patch_r5_grand_from_r4.py; test_package_r5_grand_from_r4.py | 30 synthetic R4->R5 regression tests total; GitHub CI gate |
| .github/workflows/ao-r4-r5-grand-delta.yml | CI uses synthetic preview, denied review form, no playable R5 |
| tools/audit_r3_native_reward_sources.py | Local JAR + source table hash/pool/weights/Paxi matching auditor, validates Paxi directory exists when provided |
| PR63 docs/handoffs/loot-update-20261015/KEEP_KAYRA_PINNED_SOURCE_POOL_EVIDENCE_20261015.json | Original six Keep Kayra pool entries/weights and native SHA evidence |
| PR63 docs/handoffs/R3_GRAND_14_OF_14_NATIVE_SOURCE_VERIFICATION_20261015.md | All14 published upstream mod JAR source identities and five proposed better native pools; research only |
| addons/ao-starter-chest/ | Vanilla bonus chest additive addon, 0.2.0 compiled |
| addons/ao-affix-trims/ | Random affixed armor trim hook 0.1.1 |
| addons/ao-augmenting-sigils/ | Rarity-priced Sigils 0.1.1 |
| addons/ao-enigmatic-betterinventory/ ; addons/ao-questlog-betterinventory/ | Enigmatic Q/E, Seven Curses UI & inventory placement fixes |
| addons/ao-worldgen-safety/ | Pregen/structure safety hooks |
| release_030/overrides/config/paxi/datapacks/ | Effective structure, tier rarities, trade and starter Apotheosis exemption candidates; source precedence important |
| release_030/overrides/defaultconfigs/ftb_solo_quests-server.toml | FTB Solo Quests teamSyncEnabled=false for new worlds; existing world/serverconfig may differ |
| release_030/overrides/config/questlog/ | Questlog chapters/quests; R4 checks153 |
| docs/balance/REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv | 497-item source/risk research,421 unscored |
| docs/handoffs/REGALIA_OWNER_REVIEW_QUEUE_20261015.md | IMPORTANT latest owner native-only and full Simply Swords sword-pool overrides in END sections |
| docs/handoffs/LOOT_OVERHAUL_OWNER_DECISIONS_20261015.md; LOOT_ADDITIVE_ONLY_VERIFICATION_GATE_20261015.md | New loot additive-only and affix odds decisions; some earlier paragraphs superseded by later appendices |
| docs/research/next-agent-package-20261014/ | Boss arena measurements, progression inconsistencies, owner decisions, remaining blockers, not actual complete runtime changes |
| docs/planning/AO_CUSTOM_FEATURES_PRIORITY_DECISIONS_2026-10-11.md | Later feature roadmap and rejected ideas; historical release phase statements |
| docs/performance/V049_OVERHAUL_PREP_20261012.md | Earlier performance baselines/tools; compare with current R4 before tuning |
| docs/questing/QUEST_AUTHORING_VALIDATION_PLAN.md | Historical proposal; several opening statements superseded by implemented R4 quests |
| docs/status/CURRENT_STATE.md ; docs/status/AGENT_WORKFLOW.md ; TODO.md | Old “current baseline” material; retain as searchable history, not current source of truth |

## 10. Claude execution contract and expected outputs (per batch)
1. **Owner effort minimized:** do not ask for reupload of 338 individual JARs if they are readable locally; inspect and use the existing local Git clone. If authentication to GitHub push is missing, create branch/commit locally, then hand a short GitHub Desktop push action to the owner.
2. Before edits, output **R4 vs local-profile hash and mod-ID inventory**, changed/missing/added config resources and whether they are client-only or server-type. Resolve real mismatches before altering balance.
3. Implement in small focused commits, each with **before/after files, why, explicit owner decision, old/new SHA** and tests. Do not mix R5 Grand five-delta with the full Simply Swords Java rewrite in the same test build.
4. For every feature keep columns **design approved / source implemented / packaged / static checked / native engine fixture / multiplayer tested / owner accepted / blocked**, never one ambiguous “done”.
5. Build new experimental complete import(s) only after source acceptance. Never overwrite R4 or PR63, publish an unreviewed third-party JAR, or silently change recipes/native loot. Copy zero third-party JARs into public source repo.
6. Provide new **full CurseForge ZIP, manifest, rollback, dependency/runtime logs, source-commit SHA, full archive/JAR hashes, test results and executable owner acceptance checklist**, only if actually generated. No invented artifact links/hashes.
7. **After every completed batch** update this handoff's successor or dated appendix, docs/status/IMPLEMENTATION_PROGRESS.md and the specific system ledger; mark superseded historic handoffs as history, don't destroy them.
8. Return clear blockers requiring owner decisions, with concrete options and impact. Do not ask already-answered questions; continue on tasks with verified approved scope.

## 11. First deliverables Claude should return
- A: **ACTUAL_PROFILE_VS_R4.json/csv** (mod JAR+mod-ID+version+SHA and config/Paxi/dimension deltas, with “338 vs expected340” explanation).
- B: **PREFREEZE_NATURAL_WORLDGEN_AND_SERVER_GATES.md** (registered/observed structures, boss arenas/spawners, 30 DD, Brutal actual config, missing assets, readiness).
- C: **GRAND_FIVE_POOL_NATIVE_ACCEPTANCE.json** (5 rows, source+conditions+functions+Paxi winner+tier suitability, explicit DENIED/PASS with rationale).
- D: When (and only when) reviewed, **R5_GRAND_PRIVATE_EXPERIMENTAL.zip** built FROM exact R4 + separate rollback/receipt, with full dedicated 2-player test matrix.
- E: **BOSS_AND_REGALIA_DELTA_TO_IMPLEMENT.csv** (currently 32 boss IDs/13 Regalia/58 unique tag records; unmet full swords, missing source-mapped T2/T3, blocked combat and Regalia native-only gates).
- F: **CURRENT_OPEN_DECISIONS.md** (only genuine owner approvals missing: T2 Scrap/Treasure amounts and tables, ambiguous reward-source tier balance, any future T9 rates, later worldgen freeze/launch choices).

**Exit criterion:** Claude can tell the owner, for each of these deliverables, exactly what is physically on disk, committed to GitHub, in the packaged experimental ZIP, native-fixture-proven, dedicated-server-proven and owner-accepted — and nothing else.

---
**Do not treat this Markdown file as a proof of live changes.** Last known FULL import remains R4. New GitHub commits on PR64 after its release are preparation only unless separately packaged and verified.
