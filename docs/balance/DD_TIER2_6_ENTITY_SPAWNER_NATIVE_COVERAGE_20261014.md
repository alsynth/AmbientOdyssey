# PR56 — Tier 2–6 Dungeon Difficulty source-encounter audit (14 Oct 2026)

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
| **New** targeted pinned-JAR template scan positive in scaled candidate | **6 of 28** (seven candidate zones specifically scanned; one too large) |
| Candidate changes to vanilla spawner spawn count/delay/range | **0** — the candidate entity-rule's `spawners` multipliers are all zero |
| Gameplay configurations actually installed from PR56 | **0** |

The old ledger's 0/28 was an **evidence gap, not a count of mob-free dungeons**. New native positive findings supersede that negative screen. Direct sources: [53-zone coverage script](../../tools/audit_pr56_dd_zone_coverage.py), [new pinned source 10-site evidence](DD_PINNED_NATIVE_TEMPLATE_SPAWNER_AUDIT_20261014.json), candidate `experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json`. The evidence is built from the exact PR50-pinned NeoForge Dungeons Arise v2.1.68 and IDAS v1.13.7 JARs, SHA-1-verified by CI.

## Seven candidate Dungeons Arise sites — spawners in scanned source NBT templates

| ID | Planned tier | Distinct jigsaw templates inspected | Ordinary spawner **block occurrences** | Pool/NER scan status |
|---|---:|---:|---:|---|
| `dungeons_arise:bandit_towers` | 2 | 26 | **10** | Native graph traversed without identified errors |
| `dungeons_arise:illager_fort` | 3 | 21 | **4** | Native graph traversed without identified errors |
| `dungeons_arise:plague_asylum` | 3 | 33 | **6** | Native graph traversed without identified errors |
| `dungeons_arise:foundry` | 5 | 45 | **8** | **Partial**: jigsaw reference to a missing or externally supplied `foundry_corridor_gears` pool |
| `dungeons_arise:mechanical_nest` | 5 | 162 | **12** | **Partial**: missing native child-pool and template references |
| `dungeons_arise:keep_kayra` | 6 | 1 | **0 observed** | **Blocked**: main `.nbt` exceeds conservative 42 MB decompressed scan limit; **not proof of no mobs** |
| `dungeons_arise:aviary` (End) | 6 | 32 | **5** | Native graph traversed without identified errors |

**Total observed: 45 spawner-block occurrences across different source templates**, NOT 45 spawners inside one generated dungeon. Multiple templates can be alternatives, omitted, rotated or instantiated with different pool weights. No trial-spawner blocks were found in the successfully parsed selected templates, but this says **nothing** about unscanned pieces, scripts, later dynamic placements or custom trial mechanics.

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

**Potential hostile-mob coverage omissions:** `minecraft:creeper`, `minecraft:hoglin`, `minecraft:magma_cube`, `minecraft:phantom`, `minecraft:ravager`. They are legitimate source *review candidates*, **not an approval to include them globally**. In particular the existing filter deliberately avoids many explosive, flying, elite or boss-like types. Projectile/effect IDs `firework_rocket`, `potion` and `evoker_fangs` should **not** be added to the ordinary mob attribute regex.

## IDAS source NBT still unverified via this scanner

The source graph traversal of `idas:pillager_camp`, `idas:labyrinth` and `idas:necromancers_spire` did not yield recognizable single-template NBT paths using the vanilla weighted-pool parser. These are **incomplete source parser capabilities, not empty native structures**. The old IDAS Pillager Camp path heuristic found **four spawner blocks** with `minecraft:pillager` in `data/idas/structure/pillager_camp/pillager_camp1.nbt`. That old finding remains positive source evidence but was not newly verified as a *reachable start-pool descendant*. The next source task is understanding IDAS's `integrated_api` pool-element serialization before joining native structure IDs to concrete NBT templates.

## Priorities for the next automated pass

1. Inspect source-specific pool-element serialization for **IDAS**, separately from vanilla D&T/Dungeons Arise jigsaw formats.
2. Identify a safe bounded method for **Keep Kayra** large-template NBT parsing; do not uncap memory blindly.
3. Verify Foundry missing corridor pool and Mechanical Nest missing NBT references are intentional/non-required or evidence of actual generator problems. **Do not edit installed structure pools without reproducing and validating behavior**.
4. Source-vs-live test ordinary DD attributes on representative zombies/skeletons/pillagers, then *omitted* vanilla hostiles on actual source spawners. Explicitly test Apotheosis modifiers and boss/native scripts for double stacking.
5. Only after representative live DD acceptance, draft *isolated* rules for genuinely unsupported standard hostiles, preserving the no-native-boss/global-spawner modifications policy.

### What the owner needs

**Nothing now.** The scanner, source-jigsaw evidence and DD policy tests run without client involvement. When a safe experimental candidate exists, later use a disposable world to check mobs inside/outside one or two key structures (e.g. Bandit Towers and Foundry), plus one high-tier boss exception, with exact world seed, active datapacks and log excerpts. Do not touch the long-lived multiplayer world or its Chunky pregen during source research.

**All 53 existing candidate zones remain research-only; none of the newly scanned templates or candidate matcher gaps authorizes live DD.** Source parser unit tests explicitly reject equipment/enchantment IDs as mobs and flag 0-template custom structures incomplete. Validation: [PR56 GitHub Actions](https://github.com/alsynth/AmbientOdyssey/actions).
