# Ambient Odyssey 0.4.1 — six-fix combined experimental test

**Minecraft 1.21.1 / NeoForge 21.1.252; 331 pinned CurseForge projects; branch experimental/v0.4.1-six-fix-test-20261010. This is an UNTESTED runtime candidate, not a stable release.**

## Applied

1. Added Cardinal Components API 6.1.2 (CurseForge 318449:5845879; Fabric via Connector) to address the Mine Cells doorway `AutoSyncedComponent` crash.
2. Added Paxi `ao_v041_runtime_fixes` with NeoForge false conditions at the **19 exact recipe IDs** that failed to parse in the Oct 10 v0.4.0 runtime log (13 Mine Cells Create + Farmer's Delight, three Brewin' And Chewin', one Dimensional Dungeons; count Mine Cells=15). This **disables** already-broken recipes; it does not restore crafting recipes. Future proper rewrites need exact JAR formats.
3. Removed RAR-Compat / Reliquified Artifacts 0.9.7 (CurseForge 1100379) that cleared Artifacts' equipment slot tags. Removes its Relics-style progression for Artifacts; base Relics and Artifacts remain. Validate against a clean profile/save.
4. Reworked the `traveloptics:element_fire` Paxi tag to replace with known vanilla entries + optional modded entries; removed the nonexistent `cataclysm:old_netherite_monstrosity`. The original Traveloptics 4.4.0.1 tag is malformed: the original parse warning may persist despite a valid final override.
5. Enabled ServerCore `prevent-moving-into-unloaded-chunks` to mitigate synchronous cold-exploration spikes. No FreeTerraForged noise/terrain changes or unsupported throughput claims. Unattributed `minecraft:air` item logs and POI mismatch remain under investigation.
6. Disabled Amendments double-cake feature to mitigate generated Enigmatic Legacy+ cosmic cake missing textures. No global animation/resource changes.

## Runtime acceptance (all NOT TESTED)

- [ ] Import clean CurseForge profile: 331 projects, CCA present, RAR-Compat absent, Questlog Q1 50/13 and FTB manual 32/3 intact.
- [ ] Start with Java 21, confirm no fatal new mixins and 19 invalid recipe IDs no longer log. JEI still works. Inspect needed compatibility recipes for future actual repair.
- [ ] Place Mine Cells doorway, enter/return, kill mobs, exit, save/restart; dedicated server two clients and packet sync.
- [ ] Equip Artifacts belt/hands, Relics separately and Enigmatic amulets; no lost progression in old saves.
- [ ] Verify Traveloptics fire-element final tag; note upstream malformed JSON still potentially logged.
- [ ] Compare 0.4.0 vs 0.4.1 same seed, hardware/shaders/route: FTF chunks/s, new-chunk lag, FPS, MSPT, worldgen geometry. Note any brief movement blocking.
- [ ] Inspect `minecraft:air` item stacks, POI mismatch, Bumblezone trades, Ice & Fire attachments; cannot fix without source owner IDs.
- [ ] Check Amendments cosmic/double-cake logs, real cakes, model resources.
- [ ] Recheck 30% sleep, Q1 Questlog, FTB manuals, loot/structures, biomes, 5–7 player server after 2-player trial.

**Limitations:** No in-game test evidence; disabled recipes are a containment measure, not functional recipes. Malformed upstream mod tag, unidentified structure-item errors, damaged POIs, generic GeckoLib warnings, Ice & Fire persistence, and actual native terrain-generation throughput are not fully fixed. Static CI validates only source and ZIP integrity.
