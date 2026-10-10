# Ambient Odyssey 0.4c — Wildlife & Friendly Mob Audit (source-verified)

**Date:** 10 October 2026. **Baseline:** actual 0.4.0-b1 user client `latest(20261010-143535).log`; next 0.4c curated baseline excludes Galosphere but retains Naturalist, Better Archeology, ocean animal mods and Cosy Critters. **Native source proof:** [GitHub installed-JAR entity extraction](https://github.com/alsynth/AmbientOdyssey/actions/runs/38060841765), [Naturalist 2.0.5 SHA-pinned extraction](https://github.com/alsynth/AmbientOdyssey/actions/runs/38060695730), exact `alexsmobs.toml` 88 spawn weights. Original files were inspected as metadata only; **no author JARs or textures redistributed**.

## How to interpret the roster

A translated `entity.*` label shows **the creature is registered**, not that it is friendly, spawns naturally, or fills a passive animal cap. The long source-complete registers below deliberately include neutral predators, dangerous wildlife, technical invisible entities, and creatures with 0 natural spawn weight. **Do not count every listed name as a peaceful animal**. To make decisions easier, the first sections distinguish gentle wildlife, neutral/dangerous wildlife, monsters/bosses, and *purely visual* ambience. Source label listings are provided for audit completeness.

### Our aim
- **Familiar wildlife and genuinely useful animals**: birds, deer, rabbits, small reptiles, grazers, interesting sea life, and an occasional memorable encounter. Not 10 copies of each predator.
- **Small irritating pests**: flies/cockroaches/ant swarms/rat swarms are poor use of server spawn budget in a scenic RPG exploration pack; client-only bug effects may be more appropriate. User specifically does **not** want gorillas or pests.
- **Ocean priority**: Hybrid Aquatic is the main *living ecosystem*, Ben's Sharks for select impressive predator encounters, Alex's Mobs for distinct gameplay (e.g. tame/fish/item behaviors), Aquaculture for fishing and turtles. **Naturalist's ocean duplicates should be heavily pruned** rather than allowing every mod to spawn great white sharks, blobfish, catfish, etc.
- **No premature wholesale mod removal:** disabling natural spawn weights is reversible and normally safer than deleting the mod/registries or breaking recipes. Where config route is not proven, hold candidate for native-code/spawn audit.

## Decisions that have already been implemented in 0.4c source

| Decision | Status | Why |
|---|---|---|
| Alex's Mobs `gorillaSpawnWeight=0` | **Applied** | Explicit user request, prevents *natural* spawning, does not remove spawn egg/entity/loot registry |
| Alex's Mobs `flySpawnWeight=0` | **Applied** | Ambient sound/client Cosy Critters already supplies insects; low-value physical nuisance |
| Alex's Mobs `cockroachSpawnWeight=0` | **Applied** | Low-value pest/extra mob behavior |
| Naturalist rat / ant / giant isopod / piranha / generic shark or big-cat duplicate spawns | **Review after native spawn-rule attribution**, not yet removed | Naturalist uses custom `naturalist:add_animals` modifier; replacing arbitrary JSON can remove *all* wildlife unless the exact per-mob config is understood |
| Galosphere 1.5.5 | **Removed from next release** | User says its caves aren't needed, preserve existing Alex's Caves and established worldgen |
| Cosy Critters | **KEEP** | Client visual birds/moths/spiders, **not live server animal entities** and should not be counted against server passive mob caps |
| MineColonies | **Do not add** | User doesn't want it; extensive colony AI and conflicting settlement purposes |
| MCA Reborn | **Park for later** | User is undecided; not needed for current Guard Villagers/Easy NPC phase |

## Exact same-species overlap — names registered in **multiple installed wildlife mods**

| Species | Installed sources | Suggested direction |
|---|---|---|
| Blobfish | Hybrid Aquatic 1.7.4 · Naturalist 2.0.5 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Great White Shark | Hybrid Aquatic 1.7.4 · Ben's Sharks 1.2.6 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Piranha | Hybrid Aquatic 1.7.4 · Aquaculture 2.7.21 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Catfish | Aquaculture 2.7.21 · Naturalist 2.0.5 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Anglerfish | Hybrid Aquatic 1.7.4 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Barracuda | Hybrid Aquatic 1.7.4 · Ben's Sharks 1.2.6 | Review biome/spawn density, keep distinct gameplay roles |
| Basking Shark | Hybrid Aquatic 1.7.4 · Ben's Sharks 1.2.6 | Review biome/spawn density, keep distinct gameplay roles |
| Bull Shark | Hybrid Aquatic 1.7.4 · Ben's Sharks 1.2.6 | Review biome/spawn density, keep distinct gameplay roles |
| Carp | Hybrid Aquatic 1.7.4 · Aquaculture 2.7.21 | Review biome/spawn density, keep distinct gameplay roles |
| Comb Jelly | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Flying Fish | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Frilled Shark | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Giant Isopod | Hybrid Aquatic 1.7.4 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Giant Squid | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Hammerhead Shark | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Lobster | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Orca | Hybrid Aquatic 1.7.4 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Starfish | Hybrid Aquatic 1.7.4 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Tuna | Hybrid Aquatic 1.7.4 · Aquaculture 2.7.21 | Review biome/spawn density, keep distinct gameplay roles |
| Whale Shark | Hybrid Aquatic 1.7.4 · Ben's Sharks 1.2.6 | Review biome/spawn density, keep distinct gameplay roles |
| Crab | Friends & Foes 4.0.27 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Jellyfish | Aquaculture 2.7.21 · Naturalist 2.0.5 | Review biome/spawn density, keep distinct gameplay roles |
| Elephant | Naturalist 2.0.5 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Komodo Dragon | Naturalist 2.0.5 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Tiger | Naturalist 2.0.5 · Alex's Mobs | Review biome/spawn density, keep distinct gameplay roles |
| Rhinoceros / Rhino | Alex's Mobs; Naturalist | Prefer one source's biome spawn budget; don't automatically kill either entity |
| Whale / Cachalot Whale | Naturalist; Alex's Mobs; Hybrid Aquatic has Orca and other sea mammals | Special encounter weight, avoid routine whale pods |
| Sharks (several kinds) | Ben's Sharks; Hybrid Aquatic; Alex's Mobs; Naturalist | Choose a few species per zone and mod; ocean predator density should be low |

**Do not confuse** similar taxonomy (e.g. great white versus hammerhead) with an exact duplicate; the table's exact matches use normalized localized labels. Two mobs sharing a name can have different mechanics, loot and animation.

## Focused *peaceful / neutral / friendly encounter* shortlist

**Land:** Naturalist deer, ducks, turkeys, birds, zebra, giraffe, capybara, hedgehog, tortoise, mole, snails, butterflies and fireflies; Alex's Mobs hummingbird, roadrunner, gazelle, capuchin monkey, toucan, bald eagle, jerboa, sugar glider, moose, bison, platypus, rain frog and blue jay; Friends & Foes moobloom, glare, copper golem and tuff golem; Mowzie's Grottol (cave crystal creature), Lantern and trader-like Umvuthi. **Bears, boars, hippos, elephants, big cats, rhinos, lizards and reptiles may defend themselves or prey on things**; keep under neutral/dangerous until code/spawn testing proves behavior.

**Water:** Hybrid Aquatic schools of small reef/riverside fish, seahorses, sea angels, seadragon, garden eels, rays, dugong, manatee, otter, starfish, small crabs, jellyfish, octopus and many fish; Aquaculture fish and turtles; select Ben's Sharks krill, pilot fish, remora, whale and basking sharks. **Sharks, lionfish, piranhas, anglerfish and some squid/crabs are encounters, not presumed peaceful.** Prioritize underwater readability and fair spawn density.

**Client-only ambience:** Cosy Critters bird flocks, moths, cobweb spiders, optional Hat Man—visual effects *not mob entity population*. Atmosfera is an audio mod and does **not** add wildlife entities.

## Source-complete mod registries (includes aggressive, technical and non-natural entries!)

### Naturalist 2.0.5 — 47 distinct localized names

`Alligator` · `Anglerfish` · `Ant` · `Bass` · `Bear` · `Bird` · `Black Bear` · `Blobfish` · `Boar` · `Butterfly` · `Capybara` · `Caterpillar` · `Catfish` · `Clam` · `Crab` · `Deer` · `Desert Scorpion` · `Dragonfly` · `Duck` · `Elephant` · `Firefly` · `Giant Isopod` · `Giraffe` · `Great White Shark` · `Hedgehog` · `Hippo` · `Jellyfish` · `Jungle Scorpion` · `Komodo Dragon` · `Lion` · `Lizard` · `Mammoth` · `Mole` · `Ostrich` · `Piranha` · `Rat` · `Ray` · `Rhino` · `Snail` · `Snake` · `Starfish` · `Tiger` · `Tortoise` · `Turkey` · `Vulture` · `Whale` · `Zebra`

### Hybrid Aquatic 1.7.4 — 132 distinct localized names

`African Butterflyfish` · `Anglerfish` · `Argonaut` · `Arrow Squid` · `Barracuda` · `Barrel Jellyfish` · `Barreleye` · `Basking Shark` · `Beakling` · `Betta` · `Big Red Jellyfish` · `Blobfish` · `Blowfish` · `Blue Jellyfish` · `Box Jellyfish` · `Boxfish` · `Bull Shark` · `Carp` · `Cepheidae Jellyfish` · `Cichlid` · `Clownfish` · `Coconut Crab` · `Coelacanth` · `Colossal Squid` · `Comb Jelly` · `Corydora` · `Cosmic Jellyfish` · `Crayfish` · `Crown Jellyfish` · `Cuttlefish` · `Damselfish` · `Danio` · `Decorator Crab` · `Discus` · `Dragonfish` · `Dugong` · `Dungeness Crab` · `Fangtooth` · `Fiddler Crab` · `Firefly Squid` · `Firework Jellyfish` · `Flashlight Fish` · `Flower Crab` · `Flying Fish` · `Frilled Shark` · `Garden Eel` · `Ghost Crab` · `Giant Isopod` · `Giant Squid` · `Goblin Shark` · `Golden Dorado` · `Goldfish` · `Gourami` · `Great White Shark` · `Hagfish` · `Hammerhead Shark` · `Hatchetfish` · `Hermit Crab` · `Herring` · `Horseshoe Crab` · `Hound Shark` · `John Dory` · `Karcinogen` · `Karcinoma` · `Karkinos` · `Lantern Shark` · `Lightfoot Crab` · `Lionfish` · `Lion's Mane Jellyfish` · `Lobster` · `Mackerel` · `Mahi` · `Manatee` · `Manta Ray` · `Mauve Stinger` · `Moon Jellyfish` · `Moray Eel` · `Nautilus` · `Needlefish` · `Nomura Jellyfish` · `Oarfish` · `Ocean Sunfish` · `Octopus` · `Opah` · `Orca` · `Otter` · `Parrotfish` · `Pearlfish` · `Piranha` · `Pleco` · `Pupfish` · `Ratfish` · `Rockfish` · `Sand Tiger Shark` · `Scalyfoot Snail` · `Sea Angel` · `Sea Bass` · `Sea Cucumber` · `Sea Nettle` · `Sea Slug` · `Sea Urchin` · `Seadragon` · `Seahorse` · `Shell Beast` · `Shiner` · `Shrimp` · `Sixgill Shark` · `Sleeper Shark` · `Slickhead` · `Snailfish` · `Spider Crab` · `Squirrelfish` · `Starfish` · `Stingray` · `Stonefish` · `Sunfish` · `Surgeonfish` · `Tetra` · `Thresher Shark` · `Tiger Barb` · `Trevally` · `Triggerfish` · `Tripod Fish` · `Trout` · `Tuna` · `Umbrella Octopus` · `Vampire Crab` · `Vampire Squid` · `Viperfish` · `Whale Shark` · `Wrasse` · `Yeti Crab`

### Ben's Sharks 1.2.6 — 24 distinct localized names

`Axodile` · `Barracuda` · `Basking Shark` · `Blacktip Reef Shark` · `Blue Shark` · `Bonnethead Shark` · `Bull Shark` · `Cookiecutter Shark` · `Greater Axodile` · `Great White Shark` · `Greenland Shark` · `Krill` · `Land Shark` · `Lemon Shark` · `Mako Shark` · `Megalodon` · `Nurse Shark` · `Pilot Fish` · `Remora` · `Thalassoger` · `Tiger Shark` · `Whale Shark` · `Oceanic Whitetip Shark` · `Shark`

### Aquaculture 2.7.21 — 38 distinct localized names

`Acacia Fish Mount` · `Arapaima` · `Arrau Turtle` · `Atlantic Cod` · `Atlantic Halibut` · `Atlantic Herring` · `Bayad` · `Birch Fish Mount` · `Blackfish` · `Bluegill` · `Boulti` · `Box Turtle` · `Brown Shrooma` · `Brown Trout` · `Capitaine` · `Carp` · `Catfish` · `Dark Oak Fish Mount` · `Gar` · `Jellyfish` · `Jungle Fish Mount` · `Minnow` · `Muskellunge` · `Oak Fish Mount` · `Pacific Halibut` · `Perch` · `Pink Salmon` · `Piranha` · `Pollock` · `Rainbow Trout` · `Red Grouper` · `Red Shrooma` · `Smallmouth Bass` · `Spruce Fish Mount` · `Starshell Turtle` · `Synodontis` · `Tambaqui` · `Tuna`

### Friends & Foes 4.0.27 — 10 distinct localized names

`Copper Golem` · `Crab` · `Glare` · `Iceologer` · `Illusioner` · `Mauler` · `Moobloom` · `Rascal` · `Tuff Golem` · `Wildfire`

### Mowzie's Mobs 1.8.2 — 16 distinct localized names

`Baby Foliaath` · `Bluff` · `Boulder` · `Elokosa` · `Elokosa Howler` · `Ferrous Wroughtnaut` · `Foliaath` · `Frostmaw` · `Grottol` · `Lantern` · `Naga` · `Tongbi, the Sculptor` · `Umvuthana` · `Umvuthana Crane` · `Umvuthana Raptor` · `Umvuthi, the Sunbird`

### FTB Ocean Mobs 21.1.4 — 11 distinct localized names

`Abyssal Sludge` · `Abyssal Winged` · `Corrosive Craig` · `Mossback Goliath` · `Rift Demon` · `Rift Minotaur` · `The Rift Weaver` · `Riftling Observer` · `Shadow Beast` · `Sludgeling` · `Tentacled Horror`

**Special rule:** FTB Ocean Mobs explicitly has **no default natural spawning and no default loot**, per author description; its listed creatures are hostile/adventure content candidates, not passive wildlife.

### Hominid 1.3.4 — 7 distinct localized names

`Bellman` · `Famished` · `Fossilized` · `Incendiary` · `Juggernaut` · `Mellified` · `Vampire`

**Classification:** hostile undead humans, **not friendly wildlife**; included because it adds mobs to natural environments.

### Alex's Mobs 1.22.9 — 88 configured spawn entries

`grizzly Bear` · `roadrunner` · `bone Serpent` · `gazelle` · `crocodile` · `fly` **[disabled natural spawn]** · `hummingbird` · `orca` · `sunbird` · `gorilla` **[disabled natural spawn]** · `crimson Mosquito` · `rattlesnake` · `endergrade` · `hammerhead Shark` · `lobster` · `komodo Dragon` · `capuchin Monkey` · `cave Centipede` · `warped Toad` · `moose` · `mimicube` · `raccoon` · `blobfish` · `seal` · `cockroach` **[disabled natural spawn]** · `shoebill` · `elephant` · `soul Vulture` · `snow Leopard` · `spectre` · `crow` · `alligator Snapping Turtle` · `mungus` · `mantis Shrimp` · `guster` · `warped Mosco` · `straddler` · `stradpole` · `emu` · `platypus` · `dropbear` · `tasmanian Devil` · `kangaroo` · `cachalot Whale` · `enderiophage` · `bald Eagle` · `tiger` · `tarantula Hawk` · `void Worm` **[disabled natural spawn]** · `frilled Shark` · `mimic Octopus` · `seagull` · `froststalker` · `tusklin` · `laviathan` · `cosmaw` · `toucan` · `maned Wolf` · `anaconda` · `anteater` · `rocky Roller` · `flutter` · `gelada Monkey` · `jerboa` · `terrapin` · `comb Jelly` · `cosmic Cod` · `bunfungus` · `bison` · `giant Squid` · `devils Hole Pupfish` · `catfish` · `flying Fish` · `skelewag` · `rain Frog` · `potoo` · `mudskipper` · `rhinoceros` · `sugar Glider` · `farseer` · `skreecher` · `underminer` · `murmur` · `skunk` · `banana Slug` · `blue Jay` · `caiman` · `triops`

### Other installed mods with creatures but not primary *passive ecology* owners

- **Alex's Caves:** unusual biome-specific cave creatures and monsters, not a broad peaceful-surface population source. Its actual JAR's passive subset (e.g. cave prehistoric ecosystem) requires separate enumeration.
- **Aquamirae:** Golden Moth and Spinefish are passive/ambient; anglerfish, Maw, Eel and Maze encounters are hostile/mini-boss content.
- **Ice and Fire:** Pixies, hippocampi/hippogryphs and other potentially tamable or friendly mythical creatures exist alongside dragons/sirens/trolls. Preserve their special fantasy roles rather than compare them to ordinary wildlife.
- **Aether, Twilight Forest, Undergarden, Deeper & Darker, Eternal Starlight, Bumblezone and other dimensions:** biome- or realm-specific animals and companions are part of their **dimension exploration** roster, not candidates to disable globally for Overworld spawncap reasons.
- **Guard Villagers, Easy NPC Core/UI, Villager Names:** friendly/neutral **settlement NPC mechanics**, not wild fauna; preserve for inhabited settlements.
- **Cosy Critters:** birds/moths/spider effects are client atmosphere and not server entities; don't conflate these with Naturalist server-spawned butterflies/birds.
- **Galosphere:** previously present in 0.4.0-b1, **intentionally removed** in 0.4c; not counted in the upcoming pack.
- **FTB Ocean Mobs, Hominid, Mowzie's other monsters, Aquatic Creepers:** not counted as passive wildlife; treat as encounter/boss content instead.

## Proposed next ecology balancing pass (not all changes deployed yet)

1. **Remove redundant passive fauna spawns only when mod/biome owner's configured registration is known:** Naturalist Great White Shark, Anglerfish, Blobfish, Catfish, Jellyfish, Crab, Piranha, Ray, Starfish overlap Hybrid/Aquaculture. Naturalist tiger/rhino/elephant overlap Alex's Mobs. Candidate at least try a **single canonical source per habitat**, but preserve mod-specific drops/recipes and spawned special-case entities.
2. **Pests:** Current Alex's flies and cockroaches are zero; Naturalist ants and rats are future disable candidates after its registered `naturalist:add_animals` policy is inspected. Don't unilaterally disable all butterflies/fireflies; they add low-threat atmosphere when density kept small.
3. **Ben's Sharks:** Keep large unique predator encounters including megalodon/axodile; reduce ordinary shark duplicates in shared seas if actual spawncap measurements show crowding.
4. **Use biome tags not pure rarity if biome eligibility missing:** Test Forest, Meadow, Tropical, Cold, Swamp, Rivers, Reef, Deep Ocean and underground; each one should have its appropriate ecosystem. Avoid 100 mobs around spawn but empty modded biomes.
5. **Server sanity:** natural versus spawned mobs should be counted separately; measure `/spark` MSPT + passive/entity counts on 5–7-player equivalent distribution; don't claim entity duplication is a bug merely because two mods share species names.

**Sources:** Native installed JARs as exactly identified in the two GitHub Actions registry audits linked above; user-provided Test8.10 roster; [FTB Ocean Mobs official spawn policy](https://www.curseforge.com/minecraft/mc-mods/ftb-ocean-mobs). **Limit:** exact initial friendly/hostile attributes and actual natural spawn selection are behavior/runtime questions—language files aren't AI source code.
