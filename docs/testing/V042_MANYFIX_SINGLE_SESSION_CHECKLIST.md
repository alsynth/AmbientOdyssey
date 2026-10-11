# Ambient Odyssey 0.4.2 — one consolidated test session

**Experimental, not runtime-tested.** The full ZIP has 330 exact CurseForge references:
the 329-ref Mine Cells/Streams/TREK/Questlog version plus Dungeon Difficulty
3.9.2 (645559:9110961). Also includes Curios amulet-slot compatibility,
the v0.1.1 Hominid lifecycle addon, 32 FTB manual acknowledgment tasks, two
IDAS native fixes, prior Luki/Tan's/Streams integration, and existing six-fix recipe containment.
**The previously accepted TREK/Create spacing is unchanged.**

Test as ONE session where possible (approximately 60–120 minutes, with a later
dedicated 2–7-player session); use a fresh disposable world and keep backups.
Old quest progress survives in old saves.

## A. Initial startup, quests and inventory

- [ ] Import the INNER ZIP named Ambient-Odyssey-v0.4.2-MANYFIX-TEST.zip, not the outer GitHub Actions wrapper. NeoForge 21.1.252, MC 1.21.1, 330 mod references.
- [ ] Reach main menu and create a world; collect complete latest.log.
- [ ] FTB Field Manual, Tips and Keybind chapters do NOT self-complete on login. Click a checkmark in one page manually; the other 31 pages remain incomplete.
- [ ] WDA original main quest rewards and tasks remain intact. Questlog Q1's 50 quest entries and 13 chapters still load.
- [ ] Open Better Inventory and Questlog using both shortcut and the Q tab; photograph the entire inventory at GUI scale 2 and 3. Confirm Q does not overlay the fifth backpack, crafting or settings tab. The visual layout was previously reported wrong and is NOT yet confirmed in Minecraft.
- [ ] Curios has at least one working amulet slot. Equip/unequip a genuine Enigmatic Legacy+ amulet; verify it persists through inventory close/save/rejoin. Other Relics/Artifacts slots should be unaffected. No duplicate slot count.
- [ ] Verify normal JEI recipes and crafting. **Known limitation: 19 invalid old recipes remain intentionally disabled, not functionally restored.** Note any blocked progression.

## B. Overworld, structures, mobs and difficulty

- [ ] Inspect ordinary vanilla zombies and Hominid Juggernaut/Bellman rare replacements. This build changes the spawn lifecycle for main-thread zombies. Check the log for 'marked as removed already' and off-thread add errors. Structure-worker zombies should remain ordinary zombies.
- [ ] Explore Tan's Huge Trees and Luki Woodland Mansions; check native jigsaw fragments, tree mobs and trial keys; save and restart.
- [ ] Trek common/medium/rare discoveries look consistent with your previous approved density; nonfarming Create structures are less common; Create barns, windmills, honey/chocolate pits unchanged.
- [ ] Check Farmers Structures in one modded Overworld biome and major WDA/IDAS structures for broken chests or terrain clipping.
- [ ] Six new Dungeon Difficulty regions: Dungeon Crawl dungeons, Adventure Dungeons trialrooms, WDA illager fort, Keep Kayra, Plague Asylum, Iron's Spellbooks catacombs. Compare newly spawned vanilla hostile mob HP/attack/armor inside/outside their structure using in-game attribute data.
- [ ] Bosses from Cataclysm, Mowzie, Mine Cells, Iron's scripted bosses should NOT receive a global buff. Dungeon Difficulty's default loot scaling, player-count scaling and spawner-count scaling are disabled in this pilot.
- [ ] Dungeon Crawl spawner block entities remain an unresolved native worldgen issue. Verify their mobs actually spawn after save/restart.

## C. Dimensions, world map, resources and performance

- [ ] Enter Mine Cells Prison and Promenade, use portals, die/return, re-enter after restart; no broken stairs/cells. Inspect normal Overworld Streams rivers before and after re-entry.
- [ ] If Xaero World Map loses a previously visited tile, distinguish world terrain actually missing from a cave/height layer or cache display change; photograph before/after and back up data.
- [ ] Watch for invalid-air items, unknown Forge attributes, POI mismatches, missing models, broken trader offers and cold-generation stalls. These are not globally fixed.
- [ ] Check 30% sleep, no fire tick, and inherited mob-griefing rule; beware these may affect boss mechanics.
- [ ] Collect comparable Spark profiles on warm stationary, cold new-chunk travel and warm revisit with same Java/RAM/shaders/distance. No measured performance gain is claimed.
- [ ] A second Spark-background-OFF ZIP in the same artifact is ONLY for profiler-overhead A/B, not a separate feature build.
- [ ] If possible test two-player dedicated-server join, FTB individual quest progress, Curios slots, Hominid mobs, Mine Cells portal synchronization, save/restart, then 5–7 players.

## Still not solved by this ZIP

- 19 broken recipes remain disabled rather than made craftable; no invented recipe changes.
- Historical 504–540 'minecraft:air' item warnings span multiple mods; source attribution is incomplete; no destructive global replacements.
- Dungeon Crawl spawner lifecycle needs an actual correct persistence-safe implementation.
- Better Inventory Questlog Q visual position still needs full-screen UI evidence.
- Goblin-Tuned chainmail payment increases are researched but NOT applied; preserve native attribute-component gear rewards before any trade replacement.
- Random cosmetic trims on genuine Apotheosis affix-rarity armor were researched, but no addon is compiled/shipped for this.
- Full nine-tier boss balance, Q2 quests, keybind overhaul, under-canopy audio, resourcepack ordering and dedicated multiplayer release acceptance remain unfinished.

The candidate is for **private testing**. Some existing repaired NBT resources
come from native mod JARs and require redistribution-rights review before
any public CurseForge upload.
