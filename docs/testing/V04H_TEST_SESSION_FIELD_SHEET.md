# Ambient Odyssey 0.4h — first gameplay test session

Source build: 331 project references, Java 21, Minecraft 1.21.1, NeoForge 21.1.252. All checks begin NOT TESTED; metadata-only checks do not grant a runtime PASS.

## Phase A: install and main menu
1. Import the INNER private CurseForge ZIP into a NEW disposable instance. Never import the outer GitHub Actions artifact wrapper.
2. Confirm all pinned projects downloaded; resource packs and shaders may not appear as JARs. Disable shaders initially and use the supplied 12 render / 6 simulation distance.
3. Run the read-only Windows diagnostics and create a test-session snapshot. Reach menu; if startup fails, send separately reviewed latest.log and crash report and stop before changing multiple mods.
4. Start a disposable Free TerraForged world; record seed and wait for first spawn, save, close, reopen. Do not use this as the eventual multiplayer world.

## Phase B: inventory and Questlog
1. Open E inventory at GUI scale 3 with JEI visible. Check the Questlog icon at the trial upper-left location: visible, clickable, not obscuring other widgets.
2. Try Questlog backtick key (keyboard-dependent) and FTB Quests independently; the journal should be empty with no authored quests.
3. Check JEI recipe/use R and U; Accessories/Curios and backpacks; Polymorph recipe choices; crafting tweaks.
4. Take one screenshot of full E inventory and another at GUI scale 2/windowed mode. Check status-effect GUI. Do not change the icon coordinates before capturing evidence.

## Phase C: worldgen and progression
1. Visit vanilla and modded biomes, compare Farmers Structures, WDA and Ancient Remnants; record seed, XYZ, biome ID and clipped/overlapping structures. Locate-command success is not proof of frequency.
2. Test Mine Cells, Dimensional Dungeons and their return portals; do not treat the earlier isolated four-mod Mine Cells force-load test as player testing.
3. Check End Remastered extra eyes, Integrated Stronghold, JEI recipes, Curios tarot cards and modded loot.
4. Compare water and rain vs birds/insects both under canopy and above forest. Note Sound Physics interaction with Atmosfera and Streams.

## Phase D: multiplayer and performance (after successful solo launch)
1. Construct an independently verified, server-safe mod list. Do NOT copy the entire client mod folder to a server; use JAR metadata audit and actual mod documentation.
2. Start a disposable dedicated server; join with 2 players, restart and rejoin, and enter each new dimension.
3. Check 30% sleep with an appropriate player count, FTB Solo Quests, and chest instancing. Test 5–7 player load only after two-player success.
4. Measure actual FPS separately from dedicated MSPT/TPS, chunk generation stalls, shader frametime and memory use; no optimistic FPS/TPS promises from static checks.

## Issue record
| ID | PASS/FAIL/NOT TESTED | Actual vs expected | Seed/dimension/XYZ | Screenshot/log | Reproducible |
|---|---|---|---|---|---|
| A1 startup | NOT TESTED | | | | |
| A2 save/reopen | NOT TESTED | | | | |
| B1 Questlog button | NOT TESTED | | | | |
| B2 FTB Quests coexistence | NOT TESTED | | | | |
| C1 Mine Cells | NOT TESTED | | | | |
| C2 Dimensional Dungeons | NOT TESTED | | | | |
| D1 dedicated server join | NOT TESTED | | | | |

Original verified artifact: https://github.com/alsynth/AmbientOdyssey/actions/runs/38077302870/artifacts/11679672185
The first-test snapshot contains no raw logs or screenshots. Inspect each report before sharing; actual logs/screenshots are optional separate attachments.
