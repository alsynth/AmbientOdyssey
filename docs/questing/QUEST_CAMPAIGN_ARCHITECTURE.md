# Ambient Odyssey — Quest Campaign Architecture (planning v0.1)

**Created:** 10 October 2026 · **Engine under evaluation:** Infernal Studios Questlog 3.4.1 (NeoForge 1.21.1); FTB Quests as the *educational reference book*. **No production Questlog installed or quest definitions authored yet.** This is a **content and milestone map**, not validated live quest identifiers.

## Player experience / overarching rules

1. **An adventurous journal, not an errand log.** Each major quest advances the player's relationship with the world: first encounter, meaningful skill acquired, danger prepared for, boss confronted, important reward explored. Avoid tedious "craft 500 blocks" objectives.
2. **Main campaign is compact and beginner-friendly**, about 80–140 eventual substantive quests across Tier 0–8, with several independent optional arcs rather than requiring every dimensional mod. Almost all major mod-specific quests belong to separately startable optional chapters.
3. **Questlog owns story/milestone content. FTB Quests owns education.** Questlog offers a short explanation and optionally opens/refers to the relevant FTB chapter for recipes, controls, upgrade recipes, pages of material tables, alternative build setups and screenshots. Avoid two identical fetch quests and two copies of reward payouts.
4. **Quest triggers must represent something that happened:** `visit_structure`, `visit_biome`, `visit_dimension`, `entity_kill`, `item_obtain`, `advancement`, `quest_complete`, plus command/triggers only where needed. Do not assume "placed a block", "cleared room", "used a skill" or "completed dungeon" has an automatic built-in objective type; verify predicate.
5. **No one Origin, discipline, armor set, weapon school or cursed mode is required.** Quest completion paths should be compatible with different Origins / class configurations and co-op formations. AO boss tier is a *recommended gear benchmark*, not a hard gate for exploration.
6. **Per-player quest progress on a private server.** Questlog's saves are per UUID by source, but shared boss kill contribution / completion credit, death, logout and restart all need live multi-user testing. FTB Solo Quests is currently staged for a different purpose; its behavior does not prove Questlog integration.
7. **Avoid RNG hostage quests.** Being unable to find a rare biome/structure after hours should not block the next chapter. Major optional encounters are allowed to be truly rare; the required backbone always has alternate routes.
8. **Show impending danger without spoilering unknown secrets.** New location → short journal message → approximate boss tier, environmental hazard and recommended equipment band; hidden loot remains hidden until discovered.
9. **Respect previously rejected features.** No exploration museum, Lost Expedition Stories/multi-location narrative, bespoke Party Expedition Planner, World-First Discovery Records, mandatory guilds or scheduled world events. Optional contracts/rumors/field notes remain allowed.
10. **Balance targets:** Tier 2 assumes enchanted diamond armor and >=2 grade-A combat-support items. Relics, Enigmatic Legacy, Origins and advanced spells can change real readiness; the Atlas later supplies calibrated gear advice.
11. **Progression chapter boundaries should be navigable, not restrictive.** Do not forbid a player entering a higher-tier location early; reveal danger and track discoveries independently of defeats.

## Three layers

### Layer I — The main adventure (Questlog)

| Proposed chapter | Rough AO tier | Why it exists | Representative milestones | Rough target |
|---|---|---|---|---:|
| **The First Pages** | 0 | Newcomer onboarding and real UI discovery | Find JEI uses/recipes, craft shield and bag, understand Curios, eat safely, learn claim/map basics | 10–16 |
| **The Open Road** | 1 | Explore naturally rather than grind | Discover distinct biomes, find village/ruin, improve travel, establish safe expedition kit | 10–15 |
| **Trial by Steel** | 2 | First demanding combat thresholds | Get enchanted diamond, acquire two useful combat supports, beat first curated dungeon/boss | 10–14 |
| **The Wider World** | 3 | Choose first personal specialism and elective dimension | Earn first notable enchanted weapon, try a magic/weapon style, investigate a distinct region | 10–16 |
| **The Threshold** | 4 | Prepare for meaningful dungeon chains | Nether/stronghold/early optional realm challenge and more developed combat loadout | 8–14 |
| **Old Powers** | 5 | Substantial encounter progression | Midgame expedition and spell/relic upgrades, first Cataclysm encounters | 8–14 |
| **The Legendary Hunt** | 6 | High-risk fights | Ignis and other curated tier-6 threats, endgame forging | 8–14 |
| **The Breaking Point** | 7 | Extreme endgame | Maledictus and high-end bosses, deep mastery | 6–12 |
| **Beyond the Known** | 8 | Optional final superbosses | Scylla, Echo of Tyros and selected final encounters, mastery | 6–12 |

