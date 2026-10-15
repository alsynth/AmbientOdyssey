# Ambient Odyssey — Claude: complete every decided draft and assemble the next full private import

**15 October 2026 · Minecraft 1.21.1 · NeoForge 21.1.252 · private experimental build**

## 1. Your assignment and the owner's latest instruction

Build **one complete, installable private CurseForge import ZIP containing everything that has been decided**, including all relevant source draft implementations that have not yet been compiled or tested. Finish the integration/build work necessary to turn those sources into actual packaged runtime artifacts. Do not merely collect source files or return another plan.

The owner explicitly said:

> “write a highly detailed handoff for claude to put together the import zip, then we will run tests here”
>
> “include all source draft implementations even that ones that havent been complied or tested, we will test it here, have him put everything that has been decided in”

Accordingly:

1. Lack of prior compilation or runtime tests is **not a reason to omit an approved draft** from the experimental integration. Repair compile errors, reconcile overlapping versions and package the implementation.
2. Perform the build/packaging checks needed to produce a legitimate import: compilation, resource/manifest validation, duplicate detection, ZIP integrity and hashes. Write or update the runtime acceptance/probe scripts as needed.
3. **Do not require a new Minecraft playtest or run a full client/server/statistical test campaign before producing the ZIP.** We will run those tests back in this Codex chat. Label the new ZIP untested wherever it is untested.
4. Do not silently use the previous R1 ZIP as the new result: it predates the newest loot decisions and the unique-weapons-only correction.
5. “Everything decided” does not authorize inventing unspecified probabilities, unknown boss identities, missing registry IDs or approvals for unreviewed items. Finish every concrete approved slice, and make genuinely unspecified decisions visible in a precise exception ledger. Do not hide an entire approved feature behind a broad “later” label because some individual sources still need verification.
6. Build only in an isolated experimental branch. Do not merge into main, replace historical artifacts, deploy a live profile or generate the permanent world.

The server is obsolete and will be rebuilt fresh. **There is no current server package to preserve, migrate or treat as authoritative.** Keep old files/backups intact, but construct the new candidate from the pinned baseline and approved integration. The owner's currently installed client version remains unknown; do not claim this new package is installed.

## 2. GitHub source of truth and exact checkpoint

Repository: `alsynth/AmbientOdyssey`.

Continue from the latest HEAD of **`experimental/master-integration-20261015`**, draft **PR #63**:

- PR: https://github.com/alsynth/AmbientOdyssey/pull/63
- Source branch: https://github.com/alsynth/AmbientOdyssey/tree/experimental/master-integration-20261015
- This handoff: `docs/handoffs/CLAUDE_COMPLETE_IMPORT_ZIP_HANDOFF_20261015.md`.

Important history:

| Checkpoint | Meaning |
|---|---|
| `138259fd3c6efcdfdc287cc1a7d7c68fae69f0c9` | Gameplay source that produced the prior tested R1 ZIP. **Not the newest loot implementation.** |
| `b76c84da9e40f09c8b6c9587d0fe1c89aff6c40c` | R1 evidence and byte-exact original rollback preservation. |
| `455a7cc1e6593df93b37d0ce2cb5275830d90a68` on `handoff/boss-balance-package-review-20261015` | Latest fetched upstream owner-decision documents: additive loot, corrected rarity rates, exclusions, Grand Treasure definition. |
| `5c9b49f` | Merge of that upstream handoff into the integration branch. |
| Commits after `5c9b49f`, including this handoff | New loot source drafts, source-audit outputs and packaging continuation instructions. **Uncompiled/untested unless a newer receipt explicitly proves otherwise.** |

Read the actual HEAD and preserve its SHA in your output receipt. Do not assume a PR title, an earlier successful workflow or the presence of a JAR proves it contains current source.

### Read in this order

1. This handoff and the two quoted latest owner instructions above.
2. `docs/handoffs/LOOT_OVERHAUL_OWNER_DECISIONS_20261015.md` — read to the end; later corrections override earlier paragraphs.
3. `docs/handoffs/LOOT_ADDITIVE_ONLY_VERIFICATION_GATE_20261015.md`.
4. `docs/handoffs/GRAND_TREASURE_AND_T2_LOOT_PILOT_20261015.md` — its final native-best-pool definition overrides the initial custom-bundle proposal.
5. `docs/handoffs/REGALIA_OWNER_REVIEW_QUEUE_20261015.md` — later blanket exclusions override its early individual approvals.
6. `docs/handoffs/WORK_MODE_MASTER_IMPLEMENTATION_HANDOFF_20261015.md` — original 20-PR audit and all continuing constraints.
7. `docs/handoffs/integration-20261015/README.md`, `VERIFICATION.md`, `pr-audit.json`, `boss-reconciliation.json`, `native-balance-ledger.json`, `dd-effective-zones.json`, `final-package-receipt.json`.
8. The new source drafts and `docs/handoffs/loot-update-20261015/` outputs listed below.
9. `AGENTS.md`, current workflow/map, and relevant older PR sources when resolving a conflict. Some root status/TODO prose is historical and must not override the newer decision records.

