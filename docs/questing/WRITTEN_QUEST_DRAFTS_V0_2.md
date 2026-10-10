# Ambient Odyssey — Written Quest Drafts v0.2

**Status:** original in-game-facing copy, **NOT implemented quests**. These drafts expand existing content seeds and can be rewritten after the content expansion. Trigger and reward specifications are deliberately pending verification. Each quest links to the same existing seed ID; chapter order is provisional and optional routes never gate the main story.

## First Pages

### 1. A New Page

This world is considerably larger than it first appears. You do not need to learn everything today; you only need a reason to take the next step.

**Objective:** Read the first entry in your Adventure Journal.

**Player hint:** Your discoveries and encounters will open more journeys. The detailed Field Manual is separate.

*Seed ID:* `ao_first_pages_01_welcome_to_ambient_odyssey` · *Candidate tracking:* `read` · *Implementation note:* Always available on first joining.

### 2. A Journal of Your Own

Quests here follow the adventures you choose. Some are invitations rather than instructions; an unfamiliar ruin does not demand you conquer it immediately.

**Objective:** Open this entry and learn how optional chapters appear.

**Player hint:** The journal records your story; it is not a checklist you must finish before exploring freely.

*Seed ID:* `ao_first_pages_02_learn_how_to_follow_an_adventure` · *Candidate tracking:* `read` · *Implementation note:* Read-once intro; do not repeatedly toast.

### 3. The Field Manual

A good explorer knows where to look for answers. The Field Manual contains the detailed explanations that would interrupt an adventure.

**Objective:** Read how to open the FTB Field Manual when you need it.

**Player hint:** The Adventure Journal is for goals; the Field Manual is for mechanics, recipes and examples.

*Seed ID:* `ao_first_pages_03_open_the_educational_field_manua` · *Candidate tracking:* `read` · *Implementation note:* No reliable direct open-FTB objective established; optional reading.

### 4. The Recipe Beneath the Recipe

A strange item is a question, not a dead end. Many useful materials become obvious once you know what they are used for.

**Objective:** Learn how to inspect an item's recipes and uses through JEI.

**Player hint:** Use the recipe and uses shortcuts shown in the Field Manual; exact keybinds can be remapped.

*Seed ID:* `ao_first_pages_04_use_jei_to_look_up_a_recipe` · *Candidate tracking:* `read` · *Implementation note:* No documented Questlog objective for opening JEI recipe screen; educational only.

### 5. Behind the Shield

An axe or sword can win a quick encounter; a shield may let you survive an unfamiliar one. Defense is worth more than one extra hit when you don't know the enemy.

**Objective:** Obtain a shield and try blocking a safe attack.

**Player hint:** Hold it in your off-hand and use its action key; some modded attacks may bypass a shield.

*Seed ID:* `ao_first_pages_05_craft_a_shield_and_learn_off_han` · *Candidate tracking:* `item_obtain` · *Implementation note:* Use vanilla shield ID only for possession, never claim blocking proved.

### 6. Stronger Than Bare Hands

Armor is your allowance for mistakes. Even ordinary pieces are worthwhile when your next cave contains creatures you have never seen.

**Objective:** Equip a useful piece of armor.

**Player hint:** Begin with any armor that fits your playstyle. Rare items are not necessary for the first expedition.

*Seed ID:* `ao_first_pages_06_equip_your_first_useful_armor` · *Candidate tracking:* `item_equip` · *Implementation note:* Any vanilla armor slot allowed. Do not enforce full matching set.

### 7. Provisions for the Road

The first rule of a long expedition is to return from it. Take more food than you expect to need; it is much harder to gather when danger is already chasing you.

**Objective:** Obtain a small supply of food before venturing far.

**Player hint:** Cooked food lasts longer than relying on whatever you find underground. Exact amount will be set during balance QA.

*Seed ID:* `ao_first_pages_07_prepare_food_for_an_expedition` · *Candidate tracking:* `item_obtain` · *Implementation note:* Select flexible edible tag/OR objectives after ingredient availability test.

### 8. A Marker Left Behind

Defeat is part of discovery. Before traveling, understand what happens to equipment when you die and how your recovery system works.

**Objective:** Read the death-recovery page in the Field Manual.

**Player hint:** Do not gamble an irreplaceable item until you know your world's grave and recovery rules.

*Seed ID:* `ao_first_pages_08_understand_what_death_and_a_tomb` · *Candidate tracking:* `read` · *Implementation note:* Do not promise particular tombstone behavior without exact current config.

