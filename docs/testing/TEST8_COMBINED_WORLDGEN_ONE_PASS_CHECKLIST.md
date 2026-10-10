# Ambient Odyssey v0.3.8 — Combined prefreeze one-pass test checklist

**Status:** 10 October 2026 — **preview ZIP statically verified, NOT runtime tested**. **Minecraft 1.21.1 / NeoForge 21.1.252.** Working branch: `structure/test6`. **Worldgen is NOT frozen.**

**Preview ZIP:** `Ambient-Odyssey-v0.3.8-Combined-Prefreeze-Test1.zip` — **262 CurseForge projects**, **1,063 ZIP entries**, **67,974,728 bytes**, SHA-256 **`59714d91a5007befc1fe22361efadfabd2a4fdb20c933a0273f3e55420550cb0`**. Constructed from the **user-tested v0.3.7 Dev3 predecessor** via targeted manifest/worldgen/config patches; **not yet built by the authoritative `build_release_030.py` repo script or re-exported by CurseForge desktop**. ZIP CRC, duplicate, manifest, selected pins, and source-derived changes checked. **No full Minecraft startup or loader/dependency test has been performed for this particular candidate.**

## Important: two manual setup steps before testing

The preview's CurseForge manifest **does NOT include** these two approved additions, because safe exact-file distribution wasn't established. **Do not overlook them:**

- [ ] In the freshly imported profile, use **Add More Content** in CurseForge to add **Better Bastions: Nether Bastion Remnant Overhaul (NeoForge)**, choosing exact `betterbastions-1.0.0+neoforge-1.21.1.jar`. Official page: https://www.curseforge.com/minecraft/mc-mods/better-bastions . Its project ID is `1713723`; exact CurseForge file ID was not safely resolved here. **Do not add a different Minecraft version or the Forge variant.** The published mod claims Incendium-compatible bastion biome tags; runtime still untested
- [ ] Install **NeoReefRedux (Reef Redux NeoForge 1.21.1 Port)** from its official Modrinth page directly into the same test profile `mods/`: https://modrinth.com/mod/neoreefredux . It does not have a verified CurseForge project ID; there is **no loose third-party JAR** in the import ZIP. Record its exact installed version and checksum if possible
- [ ] If either of the above cannot be installed, write down which was absent. Mark any related test results **NOT TESTED**, not PASS. Do not silently treat this as the complete all-mod run

## A. Import and client health

- [ ] Import ZIP as a **new CurseForge instance**; never overwrite successful v0.3.7 or the only world save
- [ ] Confirm version `0.3.8-worldgen-prefreeze-test1`, Minecraft 1.21.1, NeoForge 21.1.252, RAM recommended 10,240 MiB (requires enough physical memory)
- [ ] Verify 262 CurseForge project/file references installed, **plus** the two separate manual mods above
- [ ] Confirm both shader packs **Solas V2.3** and **Complementary Reimagined r5.9.3** appear in Shader Packs, not in the Java mods folder. Keep shaders OFF for initial performance measurements
- [ ] Confirm **Iron's Jewelry v2.0.2** loads without downgrading Iron's Lib; Iron's Spells and other installed Iron dependencies work
- [ ] Confirm **Dimensional Doors remains absent**; Creative tabs/inventory, JEI and Better Inventory open without its previous `dimdoors:reality_sponge` exception
- [ ] Fresh-profile narrator does not announce accessibility onboarding; `narrator:0`, `narratorHotKey:false`, `onboardAccessibility:false`, Shader Packs menu works (background blur off)
- [ ] Check Borderless Window, Shadow Drop, Curios accessories and Sophisticated Backpacks UI; Better Inventory auto Tool Rack still activates if rack slots filled (leave slots empty if unwanted)
- [ ] Record cold launch minutes and first-menu/first-world loading, client warnings, `latest.log`, and any `crash-reports/*-client.txt`

## B. New Overworld biome and terrain distribution — use fresh seeds