The original `NEXT_AGENT_PACKAGE.zip` has now been imported into GitHub under `docs/research/next-agent-package-20261014/`: all documents 00–21, tools and 39 original rollback configs. Its older text saying the package was not imported is stale. All 39 supplied hashes were verified, and Git attributes preserve original bytes. Its historical Geburah and Brutal Bosses decisions are superseded.

## 3. The previous full package: use as provenance/rollback, not as a substitute for the new build

Private **unpublished draft release** containing R1 and its receipts:

https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-b03689fd5a3d66649cf0

Release API ID: **413289070**. A public unauthenticated request may not see a draft release; use the authorized GitHub account/API.

### Known R1 artifact

- `Ambient-Odyssey-MASTER-INTEGRATION-R1-PRIVATE-20261015.zip`
- Size: **154,479,187 bytes**
- SHA256: **`c8850ebf0fe89fa9bcde42eaf4f9fb1e60f9c98a289633bf820f3a5a8749f85b`**
- 337 CurseForge references = 330 official mod references + 7 resource/shader references.
- 10 bundled custom JARs; expected **340 direct production mod JARs after import**.
- 153 configured Questlog entries / 20 configured chapter files, including original 52 quests / 13 chapters; original 32 manual pages preserved.
- 83 of the added entries are reading acknowledgements, not proven combat tasks.
- The R1 package was rebuilt byte-identically.

Other assets in that same release:

- `Ambient-Odyssey-MASTER-INTEGRATION-R1-PRIVATE-20261015-Rollback.zip` — exact changed PR50 payloads plus removal receipt, **not an import ZIP**.
- `Ambient-Odyssey-MASTER-INTEGRATION-R1-PRIVATE-20261015.zip.report.json` — every ZIP member SHA256, custom JAR hashes, before/after path inventory.
- `AO-Master-Integration-Verification-and-Handoff.zip` — research/evidence archive.
- `VERIFICATION-AND-BLOCKERS.md`, `OWNER-TEST-STEPS.md`, `CHANGELOG-AND-ROLLBACK.md`.
- `STATIC-VERIFICATION.json`, `DEPENDENCY-AUDIT.json`.

### Original reconstruction base

The existing packager is hash-gated to the exact PR50 full import:

- `Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip`
- Size: **154,378,233 bytes**
- SHA256: **`dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f`**
- Original 338 references; 7 inherited custom JARs.

Use that exact baseline and the reviewed packaging chain, or derive a new audited packager from the exact R1 archive. If deriving from R1, explicitly replace its campaign JAR and other changed payloads rather than layering duplicate versions. Never disable a hash gate just to accept an unrelated ZIP.

The repository's old root/source-lock roster is **not** the complete current import roster. Its updated legacy static count is 329 after Sky Arena removal, while the complete R1 import has 337 references. Do not “fix” this by dropping the additional PR50 pins or reintroducing removed mods.

## 4. Continuing structure/worldgen and difficulty decisions

### Generation-sensitive content

- Remove **Demi's Sky Arena**, including Sky/Ice Arena content: CF project **1141465**, file **7053645**, original JAR `SkyArena-1.3.6-1.21.1.jar`.
- This does **not** remove unrelated Sky Whale Ship content.
- Four obsolete Sky Arena configs and its density-compiler input were removed in the integration. Do not let an older compiler regenerate them.
- Preserve existing Paxi aliases for Foundry corridor gears and Mechanical Nest decorations. Do not add duplicate fixes for aliases already supplied.
- Brutal Bosses must be **70 spawn chance / 30 minimum distance / HP ×4 / damage ×3**. Not ×4 damage. Individual boss JSONs, spawn tables and dummyboss remain unchanged.
- Preserve FTF/curated climate, installed biome content, existing structure repairs and generation settings unless a later explicit decision requires a scoped change.
- No permanent pregen. Overworld first when the later acceptance gates pass; Nether/End/modded dimensions later.

### Dungeon Difficulty approved attributes

These are additive-to-base DD modifiers for eligible ordinary mobs, independent of native boss multipliers:

| Structure tier | HP `MULTIPLY_BASE` | Attack `MULTIPLY_BASE` | Armor `ADDITION` |
|---|---:|---:|---:|
| T2 | 1.0 | 0.4 | 3 |
| T3 | 1.5 | 0.6 | 5 |
| T4 | 2.0 | 0.8 | 8 |
| T5 | 2.5 | 1.0 | 11 |
| T6 | 3.0 | 2.0 | 15 |

