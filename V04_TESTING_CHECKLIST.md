# v0.4 experimental — one grouped acceptance run

Use a new CurseForge profile and disposable worlds. Keep the working Test8.2/0.4b instance and saves. Import the actual ZIP containing root `manifest.json`, not a GitHub artifact wrapper. Use Java 21 and start around 10 GiB client RAM if the machine has adequate free memory.

## Startup and data

- [ ] Confirm Mine Cells, Connector, Forgified Fabric API and existing NeoForge owo-lib are present; no original Fabric API, duplicate owo, transformed `.connector` exports or Dimensional Doors.
- [ ] Reach main menu and create a fresh world; collect complete logs. No fatal mixin/registry/module errors or invalid recipes/tags/loot tables. Check Traveloptics fire tag and Fungi mushroom cooking.
- [ ] Check JEI Flight Rings crafting and both smelting salvage recipes, Curios/Enigmatic amulet slots, mod crafting/cooking, loot and creative inventory. Sample dungeon chests and look for legacy missing-item losses.
- [ ] Verify 5 resource packs and 2 shader references install to the appropriate folders. Test NeOculus/Embeddium with shaders off, then each shader independently. Test camera UI, Exposure persistence, tooltip/HUD overlap and screenshot browser.

## World generation and dimensions

- [ ] Record seed, preset and coordinates. Compare natural structures in vanilla and modded biomes; Farmers Structures, WDA major rarity, mushroom-only village, lighthouses, dragon caves/tower and huge trees.
- [ ] Inspect 273-repair structure families, Archaion keep, cook/angler rooms, Graveyard crypt, Towns & Towers lighthouse/Swiss village, independent Create windmills. `/locate` alone does not verify natural frequency or assembly.
- [ ] Inspect bridge/Streams geometry, coast and oceans, Nether Black Spiral/Bastions and End distribution. Confirm all existing dimensions still enter/save/reload.
- [ ] Mine Cells: naturally discover entry, follow portal progression through prison, promenade, ramparts, black bridge and insufferable crypt. Test respawn/death return, boss phases, progression locks, loot/crafting and exit. The automated test forced dimension chunks; it did not perform this gameplay.
- [ ] Restart and re-enter dimensions; do not reset a permanent Mine Cells realm or adopt this world as the final server map yet.

## Multiplayer and rules

- [ ] Run a dedicated server with client-only mods excluded using their actual sidedness; no blind client-folder copy. Test two players joining, shared portals, dimension transitions, entity synchronization and restart/rejoin.
- [ ] Check 30% sleeping after load and `/reload`; confirm fire/grief rules. Check villager farming consequences and boss explosion exceptions.
- [ ] Confirm FTB Solo Quests keeps independent completion/rewards while sharing teams/chunks. It does not support integrated/LAN worlds equivalently.
- [ ] Bonus Chest ON: two non-op players independently loot the same physical chest, then late join/restart. Lootr conversion remains unverified; no generous custom starter table is promised.
- [ ] Check key conflicts with Controlling after every selected mod registers. Full keybind redesign and quest implementation remain later work.

## Ambience and performance

- [ ] Compare rain, stream and coast audio against forest birds/insects, including above and below canopy. Existing players may need Weather 20%, Blocks 40% manually; the Waves fix is not a water-event-specific patch.
- [ ] Measure 60-second stationary, village, new-chunk travel, cold dimension entry and cached return routes. Record hardware, Java, RAM, shader, render/simulation distance, FPS lows, MSPT, memory and generation throughput.
- [ ] Repeat with 5–7 players travelling separately and with shaders off/on. Separate client FPS from server stalls. Compare 12/6 defaults to the user's earlier 12/12 profile; no preflight performance guarantee.
- [ ] Review POI duplication, Streams fast-terrain fallback, GC pressure, duplicate cave/particle effects and first-use dimension delays. Keep worst-case logs and reproduction coordinates.

Acceptance remains experimental until these client/gameplay/multiplayer checks pass. Report each as PASS / FAIL / NOT TESTED with its actual evidence.
