# Ambient Odyssey — Balance Lab 0.1
**Isolated experimental patch**, not release default. Reversible post-processing of the user-validated **329-project** combined v0.4.1 control ZIP.

## What is added
- CurseForge **Dungeon Difficulty 3.9.2+1.21.1 NeoForge**, project **645559**, file **9110961**, no transitive DLC added.
- Native server config `overrides/config/dungeon_difficulty_v2.json`, authored from [current Config.java](https://github.com/ZsoltMolnarrr/DungeonDifficulty/blob/1.21.1/common/src/main/java/net/dungeon_difficulty/config/Config.java) and the [v3.9 defaults](https://github.com/ZsoltMolnarrr/DungeonDifficulty/blob/1.21.1/common/src/main/java/net/dungeon_difficulty/config/Default.java).
- Only six **explicit** real AO structure registry IDs receive initial difficulty. No global Overworld/Nether/End/dimension blanket modifier. No Mine Cells damage or boss modification.
- Whitelist only common **vanilla hostile mob types**, not scripted bosses or arbitrary custom entity classes; first isolated phase before modded mobs are introduced.
- HP, attack and armor slightly stronger by local difficulty level, **no additional spawner count, no item scaling**, no player mining debuff. Local difficulty levels **are not AO's official nine combat tiers**.
- Automatic generated loot *completely disabled* (`loot_scaling.armor=[]`, `weapons=[]`, smithing upgrade scaling off, type allow_loot_scaling=false). Native loot tables and Goblin Tuned item components untouched.
- Automatic multiplayer difficulty off until specific Boss Ultimatum / Multiplayer Bosses option is selected, to avoid double scaling with other systems.

## Areas selected in the first experiment
| Structure | Local type/level | Notes |
|---|---|---|
| `dungeoncrawl:dungeon` | ao_dungeon 2 | Equipped mob spawner dungeons; verify spawn stats and existing gear |
| `adventuredungeons:trialrooms` | ao_trial 2 | Verify whether trial-spawner populations are correctly affected |
| `dungeons_arise:illager_fort` | ao_patrol 2 | Light engagement buff, no spawner boost |
| `dungeons_arise:keep_kayra` | ao_dungeon 3 | Large combat structure |
| `dungeons_arise:plague_asylum` | ao_dungeon 3 | Lower than scripted boss tiers |
| `irons_spellbooks:catacombs` | ao_dungeon 2 | Ordinary vanilla hostiles only; scripted Dead King/Tyros untouched |

**Note on vanilla entity matching:** the static config uses a deliberate exact anchored regex whitelist and DOES NOT buff arbitrary modded enemies, Cataclysm bosses, Iron's boss entities, or Mine Cells mobs. This is a conservative proof-of-mechanism patch, not full encounter balance.

## Validation gates
1. Verify original 329-project combined ZIP remains byte-identical and its 2 authored AO mod JARs are preserved.
2. Diff final export: exactly +1 project reference (645559:9110961), exactly +1 config, updated `manifest.json`; **all other files identical**.
3. CurseForge import and log confirm Dungeon Difficulty mod ID and JSON parse/no sanitize fallback.
4. Spawn vanilla zombies/skeletons in mapped structure and same-type creatures just outside; compare `/attribute` stats, especially levels 2 vs 3. New-spawn entities only.
5. Verify Cataclysm/Mowzie/BOMD and Mine Cells bosses unchanged in the same world and Overworld Streams rivers still form.
6. Check that dungeon chest and goblin gear items do NOT acquire a Dungeon Difficulty loot power level.
7. Verify party-size scaling does not engage when a second player joins; no player-effects/mining debuff.
8. A/B performance with 2-3 players at structure borders to check location-query pressure and chunk stalls.
9. Fix any incompatibilities **before** merging into the next working 0.4.x release. Never claim the successful code build is an actual Minecraft runtime test.

## Goblin Traders
See [Goblin-Tuned trade-economy investigation](../../docs/balance/V041_GOBLIN_TUNED_TRADE_ECONOMY.md). Pricing is intentionally NOT changed yet pending holistic loot balance.
