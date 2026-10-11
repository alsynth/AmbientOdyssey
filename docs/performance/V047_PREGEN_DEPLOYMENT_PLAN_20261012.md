# Ambient Odyssey — Pregeneration-first performance strategy (12 Oct 2026)

**Status:** PLANNING ONLY. No production pregeneration, generated-world acceptance, performance improvement, or full server runtime validation claimed.

**Source:** Isolated planning branch based on `experimental/v046-wetsand-apotheotic-ports-20261011`. Never overwrite `main`, `structure/test6`, older performance branches, latest tested client, or rollback saves.

## User decision / deployment target

The owner intends to leave the production dedicated server running with **Chunky pregenerating a large circular Overworld around spawn before inviting the 5–7 players**. Initial target **10,000-block radius**; stretch goal **20,000-block radius**, provided storage and measured throughput make it worthwhile. Running pregeneration for hours or days is acceptable. Players should spend early exploration traveling already-generated land.

**This changes performance priorities:** pre-generating moves expensive first-generation Free TerraForged / Streams / Roads / trees / structures work before launch, but does **not** inherently increase shader GPU FPS, remove chunk disk-load/meshing/network costs, entity/block tick work, or fix corrupt structure NBT and threading. Keep shader rendering, FPS lows, TPS, entities, particles and existing-chunk loading as distinct optimization tracks.

## Scale and timing (planning calculation, not a Chunky benchmark)

Approximate circle chunk count `N = pi * (radius_blocks / 16)^2`; actual edge alignment and existing chunks change total to create.

| Radius | Approx. chunks | At 7 chunks/s | At 20 chunks/s | Required chunks/s to finish in 24h |
|---|---:|---:|---:|---:|
| 5,000 blocks | 306,796 | 12.2 h | 4.3 h | 3.6 |
| 10,000 blocks | 1,227,185 | 48.7 h | 17.0 h | 14.2 |
| 20,000 blocks | 4,908,739 | 194.8 h | 68.2 h | 56.8 |

Historical Free TerraForged summary measured **5.13** or **7.14** chunks/s on older integrated gameplay workloads; do not treat these as true Chunky/dedicated-server benchmarks or a prediction of exact time. Rate depends on selected worldgen, CPU, worker behavior, RAM/GC, server storage and encountered structures.

## Stage gates (in order)

1. **Freeze source content and worldgen**: pin the exact NeoForge 1.21.1 mod/Addon JARs, Free TerraForged preset, Biolith / biome roster, Streams/Reflowing, The Roads More Travelled, major structure/biome placement, Paxi patches, Tan's trees, Mine Cells dimension guards and other relevant worldgen changes. Repair confirmed off-thread Hominid/Tan entity spawning, invalid structure items/pools/spawners, and startup faults *before* committing to millions of chunks. Generating early locks in existing chunk geometry/structures; later configs do not retroactively change these chunks.
2. **Choose real final-world seed and spawn center**, confirm compatible Chunky NeoForge 1.21.1 JAR (official Chunky v1.4.23 available, exact installation to verify), finalize world backup/restore routine and disk quota/snapshot accounting. Do not accidentally set the center to (0,0) if actual chosen spawn is elsewhere.
3. **Pilot pregen**: empty dedicated server, radius ~2,000–5,000 in a disposable full-mod test world with all source mods and Paxi patches; record Chunky completed/processed chunks, chunks/sec, elapsed, peak heap and GC, disk-growth per 10k chunks, crashes/error rates and TPS/MSPT. Compare true saved-world behavior across stop/restart/reload, portals and representative structures. Verify Chunky skips already generated regions and supports resume. Do not infer time from compressed resource pack size.
4. **Production stage 1**: make verified pre-run backup, run 5k circle, check status, errors, disk, visual structure/biome quality and server saves, then extend to **10k**.
5. **Production stage 2 optional**: if real rate, disk and owner schedule allow it, expand circle toward **20k** without deleting/regenerating existing chunks. Estimate remaining ring size (~3.68 million chunks, roughly triple the 10k coverage) and adapt. Ensure disk free space includes temp IO, backups and continued gameplay growth; no generic gigabyte promise without measured bytes/chunk.
6. **Dimensions and boundary strategy**: consider targeted pregeneration for Nether (vanilla equivalent travel scale ~8:1 vs Overworld), End and important player-explored modded dimensions **using their actual dimension IDs and custom generation costs**. Mine Cells and bespoke dimensions require isolated testing, not blanket radius duplication. Players traveling far past the pregen edge can still generate new terrain: optionally enforce/test a compatible boundary or clearly communicate the intended first-stage world radius. A vanilla worldborder is square, unlike Chunky's circular region, so do not equate vanilla border size with fully pregenerated circular coverage.
7. **After pregen**: take a clean finalized backup, restart server, let idle load settle, and benchmark two independent scenarios: already-generated-chunk exploration and multiplayer entity/combat/quest load. Monitor 5–7 player p95 MSPT/TPS (20 TPS target), client shader OFF/ON FPS and 1% lows, VRAM, heap/GC and data transfer. Any unseen chunk generation at the edge is a separate overflow test.

## Operational commands (confirm names/permissions on installed release)

For official Chunky, server console, after selecting desired world/dimension (the name may be `world`, `overworld`, `minecraft:overworld` or another server-specific identifier):

```text
chunky world <actual-world-name>
chunky shape circle
chunky center <chosen-spawn-X> <chosen-spawn-Z>
chunky radius 5000
chunky selection
chunky start
chunky progress
chunky pause
chunky continue
```

Increase radius after confirming completion/quality. Chunky's `radius` uses **blocks** not chunks; a 10k radius means 20k diameter. Use `chunky spawn` if spawn point is intentionally the center, and confirm selection. Check the server's `pause-when-empty-seconds=-1` if supported by its server version, so pregeneration does not pause with no connected players. Do not use `/tick freeze`. Store Chunky progress safely before shutdown. See https://github.com/pop4959/Chunky/wiki/Commands and https://github.com/pop4959/Chunky/wiki/FAQ .

## Implications for the broader performance patch

- **More important after pregeneration**: Embeddium + NeOculus rendering, culling, shader preset tuning (Complementary/Solas), particle overdraw from atmosphere mods, GPU VRAM use, entity/block-entity render/tick work, existing-chunk IO, GC and multiplayer simulation.
- **Still important before the long pregen job**: reliable fast worldgen, threading correctness, stalls/crashes/invalid structure NBT, measured Noisiumed/Structure Essentials or other supported optimizers. Any A/B worldgen change **must be decided before production pregeneration**.
- **Optional / late**: C2ME due custom-worldgen threading risk; Distant Horizons/Voxy only independently after engine compatibility and GPU/LOD evaluation; no simultaneous renderer stacking.
- **No removal of valued terrain/content** merely to reach a stated arbitrary chunks/sec.
- **No promised completion in one day**: 20k needs about 56.8 generated chunks/sec sustained for 24h, and total world/server backups can be large.

## Validation evidence

Record before/after ZIP hash, mod roster, worldgen config hash, chosen world seed *privately*, spawn center, radius/shape, dimension ID, chunky version, generated/existing chunk counts, chunks/sec distribution over time, disk used/available, heap/GC, server MSPT/TPS, restart status, plus shader-on/off client frametimes at warm explored locations. Treat previous historical Spark rolling metrics and Free TerraForged shutdown averages as context, not a production pregen benchmark.
