# R3 RECONCILED draft and implementation-plan reconciliation â€” 15 October 2026

## Result

The audit does NOT support saying every approved plan is finished. R3 packages the current implemented experimental version and fixes two concrete omissions found in R2. Planned, source-gated and runtime-gated work is listed separately below. Stable/main and R2 artifacts remain untouched.

Authority: latest owner chat decisions (unique weapons only), WORK_MODE_MASTER_IMPLEMENTATION_HANDOFF_20261015.md, latest end-of-document owner updates in the four loot decision handoffs, complete Claude handoff, Claude R2 bundle and current sources. Newest conversation instructions permit packaging untested source; they do not authorize invented IDs, undefined probabilities or excluded loot.

GitHub branches refreshed and live PR list read. The 31 historical pinned draft heads were unchanged. During upload, new commits landed on integration PR63 (through35ec28f) and the master handoff branch (2605284). Both were merged before final packaging; their new native-source audit, overlay tooling, tests and revised owner Grand policy are now included. No PR beyond63 appeared in the queried list. The 20 significant drafts and 11 requested older drafts were rechecked by changed-file surface and current target content. Exact-content differences are flags for reconciliation, not automatically missing features or permission to restore superseded changes. Machine report records every surface and actual package/source/resource comparison.

## Implemented in this pass

1. **Missing dedicated-server quest default:** source `release_030/overrides/defaultconfigs/ftb_solo_quests-server.toml` existed but was absent from the PR50-based R2 import. Add it to the packaging whitelist with `teamSyncEnabled=false`. Installed ftb-solo-quests 1.1.2 bytecode registers its config as `ModConfig.Type.SERVER`, with native true default. The restored default seeds NEW worlds; existing worlds need their own serverconfig checked. Dedicated two-player behavior remains NOT TESTED.
2. **Eternal Starlight Regalia omission:** the compiler previously selected only seven Artifacts and two Aquamirae exceptions. Add four already catalogue-ranked C0/C1 items authenticated against installed native recipes/language keys: Dagger of Hunger, Chain of Souls, Soulit Spectator and Etheric Eye. All have unconditional crafting outputs and no direct occurrence in native boss loot tables. No native table/recipe is changed. Runtime registry lookup still fails closed; registry/gameplay acceptance remains NOT TESTED. Do not extrapolate this source check to every recipe ingredient's entire acquisition graph.
3. Campaign becomes **0.3.2-experimental** and package becomes **R3 / 0.5.3**, keeping R2 immutable. Policy grows from 9 to 13 curated Regalia; 32 boss IDs, 58 unique tag records and 14 Grand candidates remain.
4. Actual-package validator now requires the missing Solo Quests server default. Added native-recipe acceptance checks reject ingredient-only matches, conditional recipes and smithing transforms. New audit compares draft heads, current files, packaged overlays and all resources in three rebuilt addons.
5. Correct the historical audit's two obsolete requirements: current approved base is 52 quests/13 chapters (campaign overlay adds 101/7), and owner-required Hominid removal must remain excluded rather than restoring an older 0.1.3 candidate. No failing gameplay test was suppressed; existing history tests now use current source authority.

## Reconciliation of the 20 significant drafts

| Draft | Current disposition |
|---|---|
| 62 | Partial: stronger owner DD budgets in 23 scoped Overworld zones. 497-row list remains a source/dimension/tier review queue. Provisional extra arenas withheld. |
| 61 | Continuity/owner decisions carried forward; documentation is not runtime evidence. |
| 60 | Boss/arena audit tools retained; natural arena and freeze acceptance still pending. |
| 59 | Packaged 70 chance / distance30 / HPx4 / damagex3, individual boss files unchanged. |
| 57 | Campaign, mastery and Simply More suppression included; obsolete gem grants/Pinnacle unlock and Rage Glove gate superseded. Current campaign 0.3.1 replaces original draft binary. |
| 56 | Native structure research preserved. Research rows do not automatically create effective DD zones. |
| 54 | Built Sigils 0.1.1 with approved rarity costs and native namespace; preserved in R3. |
| 53 | Four rarity overlays present; exact seven approved native weight edits verified in R2 and unchanged in R3. |
| 52 | Full-import ledger and execution handoff retained; packaging uses hash-pinned PR50 base. |
| 51 | Additive starter, Goblin prices, ring recipes, Lootr configuration retained. Old native gem suppression removed. Two-player conversion is untested. |
| 50 | Exact full import is reconstruction base; later overrides/removals intentionally change it. |
| 49 | Ranking catalog retained. Only 13 selected Regalia enter runtime policy; broad curation is incomplete. |
| 48 | Wave2 catalog/research included as source, not automatically a valid reward list. |
| 47 | Initial catalog retained; native exclusive acquisition must be respected. |
| 46 | Work/Claude coordination retained. No competing general boss scaler introduced. |
| 45 | DD v3 research/tooling retained; obsolete T0/T1 and Mechanical Nest blanket zones not restored. |
| 44 | Boss design retained with latest tier/category exceptions; old gatekeeper/tiers/gem designs superseded. |
| 42 | Wildlife/ambience/performance overlays inherited from pinned full base, source differences require the newer base's authority; no new benchmark claim. |
| 41 | Performance presets/UI/Streams fixes retained from full base; no rejected mod restored. Measured performance remains open. |
| 40 | Benchmark tooling retained; tools are not evidence of improved performance. |

