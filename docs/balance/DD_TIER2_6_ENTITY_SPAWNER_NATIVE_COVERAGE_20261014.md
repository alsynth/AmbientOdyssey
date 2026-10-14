# PR56 — Tier 2–6 Dungeon Difficulty source-encounter audit (14 Oct 2026)

> **LATEST pinned-source result:** A bounded streaming NBT reader now successfully scans Keep Kayra’s large templates and detects **9 ordinary source spawners** plus **the exact slime → creeper passenger combination** reported by the owner. The full read-only scan covers **78 spawner-block occurrences in alternative NBT templates across 10 structure IDs** (Dungeons Arise **54**, IDAS **24**) and yields **7/28** candidate DD Tier 2–6 zones with positive pinned-native encounter evidence. This is **not** an in-game spawn count or proof of DD application. [Machine-readable report](DD_PINNED_NATIVE_TEMPLATE_SPAWNER_AUDIT_20261014.json).

**Decision: DO NOT DEPLOY or widen the vanilla-only DD matcher yet.** This is a read-only native source inspection, not proof that a mob spawns, that DD applies at runtime, that an Apotheosis invader would not be double-stacked, or that alternate jigsaw pieces are reachable/selected naturally. The target is to verify *actual* coverage before buffing content.

## Existing candidate consistency — all static checks passed

| Metric | Source-checked result |
|---|---:|
| Existing DD candidate zones | **53** |
| T0–1 unbuffed/no entity attributes | **25** |
| T2–6 attribute candidate zones | **28** |
| Candidate zone vs PR56 first-pass tier mismatches | **0** |
| Tier0 owner-approved (26) structures incorrectly given active T2+ DD | **0** |
| Exact vanilla entity types in candidate matcher | **17** |
| Old historical linked-positive NBT evidence among the 28 | **0 of 28** |
| **New** targeted pinned-JAR template scan positive in scaled candidate | **7 of 28** (all seven candidate Dungeons Arise structures scanned) |
| Candidate changes to vanilla spawner spawn count/delay/range | **0** — the candidate entity-rule's `spawners` multipliers are all zero |
| Gameplay configurations actually installed from PR56 | **0** |

The old ledger's 0/28 was an **evidence gap, not a count of mob-free dungeons**. New native positive findings supersede that negative screen. Direct sources: [53-zone coverage script](../../tools/audit_pr56_dd_zone_coverage.py), [new pinned source 10-site evidence](DD_PINNED_NATIVE_TEMPLATE_SPAWNER_AUDIT_20261014.json), candidate `experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json`. The evidence is built from the exact PR50-pinned NeoForge Dungeons Arise v2.1.68 and IDAS v1.13.7 JARs, SHA-1-verified by CI.

## Keep Kayra — native mounted encounters verified

From the exact pinned Dungeons Arise JAR, the Keep Kayra start-pool graph reaches **10 NBT templates containing nine ordinary spawner block occurrences**, with **skeleton**, **slime** and **wither skeleton** as primary spawner entities. The source graph has no identified missing resources under the updated bounded scanner.

The scanner follows SpawnData.entity.Passengers, SpawnPotentials entity payloads, nested passengers, and prebuilt entity passengers without misidentifying equipment/item IDs as mobs.

**Exact source location:** `dungeons_arise:keep_kayra/keep_kayra_spawner_3` (`data/dungeons_arise/structure/keep_kayra/keep_kayra_spawner_3.nbt`) contains the slime vehicle with a creeper passenger. The reference was traced from the pinned v2.1.68 native start-pool graph, not inferred from an image or a structure name. See [the retained per-template evidence](DD_PINNED_NATIVE_TEMPLATE_SPAWNER_AUDIT_20261014.json).

| Vehicle | Passenger | Recommended treatment |
|---|---|---|
| Slime | Creeper | **User-observed combination verified in source. Preserve without specially buffing either half.** |
| Skeleton | Potion entity | Projectile/effect, not a hostile-mob DD attribute target |
| Wither Skeleton | Potion entity | Same; preserve the scripted pairing |

