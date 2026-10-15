# Ambient Odyssey — R3 Grand Treasure mapped-source review
**15 Oct 2026 · Draft mapping audit, not gameplay approval or tested effective resources**

## Findings from committed R2 candidate list
The current R2 policy includes **14** T3+ Grand Treasure contexts at the approved **5% per eligible chest** rate. Of these, **6** draw from a pool in the triggering chest's own table; **8** draw from a different loot table. The latter is not automatically wrong: the owner chose the structure's best existing native loot pool, even when that is elsewhere within the same structure. But the **specific chosen pools were scored heuristically, not confirmed as the best native source by the owner or a live loot audit**.

The issue is not that a bonus uses a different native chest table. The issue is **verification** that that source really belongs to this structure, is an appropriate best pool, and preserves native treasure behavior. Do not silently replace any of these with homemade generic rewards.

## All 14 current contexts

| # | Structure | Triggering chest table path | Selected native source path + pool | Review |
|---:|---|---|---|---|
| 1 | `adventuredungeons:murkydungeon` | `chests/murkydungeon/murky_chest_reward` | `chests/murkydungeon/murky_chest_reward` #0 | Self-table |
| 2 | `dungeons_arise:illager_fort` | `chests/illager_fort/illager_fort_normal` | `chests/illager_fort/illager_fort_normal` #2 | Self-table |
| 3 | `dungeons_arise:infested_temple` | `chests/infested_temple/infested_temple_room_normal` | `chests/infested_temple/infested_temple_room_normal` #3 | Self-table |
| 4 | `dungeons_arise:infested_temple` | `chests/infested_temple/infested_temple_room_supply` | `chests/infested_temple/infested_temple_room_normal` #3 | Cross-table: review |
| 5 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_garden_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Self-table |
| 6 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_library_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 7 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_library_treasure` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 8 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 9 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_treasure` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 10 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_rooms` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Cross-table: review |
| 11 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_top_rooms` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Cross-table: review |
| 12 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_top_treasure` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Self-table |
| 13 | `irons_spellbooks:catacombs` | `chests/catacombs/hidden_trough_treasure` | `chests/catacombs/hidden_trough_treasure` #3 | Self-table |
| 14 | `irons_spellbooks:catacombs` | `chests/generic_magic_treasure` | `chests/catacombs/hidden_trough_treasure` #3 | Cross-table: review |

**Note:** This table is generated from `docs/handoffs/loot-update-20261015/grand-treasure-candidates.json`; per-source original expected SHA256 values reside in that JSON. It does **not** establish which datapack definition wins at runtime.

## Binding source proof / acceptance for each mapping
1. Extract from the **exact installed JAR** (not generic online documentation). Match source-resource SHA256; verify the triggering loot table exists and its structure/template NBT actually references it; verify owner/structure association and dimension.
2. List selected pool's original entries/weights, conditions, functions, table-level functions, optional gated items and any recursion/unique trophies. `getRandomItemsRaw` must represent exactly one extra native-source draw and must not reproduce guaranteed unique boss rewards.
3. For each **cross-table** mapping, state why the selected pool is the best suitable existing native treasure pool in that structure. A room chest pulling from top treasure can be intentional; a garden-normal pool from a library-treasure chest needs justification. If not defensible, hold that trigger or identify its own verified native treasure pool instead.
4. Confirm exact installed Paxi / data resource precedence and loot-modifier timing, including Lootr conversion and individualized loot generation. `replace:false` is insufficient to establish Java append behavior; explicitly assert original list contents remain intact.
5. Mark entries **SOURCE VERIFIED / REVIEW HELD / STATIC UNKNOWN / RUNTIME ACCEPTED** separately. No automatically promoted reward pool or invented item IDs.

## Reproducible evidence tool added to PR #63
After installing the **actual** modpack locally via CurseForge, run on Windows:

```powershell
python tools/audit_r3_native_reward_sources.py --mods "C:\Minecraft\Instances\Ambient Odyssey\mods" --paxi "C:\Minecraft\Instances\Ambient Odyssey\config\paxi\datapacks" --out build\r3-reward-source-audit.json
```

Substitute actual profile path. Script reads JARs, checks source and trigger tables, expected SHA256, pool index and entries, and detects matching Paxi overrides. It also scans all Regalia catalogue candidates for *static* item-model/recipe clues and honors exclusions; **it does not prove item registration or approve new Regalia**. It never mutates modpack files.

### Important packaging boundary
The public GitHub Git tree does **not** contain official installed JARs; R2's CurseForge import ZIP has 337 manifest refs plus 10 custom JARs, not the other ~330 official mod binaries. Therefore this document and CI synthetic tests cannot substitute for a real installed-mod/JAR source audit.

Until those artifacts are audited, **do not claim all 14 are verified or expand beyond them**. Reuse R2 only as an experimental source, and keep R3 archive separate.

## Owner-approved R3 correction — 15 October 2026
The owner agrees to replace the old **structure-wide highest-scoring source pool** selection. **Choose a fitting and valuable existing native loot pool by chest category**, strongly preferring the triggering chest table's own selected valuable pool where it is appropriate. A cross-table source in the same dungeon remains possible *only with explicit supporting evidence* of superior category fit. Keep Kayra library treasure must not borrow garden-normal merely because the algorithm assigned more points to a few vanilla items. Preserve native contents; one bonus draw at 5%; retain unrelated native mod loot, Apotheosis affixes/gems, and Lootr independence. **This is an R3 owner decision; the currently compiled R2 JAR/policy is unchanged.**

The source audit already contains alternative selected pools for the eight borrowed-table mappings, documented in `docs/handoffs/loot-update-20261015/R3_SAME_TABLE_GRAND_ALTERNATIVES_UNAPPROVED.json`. The **approach** is approved, not these exact indices or contents: verify item weights/functions/conditions, SHA256, Paxi effective precedence and that each extra roll comes from the verified suitable native pool before changing the R3 runtime policy.

## R3 implementation preparation: reproducible 14-context preview (15 Oct 2026)

A **non-runtime R3 preview** is now committed:
- `docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json` — 14 trigger→own-native-table candidates, retaining each source's audited pool index/hash; unlike R2's policy, **none borrows a sibling chest's pool automatically**.
- `docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_REVIEW_LEDGER.json` — one hold/review row per candidate, recording whether the old R2 source changed. Eight of fourteen changed. All fourteen remain **NEEDS_INSTALLED_JAR_REVALIDATION / NEEDS_MANUAL_REVIEW**.
- `tools/prepare_r3_grand_chest_policy.py` — reproducible preview generator from historical NBT + native chest audit. This is intentionally **not** wired to `tools/compile_additive_loot_policy.py` or the currently packaged campaign JAR, because exact source checks and per-category choices have not been finished.

To reproduce a fresh untracked preview without touching the live source policy:

```powershell
python tools/prepare_r3_grand_chest_policy.py --out build/r3-grand-candidates.json --review build/r3-grand-candidate-review.json
```

To check the actual installed native JARs against those proposed bonus sources:

```powershell
python tools/audit_r3_native_reward_sources.py --mods "C:\Path\To\AO-Profile\mods" --paxi "C:\Path\To\AO-Profile\config\paxi\datapacks" --candidates docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json --out build/r3-grand-native-source-check.json
```

The improved native JAR auditor now records **ALL native pools for each candidate table**, including individual item IDs, relative weights, original roll counts, conditions, function definitions and nested/composite-entry flags. The intent is a real comparison of library treasure versus garden normal, **not** blindly taking a maximum score. Output is static JAR evidence, not a verified item-registry/runtime-loot declaration.

**Promotion gate:** Human review each selected category's relative reward pool; verify hash, effective datapack order and that no unique/gated rewards can be duplicated; run Lootr two-player and unchanged-native-loot tests; only then opt in to that specific R3 candidate by regenerating the campaign policy and recompiling `ao-campaign`. Leave failed cases disabled/held instead of shipping heuristic guesses. Keep all original R2 mappings/archives unchanged.
