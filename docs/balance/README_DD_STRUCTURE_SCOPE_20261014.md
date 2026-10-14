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

## Current DD configuration — direct 53-zone triage (14 Oct)

[Exact existing rule triage](DD_EXISTING_ZONE_TRIAGE_20261014.csv) compares every `zone_matches.structure` in the **PR #45 candidate** against the user-approved T0–1 exclusion. **No DD config edits have been made.**

| Config tier | Current zones | Next v4 handling |
|---|---:|---|
| 0 | 6 | Remove redundant no-op zones |
| 1 | 19 | Remove redundant no-op zones |
| 2 | 7 | Retain *only* on proven combat sites |
| 3 | 10 | Prove combat eligibility / no native double-scaling |
| 4 | 7 | Same; inspect trial/spawner/native effects |
| 5 | 2 | Same; test elites first |
| 6 | 2 | Same; test elites first |

**25 of 53 current DD zone mappings are Tier 0 or 1 and have no entity-attribute effects.** They can be **omitted from a future v4 candidate** without changing the combat-buff intent; leave the actual PR #45/PR #50 config untouched until its own regression/rollback checks pass. There are currently **28 Tier 2–6 attribute-buff rules**, not 53 hard combat rules. One of the T1 legacy site IDs is `dungeons_arise:small_blimp`, previously disabled from natural generation; removing a no-op rule does not re-enable the structure.

When implementing v4, preserve the same qualified T2–6 whitelist and ensure no removed T0–1 record was previously used for an unintended location fallback. Do not treat the arithmetic reduction as gameplay-runtime verification.

## Second catalogue pass — direct template indicator audit (14 Oct)

**Source evidence added, NOT Minecraft runtime validation.** Joined the 1,219-row native-ID scope ledger with PR45's **2,805 NBT indicator template rows** and 130 `ENCOUNTER_CONTROL_GAPS` rows (28 selected pilots + 102 held), without modifying native resource files. `ENCOUNTER_NBT.csv` is an **indicator-only census**, not a list of all structure templates. A missing record can mean *not scanned / no indicator / native code-based spawn*, never evidence of no combat.

### New files
- [NBT joined native-ID scope ledger](DD_NATIVE_NBT_EVIDENCE_20261014.csv): 1,219 rows with resource-path association and sample template; zero DD config modifications.
- [Prioritized linked structure review](DD_NBT_COMBAT_REVIEW_QUEUE_20261014.csv): 70 records with positive NBT spawner/trial indicators. Based on names/path heuristics only, not actual reachable game assembly.
- [All PR45 held encounter candidates](DD_HELD_ENCOUNTER_EVIDENCE_20261014.csv): 102 held review records; 24 have traced NBT spawner/trial markers, **not necessarily DD-compatible vanilla entities**.

### Quantified findings
- 121 structure IDs have at least one path-associated NBT indicator template; 70 have NBT mob spawner or trial spawner blocks. *Templates may repeat across versioned folders and may not be reachable; counts must not be interpreted as spawned enemies.*
- **8 formerly name-screened low-priority exploration structures have template spawner/trial evidence** and are now flagged for an encounter review. This is a **review upgrade**, **not a tier assignment**.
- 18 previously uncertain/unmapped IDs show similar positive indicators.
- 2 T0–1 structures have templates with spawners. They remain **excluded from DD** by owner policy, but should not be described as purely peaceful.
- 42 already mapped T2–6 IDs have path-associated template encounter evidence. These are not automatically eligible for DD attribute buffs, since modded mobs, projectile damage, and special scripts often bypass its vanilla allowlist.

**Highest-priority additions from low-priority or unknown scope:**

| Native structure | Template spawners | Trial spawners | Association |
|---|---:|---:|---|
| `mns:large_house_1` | 21 | 0 | source_nbt_path_correspondence |
| `mss:red_sand` | 20 | 0 | source_nbt_path_correspondence |
| `idas:collectors_museum` | 18 | 0 | source_nbt_path_correspondence |
| `mss:taiga` | 18 | 0 | source_nbt_path_correspondence |
| `idas:tinkers_workshop` | 10 | 0 | source_nbt_path_correspondence |
| `mns:medium_house` | 8 | 0 | prefix_template_path_candidate |
| `mss:small_deepslate_house` | 8 | 0 | source_nbt_path_correspondence |
| `mvs:prismarine_house_1` | 8 | 0 | source_nbt_path_correspondence |
| `mss:jungle` | 8 | 0 | source_nbt_path_correspondence |
| `mss:muddy_water_hole` | 7 | 0 | source_nbt_path_correspondence |
| `idas:abandonedhouse` | 6 | 0 | source_nbt_path_correspondence |
| `mss:leaf_hollow` | 6 | 0 | prefix_template_path_candidate |
| `mss:mangrove` | 6 | 0 | source_nbt_path_correspondence |
| `mss:mushroom` | 6 | 0 | source_nbt_path_correspondence |