- [ ] In **two different fresh worlds**, record seed and a reproducible route at F3; sample different regions rather than one local radius
- [ ] Prairie occupies **less relative land** than the previous pack while retaining its interesting farms/structures (canonical weights reduced)
- [ ] Naturally find new **BWG Baobab Savanna**, **BOP Dryland**, **BWG Tropical Rainforest** in their appropriate climate targets; verify they are neither impossible to find nor dominating
- [ ] Inspect flower fields / Grassland / Pumpkin Patch / Maple and Sakura forest diversity; verify structures in modded biomes vs vanilla
- [ ] **Stony Shore → BWG Dacite Shore** replacement: coast cliffs, beaches and river mouths should fit FreeTerraForged terrain without obvious seams or floating water
- [ ] Mountains, taiga, vegetation, giant trees, coasts, continent scale and **Streams Reflowing rivers** remain coherent; newly generated chunks only
- [ ] Inspect vanilla-vs-modded biome structure parity; farmhouses/structures should not disappear in new baobab/dryland/tropical biomes
- [ ] Document any strange biome ID (F3 screenshot, world seed, X/Z and screenshots before changing settings)

## C. Structure rarity, placement, collisions and bridges

- [ ] **WDA Lighthouse** and **IDAS Abandoned Lighthouse** are noticeably rarer than before, without reducing WDA fishing hut/temple or IDAS ordinary small structures; unique rare grids now separate them
- [ ] Check other lighthouse sources (Structory Towers, Towns & Towers beach lighthouse) for remaining excess density; unresolved `kaisyn:village/beach_lighthouse/villager_lighthouse_master` template-pool warning
- [ ] **Eternal Starlight portal ruins** rarer (five variant sets spacing 45/separation 32), yet still naturally reachable
- [ ] Block Factory **Dragon Tower** rarer (96/48), AND placement no longer causes frequent serious collisions. Rarity alone does not geometrically prevent overlaps
- [ ] **Bridges across vanilla rivers vs Streams Reflowing streams**: compare YUNG's Bridges and other bridge sources; log bridges found per ~1,000 new river blocks; inspect bridge orientation, height, supports and clipping. Existing `streamsreflowing:stream` tag is present, but **physical bridge placement is NOT yet fixed**. Report problem rather than assuming parity
- [ ] Confirm WDA Small Blimp and Coliseum absent as intended; WDA mushroom village on Mushroom Fields only; Farmers Structures still present, correct structures in deserts/oceans
- [ ] Look for giant intersections: Block Factory boss tower, WDA large landmarks, YUNG temples/bridges, IDAS, Create ruins and Luki structures

## D. Ocean expansion — record specific new mod behavior

- [ ] **Aquamirae 7.2.10**, plus required **Fragmentum** & existing GeckoLib, load; Ice Maze/Ship Graveyard in appropriate icy ocean, bosses/loot/gear and terrain fit
- [ ] **Hybrid Aquatic 1.7.4** marine biodiversity, reef/trench features, performance/spawn overlap with existing Aquaculture/Ben's Sharks/Alex's Mobs
- [ ] **YUNG's Better Ocean Monuments 4.1.2**: new monument design, normal monument eligibility, sane integration with Deeper Oceans, loot and no buried entrances
- [ ] **Better Shipwrecks 1.0.3**: new wrecks vs WDA Seven Seas/Antique Trading Ship; reasonable frequency, no major duplicate wrecks or overlapping coastlines
- [ ] **FTB Ocean Mobs 21.1.4**: entity registration, spawn rates and TPS; **no default mob loot**—flag progression loot TODO and do not claim rewards exist
- [ ] **Aquatic Creepers** spawn appropriately, no excessive explosion damage to seabeds/coral/underwater player bases
- [ ] **Small Ships** vessels are craftable, drivable and controllable in waves; multiplayer entity/collision behavior
- [ ] **Ocean's Delight** recipe/JEI support, Farmer's Delight integration and item textures
- [ ] **Deeper Oceans 2.0.1** actually increases depth; inspect ocean monuments, shipwrecks, Aquamirae structures and underwater villages at deeper y-levels; **high-priority FTF conflict check**
- [ ] **NeoReefRedux (manually installed)** changes coral terrain, caves/arches/rocky reefs, retains vanilla corals or honors configurable disable; collision/performance with Hybrid Aquatic
- [ ] Compare 3+ deep/frozen/warm ocean biomes, underwater structures, sea monsters, reef visual density and ocean exploration rewards without rendering/shader enhancements