### 9. A Pack for the Journey

New loot is most useful when you can carry it home. An extra bag also makes it easier to separate emergency gear from what you hope to sell or study.

**Objective:** Obtain a starter backpack or other suitable portable storage.

**Player hint:** See the Field Manual for upgrades, filters and how the backpack interacts with your inventory.

*Seed ID:* `ao_first_pages_09_make_a_starter_bag_or_backpack` · *Candidate tracking:* `item_obtain` · *Implementation note:* Resolve Sophisticated Backpacks and alternate carry-items before deciding OR predicate.

### 10. Mark the Way Home

The world is easy to lose yourself in. A single marked shelter or Waystone can turn an uncertain journey into a repeatable route.

**Objective:** Learn how to mark an important place on your map.

**Player hint:** A waypoint does not mean your character is safe. Keep track of portals and the path back, too.

*Seed ID:* `ao_first_pages_10_learn_the_map_and_waypoint_contr` · *Candidate tracking:* `read` · *Implementation note:* Xaero actions may need custom integration; educational completion only initially.

### 11. A Roof Among Strangers

Settlements are places to rest, trade and gather information. They are also worth returning to when a future adventure takes you through familiar country.

**Objective:** Find a settlement or establish a safe home base.

**Player hint:** A naturally generated village is one option; your own protected shelter should also satisfy the spirit of this milestone.

*Seed ID:* `ao_first_pages_11_reach_a_village_or_safe_settleme` · *Candidate tracking:* `alternative` · *Implementation note:* Do not gate mainline on any specific village structure ID or forced travel.

### 12. A Chest for Every Explorer

In a multiplayer dungeon, one player's discovery should not necessarily empty the rewards for everyone else. Some containers are personal; others are shared.

**Objective:** Read the Lootr and chest-sharing explanation.

**Player hint:** Ask before taking the last shared item. Individual loot containers may look different from ordinary chests.

*Seed ID:* `ao_first_pages_12_understand_individual_lootr_ches` · *Candidate tracking:* `read` · *Implementation note:* No automatic loot claim required; preserve fair multiplayer etiquette.

### 13. Know Your Equipment

Your armor is not your whole defense. Rings, charms and unusual relics can change how you survive a battle—but some compete for the same equipment slot.

**Objective:** Read the basic combat-support and equipment-slot guide.

**Player hint:** The strength of a support depends on when its effect activates, not just how impressive its name sounds.

*Seed ID:* `ao_first_pages_13_read_the_basic_combat_and_suppor` · *Candidate tracking:* `read` · *Implementation note:* Reference Gear Atlas; verify Curios/Accessories slots.

## Open Road

### 1. Where the Grass Changes

Beyond the safety of your first camp, the world changes. The next landscape may have new wildlife, unfamiliar materials and a new kind of danger.

**Objective:** Discover a biome you have not visited before.

**Player hint:** Only naturally visited, enabled biomes should count in the future Explorer's Journal.

*Seed ID:* `ao_open_road_01_record_your_first_new_biome` · *Candidate tracking:* `advancement_bridge` · *Implementation note:* A generated biome checklist can record first visits; Questlog no universal new-biome objective.

### 2. A Different Horizon

A forest, a rocky peak and a wetland are not interchangeable places. Learning to recognize a region will matter when searching for unusual creatures and ruins.

**Objective:** Explore a contrasting landscape or biome family.

**Player hint:** Any suitable climate family should count; avoid sending a new player across thousands of blocks by chance.

*Seed ID:* `ao_open_road_02_reach_a_contrasting_biome_family` · *Candidate tracking:* `alternative` · *Implementation note:* Biome-family OR objective depends on validated active tags/registry.

### 3. The Shape of the World

Not every great discovery contains a loot chest. A valley, a natural arch or a towering cliff can be worth recording simply because it exists.

**Objective:** Record a remarkable natural location.

**Player hint:** For procedural terrain, use an opt-in journal mark or screenshot—not a fabricated structure detector.

*Seed ID:* `ao_open_road_03_visit_an_interesting_natural_for` · *Candidate tracking:* `manual_optional` · *Implementation note:* Never hard-require a mathematically arbitrary scenic viewpoint.

### 4. Stones That Outlasted Their Builders

Ruins are signs that someone—or something—was here before you. Most are safe enough to investigate cautiously; a few are warnings.

**Objective:** Discover a minor ruin, small tower or other notable landmark.

**Player hint:** Do not assume every tower is safe. Look for mobs, traps or an obvious entrance before rushing inside.

