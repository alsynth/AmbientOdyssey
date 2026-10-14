# Dungeon Difficulty — native structure scope screen (14 Oct 2026)

**New catalogue screening, not gameplay changes.** Derived from PR #45 source `docs/balance/AO_HISTORICAL_STRUCTURE_REGISTRY_CROSSWALK_2026-10-13.csv`, PR #45 tier catalogue, and the **338-reference PR #50** reconciled import's `FULL_IMPORT_INPUTS.json` (`1cebd86eefe71dd365a991909962e5aed26b7c1c`). The historical crosswalk predates PR #50 and is not a registry/live encounter census.

## What changed

- [Full native ID screen](DD_NATIVE_STRUCTURE_SCOPE_20261014.csv): **1219 historical native structure ID records**, individually flagged as present/absent by **exact mod-JAR filename** in PR #50, with existing catalogue tier, family, low-priority/combat review screening and safe next action. **Never treat a name-based guess as a verified tier or peaceful structure.**
- [Provider work queue](DD_PROVIDER_SCOPE_SUMMARY_20261014.csv): **65 historical source-provider groups** ranked by historical ID count and scope.
- [High-volume families](DD_HIGH_VOLUME_FAMILY_SCREEN_20261014.csv): **107 per-family/priority groupings** of 8 historical providers that contain at least 50 IDs, so repeated structures are handled as types.

The PR #45 tier catalogue has **427 rows**, but **41 are placeholder/family rows** rather than independent active sites. Of the 1219 historical native IDs, **361** had direct catalogue matches and **858** did not. **Unmapped is NOT Tier 0** and **historical tier is NOT an instruction to deploy DD**.

### Triage buckets (all historical IDs)

| Category | IDs | Interpretation |
|---|---:|---|
| JAR absent from PR #50 roster | 107 | No DD configuration; do not re-add missing mods merely to fill the catalogue |
| Historical Tier 0–1 | 50 | Explicit DD exclusion under owner's Tier 0–1 policy |
| Historical Tier 2–6 | 295 | Inspect actual combat sources, installed resources and DD compatibility before adding rules |
| Historical Tier 7–9 | 13 | Prefer native boss and arena controls |
| Mixed-tier same ID | 0 | Resolve variant/dimension first |
| Unmapped; low-priority exploration *candidate* | 389 | No DD by default; reassess if spawned hostile encounters are proven |
| Unmapped; plausible combat archetype | 72 | Inspect hostile encounters, exact structure registration and tier |
| Unmapped; unclassified | 290 | Cannot safely exclude or add DD without source evidence |
| AO-generated historical clone | 3 | Verify generated datapack and current active ID first |

Totals above represent **historical native IDs**, not unique balance jobs and not proof of natural generation.

## High-volume source audit

| Historic provider JAR | IDs | PR #50 exact JAR | Matched T0–1 | Matched T2–6 | Matched T7+ | Unmapped low-priority | Unmapped combat review | Unmapped unknown |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| MoogsVoyagerStructures-universal-1.21-5.1.3.jar | 130 | Yes | 4 | 10 | 0 | 101 | 1 | 14 |
| pasterdream-0.9.6.jar | 115 | Yes | 3 | 25 | 0 | 63 | 0 | 24 |
| repurposed_structures-7.5.22+1.21.1-neoforge.jar | 107 | No | 0 | 0 | 0 | 0 | 0 | 0 |
| dungeons-and-taverns-v4.4.4 [NeoForge].jar | 96 | Yes | 2 | 33 | 0 | 28 | 15 | 18 |
| idas-1.13.7+1.21.1-neoforge.jar | 84 | Yes | 1 | 24 | 0 | 13 | 1 | 45 |
| [Neoforge]ctov-3.6.3.jar | 78 | Yes | 0 | 0 | 0 | 66 | 12 | 0 |
| t_and_t-fabric-neoforge-1.13.11.jar | 60 | Yes | 0 | 0 | 0 | 29 | 31 | 0 |
| MoogsNetherStructures-universal-1.21-3.1.1.jar | 52 | Yes | 1 | 13 | 0 | 14 | 0 | 24 |

**Specific findings:**
- **Repurposed Structures (107 IDs)**: its historic binary **does not appear** in the PR #50 full-import roster. Consequently, all these IDs are *out of active DD scope*. If it is reintroduced later, its bastion, ancient-city, fortress, monument, mansion, stronghold and outpost variants must be reassessed as possible combat archetypes—not labelled T0/T1 by default.
- **Moog's Voyager (130)**: broad scenery/house/well/log/tree families screen as *low-priority*, but mapped tiers and hostile-named ruins/towers remain on the review list. A large mod can therefore have relatively few DD targets.
- **Pasterdream (115)**: many suffix variants are scenery/parts, but preserve its shadow dungeons, towers, arena portals and other mapped fights. Also verify each site’s actual Pasterdream-dimension placement before writing a DD rule.
- **CTOV (78)** and **Towns & Towers (60)**: primarily village variants; pillager outposts are **combat-review**, *not* automatically exempt. Check if structure placement is a true separate native ID vs replacement routing; never create a wildcard for every village.
- **Dungeons & Taverns (96)** and **IDAS (84)** still have substantial potentially meaningful combat content. Do not filter them out just because they also add numerous cosmetic structures.

## Operational filter and next steps

1. **Tier 0–1: zero DD rules** by user choice. For unmapped village/scenery IDs, default to *no DD rule until hostile evidence exists*, but keep tier **unknown**, not 0.
2. **Tier 2: DD only for substantial combat**, not a tower/building that merely houses ordinary passive mobs.
3. **Tier 3–6: prioritize real combat dungeons** and compare exact active resources, encounter NBT and installed JARs before promoting any held rules. The existing PR #45 **28-attribute / 25-natural / 374-held** state is unchanged.
4. **Tier 7–9: boss or native arena configs**, not bulk DD multipliers. Do not double-stack the Sky/Ice Arena wave scaler or Apotheosis/Brutal elites.
5. For high-volume providers, review one **native family** at a time rather than manually balancing every biome/visual variation. `native_family` is a work-queue grouping **only**; it does not mean DD accepts a family key or wildcard.
6. Next evidence pass should start with **CTOV/Towns & Towers pillager outposts**, **unmapped Moog hostile towers**, **Repurposed only if re-added**, and **the high-tier mapped D&T/IDAS/Pasterdream encounters**. Prefer a generated evidence ledger showing exact spawner/inline mob/trial/boss configuration instead of name inference.
7. Before production, compare actual effective resource providers, loaded datapacks, natural generation, elite modifiers and current dedicated-server roster. PR #50 filename match is **not** that test.

**Worldgen freeze policy:** This catalogue update changes no mod roster, placement, biome eligibility, templates, loot, entity stats or generated chunks. DD screening does **not** block pregeneration after the actual structure/arena and terrain generation freeze is accepted.
