# v0.4.6 gem-tier source review (UNBUILT, UNRUN)

Branch `experimental/v046-gem-tier-source-review-20261012`, from `4ed1429`.
Reviewed against Apotheosis 1.21 branch `802ce7a` (source, not the 8.9.0 binary).
**Nothing here was compiled or run**: the review sandbox cannot reach
`maven.neoforged.net`. Only a javac syntax-level parse of the three edited files
was done. Treat every behavioral claim about the port as unverified until the
local plan below passes. No subsystem is complete; no drops were enabled; no
CurseForge build was produced; stock gems/rarities/recipes were not touched.

## Mapping assumed (unchanged)
Tiers 0..4 = native purities CRACKED..FLAWLESS; tiers 5..8 (Ancient, Artifact,
Heirloom, Esoteric) all back onto native PERFECT, separated by the
`legacy_gem_tier` component. All nine tiers are preserved.

## Findings (from stock source)
| # | Finding | Stock evidence | Status |
|---|---|---|---|
| F1 | `UnsocketedGem.equals` is `final` and compares gem + purity only, so Artifact/Heirloom/Esoteric stacks of one gem are "equal". It cannot be overridden. | `UnsocketedGem.java` equals/hashCode | Characterized by a new test; mitigated, not changeable |
| F2 | `PurityUpgradeRecipe` rejects PERFECT bases (`isValidBaseItem`), so stock cutting cannot upgrade or merge upper tiers through equality. Safe as long as upper tiers stay PERFECT. | `PurityUpgradeRecipe.java` | OK by source; needs in-game confirm |
| F3 | Stale-data bug in the prior checkpoint: `toLegacyStack` put the component and a literal tier name on tiers 0..4. A stock upgrade copies the stack and bumps purity, leaving e.g. component 4 on a PERFECT stack, so it kept the Mythic value and a "mythic" name. | `PurityUpgradeRecipe.assemble` copies base | **Fixed in source (unrun)**: only tiers 5..8 get component/name |
| F4 | `createModifier` threw `IllegalArgumentException` for an unsupported exact tier (e.g. /give with component 8 on a gem lacking tier 8). It runs in attribute events and tooltips, so a crash path. | `AttributeBonus.addModifiers`/tooltip call it | **Fixed (unrun)**: fail closed to a 0.0 modifier |
| F5 | Component/purity mismatch could escalate (component 8 on a FLAWLESS stack). | n/a | **Fixed (unrun)**: purity is the ceiling; component only honored on PERFECT with value 5..8 |
| F6 | `GemCaseTile` stores `EnumMap<Purity,Integer>` per gem; depositing an upper-tier stack collapses it to PERFECT and extraction yields a stock Ancient-equivalent. Tier loss (downgrade). | `GemCaseTile.depositGem/extractGem` | **OPEN**, needs a design decision |
| F7 | `GemIngredient.test` matches by purity only, so any recipe asking for a Perfect gem accepts Artifact/Heirloom/Esoteric and consumes them. | `GemIngredient.test` | **OPEN**, needs a design decision |
| F8 | Missing-component fallback: PERFECT with no component resolves to Ancient if supported, else the lowest supported upper tier. Kept as-is, now centralized in `LegacyGem.resolveTier`. Display name for such stacks is the stock "Perfect" name. | `LegacyGem.resolveTier` | Needs production design review |

## Code changes (all unbuilt)
- `LegacyGem`: `resolveTier(stack, purity, supports)` (never escalates, never throws); component and custom name only for tiers 5..8; `tier()` deprecated.
- `LegacyAttributeBonus.createModifier`: uses `resolveTier`; invalid gives a 0.0 modifier.
- `ApotheoticGemGameTests`: first test now expects no component below tier 5; added `tierResolutionFailsClosedAndNeverEscalates` and `stockUnsocketedEqualityIgnoresUpperTierComponent`.
- `build.gradle`: required GameTest count 9 -> 11 (message updated). **If local runs show a different total, fix the count, never loosen the log check.**

