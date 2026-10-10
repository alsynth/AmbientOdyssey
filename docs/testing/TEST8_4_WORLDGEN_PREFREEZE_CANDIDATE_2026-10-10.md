# Ambient Odyssey — Test8.4 targeted worldgen candidate

**Source branch:** `worldgen/test8.4-prefreeze` branched from successful Test8.3's successor `structure/test6` at `43c93f5030a08ffbee289874cfae1859c70566c9`. **Date:** 10 October 2026. **Minecraft:** 1.21.1 / NeoForge 21.1.252.

## Status and scope
**Implemented on this branch, JSON/source inspected, runtime NOT tested.** Preserve the user's successful **Test8.3** profile and world. This is an isolated source candidate, **NOT a built/importable public CurseForge release and NOT final worldgen acceptance**. A clean repo builder run and full static validators are still required before importing; `validate_worldgen_test84.py` covers only scoped data consistency. No world-height numbers or dragon-spawn guarantees may be inferred without a fresh-world run.

The user actually flew underground in Spectator mode and did not find dragon caves. Do **not** dismiss that report as mere surface flyover. There are known external IceAndFire-CE compatibility reports for modded biomes; our existing `ao_dragon_caves` eligibility replacement remains enabled and unchanged.

### Exact changes

| Subsystem | Test8.3 → Test8.4 | Why / guardrails |
|---|---|---|
| Prairie, plains pool | replacement weight **23 → 14** | Less overrepresentation; other three donors unchanged. Native vanilla retention unchanged. |
| Prairie, savanna pool | **30 → 18**; BWG Baobab Savanna 25→30; BOP Dryland 20→25; NS Floral Ridges 10→12 | Shift warm/open land towards other *already-approved* biome donors. No new biomes. |
| Prairie, windswept savanna pool | **22 → 14**; BWG Baobab 35→39; BOP Dryland 10→12; NS Floral Ridges 18→20 | Keep visual variety. |
| Forced Prairie climate fallbacks | Warm Skyris Vale now → RU Grassland; hot Floral Ridges now → BWG Baobab Savanna | Original conditions kept; donors remain in approved roster. Cold RU Grassland fallback still uses Prairie when native RU climate isn't viable. |
| FreeTerraForged height | mountain-only `verticalScale: 0.88917524 → 1.35`; `mountainVariety: 0 → 0.9` | FTF #95 documents deterministic low/center/high mountain variants, with max-variety high variant at +20% vertical scale. Larger peaks should become possible without globally raising hills, plains, rivers or oceans. **Peak Y still unmeasured.** |
| Ice & Fire CE cave chances | Fire, lightning and ice **0.50 → 0.72** | A modest increase in per-type generator chance, NOT surface roost chance, cave density guarantee, or correction for failed biome/height constraints. 1,000-block dangerous-distance rule unchanged. |
| Archaion Ancient Keep | New Paxi overrides of `archaion:ancient_keep/rooms` and `rooms_x` | Author's **1.21.1 source** contains exactly two **zero-byte NBTs**, `misc_room.nbt` and `misc_room_x.nbt`, matching observed EOF errors in Test8.3. Their references removed from authored source-backed pool JSON. Other **10+7** room choices preserved, original structure remains active. Verify actual packaged binary matching upstream before claiming confirmed fix. |

**Unchanged:** FTF overall `globalVerticalScale=0.6`, preset sea level 63 and world height 512, continent scale 6500, river count 15, Streams Reflowing, general structure density, WDA lighthouses, Farmers 20 sets, End grids, original dragon surface roosts, Ice+Fire cave eligibility selectors, all mod pins, render stack, gameplay balance/performance work.

