# R4 current-state reconciliation — 15 October 2026

**Result:** R4 ZIP is intact and readable. The local 338-JAR profile is **not R4**; it is the older v0.4.9.1 profile. Every R4 CurseForge pin is installed at the same file ID, but 3 R4 custom JARs, 4 R4 Paxi packs, 3 R4 defaultconfigs and the R4 Brutal Bosses / DD / Solo Quests values are missing locally, and SkyArena (removed in R3/R4) is still installed. One packaged R4 conflict was found: an `ao_campaign_gates` Pinnacle override that contradicts the owner's "native World Tier unlocks stay authoritative" rule.

**Next action:** import the exact R4 ZIP as a new CurseForge profile (owner, ~2 min), then run queue item 1 (Pinnacle check) and item 2 (R5 five-pool installed-source audit).

Baseline: PR #64, `experimental/master-integration-r3-reconciled-20261015` @ `3806fa1`. Method: Python `zipfile`/`hashlib` only; no JAR edited, no file corrected. Machine-readable evidence: [`ACTUAL_PROFILE_VS_R4_20261015.json`](ACTUAL_PROFILE_VS_R4_20261015.json).

Status words follow §2 of the canonical handoff: SOURCE IMPLEMENTED / PACKAGED R4 / STATIC VERIFIED / NATIVE ENGINE FIXTURE PASS / MULTIPLAYER TESTED. "Verified here" means checked in this session against the actual R4 ZIP bytes; "per R4 docs" means taken from R4 receipts without re-running.

---

## 1. Verified facts

### Resources (Step 2)
| Item | Path | Check |
|---|---|---|
| R4 import ZIP | `C:\Users\headq\Documents\Codex\2026-10-15\continue-development-of-ambient-odyssey-using\outputs\Ambient-Odyssey-MASTER-INTEGRATION-R4-PRIVATE-20261015.zip` | 154,493,674 B, SHA256 `31b037a7…6c6d` = receipt ✔ |
| R4 rollback ZIP + report | same folder (`…-R4-PRIVATE-20261015-Rollback.zip`, `.zip.report.json`) | present, not hashed |
| R1–R3 ZIPs | same folder | present (immutable history) |
| Installed 338-JAR profile | `C:\Users\headq\curseforge\minecraft\Instances\Ambient Odyssey v0.4.9.1 - Structure Difficulty + Celestisynth TEST` | 338 JARs, configs, `config/paxi/datapacks` (16 packs), world `saves/Test` (serverconfig empty), **no kubejs** |
| Nearest-to-R4 profile | `…\Instances\Ambient Odyssey - Full Experimental Pack through PR54 + Campaign and Deferred Features` | 341 JARs; has older campaign 0.1.3 / starter 0.1.0 |
| R4 campaign addon | `overrides/mods/ao-campaign-0.3.2-experimental.jar` | SHA256 `802461a6…39b7` = receipt ✔ |

**No local CurseForge profile was installed from R4.** All local evidence below is "pre-R4 profile vs R4 package".

### Count explanation (331 / 337 / 338 / 340)
| Number | What it is |
|---:|---|
| **337** | R4 CurseForge refs = 330 mods + 5 resource packs + 2 shader packs |
| **340** | R4 expected production mod JARs = 330 CF mods + 10 custom JARs |
| **338** | Local v0.4.9.1 profile = 331 CF mods + 7 custom JARs |
| **331** | CF mod projects in the local profile = R4's 330 + **Demi's Sky Arena**. (Also the JAR count of the git-tracked repo copy, which had no custom JARs.) |
| 341 | PR54 full-pack profile = 331 CF mods + 10 older custom JARs |

