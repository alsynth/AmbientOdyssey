# Ambient Odyssey — PR #45 integration: Work mode and Claude division of labor
**13 October 2026 · Coordination-only handoffs. No gameplay/source changes.**

## Main links
- [Draft PR #45 — installed-profile audit and reversible difficulty pilot](https://github.com/alsynth/AmbientOdyssey/pull/45): `experimental/structure-difficulty-v3-20261013` on `performance/v049-visual-ecology-20261013`.
- [Draft PR #44 — RPG/loot/boss/quest planning](https://github.com/alsynth/AmbientOdyssey/pull/44): `research/rpg-boss-loot-campaign-design-20261013`.
- **[Handoff for Work mode](WORK_PR45_RUNTIME_RPG_INTEGRATION_20261013.md)** — reproduce/accept PR #45, test exact config/runtime and introduce tiny loot and quest slices.
- **[Handoff for Claude](CLAUDE_PR45_ENCOUNTER_ENGINEERING_20261013.md)** — research/patch low-level limitations (elite stacking, native arena wave config, parser edge cases, small trial-spawner integration, source-level boss probes).

## Technical status as of PR #45
| Metric | Evidence | Interpretation |
|---|---|---|
| Installed profile | 332 physical mod JARs in v0.4.9 client-performance test | Physical roster, **not** latest code branch manifest |
| Catalogue | 427 rows, 386 named candidates, 41 reference rows | Mapped **resources**, not verified active generation |
| Eligibility | 53 rules: **28 attribute pilots**, **25 preserve natural** | Narrow/approved T0–6 safety scope |
| Held | **374** rows | Mostly intentional: Tier7–9, new proposals, resource conflicts, absent compatible mobs |
| Native attributes | Tier 2–6 HP +10/20/30/40/50% base, attack +5/10/15/20/25% base, armor +0.5/1/1.5/2/2.5 | Test values only, not balanced encounters |
| Loot/trial/bosses | No tiered loot, no spawner/equipment/boss behavior modifications | Next implementation work |
| Validation | 10 new + 3 inherited tests, native Gson schema, prior quest/manual source tests | **Static only**, no Minecraft client/server/multiplayer |
| Rollback | Exact original DD JSON + independent candidate | Restore save too for already modified mobs |
| Native Remnant | **2.7.0 installed** in checked physical v0.4.9 profile | Static metadata compatible; gameplay still untested |
| YUNG replacement | Installed config disables vanilla fortress/monument | Use effective YUNG IDs, not both vanilla and replacement |
| Sky/Ice Arena | Approved Tier3, native wave system; no DD pilot | Separate native tuning required |

## Cross-team ownership and sequencing
| Lane | Owner | Input | Deliverable | Gate |
|---|---|---|---|---|
| 1. Reproduce 53-zone kit and rollback | **Work** | PR45 candidate/tests/installed roster | Exact hashes and cloned-client/server acceptance report | No live server overwrite |
| 2. Elite/Brutal/APO stacking exclusion | **Claude** | DD 3.9.2 bytecode and source/mod hooks | Small code/config safety patch + tests or explicit 'not feasible' | Work merges only after combat proof |
| 3. Sky/Ice Arena source ID + wave budget | **Claude** | `SKY_ARENA_NATIVE_CONTROLS.json` and installed jars | Validated native arena config sample/rollback | Work tests 1–20, 21–40, 41+ waves |
| 4. Effective generation/override precedence | **Work** | Collisions, held catalogue, loaded datapacks | Confirmed winning resources for selected locations | Runtime truth over historical jars |
| 5. Archaion NBT/D&T pool parser | **Claude** | 2 NBT errors, 1 pool parser error | Correctly classified edge cases and unit tests | No JAR modification unless runtime evidence |
| 6. One trial-spawner/equipment site | **Claude** | PR45 trial/vault resource and NBT paths | Narrow, optional datapack proof | Work source+runtime accept |
| 7. Two loot-role sample dungeons | **Work** | Class system & real loot table index | One T3 and one T5 test overlay | Preserve vanilla native/Lootr and Mine Cells early loot |
| 8. Boss roster/campaign integration | **Work** with **Claude** source probes | PR44 design, existing 52 quests and latest registry | Two alternate T5 milestone candidates + validated T6 gate feasibility, NOT auto-hardlocked | Final T5/T6 approvals provisional until playtest |
| 9. Final boss capability survey | **Claude** | Installed 2.7.0, Cataclysm, F.D. Bosses etc | Targeted editability matrix | Keep Geburah and third T9 End boss unassigned |

### Risk worth investigating first
`SKY_ARENA_NATIVE_CONTROLS.json` contains references to **`born_in_chaos_v1` entities** despite no Born in Chaos JAR in the PR45 physical roster. The effect on the arena at runtime is **unknown**. Claude should verify missing-ID behavior and submit a safe, reversible filtered or substitute pool.

### User-approved design constraints
- Sky Arena/Ice Arena **T3**; Aviary **The End T6**; Keep Kayra **T6**; Bastion **T5**, Fortress **T4**; Twilight Hydra Lair **T4**.
- Maledictus in **Frosted Prison**, boss **T7**; Tyros/Scylla **T9**; Umbrakar **T8**, Remnant Ossukage/Kotsukage **T7**.
- **Geburah unassigned**. Third **End Tier 9** superboss unselected. Do not turn a placeholder into a final choice.
- Loot roles **Scrap / Supply / Equipment / Treasure / Grand Treasure**; preserve T0–2 and early Mine Cells loot; no guaranteed powerful gem through easy spawner farm.
- Main campaign accessible and solo-first, with independent optional dimensions, no RNG hostage gates and no forced group, Origin or curse.

## Conflict control
1. **Work mode owns** PR45 candidate/rollback integration, server/profile tests, Questlog and high-level loot authoring.
2. **Claude owns** independent addon/library/pilot patches and source-level research; create *separate* engineering branch; no PR45 direct edits unless Work explicitly coordinates.
3. Both can read all branches; neither merges draft PR #44/#45 blindly or resets the known-good r19 package. Use exact hashes and chosen source ancestor.
4. Store evidence (per-mod metadata, source hashes, diff/log/test results) in new topic-specific docs; never copy user local paths/private login info into public GitHub logs.
5. Hand off only changes labeled design/source/static/runtime with proper supporting evidence. No claims that static tests make Dungeon Difficulty, Bosses' Rise or multiplayer verified.

## Final review agenda for user (not a reason to block research)
When owner returns, present outcomes and remaining *actual* choices: final T5 alternative bosses, comparable strong T6 Pinnacle alternative, Geburah tier, third Tier9 End boss, long-term loot/drop odds and party sharing. Do not solicit a decision for already approved arena/structure tiers.

**This coordination handoff does not run any tests, write gameplay configs, modify PR #45, or assert a release build.**
