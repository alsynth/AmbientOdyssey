# AO Starter Bonus Chest — Experimental source module

This source module is **not** automatically installed by the existing CurseForge import. PR #51 is a *draft* and no Minecraft runtime approval is claimed. Build it with `gradle -p addons/ao-starter-chest build`, then install its built JAR in a disposable client + dedicated server profile when CI compiles.

## Intended contents (4 guaranteed categories)
- Exactly one equally weighted `enigmaticlegacyplus` spellstone: `blazing_core`, `golem_heart`, `ocean_stone`, `angel_blessing`, `lost_engine`. Names verified in Enigmatic Legacy Plus registry source (upstream branch main, commit 9093d409).
- One real Apotheosis affix item, selected from early-game weapons/tools/armor; rarity selected as common 55% / uncommon 30% / rare 15% using `LootController.createLootItem`, *not* fake rarity lore.
- 32–48 torches.
- 16–48 of one randomly selected cooked meat (beef/pork/chicken/mutton).

The bundled `minecraft:chests/spawn_bonus_chest` loot table supplies the first, third, and fourth categories. The custom NeoForge global loot modifier supplies the actual affix item, because ordinary vanilla loot JSON cannot guarantee correct Apotheosis-generated affixes at fixed rarity percentages.

Apotheosis's native 1.21 chest-loot modifiers otherwise match the Bonus Chest (`chests.*`), injecting extra affix loot and sometimes gems. AO stages three **first-match, zero-chance Bonus-Chest-only exclusions** under `config/paxi/datapacks/ao_starter_apotheosis_exemptions`: `affix_conversion`, `affix_loot_injection` and `gem_loot_injection`. The remainder of each mod's native data is preserved, and `tools/validate_ao_starter_apotheosis_exemptions.py` compares it with the installed pinned 8.9.0 JAR. This should prevent duplicate random rewards without changing normal dungeon chests, subject to Paxi load-priority verification.

**Critical gates before shipping:**
1. Native Gradle compilation against pinned Apotheosis 8.9.0/NeoForge 21.1.252.
2. Confirm exactly ONE affixed item from each Bonus Chest, despite generic Apotheosis chest-injection modifiers; their execution order is load-order-sensitive. Do not assume the `removeIf` guard is sufficient if another modifier executes after it.
3. Confirm an affixed item is always generated in Haven (not empty) and matches 55/30/15 distribution over many rolls. Confirm the random trim addon applies to eligible affixed armor.
4. Verify that world-creation **Bonus Chest** actually becomes a Lootr individualized container; test two non-operator players and a fresh dedicated server. If the vanilla Bonus Chest bypasses Lootr, choose a deliberately configured replacement container and document admin setup, not silent shared single-use loot.
5. Confirm the world-creation Bonus Chest toggle OFF yields no extra items and other structures' loot remains unchanged.
6. Verify the exact official Enigmatic Legacy Plus JAR version and item registry names in the installed pack.
7. Ensure both standard enchantment/affix loot injection systems do not introduce extra roll categories in the starter chest.
8. Add the tested compiled addon JAR to the full import only *after* acceptance and conflict tests; preserve source and rollback.

The GitHub draft CI runs JSON/static source checks and attempts addon compilation; it does not run Minecraft or assert server/Lootr behavior.
