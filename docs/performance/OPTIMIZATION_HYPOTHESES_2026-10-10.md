# AO v0.4h — diagnosis-driven optimization candidates

**Not a measured Spark diagnosis.** The 2026-10-10 user Spark capture `yDmMR0wqyC` could not be read. These are *source/config-backed* candidates ranked by expected impact if each symptom is found, not claims that any named mod causes lag. Preserve the 331-ref pinned mod roster, Questlog Q1/FTB, high-value structures, biome diversity, Free TerraForged identity, Mine Cells, key gameplay systems and all rollback files until independent testing proves a change is safe.

## What we actually found in source

- Free TerraForged preset `release_030/overrides/config/freeterraforged/presets/Ambient Odyssey 0.3.1.json` uses complex terrain and climate noise plus `worldHeight: 512`, `worldDepth: 256`, `fancyMountains: true`, 5-octave continental and biome-edge noise settings. These values are not automatically errors, but a strong reason to profile expensive new-chunk processing before touching scenic terrain.
- Tan's Huge Trees `release_030/overrides/config/tanshugetrees/config_world_gen.txt` **explicitly warns** that large `min_distance` can slow region pre-location and larger `group_size` can affect scanning. Its custom pack is 73.5MB inside the ZIP; compressed asset size itself does not establish runtime overhead.
- `release_030/release-lock.json` pins **Streams Reflowing 2.14.4** and **The Roads More Travelled**; users observed slow terrain loading in previous tests. Association is *not* a sampled hotspot.
- `release_030/overrides/config/structureessentials.json` has `useFastStructureLookup: true`, structure placement logging off, no global distance enforcement. Current worldgen patches already fix many structures; avoid reinstating global collision scans or debug logging as a performance 'fix'.
- `release_030/overrides/config/ftbchunks-world.snbt` currently allows `max_force_loaded_chunks: 25` per team; `force_load_mode: "default"`, `long_range_tracker_interval: 20`. This is a **capacity/risk review**, not evidence that chunks are currently force-loaded or laggy.
- Existing `embeddium-options.json` enables entity/fog/block-face culling and `immediatelyfast.json` has safe core optimizations on with experimental rendering toggles off. NeoOculus shader renderer is pinned in the lock. Extra renderer/mixin optimizers should not be added blindly.
- `modernfix-common.toml` specifically pins `jepb:jei_plugin` to the main thread. Do not remove blacklist without an actual crash/compatibility A/B, as it may be compensating for a compatibility fault. `lithium.properties` has no custom feature overrides.
- `spark/config.json` has `backgroundProfiler: true`; Spark temporary paths are packaged. Benchmark profiler overhead if relevant, but do not present this as a major lag fix.
- Prior user audio feedback: Streams Reflowing water and rain overpower nature ambience, and some insects/birds vanish under canopy. This needs **separate acoustic balancing** even if no measurable FPS/TPS problem exists.

## Branch-ready proposed A/B experiments — choose ONLY matching hot path