- R1 has **23 scoped Overworld zones**, not 497 verified/active zones.
- Full Dungeon Crawl is T3; Foundry is T6; Philip's level-three ruins follows selected category-default T2.
- No generic Tier0/1 scaling, no blanket Mechanical Nest ordinary-mob zone, no global wild-mob buff.
- Pasterdream and non-Overworld candidates remain Review Later for this phase.
- Structure tiers and boss tiers are separate. A T8/T9 boss does not imply a T8/T9 DD type; defined ordinary DD types stop at T6.
- Frosted Prison/Sunken City DD structure tiers remain held rather than borrowing boss tiers. Acropolis is End-side in the current policy.
- Preserve owner ledgers in `experiments/structure-difficulty-v4/`. Include approved executable drafts after reconciling exact IDs/dimensions; do not copy all provisional catalogue rows into active config.
- The broad expansion goal remains: add decided eligible sites as their actual effective source/dimension is established. An untested source implementation can be packaged experimentally under the latest owner instruction; an invented ID or unapproved classification cannot.

No newer numeric boss/DD schedule was found in the fetched branch delta. Most new commits concern the loot economy that sits on top of the already integrated structure/boss/difficulty decisions. Do not invent new combat changes because the user mentioned those areas generally.

## 5. Boss combat and classification: preserve exact exceptions

| Boss category | HP target | Ordinary direct attack target |
|---|---:|---:|
| T2 | ×2 | ×1.5 |
| T3 | ×3 | ×2 |
| T4 | ×5 | ×3 |
| T5 | ×7 | ×4 |
| T6 | ×10 | ×5 |
| T7 | ×10 | ×6 |
| T8 | ×10 | ×10 |
| T9 | ×10 | ×10 |

- **Chesed, Malkuth, Geburah: T5 category; completely exempt from both ordinary HP and damage scaling.** Preserve hit counters and vulnerability mechanics.
- **Dead King and Captain Cornelia: T6 category, loot and quest rewards; T7 combat treatment ×10 HP / ×6 attack.** Never give them T7 loot because of the combat exception.
- Ignis, Maledictus, Leviathan: T8. Tyros, Scylla, Obsidilith: T9.
- Bosses'Rise **is** Block Factory's Bosses, not a missing separate mod.
- Mother of Maze is not a boss.
- Mechanical Nest boss is intended near Harbinger, but exact identity/tier reconciliation is unresolved; no blanket minion buff.
- Accept the observed native 1024 HP cap. Preserve the requested uncapped target and actual configured/observed value separately; never advertise capped health as achieved ×10.
- Ordinary attack fields do not prove scaling of spells, waves, fixed ability damage or percentage-health attacks.
- Preserve Stronger Fire Boss soul mode and native participant behavior. Do not duplicate the separate future damage-reinforcement addon.
- No additional elite-gatekeeper subset. Keep legitimate existing campaign progression gates unless explicitly superseded; native gem progression is discussed separately below.

R1 applied **51 native config field changes**. Use `native-balance-ledger.json` as the exact before/after field inventory. It covers Cataclysm, BOMD, Block Factory, Remnant, Iron's and Hydra-specific HP. `defaultconfigs/irons_spellbooks-server.toml` and `defaultconfigs/block_factorys_bosses-server.toml` are required for fresh worlds.

Outstanding routes are real work, not fictitious completion: Cornelia/Last of Deepslate have no verified native config route; Hydra ordinary damage lacks a native key; Lich's ordinary attack differs from missile damage; Coralssus lacks a mapped combat section; Eternal Starlight family selection is still TBD. Include every actual approved source implementation you can reconcile, but do not create a competing generic scaler or silently buff shared surface-dragon species settings.

## 6. Latest boss loot contract — implement and package it

Preserve native drops/uniques/materials. **Every eligible player-credited T2–T9 boss kill, including repeat kills, gets these separate additions:**

1. One genuine randomized **Apotheosis-affixed equipment item**, generated through the installed Apotheosis API and normal world-tier rules for the guaranteed roll.
2. One eligible **Regalia item** from the curated supplemental pool, respecting exclusions and native-exclusive acquisition.
3. One **Simply Swords UNIQUE WEAPON**, using the verified installed native unique-weapon pool.
4. For categories T6–T8, the independent extra affixed-item rolls below.

### Critical newest correction from this chat

The owner answered the ordinary-versus-all-weapon question:

> “bosses should only include weapons that count as unique weapons”

This **supersedes** all prior “whole installed sword pool”, “all swords”, and “full native weapon pool” descriptions. Do not include ordinary iron/gold/diamond/netherite/runic weapons merely because the broad `c:swords` tag contains them. Conversely, do not exclude a powerful weapon, hammer or other weapon type if it genuinely belongs to the installed unique-weapon class/pool.

Native source: `simplyswords-neoforge-1.70.2-1.21.1.jar`, tag **`simplyswords:uniques`**. The source audit found **58 tag records**, not 58 runtime-verified item IDs. Some records are optional objects such as `{ "id": "simplyswords:dreadtide", "required": false }`. Normalize string and object entries, resolve actual installed registered unique weapons, retain valid awakened variants, and skip genuinely absent optional IDs with an explicit receipt. Do not use only the smaller `lootable_uniques` tag if it would omit registered approved unique variants without an acquisition/progression reason.

