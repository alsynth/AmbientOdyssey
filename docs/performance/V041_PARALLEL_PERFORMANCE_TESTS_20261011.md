# Ambient Odyssey v0.4.1 — parallel performance benchmark and patch gate

**Date:** 11 October 2026
**Branch:** `performance/v041-parallel-benchmark-prep-20261011` (based on `experimental/v041-engineering-repairs-20261011`)
**Status:** tooling and test plan, **not an optimized release or a new gameplay benchmark**.

## What to test

Use the same experimental **329-reference** Engineering IDAS import and the three source-built AO addons for the initial profile. Do **not** benchmark the older 331-reference release or 328-reference Mine Cells control as if mod counts/worldgen were identical. The official 0.4.1 engineering ZIP packages the native Questlog inventory button, Streams × Mine Cells compatibility and worldgen-safety addon. Preserve the working Mine Cells control save separately.

Initial known ZIP SHA-256 from the delivered 11 October import: `b785f60fcf83218632b57f4c13c2d226d302d583c62d7cdf5c7261f895341b0b`. **Verify locally before writing trial data**. A new re-export with a different digest must be recorded separately, even when its manifest roster matches.

**Fixed starting conditions:** Minecraft 1.21.1 / NeoForge 21.1.252; Java 21; shaders OFF; no DH-style LOD changes; render 12, simulation 6; VSync OFF; same FPS limit, resource-pack order, Java heap and PC; daytime and weather held consistent when practical. Record GPU, CPU, storage and total system RAM separately once. Do not force-install new performance mods into the benchmark profile.

### Pass 1 — minimum ~8 minutes, one pass each for triage

| ID | Window | 120-second activity | Record |
| --- | --- | --- | --- |
| P1-IDLE | Warm idle | After joining and allowing caches to settle, stand in already generated terrain | FPS and 1% lows, p95 MSPT if available, Spark, heap |
| P1-COLD | Cold chunk exploration | In disposable/new ungenerated chunks follow a fixed flight or walking direction; avoid teleports during the sample | FPS, chunk throughput if logged, Spark server thread and worldgen workers, stutters |
| P1-WARM | Same generated route | Traverse the exact same path after its chunks have saved, without newly generating beyond the boundary | FPS, p95 MSPT, Spark, stutters |
| P1-COMBAT | Existing structure / mob area | Spend 120 seconds near a repeatable group of mobs, no new chunks | FPS, server MSPT/TPS, entity tick profile |

For each in singleplayer (operator permissions required):

```text
/sparkc profiler start --thread * --timeout 120
```

Dedicated server uses `/spark profiler start --thread * --timeout 120`. Verify command syntax with in-game autocomplete; aliases/flag support vary by installed Spark build. **Do not run simultaneous Spark profilers.** Start a recording just before the scenario and capture the URL or original `.sparkprofile` when it finishes.

For a first diagnostic pass, one 120-second recording per scenario is fine. **For comparative optimization claims**, repeat matched runs **three times** per scenario after a warm-up, not just one. Keep a fresh save/route for every cold-world trial; the first visit cannot be repeated as cold on the same generated chunks. A matching warm trial can follow each cold route on that same save. When comparing *worldgen config* changes, create **independent copies from the same pre-generated-state seed/preset** and confirm geometry quality separately.

### Pass 2 — controlled A/B, after Pass 1

1. **Spark background overhead:** use the existing separately packaged Spark ON and Spark OFF v0.4.1 builds with matching settings/seed/hardware, without an active manual Spark profiler for the FPS overhead portion. Spark OFF does *not* mean removing the Spark mod. If background overhead appears meaningful, run a separate active manual Spark capture to attribute.
2. **Render distance:** compare in-game render 12 / simulation 6 against render 10 / simulation 6 **on the same build**. Reload/stabilize before recording; do not combine with shader changes. This is a client view-distance experiment, not evidence terrain generation itself became cheaper.
3. **Shaders:** compare OFF vs one fixed shader preset in the same representative warm scene; log shader preset, GPU and frame-time/1%-low readings. Spark is a CPU sampler, not a GPU profiler.
4. **Multiplayer server:** after a stable singleplayer control, run stationary, new/warm travel and entity-heavy profiles with 2 players, then 5–7, on a dedicated server. Same mod/addon JARs on both sides except intentionally client-only Questlog GUI. Record server MSPT/TPS independently of client FPS.

