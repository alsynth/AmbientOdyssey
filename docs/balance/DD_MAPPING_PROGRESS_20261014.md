# Ambient Odyssey — Structure Catalogue Progress (October 14, 2026)

> **MOST RECENT OWNER APPROVAL — 14 October:** The previous 26 spawner-positive review holds are **all owner-approved Tier 0**, preserving their source NBT spawner evidence and leaving native spawns intact. The Dungeon Crawl structure `dungeoncrawl:dungeon` is **owner-approved overall Tier 4** (was provisional Tier 3), but the user requests **upper floors Tier 2**. The available DD configuration has no floor/height-aware selector; a relative-floor resolver is a separately gated implementation. **No live DD config changed.** The existing 100% known-ID tier completeness remains unchanged. Counts: 157 HIGH, 637 MEDIUM, 420 LOW, **26 OWNER_APPROVED**, zero remaining former owner holds. See [floor implementation note](DD_DUNGEON_CRAWL_FLOOR_TIER_2_TO_4_PLAN_20261014.md).


> **LATEST STATUS — 14 October, superseding historical progress tables below:** **1,240/1,240 known native IDs** and **1,130/1,130 current-profile known IDs** have numerical **first-pass PROVISIONAL** tiers. This is *not* 100% of the live registry, accurate encountered difficulty, owner approval, or shipped Dungeon Difficulty. **157 HIGH, 637 MEDIUM, 420 LOW, 26 OWNER_HOLD** confidence classifications; all 26 owner-held numeric placeholders are blocked from deployment. See [34-site postmap audit](DD_POSTMAP_CRITICAL_AUDIT_20261014.md), [34-ID worklist](DD_POSTMAP_CRITICAL_34_TIER_REVIEW_20261014.csv), and [5-site exact entity matcher audit](DD_POSTMAP_FIVE_SITE_ENTITY_MATCHER_20261014.csv). No gameplay changes. The former percentage tables remain solely as a chronological history.


**Current known-ID universe only, not proof all registered worldgen structures have been discovered.** All new Tier 0 assignments are **name/archetype-based proposals pending approval**; none changed the gameplay config.

| Metric | Previous | Current | Change |
|---|---:|---:|---:|
| Known native IDs, historical + scoped runtime extras | 1240 | **1240** | 0 |
| Working tier / variant-labelled IDs | 374 | **593** | **+219** |
| Unranked known IDs | 866 | **647** | **-219** |
| Working tier progress, all known IDs | 30.16% | **47.82%** | **+17.66 pp** |
| Current JAR / scoped-runtime relevant IDs | 1130 | **1130** | 0 |
| Relevant IDs with working tier/variant | 374 | **593** | **+219** |
| Relevant IDs still unranked | 756 | **537** | **-219** |
| Working tier progress, current relevant IDs | 33.1% | **52.48%** | **+19.38 pp** |
| Original owner-held exact native IDs | 26 | **26** | 0 |
| Additional owner-held low-looking source-template families | 15 | **15** | 0 |
| Source NBT families without verified registry/placement links | 63 | **63** | 0 |

## New batch: 219 Tier 0 proposals

[Detailed source-by-source candidate ledger](DD_PROVISIONAL_T0_SCENERY_SETTLEMENTS_20261014.csv) has one row for each proposed Tier 0, with exact name-policy, linked NBT indicator counts, mod provider and explicit approval pending.

| Provisional screening family | New Tier0 candidates | Confidence |
|---|---:|---|
| `MOOG_SCENERY_PROPS` | 68 | HIGH_NAME_DECOR |
| `CTOV_STANDARD_VILLAGES` | 51 | MEDIUM_NAME_ARCHETYPE |
| `TOWNS_AND_TOWERS_VILLAGES` | 26 | MEDIUM_NAME_ARCHETYPE |
| `MOOG_NETHER_SCENERY` | 23 | HIGH_NAME_DECOR |
| `FARMERS_OVERWORLD` | 12 | MEDIUM_NAME_ARCHETYPE |
| `BETTEREND_TERRAIN` | 11 | HIGH_NAME_DECOR |
| `INTEGRATED_VILLAGES` | 8 | MEDIUM_NAME_ARCHETYPE |
| `BWG_NATURE` | 7 | HIGH_NAME_DECOR |
| `UNDERWATER_NONCOMBAT_DECOR` | 5 | MEDIUM_NAME_ARCHETYPE |
| `CREATE_RUSTIC_BUILDINGS` | 4 | MEDIUM_NAME_ARCHETYPE |
| `NATURES_SPIRIT_VILLAGES` | 4 | MEDIUM_NAME_ARCHETYPE |

