# Ambient Odyssey v0.4h — performance and optimization patch preparation

**Status: preparation only; no performance tuning or Minecraft runtime testing claimed.**

**Base:** `experimental/quest-atlas-website-q1-20261010` @ `48444e75e510363b155320a387fe97d7c40aaca9`. That branch was 11 commits ahead of the Q1+FTB Field Manual branch and preserves the Quest Atlas website. Do not start from stale `main`, overwrite rollback branches, or remove established content merely for FPS.

## Verified baseline (packaged ZIP, static analysis)

The 2026-10-10 Actions artifact [38080830259](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259) has a **CF-References** inner ZIP with SHA256 `c4b7fa1595a4aa99f6cc9a504266c5acaf6518c7a47b67186cc69473a6fbd88b`, and a separate private variant. The 331-reference CurseForge manifest uses Minecraft **1.21.1**, **NeoForge 21.1.252** and **recommendedRam 10240 MiB**. The inner reference ZIP contains 1,469 members. The 73.5 MB Tan's Huge Trees custom ZIP is a preserved *packaging* payload, not proof of expensive render frames.

Existing packed `defaultoptions/options.txt` suggests render **12**, simulation **6**, max FPS **160**, VSync **off**, GUI scale **3**. Weather volume **0.2**, ambient **1.0**, block **0.4**. Source includes configs for Embeddium, Lithium, ModernFix, FerriteCore, ImmediatelyFast and Spark; these configs alone do not prove exact matching binaries are installed. Embeddium culling and texture optimization switches are already on; ImmediatelyFast's experimental switches are off. Structure Essentials fast lookup is already on, and its structure placement logging is off. **Do not blindly stack new renderer/performance mods.**

Two audit leads, **not diagnosed bottlenecks**: Spark's `backgroundProfiler` is currently `true` (measure idle overhead before changing), and `config/spark/tmp*` files are exported (review for safe packaging cleanup). Questlog's periodic visit-objective polling is another source-level server profiling candidate, not a measured TPS issue.

## Controlled sequence

1. **P0 reproducibility:** import a fresh *inner* CurseForge ZIP; verify actual installed 331-project binaries, Java 21, server-sidedness, startup, and rollback integrity. First boot and first worldgen are separate timings.
2. **P1 evidence:** fixed seed, coordinates, worldgen preset, resource packs, render/sim distances, player count, weather and hardware. Three warmed trials per scenario. Compare initial generation versus **already generated** terrain, not just a single FPS number.
3. **P2 client:** collect average/p50 FPS, 1% low FPS, VRAM, heap/GC and shader-OFF baseline. A/B 12/6 versus 10/6; shader and Distant Horizons compatibility separately before combined testing. Do not assume DH is installed or compatible.
4. **P3 server:** collect median/p95 **MSPT** and TPS, startup logs, memory/GC, actual player AI/entity ticks, quest polling, 2-player then 5–7-player trips. Aim for sustained 20 TPS (~50 ms per tick available), but calibrate expectations to tested hardware and chunk state.
5. **P4 generation:** profile Free TerraForged, biomes, Streams/Reflowing, road/terrain mods and heavy structures on new chunks; pregeneration can *move* the cost to an earlier stage, not eliminate it. Preserve modded-biome eligibility, WDA/IDAS/Farmers frequency fixes and completed jigsaw repairs.
6. **P5 visuals/audio:** separately test shaders, leaves, particles, entities, weather and the under-canopy versus above-canopy ambience issue. Streams Reflowing and rain were reported too loud even with category defaults; tune actual producing sound sources, not just overall volume.
7. **P6 controlled patch:** make one low-risk source or config change per A/B group, record result and SHA256, run static validation and repeat gameplay gates. Never claim a fully working release before real client/server tests.

## Acceptance and safeguards

- Maintain 331 pinned references, 50 Questlog Q1 quests, 32 FTB Field Manual pages, WDA quest rewards, and the Mine Cells connector architecture unless a separate researched change is approved.
- Preserve vanilla/modded biome placement, structure integrity, mob variety, worldgen beauty, compatibility, existing renderer stack, and older rollback builds. Treat 30% sleep, Curse/Origin progression and inventory HUD behavior as regression checks.
- Metrics from static archive inspection are **not** FPS, MSPT, chunkgen throughput, actual JAR validation, memory use, server compatibility or multiplayer success.
- Public ZIPs must not redistribute the private NeoReefRedux binary without confirmed rights. Never automatically upload user raw logs or identifying system paths.
- `tools/perf_preflight_v04.py` and `tests/test_perf_preflight_v04.py` are planned read-only build-audit helpers; report build ZIP diff and evidence before any config changes.

### Runtime test record (all NOT TESTED)

| Test | Record | State |
|---|---|---|
| Clean boot, no shaders | launch-to-menu, heap, warnings | NOT TESTED |
| New Free TerraForged world | seed, spawn time, GC, first chunk stall | NOT TESTED |
| Reopen same world | startup time, heap, TPS | NOT TESTED |
| Static forest scene, water/rain | FPS p50 and 1% lows, audio, GPU/VRAM | NOT TESTED |
| Fixed 2 km new-chunk path | chunk count, elapsed, server p95 MSPT | NOT TESTED |
| Exact same pre-generated path | FPS lows, GC, p95 MSPT | NOT TESTED |
| Mine Cells return + major structures | stalls, portal regression, placement correctness | NOT TESTED |
| Two-player then 5–7-player dedicated server | MSPT/TPS, entity/quest ticks, networking | NOT TESTED |
| Shaders ON and optional DH A/B | FPS lows, artifacts and memory separately | NOT TESTED |

Base immutable artifact: [Q1+FTB Field Manual verified build](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259/artifacts/11680318532). No playable performance claims or optimized ZIP were produced by this preparation task.