### Approved independent rare affixed-equipment chances

| Boss category | Ancient | Artifact | Heirloom | Esoteric |
|---|---:|---:|---:|---:|
| T6 | 20% | 2% | — | — |
| T7 | 25% | 8% | **5%** | — |
| T8 | 30% | 15% | **8%** | **5%** |
| T9 | deferred | deferred | deferred | deferred |

These are extra affixed **items**, not gems and not a replacement rarity distribution for the guaranteed item. Rolls are independent: more than one extra can proc. Do not reintroduce the superseded T8 Heirloom 5%, T8 Esoteric 2%, or old T7 Heirloom 1%. T9 special/rare odds are deferred; do not invent them.

### Ownership and repeat kills

The new source draft uses one set of additions per player-credited kill and targets pickup to the credited killer. It does not grant one full set to every nearby party member. This is an implementation assumption requiring later multiplayer verification, not a separately owner-accepted party-credit model. Preserve native ownership/per-player reward mechanics and do not multiply rewards through a second `_per_player` table or double event path. Native drops must not be filtered, cleared, replaced or reassigned.

## 7. Regalia scope and exclusions

The owner wants broad access: approximately **90% of verified suitable eligible Regalia available at/before T5**, with only genuine exceptional combat cases held later. This is not permission to treat every unscored catalogue item as safe or to add every ordinary equipment entry as Regalia.

Binding supplemental-pool exclusions:

- **All Enigmatic Legacy and Enigmatic Legacy Plus items are native-only**, at all tiers, regardless of crafting or older proposed weights. No 0.1× weighting scheme; do not alter their native loot or recipes. The Infinitum is native-only, overriding its old T6–T7 proposal.
- **Pasterdream/NeoPasterDream accessories are native-only**. This supersedes old early approvals for Cecilia's Blessing, Turnback Cloak, Evasion Cloak, Counter Ring and Ghost Face Head. Qym Head stays native-only. Do not blanket-ban unrelated Pasterdream weapon families without determining their type.
- Cursium Chestplate: native-only.
- The Annihilator: still unapproved for the new generic bonus pool; do not silently include it.
- Do not copy guaranteed native boss-exclusive trophies into unrelated low-tier generic rewards.
- Simply Swords unique weapons are the separate third guarantee; do not let the Regalia list reintroduce a duplicate ordinary/full weapon pool.
- Eternal Starlight does not need a new restrictive item-by-item gating exercise. Use verified eligible IDs and preserve native acquisition/progression.

Explicit approved non-excluded high-risk exceptions: **Abyssal Tiara** and **Tempest Trident** are eligible in the broad T2–T5 supplemental pool. Their C4 editorial flags do not override the owner's approval.

Catalogue sources now copied into the integration branch:

- `docs/balance/REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv` — 497 candidates; 421 unscored, 32 C3/C4, not 497 authenticated rewards.
- `docs/balance/REGALIA_ITEM_CATALOGUE_EXPANSION_2026-10-13.csv`.
- `docs/balance/README_REGALIA_COMBAT_RANKING_20261013.md`.

The current compiler draft selects a conservative subset of already described C0–C2 Artifacts plus the two approved Aquamirae exceptions. **That is not completion of the broad curation goal.** Finish source/registry validation for the remaining suitable decisions rather than claiming the small draft subset covers the entire catalogue. Preserve an included/excluded/held list and each item's evidence.

## 8. Native gems and progression — undo the superseded campaign prototype

The latest owner decision is **native Apotheosis gem drops and crafting, including apex-tier crafting, remain authoritative**. Do not introduce bespoke AO gem drops, custom gem gates or artificial boss gemstone chances. Affixed-item rarity is not gem grade.

The older campaign prototype had first-clear Artifact/Heirloom/Esoteric gem grants and a T6 automatic Pinnacle-unlock route. The new source draft removes those from `AOCampaign.death`. Complete the reconciliation:

1. Do not ship an old `ao-campaign-0.2.0-experimental.jar` that still contains those old grants.
2. Preserve native world-tier advancement/unlock and gem recipes/drops. Do not change global weights or unlocks just to make a bespoke gem route work.
3. Update `tools/compile_ao_v050_campaign.py`, generated quest descriptions/objectives and mapping CSVs that still refer to `artifact_reward`, `heirloom_reward`, `esoteric_reward` or the boss-as-Pinnacle route. Preserve stable quest IDs; do not leave unreachable objectives or a description promising a removed gem reward. Use honest native-progression information or an appropriate existing boss milestone where justified.
4. `BossGems.java` may remain historical source, but it must not be an active production reward path. Old probes testing it are not evidence that bespoke gem rewards remain desired.
5. The unrelated held-item `/ao_mastery upgrade` campaign decision and its existing Tyros/Scylla/Obsidilith requirements are not automatically deleted by “native gems”. Preserve it unless a newer specific decision changes it.

