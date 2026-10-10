# Ambient Odyssey — FTB Field Manual Draft Pages v0.2

**Purpose:** original educational writing for FTB Quests. These are **draft articles, not installed FTB pages**; illustrations, keybinds, exact recipe listings and modded numeric attributes require a final-version game audit. Only Questlog should award gameplay completion rewards for overlapping topics.

## 01. Two Books, Two Purposes

*Newcomers / navigation*

**Adventure Journal (Questlog)** tells you what is happening: which place you discovered, which challenge looks appropriate, and what optional journey has just become available. **Field Manual (FTB Quests)** answers the questions that interrupt an adventure: what an item does, where a spell comes from, how a crafting system works and what a particular button means.

Both books are meant to be browsed, not finished in a strict order. The manual can be opened when a Questlog entry points to a mechanic you have not learned. Reading an explanation should not automatically grant the same reward a player receives for completing the associated adventure.

**Try this:** Find the topic for your current tool or spell, then return to the Adventure Journal.

**Verification before publication:** Exact menu button/keybind needs UI smoke test. FTB page should not duplicate Questlog rewards.

## 02. JEI: Your Recipe Encyclopedia

*Newcomers / items*

An unfamiliar material may be useful long before its purpose is obvious. JEI helps answer two different questions: **How do I craft this?** and **What can I make with it?** That distinction matters with modded components that have dozens of possible recipes.

Use the search bar for a name or ingredient, hover the result to inspect details, and use the recipe and uses actions listed in your controls. Common defaults may be changed by the modpack, so the on-screen controls take priority. Some recipes also require special stations, rituals or progression. A recipe appearing in JEI does not guarantee it is currently accessible.

**Try this:** Inspect a loot item, then look up both one recipe that makes it and one recipe that consumes it.

**Verification before publication:** Confirm JEI version, mouse/keyboard mappings, JEI recipe filters and any disabled recipes in final pack.

## 03. Shield, Off-Hand and Unusual Attacks

*Newcomers / combat*

A shield occupies the off-hand and can prevent damage from many ordinary attacks when raised at the right time. It does not make you invulnerable. Some enemies use magic, area attacks, knockback or attacks whose behavior differs from vanilla Minecraft.

Before a dungeon, practice using your shield against familiar mobs. Check whether your weapon has unusual timing, reach or a special action. If a monster has a telegraphed move, moving out of its path may be safer than standing still and relying on armor.

**Try this:** Block a basic attack safely, then practice moving while keeping your retreat route clear.

**Verification before publication:** Check Better Combat weapon behavior, shields with modded cooldowns and optional tutorial screenshots.

## 04. Equipment Slots and Combat Supports

*Gear / Curios*

Some items work simply by sitting in an equipment slot; others activate on hit, after damage, on movement or when triggered manually. Two objects can both be called accessories without fitting into two usable slots. Always check the actual Curios or other equipment layout rather than assuming that carrying them grants their effects.

AO grades combat-support items by how much they help in a fight, not only by rarity. The early **Tier 2** benchmark is enchanted diamond armor around Protection III plus **two compatible A-grade combat supports**. A powerful Origin passive does not substitute for either item. Some exceptional EX-grade effects still need balance testing.

**Try this:** Compare the effects, cooldowns and occupied slots of two supports in the AO Gear Atlas.

**Verification before publication:** Requires final Curios and Enigmatic slot audit; grade assignments remain provisional.

## 05. Lootr, Shared Loot and Multiplayer Courtesy

*Newcomers / multiplayer*

Some dungeon containers may provide personal loot for each player, while other containers behave as ordinary shared storage. Learn the difference before the first multiplayer expedition. A player reaching a chest first should not automatically mean everybody else loses access—but a personal loot feature must not be assumed for every chest and inventory.

Keep the group informed about especially rare finds, and be cautious around equipment dropped after death. A server may have additional rules for tombstones, claims and borrowed gear; the Field Manual should describe the current AO setup rather than generic defaults.

**Try this:** With a friend, inspect a known personal-loot container and a normal chest to recognize the difference.

**Verification before publication:** Verify Lootr conversion and anti-grief rules on live server.

## 06. Waystones, Maps and Returning Safely

*Navigation*

A map marker helps you remember a place; a Waystone provides another kind of travel convenience when it has been discovered or configured. Neither replaces expedition planning. A portal that leads somewhere unfamiliar may require a different route back, and a waypoint does not guarantee safety at its destination.

Record at least one home marker and label important portals clearly. When a major dungeon is too dangerous, save its location instead of forcing the fight. AO's planned Explorer's Journal will only show or export locations you have genuinely discovered.

**Try this:** Create a clearly named home waypoint and one marker for a distant landmark.

**Verification before publication:** Confirm final Xaero keybinds and Waystones teleport cost/permissions; do not promise an integration API.

## 07. Apotheosis: Affixes, Gems and Sockets

*Advanced equipment*

Apotheosis adds another layer to equipment evaluation beyond its vanilla base type. An item can have special affixes, rarities, sockets or gem-related bonuses. Those modifiers are not interchangeable with ordinary enchantments, and stacking the wrong effects may produce a worse build than choosing two complementary ones.

Inspect each item's complete tooltip before salvaging or reforging it. Ask whether a modifier improves survivability, damage, mobility or a narrower trigger condition. A shiny rarity label is less informative than the actual benefit against an upcoming boss. The AO Gear Atlas will compare results using the installed 1.21.1 Apotheosis configuration.

**Try this:** Compare two items of the same base material but with different affixes and explain why one suits your build better.