### Mod inventory (Step 3) — local 338 profile vs R4
- **Missing (R4 ref not installed):** 0.
- **Updated (installed file ID ≠ R4 file ID):** 0.
- **Installed file hash ≠ CurseForge file hash:** 0 (all 331 CF JARs match their CurseForge SHA-1; earlier session also matched originals byte-for-byte from the CDN).
- **Added (not in R4):** 1 — Demi's Sky Arena `1141465:7053645` (`SkyArena-1.3.6-1.21.1.jar`). R3/R4 removed it on purpose.
- **Renamed/.disabled:** 0. **Duplicate mod IDs:** 0 (parsed `[[mods]]` from each JAR's `neoforge.mods.toml`).
- **Custom JARs:** 7 of 10 present, all SHA256-identical to R4. **Missing:** `ao-campaign-0.3.2-experimental.jar`, `ao-augmenting-sigils-0.1.1-experimental.jar`, `ao-starter-chest-0.2.0-experimental.jar`.

### Config and datapack diff (Step 4)
5,378 R4 override files (config/defaultconfigs/shaderpacks) vs 5,346 local files.
- **27 files differ.** Key gameplay ones, local value → R4 value:
  - `config/brutalbosses.json`: chance 30 / distance 100 / HP 1.0 / dmg 1.0 → **70 / 30 / 4.0 / 3.0**
  - `config/dungeon_difficulty/difficulty_v2.json`: 53 structure entries (PR45 pilot) → **30 scoped zones**
  - boss configs changed by R4: `block_factorys_bosses-server.toml`, `bosses_of_mass_destruction.json5`, `cataclysm-common.toml`, `iceandfire/iaf-common.json`, `irons_spellbooks-server.toml`, `remnant/bosses/{kotsukage,ossukage,umbrakar}.json`
  - `lootr-common.toml`, `paxi/datapacks/ao_flight_balance/…/{basic,advanced}_ring.json`
  - Locally newer than GitHub (local edits after the last commit for that path): `apotheosis/enchantments.cfg`, `apotheosis/name_generation.cfg`, `sophisticatedcore-common.toml`, `oculus.properties`, `shaderpacks/AO Balanced.txt`, three FTB manual chapters (`field_manual`, `keybind_cheatsheet`, `tips_and_tricks`.snbt). Client-only/rewritten: `betterinventory-client.toml`, `screenshot_viewer-client.toml`, `fabric/indigo-renderer.properties`, `euphoria_patcher/.data.json`, `sound_physics_remastered/sound_rates.properties`, `bountiful/errors.log`.
- **123 R4 files missing locally:** 108 Questlog files, 12 files in 4 Paxi packs (`ao_campaign_gates`, `ao_goblin_trades`, `ao_starter_apotheosis_exemptions`, `ao_world_tier_balance`), 3 defaultconfigs.
- **91 local-only files:** Mine Cells (36), Tombstone (10), SkyArena configs, `.bak` files, JEI, Celestisynth, others.
- **Which source wins at runtime:** mods read the instance `config/`. A world's `serverconfig/` overrides `config/` (the `Test` world's is empty). R4's `defaultconfigs/` files are copied into the serverconfig of **new** worlds only, overriding `config/` there. Paxi loads `config/paxi/datapacks` (load order list empty → default order). So on the local profile, today's runtime = local `config/`, i.e. the pre-R4 values above.

### Branches (Step 5)
95 remote branches: 58 contained in PR #64, 1 in main. **37 have commits not in PR #64** (full list in the JSON). Ancestry is not content: e.g. PR #59's Brutal values and the SkyArena removal are present in R4 even though those branches aren't ancestors. Ones that matter:

| Branch / PR | Updated | Not in #64 | Note |
|---|---|---:|---|
| #63 master-integration (R2) | 10-15 | 41 | Native loot research; five pools already ported via PR64 tools. Don't use as base. |
| #62 dd-v4-stronger-pilot | 10-15 | 20 | Stronger T2–T6 values, superseded by R4 budgets; not active. |
| #56 dd-native-structure-scope | 10-14 | 317 | DD research incl. Mechanical Nest / Foundry evidence. |
| #60 pregen-boss-roster-freeze-gate | 10-14 | 6 | Source audit (Bosses' Rise = Block Factory per later owner fact). |
| fix/pregen-drop-demis-skyarena (no PR) | 10-14 | 1 | SkyArena manifest filter; R4 manifest already lacks SkyArena. |
| #51, #52, #59 | 10-14 | 2–5 | Later commits after R4 inputs; content mostly integrated. |
| #44, #46–#49 | 10-13 | 21–38 | Design/Regalia research, docs only. |
| v046/v047 branches (no PR) | 10-12 | 57–65 | Gem-tier verification, Wet Sand/Apotheotic port handoffs, pregen plan. |
| Older #11–#29 side branches | 10-10/11 | 1–22 | Superseded content waves, quest site, perf kit. |

