# PR56 — effective encounter verification sequence (14 Oct 2026)

Planning/test protocol for **29 outstanding high-priority IDs** in `DD_PREGEN_FAMILY_EVIDENCE_MATRIX_20261014.csv` and `DD_PREGEN_REMAINING_HIGH_PRIORITY_MATRIX_20261014.csv`. This does not claim live testing or assign tiers.

## Phase A — resolve one representative from each encounter family
| Order | Representative | Why first | Required evidence / stop condition |
|---|---|---|---|
| A1 | `dungeoncrawl:dungeon` | Core RPG dungeon and candidate DD target | Effective structure registration/placement; actual generated rooms; spawner block entity IDs and equipped combatants |
| A2 | `nova_structures:firewatch_tower_forest` | 9-variant family; basic vanilla forest selector | Active Paxi override and structure set; reachability; natural / generated mobs; no family inheritance until differences reviewed |
| A3 | `nova_structures:remnant_graveyard` | 2-variant remnant group | Determine if hostile combat exists at all; defer if small low-looking structure has spawner |
| A4 | `idas:pillager_camp` | Four source spawner block observations | Verify source ID and actual hostile spawns; assess DD matcher for pillagers; no blanket promotion from NBT |
| A5 | `ctov:pillager_outpost_mesa` | Sole 42-outpost-proposal exception | Reconcile historical missing structure-set association with effective Paxi and registered set before Tier2 proposal |
| A6 | `fdbosses:geburah_arena` | Registered boss arena; native boss logic | Detect summoned/boss entities; check if adding DD would double-stack boss modifiers; boss-tier policy belongs to boss balancing |
| A7 | `skyarena:sky_arena` | Registered separate arena family | Check natural placement and spawned entities, then ice variant separately |
| A8 | `eternalnether:piglin_manor` | Registration yes but custom definition type equals citadel | Prove actual Nether natural placement and why shared `eternalnether:citadel` type is used; do not infer a bug or fix |
| A9 | `eternalnether:catacomb` | Reachable 13-pool /19-template graph, with hostile IDs | Check real Nether assembly, special spawns, and features; then compare citadel |

## Phase B — 20 remaining ID-specific checks
- Firewatch variant IDs: birch, cherry, dark_oak, jungle, mangrove, savanna, swamp, taiga (8). Look for differences in structure set, biomes, templates, NPC spawns; representative test cannot prove all.
- `nova_structures:remnant_birch_graveyard` (1); keep low-looking spawner protection.
- `eternalnether:citadel` (1), `skyarena:ice_arena` (1).
- `formationsoverworld:small_temple`, `formationsoverworld:tower_remnant` (2).
- `graveyard:small_desert_graveyard`, `graveyard:small_graveyard` (2), hold owner review if low-looking + spawner.
- `mowziesmobs:monastery`, `mtr:stronghold` (2), investigate native boss scripts before DD.
- `structory:firetower`, `structory:graveyard` (2), examine ambient-only vs hostile.
- `nova_structures:nether_port` (1), known source spawner lead.

## Compact evidence record per structure
Record: exact installed mod filename/hash; effective structure JSON or registered type; effective structure-set key with Paxi precedence; dimension and biome selector; natural placement observation (seed and coordinates); /place reproduction separately; native NBT ordinary spawner IDs; trial/script/spawn overrides; any hostile attitude check; whether existing Tier2–6 DD regex matches; owner-approved tier (if any); result for modded boss scaling; whether it blocks **Overworld** or **Nether** pregeneration. Mark each signal `YES`, `NO`, or `UNKNOWN`, not assumed.

## Scope and progression
- First freeze final **Overworld** JARs/datapacks/spacing before large Chunky pregen. Nether Eternal Nether and Pasterdream dedicated-dimension work should remain separate unless cross-dimension placement is verified.
- Do **not** run huge radius /locate scans on the live multiplayer server; use temporary seed and bounded /place/seed checks.
- Trial spawner and scripted boss mob rules must not be treated as ordinary mob attribute scaling. Existing DD tier matcher is not a universal solution for modded entities.
- 26 native owner-deferred structures plus 15 unranked source family leads are protected. Never assign them automatically.
- User's relic/Gnat exclusions are independently recorded in `AO_CONTENT_EXCLUSIONS_REQUEST_20261014.md`.

**Catalogue numbers unchanged until actual new working-tier decisions or registry discoveries:** current profile 635/1130 (56.19%) labelled; 495 not ranked; total known 635/1240 (51.21%) labelled. Full census and runtime confirmation outstanding.