*Seed ID:* `ao_open_road_04_discover_a_minor_ruin_or_small_t` · *Candidate tracking:* `structure_or_advancement` · *Implementation note:* Use a list of actual common structure IDs, plus safe alternate proof.

### 5. A Ruin Is Not a Dungeon

One abandoned house may hold a little loot. Another structure can contain several floors of enemies and a boss. Knowing the difference is an exploration skill.

**Objective:** Read the danger-rating system used in the AO Atlas.

**Player hint:** A location's tier means recommended preparation, not that you are forbidden to enter.

*Seed ID:* `ao_open_road_05_learn_the_difference_between_a_l` · *Candidate tracking:* `read` · *Implementation note:* Pure learning objective; no need for registered structure.

### 6. Beneath the Surface

The stone under your feet hides materials, creatures, old corridors and even entire unfamiliar habitats. Bring light and a way back.

**Objective:** Explore beneath the surface and safely return.

**Player hint:** Avoid a depth-only task that rewards digging a hole. Prefer a normal cave expedition or accepted exploration milestone.

*Seed ID:* `ao_open_road_06_explore_a_cave_below_the_surface` · *Candidate tracking:* `custom_or_optional` · *Implementation note:* A generic arbitrary cave visit is not a reliable Questlog structure objective.

### 7. An Edge Worth Carrying

There is no perfect weapon for every threat. A sturdy blade, a spear or a ranged choice can each be useful depending on what you're facing.

**Objective:** Upgrade to a reliable primary weapon.

**Player hint:** A diamond weapon is an early benchmark, not a permanent ban on alternative modded weapons.

*Seed ID:* `ao_open_road_07_upgrade_to_a_diamond_weapon` · *Candidate tracking:* `item_obtain_or` · *Implementation note:* Accept comparable modded weapon alternatives after tier calibration.

### 8. A Small Advantage

The first helpful charm or artifact will teach you something about your build. Look for effects you can actually notice while exploring.

**Objective:** Find and try a travel or utility accessory.

**Player hint:** Check whether the item needs equipping, charging or activating; picking one up may not reveal its function.

*Seed ID:* `ao_open_road_08_equip_a_travel_accessory` · *Candidate tracking:* `item_obtain` · *Implementation note:* True equipped-state proof may require custom accessories integration.

### 9. Somewhere Worth Remembering

Good explorers recognize the places they will want to revisit. A strange tower that is too dangerous today may become tomorrow's destination.

**Objective:** Save a discovered location for a later expedition.

**Player hint:** Use an existing map waypoint; never reveal the coordinates of places you have not found yourself.

*Seed ID:* `ao_open_road_09_bookmark_a_place_worth_returning` · *Candidate tracking:* `read` · *Implementation note:* Waypoint event not supported natively; instruct and complete by reading.

### 10. The Return Journey

The trip home is part of the expedition. With an established route, distance becomes an opportunity rather than a risk.

**Objective:** Establish a reliable return route or activate a Waystone.

**Player hint:** Carry supplies for the return trip. A Waystone is helpful, but not every expedition starts near one.

*Seed ID:* `ao_open_road_10_find_a_safe_return_route_or_ways` · *Candidate tracking:* `alternative` · *Implementation note:* Avoid requiring an exact Waystone ID if travel system changes.

### 11. The Explorer's Record

A world this large deserves a record. You should be able to see what you have discovered without remembering every biome name yourself.

**Objective:** Learn how your personal Explorer's Journal tracks discoveries.

**Player hint:** The checklist records visits; finding a dungeon does not mean its boss has been defeated.

*Seed ID:* `ao_open_road_11_open_your_explorer_s_journal` · *Candidate tracking:* `read` · *Implementation note:* Journal UI not selected/installed; keep as hidden until engine chosen.

### 12. The Shape of Danger

A massive citadel and a quiet roadside ruin should never feel equally threatening. Learn when to step inside—and when to return later.

**Objective:** Consult the difficulty guidance for a discovered major structure.

**Player hint:** Look at armor, support items and environmental hazards together. Retreating is preparation, not failure.

*Seed ID:* `ao_open_road_12_discover_why_some_ruins_are_much` · *Candidate tracking:* `read` · *Implementation note:* Cross-link Boss Atlas once that location has a validated tier.

## Trial Steel

### 1. A Diamond Foundation

The first demanding battles will punish weak armor. Diamonds are not the end of the journey, but they offer a reliable starting point.

