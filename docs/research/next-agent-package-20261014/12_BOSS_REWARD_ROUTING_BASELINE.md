# Boss rewards: baseline for the loot and reward economy (14 October 2026)

**Status:** research notes, no game changes. Sources: branches `experimental/loot-economy-first-pass-20261013`, `research/rpg-boss-loot-campaign-design-20261013`, `experimental/apotheosis-world-tier-rarity-20261014`, `experimental/v046-wetsand-apotheotic-ports-20261011`, the Apotheosis 1.21 source (`AffixLootModifier`, `LootRarity`) and the instance log (`ao-apotheotic-port-prototype-0.4.8-prototype.jar` is installed).

## Already decided or built by other workstreams (do not redo)
- Owner-approved Apotheosis World Tier rarity weights for Common to Mythic (isolated datapack, not merged), and the starter chest, flight ring and Goblin-Tuned changes of the first loot pass.
- Design rules (provisional register D08, D09, D13, D14, D22): boss-specific rewards are **authored per encounter**, never rolled from ordinary chests; first clear is a per-player quest milestone plus the boss's native drops; boss tier and structure tier are separate; gem ladder `Perfect < Ancient < Artifact < Heirloom < Esoteric` is a different thing from affix rarities.

## What blocks the Tier 6 to 9 reward targets as written
1. **The high grades are a prototype.** The installed Apotheotic port keeps Artifact, Heirloom and Esoteric, but only 25 of 118 attribute affixes and 5 of 71 gems are active; **natural drop weights are zero**; gem cutting does not support the three upper tiers; "bosses, loot, recipes/reforging/trades remain pending".
2. **Native Apotheosis loot injection never reaches boss kills.** Its modifiers (`apotheosis:affix_loot`, `apotheosis:gems`, `apotheosis:affix_conversion`) match the **loot-table id by regex**; the shipped patterns are `chests.*` and similar, while a boss kill uses an entity table. Only `affix_conversion` (pattern `.*`, 35%) can turn gear that a boss already drops into an affix item.
3. **A boss-specific entry is possible in data, but one point is unverified.** An `AffixLootModifier` entry takes a table pattern, a chance, an optional pool of affix entries and an optional set of **rarities** that overrides the rarity choice. Whether a rarity whose weight is zero in every tier can be selected that way depends on Placebo's weighted selection (not read yet). If it cannot, forcing Artifact or above needs small custom code or a boss-only non-zero weight.

## Open dependencies on boss decisions
- Rage Glove: reserved as a rare reward of a **Tier 7 Nether boss**, still to be named (proposal: `cataclysm:netherite_monstrosity`, which is on the handoff's Tier 7 list; owner to confirm).
- Third Tier 9 boss and Geburah's tier stay unassigned (D03, D04).

## Next steps (in this order)
1. Read Placebo's selection to settle point 3; read the port's rarity JSON.
2. Map each Tier 6 to 9 boss to its loot route (entity loot table overridable by datapack, loot modifier, or mod config) from the capability catalogue.
3. Draft a reward table in **expected kills per drop** for owner approval (no numbers are approved yet).
4. Only then build a reversible reward datapack, enabling only the grades the port can really support.
