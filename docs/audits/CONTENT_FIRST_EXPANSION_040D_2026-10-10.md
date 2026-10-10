# Ambient Odyssey — Content-first development decision and 0.4d candidate
**Decision date:** 10 October 2026 · **Target public multiplayer opening:** approximately 15 October 2026 · **Status:** staged on experimental branch, NOT Minecraft-runtime approved.

## Binding priority order
1. **Expand first:** substantial waves of exploration, encounters, RPG mechanics, buildings, aesthetic detail and selected compatibility. Do not ask for a new user Minecraft session per one or two mods; only stop expansion for concrete fatal or destructive issues.
2. **Fix content-level defects and UX issues after roster selection:** audio mix (Streams/Waves/weather; ambient sounds under foliage), wildlife duplicates and biome spawn weights, Curios/Enigmatic slots, Conflicting keybinds (**Controlling works; overhaul after content expansion**), POI/loot and superficial model overlap. Track observations now without incidental rewrites.
3. **Worldgen/performance/optimization:** Streams Reflowing slow FreeTerraForged height fallback, cold chunkgen stalls, actual TPS/server AI counts, structure clipping, bridge terrain-fit, pregen after final worldgen and seed lock.
4. **Balance:** bosses, rarity, difficulty, magic, equipment, progression, spawn frequency, economy and rewards.
5. **Quests LAST:** archaeology's valuable specialist quests, FTB Quests, FTB Solo integration, fully authored Questlog and tutorials only after systems/worldgen are stable and balance direction established.
6. **After quests:** consider MCA Reborn, further bridges and other explicitly deferred features. MineColonies remains rejected; Galosphere remains removed; Big Globe and experimental Connector dimensions remain parked.

**Five-day window is a target, not proof that an untested candidate is launch-ready.** Source CI or CurseForge import never substitutes for real Minecraft launch/dedicated-server testing. No server pregeneration until final worldgen roster and seed. Preserve existing 0.4c and Test8.10 rollbacks.

## 0.4d substantive content additions (7 exact CurseForge file references)
| Category | Native NeoForge 1.21.1 project | CF project:file | Value |
|---|---|---:|---|
| Monster encounters | Mutant Monsters v21.1.1 | 852665:7232511 | Memorable elite-like hostile mobs; later tune spawn and combat tier |
| Raids | Illager Invasion v21.1.6 | 891324:6492670 | Distinct illager enemies/raid encounters; later examine overlapping raid mods and guards |
| Decorative blocks | Chipped v4.0.2 | 456956:5813117 | Broad block variations for player building |
| Furniture | Handcrafted v4.0.3 | 538214:6330030 | Usable building/furniture set |
| Ports/markets | Dusty Decorations v1.13 | 843344:7917189 | Nautical/settlement decoration; exact stable NeoForge build (new 2.2 port to be assessed separately) |
| Lighting | Night Lights v1.4.0 | 1199355:8555615 | Smart switches, dyeable lighting, structures built by players |
| Combat integration | Apothic Combat v1.2.1 | 986982:6105085 | Better Combat reach + Apotheosis attribute tooltips; no balance assumptions |

Count proposed: **288 → 295 CurseForge manifest refs**, only if baseline lacks duplicate projects and required libraries are present. The original Test8.10 fixed 273 NBT repairs, FreeTerraForged, Biolith, stream generation, original c0 Paxi rules and audio adjustments must remain unchanged.

## Dependencies requiring verified closure before importer distribution
- Chipped: **Resourceful Lib** (CF project 570073), **Athena** (841890); Handcrafted also uses Resourceful Lib.
- Mutant Monsters and Illager Invasion: **Puzzles Lib** (495476), with its Forge Config API Port relation to check for the NeoForge runtime.
- Dusty Decorations: **GeckoLib** (388172), already used by Naturalist but check actual manifest identity.
- Do **not** update existing library versions without source-native compatibility evidence. If one of the named required libraries is absent, CI will stop pending an exact dependency pin. Exact file versions from official CurseForge pages, not an automatically assumed bundled library.

## Logged issues: do not block new content for these alone
- 0.4b playtest reported 6116 chunks generated, 18 cold generation server lag warnings (worst 18.6s), nine generic POI mismatch errors, no crash and no structure missing-pool warnings.
- Atmosfera forest bird/insect audio appears louder over tree canopy than under leaves; source attribution pending.
- Waves/rain/block audio may still require tuning after c0 defaults; existing user options may override new defaults.
- Ocean wildlife duplication across Hybrid Aquatic, Naturalist, Ben's Sharks and Alex's Mobs; exact spawn-rule sources and creature uniqueness should determine future curation.
- New monster population and Guard Villagers raid reaction, night light render/tick cost, huge Chipped item catalog/JEI rendering and port furnishings must be checked in later content acceptance.
- New 0.4c gamerule `mobGriefing=false` affects villager crop farming: note trade-off and decide during later compatibility pass.

## Explicitly not being done in this source wave
No quest SNBT, reward scripts, keybind remap, worldgen rebalance, sound overhaul, boss stats, pregeneration, renderer replacement, MCA Reborn, more bridges or server deployment. Do not merge until required dependencies and CI, followed by a meaningful larger Minecraft acceptance test, are complete.