The candidate vanilla DD type filter covers skeleton and wither skeleton, **but excludes both slime and creeper**, so the slime/creeper pair is outside this generic entity-type rule. Other game systems may affect them, and runtime behavior has not been tested.

The owner also remembers zombies in Keep Kayra. Zombies are not among the primary IDs in the nine linked spawners inspected here, but may occur through other spawn sources. Do **not** conclude there are no zombies.

**Balancing preference:** Prioritize ordinary vanilla hostiles that define each dungeon. Quark and Alex's Mobs appear only as incidental enemies in current planning and do **not** merit special DD tuning by default. Preserve mounted encounters, boss-specific mechanics, and Apotheosis modifier interactions until a targeted runtime check.
## Seven candidate Dungeons Arise sites — spawners in scanned source NBT templates

| ID | Planned tier | Distinct jigsaw templates inspected | Ordinary spawner **block occurrences** | Pool/NER scan status |
|---|---:|---:|---:|---|
| `dungeons_arise:bandit_towers` | 2 | 26 | **10** | Native graph traversed without identified errors |
| `dungeons_arise:illager_fort` | 3 | 21 | **4** | Native graph traversed without identified errors |
| `dungeons_arise:plague_asylum` | 3 | 33 | **6** | Native graph traversed without identified errors |
| `dungeons_arise:foundry` | 5 | 45 | **8** | **Partial**: jigsaw reference to a missing or externally supplied `foundry_corridor_gears` pool |
| `dungeons_arise:mechanical_nest` | 5 | 162 | **12** | **Partial**: missing native child-pool and template references |
| `dungeons_arise:keep_kayra` | 6 | 10 | **9** | Source graph traversed using bounded two-pass NBT parsing; mount pairs verified |
| `dungeons_arise:aviary` (End) | 6 | 32 | **5** | Native graph traversed without identified errors |

**Dungeons Arise subtotal: 54 spawner-block occurrences across different source templates**, NOT 54 spawners inside one generated dungeon. Multiple templates can be alternatives, omitted, rotated or instantiated with different pool weights. No trial-spawner blocks were found in the successfully parsed selected templates, but this says **nothing** about unscanned pieces, scripts, later dynamic placements or custom trial mechanics.

### Exact-type DD coverage gap

These are **spawner entity IDs in successfully parsed source NBT**. Type-only regex matches are NOT runtime DD application proof; each entity's `HOSTILE` attitude, block-spawner NBT interpretation and elite modifiers still need verification.

| Source site | IDs covered by DD filter | Not covered by filter |
|---|---|---|
| Bandit Towers | `minecraft:pillager`, `minecraft:skeleton` | `minecraft:firework_rocket` (non-mob entity type) |
| Illager Fort | `minecraft:cave_spider` | None in parsed source |
| Plague Asylum | `minecraft:husk`, `minecraft:skeleton`, `minecraft:witch`, `minecraft:wither_skeleton` | `minecraft:evoker_fangs` (effect entity type) |
| Foundry | `minecraft:blaze`, `minecraft:piglin_brute`, `minecraft:wither_skeleton` | `minecraft:hoglin`, `minecraft:magma_cube`, `minecraft:phantom` |
| Mechanical Nest | `minecraft:skeleton`, `minecraft:wither_skeleton`, `minecraft:zombie` | `minecraft:ravager`, `minecraft:potion` (projectile) |
| Aviary | `minecraft:skeleton` | `minecraft:creeper`, `minecraft:phantom` |
| Keep Kayra (root spawner entities) | `minecraft:skeleton`, `minecraft:wither_skeleton` | `minecraft:slime`; passenger `minecraft:creeper` (excluded), `minecraft:potion` (non-mob) |

