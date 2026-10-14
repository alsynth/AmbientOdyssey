# Ambient Odyssey — Structure Catalogue Mapping Progress (14 October 2026)

This is the reproducible **mapping denominator** used in replies. All figures are **known IDs / evidence gathered so far**, not an exhaustive worldgen census.

## Current progress
| Metric | Progress |
|---|---:|
| Known unique native IDs (historical + scoped client query extras) | **1240** |
| IDs with single working numeric tier | **370** |
| IDs with variant-dependent multiple tiers, needing per-site resolution | **4** |
| **Working tier coverage on known IDs** | **374/1240 = 30.16%** |
| **Still without any numeric/variant tier** | **866** |
| Exact-PR50-current-JAR or runtime-registered known IDs | **1130** |
| Working-tier coverage in that relevant subset | **374/1130 = 33.10%** |
| Relevant subset without numeric/variant tiers | **756** |
| Historical IDs belonging to an absent JAR | **107** |
| Historical AO-generated clone records requiring effective datapack check | **3** |
| IDs actually **queried** by PR50 337-client membership test | **382** (all true, but **only scoped queries**) |
| Client-tested IDs shared with historical native list | **361** |
| Client-tested IDs **outside** historical native list | **21** |
| Source NBT template families with **unproven native IDs/placement** | **63**; **not counted** as 63 registered structures |
| Exact native IDs parked **UNRANKED** for owner review | **26** |
| Additional low-looking source families parked **UNRANKED** | **15** |

**What “mapped” means in this table:** an ID has been assigned a *working* tier or has a documented shared-native-ID variant-tier conflict. This is **not** owner approval; most numerical labels come from provisional user catalogue proposals. A strong benchmark requires approved tiers **and** actual natural/worldgen validation; do not confuse that with this planning percentage. `minecraft:end_city` currently has *Tier 2 and Tier 5* variant labels on one registry ID, not a single deployable DD rule.

**Why the baseline may grow:** the **1,219 historic native IDs** are a static scanned subset. PR50's 337 candidate client queried **382 specific IDs**, not the whole runtime registry: **361** occur in the old native set and **21** do not. Discovery of other real native IDs can raise the denominator. Older worldgen features, replacement structures, modded dimension locations, and custom scripted bosses may not be represented even by the known-ID union.

**Progress from this pass:** 21 runtime-positive registered IDs reconciled, including 3 Eternal Nether arenas/catacombs which have PR50 static jigsaw/source graph support but no owner-approved tier and no natural-generation proof. The other 18 already had catalogue site labels, including vanilla and Twilight Forest IDs. **This is reconciliation, not 21 newly finished tiers.** Added candidate associations for a handful of Mowzie/BOMD template families with queried native IDs; association remains unverified for actual reachable templates.

**Priorities:** 
- **Before Chunky pregeneration:** finish active Overworld/Nether structural roster and placement, particularly Create: Structures Arise, Eternal Nether 3, and effective replacement mods; get registered IDs + real natural placement and dimension checks.
- **After/parallel to pregen:** work through 756 unranked known active ID records, filtering decor/settlements by enemy evidence without automatic tiering. Owner-deferred 26 exact native IDs and 15 source families remain untouched.
- **Later balance:** confirm structure/DD eligible mobs, tier owner signoff, native boss mechanics and elite stacking; no blanket DD for all structures.

[Union ledger](DD_KNOWN_NATIVE_ID_MAPPING_LEDGER_20261014.csv) | [21 additional client-verified native IDs](DD_21_PR50_RUNTIME_EXTRA_IDS_20261014.csv) | [source family evidence](DD_UNMAPPED_PROVIDER_ENCOUNTER_FAMILIES_20261014.csv) | [machine-readable metric snapshot](DD_MAPPING_PROGRESS_BASELINE_20261014.json)

**No gameplay files changed.** No Minecraft runtime tests were performed in this catalogue pass; registry-query results are inherited from PR50's previously executed client experiment and not dedicated-server/natural-generation acceptance.

**Variant correction:** Three historical Dungeons Arise identifiers (`heavenly_challenger`, `heavenly_conqueror`, `heavenly_rider`) already had multi-tier labels (`3|6`, `4|6`, `4|6`); harmonized their working state with `minecraft:end_city` as 4 **variant conflicts**. These count as mapped-but-not-resolved working tier variants, not four deployable DD rules. Total 370 numeric + 4 variant = 374 tier-labelled, and 866 unranked.

## Seventh-pass focused worldgen evidence — Eternal Nether 3 locations

The [Eternal Nether source-graph extraction](DD_ETERNAL_NETHER_REGISTERED_WORLDGEN_EVIDENCE_20261014.csv) adds dimension, exact **biome selector**, start pool, jigsaw size, spawn override mobs, source reachable pools/templates and unresolved source refs for the three PR50 client-registry-positive structures. **All 3 remain UNRANKED**.

| Native registered ID | Source templates | Explicit worldgen spawn overrides | Special evidence |
|---|---:|---|---|
| `eternalnether:catacomb` | 19 | `minecraft:magma_cube` | Vanilla wither-skeleton NBT spawner + 3 native configured features |
| `eternalnether:citadel` | 5 | `minecraft:enderman | eternalnether:warped_enderman` | Warped Enderman native feature |
| `eternalnether:piglin_manor` | 2 | `minecraft:piglin | eternalnether:piglin_hunter` | Piglin hunter + additional strider/piglin features; type annotation discrepancy |

**Pre-pregen diagnostic:** Piglin Manor's source definition is stored at registry ID `eternalnether:piglin_manor` but its `type` field is `eternalnether:citadel`. That *might* be an intentionally shared codec/type, or a copy/paste wiring mistake. **Flag for actual worldgen verification**, do not assume it fails and do not silently correct it. Prior PR50 natural probes didn't encounter all 3, and broad Nether `/locate` could stall server ticks; prefer bounded exploration/worldgen checks.

**Confidence:** structural source graph checked; in-game registration checked in a scoped PR50 client query; natural generation **not** demonstrated; no DD/boss settings touched; DD itself may not cover modded feature-generated mobs.