**Verification before publication:** Verify Apotheosis 8.9.0 versus final version, gems/purity/socket mechanics and recipes from exact JAR/config; no invented drop rates.

## 08. Apotheosis: Enchanting and Upgrading

*Advanced equipment*

An enchanting setup is more than surrounding a table with generic bookshelves. This modpack may use additional shelf types and several interacting enchanting attributes. The right table configuration depends on whether you are trying to access stronger enchantments, control undesirable ones or use a particular modded item.

The manual should eventually show one **actual AO-tested** setup and explain what every displayed attribute does. Until we verify current configs, avoid copying a maximal build from a different Minecraft version. JEI recipes are the place to confirm which shelves and workstations are actually available.

**Try this:** Review the enchanting screen's attribute labels and locate the manual's tested starter arrangement.

**Verification before publication:** Need exact mod version, UI labels, shelf effects, enchantment power/quality/eterna/arcana/quanta configuration.

## 09. Relics: Effects, Activation and Growth

*Relics / Artifacts*

Relics and Artifacts are not all passive bonuses. Some ask you to press a key, some depend on a cooldown, and some gain functionality or strength through the mod's own leveling or charging rules. A useful passive that triggers constantly can be more valuable than an impressive special ability you seldom remember to activate.

The Field Manual will document each important support's slot, activation method, level behavior and any known conflicts with other equipment. The Adventure Journal should reward using a meaningful relic well—not endlessly collecting every relic in the pack.

**Try this:** Pick one item you own, identify exactly when it helps, and verify it can be equipped in your current layout.

**Verification before publication:** Audit installed Relics 0.10.7.8, More Relics 1.7.7, Artifacts 13.2.5; do not fabricate exact numbers or guarantees.

## 10. Iron's Spellbooks: Schools and Casting

*Magic / spellbooks*

Spellbooks hold spells with particular costs, cast requirements and school-related properties. When a new spell looks weaker than expected, consider whether the problem is its level, available mana, cast time, cooldown or the enemy's defenses. In combat, learning to recognize when a spell is ready is as important as unlocking one with a larger number.

The manual should contain the exact AO-tested routes for finding scrolls, upgrading books and understanding school interactions. It should also distinguish spells added by Traveloptics or other addons from the core Iron's Spellbooks spell roster.

**Try this:** Equip a basic book, read the mana cost of one spell and test it against an ordinary enemy before fighting a wizard boss.

**Verification before publication:** Verify final spell list, installed add-ons and player source of scrolls; no promise of exact wizard-tower drops.

## 11. Ars Nouveau: Build a Spell with Glyphs

*Magic / Ars Nouveau*

Ars Nouveau lets players compose magical effects rather than merely choose a finished attack. A spell begins with how it targets something, then adds effects and modifiers to shape what happens. Small combinations often provide enormous utility: moving something, placing light or helping with ordinary exploration can matter more than a large damage spell.

Start with a simple, reproducible spell and confirm its resource cost. Only then add further glyphs or complex rituals. The Field Manual should provide step-by-step examples in the *actual pinned AO version*, with a clear distinction between combat spells, utility spells and automation.

**Try this:** Build a basic useful spell and explain which component selects a target and which creates the result.

**Verification before publication:** Validate specific glyph names, recipes, casting apparatus and addon interactions.

## 12. When a Dungeon is Above Your Tier

*Encounter readiness*

AO tiers indicate how demanding a location is expected to be. They are a preparation guide, not an invisible wall. A Tier 6 arena may be discovered while you are still wearing Tier 2 equipment; the journal should record the find and allow you to return later instead of punishing curiosity.

Before entering, compare your armor, supports, damage options, resistances and escape route to the boss dossier. Some encounters require the right response to a mechanic, not just better numbers. Discovery, conquest and optional mastery are different kinds of progress.

**Try this:** Identify a discovered dungeon's provisional difficulty tier and one improvement you want before entering.

**Verification before publication:** Check against AO Atlas and actual balance tweaks; avoid claiming Boss Tier equal power of every mod version.

## 13. The Dreamscape and Its Native Systems

*Optional mod / NeoPasterDream*

NeoPasterDream includes unusual world rules, equipment and puzzle interactions. Its dream dimension is not just another place to mine familiar ores. The player's first step should be to examine the native guidebook and learn how to travel safely; more specialized workshop and puzzle chapters can then become optional.

The current AO historical JAR is version 0.9.6. Later web descriptions list additional realm content, so an instruction must not mention a dimension or recipe that this specific version cannot access. This manual should eventually show real photographs of the game's own GUI rather than generic mockups.

**Try this:** Find the version-specific guidebook, and distinguish which content is currently available from unfinished future features.

**Verification before publication:** Verify Dyedream rift config, actual dimension names, weapon workshop, flower puzzles and Cold Domain for 0.9.6.

## 14. Enigmatic Legacy: The Choice of Curses

*Optional mod / Enigmatic Legacy*

Enigmatic equipment can be explored without automatically agreeing to the Ring of the Seven Curses. AO treats the ordinary artifact route and the cursed route as **separate optional adventures**. The cursed route is for players who deliberately want stronger constraints and unfamiliar risk; it is never a requirement for the main campaign.

Before a player intentionally accepts the curse, the manual should show the exact current restrictions, whether its effects can be reversed, and which items really require the cursed state. Neither picking up a ring nor opening a quest should secretly trigger that choice.

**Try this:** Compare two known non-cursed relics and read the full warning before deciding whether the optional challenge interests you.

**Verification before publication:** Inspect Enigmatic Legacy Plus 1.1.2 item/advancement IDs, curse-state flags, multiplayer behavior and actual possibility of reversal.

