# Arena check guide (worldgen freeze)

## 0. Which variant of the arenas is active? (one command)

Cataclysm and Integrated Cataclysm (and BOMD and IBOMD) both define the same boss arenas. In the world, run `/datapack list enabled` and send the output. The packs are listed in priority order; the **later** one wins, and we want `mod/integrated_cataclysm` (and the IBOMD pack) **after** the original.

## 1. Run the automated locate check

Use a **fresh world with the final AO world preset** (not Superflat; worldgen settings frozen), creative, cheats on. Put `AOA-arena-locate-datapack.zip` into the world's `datapacks` folder (or pick it when creating the world), `/reload`, then:

- `/function aoa:start`: **Overworld, 87 searches. This is the one that matters before the first pregeneration.**
- `/function aoa:start_other`: Nether, End and the Eternal Starlight dimension, 28 searches (later). The Eternal Starlight dimension has no vanilla control, so a NOT FOUND there is weaker.

One search per second; each prints an `AOA|LOCATE|...` line and the last line is `AOA|DONE`. The world generates a lot of chunks and the game may freeze for seconds at a time: that is normal. It changes nothing in the world. Send the whole `latest.log`; `python tools/aoa_parse_locate.py latest.log` turns it into verdicts. **A NOT FOUND is not proof of absence** (spacing, biome rules and distance all matter); a failed vanilla control withdraws every verdict for that dimension.

## 2. For every NOT FOUND: is the structure registered at all?

A structure that is not registered fails exactly like one that is merely far away. Type `/locate structure <id>` yourself: **"Could not find"** means it is registered but not within range; **"Unknown structure"** (or an error naming the id) means it is not registered, which is a real blocker.

## 3. Encounter check per located arena

Click the coordinates in the `/locate` result to teleport (or use `/tp`), look at the arena, then run the command in the last column: **"Test passed"** means that boss entity is loaded within 300 blocks. Record the rest in `ENCOUNTER_RESULTS_TEMPLATE.csv`: whether the arena is complete, whether the boss was there on arrival, and otherwise what makes it appear (altar, item, proximity, nothing). Ancient Remnant needs its special interaction.

