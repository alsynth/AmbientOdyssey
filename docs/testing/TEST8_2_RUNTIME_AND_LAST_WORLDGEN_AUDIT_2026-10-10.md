# Ambient Odyssey — Test 8.2 actual runtime acceptance & last worldgen audit
**Updated:** 10 October 2026. **Log:** user-uploaded `latest(20261010-014111).log` (7,714 lines). Preserve users' credentials/IDs/Windows paths by **not committing raw log**. Active branch `structure/test6`; `main` remains old Test5 rollback.

## What passed (actual runtime, not just ZIP checks)

- **Previous startup crash cleared.** No `java.lang.module.ResolutionException` with `mpf` / `com.twelvemonkeys.image`. My Picture Frame is not present in mod list; Iron's Jewelry **2.0.2** and Iron's Lib **2.2.0** both load.
- **Client reached live integrated game** and created `New World`. Integrated server startup logged ~03:32:57, player joined ~03:34:42, session ended with normal save of Overworld and all registered dimensions and clean shutdown at ~03:40:58. **No fatal exception or Minecraft crash in this log**.
- Hybrid API 1.1.3, Atlas API 1.2.0, Hybrid Aquatic 1.7.4, Aquamirae 7.2.10, Fragmentum, Deeper Oceans, NeoReefRedux, Better Bastions, Flight Rings 2.0.0, MidnightLib and FTB Solo Quests are **loaded/registered**. This does NOT establish that their worldgen placement, gameplay and multiplayer functions work.
- User Paxi data packs `ao_dragon_caves`, `ao_flight_balance`, `ao_structure_density`, `ao_biome_replacement`, `ao_compatibility`, etc. discovered and auto-enabled. Biolith logged `Applying biome placement data from 1 source(s)`. This proves loading/registration, **not cave rarity, crafting or worldgen quality**.
- No Worldgen registry failure prevented new Overworld generation or save.

**Startup timing:** ModernFix measured **262.906 seconds** to load game and open world. Note first-time integrated-world creation, not a warm-start benchmark.

## Nonfatal errors — prioritize by affected gameplay

1. **Two original Flight Rings smelting recipes reject legacy string result.** `flight_rings:smelt_basic_ring` and `flight_rings:smelt_advanced_ring` failed 1.21.1 recipe parser (`Not a JSON object`). **Source fixed for NEXT build:** Paxi `ao_flight_balance` overrides both, preserves original salvage gold-ingot/netherite-ingot behavior using `result:{id:...,count:1}`. New crafting recipes were auto-loaded as datapack but user still needs to verify them in JEI.
2. **Windmill structure-set collision:** Structure Essentials at source log line 6154: exact duplicated salt **353987075** between `create_easy_structures:windmill` and `create_structures_arise:windmill`. Author's published upstream `SmartStreamLabs/Create--Structures-Arise` `src/main/resources/data/create_structures_arise/worldgen/structure_set/windmill.json` confirms native **spacing 90/separation 10/salt 353987075**. **Source fixed for NEXT build:** `release_030/structure-density.json` and generated `ao_structure_density` override preserve spacing 90/separation 10 and set salt **1543892757** for *Create Structures Arise windmill only*. Salt independence removes one placement-grid coincidence, **does not guarantee no structure bounding-box intersections**. Existing Create Rustic barn/windmill/smithy/well density changes continue separately.
3. **Worldgen data tag mismatch:** `additionalstructures:has_structure/skeleton_skull` requires `minecraft:pale_garden`, a biome absent in MC 1.21.1. This invalidates the tag and may suppress skeleton-skull structure eligibility. **Next audit:** recover exact Additional Structures 6.3.2 native tag and make pale-garden reference optional WITHOUT dropping other eligible biomes. Don't replace the whole tag with made-up biomes.
4. **Other content errors (non-worldgen launch blockers):** malformed `traveloptics:element_fire` entity tag JSON; `traveloptics:can_cast_reversal` referencing missing `#forge:tools`; Fungi Delight references missing `forge:mushrooms/*` tags; Iron's Jewelry `irons_jewelry:generate_jewelry_test_materials` loot table uses `#irons_jewelry:gem` / `#irons_jewelry:metal` in a resource location, causing parse failure; Astrological atlas `astrological:mask` unknown type; Enigmatic Legacy cosmic cake missing texture; BetterEnd Patchouli guidebook failed; Bumblezone has 4 invalid optional trade entries. Most should be fixed in independent technical-content polish after worldgen, not used as evidence that worldgen is valid.
5. ~26 GeckoLib animation parsing errors (not fatal), FTB Library warns about legacy invisible entity icons, and hundreds of invalid `ItemStack` registry keys (including old `byg:snowdrops`, `supplementaries:quark/hanging_sign_blossom`, and `minecraft:air`). **Inspect structure chest/template sources and track loot loss**, especially if naturally discovered structures contain empty/incorrect items. Do not globally replace all old IDs without owner attribution.
6. One POI data mismatch at Overworld `(-43,-36,375)`. Not a crash; prioritize only if villagers/navigation/POI corruption repeats at reproducible coords.

## Performance numbers from this exact session

