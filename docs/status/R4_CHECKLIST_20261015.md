# Ambient Odyssey — R4 status checklist (15 October 2026)

**Summary:**
- **Next actions:** you import R4 as a new CurseForge profile; I run the Grand five-pool audit (deliverable C). Most remaining items need in-game, server or two-player testing, which only you can run.
- **Owner-decision conflicts:** one commit contradicts the latest owner decision: `9643b17`. It's superseded by `66322a5`; don't merge `fix/pinnacle-gate` on its own. R4 itself still ships a Pinnacle gate that breaks both the old and the new decision.
- **Premise correction:** no commit reverts the Simply Swords full pool, locally or on GitHub. It's on `feature/simply-swords-full-pool` (`2067e4a`) and matches the owner decision.

**Sources:** canonical handoff §5, §10 and §11 (deliverables A–F, the only "A–F" list in the docs); `R4-IMPLEMENTED-REMAINING-AND-TESTS.md`; `IMPLEMENTATION_PROGRESS.md`; `REGALIA_OWNER_REVIEW_QUEUE_20261015.md` (latest sections); `LOOT_OVERHAUL_OWNER_DECISIONS_20261015.md` (latest sections); owner decisions given in this session.

**Branches cross-checked** (all local, none pushed; GitHub fetched, PR64 head still `3806fa1`):

| Branch | Commits beyond PR64 `3806fa1` |
|---|---|
| `status/r4-reconciliation-20261015` | `132e368` reconciliation report |
| `fix/pinnacle-gate` | `9643b17` delete Pinnacle gate |
| `feature/pinnacle-cornelia` | `9643b17`, `66322a5` Cornelia gate, `5fddc71` line-ending-safe check |
| `fix/source-r4-parity` | `d7062ea` parity sync, `37d0954` Structory Towers v1.0.14 |
| `feature/simply-swords-full-pool` | `2067e4a` full sword pool |
| `hygiene/untrack-jars` (from `main`) | `588c8d6` untrack 331 JARs, `c4e045c` ignore rules |

