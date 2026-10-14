# PR #56 — Post-100%-mapping critical audit (14 October 2026)

**Status:** research / planning, draft only. The earlier milestone is **100% numeric first-pass of the _known_ 1,240-ID union**, not 100% registry discovery, accurate encounter tiers, approval, or applied DD behavior. This document begins the owner's requested *details-after-100%-mapping* phase.

## Consistency checkpoint — completed using PR #56 current CSV files

| Checked property | Observed | Interpretation |
|---|---:|---|
| Unique first-pass native-ID rows | 1,240 | 1,219 historical IDs + 21 positive scoped-client extras |
| Current roster / scoped-client-relevant known IDs | 1,130 | Historical absence accounts for 107, plus 3 unverified AO-generated clones |
| First-pass numeric tiers | 1,240 | No unassigned numeric **draft** tiers |
| Exact tier mismatches between tier-map and confidence-category exports | **0** | The two catalogue views agree |
| HIGH / MEDIUM / LOW / OWNER_HOLD tier-confidence IDs | 157 / 637 / 420 / 26 | Confidence in archetype, not active mobs/difficulty |
| New draft entries / shared-ID conflict cases | 371 / 4 | 375 review backlog records |
| Owner-held spawner-positive **exact native IDs** | **26** | Have numeric first-pass placeholders but retain **NO-DEPLOY** protection |
| Source-family-only owner holds | 15 | **Not** verified native IDs or part of 1,240-ID total |
| Rows currently authorized for live Dungeon Difficulty deployment | **0** | All 1,240 tier-map `eligible_for_live_DD` values are `NO` |
| Native natural-generation/actual hostile encounter verification | **not established** | Static catalogue and scoped registry hits cannot substitute |

The **337-client profile's 382 positive registration probes are a scoped sample, not full enumeration of the 1,130 or all possible current live IDs**. A true 100% registered structure census, effective Paxi stack and generated encounter census are still outstanding.

## New actionable postmap artifact

[**34 exact-ID critical review rows**](DD_POSTMAP_CRITICAL_34_TIER_REVIEW_20261014.csv) replace the vague "all unranked" priority framing after the first-pass placeholder assignment. They have:
- Exact ID, current numeric *draft* tier, confidence and current client-registry status;
- Existing source evidence (distinguishing raw template spawners from generated enemy encounters);
- Decisive missing question and specific next verification;
- An explicit `live_DD_allowed=NO` and tier-change/hold action.

**Wave partition:** 1 owner tier-policy conflict, 4 native-ID variant conflicts, 3 Eternal Nether worldgen checks, 1 outpost structure-set question, 4 boss/native-scaling checks and 21 potential combat/encounter checks = **34**. The 29 originally identified urgent sites are still covered **29/29**; the additional five are the four shared-ID conflicts plus the Hydra plan discrepancy. These 34 are *audit targets*, not proposed DD rules.

## Specific contradictions and decisions to resolve

1. **Twilight Hydra:** `twilightforest:hydra_lair` inherited historical **Tier 4**, while the owner's later combat/boss plan explicitly places **Twilight Hydra at Tier 7**. This is a concrete **catalogue-vs-boss-policy mismatch**, not proof the structure must receive a generic DD Tier7 rule. Confirm boss-to-structure relationship and correct the *catalogue planning reference* once reconciled; use boss-native tuning for the fight.
2. **Shared-ID Heavenly trio:** `dungeons_arise:heavenly_challenger` prior variants Tier3|6, `heavenly_conqueror` Tier4|6, `heavenly_rider` Tier4|6. Each currently shows **draft Tier6** only because the previous first pass chose the higher variant. One registered ID cannot independently encode the two variants' separate difficulties in a simple structure-name matcher. Identify the actual variant selectors/NBT or keep this as an unresolved single-ID limitation.
3. **End City:** `minecraft:end_city` carries prior Tier2|5 variants but currently displays a single **draft Tier5** for the same reason. Do not deploy a blanket Tier5 zone based on this placeholder.
4. **Eternal Nether:** `eternalnether:catacomb` T4, `citadel` T4, `piglin_manor` T3 are all **new draft proposals**, despite some source-jigsaw graph evidence. `piglin_manor`'s source uses definition type `eternalnether:citadel`; the relationship is not yet explained, and none was observed naturally generated in the prior scoped Nether test. This is a **Nether** worldgen gate, not evidence to delay Overworld Chunky solely for Nether structures.
5. **CTOV Mesa:** `ctov:pillager_outpost_mesa` now displays draft Tier2 even though the original source scan did **not** establish its effective registered structure set. Structure-set and Paxi override need checking before this can be considered an active outpost.
6. **Minor graveyard/temple landmarks:** They carry unapproved low numeric guesses, not a conclusion that they should become hostile DD zones. If a low-looking site is source-spawner positive during detailed review, leave its actual classification for the owner and apply the same non-deploy hold policy.

## Separate worldgen vs combat gates

- **Before committing to very large Overworld pregen:** freeze the intended Overworld structure-provider JARs and datapacks, verify effective Paxi overrides and placement/spacing for critical Overworld families, then do a bounded seed generation test. Structure *tier* guessing is not a replacement for generation checks.
- **Before Nether pregen:** resolve Eternal Nether native types/jigsaw reachability and natural generation in the Nether. Pasterdream source structures live in another research lane and are not an automatic Overworld block.
- **Before Dungeon Difficulty v4 candidate:** verify actual hostile entities, vanilla ID regex/matcher compatibility, trial-spawner or native boss mechanics and elite double-stacking. Keep Tier0–1 out of DD by policy, and do not assume every Tier2–6 structure merits a zone.
- **Before any production tier import:** require explicit owner approval for previously heuristic assignments; do not import 26 protected numeric placeholders, 107 Repurposed historical IDs absent from the active roster, three unverified generated clones, or unresolved shared-ID tier guesses.

## Limits of this continuation

This is a **static consistency and prioritization audit** of already committed catalogue, pregen and owner-policy evidence, not fresh native JAR inspection, full registry enumeration, a natural generation test, actual hostile-mob observation, or a runtime performance benchmark. No mod roster, loot tables, Dungeon Difficulty JSON, structure/biome placement, boss mechanics, or world files were changed. Keep this PR **draft** and do not merge for gameplay use.

## Cross-references

- [Complete first-pass map](DD_FULL_FIRST_PASS_TIER_MAP_20261014.csv)
- [375-item unresolved/first-pass review backlog](DD_FULL_FIRST_PASS_UNVERIFIED_BACKLOG_20261014.csv)
- [Confidence category audit](DD_CONFIDENCE_CATEGORIES_SUMMARY_20261014.md)
- [Earlier 29 high-priority site verification protocol](DD_29_SITE_ENCOUNTER_VERIFICATION_PLAN_20261014.md)
- [Eternal Nether source-graph evidence](DD_ETERNAL_NETHER_REGISTERED_WORLDGEN_EVIDENCE_20261014.csv)
- [26 owner-held native ID records](DD_OWNER_UNRANKED_SPAWNER_REVIEW_20261014.csv)