**Safety constraints:** Only IDs from current PR50 mod-JAR filenames that were previously **UNRANKED**, did not have a positive linked NBT spawner/trial block signal, and did not belong to any of the owner's 26 protected native IDs were considered. Obvious hostile/outpost/dungeon/arena/fortified/underground names were excluded. *No detected linked NBT spawner signal* is not proof a structure cannot have generated monsters: NBT scan is partial and no in-game native code, spawned mobs, full jigsaw/pool assembly, or live placement were verified. Each proposal is reversible and pending owner approval; do not translate it into DD config or finalized boss tiers.

## Progress interpretation and remaining work

**593/1240** known IDs have some working tier label (including 219 **new name-only provisional Tier0 proposals** and 4 unresolved variant-tier IDs), leaving **647 unranked**. The relevant installed/runtime universe is **593/1130**, leaving **537**. These are **coverage measures only**, NOT 52% game balance acceptance. Owner-approved and natural-generation-tested status must be tracked separately.

**Next mapping priorities:** The still-unranked high-count providers are Pasterdream 87, Dungeons & Taverns, IDAS, remaining Moog structures, CTOV/Towns & Towers pillager outposts, and structure mods with source-only unregistered templates (Create Structures Arise). Separate NPC combat from passive settlement variants; do not auto-tier low-looking spawner sites. Real structure registrations and worldgen assembly must be proven before the Chunky worldgen freeze, whereas DD effects can be tuned separately afterward.

- [All 1,240 known ID ledger](DD_KNOWN_NATIVE_ID_MAPPING_LEDGER_20261014.csv)
- [219 provisional Tier 0 suggestions](DD_PROVISIONAL_T0_SCENERY_SETTLEMENTS_20261014.csv)
- [Existing 26 owner-deferred](DD_OWNER_UNRANKED_SPAWNER_REVIEW_20261014.csv)
- [Source-only 63 unverified families](DD_UNMAPPED_PROVIDER_ENCOUNTER_FAMILIES_20261014.csv)
- [Machine-readable progress JSON](DD_MAPPING_PROGRESS_BASELINE_20261014.json)

## Remaining unranked current-pack IDs — prioritized after Tier0 proposal screen

The [537-record remaining source/encounter priority queue](DD_REMAINING_ACTIVE_UNRANKED_PRIORITY_20261014.csv) and [provider-level backlog](DD_REMAINING_BY_PROVIDER_20261014.csv) classify unresolved known current-package identifiers without promoting them. **These are unranked research records; some are disabled, incomplete, noncombat, aliases or differently dimensioned, so this queue is not a deployable 537-rule DD plan.**

| Review lane | Unranked native IDs |
|---|---:|
| `P0_NETHER_WORLDGEN_FREEZE_GATE` | 3 |
| `P1_PILLAGER_OUTPOST_SOURCE_REVIEW` | 43 |
| `P1_COMBAT_DUNGEON_OR_BOSS_REVIEW` | 23 |
| `P1_STATIC_NBT_SPAWNER_TIER_UNRANKED` | 2 |
| `P2_PASTERDREAM_DIMENSION_SOURCE_REVIEW` | 87 |
| `P2_SCENERY_OR_SETTLEMENT_UNVERIFIED` | 142 |
| `P2_PROVIDER_FAMILY_PROBE` | 115 |
| `P2_UNKNOWN_NO_TIER_EVIDENCE` | 96 |
| `OWNER_HOLD_UNRANKED_SPAWNER` | 26 |

