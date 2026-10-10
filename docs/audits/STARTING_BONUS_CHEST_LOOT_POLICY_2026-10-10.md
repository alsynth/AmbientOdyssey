# Ambient Odyssey — Bonus Chest / Starting Loot Policy

**Decision: 10 October 2026. Status: approved design direction; not yet implemented/tested.**
**Specific chest:** Minecraft Java's **optional world-creation Bonus Chest** (the toggle in Create World), **not** an arbitrary structure chest and **not** assumed to be a per-player placed starter chest.

## User decision — supersedes earlier excessive conservatism

- **A valuable starting loot pool is desirable and acceptable.** The earlier worry that the first player could empty a single shared starter chest was based on treating the Bonus Chest as an ordinary shared container.
- Ambient Odyssey uses **Lootr**, whose instanced loot grants each player their **own roll when opening a compatible converted loot container**. A party of 5–7 should each have an opportunity to open the spawn Bonus Chest rather than compete for one set of starter items.
- **Do not constrain the Bonus Chest to only tiny amounts of food, wooden tools and torches** merely to avoid first-arrival unfairness. Meaningfully helpful equipment, useful modded expedition supplies, and exciting rare rolls are on the table. User is comfortable with a substantial start.
- A personal Lootr roll **does not imply everyone receives identical contents**. To achieve consistent fairness, distinguish a modest guaranteed base kit (if desired) from probabilistic valuable extras; choose/implement the actual table later.
- **No item whitelist or specific numerical reward rate approved yet.** Proposed starter equipment, rarity bands and balance constraints must be curated when the final progression is established. Avoid adding hard bans on spellbooks/accessories/rare finds based on the outdated first-player argument.
- Lootr's *instanced distribution* solves shared-chest scarcity, **but does not eliminate progression/economy balancing:** 5–7 players each receiving a valuable item increases the amount of material/gear entering the server, and starter items should remain exciting without completely replacing the first several dungeon rewards.
- This chest is **optional** for world creation. Players choosing a no-Bonus-Chest world should still be able to progress normally; don't make a quest or recipe require a chest-only item.

## Technical verification gate (not yet proven for AO)

**Minecraft's vanilla Bonus Chest uses the loot table `minecraft:chests/spawn_bonus_chest`.** Vanilla creation places **one** physical chest near world spawn (not one chest per player). Lootr converts compatible **loot-table-bearing** containers and offers each player an independent inventory roll. However, the *vanilla world-creation Bonus Chest's actual Lootr conversion path has not been demonstrated in AO's exact 1.21.1 NeoForge instance*. Worldgen timing, Lootr configs, already-opened ordinary chests and spawn protection can affect the experience.

1. On a **disposable new world** with **Bonus Chest = ON**, check whether the spawn container has become the recognizable Lootr chest before anyone opens it. Never rely on a world already generated with Bonus Chest disabled.
2. With **two non-operator players**, have player A open and take everything, then player B open the **same physical chest**. Both should have independent loot and the chest must remain accessible. Check spawn protection and player permissions.
3. Verify loot is generated from the *overridden* `minecraft:chests/spawn_bonus_chest` table and that two players can receive different randomized items without consuming each other's rolls; test rejoin and late join.
4. Repeat on the future dedicated server's **actual worldgen/startup path**, since the optional world-creation control and server setup differ. The Lootr item/loot-table and converted-entity state must persist across restart.
5. If natural Bonus Chest conversion fails, **do not silently assume Lootr is working**. Check config and source; a user-approved fallback is possible with a deliberately placed Lootr custom container at spawn using `/lootr custom`, which duplicates prefilled contents individually. **This is a separate implementation** from rewriting the world-creation Bonus Chest and requires explicit admin setup and spawn-protection checks.
6. Inspect existing/added loot-table datapacks in `release_030/overrides` and future KubeJS/Paxi pack. Implement the final pool in the correct **1.21.1** data-pack format and test no config/namespace precedence conflict.
7. **No active build, Bonus Chest loot JSON or loot distribution changed yet.**

## Reward-policy compatibility

- The Bonus Chest is a **welcoming gift**, not a Questlog quest or FTB lesson reward. It can feature a stronger or rarer opening reward than an ordinary trivial tutorial task.
- Since quests will eventually offer hundreds of additional rewards, assess *combined* early-game supplies across Lootr Bonus Chest, first Questlog quests, other Lootr structure chests, starting Origins passives, and accessible dungeon loot.
- Keep distinct: starting loot pool generosity is **approved**; *working automatic per-player Bonus Chest conversion* is a **technical hypothesis to test**.
- Content ideas and balance can be revised after the major AO content expansion; no premature chest pool finalized.

## Supporting public documentation

- Official Lootr Minecraft Forge/NeoForge description: https://www.curseforge.com/minecraft/mc-mods/lootr
- Official Lootr Modrinth FAQ and per-player loot-table semantics: https://modrinth.com/mod/lootr
- Official Lootr starter custom chest instructions: https://github.com/LootrMinecraft/Lootr/wiki/FAQs
- Custom-container command guidance for 1.21.1 branch: https://github.com/LootrMinecraft/Lootr/wiki/Custom-Containers-and-Maps
- Vanilla spawn Bonus Chest loot table: `minecraft:chests/spawn_bonus_chest` / Minecraft Wiki Bonus Chest page: https://minecraft.wiki/w/Bonus_Chest

**Bottom line:** Treat the chest as a **valuable per-player starter reward provided that Lootr conversion is verified**, and remove shared-container scarcity as an argument against worthwhile contents.