Older required drafts 39,38,37,36,35,34,33,32,31,30,28 are also represented in the machine surface report. Their inherited port/UI/tooltip/Mine Cells/recipe/Curios fixes are checked against the actual full package, rather than overwritten wholesale with older branch copies.

## Remaining incomplete work â€” not silently counted as implemented

| Area | Actual coverage / what remains |
|---|---|
| Regalia breadth | 13 selected IDs against a 497-row ranking catalog, of which 421 are unscored. Not the approximate 90%-of-suitable-by-T5 goal. Unscored items, unclear IDs and native-exclusive boss trophies remain held. Cataclysm direct boss items, expensive Flight Ring recipes and Aquamirae summoning/navigation items were not indiscriminately made generic low-tier rewards. |
| Boss reward coverage | 32 exact entity IDs: T4=1,T5=6,T6=5,T7=7,T8=10,T9=3, plus constrained Remnant namespace alias handling. **No T2/T3 boss identities are mapped**, so the broad T2â€“T9 design is not fully realized. Need approved source-backed identities, not guessed strings. |
| Combat | Native field ledger has 51 edits. Cornelia, Last of Deepslate and Coralssus lack implemented scoped native stat routes; Ice & Fire Hydra attack remains unimplemented, and BOMD Lich missile parameters do not prove ordinary/ability damage scaling. Eternal Starlight boss family and Mechanical Nest boss identity remain unresolved. Fixed scripted damage needs mod-specific work; separate later reinforcement addon is not duplicated. |
| Dungeon Difficulty | 497 plan rows: 23 KNOWN_OVERWORLD_EXISTING, 342 DIMENSION_AND_REGISTRY_CHECK, 117 REVIEW_LATER,14 EXCLUDED_T0_T1,1 BOSS_ONLY_EXCEPTION. Current package has 23 active scoped zones. Do not interpret 497 minus23 as 474 approved omissions. Need source/dimension/provider/tier checks before additional activation. |
| Grand Treasure | Latest owner chest-category rule implemented: 14 own-table native pool mappings, including eight corrected formerly borrowed-table choices. Exact installed-JAR source audit:14 direct,0 cross-table,0 static blockers, no mapped-table Paxi override. Source generator checks template/NBT reachability. Single native-pool draw and5% chance retained. Coverage still limited to14 of70 source contexts; native semantics, Lootr incidence/once-only/per-player behavior and gameplay value remain unaccepted. |
| T2 Scrap/Treasure | Not implemented: exact per-source increases still unapproved. No numeric rates invented. |
| Loot ownership | One set goes to credited killer. Participant/contribution fairness and delivery/persistence still require implementation/acceptance; not per-party guaranteed rewards. |
| Worldgen | SkyArena removed, curated FTF/Paxi repairs retained. Natural arenas, table/spawner placement, effective datapack winners and registry/dimension checks remain necessary before irreversible pregen. |
| Runtime | No R3 Minecraft startup, natural fights, Lootr statistics, dedicated server, multiplayer, save/restart, respawn, shaders/performance or Chunky acceptance. Older R1 smoke is historical. |
| Later approved backlog | Quest Atlas, custom menu, optional realm campaigns, player build comparisons and comprehensive keybind/ambience work remain deferred; their design files are not playable implementations. |

## Explicit exceptions/exclusions preserved