**Total rough backbone 76–127** quests, intentionally not a requirement to complete every optional world or mod. Exact bosses must follow the latest AO Progression Atlas and runtime encounter inventory.

### Layer II — Large optional campaigns (Questlog)

| Optional quest line | Relevant mods | Approx. quest goal | Examples of beats |
|---|---|---:|---|
| **The Twilight Path** | Twilight Forest | 20–35 | Portal, progression biomes, naga, towers, labyrinths, boss ladder |
| **Kingdoms of the Sky** | Aether, Deep Aether, Aether Villages | 18–32 | Portal, resources, sky dungeons, bosses, optional Deep Aether research |
| **The Starlit Frontier** | Eternal Starlight | 16–30 | Portal, biomes, key structures, enemies, boss progression |
| **Below the Bedrock** | Undergarden, Deeper and Darker | 12–28 each | Access, exploration, unique loot, major dangers |
| **The Bumblezone** | Bumblezone | 8–18 | Entry, special ecology, hive discoveries, non-boss alternatives |
| **The Six Cave Expeditions** | Alex's Caves | 18–35 | Cave discovery, unique creatures/resource systems, major encounters |
| **Dreamseeker's Notes** | NeoPasterDream 0.9.6 | 25–55 | Dream access, diary pages, Dyed Dreamscape, Shadow Lanterns, wind realm where available, cold realm, workshop, Aaroncos / end encounter; **exact feature set version audit mandatory** |
| **The Seven Curses (opt-in)** | Enigmatic Legacy Plus | 12–25 | Optional ring explanation and explicit player choice, separate cursed recovery/power progression; no forced initiation |
| **The Relic Scholar (normal)** | Enigmatic Legacy Plus | 10–22 | Non-cursed enigmatic artifacts, relics, puzzles and crafting; must stay accessible without cursed ring |
| **Frozen Seas** | Aquamirae, Ice and Fire, ocean content | 10–23 | Prepare for icy waters, ice maze, ship graveyard, pirates, Eel, Mother of Maze, Cornelia |
| **The Arcane Academy** | Ars Nouveau | 12–25 | Glyphbook, basic spells, magical discovery, rituals and upgrades |
| **The Spellwright's Journey** | Iron's Spells, Traveloptics, Cataclysm Spellbooks | 14–30 | First spellbook, spell school, towers, battle mages, boss-linked rewards and spells |
| **Forbidden Research** | Forbidden & Arcanus, Astrological | 10–22 | Magical resources, signature items, structures, optional encounters |
| **The Dragon Hunter** | Ice and Fire | 12–25 | Recognize dragons, survive raids/roosts, cave encounter and exceptional equipment |
| **A Hunter of Legends** | L_Ender's Cataclysm, BOMD, Mowzie's, Remnant, FD bosses, Bosses' Rise, Gateways | 30–65, split by tier | Encounter dossier, optional boss families, reforge trophies/gear, no global leaderboard |
| **Weapon and Relic Mastery** | Apotheosis, Simply Swords/More, Relics, More Relics, Artifacts, Iron's Jewelry | 14–35 | Unlock selected weapon/relic systems, forge viable loadout, nonmandatory mastery |
| **The Eyes of the End** | End Remastered, Integrated Stronghold | 12–24 | Diverse eye sources and the eventual End approach, with flexibility for sources |
| **Oceanographer** | Hybrid Aquatic, FTB Ocean Mobs, YUNG Ocean Monument, Better Shipwrecks, Small Ships, Deeper Oceans | 8–20 | Ship journey, marine hazards, biomes, monuments, deep-sea loot; scenic content without kill-everything |