**Potential hostile-mob coverage omissions:** `minecraft:creeper`, `minecraft:hoglin`, `minecraft:magma_cube`, `minecraft:phantom`, `minecraft:ravager`. They are legitimate source *review candidates*, **not an approval to include them globally**. In particular the existing filter deliberately avoids many explosive, flying, elite or boss-like types. Projectile/effect IDs `firework_rocket`, `potion` and `evoker_fangs` should **not** be added to the ordinary mob attribute regex.

## IDAS — Integrated API native element support now VERIFIED

The native IDAS jigsaw pool uses **`integrated_api:integrated_api_single_pool_element`** rather than Minecraft's default single-pool element. After adding source-exact parser support, the SHA-1 verified IDAS 1.13.7 JAR now traces genuine start-pool descendants without missing-template errors:

| IDAS source structure | Native templates inspected | Ordinary spawner **block occurrences** | Spawner ID samples | Source pool graph |
|---|---:|---:|---|---|
| `idas:pillager_camp` | 1 | **2** | `minecraft:pillager` | Traversed successfully |
| `idas:labyrinth` | 5 | **18** | `minecraft:blaze`, `cave_spider`, `husk`, `spider`, `stray`, `alexsmobs:anaconda`, `quark:forgotten`, `quark:wraith` | Traversed successfully |
| `idas:necromancers_spire` | 4 | **4** | `minecraft:skeleton`, `alexsmobs:soul_vulture` | Traversed successfully |

**IDAS subtotal: 24 additional source template occurrences. Grand total for all 10 scanned structure IDs: 78 ordinary spawner blocks in distinct source templates (all 10 sites source-positive).** Eight native pool graphs were traversed without identified parser/source errors; Foundry and Mechanical Nest remain partial. These are *not* natural spawn counts or proven effective DD targets.

The previous filename/path heuristic had reported **four** spawner blocks in `data/idas/structure/pillager_camp/pillager_camp1.nbt`; the actual current native `pillager_camp` start pool points to a different template location with **two** observed spawner blocks. These are different source-scan scopes; **do not sum or silently replace the old count**.

### Modded entity compatibility