## E. Nether, End, quests and multi-player

- [ ] **Better Bastions (manually installed)** alters bastion remnants in **NEW Nether chunks**; biome-themed styles, loot, mobs, no severe Incendium/YUNG fortress/Black Spiral overlaps
- [ ] Measure first portal crossing and **repeat visits** for Nether and End; report duration, TPS and GPU frame-times separately
- [ ] Nether **Explorify Black Spiral** remains working; Incendium special weapon textures still need **Sparkles resource pack**, separate from Solas/Complementary shaders
- [ ] End ships/Heavenly structures and End biome eligibility unchanged; report genuine rarity after multiple locates and natural exploration
- [ ] **Solo Quests 1.1.2, FTB Quests 2101.1.36:** verify 2 players in **the same FTB Teams party on a DEDICATED server**, Player A completes task while Player B does NOT. `defaultconfigs/ftb_solo_quests-server.toml` sets `teamSyncEnabled = false`; inspect actual generated `world/serverconfig/ftb_solo_quests-server.toml`
- [ ] Verify FTB Teams/Chunks *shared land claims still work*, rewards not accidentally duplicated or lost, and the questbook's basic tasks/JEI icons still work
- [ ] If using existing quest progress, **backup `world/ftbquests`**; inspect `/soloquests status` and migration commands before altering progress. In **singleplayer/LAN Solo Quests may not function**; do not infer failure for dedicated server from SP results

## F. Benchmark and release freeze decisions

- [ ] Record no-shader/no-Distant-Horizons standing-still FPS and **1% lows** (same seed/settings) vs Dev3
- [ ] Record new-chunk FreeTerraForged generation time, server `Can't keep up` warnings, freeze duration and RAM use; compare old measured ~9.06 new chunks/sec under previous Test6, not as fixed target
- [ ] Test 2–3 crossings per dimension; check dedicated server join, saves, backup/restore, new-vs-existing chunks, client model/log warnings
- [ ] Record a **single defect list** with severity BLOCKER/HIGH/MEDIUM/COSMETIC and reproducible seed/biome/coordinates, including missing assets (`astrological:crying_duct`, pool references, Incendium textures), Curios/Enigmatic amulet and bridge geometry
- [ ] Decide **keep/disable/reconfigure** for Deeper Oceans, NeoReefRedux, Aquamirae and any content that causes major overlap, performance regressions or overpopulation
- [ ] Only when reviewed can worldgen be **FROZEN**. Do not pick the permanent server seed or pregen until a final exact source/ZIP passes these gates
- [ ] **Later audit, NOT in this test:** Beyond the Ocean (large post-End dimension/content system); Tide 2, Sea Myths and Create Deep Seas **explicitly excluded**; Upgrade Aquatic omitted in favor of Hybrid Aquatic
- [ ] Prepare clean CurseForge app export for project moderation **only after** manual exceptions are incorporated through approved distribution and exact source build + runtime verification. Current ZIP is a developer test import, not publication-ready

## Feedback format

For each problem include **dimension, seed, coordinates, F3 biome ID, approximate travel distance, timestamp, one screenshot and latest.log**. When reporting a soft lock/fatal crash attach `crash-reports/crash-*.txt`. Compare actual measured spawn rates, not only `/locate` success; new worldgen never retroactively changes old generated chunks.