## Open design decisions (not implemented)
1. F6, options: (a) block deposit of tiered stacks via a server-side event/capability guard if one exists in 8.9.0 (unverified); (b) a port-owned tier-aware case; (c) accept downgrade and document. Prefer (a) or (b); verify the 8.9.0 binary, not only the 1.21 source.
2. F7, options: a port ingredient type matching exact tier for upper-tier recipes, and leave stock PERFECT recipes alone vs. also excluding component-bearing stacks (the latter changes stock behavior, so needs explicit approval).
3. Dedicated upper-tier upgrade recipe (Ancient->Artifact->Heirloom->Esoteric): must preserve the exact component and original costs.
4. Upper-tier display names: stock `getName` uses purity (shows Perfect); the custom name is a literal English prefix. Needs lang keys and a stable approach (custom-name staleness on rename/anvil).
5. Esoteric acquisition path stays restricted; do not add natural weights.

## Local verification plan (run in order on the Windows workspace)
Prereqs from the handoff: `CI=true`, Gradle 9.2.1, Java 21.
1. `gradle -p ports/apotheotic-additions/neoforge build runGameTestServer --console=plain`.
   Pass = fresh log `All 11 required tests passed :)`. Triage compile errors first
   (never compiled): `IntPredicate` method ref `bonus::supportsTier`, `OptionalInt` use,
   `ItemStack.has/get`.
2. If GameTest 1 fails for tiers < 5, check `GemItem.setPurity` and `toStack` behavior.
3. Wet Sand module unaffected; rerun its build only to confirm CI parity.
4. Manual, in a copied profile with the prototype JAR: `/give` a gem with
   `legacy_gem_tier` 8 on a gem lacking tier 8 (expect no crash, 0 bonus, tooltip OK);
   socket an Artifact then Heirloom of one unique gem (expect rejection);
   upgrade a FLAWLESS gem at the gem-cutting table and check bonus/name now Ancient/Perfect;
   deposit an Esoteric gem in a Gem Case and record the tier it returns (confirms F6);
   craft with an upper-tier gem in a Perfect-gem recipe (confirms F7).
5. Save/restart round trip with sockets of each upper tier.
6. Record logs under `docs/testing/v046-evidence/` and update the status table only with real results.

## Not run / not established
Compilation, all GameTests, F2 in-game confirmation, F6/F7 reproduction, the 8.9.0 binary
(vs. 1.21 source) equality behavior, client tooltip/naming, and dedicated server.

## 12 October local verification follow-up (supersedes UNBUILT status above)

Imported Claude format-patch 74e170adefd136cb722a4156c211974dcb13415a on isolated
branch experimental/v046-gem-tier-local-verification-20261012. Original patch
compilation and all 11 tests PASS against actual Apotheosis 8.9.0, Placebo 9.9.2,
Apothic Attributes 2.11.0 and NeoForge 21.1.252 binaries.

Review found two additional verification/implementation gaps and addressed them:
- The unsupported-modifier test used Hearty, which supports tier 7, and only
  checked non-null. It now uses an actual restricted LegacyAttributeBonus and
  requires zero amount for unsupported tier 7, with supported FLAWLESS amount
  2.5 also asserted.
- Native GemView clamps upper-only gems to minimum PERFECT. Checking only the
  view purity could still honor a malicious upper component on a raw FLAWLESS
  stack. resolveTier now takes the lower of supplied view and actual stored
  GemItem purity. A malformed Warden stack is tested to return zero.

Tests now invoke the installed stock PurityUpgradeRecipe assembly: FLAWLESS
Hearty becomes PERFECT/Ancient +3, without stale component/custom name. The stock
base validator rejects an Esoteric upgrade base. UnsocketedGem equality and
PurityUpgradeRecipe behavior were also inspected directly in the 8.9.0 bytecode.

Added one separate native characterization test, so the required count is now
12 (the strict freshness/pass check remains). The test places a real native
Gem Case, deposits Esoteric Hearty, and extracts it without the legacy component,
with Ancient +3 instead of Esoteric +5. It also confirms native GemIngredient
PERFECT accepts an Esoteric stack. These are reproduced UNRESOLVED hazards,
not successful compatibility or fixes; upper-tier storage/recipes block release.

Final compilation + all 12 required native tests PASS; no data ERROR observed.
Evidence: docs/testing/v046-evidence/apotheotic-twelve-gem-tier-patch-gametests.log.
Tested JAR SHA-256:
435dae1208b54850081c667bfe56118157cd01615ee2ef383a36fddc76cdc15d.
Client presentation, live UI interactions and complete pack compatibility were
not rerun for this patch. No drops enabled, no CurseForge test ZIP, no live
profile or v0.4.5/main edits. CI includes this verification branch but its remote
result must be checked separately after push.
