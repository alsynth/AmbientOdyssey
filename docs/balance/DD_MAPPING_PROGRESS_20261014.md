# Ambient Odyssey — Structure Catalogue Progress (October 14, 2026)

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