The **26 owner-deferred spawner cases stay UNRANKED** and are intentionally last in operational review. CTOV/Towns & Towers pillager outposts remain separate **43-source-ID combat review targets**, not low-tier presumptions. Eternal Nether 3 are worldgen gates that require generation verification before pregeneration. Pasterdream's 87 unranked entries require dimension/code-level analysis. All other structure tiers remain provisional unless explicitly user-confirmed.


## October 14 — 42 provisional Tier 2 outpost variants

Mapped **42 pillager-outpost IDs** (31 Towns & Towers and 11 CTOV) to **proposed/unapproved Tier 2**, inheriting existing **provisional** vanilla Pillager Outpost Tier 2. The source archive identifies `towns_and_towers:towers` versus `minecraft:pillager_outposts` structure sets, not guaranteed equivalent enemy mechanics. **5 CTOV variants** have AO-compatibility datapack worldgen resource collisions requiring effective winner checks; optional Savage & Ravage addon resources may be disabled. **One other outpost, `ctov:pillager_outpost_mesa`, remains UNRANKED** due to no historical structure-set link. 42 IDs were not in the scoped positive PR50 client registry query, and there is no natural-generation or combat test.

| Mapping coverage | Previous | Current |
|---|---:|---:|
| Working-tier labels (all 1240 known IDs) | 593 (47.82%) | **635 (51.21%)** |
| Working-tier labels (1130 current-profile known IDs) | 593 (52.48%) | **635 (56.19%)** |
| Current-profile ID records still UNRANKED | 537 | **495** |
| Protected owner deferred native ID records | 26 | **26** |
| Protected source-template families | 15 | **15** |

[42 Tier2 outpost proposals](DD_PROVISIONAL_T2_PILLAGER_OUTPOSTS_20261014.csv). [495 remaining current-profile unranked](DD_REMAINING_ACTIVE_UNRANKED_PRIORITY_20261014.csv). Working tier coverage is not owner approval, DD functionality or natural-generation coverage. No mod, worldgen, loot, boss or DD configuration edits.


## October 14 continuation: +57 additional conservative Tier 0 proposals

The **latest authoritative totals** are **692/1240 (55.81%)** known ID working tier/variant labels, **548** still unranked; and **692/1130 (61.24%)** current-profile relevant tier labels, **438** still unranked. Previous PR56 totals immediately before this pass: 635/1240 (51.21%) and 635/1130 (56.19%). **+57 IDs; +4.60 pp all known; +5.05 pp current profile.** The earlier table in this document is historical (first 219 batch), not latest. Source JSON progress baseline and master ledger are authoritative.

Selected narrowly name-based scenery/utility archetypes: Moog Soaring trees and small cottages, Moog Voyager harmless-looking huts and log piles, Formations small houses/fountains/wells, nature End formations, scenery islands, small ruins and underwater broken-house/gate variants. Selection excluded all current owner-deferred IDs and all positive linked spawner/trial indicators in the partial source scan. **This is NOT verified peaceful placement or approval**; actual NBT and in-game spawn mechanics might differ. They are **provisional Tier0 labels only**, create no Dungeon Difficulty rules or gameplay config change. Existing 26 exact owner holds and 15 source-template family holds remain UNRANKED. This batch addresses catalogue % rather than claiming DD readiness.


## 14 October third T0 mapping batch — 62 provisional settlement/utility names

Previous current-profile progress: **692/1130 (61.24%)**; new: **754/1130 (66.73%)**; remaining 376. All known: **754/1240 (60.81%)**; remaining 486. This batch includes regular villages (excluding fortified/underground/occupied), taverns, wells, cottages, statues, small settlements and utilities with no positive linked NBT spawner or trial indicators in the *partial* scan. All assignments provisional Tier0 / user review pending; do not assume peaceful or deploy Dungeon Difficulty. Protected 26 owner-held positive-spawner native IDs and 15 low-looking source families unchanged.


## Later continuation: +4 provisional Tier1 small surface ruins and Apotheosis comparison

Mapped four previously UNRANKED small surface ruin IDs as owner-pending provisional Tier1: `mvs:small_ruin`, `structory:dense_forest_ruin`, `structory:ruin_grassy`, `structory:taiga_ruin_surface`. These have **zero linked spawner/trial indicators in the incomplete source scan**, not proof that there are no spawners or mobs; mark outside DD until inspected. Twenty-six user-held native spawner IDs remain UNRANKED.

