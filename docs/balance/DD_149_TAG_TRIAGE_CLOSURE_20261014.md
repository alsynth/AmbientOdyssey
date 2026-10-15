# PR56 — Removed-biome tag triage closed at *source* stage (14 Oct 2026)

**Outcome:** This research wave has checked **all source-priority Overworld combat cases** selected from the old 149-entry unresolved-tag subqueue. **No confirmed live worldgen break** was found among these ten targeted pinned-native combat audits, so no global tag expansion, structure-frequency increase or removed-biome restoration is justified. The wider **705 historical zero-curated-hit** catalogue remains a *source warning list*, not 705 broken structures. This is emphatically **not** full runtime registry/placement verification.

## Queue disposition — 149 historical source unresolved-tag rows

| Fail-closed triage lane | Number |
|---|---:|
| Historical ID outside the 1,240 known current first-pass rows | 40 |
| Provider absent from the reconciled PR50 roster **by filename** | 30 |
| Tier0/1 or not a Tier2–6 combat-priority row | 34 |
| Tier2–6 sites with explicit End tags/namespace; separate End workstream | 20 |
| Tier2–6 sites with explicit Nether native tags/namespace; separate Nether workstream | 8 |
| Tier2–6 retained current-roster sites with exact pinned native source tag examined; **NO AUTO REPAIR** | 17 |
| **Remaining source-priority Overworld combat structures without a pinned native investigation** | **0** |
| **Total** | **149** |

Machine-readable row-level ledger: [`DD_149_TAG_SOURCE_PRIORITY_QUEUE_20261014.csv`](DD_149_TAG_SOURCE_PRIORITY_QUEUE_20261014.csv). These are historical Test5 candidates; `present_pr50_by_filename` is **not** complete dynamic registry evidence. Every row remains `worldgen_edit_authorized=NO` and `live_registration_or_generation_proven=NO`.

## Exact-JAR verified combat site source evidence (17 Overworld-tag candidates)

- **When Dungeons Arise (5):** `bandit_towers`, `bandit_village` use **Badlands** tags; `ceryneian_hind`, `scorched_mines`, `shiraz_palace` use **Desert** tags, with a native `minecraft:desert` reference in the last three. Native major-set spacing 50/separation 45; AO `ao_structure_density` already overrides source placement with a frequency modifier. Preserve it.
- **IDAS (3):** `desert_pyramid`, `desert_ruins`, `labyrinth` use Desert sources with vanilla `minecraft:desert` and external tags. Native rarity uses `integrated_api:advanced_random_spread`; AO already has a placement override for the shared `idas_common` set, which must not be overwritten or changed blindly.
- **YUNG Better Mineshafts (5):** `mineshaft_acacia` has savanna source routes; `mineshaft_desert` contains vanilla desert; `mineshaft_mesa`/`mineshaft_red_desert` depend on external Badlands tags; `mineshaft_mushroom` contains `minecraft:mushroom_fields`. Source documents unresolved `c:/forge:/minecraft:` tags; their existence in the native JAR alone is not the complete effective loaded tag.
- **Dungeons & Taverns (3):** `badlands_miner_outpost` has native Badlands/wooded Badlands plus other optional entries, `desert_ruins` has vanilla desert and old optional entries, and `trident_trial_monument` depends on external `#minecraft:has_structure/ocean_monument`. **No shared D&T biome-tag bridge deployed**; the four tower-specific test datapack is independent.
- **Moog's Temples Reimagined (1):** `mtr:badlands_temple` selects `#minecraft:is_badlands` and `#c:is_badlands`. Badlands is not shown as a direct Biolith replacement target in the recorded AO placement file; vanilla biome fallback may exist. No auto-repair.

The **IDAS `necromancers_spire`** was originally counted as a plausible Overworld source concern, but the verified IDAS native `idasnether` tag shows it belongs in the **Nether**. Likewise, **Friends & Foes `citadel`** exclusively selects `#minecraft:is_nether` and `#c:in_nether`, so it also moves to Nether acceptance. Source-only JAR evidence proves tag *definitions*, not natural placement.

Exact primary evidence:
- [PR50 pinned When Dungeons Arise + IDAS](DD_DUNGEONS_ARISE_IDAS_COMBAT_BIOME_SOURCE_20261014.json)
- [Four-provider pinned combat source including Friends & Foes and Moog's](DD_FOUR_PROVIDER_COMBAT_BIOME_SOURCE_20261014.json)
- [YUNG native 7-variant biome source](DD_YUNGS_MINE_SHAFT_NATIVE_BIOME_SOURCE_20261014.json)
- [D&T pinned collection and three additional sources](DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json)

## Preserved existing AO worldgen policy

- No direct change to **Dungeons Arise major-set `ao_structure_density` modifier**, **IDAS common-set placement**, or AO **vanilla village spacing 36/separation 8** override; existing settings take precedence over native-JAR defaults in the intended source stack, but the runtime resource winner still needs a real profile check.
- No generic changes to `minecraft:is_badlands`, `#c:is_desert`, `c:plains`, `minecraft:has_structure/pillager_outpost` or `minecraft:has_structure/ocean_monument`.
- No restoration of removed biome providers or introduction of worldgen changes to the installed pack, no increased Dungeon Difficulty, spawner, structure-set, loot, mob, boss or rollback edits.
- The four D&T firewatch **structure-specific** draft is a *separate* **TEST-ONLY** datapack, not a live profile: see [controlled A/B test sheet](../testing/PR56_FIREWATCH_TEST_ONLY_ACCEPTANCE_20261014.md).

## What needs the owner, and when

**Now:** nothing. Existing Tier0=26 and uniform Dungeon Crawl Tier3 decisions are protected by tests and do not need reapproval.

**Before final 10k–20k Chunky pregen:** use one disposable-world smoke/acceptance pass with the exact current pack and enabled Paxi datapacks; inspect firewatch natural placement/density (especially common Prairie) and representative major structure and Nether sites if they are missing. **Do not schedule separate tests for each of these 149 historical IDs.** If live generation works, mark that family verified rather than changing any config.

**Remaining independent research:** real source/runtime placement review of other high-priority entries in [34-ID critical audit](DD_POSTMAP_CRITICAL_34_TIER_REVIEW_20261014.csv), including Nether Eternal Nether placements, and DD T2–6 **mob/elite mechanics**. A fully current native registry enumeration and runtime natural placement check remain incomplete.

### Automated verification
[Actions run 38609454404](https://github.com/alsynth/AmbientOdyssey/actions/runs/38609454404) completed **six successful jobs** (catalogue policy, pinned D&T, native YUNG, three other pinned mod sources, native four combat providers, and PR50 Paxi source comparison). This certifies only the listed static and pinned-native checks.

**PR #56 stays DRAFT, research-only. No gameplay changes deployed.**
