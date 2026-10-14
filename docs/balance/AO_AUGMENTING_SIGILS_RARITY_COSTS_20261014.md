# AO rarity-priced Augmenting Table Sigils — experimental port integration

Owner approval (14 October 2026). Minecraft 1.21.1, NeoForge 21.1.252, Apotheosis 8.9.0. Source module at `addons/ao-augmenting-sigils/`.

| Rarity | Sigils: Reroll | Sigils: Upgrade |
| --- | ---: | ---: |
| Common, Uncommon, Rare, Epic, Mythic | **1** | **2** |
| Ancient | **6** | **12** |
| Artifact | **18** | **36** |
| Heirloom | **24** | **48** |
| Esoteric | **32** | **64** |

*No change to Augmenting Table XP costs:* reroll 175 levels and upgrade 225 levels. No change to the effects of reroll/upgrade, gem costs, salvaging, forging, World Tier rarity rolls, affix drops, or boss loot.

## How it works

- `SigilCosts` gets the item's **actual Apotheosis rarity data component**, not display-name text or number of affixes.
- Prototype port rarity IDs accepted: `apotheosis:ancient`, `apotheotic_additions:artifact`, `apotheotic_additions:heirloom`, `apotheotic_additions:esoteric`, and `ao_apotheotic_port` namespace alternatives for the latter three. Confirm the installed **exact r19 custom JAR** actual IDs before acceptance, since the port source JAR is not checked into GitHub.
- Common to Mythic and unrecognized/custom rarity IDs fall back to Apocalypse's existing synced config values (1/2).
- One server-side NeoForge Mixin substitutes the per-item values in both `AugmentingMenu.clickMenuButton` (actual charge) and `hasUpgradeCost()/hasRerollCost()` (affordability checks).
- One client-side Mixin changes both hover tooltip Sigil costs so 32/64 prices are visible and shown unaffordable when the player has too few.
- No custom packets or extra slots are introduced. Apotheosis's `apotheosis:sigil_of_enhancement` is a standard stack of 64; the maximum Esoteric upgrade cost is exactly one stack, so the existing single Sigil input slot suffices.
- Original XP check/consumption stays in untouched native code.
- Creative mode remains free, as Apotheosis currently implements it.

## Required validation

1. Gradle Java 21 compile & build of addon against pinned Apotheosis 8.9.0; package a clean production JAR and exclude `AOAugmentingGameTests.class`.
2. Native server GameTests: exact five-tier cost maps, unknown/custom defaults, single 64-Sigil stack accepted, 175/225 XP costs untouched, and successful loading of server Mixin target.
3. **Client UI test:** Inspect the actual Augmenting Table with Ancient/Artifact/Heirloom/Esoteric items and confirm both tooltips, cost colors and button states, including 63 vs 64 Sigils for the Esoteric upgrade. No test of UI on the dedicated server is a substitute for this.
4. **Server security test:** With 1 Sigil, a client must be refused 32-Sigil Esoteric rerolls; at 32 it must consume exactly 32. With 63 vs 64 Sigils, an Esoteric upgrade must reject and then consume exactly 64.
5. Retest every rarity with more than one affix to prevent paying for the wrong affix or repeatedly upgrading beyond native cap.
6. Verify `Apoth.Components.RARITY` keys from **the specific r19 AO Apotheotic prototype** and adjust aliases if its registry differs. Verify normal Common–Mythic vanilla behavior and individual sigil XP costs.
7. Do not import the addon into a release profile until compiled, client-tested and a fresh dedicated-server test has passed.

Source is isolated on `experimental/apotheosis-augmenting-sigil-costs-20261014` above draft #53, which itself is above #51. **Do not silently mix into Work's previously constructed full import**; this adds a *new* ninth custom mod if using the previous PR #51 base (physical mods 339→340). No PR merged.