**Do not double-count** Cross-mod campaigns as if each constituent addon requires its own separate chapter. This is a content budget, **not a promise that all candidate encounters spawn or are complete**.

### Layer III — Curated anthologies and compact sidequests (Questlog)

- **The Explorer's Atlas:** Overworld biomes, naturally discovered unique structures, major villages, towers, bridges, floating islands, underwater ruins, rare sights. Source mods include WDA, Seven Seas, Dungeon Crawl, Adventure Dungeons, IDAS, Additional Structures, Explorify, Archaion, Dungeons and Taverns, Phillip's Ruins, Repurposed Structures, Moog's structures, Farmer's Structures, YUNG, Sky Villages, Structory, etc. Use **location types** and *representative* serious challenges, not a checklist of every generated roof variant.
- **The Nether and End:** Incendium, BetterEnd, Better Bastions, YUNG fortresses/End island, End Remastered, Echoes of the End, Moog's End structures, modern dragon arena.
- **Creature field notes:** Alex's Mobs, Opposing Force, Hominid, Hybrid Aquatic, Friends & Foes, Ben's Sharks, rare/boss mobs. Observe unusual creatures and choose challenging fights; no massacre of ambient animals.
- **Daily-life cameos:** Create, Farmer's Delight plus cooking addons, sophisticated storage/backpacks, Aquaculture, Goblin Traders, Bountiful and shipbuilding. One to four thoughtful sidequests at most; offer FTB manual for serious Create complexity.
- **Origin/discipline identity:** future Origin and combat specialty onboarding, lightweight quests, conditional branches. Currently hypothetical: must wait for installed backend/Origin decisions.
- **Bonus challenge scrolls:** Gateways, arena variants, personal boss speed/no-death (only if credit technically supportable), cursed ring advanced feats. Completely optional.

## FTB Quests — educational-only architecture

Avoid duplicating complete Questlog campaigns. Use FTB **as a searchable illustrated field manual**, organized by subject:
1. **Minecraft/JEI survival for newcomers:** item uses, recipes, tooltips, dropping stacks, off-hand/shields, Minecraft enchantments, safe nighttime and coordinates.
2. **Traveler's kit:** backpacks, Waystones, maps, Curios/accessory slots, Lootr/individual chests, navigation, death recovery, map sharing and server rules.
3. **Combat systems:** Better Combat / weapon reach and animations, combat control, potion/status handling, boss danger indicators, gear tiers and resistances.
4. **Apotheosis & enchanting:** enchanting table stats, mob affixes, reforging, gems/socketing, Salvaging, rarity/affix weighting and safe upgrades.
5. **Relics & Artifacts:** items vs slots, attunement/level scaling, effect triggers, stack constraints and synergies; links to Gear Atlas combat-support grades.
6. **Magic encyclopedia:** Iron's spells school tree, acquiring spells, spellbooks/slots/mana; Ars Nouveau glyph crafting, spell composition, rituals, automation; Forbidden & Arcanus and boss-spell integrations.
7. **Optional niche systems:** Create kinetic power, farms/cooking, storage automation, fishing, improved crafting, special Portal / multiblock rules.
8. **World/dimension reference:** what to expect in new realms and basic portal prerequisites, without spoiling optional encounters.
9. **RPG character systems (later):** Origin passives/tradeoffs, background and discipline interactions, future respec.
10. **Server quality & multiplayer:** permissions, separate quests, map/waypoint rules, how to ask for help, keybind troubleshooting.
11. **Quest mechanics itself:** where to open Questlog, how prerequisites/rewards work, how to pin/find FTB reference, avoiding auto-complete/achievement confusion.

