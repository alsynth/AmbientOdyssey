# AO Structure Categories: Reviewed Provisional Tier Confidence (14 Oct 2026)

Research-only classification, part of draft PR #56. No Minecraft settings changed.

## Totals
- All known structure IDs: **1,240 / 1,240** have previously assigned first-pass numeric estimates. Known current-profile roster: **1,130 / 1,130**. **These percentages measure completeness, not confidence, registration, or gameplay correctness.**
- **157 HIGH**, **637 MEDIUM**, **420 LOW**, **26 OWNER_HOLD**. Only HIGH entries are in the tier shortlist. No rating signifies runtime validation or authorization for DD rules.
- 26 spawner-positive small-looking IDs still owner protected, even with prior numeric placeholder guesses. Additional 15 source-only family holds not counted as structure IDs.
- 107 historical Repurposed Structures ID variants are absent from the current modpack JAR profile, not counted among HIGH entries.

## Provisional progression bands
| Tier | AO progression category |
|---|---|
| 0 | T0_CIVILIAN_AMBIENT |
| 1 | T1_LIGHT_EXPLORATION |
| 2 | T2_EARLY_HOSTILE |
| 3 | T3_MIDGAME_DUNGEON |
| 4 | T4_MAJOR_DUNGEON |
| 5 | T5_ADVANCED_DUNGEON |
| 6 | T6_ELITE_BOSS |
| 7 | T7_LATE_BOSS |
| 8 | T8_SUPERBOSS |
| 9 | T9_APEX_BOSS |

## HIGH-confidence shortlist: 157 exact IDs
The shortlist has high confidence in **structure archetype and broad proposed progression tier**, not in runtime encounter mechanics or suitability for global DD multipliers.

| Archetype / tier | Count | Examples |
|---|---:|---|
| CIVILIAN_VILLAGE / Tier 0 | 82 | `ctov:large/village_beach`, `ctov:large/village_christmas`, `ctov:large/village_dark_forest` |
| ILLAGER_OUTPOST / Tier 2 | 43 | `ctov:pillager_outpost_badlands`, `ctov:pillager_outpost_beach`, `ctov:pillager_outpost_dark_forest` |
| ABANDONED_MINESHAFT / Tier 2 | 13 | `bettermineshafts:mineshaft_acacia`, `bettermineshafts:mineshaft_desert`, `bettermineshafts:mineshaft_dripstone` |
| WITCH_HUT / Tier 2 | 1 | `minecraft:swamp_hut` |
| RAID_MANOR / Tier 3 | 1 | `minecraft:mansion` |
| MONUMENT / Tier 3 | 1 | `minecraft:monument` |
| FORTRESS / Tier 4 | 1 | `minecraft:fortress` |
| STRONGHOLD / Tier 4 | 1 | `minecraft:stronghold` |
| TRIAL_DUNGEON / Tier 4 | 1 | `minecraft:trial_chambers` |
| BASTION / Tier 5 | 1 | `minecraft:bastion_remnant` |
| ANCIENT_CITY / Tier 6 | 1 | `minecraft:ancient_city` |
| LATE_BOSS_LOCATION / Tier 7 | 5 | `cataclysm:burning_arena`, `cataclysm:cursed_pyramid`, `cataclysm:frosted_prison` |
| SUPERBOSS_ARENA / Tier 8 | 5 | `block_factorys_bosses:dragon_tower`, `block_factorys_bosses:kraken_ship`, `block_factorys_bosses:sandworm_nest` |
| APEX_BOSS_LOCATION / Tier 9 | 1 | `cataclysm:sunken_city` |

## Confidence interpretation
- **HIGH**: vanilla-defined, documented CTOV/Towns & Towers villages and pillager outposts, documented YUNG abandoned mineshaft family, or clearly named boss encounters already placed in the AO boss-tier plan. **Not runtime-tested; no DD generated.**
- **MEDIUM**: strongly suggested encounter type but mob strength, native rules, active registration or effective datapack source unverified.
- **LOW**: not enough evidence beyond provisional numeric heuristic; Pasterdream, fortified/underground CTOV, and unresolved special sites require later study.
- **OWNER_HOLD**: never deploy a tier until the user reviews the original 26 positive-spawner structures.
- Existing known inconsistency: `twilightforest:hydra_lair` remains historical Tier 4 in this catalogue although the user's subsequent boss plan has Hydra at Tier 7. Its tier is deliberately not considered HIGH. `minecraft:end_city` also has an unresolved original mixed tier interpretation (2|5) and is LOW.

## Data
- [All ID categories and confidence](DD_PROVISIONAL_CATEGORIES_CONFIDENCE_20261014.csv) — 1,240 one-to-one mapped rows.
- [Confidence-backed tier shortlist](DD_HIGH_CONFIDENCE_TIER_SHORTLIST_20261014.csv) — 157 high rows only.
- [Original 100% numeric draft](DD_FULL_FIRST_PASS_TIER_MAP_20261014.csv) remains unchanged.

## External archetype references
- [Towns & Towers description](https://www.curseforge.com/minecraft/mc-mods/towns-and-towers) — vanilla-like villages and varying pillager outposts.
- [ChoiceTheorem's Overhauled Village](https://www.curseforge.com/minecraft/mc-mods/choicetheorems-overhauled-village) — village and pillager outpost variants.
- [YUNG's Better Mineshafts](https://www.curseforge.com/minecraft/mc-mods/yungs-better-mineshafts-neoforge) — 13 biome-variant abandoned mineshafts.
- [Repurposed Structures](https://www.curseforge.com/minecraft/mc-mods/repurposed-structures) — vanilla structure analogues, only historical scope in this PR.

**No source scan, Natural Generation, Paxi, DD entity matcher, boss scaling or server test was run by this classification.**
