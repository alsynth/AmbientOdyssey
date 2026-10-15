# Proposal: package campaign 0.3.3 (15 October 2026)

**Result:** proposal only, no tool changed. Campaign 0.3.3 (Simply Swords full pool, `2067e4a`) can't be packaged today: five tools hard-code 0.3.2. Recommended: keep R5 as the 0.3.2 Grand-only patch, then ship 0.3.3 in a separate full build (R6). This follows handoff rule 10.3 ("never mix R5 with the Simply Swords rewrite").

## Where 0.3.2 is hard-coded

| File | What it pins | Why it matters |
|---|---|---|
| `tools/package_master_integration.py:15,24,29` | Builds from `ao-campaign-0.3.2-experimental.jar` and refuses other metadata | The full-build path; it must accept 0.3.3 |
| `tools/validate_master_integration.py:32` | Asserts the packaged campaign file name is 0.3.2 | Would fail any 0.3.3 import |
| `tools/patch_r5_grand_from_r4.py:22,110` | Patches R4's compiled 0.3.2 JAR (resources only) | Correct as is: R5 must start from R4's exact JAR |
| `tools/package_r5_grand_from_r4.py:23` | R4 campaign path | Correct as is, same reason |
| `tools/log-probe/build.gradle:8` | Test probe compiles against 0.3.2 | Test-only; never shipped |

## Why R5's patch path can't carry 0.3.3
- R5 changes only `ao_loot_policy.json` inside R4's compiled JAR.
- 0.3.3 changes Java code (`BossRewards.swordPoolIds()`) and adds `ao_sword_pool.json`, so it needs a real Gradle build.
- The R5 tools check R4's JAR SHA and 0.3.2 identity, so they correctly refuse 0.3.3.

## Proposed change (for the R6 full build)
1. **One version source:** read the campaign version from `addons/ao-campaign/build.gradle` and check it matches `neoforge.mods.toml`. Use it in `package_master_integration.py` and `validate_master_integration.py`, replacing the hard-coded `0.3.2`.
2. **Keep the guards:** fresh build only, no stale `ao-campaign-*.jar` in `build/libs`, exactly one campaign JAR, 10 custom JARs, required classes present. For 0.3.3, also require `ao_sword_pool.json`, with a pool count equal to the source file (133 now).
3. **Same mod ID:** `ao_campaign` doesn't change, so existing worlds still load. The file name changes, so the rollback receipt must remove `ao-campaign-0.3.3-experimental.jar` and restore the 0.3.2 file.
4. **Carry the R5 Grand decisions into source:** once you approve the five R5 pools, apply the same five indices to the source `ao_loot_policy.json`, so R6 doesn't drop them. Hash-check the result against the R5 patched policy.
5. **Carry the Pinnacle gate:** R6 must include the Cornelia gate (`feature/pinnacle-cornelia`). The new impossible-gate check in `package_r5_grand_from_r4.py` (`feature/r5-gate-safeguard`) should also run in `validate_master_integration.py`.
6. **Leave the R5 tools pinned to 0.3.2.**

## Order
1. R5: Grand five pools (0.3.2 patch) + Pinnacle gate. Needs your pool approvals and the Grand audit.
2. Simply Swords decisions: the 17 routes (`UNIQUE_ROUTES_17.md`), the 53 candidates, Simply More.
3. R6: apply steps 1–5 above, run a Gradle build, package, validate, then engine and two-player tests.

## Decision needed from you
- Approve the R5 → R6 split, or choose a single combined 0.3.3 build (that would retire the R5 patch path).