### Important metric distinction

**"Can't keep up! Running 27486ms" is one server stall warning, NOT p95 MSPT.** Historical log counts can establish regressions and the frequency of *reported* stalls, but full p95 MSPT/TPS requires a per-tick measurement from Spark or a server performance report. Similarly, the FreeTerraForged shutdown summary gives *session-wide* chunk generation and thread efficiency, not the throughput of one isolated two-minute route.

Use `python tools/perf_v041_log_report.py latest.log --out performance-log-summary.json` to extract privacy-safe stall and FTF summaries (never exports raw player identifiers/paths). Use `docs/performance/V041_PARALLEL_BENCHMARK_TEMPLATE.csv` to enter readings (set `status=MEASURED` only for actual observations), then:

```text
python tools/perf_v041_trials.py docs/performance/V041_PARALLEL_BENCHMARK_TEMPLATE.csv --out build/v041-performance-trials.json
```

Incomplete rows stay **PLANNED** and cannot become fabricated performance gains. The aggregator labels fewer than three trials PROVISIONAL and detects mismatched settings within a group. It does not automatically conclude a variant is faster based on incompatible data.

## Where to profile first

Earlier 11 October **328-control** client log (not the new 329-ref candidate): 12 separate server "Can't keep up" warnings, worst **27,486ms**. First 328-control log recorded 3 warnings and FreeTerraForged 1,840 generated chunks, 5.13 real chunks/sec, 121.10 thread-ms/chunk and 6.9% parallel efficiency. These samples have different time windows and scene workloads; don't present one as performance regression vs the other.

Ranked testable areas **after** Spark evidence:
- **Worldgen workers dominate cold only:** identify specific FreeTerraForged / Streams Reflowing / Tan's Huge Trees / Roads / structure placement hot paths. Preserve FreeTerraForged's world shape, major structures, curated biome eligibility, Mine Cells dimension bypass and user-valued ecology. Implement one source-supported config or Mixin adjustment per **isolated** A/B.
- **Server thread congested even warm:** inspect entity AI, spawner work, chunk-loading/FTB claims and Questlog objectives before touching terrain; log player count and force-loaded chunks. Keep Dungeon Crawl spawner and Hominid/Tan threading safety fixes as independently testable engineering changes.
- **Client FPS low but MSPT stable:** profile render CPU, particle/weather density, entities and shaders separately. Keep visual quality default for powerful clients and offer optional low/medium settings, rather than removing content.
- **GC/heap spikes:** compare stable Java 21 client heap allocations on one machine using equal scenarios. The pack's recommended 10,240 MiB is a suggestion, not evidence every 16-GB system should allocate 10GB.
- **Spark profiler overhead:** background-profiler OFF comparison is already packaged. No measured speed-up yet; treat as optional diagnostic until paired runs.

## Proposed patch gates

A change may enter an experimental performance patch only when (a) a measured hotspot or repeatable nuisance is linked to it, (b) source/config has a verified, reversible option, (c) 3 matched trial medians and 1% lows/p95 tick measurements are compared, and (d) Mine Cells full dungeon, overworld rivers, major WDA/IDAS/Farmers structures, quests, Curios, multiplayer and atmosphere regressions are checked. Avoid treating one lower spike as proof. Do not merge altered terrain generation into an existing survival world or begin broad pregeneration before worldgen freeze.

**Evidence to return for next engineering cycle:** four Spark URLs/.sparkprofile captures, final latest.log, completed CSV rows or equivalent typed metrics, CPU/GPU/RAM allocation once, and exact build ZIP SHA. Do not send a world seed or local PC username publicly if privacy matters; anonymize before publishing.
