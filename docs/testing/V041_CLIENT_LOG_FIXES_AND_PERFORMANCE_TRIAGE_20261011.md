# Ambient Odyssey — 11 October 2026 client log audit and performance start

Source: user-supplied 9,447-line **client** `latest.log` (03:47 local, 11 October) from the **328-ref Mine Cells Structure Control** instance, with manually installed AO Questlog bridge v0.1.1, **without** Streams Reflowing or the custom Streams compatibility addon. Private player IDs, file paths, seed and coordinates are deliberately not reproduced.

## Outcome

The client successfully loaded into the world, entered Mine Cells Prison, returned to the Overworld and saved/shut down normally. No fatal crash. **Do not use this to sign off the newer 329-ref Streams + Mine Cells combined build**. User reports Curios equipment appears fine, and Luki key textures appear correct. The Questlog Q is reported visually overlapping the fifth backpack slot.

## Sorted engineering findings

1. **Reproducible off-thread entity creation** (3 Cupboard warnings with genuine stack traces):
   - `com.alganaut.hominid.registry.event.HominidClientEvents.onEntityJoinWorld` at line 76/85 calls `ServerLevel.addFreshEntity` from chunk-generation / structure template placement workers.
   - `tannyjung.tanshugetrees_core.game.GameUtils$Mob.summonWorldGen` and `TreePlacer.place` similarly invoke entity creation from generation workers.
   - **Direct sources identified.** Explore source-supported scheduled-on-main-thread fixes or opt-out of the problematic spawned entities without gutting Hominid or tree generation. **Do not add simplistic async wrappers** (worldgen lifecycle and duplicate entity risk). Mark game/data safety concern, not proof of crash.
2. **Severe cold-chunk/server-thread stalls:** 12 `Can't keep up` reports, 27,486 ms worst, then 5,657/5,193/5,154 ms among others. The worst stall was near a teleport into a large structure with concurrent generation warnings; attribution **not yet proven**. Benchmark new versus pre-generated terrain. A new Spark profiling capture is needed for exact thread attribution.
3. **Worldgen item NBT provenance:** 540 `Item must not be minecraft:air` errors while exploring, plus `redeco:hammer`, `biomesoplenty:rose_quartz_shard` unresolved registry references. Don't rewrite generic air as arbitrary items globally. Audit source mod-authored structure NBT with exact registry keys and item container paths; repair only pinned matching templates.
4. **Luki Woodland Mansions structure:** 4 `mansions:mansion/bottom_back_left` unresolved jigsaw template pool warnings while generating a mansion. Existing **key texture** patch is unrelated and works in user's gameplay. Inspect exact native JAR for the correct missing pool and its intended terminal; fix source-backed data, not fabricated empty pool blindly.
5. **Dungeon Crawl:** one `Failed to fetch a mob spawner` at generation; matches known block-entity lifecycle issue. Retain dungeon content; isolate the specific native generation path before modifying. 
6. **Worldgen biome tag errors:** 4 failed tag loads refer to `streamsreflowing:stream` or tags dependent on it, in this Streams-absent control build. **The newer combined build includes Streams Reflowing 2.14.4; retest before patching the tags.** The missing tag can affect sky villages, YUNG's bridges and dragon-cave biome eligibility in this old control.
7. **Resource warnings:** 138 missing-texture model warnings and 124 additional missing blockstate-variant warnings, plus model/animation warnings including Amendments foods and GeckoLib. Prioritize visible broken items or blocks after gameplay confirmation; model problems can be real despite no crash. Luki's key visuals are a user-reported pass.
8. **Legacy modifiers:** 572 unknown legacy `forge:` attribute warnings (mob and structure NBT, typically gravity, step height and swim speed); exact native source attribution required for 1.21.1 migration. Do not blanket-rewrite entity NBT without checking target registries and semantics.
9. **Other:** Bumblezone 4 missing required trades; BetterEnd Patchouli guidebook failed to load; Irons Jewelry and Traveloptics tag/model errors; occasional JEI long recipe registration on startup; non-fatal GlitchCore/renderer mixin taint. These need source-specific investigation after higher-priority structure/data faults.

## UI and quests

- v0.1.2 of AO client bridge updates button widget coordinates every frame from Better Inventory's **current** GUI origin rather than its initial position and centers the 24×20 native-style Q tab just past the settings gear. Keeps its notification `!`.
- Questlog 50 actual adventure quest definitions are separate from FTB's original WDA quests and 32 informational pages. Source SNBT previously attached **32 checkmark tasks** to those 32 FTB articles, which could reasonably look like duplicative quests. The current branch changes only the three AO educational manual chapters to `tasks: [ ]`, retaining `rewards: [ ]` and the WDA chapter exactly as shipped. FTB auto-completion/visibility requires client validation.

## Performance work already recovered

Recovered previous performance-preflight branch `performance/v0.4h-preflight-20261010` docs, benchmarks, profiler instructions and read-only ZIP comparison code into this current combined branch. Profile with the **actual 329-ref + 2-addon** build rather than legacy 331-ref references; the performance preflight accepts `--expected-refs 329`. No FPS/MSPT speedup claimed or FreeTerraForged terrain changed.

## Next concrete work, in order

1. Confirm final Q position and FTB manual visibility in client (no overlapping panels). Confirm new combined Streams profile, fresh-world Mine Cells and overworld tag loads.
2. Audit/fix Hominid and Tan's tree off-thread spawning paths with pinned native source and safe lifecycle controls.
3. Audit pinned Luki Mansion template pools, Dungeon Crawl spawner behavior, invalid air items and worst legacy attributes.
4. Three matching Spark samples: warm stationary, new-chunk travel and repeat over pregenerated chunks; report actual server thread and chunk workers separately. Then implement source-supported worldgen/renderer config A/B patch, with rollback and no unfounded benefit claim.
5. Dedicated server 2-player, then 5–7-player and backup/pregeneration only after roster/worldgen freeze.