The latest draft also deletes the **Bonus Chest gem-injection exemption** so native gem drops are no longer suppressed there. Finish the corresponding packager/validator changes. The two affix-only Bonus Chest anti-double-roll exemptions are a separately documented legacy exception needed for the approved exactly-one-affixed-starter result, not permission to suppress normal chest affixes anywhere else.

## 9. Dungeon additions: native best-pool Grand Treasure and T2 enhancement

### Approved Grand Treasure behavior

- Starting at structure T3, **5% independently per eligible dungeon chest**, not per dungeon and not an archetype allocation.
- On proc, append **one additional draw from that structure's existing best appropriate native loot pool**.
- Never replace original contents, generate the whole native multi-pool table a second time, copy fixed boss trophies, or invent a diamonds/books reward catalogue.
- Preserve the chosen native entries' relative weights, conditions, functions, access/dimension predicates and unique/first-clear semantics.
- No Grand roll for T0–T2, starting Bonus Chest, arbitrary villages, decorative barrels, unrelated shared vanilla tables, early Mine Cells, spawner farming or fixed trophy/quest chests.
- Native chest Apotheosis affix probabilities and gem rules remain unchanged.
- Use Lootr's per-player generation once; no new roll on reopen/relog/restart. Prevent recursion and double modifier registration.
- If a source hash/provider/pool is wrong or missing, skip the optional addition with an explicit diagnostic; never discard native loot.

### Current source audit: useful evidence, not a finished rollout

`tools/audit_additive_loot_sources.py` traverses current scoped structure start pools, jigsaw/NBT template references and chest loot IDs against exact installed resources, including source Paxi overrides. It currently produced:

- **70 chest/structure contexts**, after excluding non-chest block types in the second pass.
- **14 narrow Grand candidate contexts** with basic valuable native pool candidates.
- Detailed paths/hashes in `docs/handoffs/loot-update-20261015/chest-source-audit.json`.
- Proposed mappings in `grand-treasure-candidates.json`.

These are **SOURCE-ONLY** outputs. They do not prove natural placement, final effective runtime resource priority or Lootr behavior. The current “best pool” selector uses a simple scoring heuristic for basic native treasures; it is **not owner approval that this is the best appropriate pool**. Finish that review against the complete same-structure native rewards. Do not promote a weaker arbitrary pool simply because the actual best pool needs investigation, and do not claim 70 active Grand sources when only 14 candidate contexts exist.

### New Grand source draft

`GrandTreasure.java` attempts an exact-table + exact-structure + Overworld-scoped append-only global loot modifier. It verifies effective native table bytes against the captured SHA256, extracts a selected single pool, sets its roll count to one, preserves functions and uses raw generation to avoid calling the whole global modifier chain again. It has recursion/context guards and fail-closed diagnostics.

**This class has not been compiled or runtime-tested.** Review resource-reload caching/rejection behavior, lookup APIs, raw generation semantics, pooled conditions, RNG ownership, concurrent calls and Lootr context before declaring the implementation complete. Include the finished compiled feature in the experimental ZIP; mark runtime checks pending rather than omitting it merely for lack of prior gameplay testing.

### T2 Scrap/Treasure remains a separate decision

The owner approved improving existing Scrap/Treasure starting T2, without changing worldgen/chest counts or rewriting whole native tables. **Exact per-source increase amounts remain unapproved.** Produce actual native before/after proposals and keep this numerical gap explicit. Do not silently freeze an invented multiplier, and do not confuse the decided 5% Grand chance with an approved T2 boost. Source tooling and all already decided implementations must still be included in the handoff/build rather than dropped.

## 10. Exact new source drafts and known build blockers

These files are intentionally included even though they have not yet been compiled/tested. They are **implementation drafts, not proven finished features**:

| Path | Current purpose / limitation |
|---|---|
| `addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/BossRewards.java` | Append-only `LivingDropsEvent` additions; native affix factory, curated Regalia, unique tag pool, independent rare rates. Compile and complete validation/ownership behavior. |
| `addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/GrandTreasure.java` | Scoped 5% single-native-pool draft described above. Uncompiled. |
| `addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/AOCampaign.java` | Registers new providers and removes old gem/Pinnacle grants; remaining journal/mapping reconciliation still required. |
| `addons/ao-campaign/build.gradle` and `src/main/resources/META-INF/neoforge.mods.toml` | Source version bumped to **0.3.0-experimental**; no matching built 0.3.0 JAR exists yet. |
| `.../data/ao_campaign/loot_modifiers/grand_treasure.json` | New serializer entry. |
| `.../data/neoforge/loot_modifiers/global_loot_modifiers.json` | `replace:false`, adds Grand provider; unresolved Rage Glove provider remains inactive. |
| `tools/audit_additive_loot_sources.py` | Exact installed-resource/source-NBT audit; currently has local default path to the prior isolated runtime's mods. Parameterize or supply an authenticated cache when running elsewhere. |
| `tools/compile_additive_loot_policy.py` | Draft policy compiler. **Currently fails**, see below. |
| `docs/handoffs/loot-update-20261015/` | Source-only chest/unique-tag snapshots with hashes, including optional tag entries. |
| Deleted `release_030/.../ao_starter_apotheosis_exemptions/.../gem_loot_injection.json` | Restore native gem behavior; finish dependent packager changes. |
| `tools/validate_ao_starter_apotheosis_exemptions.py` | Updated draft expects two affix-only exceptions and no gem override; no rerun for this revision. |

