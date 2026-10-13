# AO starting Bonus Chest — approved contents and implementation gates

Status: **approved specification; not yet deployed**, 14 October 2026. The dedicated chest is vanilla `minecraft:chests/spawn_bonus_chest` (optional world-creation Bonus Chest), not every structure chest.

## Exactly four guaranteed categories per player
1. **One random Enigmatic Legacy Spellstone**, uniform 20% among *Blazing Core*, *Heart of the Golem*, *Will of the Ocean*, *Angel's Blessing*, *Lost Engine*. Use the installed JAR's exact registered item IDs; do not infer these from display names. Do not permit another Spellstone to enter via the chest's vanilla pools.
2. **One genuine Apotheosis affix-bearing item**, random rarity Common 55% / Uncommon 30% / Rare 15%. Item must bear real Apotheosis rarity and rolled affix components. Verify installed v8.9+/port rarity IDs and use loot creation hook, not a cosmetic tooltip or an un-affixed vanilla item. Eligible armor retains the AO random trim behavior.
3. **32–48 torches** randomized independently.
4. **16–48 cooked meat**, choosing from cooked beef, porkchop, chicken or mutton.

Each player has **independent Lootr rolls**, never identical predetermined chest contents. The vanilla Bonus Chest's Lootr conversion is **not yet validated** on the exact installed profile. Test two non-operator clients and dedicated server + rejoin with Bonus Chest enabled. The chest is optional, no mandatory item or quest gate should depend on its contents.

## Implementation
- Preserve early/midgame standard mod chest generation untouched.
- Verify exactly five Spellstone resource IDs in the installed Enigmatic Legacy JAR and ensure Lost Engine is an actual item in that version.
- Verify Apotheosis loot controller API + correct loaded World Tier level / rarities. Ensure startup can provide an affix item independent of later World Tier unlocks; do not give a fake rarity.
- Use an exact-path Paxi datapack override for only `data/minecraft/loot_table/chests/spawn_bonus_chest.json` when every category works. Do not ship a partial table that omits the Spellstone or affix.
- Vanilla torches and cooked meat can use `minecraft:set_count` with `uniform` range (32,48) and (16,48), respectively. Serialize as one loot pool each with guaranteed roll and meat candidates each of equal weight.
- Check potential conflict between Lootr re-rolling and chest table override, and verify 1.21.1 format/priority.
- Sample at least 100 generated rolls to check each guaranteed category, rarity proportions and absence of empty/invalid stacks. 100 rolls are a smoke sample, not statistical certification.
- Test 5–7 player loot without duplicate single-roll behavior. Existing approved policy: `docs/audits/STARTING_BONUS_CHEST_LOOT_POLICY_2026-10-10.md`.

## Other economy approvals
- Goblin Tuned chainmail: 32 diamonds + 4 `irons_spellbooks:cinder_essence` per piece, preserve modifiers and offer rarity. Stage native trader JSON edit only after its pinned offer JSON is extracted; no guessed trade payloads.
- Flight Ring recipes are independently implemented in this draft: basic diamond -> Nether Star; advanced requires Iron's Spellbooks Cinder Essence + Arcane Ingots and Ars Nouveau Air Essence; validate installed JAR registries and JEI on runtime.
- Rage Glove: gate behind an unselected Tier 7 Nether boss; do not change until boss chosen and existing loot sources enumerated.

## Non-goals
- No broad early/midgame loot overhaul.
- No mobility rebalance beyond explicitly approved Flight Ring recipes.
- No Infinitium or Cursed Ring edits.
- No merge to main.