| Candidate | Trigger from actual Spark / gameplay | Variant to test | Risk / acceptance |
|---|---|---|---|
| GEN-01 terrain | New chunks disproportionately slow, FTF noise calls high | Clone preset into disposable world and reduce selected terrain/noise complexity *one knob at a time* (e.g. optional fancy terrain / selected octaves), compare same seeded new-chunk route | High visual/world-save compatibility risk; never edit live world. Favor retaining spectacular mountains if benefit small |
| GEN-02 rivers/roads | Streams Reflowing or roads placement search dominates worldgen worker samples | Compare present pinned config to narrower spawn/search/frequency options **only where the mod exposes supported settings**; no unverified config keys | Preserve interesting roads/streams, biome placement, bridges and structure integration; test generated terrain |
| GEN-03 trees | Huge Trees pre-location/group-scan methods are hot | A/B smaller species group sizes and overly large `min_distance` for only expensive species in throwaway world | Avoid cutting overall tree diversity or damaging canopy/landscape; maintain locked config semantics |
| GEN-04 structures | Repeated jigsaw/placement/collision searches dominate new-chunk samples | Audit retry-heavy *minor* structures and config-backed placement filters; decrease specific low-value ruin/graveyard attempts before touching iconic castles/boss arenas | Must preserve modded-biome selection, Farmers Structures presence, WDA, IDAS and curated large/dimensional content |
| ENT-01 entities | Entity tick/pathfinding high in warm stationary and 2+ player tests | Lower spawns of low-value pest/duplicated wildlife, cap expensive mobs *by species*; retain ecological variety | User prefers animal variety but explicitly dislikes pointless gorillas/pests; don't cull unique bosses |
| ENT-02 chunk loading | Persistent chunk ticks despite no nearby players or idle bases | A/B FTB Chunks 25 force-loaded/team vs smaller **server-only** 9–16 limit and offline-mode policy | First inspect actual loaded chunk counts, rights and expected farms; don't remove feature without need |
| QUE-01 Questlog | Questlog visit polling/FTB progress methods measurable on server thread | Benchmark 0/50/200 active objectives, aggregate/reduce unnecessary world-position checks only if APIs support safe changes | Never break 50 Q1 quests, 13 chapters, 32 informational FTB pages or per-player reward semantics |
| RND-01 shader/GPU | GPU frame cost high, Spark CPU render thread not hot | Shader OFF vs Solas/Complementary; adjust shadow distance, volumetrics, reflections and shader internal resolution using *supported* shader settings | Keep pretty default for capable PCs, offer performance preset without shipping ambiguous duplicate client configs |
| RND-02 entities/particles | Render thread/entity/particle CPU hot in shader-OFF baseline | A/B particle density, shadow-casting particles, weather FX, cosmetic visibility; review Embeddium chunk builder auto-thread count `0` only with evidence | Preserve iconic ambience and avoid existing engine/mixin conflicts |
| MEM-01 garbage collector | Pauses correlate with GC/heap occupancy | Compare 8GB/10GB/12GB **client** allocations on same machine, Java 21; choose lowest stable allocation | Bigger heap may increase pauses, dedicated server memory is separate |
| MEM-02 load overhead | Long resource/JEI startup, no ongoing stutter | Profile initialization and recipe/index building separately; do not delete content or blacklist plugin without explicit source evidence | Load time improvement alone cannot be called gameplay FPS increase |
| AUD-01 sound mix | Rain/water unusually loud; no demonstrated CPU hotspot | Build source-specific streams/rain acoustic patch, test forest canopy versus open-air with Sound Physics Remastered | Soundscape QA is perceptual; master/weather slider alone won't correctly rebalance every sound source |
| DIAG-01 Spark | Profiler overhead measurable at idle | A/B `backgroundProfiler` true/false, remove only temporary generated Spark export files after safe packaging audit | Diagnostic quality vs tiny potential overhead; do not pretend it fixes major worldgen |
| SERVER-01 chunk pregeneration | Steady loaded terrain fine; only unexplored chunks stutter | Pregenerate server map **after roster/worldgen finalized**; keep radius reasonable and run before players join | Shifts workload to setup, raises storage and startup duration; changed worldgen configs won't retroactively repair chunks |

## Sequence, acceptance and no-regression rules

1. **Receive first actual Spark profile** as `.sparkprofile` file or `?raw=1&full=true` JSON. Record platform/thread sample duration, periods of actual lag, and main method signatures. If link inaccessible, mark UNKNOWN.
2. Make 3 separate baseline profiles (warm static, new chunks, same path pre-generated); shader/frame-time A/B separately.
3. Classify whether issue is CPU main thread, async worldgen, GPU shader/VRAM, GC/heap, slow IO or actual world tick performance. Do not optimize a subsystem without symptoms or measurements.
4. Implement maximum *one* variable group at a time on a performance branch, verify generated ZIP diff, keep mod pin list and quest JSON IDs stable. In-game worldgen acceptance: biome balance, structures, rewards, roads/streams and terrain quality.
5. Compare 3 trial medians and worst stutters, not one instantaneous FPS; record reproducible coordinates and exact Java/JVM settings.
6. Only ship reversible patches with meaningful improvement and no evidence-backed compatibility regression. Include separate client-quality presets rather than one-size-fits-all low quality.

**Current status:** Proposals ONLY; no runtime-tested bottleneck, performance gain or solution has been proven.
