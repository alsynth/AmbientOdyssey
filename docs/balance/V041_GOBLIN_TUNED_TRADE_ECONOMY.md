# Ambient Odyssey — Goblin Traders item-economy investigation
**Date:** 11 October 2026 · **Status:** researched, awaiting actual loot economy review; **no live trade change yet**.

## Confirmed actual NeoForge 1.21.1 trade implementation
Sources: [GoblinTradeProvider.java](https://github.com/MrCrayfish/GoblinTraders/blob/multiloader/1.21.1/common/src/main/java/com/mrcrayfish/goblintraders/datagen/GoblinTradeProvider.java), [TradeManager.java](https://github.com/MrCrayfish/GoblinTraders/blob/multiloader/1.21.1/common/src/main/java/com/mrcrayfish/goblintraders/trades/TradeManager.java), [BasicTrade.java](https://github.com/MrCrayfish/GoblinTraders/blob/multiloader/1.21.1/common/src/main/java/com/mrcrayfish/goblintraders/trades/type/BasicTrade.java), [EntityTrades.java](https://github.com/MrCrayfish/GoblinTraders/blob/multiloader/1.21.1/common/src/main/java/com/mrcrayfish/goblintraders/trades/EntityTrades.java).

- Goblin-Tuned armor adds `minecraft:generic.armor` modifier **+0.5 ADD_MULTIPLIED_BASE** (`goblintraders:goblins_armour`) to the equipped item slot. This is *not* directly identical to “50% damage reduction”; armor reduction math and other sets matter.
- `durable()` changes `minecraft:max_damage` to **10× normal durability**; `tuned()` itself writes rarity/lore.
- Overworld Goblin Trader's **epic** armor trades: tuned chainmail helmet, chestplate, leggings, boots, each **1–3 iron ingots + 6–14 emeralds**, `max_trades=1` per generated offer.
- Vein Goblin Trader's **legendary** armor trades: tuned netherite helmet, chestplate, leggings, boots, each **2 Nether Stars + 1 Dragon Head**, `max_trades=1`.
- Specific Netherite helmet/boots also have special effects; preserving the original output item components is critical.
- Diamond tuned tools in overworld legendary category cost **1 Nether Star + 1 Dragon Head** and offer unique reach/mining/attack attributes.
- Goblin-Trader config `goblintraders-entities.toml` tunes spawning, rarity probability, number of offers and restocking, **not the actual payment amounts**.

## Recommended future loot-balancing policy (proposal only)
**Keep Goblin-Tuned gear as a prestigious alternative item path, do not nerf the +50% armor modifier just to make the economy work.** Focus primarily on chainmail's unexpectedly low entry price and durability.

- Chainmail: **trial suggestion 4–8 diamonds + 16–32 emeralds** per piece (replacing 1–3 iron + 6–14 emeralds), no trade-spam loops, max one per offer. These quantities are provisional, not approved nor deployed; verify how much diamond/emerald players obtain after T2–T3 dungeons.
- Netherite: **keep 2 Nether Stars + 1 Dragon Head until boss/drop economy is measured**; 2 Nether Stars may be plentiful if Wither farmable or expensive if Wither currently a tier-gated challenge. If too cheap in practice, raise star cost or add an uncraftable dungeon trophy as secondary item **only if exchange schema supports two payment item slots**. The mod currently supports exactly two direct cost entries, so a “trade-in item plus stars plus head” would require two-stage voucher mechanics or a custom addon.
- Keep rare/legendary presentation meaningful; limit rerolls and restocking exploits if repeated offers flood the economy.
- Compare against Apotheosis affix bonuses, smithing upgrades, armor caps and boss time-to-kill. Do not stack Dungeon Difficulty's automatic item scaling on these components (balance pilot explicitly disables it).
- Cross-test reported upstream armor refresh anomalies: [equipment swap bug #124](https://github.com/MrCrayfish/GoblinTraders/issues/124), [smithing upgrade bug #119](https://github.com/MrCrayfish/GoblinTraders/issues/119). Read the active version's code first; do not assume upstream fixed these.

## Correct no-code implementation route once economy prices are approved
- Use **server-side datapack trade overrides**, not an entity spawn config.
- For the original 1.21.1 trade system, native trade resources are loaded from `data/goblintraders/goblin_trades/<goblin_trader|vein_goblin_trader>/<epic|legendary>.json`. On original trade categories, preserve all original `trades` entries and `offer_item` components; edit **only** the target `payment_item` / `secondary_payment_item` price ranges and perhaps `max_trades`. Load an exact-path resource replacement at higher pack priority.
- The `GoblinTradeProvider` generator describes original prices and output custom attributes; **DO NOT recreate tuned armor as a bare vanilla ItemStack** or the armor bonus and 10× durability will disappear.
- Trade JSON uses `goblintraders:basic` with `offer_item`, `payment_item`, `secondary_payment_item` (optional), `price_multiplier`, `max_trades`, `experience`. Costs use `id`, `count` as a constant or `{min,max}`, optional `components`. Items use 1.21.1 data-components codec.
- Reload and verify both traders' complete offer lists with already-spawned *and freshly spawned* goblins, and check one-per-offer behavior. No claim that a new datapack retroactively updates existing selected merchant offers.
- Do not rely on outdated pre-1.20.5 trade datapack examples. [Upstream #127](https://github.com/MrCrayfish/GoblinTraders/issues/127) documents this exact migration issue.