Current known-ID catalogue = **758/1240 (61.13%)**; current profile = **758/1130 (67.08%)**, leaving **372** unranked. Compared with preceding 754/1130 (66.73%), this is **+4 IDs, +0.35 pp**. Current authoritative numbers live in `DD_MAPPING_PROGRESS_BASELINE_20261014.json`; prior sections remain historical progress snapshots.

Separate user-requested reference: `AO_APOTHEOSIS_BASE_VS_PR53_RARITY_20261014.md` compares default Apotheosis World Tier affix-rarity weights against AO PR53's validated but **not confirmed deployed** tuning. It does not change affix-item injection chances.


## 14 October — Full FIRST-PASS numeric tier coverage (supersedes historical snapshots above)

**1,240/1,240 known native structure IDs (100%) have an explicit numeric proposed tier; 1,130/1,130 current-profile-relevant IDs (100%) have a numeric proposed tier.** Starting state 869/1240 and 869/1130. Newly proposed **371** numeric tiers; **4** previously tier-conflicted shared IDs tentatively resolved using the highest existing variant tier. New proposal ranges include 107 historical Repurposed Structures IDs **absent from the active modpack**, 87 Pasterdream IDs, current complex dungeon/boss/arena IDs, and all 26 owner-held spawner-positive IDs **whose owner HOLD flag remains set**. Tier mapping **does not mean inspected, owner approved, live-registered, naturally placed, or config-deployed**. No Dungeon Difficulty rules or worldgen modified.

- [Full 1240-ID numeric map](DD_FULL_FIRST_PASS_TIER_MAP_20261014.csv) provides per-ID original tier, new tier, confidence, source status, and deployment = NO.
- [375-item review backlog](DD_FULL_FIRST_PASS_UNVERIFIED_BACKLOG_20261014.csv) keeps all new and variant-conflicted cases for later inspection.
- [Pre-pass original 261-ID active unranked queue](DD_PRE_FULL_PASS_UNRANKED_QUEUE_SNAPSHOT_20261014.csv) is preserved for provenance. The current UNRANKED queue now contains zero entries; **this does not mean zero verification tasks**.
- Full 1,240-ID set is **historical 1,219-ID union + 21 scoped runtime positives**; not an exhaustive live registry enumeration. Some 107 historical IDs are from absent JARs and 3 AO clone IDs remain runtime-unverified. **Do not say 100% of every live structure without enumerating the active registry.**
- Owner holds: **26 native positive-spawner IDs** have guessed numeric tiers solely to satisfy 100% first-pass categorization, but remain **OWNER_HOLD_NO_DEPLOY**. 15 additional source-template family holds are **not registered IDs** and are not artificially added to denominator.
- All previously assigned 865 numeric tiers remain unchanged. No direct runtime evidence of combat and no new DD zone configuration.


## 14 Oct — Functional categories and confidence-ranked first-pass tiers

**Numeric coverage stays 1,240/1,240 (100%)**, but this does **not** imply 1,240 validated/approved tiers. A confidence audit has now separated:

| Provisional confidence | IDs | Interpretation |
|---|---:|---|
| HIGH | **157** | Well-characterized archetype and broad proposed tier, still not runtime/owner approved |
| MEDIUM | **637** | Structure function suggested by family/name or partial source proof; specific combat/difficulty not verified |
| LOW | **420** | Name-only or unknown custom mechanics; no deployment recommendation |
| OWNER_HOLD | **26** | Positive spawner-source indicators; numeric tier placeholder but owner approval mandatory |

Read [complete per-ID category confidence](DD_PROVISIONAL_CATEGORIES_CONFIDENCE_20261014.csv), [157 high-confidence provisional tier shortlist](DD_HIGH_CONFIDENCE_TIER_SHORTLIST_20261014.csv) and [source/definitions](DD_CONFIDENCE_CATEGORIES_SUMMARY_20261014.md). Confidence here means reasonableness of rough archetype placement, not verified natural placement, native hostile mobs, Paxi override compatibility or active DD zone. Original first-pass tiers, owner holds, config and gameplay are unchanged.