**Test levels:**
- **source:** committed code or config.
- **static:** hashes, schema or unit tests.
- **engine:** a real Minecraft engine run under synthetic fixtures (R4's own runs, per R4 docs).
- **multiplayer:** a real two-or-more-player or dedicated-server test. Nothing has reached this level.

"Owner?" = Y if the next action needs you: a decision, an approval or an in-game run.

## A. Canonical handoff §5 — binding owner decisions

| # | Item | Status | Evidence | Test level | Next concrete action | Owner? |
|---|---|---|---|---|---|---|
| 5.1 | Brutal Bosses 70 / 30 / ×4 HP / ×3 dmg | done (packaged R4) | R4 `config/brutalbosses.json` (verified in `132e368`) | static | Confirm the same file on the actual pregen server before any Chunky run | Y |
| 5.2 | Chesed/Malkuth/Geburah T5, exempt from HP/attack multipliers | done | `ao_loot_policy.json` tiers; no `fdbosses` ledger edits (`test_master_integration`) | static | Real fights | Y |
| 5.3 | Dead King / Cornelia: T6 loot, T7 combat | partial | Dead King ledger 4500 HP / 50 dmg. Cornelia flagged "BLOCKED", but R4 ships `captain_cornelia_attributes` (300 HP, armor 16) in `aquamirae-common.toml` (`66322a5` proof doc) | static | Owner: set Cornelia T7 values through her native config | Y |
| 5.4 | Boss target multipliers T2–T9 (1024 HP cap) | partial | `docs/handoffs/integration-20261015/native-balance-ledger.json` (51 fields) | static (+partial engine per R4 docs) | Measure the 5 unmeasured bosses; map T2/T3 IDs | N |
| 5.5 | DD only for scoped Overworld hostiles T2–T6 | done (30 zones) | R4 `dungeon_difficulty/difficulty_v2.json` (30 verified in `132e368`) | engine (34/34 synthetic, R4 docs) | Natural-spawn test in the 7 new sites | Y |
| 5.6 | Simply Swords: full installed sword pool, separate roll | partial (source only) | `2067e4a`: 133 IDs, `ao_sword_pool.json`, campaign 0.3.3 | static + javac compile | Owner decides the 53 candidates (35 non-blade types, `sword_on_a_stick`, 17 non-lootable uniques), uniform weighting and Simply More; then a Gradle build and a packager update | Y |
| 5.7 | Enigmatic, Pasterdream accessories, Qym, Cursium: native-only in Regalia | done (13 IDs) | R4 policy Regalia list; `test_master_integration` | static | Enforce in every future Regalia batch | N |
| 5.8 | Grand Treasure: T3+, 5% independent, one extra category-fitting native draw | done R4 (14); R5 five pools review-only | R4 policy; PR64 `tools/*r5_grand*`, `REVIEW_ONLY_FIVE_POOL_DIFF.json` | engine (R4 fixture) / static (R5, 30 synthetic) | Deliverable C audit, then owner approval of each pool | Y |
| 5.9 | T6/T7/T8 rare extra affix rates | done | R4 campaign JAR policy: T6 20/2, T7 25/8/5, T8 30/15/8/5 | engine (600 factory samples, R4 docs) | Economy check over repeated kills | N |
| 5.10 | T2+ Scrap/Treasure boosts | blocked | No approved amounts | — | Owner sets amounts and source tables | Y |
| 5.11 | No PR57 automated Pinnacle unlock | **superseded:** Pinnacle = 5 native epic gear + Captain Cornelia kill | `66322a5`, `5fddc71` (`feature/pinnacle-cornelia`); proof doc | static (13 tests) + packager dry run | Engine: `/locate` Ice Maze and a pirate ship, kill Cornelia, confirm the unlock. Owner: assist-credit fix and R5 toolchain change | Y |
| 5.12 | BF Bosses = Bosses'Rise; T9 Tyros/Scylla/Obsidilith; T8 Ignis/Maledictus/Leviathan | done | R4 policy tiers (`132e368`) | static | — | N |
| 5.13 | Keep approved worldgen; no unmeasured overhaul | done (nothing changed) | `d7062ea`: 0 real config differences vs R4 | static | Owner freeze test | Y |
| 5.14 | Declined: Origins, Ocean Loot, MCA, Big Globe, Mob Plaque, forced Mine Cells start | done | R4 roster check (this doc): none present | static | — | N |
| 5.15 | Quest Atlas, menu, dimension quests, builds: later | not started (by design) | — | — | After worldgen freeze | Y |
| 5.16 | No blanket reroll; native loot protected | done (design) | `global_loot_modifiers.json` `replace:false`; additive `GrandTreasure` | static | Lootr two-player test | Y |

## B. Priorities A–F (handoff §11 deliverables)

| # | Deliverable | Status | Evidence | Test level | Next concrete action | Owner? |
|---|---|---|---|---|---|---|
| A | ACTUAL_PROFILE_VS_R4 | partial | `132e368` (`ACTUAL_PROFILE_VS_R4_20261015.json`), against the **pre-R4** v0.4.9.1 profile | static | Owner imports R4 as a new profile; rerun the inventory | Y |
| B | PREFREEZE_NATURAL_WORLDGEN_AND_SERVER_GATES | not started | — | — | R4 profile, then `/function aoa:start` and `/locate` runs | Y |
| C | GRAND_FIVE_POOL_NATIVE_ACCEPTANCE | not started (unblocked) | Tools on PR64 | — | Run `preview_r5_grand_from_r4.py` and `audit_r3_native_reward_sources.py` against the installed mods and R4 Paxi | N |
| D | R5 private ZIP | not started (correctly) | — | — | Needs C, owner pool approvals and a decision on the R5 Pinnacle gate | Y |
| E | BOSS_AND_REGALIA_DELTA CSV | not started | Inputs: 32 bosses / 13 Regalia / 58 uniques (R4), 133 swords (`2067e4a`) | — | Build the CSV | N |
| F | CURRENT_OPEN_DECISIONS | not started as a file | The "Owner? = Y" rows here | — | Write it from this checklist | N |

## C. Handoff §10 — execution contract

| # | Rule | Status | Evidence | Test level | Next concrete action | Owner? |
|---|---|---|---|---|---|---|
| 10.1 | Use the local modpack; minimal owner effort | done | Paths in `132e368` | static | — | N |
| 10.2 | R4 vs local inventory before edits | partial | `132e368` (local = pre-R4) | static | Redo on an R4 install | Y |
| 10.3 | Small focused commits; never mix R5 with the Simply Swords rewrite | done | Separate branches; `ao_loot_policy.json` byte-identical on `2067e4a` | static | — | N |
| 10.4 | Separate status columns per feature | done | This checklist; branch docs | — | — | N |
| 10.5 | Never overwrite R4/PR63; no third-party JARs in repo | partial | R4/PR63 untouched. **331 third-party JARs are in pushed `main` history** (`7177883`); untracked only on unpushed `hygiene/untrack-jars` (`588c8d6`, `c4e045c`) | static | Owner: push the hygiene branch; decide on a history rewrite and force-push | Y |
| 10.6 | Release artifacts only if really generated | done | No ZIP produced; the parity and dry-run rebuilds are local checks in `C:\Users\headq\aowt\_parity\` | — | — | N |
| 10.7 | Update the handoff successor and IMPLEMENTATION_PROGRESS after each batch | partial | Each branch appends its own IMPLEMENTATION_PROGRESS entry, so merging will conflict; no dated handoff appendix yet | — | Write a handoff appendix once the merge order is decided | N |
| 10.8 | Return blockers with options | done | Branch docs | — | — | N |

## D. R4 implemented/remaining doc and IMPLEMENTATION_PROGRESS "still incomplete"

| # | Item | Status | Evidence | Test level | Next concrete action | Owner? |
|---|---|---|---|---|---|---|
| D1 | Owner test 1: import R4 as a new profile, normal FTF world | not started | No local R4 install (`132e368`) | — | Import the R4 ZIP | Y |
| D2 | Owner test 2: `/locate` the 7 new DD sites, check rooms and spawners | not started | — | — | Run after D1 | Y |
| D3 | Owner test 3: mob stats inside/outside zones; Brutal/Apotheosis stacking | not started | — | — | Run after D1 | Y |
| D4 | Owner test 4: boss rewards, gems, journal, Solo Quests | not started | R4 engine fixtures only | engine (fixture) | Real kills; check `teamSyncEnabled=false` in a new world | Y |
| D5 | Owner test 5: no production pregen before acceptance | in force | — | — | Bounded 1k Chunky pilot after freeze | Y |
| D6 | Natural placement, elites, ability scaling, respawn | not started | — | — | In-game | Y |
| D7 | Boss contribution fairness | not started | Same issue for the Pinnacle Cornelia kill (killer-only credit; fix proposed in the proof doc) | — | Owner decides the contribution rule | Y |
| D8 | Dedicated-server startup and sidedness | not started | — | — | Disposable dedicated server | Y |
| D9 | Two-player Lootr, reopen, restart | not started | — | — | Two-player test | Y |
| D10 | Shaders and performance benchmark | not started | — | — | Apples-to-apples runs | Y |
| D11 | Regalia toward 90% of eligible items by T5 | partial (13) | R4 policy | static | Next reviewed batch from the 421 unscored rows | N, then Y |
| D12 | T2/T3 boss identities | not started | Policy has none | — | Source research | N |
| D13 | DD beyond 30 zones | not started | 112-row queue (78 to review, 25 no Overworld biome) | static | Owner approves the next tier batch | Y |
| D14 | Grand beyond 14 contexts | not started | — | — | After C | Y |
| D15 | T9 rare odds | deferred | Owner deferred | — | — | Y |
| D16 | Party credit; delivery, respawn and restart of rewards | not started | — | — | In-game | Y |

## E. Owner decision docs (latest sections) and this session's decisions

| # | Decision | Status | Evidence | Test level | Next concrete action | Owner? |
|---|---|---|---|---|---|---|
| E1 | Pasterdream accessories native-only | done | Not in R4 Regalia | static | — | N |
| E2 | Eternal Starlight: no special gating | done | 4 ES items in R4 Regalia | static | — | N |
| E3 | Abyssal Tiara and Tempest Trident in the T2–T5 pool | done | R4 Regalia list | static | — | N |
| E4 | Cursium native-only | done | Absent from Regalia | static | — | N |
| E5 | The Annihilator | blocked | "owner decision outstanding" | — | Owner decides | Y |
| E6 | Three separate per-kill rewards (affixed item, Regalia, sword), repeat kills included | done (R4 unique-only) / partial (full pool `2067e4a`) | R4 policy; `2067e4a` | engine (R4 fixture) / static | See 5.6 | Y |
| E7 | One reward set per credited kill; no party multiplication | done | Policy `ownership` | static | Revisit with D7 | Y |
| E8 | T7 Heirloom 5%, T8 Heirloom 8%, T8 Esoteric 5% | done | R4 policy | engine (fixture) | — | N |
| E9 | Gems: native only, no AO gem drops or gates | done | `test_no_bespoke_gem_grants` | static | Confirm 60 gems on an R4 install | Y |
| E10 | Grand: chest-category selection (latest) | done R4 / R5 review-only | See 5.8 | — | See C | Y |
| E11 | **Session:** Pinnacle = native epic gear + Cornelia kill | done (source) | `66322a5`, `5fddc71` | static | See 5.11. Also confirm horn supply for 5–7 players (one horn per pirate ship, used up per summon) | Y |
| E12 | **Session:** Structory Towers v1.0.14 in the approved list, with the v1.0.17 crash note | done | `37d0954` | static | — | N |
| E13 | **Session:** untrack third-party JARs; ignore `*.jar` except the 10 R4 customs | done (local) | `588c8d6`, `c4e045c` | static | See 10.5 | Y |
| E14 | **Session:** treat the R4 ZIP as authoritative for config parity | done | `d7062ea`: 0 real diffs, 17 documented mod rewrites | static | Decide whether to normalize Questlog line endings (109 CRLF-only diffs) | Y |
| E15 | **Session:** don't touch the owner's local profile | complied | Read-only access only | — | — | N |

## F. Flags

### Commits or artifacts that contradict an owner decision
1. **`9643b17` (`fix/pinnacle-gate`)** deletes the Pinnacle gate ("native unlock stays in charge"). That contradicts the newer Cornelia decision. `66322a5` builds on it and corrects it; merge `feature/pinnacle-cornelia`, not `fix/pinnacle-gate` alone.
2. **`132e368`** (status report) and the `fix/pinnacle-gate` IMPLEMENTATION_PROGRESS entry still describe "native unlocks stay in charge". Read them as superseded.
3. **R4 itself (packaged):**
   - `ao_campaign_gates` uses `minecraft:impossible` for Pinnacle, which breaks both the old and the new decision.
   - The R5 toolchain copies it unchanged.
4. **Not a contradiction:** the Simply Swords full pool was **not reverted** anywhere (`git log --all` shows no revert). `2067e4a` implements the owner decision. Its open point: it includes 35 spears, glaives, halberds, scythes, chakrams, greathammers and greataxes, which the mod tags as swords. The owner asked to tell these apart, and the instruction was not to exclude anything without an owner decision.

### In the logs but not in the PR64 canonical handoff
- R4's Pinnacle `impossible` gate; the Cornelia decision; Cornelia is horn-summoned with no arena; R4 already has a native Cornelia stats config.
- The Simply Swords 133-ID pool and campaign 0.3.3; R4's packager is hard-coded to 0.3.2.
- The R5 toolchain would carry the R4 Pinnacle gate.
- Source vs R4:
  - All 32 differing files come from the PR50 base ZIP.
  - The Mine Cells recipes were build-generated but never committed (fixed in `d7062ea`).
  - New `MOD_REWRITTEN_CONFIGS.json`.
  - 109 Questlog files differ only in CRLF line endings.
- Local profiles: none was installed from R4. The local 338-JAR profile is pre-R4 and still has Sky Arena, the 53-zone DD pilot, Brutal defaults and Solo Quests team sync on.
- `main` history contains 331 third-party JARs: commit `7177883` "whole pack push", pushed 15 Oct.
- `main`-only docs `d60537c` and `6a01951` (Simply More Stun crash log, flicker-disable request, v0.4.9 local mod list) aren't on PR64. The handoff only mentions the "anti-flash/stun changes" in general.
- Merge hazard: all four feature branches append to `IMPLEMENTATION_PROGRESS.md`.
- Test environment: 2 tests (`test_v041_idas_create_items`, `test_v041_invalid_item_source_coverage`) fail to import because `nbtlib` isn't installed. They fail the same way on the untouched branch.

## Top next actions
1. **Owner:** import the R4 ZIP as a new profile and run D1–D4.
2. **Me:** deliverable C, the Grand five-pool audit.
3. **Owner:** Simply Swords candidates and weighting; Annihilator; T2 amounts; Cornelia assist credit; the R5 toolchain change.
4. **Me:** deliverable E (CSV) and F (open-decisions file).
5. **Owner:** push or merge order, and the `main` JAR history decision.
