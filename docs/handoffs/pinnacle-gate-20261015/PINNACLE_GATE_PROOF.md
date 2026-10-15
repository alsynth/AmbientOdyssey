# Pinnacle gate — grant-chain proof and source fix (15 October 2026)

**Result:** In R4, Apotheosis Pinnacle **cannot be earned in normal play**. The only route is an operator running `/advancement grant … apotheosis:progression/pinnacle`. Source fix removes the gate so the native Apotheosis requirement applies again. Status: **SOURCE IMPLEMENTED + STATIC TEST PASS**. Not packaged, not engine-tested, not multiplayer-tested.

## Evidence (R4 ZIP SHA256 `31b037a7…6c6d`, installed Apotheosis 8.9.0 = R4 pin)

| Source | What it says |
|---|---|
| R4 `overrides/config/paxi/datapacks/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json` (SHA256 `9de71607…2bad`) | Replaces all criteria with one `strong_t6: minecraft:impossible`. Text: "Defeat the Dead King or the experimental alternate Kobolediator to unlock Pinnacle." |
| Native `Apotheosis-1.21.1-8.9.0.jar` → `data/apotheosis/advancement/progression/pinnacle.json` | Requires epic+ affixed helm, chest, legs, feet, hand (`apotheosis:equipped_item`) **and** `kill_ender_dragon`. Same pattern as haven → frontier → ascent → summit. |
| Native `Apoth$Advancements.class` | World Tier unlocks are keyed to `progression/haven…pinnacle` advancements. |
| R4 campaign 0.3.2 JAR (SHA256 `802461a6…39b7`) | No class or resource references `progression/pinnacle`, `PINNACLE` or `getUnlockAdvancement`. `grant()` is only called for `ao_campaign:milestones/*`. |
| Campaign source `AOCampaign.java` | Comment: "native World Tier unlocks remain authoritative." Unused `import …tiers.WorldTier` left over. |
| Other 9 R4 custom JARs, all 330 installed CF mod JARs, all R4 config/quest files | No override of, or reference to, `apotheosis:progression/pinnacle`. Only R4 config file containing `minecraft:impossible` is the gate itself. |

## History (why it broke)
1. `ed1a299` (PR57, 14 Oct) added **both** the Paxi gate and a code grant: on a T6 boss kill, `AOCampaign` awarded `WorldTier.PINNACLE.getUnlockAdvancement()`.
2. `01c2c58` (15 Oct) removed the code grant per the owner decision (native unlocks authoritative), but **left the Paxi gate**. R2, R3 and R4 all shipped it.

Grant chain in R4: **none.** `minecraft:impossible` is satisfied only by `/advancement grant` (operator) or code; no code grants it.

## Intent check
- Superseded intent: `docs/balance/V050_BOSS_ROSTER_AND_GATES_PROVISIONAL.md`, `V050_LOOT_GEAR_ECONOMY_PROVISIONAL.md`, `docs/questing/V050_QUEST_CAMPAIGN_BLUEPRINT_PROVISIONAL.md` (13 Oct, "provisional") describe a strong-T6 Pinnacle unlock.
- Binding latest: canonical handoff §5 item 11 ("PR57 automated Pinnacle unlocking … superseded/disabled. Do not restore"), §4 Gems row ("no … automatic Pinnacle unlock in R3/R4"), R2–R4 package notes ("Pinnacle auto-unlock … removed"), and the owner instruction of 15 Oct: native Apotheosis unlocks stay in charge.
- So the gate contradicts the latest decision. It is not intentional in R4.

## Fix (this branch)
- Deleted `release_030/experimental_overlays/v050/overrides/config/paxi/datapacks/ao_campaign_gates/` (2 files). The overlay copy loop in `tools/package_ao_full_pr54.py` now copies no Paxi pack from that overlay.
- Added both paths to `docs/handoffs/integration-20261015/removed-source-paths.json`, so `tools/package_master_integration.py` also pops them from any inherited payload.
- New `tests/test_no_impossible_tier_gates.py` (5 tests):
  - No source overrides `apotheosis:progression/*`.
  - Every advancement with `minecraft:impossible` must be granted in `AOCampaign.java`; the 9 campaign milestones pass.
  - The campaign doesn't use `WorldTier.`/`getUnlockAdvancement`.
  - The gate files are gone and recorded as removed.
- Other gates checked: the 9 `ao_campaign:milestones/*` files use `minecraft:impossible` **intentionally**. Each is granted by code: `tier_<n>` and `tyros`/`scylla`/`obsidilith` on a boss kill, `heirloom_upgrade` by `/ao_mastery upgrade`. No other gate file exists.

## Rollback (exact)
`git revert <this commit>`, or restore the two files byte-exact from `3806fa1`:
- `…/ao_campaign_gates/pack.mcmeta` SHA256 `df2d65815abd6c30dbb3cd632e5a638581e3c5655eb3f1965222efea9027603c`
- `…/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json` SHA256 `9de71607ca79fd3e063ed1c48b6b0982dda48a1642a7b54a4123a685ea562bad`

and remove the two added lines from `removed-source-paths.json`. R4 ZIP itself is unchanged.

## Remaining
- **Engine test:** in a fresh world from the next build, confirm `/advancement` shows native Pinnacle criteria and that equipping five epic affixed pieces plus a dragon kill unlocks the Pinnacle World Tier.
- **R5 packager:** `tools/package_r5_grand_from_r4.py` copies all R4 bytes except the campaign JAR and manifest, so an R5 built with it would still contain the gate. It needs an owner OK to drop these two members there too.
- The unused `WorldTier` import can be removed at the next real Java build. It was left untouched because nothing can be compiled here (no Gradle).