**Objective:** Assemble a full set of diamond-grade armor.

**Player hint:** Vanilla diamond or genuinely equivalent tested armor should qualify; avoid strict item-only restrictions on viable builds.

*Seed ID:* `ao_trial_steel_01_acquire_a_full_set_of_diamond_ar` · *Candidate tracking:* `inventory_set_bridge` · *Implementation note:* Questlog cannot directly inspect whole equipment profile as one predicate without bridge.

### 2. Protection Is a Decision

Armor makes room for mistakes, and enchantments make room for bigger ones. For the coming trials, enchantments matter as much as raw armor value.

**Objective:** Bring your protection to approximately Protection III across your diamond armor.

**Player hint:** AO's Tier 2 benchmark is enchanted diamond at roughly Protection III; do not require identical enchantments if equivalent protection exists.

*Seed ID:* `ao_trial_steel_02_enchant_the_armor_for_real_prote` · *Candidate tracking:* `attribute_bridge` · *Implementation note:* Requires full gear/enchantment equivalence policy and custom verification.

### 3. Choose Your Weapon

A good weapon is not simply the one with the highest damage number. Reach, speed, spells and special effects all change how it handles danger.

**Objective:** Equip a reliable weapon suited to a major encounter.

**Player hint:** Try it against ordinary enemies before committing to a dungeon with unfamiliar mechanics.

*Seed ID:* `ao_trial_steel_03_upgrade_the_primary_weapon` · *Candidate tracking:* `item_equip_or` · *Implementation note:* Allow swords, bows and spellbooks/alternatives; never lock one class.

### 4. Hidden Strength

Combat accessories turn ordinary equipment into a build. Some reward aggressive attacks, some save you from mistakes, and others help you move.

**Objective:** Read how A-grade combat-support items are evaluated in the Gear Atlas.

**Player hint:** An item belongs in A grade because it meaningfully helps in combat, not because its rarity looks impressive.

*Seed ID:* `ao_trial_steel_04_learn_meaningful_combat_support_` · *Candidate tracking:* `read` · *Implementation note:* A/EX grade source is AO provisional Gear Atlas; verify versions.

### 5. The First Reliable Companion

An accessory with a dependable effect is worth more than a collection of curios you never use. Choose one that suits your preferred way to fight.

**Objective:** Equip one compatible A-grade combat-support item.

**Player hint:** Read the item's tooltip: does it trigger passively, on hit, on damage, or after a cooldown?

*Seed ID:* `ao_trial_steel_05_equip_your_first_a_grade_combat_` · *Candidate tracking:* `custom_equipment_bridge` · *Implementation note:* Curios/Relics equipped-state not covered by vanilla Questlog item_equip slots.

### 6. A Second Layer of Defense

A single charm can save you once. Two carefully chosen supports can cover different weaknesses—if you can equip them together.

**Objective:** Equip two simultaneously usable A-grade combat-support items.

**Player hint:** Two items in the same slot do not count as a two-item loadout. Avoid counting EX-grade effects until balanced.

*Seed ID:* `ao_trial_steel_06_equip_a_second_compatible_a_grad` · *Candidate tracking:* `custom_equipment_bridge` · *Implementation note:* Tier 2 user-required threshold. Cross-check actual slot exclusivity.

### 7. What Fits Together

Two powerful items are not always stronger together. They can compete for a slot, overwrite an effect or multiply into something that needs rebalancing.

**Objective:** Review the slots and mechanics of your current combat supports.

**Player hint:** Open the Gear Atlas if you need to compare activated and passive effects.

*Seed ID:* `ao_trial_steel_07_check_support_slot_limits_and_ge` · *Candidate tracking:* `read` · *Implementation note:* Never grant equivalent power via Origin/class passives.

### 8. A Door That Feels Too Heavy

Major dungeons leave a different impression from ordinary ruins. Finding one is a discovery in itself—even if today you only mark its entrance.

**Objective:** Discover one appropriate Tier 2 major dungeon or dangerous landmark.

**Player hint:** You can return later. The discovery records where the next challenge lies, not whether you won.

*Seed ID:* `ao_trial_steel_08_discover_a_tier_2_major_dungeon` · *Candidate tracking:* `structure_or_advancement` · *Implementation note:* Require natural registered location from actual AO Atlas; choose several alternatives.

### 9. Before the First Step Inside

Take a moment to prepare. Food, armor, escape options and information are easier to gather outside than inside a boss arena.

**Objective:** Read the equipment and hazard recommendations for your selected dungeon.