The exact PR50 import manifest includes `alexsmobs-1.22.9.jar` (Alex's Mobs) and `Quark-4.1-487.jar`. Thus **the provider JARs are present by filename**; don't claim the NBT IDs `alexsmobs:anaconda`, `alexsmobs:soul_vulture`, `quark:forgotten` or `quark:wraith` are missing merely because they are not vanilla. However, actual entity registration, spawn behavior, hostility and elite interactions in the effective client remain unverified.

All four of those modded entity IDs are outside the existing `minecraft:`-only DD regex. **IDAS Labyrinth is provisionally Tier 4, but is not one of the 53 original candidate DD zones**, and the Nether-tagged Necromancer's Spire requires its separate dimension review. No widening of regex or deployment is authorized from these findings.


## Mechanical Nest — owner-approved boss-first exception

**Owner decision (14 Oct):** Mechanical Nest's **boss is the only balancing-critical encounter**. Treat ordinary zombies, skeletons, ravagers and mounted creepers as incidental; **do not** spend time scaling each of them with DD. The provisional structure Tier 5 remains research-only, and the previous whole-structure `ao_tier_5` DD zone is **not approved for deployment unchanged**. When the boss is identified, prefer native/boss-specific tuning and guard against Apotheosis double-stacking. No live DD configuration has been modified.

**Native source reality:** The exact PR50 SHA1-pinned Dungeons Arise 2.1.68 JAR contains **160 Mechanical Nest `.nbt` templates**, including spawner variants. The only explicitly named native spawner payload recognized by the audit is **Gearling** (`minecraft:zombie`, baby, 6 NBT Health), which is **not verified to be the boss**. A distinct boss identity/mechanism could be introduced through other installed mods or game logic. The source scan does **not** prove the boss is missing or establish what to buff.

**Mechanical Nest native source resource warnings (no auto-repair):** `mechanical_nest_spawner_6.nbt` is referenced but missing from the pinned native JAR; `mechanical_nest_bridge_terminator_6_.nbt` includes an extra trailing underscore compared with a similar existing file; the template `mechanical_nest_towers_1.nbt` points at singular `mechanical_nest_decoration`, while a plural `mechanical_nest_decorations` pool exists. These are potential native-source mismatches, not yet evidence of a broken deployed dungeon. Do not alter the effective Paxi/worldgen profile without controlled repro.

**Foundry:** Source spawners contain named, stat-modified vanilla enemies—Foundry Guardian (blaze, 55 NBT Health), Debris Miner (piglin brute, 50), and Forge Sentry (wither skeleton, 55 or 80). These need **avoidance of blind generic double-scaling**, not automatic boss classification. `foundry_corridor_crossing_2.nbt` references absent native pool `dungeons_arise:underworld/foundry/foundry_corridor_gears`; check the final effective source and test generation before editing.

See [pinned native boss / jigsaw evidence](DD_MECHANICAL_NEST_FOUNDRY_NATIVE_BOSS_REFS_20261014.json) and [owner's boss-only policy file](DD_OWNER_BOSS_CENTRIC_SCOPE_20261014.json). Both were recorded while keeping the active modpack unchanged.
## Other native mounted-encounter exceptions

The same passenger scanner found additional intentionally combined native encounters in the pinned source. These are **source NBT pairs**, not guaranteed natural-generation outcomes:

| Source | Mounted pair | Implication for future DD work |
|---|---|---|
| Foundry, `foundry_wither_skeleton_1.nbt` | Hoglin carrying Wither Skeleton | Avoid unintentionally overbuffing the rider relative to its mount; test exact encounter first |
| Foundry, `foundry_wither_skeleton_3.nbt` | Phantom carrying Wither Skeleton | Flying mount mechanics; preserve before general phantom scaling |
| Mechanical Nest, `mechanical_nest_spawner_4.nbt` | Ravager carrying Creeper | Preserve explosive mounted mechanic; don't expand creeper/ravager DD globally from this one example |

Other passenger entities include potions, fireworks and lightning effects. They are **not ordinary hostile mob targets**. No change to the 17-vanilla-mob DD candidate regex is authorized; Apex/boss and Apotheosis interactions remain outside this passive source scan.
## Priorities for the next automated pass

1. **DONE:** Verify IDAS custom `integrated_api` pool-element serialization and cross-check its actual start-pool linked spawner/entity source IDs.
2. **DONE:** Use bounded two-pass NBT streaming for Keep Kayra; detect nested passenger pairs without classifying item IDs as mobs.
3. **PINNED SOURCE COMPLETE, RUNTIME PENDING:** Foundry absent corridor-gears pool and three Mechanical Nest native asset-name gaps identified with exact paths. Reproduce the **effective** datapack winner and generation consequences before proposing any pool fixes. For Mechanical Nest, prioritize finding and testing its boss, not scaling incidental spawner mobs.
4. Source-vs-live test ordinary DD attributes on representative zombies/skeletons/pillagers, then *omitted* vanilla hostiles on actual source spawners. Explicitly test Apotheosis modifiers and boss/native scripts for double stacking.
5. Only after representative live DD acceptance, draft *isolated* rules for genuinely unsupported standard hostiles, preserving the no-native-boss/global-spawner modifications policy.

### What the owner needs

**Nothing now.** The scanner, source-jigsaw evidence and DD policy tests run without client involvement. When a safe experimental candidate exists, later use a disposable world to check mobs inside/outside one or two key structures (e.g. Bandit Towers and Foundry), plus one high-tier boss exception, with exact world seed, active datapacks and log excerpts. Do not touch the long-lived multiplayer world or its Chunky pregen during source research.

**All 53 existing candidate zones remain research-only; none of the newly scanned templates or candidate matcher gaps authorizes live DD.** Source parser unit tests explicitly reject equipment/enchantment IDs as mobs and flag 0-template custom structures incomplete. Validation: [PR56 GitHub Actions](https://github.com/alsynth/AmbientOdyssey/actions).