### Fix these concrete issues before building the new ZIP

1. **Policy compiler failure:** `sorted(set(unique))` raises `TypeError: unhashable type: 'dict'` because the native unique tag contains optional object entries. Normalize the tag records properly, preserve optional/required semantics, authenticate registered unique weapons and rerun the compiler.
2. Consequently **`addons/ao-campaign/src/main/resources/ao_loot_policy.json` has not been generated** at this checkpoint. `BossRewards` requires it at runtime. Do not build a JAR missing this policy or substitute an empty policy and call the guarantees done.
3. `tools/package_master_integration.py` still selects **campaign 0.2.0**. Update it to the newly compiled **0.3.0** or your versioned successor. It must not silently package the old JAR from an existing `build/libs` directory.
4. `tools/log-probe/build.gradle` also still references campaign 0.2.0. Update before preparing the future Codex test probe.
5. `tools/package_ao_loot_economy_pilot.py` still tries to read the now-deleted **gem_loot_injection.json** exemption. Reconcile it with the two affix-only legacy exceptions; do not restore the obsolete gem suppression just to make the old script succeed.
6. `tools/validate_master_integration.py` currently expects **no campaign global modifiers**, because R1 only disabled Rage Glove. Update the exact expected list to the reviewed append-only Grand provider and assert Rage Glove remains absent. Preserve duplicate/`replace:true` protections.
7. `tests/test_master_integration.py` has the same R1 empty-list assertion. Update it to test the actual new contract rather than loosening validation indiscriminately.
8. `tools/compile_ao_v050_campaign.py`, generated quest JSONs, notes and old packager text still describe obsolete boss gem routes and/or old campaign behavior. Regenerate all affected resources while retaining stable IDs.
9. Review actual compilation of `BossRewards` and `GrandTreasure` against NeoForge 21.1.252 / Apotheosis 8.9.0. No compile or native API check was run after these drafts were written. Treat every assumed method/type as needing the compiler, especially unique-tag lookup, player attribution and native single-pool codec/raw generation.
10. Expand/verify the curated Regalia policy without reintroducing excluded mods, unscored progression-breaking items or native boss-exclusive trophies. Record every omitted/held candidate explicitly.
11. Extend the boss reward mapping only with actual approved boss-category IDs. The draft intentionally holds unknown T2/T3 identities, unselected Eternal Starlight family members and underground-vs-surface dragon ambiguity; do not pretend a broad generic “boss” matcher solves category selection.
12. Cache invalidation/retry in `GrandTreasure` needs review: a rejected source should not remain incorrectly rejected after a valid reload/rollback, and the same context must not be rewarded twice. Do not infer successful behavior from source guards alone.

The owner's latest instruction authorizes completing these draft implementation/build issues without asking again simply because they are untested. It does not authorize skipping compiler errors or shipping source-only placeholders instead of compiled production code.

## 11. Preserve all other integrated decisions

- Starter addon **0.2.0**: keep **original vanilla Bonus Chest loot**, then add one of the five genuine Enigmatic spellstones uniformly, one genuine affixed item Common55/Uncommon30/Rare15, 32–48 added torches and 16–48 added cooked meat. Bonus Chest OFF gives nothing. Only that exact optional table is targeted. The Regalia Enigmatic exclusion does **not** cancel this separate approved onboarding reward.
- Lootr per-player Bonus Chest whitelist and conversion draft stay included, with multiplayer verification pending.
- Goblin Tuned chainmail: **32 diamonds + 4 `irons_spellbooks:cinder_essence`** per piece; preserve 22 native epic offers and equipment components.
- Flight Ring recipes from PR51 stay included; no silent old-recipe reversion.
- Sigils **0.1.1**: Common–Mythic 1/2; Ancient reroll6/upgrade12; Artifact18/36; Heirloom24/48; Esoteric32/64. Preserve native XP costs and the actual installed r19 rarity namespace.
- Keep armor trim integration, Q/E placement, tooltip fixes, supported Mine Cells integration, native gem/crafting systems and existing original quest IDs/manual.
- Simply More stun/implicit_stun/dazzled suppression remains included.
- The old **10% Netherite Monstrosity Rage Glove gate is not approved** and stays inactive. Do not filter native Rage Glove drops. Its retained research class is not a license to register it.
- Preserve exact inherited Wet Sand and Apotheotic port binaries; source/version/hash verification is required for any replacement. Do not rebuild the owner's port from unrelated source or silently upgrade it.
- No Origins, Ocean Loot, MCA Reborn, Big Globe, Mob Plaque or reintroduced Subtle Effects/exclusive patch.
- Custom AO menu, Quest Atlas and optional realm campaigns remain accepted later work, not permission to fabricate completed features in this ZIP. Include actual approved source drafts if present, but distinguish an installable implementation from a design document.