**Player hint:** Your recommended tier is a guideline; a clever build still needs survivability and familiarity with the enemy.

*Seed ID:* `ao_trial_steel_09_study_its_recommended_gear_level` · *Candidate tracking:* `read` · *Implementation note:* Cross-link to verified boss dossier, don't spoil loot prematurely.

### 10. Your First Great Test

You have learned how to travel, survive and improve your equipment. Now use those skills in a challenge that actually asks something of you.

**Objective:** Overcome one approved Tier 2 dungeon or miniboss encounter.

**Player hint:** You can choose from several encounters. The main campaign must not depend on finding one ultra-rare boss.

*Seed ID:* `ao_trial_steel_10_overcome_a_suitable_tier_2_encou` · *Candidate tracking:* `boss_kill_or_advancement` · *Implementation note:* Need whitelist of validated Tier 2 boss IDs and party credit policy.

### 11. Found, Fought, Finished

Entering a ruined fortress is one achievement. Defeating its guardian is another. Finding every secret is a third, entirely optional goal.

**Objective:** Read how discovery, conquest and mastery are tracked separately.

**Player hint:** Mastery is an optional bonus; it should never block normal chapter progression.

*Seed ID:* `ao_trial_steel_11_learn_how_dungeon_completion_dif` · *Candidate tracking:* `read` · *Implementation note:* Journal found/cleared/mastered state planned, not implemented.

### 12. The World Opens Wider

The next chapters will introduce stranger lands and harder enemies. You already know the important part: choose your own route, and prepare for what you find.

**Objective:** Complete the Tier 2 preparation and encounter milestone, then choose an optional expedition.

**Player hint:** No single modded dimension is required to continue. Your character's path is yours to shape.

*Seed ID:* `ao_trial_steel_12_review_the_next_tier_without_loc` · *Candidate tracking:* `quest_complete` · *Implementation note:* Only complete when actual previous quest verified, allow alternative Tier 2 encounters.

## Enigmatic Normal

### 1. A Peculiar Invitation

Some items appear ordinary until you learn what they are willing to do for you. Enigmatic artifacts reward curiosity, but not every mystery asks for a sacrifice.

**Objective:** Read the introductory notes on Enigmatic Legacy's artifacts.

**Player hint:** This path is separate from the Seven Curses route. You do not need to equip the cursed ring.

*Seed ID:* `ao_enigmatic_normal_01_discover_the_enigmatic_legacy_re` · *Candidate tracking:* `read` · *Implementation note:* Normal route independent of cursed flags.

### 2. A Choice Not Yet Made

The first useful relic should teach you how unusual equipment works before you make riskier decisions. Read its effect, slot and limits carefully.

**Objective:** Inspect one accessible non-cursed enigmatic relic.

**Player hint:** An item's presence in JEI does not prove it is accessible without the cursed ring; verify crafting and drops.

*Seed ID:* `ao_enigmatic_normal_02_understand_normal_relics_versus_` · *Candidate tracking:* `item_obtain` · *Implementation note:* Must source-check actual obtainable Enigmatic Legacy Plus 1.1.2 item.

## Enigmatic Cursed

### 1. The Warning on the Ring

Some bargains are not meant to be undone. The Seven Curses route is available to those who deliberately want a harsher game, not a rite of passage for every adventurer.

**Objective:** Read the full risk notice before deciding whether to proceed.

**Player hint:** Nothing in the main campaign requires this ring. Choosing not to wear it will not close other quests.

*Seed ID:* `ao_enigmatic_cursed_01_read_the_seven_curses_warning_an` · *Candidate tracking:* `read` · *Implementation note:* No auto-equip, no forced cursed state; warn about permanence where verified.

### 2. An Unclaimed Oath

Possessing an object and accepting its terms are different choices. The journal will never treat picking up the ring as consent.

**Objective:** Learn how this mod distinguishes holding the ring from activating its curse.

**Player hint:** Keep normal artifact progression available whether or not the player chooses this branch.

*Seed ID:* `ao_enigmatic_cursed_02_consider_alternative_normal_rout` · *Candidate tracking:* `read` · *Implementation note:* User must explicitly opt in outside Questlog; do not award/force ring equip.

## Dream

### 1. The Shape of a Dream

Beyond familiar terrain lies a world that does not follow familiar rules. Before crossing into it, find out which dreams are actually reachable in this version.

**Objective:** Investigate the documented route into the Dreamscape.

**Player hint:** This entry will stay hidden until the pinned NeoPasterDream 0.9.6 realm access is verified.

