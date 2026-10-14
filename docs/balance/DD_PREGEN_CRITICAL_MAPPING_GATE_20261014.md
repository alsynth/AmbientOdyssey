# PR56 continuation — pregeneration-critical encounter mapping gate (2026-10-14)

Status: **research only**, no structure tier, loot, Dungeon Difficulty config, registry, or worldgen change. Based on PR56 head d228c285 and the 495 unranked current-profile entries in `DD_REMAINING_ACTIVE_UNRANKED_PRIORITY_20261014.csv`.

## Coverage and denominator
- All historical + scoped-client native IDs: **635 / 1240 = 51.21%** provisional working tiers; 605 unranked.
- Current-modpack relevant: **635 / 1130 = 56.19%** provisional working tiers; **495 unranked**.
- Tiers in this research ledger are *not* approved DD rules, and 1130 is *not* a full current runtime registry enumeration.
- 26 owner-held native IDs with positive spawner indicators and 15 additional source-template families remain **UNRANKED**; never tier by automatic family inheritance.
- Historic structure presence, source NBT, client-registration probe, and observed natural generation are different evidence types.

## Minimum gate before freezing Overworld pregeneration
1. Lock the exact PR50-and-later mod JAR roster, datapack/Paxi priority and all structure-set spacing/separation overrides. *Chunky pregen fixes generated terrain and structures; later worldgen changes need fresh chunks.*
2. Check Overworld placement/override for **Dungeon Crawl**, Dungeons & Taverns (especially 9 firewatch-tower variants and 2 remnant graveyards), IDAS pillager camp, Formations Overworld small temple/tower remnant, Graveyard small graveyards, Structory firetower/graveyard and other known combat locations. Source files alone are not generation confirmation.
3. Inspect actual encounter mechanism: source NBT spawner/trial blocks, entity IDs, custom code/spawn rules, and whether DD entity matcher sees native hostile entities. Document one result per *encounter family* before expanding the same outcome to variants.
4. Check structures that have named bosses or scripted fights (e.g. Geburah arena, Mowzie monastery, SkyArena entries) independently of regular DD buffing; boss-tier balance may be external to DD.
5. Regression-test /locate or exploration and pregeneration in a temporary seed before freezing the final Overworld. The PR50 382-name query was a **membership probe**, not natural-generation validation.

## Immediate high-priority 29-ID source audit (not 29 DD rules)
- **3 P0 Nether:** `eternalnether:catacomb`, `eternalnether:citadel`, `eternalnether:piglin_manor`. Check custom `piglin_manor` definition's `eternalnether:citadel` type, actual placement and jigsaw applicability. These are **not necessarily Overworld pregen blockers**; track as Nether freeze gate separately.
- **1 outpost exception:** `ctov:pillager_outpost_mesa`: no linked historical structure set; validate effective CTOV/Paxi placement and registry before extending Tier2 variant policy.
- **23 combat/boss source-review IDs:** `dungeoncrawl:dungeon`; nine `nova_structures:firewatch_tower_*`; `nova_structures:remnant_birch_graveyard`, `nova_structures:remnant_graveyard`; `fdbosses:geburah_arena`; `formationsoverworld:small_temple`, `formationsoverworld:tower_remnant`; `graveyard:small_desert_graveyard`, `graveyard:small_graveyard`; `mowziesmobs:monastery`; `mtr:stronghold`; `skyarena:ice_arena`, `skyarena:sky_arena`; `structory:firetower`, `structory:graveyard`. First consolidate variants into families, then check registered placement and encounters.
- **2 positive source-NBT spawner leads:** `nova_structures:nether_port` (1 block observation), `idas:pillager_camp` (4). Counts are template observations, *not* mobs or verified encounters. Neither belongs to the owner-deferred low-looking list.

## Long-tail backlog and prioritization
- Owner held: **26**, keep out of automated tiers / DD.
- Pasterdream dimension source review: **87**, separate dimension campaign from initial Overworld pregen *only after confirming no cross-dimension placement*.
- Provider-family probe: **115**, batch verify mods/structure sets before individual name ranking.
- Scenery/settlement unverified: **142**, seek real source/placement proof; do not guess Tier0 from peaceful-looking names.
- Unknown no tier evidence: **96**, source/registry needed.

These five lanes plus the 29 immediate IDs add to **495**. None of the 495 can be marked tiered just because this triage exists.

## Next continuation plan
1. Research *Dungeons & Taverns* 11 unmapped high-priority variants as **two families** (firewatch and graveyard), explicitly test whether each contains hostile combat, and record each individual ID separately.
2. Resolve Dungeon Crawl's native `dungeoncrawl:dungeon` ID and effective placement; investigate DD compatibility using the actual enemy roster.
3. Reconcile the 3 Eternal Nether registry definitions and custom type/placement, independent of Overworld.
4. Review IDAS pillager camp + CTOV mesa outpost and the 2 additional static-spawner leads before provisional Tier2+ candidates.
5. Only after encounter/registry evidence, propose reversible individual tiers and update the numeric progress tracker; never count a planned audit as mapped coverage.

**No live runtime, JAR byte inspection, or natural generation test was performed in this continuation.**