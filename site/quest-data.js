window.AO_QUEST_DATA = {
  "schema": "ambient_odyssey_quest_atlas_v1",
  "version": "v0.4h Q1 experimental",
  "game_version": "1.21.1",
  "questlog_version": "3.4.1",
  "data_status": "source-authored; full game runtime not verified",
  "chapters": [
    {
      "id": "first_pages",
      "name": "The First Pages",
      "icon": "minecraft:book",
      "order": 0,
      "quest_count": 13
    },
    {
      "id": "open_road",
      "name": "The Open Road",
      "icon": "minecraft:compass",
      "order": 1,
      "quest_count": 12
    },
    {
      "id": "trial_steel",
      "name": "Trial by Steel",
      "icon": "minecraft:iron_sword",
      "order": 2,
      "quest_count": 7
    },
    {
      "id": "trail_notes",
      "name": "Rumours of the Wild",
      "icon": "minecraft:spyglass",
      "order": 3,
      "quest_count": 5
    },
    {
      "id": "archaeology",
      "name": "Unearthed Histories",
      "icon": "minecraft:brush",
      "order": 4,
      "quest_count": 3
    },
    {
      "id": "enigmatic_normal",
      "name": "The Relic Scholar",
      "icon": "minecraft:enchanted_book",
      "order": 5,
      "quest_count": 2
    },
    {
      "id": "enigmatic_cursed",
      "name": "The Seven Curses — Opt In",
      "icon": "minecraft:nether_star",
      "order": 6,
      "quest_count": 2
    },
    {
      "id": "dream",
      "name": "Dreamseeker's Notes",
      "icon": "minecraft:amethyst_shard",
      "order": 7,
      "quest_count": 1
    },
    {
      "id": "aquamirae",
      "name": "Frozen Seas",
      "icon": "minecraft:heart_of_the_sea",
      "order": 8,
      "quest_count": 1
    },
    {
      "id": "ars",
      "name": "The Arcane Academy",
      "icon": "minecraft:enchanting_table",
      "order": 9,
      "quest_count": 1
    },
    {
      "id": "iron_magic",
      "name": "The Spellwright's Journey",
      "icon": "minecraft:blaze_rod",
      "order": 10,
      "quest_count": 1
    },
    {
      "id": "twilight",
      "name": "The Twilight Path",
      "icon": "minecraft:oak_sapling",
      "order": 11,
      "quest_count": 1
    },
    {
      "id": "end_eyes",
      "name": "The Eyes of the End",
      "icon": "minecraft:ender_eye",
      "order": 12,
      "quest_count": 1
    }
  ],
  "quests": [
    {
      "id": "ao_first_pages_01_welcome_to_ambient_odyssey",
      "chapter": "first_pages",
      "title": "A New Page",
      "description": "This world is considerably larger than it first appears. You do not need to learn everything today; you only need a reason to take the next step.\n\nField note: Your discoveries and encounters will open more journeys. The detailed Field Manual is separate.",
      "icon": "minecraft:book",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the first page of your journal"
        }
      ],
      "rewards": [],
      "prerequisites": [],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_02_learn_how_to_follow_an_adventure",
      "chapter": "first_pages",
      "title": "A Journal of Your Own",
      "description": "Quests here follow the adventures you choose. Some are invitations rather than instructions; an unfamiliar ruin does not demand you conquer it immediately.\n\nField note: The journal records your story; it is not a checklist you must finish before exploring freely.",
      "icon": "minecraft:book",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read how the journal handles optional adventures"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_03_open_the_educational_field_manua",
      "chapter": "first_pages",
      "title": "The Field Manual",
      "description": "A good explorer knows where to look for answers. The Field Manual contains the detailed explanations that would interrupt an adventure.\n\nField note: The Adventure Journal is for goals; the Field Manual is for mechanics, recipes and examples.",
      "icon": "minecraft:book",
      "sort_order": 3,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn the difference between the Journal and the Field Manual"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_04_use_jei_to_look_up_a_recipe",
      "chapter": "first_pages",
      "title": "The Recipe Beneath the Recipe",
      "description": "A strange item is a question, not a dead end. Many useful materials become obvious once you know what they are used for.\n\nField note: Use the recipe and uses shortcuts shown in the Field Manual; exact keybinds can be remapped.",
      "icon": "minecraft:book",
      "sort_order": 4,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the JEI recipe and uses shortcuts"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_05_craft_a_shield_and_learn_off_han",
      "chapter": "first_pages",
      "title": "Behind the Shield",
      "description": "An axe or sword can win a quick encounter; a shield may let you survive an unfamiliar one. Defense is worth more than one extra hit when you don't know the enemy.\n\nField note: Hold it in your off-hand and use its action key; some modded attacks may bypass a shield.",
      "icon": "minecraft:book",
      "sort_order": 5,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:shield",
          "required_amount": 1,
          "name": "Carry 1 × shield"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 35
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_06_equip_your_first_useful_armor",
      "chapter": "first_pages",
      "title": "Stronger Than Bare Hands",
      "description": "Armor is your allowance for mistakes. Even ordinary pieces are worthwhile when your next cave contains creatures you have never seen.\n\nThis trial detects one of three vanilla chestplates; different modded armors will be added after exact registry verification. It does NOT verify a full armor set.\n\nField note: Begin with any armor that fits your playstyle. Rare items are not necessary for the first expedition.",
      "icon": "minecraft:book",
      "sort_order": 6,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Equip a practical piece of armor",
          "objectives": [
            {
              "type": "questlog:item_equip",
              "item": "minecraft:leather_chestplate",
              "slot": "chest",
              "name": "Equip leather armor"
            },
            {
              "type": "questlog:item_equip",
              "item": "minecraft:iron_chestplate",
              "slot": "chest",
              "name": "Equip iron armor"
            },
            {
              "type": "questlog:item_equip",
              "item": "minecraft:diamond_chestplate",
              "slot": "chest",
              "name": "Equip diamond armor"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 25
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_07_prepare_food_for_an_expedition",
      "chapter": "first_pages",
      "title": "Provisions for the Road",
      "description": "The first rule of a long expedition is to return from it. Take more food than you expect to need; it is much harder to gather when danger is already chasing you.\n\nField note: Cooked food lasts longer than relying on whatever you find underground. Exact amount will be set during balance QA.",
      "icon": "minecraft:book",
      "sort_order": 7,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Carry provisions for a short expedition",
          "objectives": [
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:bread",
              "required_amount": 8,
              "name": "Carry 8 × bread"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:cooked_beef",
              "required_amount": 8,
              "name": "Carry 8 × cooked beef"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:cooked_chicken",
              "required_amount": 8,
              "name": "Carry 8 × cooked chicken"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:baked_potato",
              "required_amount": 8,
              "name": "Carry 8 × baked potato"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:item",
          "item": "minecraft:torch",
          "count": 12,
          "auto_claim": false
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_08_understand_what_death_and_a_tomb",
      "chapter": "first_pages",
      "title": "A Marker Left Behind",
      "description": "Defeat is part of discovery. Before traveling, understand what happens to equipment when you die and how your recovery system works.\n\nField note: Do not gamble an irreplaceable item until you know your world's grave and recovery rules.",
      "icon": "minecraft:book",
      "sort_order": 8,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn how to recover your equipment after death"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_09_make_a_starter_bag_or_backpack",
      "chapter": "first_pages",
      "title": "A Pack for the Journey",
      "description": "New loot is most useful when you can carry it home. An extra bag also makes it easier to separate emergency gear from what you hope to sell or study.\n\nStart by establishing a safe storage point. A wearable backpack is an optional upgrade: consult JEI before choosing one. Carrying a chest does not prove a modded backpack is equipped.\n\nField note: See the Field Manual for upgrades, filters and how the backpack interacts with your inventory.",
      "icon": "minecraft:book",
      "sort_order": 9,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:chest",
          "required_amount": 1,
          "name": "Carry 1 × chest"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_10_learn_the_map_and_waypoint_contr",
      "chapter": "first_pages",
      "title": "Mark the Way Home",
      "description": "The world is easy to lose yourself in. A single marked shelter or Waystone can turn an uncertain journey into a repeatable route.\n\nField note: A waypoint does not mean your character is safe. Keep track of portals and the path back, too.",
      "icon": "minecraft:book",
      "sort_order": 10,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read how to save discovered places with Xaero's map"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_11_reach_a_village_or_safe_settleme",
      "chapter": "first_pages",
      "title": "A Roof Among Strangers",
      "description": "Settlements are places to rest, trade and gather information. They are also worth returning to when a future adventure takes you through familiar country.\n\nThis is a planning page, not automated proof of a village visit.\n\nField note: A naturally generated village is one option; your own protected shelter should also satisfy the spirit of this milestone.",
      "icon": "minecraft:book",
      "sort_order": 11,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Choose a safe home base or a friendly settlement"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_12_understand_individual_lootr_ches",
      "chapter": "first_pages",
      "title": "A Chest for Every Explorer",
      "description": "In a multiplayer dungeon, one player's discovery should not necessarily empty the rewards for everyone else. Some containers are personal; others are shared.\n\nField note: Ask before taking the last shared item. Individual loot containers may look different from ordinary chests.",
      "icon": "minecraft:book",
      "sort_order": 12,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn the difference between personal and shared loot"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_first_pages_13_read_the_basic_combat_and_suppor",
      "chapter": "first_pages",
      "title": "Know Your Equipment",
      "description": "Your armor is not your whole defense. Rings, charms and unusual relics can change how you survive a battle—but some compete for the same equipment slot.\n\nField note: The strength of a support depends on when its effect activates, not just how impressive its name sounds.",
      "icon": "minecraft:book",
      "sort_order": 13,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the basics of accessory slots and defensive support"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_01_record_your_first_new_biome",
      "chapter": "open_road",
      "title": "Where the Grass Changes",
      "description": "Beyond the safety of your first camp, the world changes. The next landscape may have new wildlife, unfamiliar materials and a new kind of danger.\n\nQuestlog's vanilla walking statistic is a proxy for beginning an expedition; it does not falsely claim to detect every modded biome. Explore any direction you like.\n\nField note: Only naturally visited, enabled biomes should count in the future Explorer's Journal.",
      "icon": "minecraft:compass",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:stat",
          "stat": "minecraft:walk_one_cm",
          "required_amount": 12000,
          "name": "Explore at least 120 blocks on foot"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 25
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_02_reach_a_contrasting_biome_family",
      "chapter": "open_road",
      "title": "A Different Horizon",
      "description": "A forest, a rocky peak and a wetland are not interchangeable places. Learning to recognize a region will matter when searching for unusual creatures and ruins.\n\nOptional demonstration of biome detection. Most AO biomes are modded, so this is deliberately not a requirement for any other quest.\n\nField note: Any suitable climate family should count; avoid sending a new player across thousands of blocks by chance.",
      "icon": "minecraft:compass",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Find one distinct vanilla region",
          "objectives": [
            {
              "type": "questlog:visit_biome",
              "biome": "minecraft:savanna"
            },
            {
              "type": "questlog:visit_biome",
              "biome": "minecraft:taiga"
            },
            {
              "type": "questlog:visit_biome",
              "biome": "minecraft:swamp"
            },
            {
              "type": "questlog:visit_biome",
              "biome": "minecraft:desert"
            }
          ]
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_03_visit_an_interesting_natural_for",
      "chapter": "open_road",
      "title": "The Shape of the World",
      "description": "Not every great discovery contains a loot chest. A valley, a natural arch or a towering cliff can be worth recording simply because it exists.\n\nScreenshots, waypoints and your own notes count. No fabricated scenic biome registry is required.\n\nField note: For procedural terrain, use an opt-in journal mark or screenshot—not a fabricated structure detector.",
      "icon": "minecraft:compass",
      "sort_order": 3,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Note an interesting landscape or landmark"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_04_discover_a_minor_ruin_or_small_t",
      "chapter": "open_road",
      "title": "Stones That Outlasted Their Builders",
      "description": "Ruins are signs that someone—or something—was here before you. Most are safe enough to investigate cautiously; a few are warnings.\n\nThis is an optional vanilla-ID detection pilot. Modded ruins are not silently treated as vanilla structures, and the quest does not gate major progress.\n\nField note: Do not assume every tower is safe. Look for mobs, traps or an obvious entrance before rushing inside.",
      "icon": "minecraft:compass",
      "sort_order": 4,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Enter a known vanilla ruin or landmark",
          "objectives": [
            {
              "type": "questlog:visit_structure",
              "structure": "minecraft:shipwreck"
            },
            {
              "type": "questlog:visit_structure",
              "structure": "minecraft:desert_pyramid"
            },
            {
              "type": "questlog:visit_structure",
              "structure": "minecraft:ruined_portal"
            }
          ]
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_05_learn_the_difference_between_a_l",
      "chapter": "open_road",
      "title": "A Ruin Is Not a Dungeon",
      "description": "One abandoned house may hold a little loot. Another structure can contain several floors of enemies and a boss. Knowing the difference is an exploration skill.\n\nField note: A location's tier means recommended preparation, not that you are forbidden to enter.",
      "icon": "minecraft:compass",
      "sort_order": 5,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn how a landmark differs from a combat dungeon"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_06_explore_a_cave_below_the_surface",
      "chapter": "open_road",
      "title": "Beneath the Surface",
      "description": "The stone under your feet hides materials, creatures, old corridors and even entire unfamiliar habitats. Bring light and a way back.\n\nReturn with iron for safer equipment. Owning the item is evidence of preparation, not proof that you personally explored a cave.\n\nField note: Avoid a depth-only task that rewards digging a hole. Prefer a normal cave expedition or accepted exploration milestone.",
      "icon": "minecraft:compass",
      "sort_order": 6,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:raw_iron",
          "required_amount": 5,
          "name": "Carry 5 × raw iron"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 45
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_07_upgrade_to_a_diamond_weapon",
      "chapter": "open_road",
      "title": "An Edge Worth Carrying",
      "description": "There is no perfect weapon for every threat. A sturdy blade, a spear or a ranged choice can each be useful depending on what you're facing.\n\nDiamond is a convenient benchmark, not a rule against equivalent modded weapons. This optional milestone will gain alternate gear after item registry inspection.\n\nField note: A diamond weapon is an early benchmark, not a permanent ban on alternative modded weapons.",
      "icon": "minecraft:compass",
      "sort_order": 7,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Carry a sturdy primary weapon",
          "objectives": [
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:diamond_sword",
              "required_amount": 1,
              "name": "Carry 1 × diamond sword"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:diamond_axe",
              "required_amount": 1,
              "name": "Carry 1 × diamond axe"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 75
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_08_equip_a_travel_accessory",
      "chapter": "open_road",
      "title": "A Small Advantage",
      "description": "The first helpful charm or artifact will teach you something about your build. Look for effects you can actually notice while exploring.\n\nField note: Check whether the item needs equipping, charging or activating; picking one up may not reveal its function.",
      "icon": "minecraft:compass",
      "sort_order": 8,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Carry a navigational or scouting tool",
          "objectives": [
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:compass",
              "required_amount": 1,
              "name": "Carry 1 × compass"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:spyglass",
              "required_amount": 1,
              "name": "Carry 1 × spyglass"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:item",
          "item": "minecraft:bread",
          "count": 4,
          "auto_claim": false
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_09_bookmark_a_place_worth_returning",
      "chapter": "open_road",
      "title": "Somewhere Worth Remembering",
      "description": "Good explorers recognize the places they will want to revisit. A strange tower that is too dangerous today may become tomorrow's destination.\n\nField note: Use an existing map waypoint; never reveal the coordinates of places you have not found yourself.",
      "icon": "minecraft:compass",
      "sort_order": 9,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Review how to mark places worth revisiting"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_10_find_a_safe_return_route_or_ways",
      "chapter": "open_road",
      "title": "The Return Journey",
      "description": "The trip home is part of the expedition. With an established route, distance becomes an opportunity rather than a risk.\n\nField note: Carry supplies for the return trip. A Waystone is helpful, but not every expedition starts near one.",
      "icon": "minecraft:compass",
      "sort_order": 10,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Plan a reliable route home or locate a Waystone"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_11_open_your_explorer_s_journal",
      "chapter": "open_road",
      "title": "The Explorer's Record",
      "description": "A world this large deserves a record. You should be able to see what you have discovered without remembering every biome name yourself.\n\nField note: The checklist records visits; finding a dungeon does not mean its boss has been defeated.",
      "icon": "minecraft:compass",
      "sort_order": 11,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn how to keep an explorer's journal"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_open_road_12_discover_why_some_ruins_are_much",
      "chapter": "open_road",
      "title": "The Shape of Danger",
      "description": "A massive citadel and a quiet roadside ruin should never feel equally threatening. Learn when to step inside—and when to return later.\n\nField note: Look at armor, support items and environmental hazards together. Retreating is preparation, not failure.",
      "icon": "minecraft:compass",
      "sort_order": 12,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the warning signs of a major dungeon"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_01_acquire_a_full_set_of_diamond_ar",
      "chapter": "trial_steel",
      "title": "A Diamond Foundation",
      "description": "The first demanding battles will punish weak armor. Diamonds are not the end of the journey, but they offer a reliable starting point.\n\nOPTIONAL vanilla gear benchmark; this does not require a particular Origin, class, relic or combat discipline, nor does it gate the rest of AO. Requiring all four items only proves they are in inventory, not enchanted or equipped.\n\nField note: Vanilla diamond or genuinely equivalent tested armor should qualify; avoid strict item-only restrictions on viable builds.",
      "icon": "minecraft:iron_sword",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:diamond_helmet",
          "required_amount": 1,
          "name": "Carry 1 × diamond helmet"
        },
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:diamond_chestplate",
          "required_amount": 1,
          "name": "Carry 1 × diamond chestplate"
        },
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:diamond_leggings",
          "required_amount": 1,
          "name": "Carry 1 × diamond leggings"
        },
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:diamond_boots",
          "required_amount": 1,
          "name": "Carry 1 × diamond boots"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 100
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_02_enchant_the_armor_for_real_prote",
      "chapter": "trial_steel",
      "title": "Protection Is a Decision",
      "description": "Armor makes room for mistakes, and enchantments make room for bigger ones. For the coming trials, enchantments matter as much as raw armor value.\n\nThe automatic criterion is one successful enchantment, NOT a fabricated check for Protection III on four equipped pieces.\n\nField note: AO's Tier 2 benchmark is enchanted diamond at roughly Protection III; do not require identical enchantments if equivalent protection exists.",
      "icon": "minecraft:iron_sword",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:enchant",
          "name": "Apply an enchantment to any item"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_03_upgrade_the_primary_weapon",
      "chapter": "trial_steel",
      "title": "Choose Your Weapon",
      "description": "A good weapon is not simply the one with the highest damage number. Reach, speed, spells and special effects all change how it handles danger.\n\nA small vanilla check rather than a claim to evaluate complex modded weapons. Endgame alternatives remain valid.\n\nField note: Try it against ordinary enemies before committing to a dungeon with unfamiliar mechanics.",
      "icon": "minecraft:iron_sword",
      "sort_order": 3,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Carry a weapon suited to your next challenge",
          "objectives": [
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:diamond_sword",
              "required_amount": 1,
              "name": "Carry 1 × diamond sword"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:diamond_axe",
              "required_amount": 1,
              "name": "Carry 1 × diamond axe"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:bow",
              "required_amount": 1,
              "name": "Carry 1 × bow"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 50
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_04_learn_meaningful_combat_support_",
      "chapter": "trial_steel",
      "title": "Hidden Strength",
      "description": "Combat accessories turn ordinary equipment into a build. Some reward aggressive attacks, some save you from mistakes, and others help you move.\n\nField note: An item belongs in A grade because it meaningfully helps in combat, not because its rarity looks impressive.",
      "icon": "minecraft:iron_sword",
      "sort_order": 4,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the principles of reliable combat support"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_07_check_support_slot_limits_and_ge",
      "chapter": "trial_steel",
      "title": "What Fits Together",
      "description": "Two powerful items are not always stronger together. They can compete for a slot, overwrite an effect or multiply into something that needs rebalancing.\n\nField note: Open the Gear Atlas if you need to compare activated and passive effects.",
      "icon": "minecraft:iron_sword",
      "sort_order": 7,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Review Curios and Accessories slot compatibility"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_09_study_its_recommended_gear_level",
      "chapter": "trial_steel",
      "title": "Before the First Step Inside",
      "description": "Take a moment to prepare. Food, armor, escape options and information are easier to gather outside than inside a boss arena.\n\nField note: Your recommended tier is a guideline; a clever build still needs survivability and familiarity with the enemy.",
      "icon": "minecraft:iron_sword",
      "sort_order": 9,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read a dungeon's preparation and hazard notes"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trial_steel_11_learn_how_dungeon_completion_dif",
      "chapter": "trial_steel",
      "title": "Found, Fought, Finished",
      "description": "Entering a ruined fortress is one achievement. Defeating its guardian is another. Finding every secret is a third, entirely optional goal.\n\nField note: Mastery is an optional bonus; it should never block normal chapter progression.",
      "icon": "minecraft:iron_sword",
      "sort_order": 11,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Learn the difference between finding and defeating a dungeon"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trail_notes_01_scout_the_sky",
      "chapter": "trail_notes",
      "title": "A Better View",
      "description": "Great expeditions begin with a way to recognize the path home. A spyglass is small, but it can spare you a dangerous detour.\n\nBring it on your next journey. You can use another exploration tool too, but this particular optional field note tracks the vanilla spyglass.",
      "icon": "minecraft:spyglass",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:spyglass",
          "required_amount": 1,
          "name": "Carry 1 × spyglass"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 35
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trail_notes_02_the_river_route",
      "chapter": "trail_notes",
      "title": "Where Rivers Lead",
      "description": "The road is not always made of stone. A simple boat can carry you past marshes, cliffs and long stretches of unfamiliar coast.\n\nBuild or find a boat. The journal records the preparation, not the distance travelled.",
      "icon": "minecraft:oak_boat",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:oak_boat",
          "required_amount": 1,
          "name": "Carry 1 × oak boat"
        }
      ],
      "rewards": [
        {
          "type": "questlog:item",
          "item": "minecraft:bread",
          "count": 4,
          "auto_claim": false
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trail_notes_03_first_catch",
      "chapter": "trail_notes",
      "title": "A Quiet Catch",
      "description": "Not every discovery announces itself with a boss bar. Spend some time fishing. Quiet moments can reveal food, supplies and a reason to return to the water.\n\nOne fish is enough for this optional introduction.",
      "icon": "minecraft:fishing_rod",
      "sort_order": 3,
      "objectives": [
        {
          "type": "questlog:stat",
          "stat": "minecraft:fish_caught",
          "required_amount": 1,
          "name": "Catch one fish"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 40
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trail_notes_04_the_first_flame",
      "chapter": "trail_notes",
      "title": "Past the Red Threshold",
      "description": "The Nether rewards preparation and punishes confidence. Bring fire protection, a return route and a spare set of supplies.\n\nCross the threshold when you choose. This is an optional journey, not the price of joining other campaigns.",
      "icon": "minecraft:flint_and_steel",
      "sort_order": 4,
      "objectives": [
        {
          "type": "questlog:visit_dimension",
          "dimension": "minecraft:the_nether",
          "name": "Enter the Nether"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 75
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_trail_notes_05_in_the_dark",
      "chapter": "trail_notes",
      "title": "Lanterns Against the Dark",
      "description": "Caves have no sympathy for the explorer who runs out of light. Carry enough torches to turn an unexpected retreat into a short walk.\n\nThis is a supply check, not a demand to mine a specific number of stone blocks.",
      "icon": "minecraft:torch",
      "sort_order": 5,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:torch",
          "required_amount": 24,
          "name": "Carry 24 × torch"
        }
      ],
      "rewards": [
        {
          "type": "questlog:experience",
          "experience": 30
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_archaeology_01_a_delicate_tool",
      "chapter": "archaeology",
      "title": "The Patient Hand",
      "description": "A brush opens a different kind of treasure hunt. Unlike breaking blocks, careful excavation can preserve traces of older journeys.\n\nMake a brush, then investigate suspicious sand or gravel wherever you naturally encounter them. The quest verifies preparation only.",
      "icon": "minecraft:brush",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:item_obtain",
          "item": "minecraft:brush",
          "required_amount": 1,
          "name": "Carry 1 × brush"
        }
      ],
      "rewards": [
        {
          "type": "questlog:item",
          "item": "minecraft:torch",
          "count": 8,
          "auto_claim": false
        },
        {
          "type": "questlog:experience",
          "experience": 40
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_open_road_01_record_your_first_new_biome"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_archaeology_02_the_first_fragment",
      "chapter": "archaeology",
      "title": "A Story in Fragments",
      "description": "One shard can tell a story, but the surrounding place matters as much as the object. Explore warm ocean ruins, trail ruins or suspicious sands with patience.\n\nCarry one of the four known vanilla pottery sherds listed below. This is an optional collecting goal, never a mandatory random drop gate. Archaeology will receive richer rewards only after actual loot tables and modded dig sites are inspected.",
      "icon": "minecraft:brick",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:or",
          "name": "Recover one pottery sherd",
          "objectives": [
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:angler_pottery_sherd",
              "required_amount": 1,
              "name": "Carry 1 × angler pottery sherd"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:archer_pottery_sherd",
              "required_amount": 1,
              "name": "Carry 1 × archer pottery sherd"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:prize_pottery_sherd",
              "required_amount": 1,
              "name": "Carry 1 × prize pottery sherd"
            },
            {
              "type": "questlog:item_obtain",
              "item": "minecraft:skull_pottery_sherd",
              "required_amount": 1,
              "name": "Carry 1 × skull pottery sherd"
            }
          ]
        }
      ],
      "rewards": [
        {
          "type": "questlog:item",
          "item": "minecraft:emerald",
          "count": 8,
          "auto_claim": false
        },
        {
          "type": "questlog:experience",
          "experience": 180
        }
      ],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_archaeology_01_a_delicate_tool"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_archaeology_03_care_for_history",
      "chapter": "archaeology",
      "title": "Leave More Than Footprints",
      "description": "A ruin is a place, not a quarry. Mark its location, take what you need and leave enough context to remember why it mattered.\n\nRead this note once you have tried a careful excavation. The journal cannot yet detect correct preservation or thoughtful behaviour; completion here is a reading acknowledgement.",
      "icon": "minecraft:written_book",
      "sort_order": 3,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the archaeological field ethic"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_archaeology_01_a_delicate_tool"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_enigmatic_normal_01_discover_the_enigmatic_legacy_re",
      "chapter": "enigmatic_normal",
      "title": "A Peculiar Invitation",
      "description": "Some items appear ordinary until you learn what they are willing to do for you. Enigmatic artifacts reward curiosity, but not every mystery asks for a sacrifice.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: This path is separate from the Seven Curses route. You do not need to equip the cursed ring.",
      "icon": "minecraft:enchanted_book",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_enigmatic_normal_02_understand_normal_relics_versus_",
      "chapter": "enigmatic_normal",
      "title": "A Choice Not Yet Made",
      "description": "The first useful relic should teach you how unusual equipment works before you make riskier decisions. Read its effect, slot and limits carefully.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: An item's presence in JEI does not prove it is accessible without the cursed ring; verify crafting and drops.",
      "icon": "minecraft:enchanted_book",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_enigmatic_normal_01_discover_the_enigmatic_legacy_re"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_enigmatic_cursed_01_read_the_seven_curses_warning_an",
      "chapter": "enigmatic_cursed",
      "title": "The Warning on the Ring",
      "description": "Some bargains are not meant to be undone. The Seven Curses route is available to those who deliberately want a harsher game, not a rite of passage for every adventurer.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Nothing in the main campaign requires this ring. Choosing not to wear it will not close other quests.",
      "icon": "minecraft:nether_star",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the warning; no curse is activated by this quest"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_enigmatic_cursed_02_consider_alternative_normal_rout",
      "chapter": "enigmatic_cursed",
      "title": "An Unclaimed Oath",
      "description": "Possessing an object and accepting its terms are different choices. The journal will never treat picking up the ring as consent.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Keep normal artifact progression available whether or not the player chooses this branch.",
      "icon": "minecraft:nether_star",
      "sort_order": 2,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the warning; no curse is activated by this quest"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_enigmatic_cursed_01_read_the_seven_curses_warning_an"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_dream_01_find_a_rumor_about_the_dream_rif",
      "chapter": "dream",
      "title": "The Shape of a Dream",
      "description": "Beyond familiar terrain lies a world that does not follow familiar rules. Before crossing into it, find out which dreams are actually reachable in this version.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: This entry will stay hidden until the pinned NeoPasterDream 0.9.6 realm access is verified.",
      "icon": "minecraft:amethyst_shard",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_aquamirae_01_plan_an_ice_ocean_expedition",
      "chapter": "aquamirae",
      "title": "The Sea Has Teeth",
      "description": "A cold sea can conceal far more than ice and wreckage. Pack for the journey, and assume that the first strange shape beneath the water is a warning.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Bring a safe return method. Swimming deeper is not the same as being ready for the thing living below.",
      "icon": "minecraft:heart_of_the_sea",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_ars_01_craft_a_basic_spellbook",
      "chapter": "ars",
      "title": "A Page of Spells",
      "description": "Magic does not begin with spectacular damage. It begins with a book, a simple glyph and the ability to combine effects deliberately.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: The Field Manual explains glyph syntax step by step. This adventure only tracks the major milestone.",
      "icon": "minecraft:enchanting_table",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_iron_magic_01_obtain_a_starter_spellbook",
      "chapter": "iron_magic",
      "title": "Ink, Paper, Power",
      "description": "The first spell you cast will not be the strongest one you ever know. Learning what a spell costs is just as valuable as learning what it does.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Start with a spell you can reliably cast and recharge. Look up spell schools in the Field Manual.",
      "icon": "minecraft:blaze_rod",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_twilight_01_find_how_to_open_a_twilight_port",
      "chapter": "twilight",
      "title": "A Forest Out of Place",
      "description": "Some forests do not belong to this world. Their paths branch toward ruins and creatures that expect preparation rather than courage alone.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Do not assume the first boss is optional to a specific Twilight portal progression gate until verified.",
      "icon": "minecraft:oak_sapling",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    },
    {
      "id": "ao_end_eyes_01_understand_that_eyes_may_come_fr",
      "chapter": "end_eyes",
      "title": "Eyes from Many Roads",
      "description": "Reaching the End should feel like the result of several adventures, not a single uninteresting shopping list. The paths to an Eye are meant to differ.\n\nThis is an introductory reading entry ONLY. It does not claim the dimension was entered, a boss was defeated, a relic was equipped, or any reward has been earned. Runtime-verified item/structure objectives will be authored later.\n\nField note: Collect eligible eyes through different optional journeys. Do not assume every named eye is mandatory.",
      "icon": "minecraft:ender_eye",
      "sort_order": 1,
      "objectives": [
        {
          "type": "questlog:read",
          "name": "Read the optional campaign introduction"
        }
      ],
      "rewards": [],
      "prerequisites": [
        {
          "type": "questlog:quest_complete",
          "quest": "questlog:ao_first_pages_01_welcome_to_ambient_odyssey"
        }
      ],
      "repeatable": false,
      "global": false
    }
  ]
};
