# Ambient Odyssey — Structure Catalogue Mapping Progress (14 October 2026)

This is the reproducible **mapping denominator** used in replies. All figures are **known IDs / evidence gathered so far**, not an exhaustive worldgen census.

## Current progress
| Metric | Progress |
|---|---:|
| Known unique native IDs (historical + scoped client query extras) | **1240** |
| IDs with single working numeric tier | **370** |
| IDs with variant-dependent multiple tiers, needing per-site resolution | **1** |
| **Working tier coverage on known IDs** | **371/1240 = 29.92%** |
| **Still without any numeric/variant tier** | **866** |
| Exact-PR50-current-JAR or runtime-registered known IDs | **1130** |
| Working-tier coverage in that relevant subset | **371/1130 = 32.83%** |
| Relevant subset without numeric/variant tiers | **759** |
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
- **After/parallel to pregen:** work through 759 unranked known active ID records, filtering decor/settlements by enemy evidence without automatic tiering. Owner-deferred 26 exact native IDs and 15 source families remain untouched.
- **Later balance:** confirm structure/DD eligible mobs, tier owner signoff, native boss mechanics and elite stacking; no blanket DD for all structures.

[Union ledger](DD_KNOWN_NATIVE_ID_MAPPING_LEDGER_20261014.csv) | [21 additional client-verified native IDs](DD_21_PR50_RUNTIME_EXTRA_IDS_20261014.csv) | [source family evidence](DD_UNMAPPED_PROVIDER_ENCOUNTER_FAMILIES_20261014.csv) | [machine-readable metric snapshot](DD_MAPPING_PROGRESS_BASELINE_20261014.json)

**No gameplay files changed.** No Minecraft runtime tests were performed in this catalogue pass; registry-query results are inherited from PR50's previously executed client experiment and not dedicated-server/natural-generation acceptance.