- Chesed/Malkuth/Geburah T5 and combat-stat exempt. Dead King/Cornelia T6 rewards, T7 combat targets; missing Cornelia route remains visible.
- Ignis/Maledictus/Leviathan T8; Tyros/Scylla/Obsidilith T9. Structure tiers separate. Mother of Maze ordinary. Block Factory = Bosses'Rise.
- Brutal x4HP/x3damage, not stale x4/x4. Native HP cap accepted; no new participant multiplier.
- Enigmatic families native-only for new Regalia; separate starter spellstone reward retained. Pasterdream accessories native-only. Qym/Cursium native-only, Annihilator unapproved. Simply Swords separate reward restricted to native unique weapons, including registered non-sword unique types; no ordinary/runic weapons.
- Native gems/crafting and native loot kept. Independent rare affix rates T6 20/2, T7 25/8/5, T8 30/15/8/5; T9 odds deferred. No Rage Glove prototype activation.
- No generic T0/T1 DD, broad Nest zone, Pasterdream/non-Overworld DD rollout or early Mine Cells loot buff. Frosted Prison/Sunken City held; Acropolis End not an Overworld T9 DD zone.
- Origins/Ocean Loot/MCA Reborn/Big Globe/Mob Plaque/Subtle Effects not added. Hominid and Dimensional Doors exclusions retained.

## Source-to-package differences reviewed

The R2 source-tree scan found six absent files and 30 byte-normalized differences. One absent file was the real Solo Quests omission, fixed in R3. Four absent Dimensional Doors/Hominid configs belong to intentionally removed mods and must stay absent. The remaining Biolith defaultconfigs/general.json matches the installed 3.0.14 native defaults exactly (true,false,4,2,1); that version loads config/biolith/general.json. Its obsolete defaultconfigs copy is inert, not a missing custom tuning change, so no new worldgen setting was introduced.

Other differing copies include native-expanded defaults/comments, shader settings and newer PR50 recipe/config migrations. In particular, the older repository Mine Cells compatibility JSONs are false-condition guards; the pinned full base carries migrated native recipe schemas. Blindly overlaying the old files would disable working recipes. The machine report exposes these differences as newer-baseline/source drift, not unconditional losses. Native runtime validation of their behavior is still separate. Runtime-generated Jade/name/log files are not new approved design features. No whole-tree stale source overlay was used.

## Acceptance boundary

The corrected ZIP is a complete import of the current implemented experimental version, not all decided design goals completed. Build/static results do not prove runtime behavior. Use the new R3 ZIP in a new profile/disposable world. Keep R2 and all earlier rollback archives. Companion receipt includes complete per-member hashes and exact PR50 rollback. See accompanying R3 static and plan-coverage reports and test instructions.

## Final R3 verification

Source commit: 7ea67e72ba3bea0877cc1910f29335a0d82f5603.
Full ZIP SHA256: 5debe094c047162f0b30f2dd76e2ab85201310c480b64333eca89a4f4376ac99.
Rollback SHA256: 8b0793cd71d53099477b7cbdfd35d0f0cfe51dd62a6e8b56b32c75c6120e1d51.
Campaign 0.3.2 clean build PASS. All 98 Python tests PASS, including newly merged regression suites. Actual R3 static validator PASS: 1021 JSON,188 JSON5,289 TOML; 337 references,10 custom JARs,23 DD zones,153 quest files. R3 runtime: NOT TESTED.

## Final concurrent-update reconciliation

Latest owner policy supersedes structure-wide best-score borrowing: select fitting valuable native pools by chest category, preferring each triggering table. R3 RECONCILED applies that approved approach with installed-source evidence. Historical R2 mappings are preserved separately; no fabricated reward catalogue or native table replacement was introduced. The alternative R2-to-R3 overlay builder and authenticated downloader were merged as tools, not mistaken for gameplay. Packaging used the existing exact-PR50 reconstruction chain and complete member-hash rollback. Earlier local preliminary R3 files are retained but superseded by Ambient-Odyssey-MASTER-INTEGRATION-R3-RECONCILED-PRIVATE-20261015.zip.

Additional concurrent source-only updates through4b21f0c were merged after archive creation: review-only candidate generator/ledgers, configurable native audit input and6 new synthetic tests. The new preview tool now reads the preserved historical R2 mapping, so it cannot mislabel active R3 mappings as R2. These tools/docs do not alter the packaged runtime payload; final suite98/98 PASS. Package gameplay source7ea67e7 remains the receipt basis.