### R4 package contents verified here
- 10 custom JARs; campaign 0.3.2 SHA ✔. Policy inside the JAR: **32 boss IDs** (T4: 1, T5: 6, T6: 5, T7: 7, T8: 10, T9: 3; no T2/T3), **13 Regalia**, **58 unique weapons (all `simplyswords:`) + 1 optional**, **14 Grand Treasure mappings**, rare affix rates T6 20/2, T7 25/8/5, T8 30/15/8/5 (matches latest owner tables), native gems "UNCHANGED", ownership "one set per credited kill".
- Global loot modifiers list only `ao_campaign:grand_treasure`; `rage_glove_gate` is in the JAR but **not registered** (inactive, as decided).
- `brutalbosses.json` 70/30/4.0/3.0 ✔. DD config 30 entries ✔. `defaultconfigs/ftb_solo_quests-server.toml` `teamSyncEnabled = false` ✔.
- Questlog: 153 quest files + 20 chapters ✔. Shader presets AO Balanced/Performance/Quality + Complementary/Euphoria ✔. SkyArena absent from manifest ✔.
- Paxi packs present: `ao_world_tier_balance`, `ao_goblin_trades`, `ao_flight_balance`, `ao_starter_apotheosis_exemptions`, `ao_campaign_gates`.

---

## 2. Discrepancies (real, found in files)