### Evidence and source
- Test8.3 log `latest(20261010-023809).log` successful startup, new-world save, **1,229** missing jigsaw references, two Ancient Keep EOF errors, Repurposed city missing `fat_tower_top`, Dungeon Crawl spawner warnings. Raw log stays private because it contains user identifiers.
- FTF mountainVariety mechanism: [upstream PR #95](https://github.com/ETcodehome/FreeTerraForged/pull/95), max-variety three regional profiles, each about a third of mountain regions, high variant max +20% `verticalScale`. It is **not** a global world-height multiplier.
- Archaion author: [`1.21.1` source `misc_room.nbt`](https://github.com/UnanimousVoid/Archaion/blob/1.21.1/src/main/resources/data/archaion/structure/ancient_keep/misc_room.nbt) and `misc_room_x.nbt` are both **0 bytes** (source tree). [Native pool `rooms.json`](https://github.com/UnanimousVoid/Archaion/blob/1.21.1/src/main/resources/data/archaion/worldgen/template_pool/ancient_keep/rooms.json) and [`rooms_x.json`](https://github.com/UnanimousVoid/Archaion/blob/1.21.1/src/main/resources/data/archaion/worldgen/template_pool/ancient_keep/rooms_x.json) were reproduced exactly except removal of one broken entry each.
- IceAndFire-CE generator's own `iaf-common.json` permits probabilities between 0 and 1, and upstream has [modded-biome compatibility concerns](https://github.com/IAFEnvoy/IceAndFire-CE/issues/237).

## Build and static gates (required)

From a full `worldgen/test8.4-prefreeze` checkout:

```sh
python --version
python validate_worldgen_test84.py
python build_release_030.py
python validate_worldgen_test84.py
python validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test84-continuation.json
python validate_structure_test6.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test84-structure.json
```

The builder retains the **historical Test5 output filename** despite newer data. The import created by this code may **exclude Test8.3 private-only assets** (NeoReefRedux and Better Bastions JARs), which are deliberately not checked into Git. Compare actual manifest, shader file refs, user-provided binary hashes, and entire ZIP to Test8.3 before claiming this is an executable replacement. Check exact root `manifest.json`, archive CRC, duplicate member IDs and mod list. Do not distribute embedded CF-hosted third-party binaries as public assets.

## Fresh-world QA in this order
1. Duplicate the known-good instance, **do not overwrite saves**. Create at least two fresh worlds with same FTF custom AO preset, record seeds and screenshots. Check `/datapack list` for `ao_biome_replacement`, `ao_dragon_caves`, `ao_worldgen_final_fixes`; look for JSON parsing, missing tag and reload errors first.
2. At several plains/savanna/windswept regions, record BWG Prairie proportion versus RU Grassland/Flower Fields, Baobab, Dryland and Floral Ridges, including warm/cool climates. Nominal pool weights are not global area percentages.
3. Fly across **at least six** independent FTF mountain regions; log highest Y, average relief and whether some ranges are sharper/higher than others; inspect rivers/FTF seams/structures near the mountain base. The new `mountainVariety` leaves about a third of mountain ranges centered on the explicit profile, so not every mountain will be taller. Check if rare high peaks are in the desired Y200–260 *exploratory target* — do not claim that height has been achieved until observed.
4. For **all three dragon caves**, use `/locate structure iceandfire:fire_dragon_cave` / `lightning_dragon_cave` / `ice_dragon_cave` then enter Spectator underground, **beyond the 1,000-block dangerous-distance protection**. Check actual cave material, adult dragon, chest/loot, air/water pockets and biome/height, recording successful and failed attempts (locate alone can be false positive). Check fire/lightning in contrasting forest/savanna/modded biomes and ice in cold only. Do not boost roosts.
5. Locate and actually assemble an **Archaion Ancient Keep** in freshly generated chunks. Check that no `EOFException` for `misc_room` or `misc_room_x` appears and that other room variants are intact. If errors remain, check Paxi pack priority and exact installed mod file before assuming upstream assets.
6. Test YUNG Bridges: compare small/medium/large across natural rivers versus Streams Reflowing. Upstream notes FTF/TerraForged's narrow rivers/steep banks can prevent valid medium/large placements. **No blanket density multiplier yet**. Record river width/height and actual biome.
7. **Still-open high-priority assembly defects**: identify 1,205 empty `minecraft:` jigsaw targets; 18 missing `create_easy_structures:undergroundtrain_station`; 6 cook-pool references; Repurposed city missing required `fat_tower_top`; Dungeon Crawl spawner lookups. Inspect provider 1.21.1 JAR assets before writing any alias or fallback; warnings are not all necessarily fatal.
8. Other unfinished worldgen gates: deep/frozen/warm oceans with Deeper Oceans/NeoReefRedux/Aquamirae/Hybrid Aquatic; coast monuments/shipwrecks/underwater villages; Nether Black Spiral/Better Bastions; End heavenly ships/cities; portal transitions; multiplayer and dedicated-server map/worldgen. **Performance tuning stays out of this source wave**, though new crashing/hanging/stalling remains an acceptance blocker.

## Decision gate

Preserve this as an experimental branch until the Minecraft run proves mountain silhouette, biome mix, actual cave generation and intact Archaion Ancient Keeps. For bad terrain or rare-cave outcomes, review data with seeds/coordinates before another global bump. Performance optimization follows after worldgen acceptance, per user instruction.
