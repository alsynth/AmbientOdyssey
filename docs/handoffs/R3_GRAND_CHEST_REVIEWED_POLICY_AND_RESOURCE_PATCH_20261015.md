# Ambient Odyssey R3 — Grand Treasure staged policy + no-recompile addon patch
15 October 2026 | PR #63, branch experimental/master-integration-20261015 | EXPERIMENTAL / NOT RUNTIME-TESTED

## Why this path is useful
R2 Java already reads chest mappings from ao_loot_policy.json stored inside its compiled ao-campaign JAR. Therefore, a mapping-only update need NOT download NeoForge or Apotheosis build dependencies or rebuild Java classes. This path substitutes that one JSON resource inside a copy of the exact R2 addon and verifies every other JAR member remains byte-for-byte unchanged.

The historical tools/compile_additive_loot_policy.py still uses the old R2 cross-table source list. Do not run it during the R3 mapping-only path: it could undo the chest-specific correction.

The owner approved category-appropriate native chest pools (5% additional draw per eligible T3+ chest, never native replacement), not automatic approval of the fourteen exact pool indices. Real native JAR source inspection and explicit human review are required.

## Inputs
- Exact R2 import ZIP (SHA256 db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617), obtainable via tools/prepare_r2_local_inputs.py on an authenticated PC.
- Actual matching CurseForge installation with the official mods/ JARs; the 154MB import ZIP doesn't include ~330 official mod binaries.
- The committed R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json under docs/handoffs/loot-update-20261015/.
- Git checkout of experimental/master-integration-20261015.

## Step 1: Verify actual installed JAR source tables
From the repository root, using the actual client profile location:

    python tools/audit_r3_native_reward_sources.py --mods "C:\PATH\TO\AO_PROFILE\mods" --paxi "C:\PATH\TO\AO_PROFILE\config\paxi\datapacks" --candidates docs/handoffs/loot-update-20261015/R3_PER_CHEST_GRAND_CANDIDATES_REVIEW_ONLY.json --out build/r3-native-source-audit.json

The audit logs native JAR source hashes, all native pool IDs/entries/weights/functions/conditions and Paxi resource collisions. It must show no blocked candidate before promotion. Source verification does not imply runtime acceptance or confirm the best pool.

## Step 2: Create the human review sheet (everything DENIED by default)

    python tools/stage_r3_grand_policy.py --mode draft --audit build/r3-native-source-audit.json --out build/r3-grand-review-decisions.json

For each native candidate review thematic chest-category fit, actual relative entry weights, functions, conditions, restricted/trophy items and item validity. Manually mark reviewed_category_fit, reviewed_native_entries_weights_conditions_functions, approved_for_experimental_build true with a substantial reviewer_rationale for genuinely reviewed entries. Change overall status to REVIEWED_FOR_EXPERIMENTAL_BUILD only when complete. Do not invent approvals to pass the gate.

This first revision is conservatively scoped to the triggering chest's own native table. Cross-table borrowing can be allowed in future with independent evidence under the owner's general policy; it is not silently selected here.

## Step 3: Stage isolated approved R3 campaign policy

    python tools/stage_r3_grand_policy.py --mode stage --audit build/r3-native-source-audit.json --approvals build/r3-grand-review-decisions.json --out build/r3-stage/ao_loot_policy.json --report build/r3-stage/ao_loot_policy.receipt.json

This checks source and audit input hashes, exact 14 chest contexts, five-percent rate, unique native JAR providers, source SHA and pool index, no unresolved Paxi collision, safe native simple pool entries and explicit individual review decisions. All non-Grand parts of the original campaign policy are unchanged. The compiled R2 JAR/source stays untouched.

## Step 4: Patch one resource in a NEW copied R2 campaign JAR

    python tools/patch_r3_grand_campaign_jar.py --r2 build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip --policy build/r3-stage/ao_loot_policy.json --staging-receipt build/r3-stage/ao_loot_policy.receipt.json --out build/r3-overlay/overrides/mods/ao-campaign-0.3.0-experimental.jar --report build/r3-reports/campaign-resource-patch.json

The patcher enforces exact input ZIP SHA, addon mod ID/version, old-vs-new policy preserving EVERYTHING except the Grand Treasure rows, unchanged trigger contexts and chance, unsigned source JAR and every other compiled JAR member byte unchanged. It writes its receipt OUTSIDE overrides/ to avoid accidentally bundling the receipt as an override. Keeping the same addon filename ensures the R2-to-R3 packager replaces the old JAR instead of adding a second ao_campaign.

This changes the addon resource but does not compile or test new Java. Any later Java modifications REQUIRE a real addon rebuild.

## Step 5: Package separate, rollback-capable R3 import

    python tools/draft_r3_change_plan.py --base build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip --overlay build/r3-overlay --out build/r3-plan.json

Fill in the overall and per-change reasons after reviewing the proposed plan, then:

    python tools/package_r3_from_r2.py --base build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip --overlay build/r3-overlay --plan build/r3-plan.json --output build/Ambient-Odyssey-R3-GRAND-EXPERIMENTAL.zip

Preserve R2, the known-good client, any save and the original 337 CurseForge reference roster. The packager generates a separate rollback and SHA receipt and checks no duplicate mod IDs.

## Required later in-game tests
In a disposable fresh normal AO/FTF world: ensure original chest loot is preserved at original odds, verify 5% extra single-native-pool roll in eligible T3+ structures, and ensure no bonuses in unrelated/T0-T2/Mine Cells chests. Compare Keep Kayra garden, library and main keep variants individually. On a disposable dedicated server, use two non-OP players to test separate Lootr instances, reopening, restarting and late joins. Confirm existing Apotheosis affix/gem sources and all native boss drops remain intact.

## Honest status
Source-review gate, patcher, rollback packager, synthetic tests and CI are prepared. Native installed-JAR review and manual approval are still pending. No R3 policy has been approved, no actual 154MB R2 asset was processed here, no real updated campaign JAR or R3 import ZIP has been built, and no Minecraft or multiplayer test has been performed.