## 12. How to assemble the full import

Use `tools/package_master_integration.py` as the starting packaging chain, after the concrete repairs above. It builds on `tools/package_ao_full_pr54.py` → `tools/package_ao_loot_economy_pilot.py` with the exact PR50 base, overlays current source configs/campaign, removes Sky Arena from both manifest and internal roster, validates counts and writes receipts/rollback. It is not currently updated for the new 0.3.0 policy.

Suggested build sequence:

1. Clone/fetch GitHub and record the chosen integration HEAD. Inspect `git status`; preserve unrelated local work.
2. Read all latest decisions; complete/reconcile the source drafts instead of selecting an older precompiled artifact.
3. Obtain exact PR50 or exact R1 source archive and verify the required SHA256 before extraction. Preserve it untouched.
4. Obtain hash-matching official dependencies and all inherited custom binaries from authorized prior artifacts/cache. Source-lock counts alone are insufficient. Use the R1 member/JAR receipt to verify unchanged files.
5. Normalize/finish new policy and source-specific Grand mappings. Reconcile journal content, legacy affix exceptions and native gem restoration. Record included/held sources accurately.
6. Compile production addons against **Java 21 / NeoForge 21.1.252 / Apotheosis 8.9.0**. This is mandatory packaging work, not a Minecraft gameplay test. Use a clean output selection; do not let stale `build/libs` JARs satisfy a filename check.
7. Verify the compiled JAR actually contains `BossRewards.class`, `GrandTreasure.class`, the generated policy, correct metadata version, serializer resources and only the reviewed global modifier entries. Verify current Starter/Sigil source resources too.
8. Assemble **one full CurseForge import** with root `manifest.json` and `overrides/`. A delta/config kit or a ZIP of the repository does not satisfy the task.
9. Keep one current version per custom addon. No probe/GameTest/development JAR in the import. Preserve original seven inherited custom artifacts unless a deliberately reviewed replacement is required; three integration addons make the prior total ten. Recompute counts instead of hardcoding if the actual architecture changes.
10. Keep the 337 complete-import CF pins unchanged except explicit later approved roster changes. Sky Arena stays removed. Do not conflate mods with the seven resource/shader refs or count nested Jar-in-Jar libraries as direct mod-folder JARs.
11. Preserve exact fresh-world SERVER configs in defaultconfigs; ship client/server-compatible addon code. A full client import is not, by itself, proof that a dedicated server can load the same 340 direct client mods.
12. Run source/resource/manifest/ZIP build checks. Produce a source-to-JAR and source-to-package report. Do not run the deferred Minecraft test campaign here.
13. Use a **new version/name**, for example `Ambient-Odyssey-MASTER-INTEGRATION-R2-ALL-DECIDED-PRIVATE-20261015.zip`, and corresponding manifest/version text. Do not overwrite R1 or any older asset. A different date/name is fine if actual work occurs later.
14. Write full SHA256/member/JAR and before/after inventories, a reversible rollback package, changelog, known-issues ledger and the exact commands for our later tests.
15. Push the implementation/build fixes and handoff/evidence to a separate experimental continuation or the authorized integration PR. Upload the new full ZIP and receipts as a **private unpublished draft release**. Do not promote to public/stable.

### Tooling and local-cache notes

The previous Windows build used Java 21 and Gradle 9.2.1 with a cached `net.neoforged.moddev` plugin 2.0.148. Use the repository Gradle files; no wrapper is assumed. The earlier starter isolated native setup used `-PaoRuntimeMods=<exact-mod-cache>` to supply Curios/Caelus where Maven cache was incomplete. These are build environment details, not source identity proofs.

The audit and rehearsal helpers currently contain local runtime/cache paths from Codex. On another machine, parameterize or supply equivalent verified inputs. Do not treat nonexistent paths as a reason to substitute arbitrary newer JARs. `tools/rehearse_master_integration.py` and `tools/run_full_pack_log_probe.py` are for later testing here, not production packaging.

## 13. Honest evidence boundary: what was actually tested before these new drafts

Only the **old R1 ZIP/hash** has the following evidence:

- Source/addon builds; two Sigil and two starter native GameTests passed.
- Integrated client startup, flat-world join and save/exit, exit 0.
- Native 153-quest parse/campaign synthetic checks.
- All 23 DD zone structure IDs registered; Sky Arena absent.
- Synthetic DD spawn-event fixtures passed, including outside/excluded controls.
- 600 actual native Bonus Chest loot rolls each yielded one spellstone and one affixed item; Common345/Uncommon177/Rare78.
- Finalized Dead King observed **1024 capped HP / 60 attack**. This is a spawn-setup observation, not proof of every phase or real damage.
- Config/archive/rarity/exemption checks and duplicate/member verification; byte-identical repeated R1 build.
- Python suite 66 pass / 2 existing historical-audit failures (stale 50-quest and removed Hominid-candidate assumptions).
- Dependency metadata had no direct issues, with embedded/bridge caveats.

**None of that tests the new 0.3.0 loot drafts, native-gem restoration, unique-only weapon rewards, rare-rate rolls or Grand Treasure implementation.** Do not transfer old PASS labels to the next ZIP. R1's three-exemption evidence is historical now that gem suppression is being removed.

Existing runtime diagnostics included BetterEnd guidebook, Iron's Jewelry test-material table, Traveloptics native tag, advancement and other warnings. No error-free runtime, normal-FTF natural structure, dedicated-server, multiplayer, real boss fight/ability/respawn, shader performance or Chunky freeze acceptance was claimed.

## 14. Tests to prepare for return to Codex — do not use them as a packaging delay

Return the new ZIP first with clear UNTESTED labels, then we will run:

1. Exact new ZIP hash/roster and isolated integrated startup/join/save.
2. Native registry validation for every boss, Regalia item, required/optional unique weapon, rarity and mapped chest pool.
3. Every-kill boss event samples for T4/T5/T6/T7/T8/T9 categories and a non-boss negative case; original drop object/content preservation, one guaranteed affix, one Regalia, one unique weapon, and no ordinary/runic weapons.
4. Rare-rate statistics separately from guaranteed items; zero forbidden high-tier/gem additions and correct Dead King/Cornelia category treatment. Test repeat kills, credited-killer pickup and no extra party multiplication.
5. Compare native baseline versus patched chest outputs and affix distribution. Validate Grand incidence near 5% over a meaningful sample, exactly one selected native pool draw, native conditions/functions retained and no full-table/trophy duplication.
6. Negative Grand cases: T0–T2, outside structure, wrong dimension, village/decor barrel, Bonus Chest, early Mine Cells, unrelated shared table, changed source hash, missing pool, duplicate/reentrant call.
7. Two non-op players using the same unopened Lootr chest; independent original+bonus rolls, no reroll on reopen/relog/restart, new player after another opens it, server save persistence.
8. Native gems, apex crafting, world-tier unlocks and journal objectives after removal of custom gem/Pinnacle grants; retain legitimate item-mastery behavior and original quest IDs.
9. Fresh dedicated-server assembly/sidedness and two-client startup; normal FTF natural arenas, actual boss setup/phases/abilities/respawn, native capped HP, FD exemptions, elite stacking.
10. Only after that, normal-world generation/performance and a disposable 1k Chunky pilot. No permanent 10k–20k pregen from a synthetic PASS.

Prepare updated probe source and exact invocation steps, but mark every new test NOT RUN until it is actually run in this chat or a separately documented authorized test session.

## 15. Required return package and completion report

Return all of these, with direct private GitHub links:

1. Full new CurseForge import ZIP containing **all decided executable changes and completed source drafts**, including formerly uncompiled/untested implementations.
2. Exact source commit/branch and draft PR.
3. ZIP SHA256/size, full direct mod/CF roster, all custom artifact names/versions/hashes, and per-member inventory.
4. Changelog separating retained R1 content, newly implemented decisions and superseded prototypes removed.
5. Decision-to-implementation matrix: each approved change → source file → compiled JAR/config → final ZIP path → build-check result → runtime status. No silent omissions.
6. Exact native-before/after loot-source audit, preserved modifier conditions, current Grand mappings and held-source reasons; Regalia/unique included/excluded/optional ID lists.
7. Immutable rollback package and restoration instructions. Keep R1 and original PR50 untouched; include removal instructions for newly added files and old-version JAR replacement.
8. Known compile/build/packaging limitations, unresolved **decisions** and deferred runtime checks. Do not describe “not tested yet” as “not included” when an approved implementation can be compiled and packaged.
9. A short continuation prompt for this Codex chat to run the new build's tests using its exact hash.

For rollback, stop the experimental client/server and restore the original profile plus a cold **pre-test save backup**. Do not use an already generated world as a substitute for restoring removed/changed content. Existing world SERVER configs require their own restoration. The new server will be built fresh; never overwrite the historical private ZIPs, rollback branches or locked Tan's archive.

**Success means a newly assembled complete experimental import with all concrete owner decisions wired into actual artifacts, honest build receipts, explicit unresolved decisions, and runtime testing left ready for us here—not another documentation-only acknowledgement.**