**FTB reference should have few or no reward-bearing tasks.** If a small hands-on teaching step is helpful, award once only in Questlog or in FTB — never both.

## A beginner-friendly quest design pattern

A main quest should be readable in under ~30 seconds and contain:
- What was discovered/why it matters, in two sentences or fewer.
- One unambiguous objective, with one optional longer description when needed.
- One contextual danger/gear hint, matched to AO tier.
- Where to learn the mechanics (FTB lesson or JEI guidance).
- If branching, disclose that alternative quests exist; never pretend every mod is compulsory.
- A single meaningful unlock or reward that doesn't break early progression.

**Example (not a final implementation):** "A Forgotten Tower" → find an actual naturally generated tower/structure; journal says *Recommended armor: Tier 2, diamond with strong enchantments*; player may investigate, leave a personal bookmark and return when ready. Completion on discovery, not boss death. Later optional quest recognizes kill or advancement evidence.

## Player flow and technical implementation notes

- **Suggested UI entry:** Questlog inventory button and keybind; optional FTB manual hotkey. Two clear labels *Adventures* vs *Field Manual*.
- **Novelty control:** About 2–5 automatically revealed goals at once, with optional branches browsable. For a 1000-quest book, avoid first-spawn 1000 quest toasts.
- **Separate authored data:** Questlog: JSON in `config/questlog/chapters/` and `config/questlog/quests/`. FTB: its current SNBT format in `config/ftbquests/quests/`.
- **Generated source of truth:** preferably author YAML/JSON/CSV seed registry in Git, validate IDs/graph/difficulty and generate Questlog JSON and FTB manual pages. Do not edit generated outputs only.
- **Questlog location objectives** can poll each active quest on player tick; avoid ~1000 simultaneous biome and structure polling quests. Hidden/locked quests need objective-registration code test before assuming absence of CPU cost.
- **Registry and feature verification per quest:** real mod id, structure/entity/item id, current actual JAR, loot/drop source, any quest trigger/reward effects, NPC/boss access, natural spawn and dimension limitations.
- **No fake real-time build claims.** Source audit and chapter/seed counts are planning coverage only; all functional acceptance requires client and server tests.

## Inspiration — patterns, not copied quest text

- **Cisco's Medieval RPG:** a primary champion-trial route plus independent boss, travel and magic branches; use flexible choices rather than one enormous dependency chain. https://ciscos-rpg.fandom.com/wiki/Quests
- **Integrated Minecraft:** thematic structure quests, exploration reward recipes, maps and conditional hidden objectives. Transfer the *design pattern* only, not text, assets or private datapacks. https://www.curseforge.com/minecraft/modpacks/integrated-minecraft
- **Prominence II:** character onboarding, readable RPG presentation and discoverable optional quest chains. Avoid importing its kingdom/guild/story modes. https://www.curseforge.com/minecraft/modpacks/prominence-2-hasturian-era
- **Questlog 3.4.1 developer docs:** triggers, chapters, objectives, rewards, rich visual descriptions, optional notifications. https://github.com/infernalstudios/Questlog/tree/1.21.1/docs/questlog

## Open audits

- Exact current Test8.3 mod JAR list against the historical 196+41 inventory / source-lock additions. Source roster includes removed and repinned content; use provenance columns and never infer every candidate is installed.
- Detailed mod feature lists for 0.9.6 NeoPasterDream; current CurseForge description may describe 0.10 beta features. Verify first.
- Each Enigmatic Legacy 1.1.2 item's crafting, curses and noncurse access (and actual user profile config); some curse-related items may be locked.
- Decide Questlog-only vs two-book approach after small dedicated-server test (no approved install now). User currently leans Questlog adventures + FTB educational.
- Calibrate exact spawn/loot and gear readiness using the AO Boss/Progression Atlas and server testing.
- Map all 249 provisional named mod entries to actual installed CurseForge IDs/JAR checksums before claiming 1:1 exact-mod audit.