- **FreeTerraForged:** 2,952 chunks generated; 464,846 ms cumulative thread time; **157.47 ms per chunk/thread**, peak **9 threads**; **413,307 ms wall time**, **7.14 real chunks/sec**, theoretical 57.15, reported **12.5% parallel efficiency**.
- **Integrated server** `Can't keep up!` **5** times: 18,932 ms (378 ticks), 3,388 ms (67 ticks), 3,591 ms (71 ticks), 5,355 ms (107 ticks), 2,314 ms (46 ticks). User can expect noticeable fresh-chunk stutters, consistent with observations from prior worldgen tests. **Root cause not proven** just by these lines; Streams Reflowing reports expensive `SR-FILL` interpolation and urgent/prefetch sessions, plus heavy FTF parallel chunk generation. Avoid claiming GPU FPS or dedicated-server TPS from this integrated session.
- New client has NVIDIA RTX 4070, Embeddium 1.0.15, NeOculus 1.8.7, NVIDIA driver workarounds; renderer warns NeOculus modifies Embeddium internals. This stack booted here, but shader performance/visuals were **not tested** (`Shaders disabled because no valid shaderpack is selected`).
- Streams Reflowing public documentation explicitly notes first-generation terrain prefetch, temporary stalls during fast exploration, recommends **Chunky pregen** and performance-preset tuning. It is a *possible* source of slowdown, not sole confirmed culprit.

## Additional structure-set salt warnings (NOT automatic faults)

Structure Essentials warns about ~25 reused salts, many intentionally across dimensions/biomes or base-game/default behavior. Cross-dimension or alternate-biome reused salt is **not evidence of geometric collision by itself**. Do not bulk randomize all native salts. Prioritize if user saw real intersections in same biomes:
- Create Arise windmill vs Easy Structures windmill: source fix staged (above).
- `aquamirae:shipwreck` vs `minecraft:shipwrecks` salt **165745295**: may be intentionally aligned to *reduce* overlap; **don't change without native placement/intent check**.
- `betterfortresses:fortress` vs `betteroceanmonuments:ocean_monument`: Nether vs Overworld; shared salt harmless in practice.
- Structory Towers ordinary/ultra-rare/End share 420699602: potential intentionally aligned grid; audit if overlaps prove real.
- Other vanilla/T&T/Repurposed/nova sets: inspect biome eligibility and placement type before editing.

## Worldgen freeze acceptance STILL OPEN

1. **Actual landscape/biome inspection:** two fresh seeds; prairie reduced, baobab/dryland/tropical rainforest and dacite shores found, mountain/coastal shapes no jagged seams, modded structure selection parity.
2. **Coastal/ocean test:** FTF + Deeper Oceans + NeoReefRedux + Hybrid Aquatic + Aquamirae, sea floor/coral, warm/frozen/deep biomes, underwater villages, YUNG monuments and shipwrecks, ocean floor height/structure clipping. No actual underwater location checks appear in this log.
3. **Bridges and streams:** YUNG's Bridges official compatibility acknowledges tiny/deep TerraForged rivers and steep banks may prevent placement; Streams Reflowing changes terrain after/beside other placement. **Structure biome eligibility already fixed but geomorphology not.** Need two seeds/coords and bridge overlap types; no blind frequency multiplier or promise of perfect bridge-on-stream geometry. See https://www.curseforge.com/minecraft/mc-mods/yungs-bridges and https://modrinth.com/mod/streams-reflowing .
4. **Structures:** rare independent WDA/IDAS lighthouses, Block Factory Dragon Tower grid/overlaps, Create Rustic collisions, new independent Create Arise windmill salt, Farmers Structures, Black Spiral and Better Bastions. Keep WDA Mushroom Village only Mushroom Fields, Coliseum and Blimp disabled.
5. **Underground dragons:** fire/lightning cave biome targets all registered Overworld, ice cold/snowy only; Paxi detected but natural cave frequency not proven.
6. **Nether/End:** log created dimension registries but does NOT show player entering/visiting Nether or End; test first/repeat transitions and heavenly ship placement plus Black Spiral, Incendium/Better Bastions. Solo Quests dedicated-server individual completion still untested (log is SINGLEPLAYER).
7. **Performance/freeze:** baseline no shaders/DH, cold vs warm terrain chunks, dedicated server 5–7 players, target acceptable stutters and source provenance before picking permanent server seed and pregen.

## Test8.3 targeted corrective candidate (NOT new feature wave)

Source on `structure/test6` bumped to `0.3.8-worldgen-prefreeze-test1.3`; 265 CF project refs **unchanged**. Private preview assembled from user's successful Test8.2 archive, adding **only three** datapack JSONs (two Flight Rings salvage recipes; Create Arise windmill salt override), changing archive root manifest version/name, preserving all other **1,076** original uncompressed members byte-for-byte:
- ZIP `Ambient-Odyssey-v0.3.8-Test8.3-Windmill-RecipeFix-PRIVATE.zip`, **71,024,039 bytes**, SHA-256 **`68b1b0ec40384428ec94d1df7f05af54eac97718c2a16f837b3fd62b338c8245`**, **1,080** entries, **265** manifest projects, root manifest and ZIP CRC static checks PASS.
- **NOT runtime-tested**. This is still a private ZIP bundling user-supplied Better Bastions and NeoReefRedux JARs. Not a CurseForge-public moderation-ready export. Exact CI builder and all validators in a fresh Git checkout still need execution.
- Expose it as the next optional test build **without discarding the user's already-working Test8.2 save**. New structure salt takes effect in **new chunks/new worlds**, and existing saves may show old placements.
