# Ambient Odyssey — all 14 R3 Grand chest native loot sources VERIFIED against pinned published JARs
**15 October 2026 | Source-table identity: verified | Lootr/gameplay: NOT TESTED | R2: UNCHANGED**

## Concrete status
All fourteen previously scoped T3–T6 Grand Treasure source tables and their candidate pool indices have now been checked against the exact released mod JARs in a read-only GitHub Actions environment. Every original **raw loot-table SHA256 matches** the repository's previous native JAR/structure audit. No official JARs were committed and no native table files were changed.

| Mod | Source version | Count | Verification |
|---|---|---:|---|
| When Dungeons Arise | 1.21.1 NeoForge **2.1.68** | **11** | CI run [38742993105](https://github.com/alsynth/AmbientOdyssey/actions/runs/38742993105), same original table sources |
| Adventure Dungeons | NeoForge **1.21 1.3.1** | **1** | CI run [38743667218](https://github.com/alsynth/AmbientOdyssey/actions/runs/38743667218) |
| Iron's Spellbooks | NeoForge **1.21.1 3.16.3** | **2** | Same CI run [38743667218](https://github.com/alsynth/AmbientOdyssey/actions/runs/38743667218) |
| **Total** | | **14/14** | Source hashes verified, category selection and runtime still open |

The individual original resource hashes, indices, weights and item IDs are retained in:
- `docs/handoffs/loot-update-20261015/R3_DUNGEONS_ARISE_11_PINNED_SOURCE_VERIFICATION_20261015.json`
- `docs/handoffs/loot-update-20261015/KEEP_KAYRA_PINNED_SOURCE_POOL_EVIDENCE_20261015.json`
- `docs/handoffs/loot-update-20261015/R3_LAST_THREE_PINNED_NATIVE_SOURCE_VERIFICATION_20261015.json`

## Five source-grounded category improvements — R3 REVIEW ONLY
Existing R2 structure-wide/general-value algorithm often added another iron/gold/diamond resource roll even to special treasure chests. The **same 14 original trigger contexts** have a separate R3 preview that instead offers five more category-appropriate pool selections from EXACT matching native table resources:

| Chest | R2-selected or earlier candidate | Proposed native pool | Why |
|---|---:|---:|---|
| Keep Kayra library treasure | garden-normal pool 1 (R2); own pool 2 (early preview) | **own pool 1** | Native enchanted book/equipment, rare Netherite Helmet (2/106 of selected single-roll weight) |
| Keep Kayra keep treasure | garden-normal pool 1 (R2); own pool 2 (early preview) | **own pool 1** | Native enchanted book/equipment, rare Netherite Boots (2/114 weight) |
| Adventure Dungeons Murky reward | own pool 0 | **own pool 2** | Native Wild/Sentry armor trim templates and music discs rather than extra minerals |
| Iron's catacombs hidden trough | own pool 3 | **own pool 1** | Native randomized spell scroll (weight 2) or blank rune (weight 1) rather than emeralds/diamonds |
| Iron's generic magic treasure | own pool 6 | **own pool 1** | Native randomized spell scroll rather than mixed iron/copper/gold |

Iron's source scroll functions are `irons_spellbooks:randomize_spell`, maintained via copying the original native pool. **Its allowed spell tier/power still requires runtime validation.** Current Grand bonus is **5% per eligible chest and one extra single-pool roll**. Native underlying pool `rolls` greater than 1 is replaced by one *bonus* roll only; original native pool and chest remain unchanged.

The source-verified category choices are explicit data in:
- `R3_KEEP_KAYRA_SOURCE_GROUNDED_CATEGORY_CHOICES.json`
- `R3_LAST_THREE_NATIVE_CATEGORY_POOL_PROPOSALS_20261015.json`

The generator `tools/prepare_r3_grand_chest_policy.py` reads and SHA-checks them against native evidence, and still emits **review-only** candidate policies. The revised `R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json` and ledger contain fourteen unchanged chest contexts and **five** source-grounded category improvements. It does not silently approve or compile them. The automated source/policy tests passed: [GitHub Actions run 38744635880](https://github.com/alsynth/AmbientOdyssey/actions/runs/38744635880) (35 synthetic tests).

## Explicit scope hold — Keep Kayra garden treasure
A **sixth Keep Kayra native chest table** was also verified: `dungeons_arise:chests/keep_kayra/keep_kayra_garden_treasure`. Its native pool #2 contains golden apples and a low-weight enchanted golden apple (1 weight / 52 total). This table was not in the original fourteen eligible R2 contexts and is **NOT silently added** as a 15th context. If expanding eligibility later, record it separately and confirm worldgen chest NBT, category, balance and new-context controls.

## Unresolved — must NOT be mislabeled 'fully verified'
The 14/14 status refers to **source-table hash and pool existence in published pinned JARs**, **NOT** the exact last effective Paxi/datapack winner in the running Minecraft pack, nor Lootr per-player roll semantics. It doesn't guarantee that the chosen pool is best balanced or that `randomize_spell` produces acceptable tiers.

Before compiling/patching the R3 addon or importing a playable R3:
1. On the matched installed profile, run `tools/audit_r3_native_reward_sources.py` against the **new 14-row R3 preview** and all Paxi datapacks. Verify current installed copies and effective resource precedence. Paxi collisions require in-engine winner proof, not a disabled hash check.
2. Manually review all 14 pool categories and any source functions, particularly random spell tiers and loot modifiers. Record exact per-pool decisions in the fail-closed `tools/stage_r3_grand_policy.py` decision form; no automatic approval.
3. Use `tools/patch_r3_grand_campaign_jar.py` only for a policy-resource change with **all compiled classes byte-identical** to R2; compile actual new Java if behavior/code changes.
4. Test in fresh FTF world and disposable dedicated two-player server: native contents retained (no replacement), per-player Lootr independence and reopening persistence, 5% independent bonus per eligible chest, no T0–T2/other structures, no recursion/boss-trophy duplication, no altered native affix/gem drops.
5. Preserve R2 immutable and never ship R3 as runtime-validated before these pass.

Other loot work — wider Regalia and T2+ Scrap/Treasure scaling — remains separate and must not be marked implemented based on this source audit.