*Seed ID:* `ao_dream_01_find_a_rumor_about_the_dream_rif` · *Candidate tracking:* `manual_gate` · *Implementation note:* Dream entry method must be confirmed from JAR/config not inferred from modern wiki.

### 2. The First Dreamseeker

Strange dimensions deserve patient explorers. If you find a Dreamseeker note, pay attention: it may be explaining a system you will need much later.

**Objective:** Find and read a real Dreamseeker note or journal item.

**Player hint:** Notes are only valid quest targets once their item IDs and obtainable locations are confirmed.

*Seed ID:* `ao_dream_02_discover_the_dream_s_access_loca` · *Candidate tracking:* `item_obtain` · *Implementation note:* Replace with exact note when verified.

### 3. Colors Beyond the World

A dream realm is more than a different sky. Its terrain, resources and inhabitants may reward a different way of traveling and fighting.

**Objective:** Make your first verified Dreamscape biome discovery.

**Player hint:** Never send players to later-release regions that do not exist in AO's 0.9.6 binary.

*Seed ID:* `ao_dream_03_read_the_original_dreamseeker_gu` · *Candidate tracking:* `visit_biome` · *Implementation note:* Verify dimension/biome registries in actual build.

## Aquamirae

### 1. The Sea Has Teeth

A cold sea can conceal far more than ice and wreckage. Pack for the journey, and assume that the first strange shape beneath the water is a warning.

**Objective:** Read the Frozen Seas preparation guide.

**Player hint:** Bring a safe return method. Swimming deeper is not the same as being ready for the thing living below.

*Seed ID:* `ao_aquamirae_01_plan_an_ice_ocean_expedition` · *Candidate tracking:* `read` · *Implementation note:* Aquamirae available in Test8.2, exact AO tier pending combat calibration.

### 2. Walls of Ice

A maze in the frozen ocean is a discovery, even when you only survive its outskirts. Map an entrance before you risk diving farther.

**Objective:** Locate the Ice Maze through natural exploration.

**Player hint:** The Ice Maze must resolve to a real registered structure or custom verified location trigger.

*Seed ID:* `ao_aquamirae_02_discover_deep_frozen_ocean_or_el` · *Candidate tracking:* `structure_or_advancement` · *Implementation note:* Verify Aqam. 7.2.10 structure key and biome eligibility.

## Ars

### 1. A Page of Spells

Magic does not begin with spectacular damage. It begins with a book, a simple glyph and the ability to combine effects deliberately.

**Objective:** Acquire your first usable Ars Nouveau spellbook.

**Player hint:** The Field Manual explains glyph syntax step by step. This adventure only tracks the major milestone.

*Seed ID:* `ao_ars_01_craft_a_basic_spellbook` · *Candidate tracking:* `item_obtain` · *Implementation note:* Verify Ars version and acceptable starter spellbook IDs.

## Iron Magic

### 1. Ink, Paper, Power

The first spell you cast will not be the strongest one you ever know. Learning what a spell costs is just as valuable as learning what it does.

**Objective:** Acquire a usable spellbook for Iron's Spells 'n Spellbooks.

**Player hint:** Start with a spell you can reliably cast and recharge. Look up spell schools in the Field Manual.

*Seed ID:* `ao_iron_magic_01_obtain_a_starter_spellbook` · *Candidate tracking:* `item_obtain` · *Implementation note:* Verify current tier of spellbooks and player access; no class requirement.

## Twilight

### 1. A Forest Out of Place

Some forests do not belong to this world. Their paths branch toward ruins and creatures that expect preparation rather than courage alone.

**Objective:** Learn how to enter the Twilight Forest.

**Player hint:** Do not assume the first boss is optional to a specific Twilight portal progression gate until verified.

*Seed ID:* `ao_twilight_01_find_how_to_open_a_twilight_port` · *Candidate tracking:* `read` · *Implementation note:* Portal recipe and progression require exact installed mod audit.

## End Eyes

### 1. Eyes from Many Roads

Reaching the End should feel like the result of several adventures, not a single uninteresting shopping list. The paths to an Eye are meant to differ.

**Objective:** Read how the pack's End Remastered eye collection works.

**Player hint:** Collect eligible eyes through different optional journeys. Do not assume every named eye is mandatory.

*Seed ID:* `ao_end_eyes_01_understand_that_eyes_may_come_fr` · *Candidate tracking:* `read` · *Implementation note:* Exact number of slots, eyes and alternatives must be validated in config.