1. **Pinnacle gate conflicts with owner rule — PACKAGED R4, not engine-tested.** R4 ships `config/paxi/datapacks/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json`, replacing native Apotheosis 8.9.0 criteria (`epic_chest` etc.) with `minecraft:impossible` ("Defeat the Dead King or … Kobolediator"). Campaign 0.3.2 code (`AOCampaign.java`) says "native World Tier unlocks remain authoritative" and grants only `ao_campaign:milestones/*`, never Pinnacle. Handoff §5.11 says the automatic Pinnacle route is superseded. Likely effect: Pinnacle World Tier cannot be unlocked in R4. Source: `release_030/experimental_overlays/v050/overrides/config/paxi/datapacks/ao_campaign_gates/`. Needs an engine check before any fix.
2. **Local profile is pre-R4** (see §1): Brutal Bosses defaults, 53-zone PR45 DD pilot, no campaign/Sigils/starter addons, no world-tier/goblin/starter-exemption Paxi packs, no Questlog content files, SkyArena installed. Any test on this profile is not an R4 test.
3. **FTB Solo Quests:** local `config/ftb_solo_quests-server.toml` has `teamSyncEnabled = true`; R4 ships `false` only as a defaultconfig (new worlds). Existing worlds keep their own value.
4. **Server-config defaults missing locally:** R4 `defaultconfigs/` (Block Factory bosses, Iron's Spellbooks, FTB Solo Quests) are absent from the local profile, so new local worlds would not get R4 server values.
5. **Source ≠ R4 bytes for 30 override files** (no override commits after R4 source `9a2af79`, so this predates R4). Examples: `moogs_structures.json` has different structure keys (`mvs:` in Git vs `mss:` in R4); 15 Mine Cells compat recipes are disabled stubs in Git but full recipes in R4 (generated at build); `regions_unexplored/common.json`, `fml.toml`, Jade and others look like runtime-rewritten copies. 4,146 R4 members (Tan's trees, shaders, 322 Paxi files, Questlog) have no file under `release_030/overrides`. Rebuilding R4 from Git alone may not reproduce it byte-for-byte.
6. **Structory Towers:** pinned at v1.0.14 (`783522:7078283`) because v1.0.17 failed with "Missing ModLoader"; `APPROVED_ADDITION_JARS.txt` on PR64 still lists v1.0.17.
7. **Simply Swords:** R4 has 58 unique-tag IDs (57 registered in engine fixture); latest owner decision wants the full installed sword pool. Known P1 gap, confirmed in the JAR.
8. **Stale docs** (already listed in handoff §6): `docs/status/CURRENT_STATE.md`, `AGENT_WORKFLOW.md`, `TODO.md` still name older baselines. `main` handoff docs (audit1/Test 6) are fully superseded.

---

## 3. Feature ledger (Step 6)

Legend: **Pkg** = in R4 ZIP; **Src** = source on PR64; **Static** = static/receipt checks; **Engine** = native engine fixture; **MP** = real multiplayer/dedicated server. ✔ verified here, (d) per R4 docs, ✖ no, — n/a.

| Feature (§4) | Pkg | Src | Static | Engine | MP | Source path | Next concrete action |
|---|---|---|---|---|---|---|---|
| Core roster 337+10 | ✔ | ✔ | ✔ | (d) startup/join/save | ✖ | `release_030/release-lock.json`, receipt | Import R4 as new profile; diff that install |
| FTF terrain / biomes | ✔ (inherited) | ✔ | (d) | ✖ | ✖ | `release_030/overrides/config`, Paxi | Natural-world sampling at freeze test |
| Structures / repairs, SkyArena removed | ✔ | ✔ | (d) | ✖ | ✖ | `ao_structure_repairs`, density/compat JSON | `/locate` + walk test; remove SkyArena from local profile only via R4 import |
| Boss arena / pregen gate | ✖ (docs) | ✔ | (d) | ✖ | ✖ | `docs/research/next-agent-package-20261014/` | Owner runs `/function aoa:start` |
| Brutal Bosses 70/30/×4/×3 | ✔ | ✔ | ✔ | ✖ | ✖ | `release_030/overrides/config/brutalbosses.json` | Verify on the actual pregen server config |
| DD T2–T6 (30 zones) | ✔ | ✔ | ✔ | (d) 34/34 synthetic | ✖ | `…/dungeon_difficulty/difficulty_v2.json` | Natural spawn test in 7 new sites |
| Seven R4 DD additions | ✔ | ✔ | (d) | (d) | ✖ | `docs/handoffs/dd-native-batch-r4-20261015/` | Same as above |
| DD future mapping | ✖ | partial | (d) 112-row queue | ✖ | ✖ | `remaining-candidate-queue.csv` | Next batch needs owner tier approval |
| Boss tier/balance routes (51 edits) | ✔ | ✔ | (d) | partial (d) | ✖ | `docs/handoffs/integration-20261015/native-balance-ledger.json` | Map T2/T3 IDs; measure 5 unmeasured bosses |
| Boss tier exceptions | ✔ (policy tiers) | ✔ | ✔ | ✖ | ✖ | `ao_loot_policy.json` | In-game fights |
| Boss base rewards (32 IDs) | ✔ | ✔ | ✔ | (d) 600 samples | ✖ | `addons/ao-campaign/…/BossRewards.java` | Real kill + credit test |
| Full Simply Swords pool | ✖ | ✖ | ✖ | ✖ | ✖ | — | Enumerate swords from installed JAR (queue #3) |
| Rare extra affix rates | ✔ | ✔ | ✔ | (d) | ✖ | `ao_loot_policy.json` | Economy sim over repeated kills |
| Regalia (13 IDs) | ✔ | ✔ | ✔ | (d) 13 resolve | ✖ | `ao_loot_policy.json`, `REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv` | Next reviewed batch; exclusions enforced |
| Regalia exclusions | ✔ (none of the excluded families in list) | ✔ | ✔ | ✖ | ✖ | owner queue (bottom sections) | Keep enforced in every batch |
| Grand Treasure R4 (14, 5%) | ✔ | ✔ | ✔ | (d) | ✖ | `GrandTreasure.java`, policy | 2-player Lootr test |
| Grand R5 five pools | ✖ | ✔ tools | (d) 30 synthetic | ✖ | ✖ | `docs/handoffs/r5-grand-from-r4-20261015/`, `tools/*r5_grand*` | Installed-source audit (queue #2) |
| T2 Scrap/Treasure | ✖ | ✖ | ✖ | ✖ | ✖ | — | Owner amounts needed |
| Starter Bonus Chest 0.2.0 | ✔ | ✔ | ✔ | (d) 600 samples | ✖ | `addons/ao-starter-chest/` | Lootr/reopen test |
| Goblin trades / flight rings | ✔ | ✔ | (d) | ✖ | ✖ | Paxi `ao_goblin_trades`, `ao_flight_balance` | Check outputs in JEI in R4 |
| Apotheosis rarity / Sigils | ✔ | ✔ | (d) | ✖ | ✖ | Paxi `ao_world_tier_balance`, `addons/ao-augmenting-sigils/` | GUI/odds test; **Pinnacle gate (discrepancy 1)** |
| Gems native | ✔ (policy) | ✔ | ✔ | (d) | ✖ | policy `native_gems` | Confirm 60 gems in R4 install |
| Affix armor trims 0.1.1 | ✔ | ✔ | (d) | (d) GameTests | ✖ | `addons/ao-affix-trims/` | Real chest/mob samples |
| Apotheotic port / Wet Sand | ✔ prototypes | ✔ | (d) | (d) partial | ✖ | bundled JARs | API/feature audit |
| Mine Cells / dimensions | ✔ | ✔ | (d) | historic owner return | ✖ | `compat/streams-minecells/` | R4 normal-world travel test |
| Questlog / FTB (153) | ✔ | ✔ | ✔ | (d) 153 parse | ✖ | `release_030/overrides/config/questlog/` | Per-player completion test |
| UI / quality | ✔ | ✔ | (d) | (d) partial | ✖ | Q/E bridges | GUI-scale check in R4 |
| Performance presets | ✔ | ✔ | (d) | ✖ R4 | ✖ | `overrides/shaderpacks` | Apples-to-apples bench |
| Chunky pregen | ✖ | docs | ✖ | ✖ | ✖ | `docs/performance/` | Only after freeze; 1k pilot |
| Player builds / later RPG | ✖ | ✖ | ✖ | ✖ | ✖ | planning | Later |

**Priority A–F** (read as the canonical handoff's §11 deliverables A–F; no other A–F list exists):

| Deliverable | State | Next action |
|---|---|---|
| A ACTUAL_PROFILE_VS_R4 | **Done for the local 338 profile** (this report + JSON). R4-installed profile does not exist yet. | Re-run against an R4-imported profile |
| B PREFREEZE_NATURAL_WORLDGEN_AND_SERVER_GATES | Not started | Needs R4 install + owner in-game runs |
| C GRAND_FIVE_POOL_NATIVE_ACCEPTANCE | Not started; tools exist and are unblocked | Queue #2 |
| D R5 ZIP | Not built (correctly) | After C + owner approvals |
| E BOSS_AND_REGALIA_DELTA | Inputs confirmed (32 / 13 / 58, no T2/T3) | Queue #3 and #4 |
| F CURRENT_OPEN_DECISIONS | Not written | See §5 blockers |

---

## 4. Prioritized unblocked queue (top 5)

1. **Pinnacle gate check.** In a disposable R4 engine run, check whether `apotheosis:progression/pinnacle` can be earned natively. If blocked, propose dropping `ao_campaign_gates` in the next build (aligned with the existing owner rule). No change to R4.
2. **Grand five-pool audit (deliverable C).** Run `tools/preview_r5_grand_from_r4.py` and `tools/audit_r3_native_reward_sources.py` against the installed mods plus R4's Paxi overrides; record PASS/DENIED per pool. All inputs are on disk.
3. **Simply Swords sword enumeration.** List every item in the installed Simply Swords JAR, classify swords vs other weapon types from the JAR's own registry and tags, and write the candidate list. No reward code yet.
4. **Boss/Regalia delta (deliverable E).** Build the CSV from the policy (32 IDs, 13 Regalia, 58 uniques) plus the 497-row catalogue, marking native-only exclusions and the missing T2/T3 IDs.
5. **Source-reproducibility ledger.** For the 30 override files where Git ≠ R4 bytes, record which are build-generated, which are runtime rewrites and which are real content differences (start with `moogs_structures.json`), so the next build doesn't silently regress R4.

## 5. Blockers

**Owner actions:**
- Import the R4 ZIP as a new CurseForge profile; the local 338 profile is pre-R4.
- In-game tests (natural worldgen, `/function aoa:start`, real boss kills, dedicated server, 2-player Lootr).
- Push the branches below (not pushed, by instruction).

**Owner decisions:**
- T2 Scrap/Treasure amounts and tables.
- Approvals for each of the five R5 pools.
- The Annihilator.
- T9 rare rates (deferred).
- The Eternal Starlight T6 family.
- The unnamed T6 boss slot.
- The next DD tier batch.
- Whether a different sword roll weighting is wanted (default: uniform).

**Technical:**
- 5 bosses never measured.
- 1024 HP cap.
- Scylla wave has no lever.
- Aquamirae and Archaion have no config.
- Worldgen not frozen; no pregen.

## Git state from this session (local only, not pushed)
- `hygiene/untrack-jars`: `588c8d6` untracks the 331 committed JARs (files stay on disk). `c4e045c` ignores `*.jar` except the 10 R4 custom JAR names and adds `* text=auto eol=lf` to `.gitattributes`. Local `main` was reset back to `origin/main` (unchanged from GitHub).
- `status/r4-reconciliation-20261015` (from PR64 head `3806fa1`): this report plus JSON evidence.
- The 331 JARs remain in `main` history (commit `7177883`, pushed). Removing them needs a history rewrite and a force-push, which is the owner's decision.