**Important limitations and guards**:
1. Resource joining is **conservative and limited** to Moog's Voyager/Nether/End/Soaring, IDAS, Dungeons & Taverns and Pasterdream, with exact filename/namespace/path conventions; native provider name collisions, replaced templates and code-spawned entities remain unresolved. For conflicting prefixes (e.g. `mega_ship` vs `mega_ship_crashed` or `medium_house` vs `medium_house_2`), longer matching ID wins; ambiguous associations are marked and excluded from counted evidence.
2. Template `equipped_mob_or_spawner_indicators` can be **ordinary equipment marker strings**, not proof an enemy actually spawns. **Positive mob-spawner/trial-spawner block counts** are stronger evidence, but no active encounter claim.
3. CTOV and Towns & Towers cannot be certified peaceful by a lack of NBT spawners; outposts commonly rely on jigsaw pools or mod mob-spawn mechanics. Reconcile the actual effective start pools and code.
4. Sky/Ice Arena, Pasterdream, Cataclysm and some boss structures have scripted or native mob spawning: no NBT indicator may exist even if an encounter is dangerous.
5. Exact installed PR50 roster still requires dedicated-server and enabled-datapack verification before making changes.
6. The existing 25 Tier 0–1 DD no-op zone entries can be removed in a *future* v4 candidate; this source pass leaves current PR45/50 configs untouched.

**Next work:** manually map the 26 upgraded/newly evidenced candidate IDs to native entity IDs, identify modded IDs unavailable in the PR50 registry, validate whether each template is reachable from the structure's actual pool, and split DD-compatible vanilla enemies from native-special mobs. Continue with the 24 existing held PR45 structures that contain spawner/trial evidence and test elite stacking before any config rollout.

## Third catalogue pass — owner override: leave low-looking spawner sites UNRANKED (14 Oct)

**Owner instruction:** Any structure that *appears* Tier 0–1 but has spawner evidence must remain **unranked for manual inspection later**. Do **not** auto-promote to Tier 2. User review is not a prerequisite for finishing other DD research. This policy supersedes **working tier labels**, while historical catalogue/crosswalk tier fields are retained *only as provenance*.

### Effective working-tier results
- **26 structures** were placed in the dedicated [owner-deferred, unranked list](DD_OWNER_UNRANKED_SPAWNER_REVIEW_20261014.csv): 10 originally low-tier/low-priority name candidates plus 16 other small/exploration-looking unmapped examples with static spawner evidence. No new tier numbers assigned.
- In particular, **`mns:giant_skull`** and **`mss:nether_portal`** were provisionally Tier 1 in the historical source but **are now `UNRANKED` in the working overlay**. Keep original “1” in `historical_tier` for traceability only; do not let a future DD script read the old value as an approved Tier 1 assignment.
- The other 2 previously unmapped obvious combat candidates (`idas:pillager_camp`, `nova_structures:nether_port`) also remain **unranked**, but belong to the *combat-tier review* lane rather than the low-looking/decorative owner list.
- Working tier/status/action now appear in [updated all-native ledger](DD_NATIVE_NBT_EVIDENCE_20261014.csv) for **all 1,219 native IDs**. The effective tier field is `dd_working_tier`: it takes precedence over the archived `historical_tier` for this research branch.
- [Updated 70-evidence queue](DD_NBT_COMBAT_REVIEW_QUEUE_20261014.csv) now carries `dd_working_tier` and `dd_disposition` so owner-deferred structures cannot accidentally become implementation targets.

### Static mob identity refinement on the 70-evidence queue

| Static NBT entity evidence class | Structures |
|---|---:|
| Contains listed vanilla-hostile entity ID | 30 |
| No vanilla-hostile ID but has modded entity ID | 2 |
| No decoded mob/entity ID despite spawner/trial block | 37 |
| Only non-hostile or projectile-like decoded IDs | 1 |

The list of known vanilla-hostile names is a **triage heuristic**, not a new DD allowlist or a runtime spawn validation. Non-vanilla entities may be perfectly valid but need specific mod/entity integration. Generic spawner-block presence is *not* evidence of an ordinary compatible enemy.

[102 held encounter source records](DD_HELD_ENCOUNTER_EVIDENCE_20261014.csv) additionally contain separated vanilla-hostile vs modded entity leads, preserving the original hold reasons and lack of runtime acceptance. The 24 source-spawner/trial-positive held cases remain **held**, not newly DD-enabled.

### Production protection
- **No changes to `AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv`**, the immutable historical/source ranking document, or to `difficulty_v2.json`. Override is explicit in the new working layer, so provenance remains auditable and any future integration must consume `dd_working_tier` instead of archived `historical_tier`.
- **No Tier 2 assignment or DD balance change** for owner-deferred sites; do not infer challenge from spawner-block quantity, which can include alternative/unreachable templates and version duplicates.
- Do not block Chunky pregeneration on future owner review of these *tiers* unless a separate actual worldgen/structure generation fault is proven. Boss arenas/structure worldgen freeze remains independent.

**Next productive catalogue phase (without owner input):** evidence-check the clearly combat-oriented held T2–6 structures, fix stale native mob IDs, verify actual template-pool reachability, and test DD native elite/mob scaling safely; user-deferred 26-site list should simply remain parked.
