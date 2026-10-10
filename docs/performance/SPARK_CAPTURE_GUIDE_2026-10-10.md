# Spark capture guide — Ambient Odyssey 0.4h (10 October 2026)

**Purpose:** collect *usable, comparable* CPU/tick evidence before editing config or mod pins. This is a working worksheet, not a diagnosis or gameplay validation.

User-supplied first Spark link: https://spark.lucko.me/yDmMR0wqyC . The viewer and raw endpoints were inaccessible to the analysis environment on 2026-10-10. **No content, thread timings, TPS, MSPT, allocation totals, mod names or flame graph were successfully read from that recording. Do not invent findings.** A correct-looking viewer URL indicates the appropriate profiling workflow; it does *not* prove a useful capture duration or that the laggy scenario was sampled.

Official docs: https://spark.lucko.me/docs/Command-Usage , https://spark.lucko.me/docs/Using-the-viewer and https://spark.lucko.me/docs/misc/Raw-spark-data .

## How to make the next recording correctly

### Singleplayer / NeoForge client

Wait until the game is fully loaded in a disposable test world. In chat:

```text
/sparkc profiler start --thread * --timeout 120
```

Perform **one defined test** for most of those 120 seconds: stationary in an established forest, travel in already generated terrain, actively fly/explore new chunks, or fight a mob-rich encounter. At timeout Spark normally publishes a new URL; you can also stop early with `/sparkc profiler stop`. Run separate sessions instead of mixing all scenarios into one unattributable two-minute average. If the installed client uses different command aliases, check in-game command suggestions rather than silently assuming `/spark` is the client command.

In singleplayer, `--thread *` matters because the client and integrated-server threads exist in one JVM. Do not interpret a large sleeping/parked fraction as lag. Spark is a sampled CPU profiler, **not a GPU/shader frame profiler**; use an FPS/frametime overlay separately.

### Dedicated NeoForge server

From operator chat or server console:

```text
/spark profiler start --thread * --timeout 120
```

Run one repeatable server load scenario. Record player count and generated versus ungenerated chunks. Capture server TPS/p95 MSPT separately. A slow-tick-only follow-up can be tried with `/spark profiler start --only-ticks-over 50 --timeout 120` if that version accepts the flag; this excludes healthy ticks, which is *not comparable* to normal whole-window CPU share.

### Four high-value independent captures

| Scenario | What to do | What it isolates |
|---|---|---|
| A. Warm idle | Existing world, stand still with shaders OFF after initial loading | Baseline entity/block ticks, GC and idle client cost |
| B. New terrain | Fly a reproducible path through ungenerated chunks | FTF, terrain noise, streams, roads, tree/structure/worldgen tasks |
| C. Warm travel | Repeat precisely the same path after chunks are generated | Chunk loading/rendering, entities and IO without full fresh generation |
| D. Populated base/combat | Fight in entity-heavy area or maintain player-built systems; 2 then 5–7 players in dedicated server when ready | AI, pathfinding, player activities, force-loaded chunks, quests |

For each: world seed/preset, dimension, XYZ route, player count, resource packs, shader status, render 12/simulation 6 or declared deviation, allocated Java heap, Java version, recording duration, whether server or client command, and subjective lag symptom. Use **3 runs** per comparable condition, not a one-off result. Use separate baseline and experiment worlds where generator settings change.

### Sharing detailed evidence

The viewer has a download/export option for the **original `.sparkprofile`**. Export this or attach JSON from `https://spark.lucko.me/<ID>?raw=1` (metadata only) and, if needed, `&full=true` (possibly huge). Upload the file directly to the analysis chat if remote viewer fetches fail. Review before sharing: profiles can include player identifiers, machine and mods metadata. Preserve original unchanged for reproducibility.

### How to interpret

1. Choose **Server thread** for TPS/MSPT, **Render thread** and client workers for client CPU frame work, and individual chunk/worldgen executor threads for terrain costs.
2. Expand hot paths, filter sleeping/waiting, and use flat sources/mod attribution where available. A 90% method on a mostly sleeping server thread is not automatically a real performance crisis.
3. Check *absolute* tick duration and whether the session was actually lagging. At 20 TPS, a tick has a 50 ms budget, but a server can sleep the unused time. Repeated p95 MSPT above 50ms is evidence of missed ticks.
4. Check garbage collection and heap only if there are spikes correlated with stutter. High available RAM is not proof of a RAM bottleneck.
5. A GPU-bound shader bottleneck may not show as a high-CPU Spark hot path; compare frametimes shader OFF / ON.

## Current data state

| Recording | Accessible and parsed? | Verified findings |
|---|---|---|
| yDmMR0wqyC | NO | None; cannot determine thread, sample duration, load state or culprit |
| Warm idle | NOT TESTED | none |
| New chunks | NOT TESTED | none |
| Warm travel | NOT TESTED | none |
| Server 2–7 players | NOT TESTED | none |