| # | Phase | Boss | Arena | Dimension | Locate command | Boss present? |
|---:|---|---|---|---|---|---|
| 1 | 1 | Dead King | irons_spellbooks:catacombs | overworld | `/execute in minecraft:overworld run locate structure irons_spellbooks:catacombs` | `/execute if entity @e[type=irons_spellbooks:dead_king,distance=..300]` |
| 5 | 1 | Kobolediator | cataclysm:kobolediator_shrine | overworld | `/execute in minecraft:overworld run locate structure cataclysm:kobolediator_shrine` | `/execute if entity @e[type=cataclysm:kobolediator,distance=..300]` |
| 6 | 1 | Eternal Starlight: The Gatekeeper | eternal_starlight:portal_ruins_common | overworld | `/execute in minecraft:overworld run locate structure eternal_starlight:portal_ruins_common` | `/execute if entity @e[type=eternal_starlight:the_gatekeeper,distance=..300]` |
| 6 | 1 | Eternal Starlight: The Gatekeeper | eternal_starlight:portal_ruins_cold | overworld | `/execute in minecraft:overworld run locate structure eternal_starlight:portal_ruins_cold` | `/execute if entity @e[type=eternal_starlight:the_gatekeeper,distance=..300]` |
| 6 | 1 | Eternal Starlight: The Gatekeeper | eternal_starlight:portal_ruins_desert | overworld | `/execute in minecraft:overworld run locate structure eternal_starlight:portal_ruins_desert` | `/execute if entity @e[type=eternal_starlight:the_gatekeeper,distance=..300]` |
| 6 | 1 | Eternal Starlight: The Gatekeeper | eternal_starlight:portal_ruins_forest | overworld | `/execute in minecraft:overworld run locate structure eternal_starlight:portal_ruins_forest` | `/execute if entity @e[type=eternal_starlight:the_gatekeeper,distance=..300]` |
| 6 | 1 | Eternal Starlight: The Gatekeeper | eternal_starlight:portal_ruins_jungle | overworld | `/execute in minecraft:overworld run locate structure eternal_starlight:portal_ruins_jungle` | `/execute if entity @e[type=eternal_starlight:the_gatekeeper,distance=..300]` |
| 7 | later | Eternal Starlight: Starlight Golem | eternal_starlight:golem_forge | eternal_starlight | `/execute in minecraft:eternal_starlight run locate structure eternal_starlight:golem_forge` | `/execute if entity @e[type=eternal_starlight:starlight_golem,distance=..300]` |
| 8 | later | Eternal Starlight: Permafrost | eternal_starlight:golem_forge | eternal_starlight | `/execute in minecraft:eternal_starlight run locate structure eternal_starlight:golem_forge` | `/execute if entity @e[type=eternal_starlight:permafrost,distance=..300]` |
| 9 | later | Eternal Starlight: Lunar Monstrosity | eternal_starlight:cursed_garden | eternal_starlight | `/execute in minecraft:eternal_starlight run locate structure eternal_starlight:cursed_garden` | `/execute if entity @e[type=eternal_starlight:lunar_monstrosity,distance=..300]` |
| 11 | 1 | Underground dragons (fire, ice, lightning) | iceandfire:fire_dragon_cave | overworld | `/execute in minecraft:overworld run locate structure iceandfire:fire_dragon_cave` | `/execute if entity @e[type=iceandfire:fire_dragon,distance=..300]` |
| 11 | 1 | Underground dragons (fire, ice, lightning) | iceandfire:ice_dragon_cave | overworld | `/execute in minecraft:overworld run locate structure iceandfire:ice_dragon_cave` | `/execute if entity @e[type=iceandfire:ice_dragon,distance=..300]` |
| 11 | 1 | Underground dragons (fire, ice, lightning) | iceandfire:lightning_dragon_cave | overworld | `/execute in minecraft:overworld run locate structure iceandfire:lightning_dragon_cave` | `/execute if entity @e[type=iceandfire:lightning_dragon,distance=..300]` |
| 12 | later | Netherite Monstrosity | cataclysm:soul_black_smith | the_nether | `/execute in minecraft:the_nether run locate structure cataclysm:soul_black_smith` | `/execute if entity @e[type=cataclysm:netherite_monstrosity,distance=..300]` |
| 13 | 1 | Ancient Remnant | cataclysm:cursed_pyramid | overworld | `/execute in minecraft:overworld run locate structure cataclysm:cursed_pyramid` | `/execute if entity @e[type=cataclysm:ancient_remnant,distance=..300]` |
| 14 | later | Ender Guardian | cataclysm:ruined_citadel | the_end | `/execute in minecraft:the_end run locate structure cataclysm:ruined_citadel` | `/execute if entity @e[type=cataclysm:ender_guardian,distance=..300]` |
| 16 | 1 | Ice and Fire Hydra | iceandfire:hydra_cave | overworld | `/execute in minecraft:overworld run locate structure iceandfire:hydra_cave` | `/execute if entity @e[type=iceandfire:hydra,distance=..300]` |
| 19 | 1 | Chesed | fdbosses:chesed_arena | overworld | `/execute in minecraft:overworld run locate structure fdbosses:chesed_arena` | `/execute if entity @e[type=fdbosses:chesed,distance=..300]` |
| 20 | 1 | Malkuth | fdbosses:malkuth_arena | overworld | `/execute in minecraft:overworld run locate structure fdbosses:malkuth_arena` | `/execute if entity @e[type=fdbosses:malkuth,distance=..300]` |
| 21 | later | Geburah | fdbosses:geburah_arena | the_end | `/execute in minecraft:the_end run locate structure fdbosses:geburah_arena` | `/execute if entity @e[type=fdbosses:geburah,distance=..300]` |
| 22 | later | Ignis | cataclysm:burning_arena | the_nether | `/execute in minecraft:the_nether run locate structure cataclysm:burning_arena` | `/execute if entity @e[type=cataclysm:ignis,distance=..300]` |
| 23 | 1 | Maledictus | cataclysm:frosted_prison | overworld | `/execute in minecraft:overworld run locate structure cataclysm:frosted_prison` | `/execute if entity @e[type=cataclysm:maledictus,distance=..300]` |
| 24 | 1 | The Leviathan | cataclysm:sunken_city | overworld | `/execute in minecraft:overworld run locate structure cataclysm:sunken_city` | `/execute if entity @e[type=cataclysm:the_leviathan,distance=..300]` |
| 25 | 1 | Bosses'Rise: Sandworm | block_factorys_bosses:sandworm_nest | overworld | `/execute in minecraft:overworld run locate structure block_factorys_bosses:sandworm_nest` | `/execute if entity @e[type=block_factorys_bosses:sandworm,distance=..300]` |
| 26 | 1 | Bosses'Rise: Yeti | block_factorys_bosses:yeti_hideout | overworld | `/execute in minecraft:overworld run locate structure block_factorys_bosses:yeti_hideout` | `/execute if entity @e[type=block_factorys_bosses:yeti,distance=..300]` |
| 27 | 1 | Bosses'Rise: Infernal Dragon | block_factorys_bosses:dragon_tower | overworld | `/execute in minecraft:overworld run locate structure block_factorys_bosses:dragon_tower` | `/execute if entity @e[type=block_factorys_bosses:infernal_dragon,distance=..300]` |
| 28 | later | Bosses'Rise: Underworld Knight | block_factorys_bosses:underworld_arena | the_nether | `/execute in minecraft:the_nether run locate structure block_factorys_bosses:underworld_arena` | `/execute if entity @e[type=block_factorys_bosses:underworld_knight,distance=..300]` |
| 29 | 1 | Bosses'Rise: Kraken | block_factorys_bosses:kraken_ship | overworld | `/execute in minecraft:overworld run locate structure block_factorys_bosses:kraken_ship` | `/execute if entity @e[type=block_factorys_bosses:kraken,distance=..300]` |
| 31 | 1 | Last of Deepslate | archaion:ancient_keep | overworld | `/execute in minecraft:overworld run locate structure archaion:ancient_keep` | `/execute if entity @e[type=archaion:last_of_deepslate,distance=..300]` |
| 33 | 1 | Scylla | cataclysm:acropolis | overworld | `/execute in minecraft:overworld run locate structure cataclysm:acropolis` | `/execute if entity @e[type=cataclysm:scylla,distance=..300]` |
| 34 | later | Obsidilith | bosses_of_mass_destruction:obsidilith_arena | the_end | `/execute in minecraft:the_end run locate structure bosses_of_mass_destruction:obsidilith_arena` | `/execute if entity @e[type=bosses_of_mass_destruction:obsidilith,distance=..300]` |

Bosses with no arena identified yet (Tyros, Cornelia, Ender Golem, Ignited Revenant, Coralssus) cannot be checked this way: they need the jar inspection first. Ossukage, Kotsukage and Umbrakar have no arena (ritual summons); `aoa:start` also searches `minecraft:ancient_city`, the source of Umbrakar's echo shard and sculk.

