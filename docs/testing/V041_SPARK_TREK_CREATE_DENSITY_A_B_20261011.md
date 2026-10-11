# AO v0.4.1 — Four Spark profiles + Trek/Create density A/B (11 October 2026)

Status: source-static candidate, no Minecraft worldgen runtime acceptance. Baseline 329-ref Engineering IDAS pack remains unchanged; test on a fresh world in a separate instance.

## Verified Spark statistics

| User-shared profile | Last-1m mean MSPT | Median MSPT | Maximum tick |
|---|---:|---:|---:|
| [m2Eglp00fO](https://spark.lucko.me/m2Eglp00fO) | 27.62 | 25.94 | 765.30 |
| [ohcUJyadut](https://spark.lucko.me/ohcUJyadut) | 41.55 | 26.76 | 5994.88 |
| [Gj6d4N6Igg](https://spark.lucko.me/Gj6d4N6Igg) | 29.48 | 25.99 | 1330.00 |
| [lhhJO6dLBL](https://spark.lucko.me/lhhJO6dLBL) | 26.48 | 25.19 | 56.96 |

Metrics are Spark platform last-minute rolling values extracted in [CI 38138630135](https://github.com/alsynth/AmbientOdyssey/actions/runs/38138630135). They do not identify the expensive mod, client FPS, or whole-capture p95. User-provided latest.log recorded 10 server lag warnings, worst 6671 ms; second Spark profile's last-5m max was 6671.3 ms. Read sampled hot methods before optimizing unrelated systems.

## Latest game log signals

- No fatal crash; saved all dimensions normally. Java 21.
- 504 invalid-air item errors, 103 removed-zombie re-add warnings, 2 POI mismatch errors, 7 unresolved item-registry errors. Old off-thread entity warning and missing Luki pool/spawner signatures absent during this particular workload, not proved permanently fixed.
- ModernFix total game-and-world load ~225 seconds, menu-to-world ~128 seconds; not yet attributed.
- Xaero World Map initialized and cleaned normally. User reported previously viewed areas disappearing on the map; no chunk deletion proven. Before changing world files, compare cave/height layers and map-selection behavior and re-enter the physical area.
- Log showed one additional AO TO Magic Registry Fix JAR beyond the documented three AO experimental addon JARs. Compare actual installed mods with the reference baseline before performance A/B claims.

## Verified native mods and density scope

Native registry audit [38138907870](https://github.com/alsynth/AmbientOdyssey/actions/runs/38138907870) downloaded exactly pinned binaries: Trek B0.6.2, Create Structures Arise 176.49.49, Create Easy Structures 0.2a. Trek contains 21 native structure sets and 139 native structure registries; Create Arise 28 sets, Create Easy 16.

| Group | Before → test spacing | Expected potential grid density* |
|---|---|---|
| TREK Overworld common | 24 → 21 | ~1.31× (more) |
| TREK Overworld medium | 30 → 26 | ~1.33× (more) |
| TREK Overworld rare | 48 → 44 | ~1.19× (more) |
| Create Arise nonfarming, 25 native sets | native spacing × 1.30 | ~0.59× (less) |
| Create Easy nonfarming, 15 native sets | native spacing × 1.30 | ~0.59× (less) |
| Create Rustic smithy | 28 → 37 | ~0.57× (less) |
| Create Rustic well | 20 → 27 | ~0.55× (less) |

*Grid opportunity ratio is approximately squared inverse spacing, not the number of successful spawned structures. Biomes, collision restrictions and terrain eligibility still affect results.

Generator: `tools/generate_v041_trek_create_rarity.py` creates a separate private Paxi data pack containing 43 source-verified structure_set JSON overrides. Only spacing changes; no structure pools, salts, weights, templates, loot, biome filters, spawn behavior, farming windmills/barns/honey/chocolate pits or End/Nether Trek groups are modified. Existing `release_030/structure-density.json` is updated solely for the nonfarming Create Rustic smithy and well grids.

## Runtime acceptance

1. Compare old 329-ref Engineering IDAS test import with the new TREK/Create variant in separate CurseForge instances; no additions/removals of third-party mod pins.
2. Use the same world seed/preset and shaders OFF, 12 render / 6 simulation, Java 21; use **fresh ungenerated chunks** in each branch's own copied test save.
3. Count TREK common/medium/rare structures separately and Create decorative/camp/industrial structures separately; farming sites must remain discoverable.
4. Compare 3 matched terrain exploration passes including Spark worker threads, worst server stalls, p95 tick duration, average/1%-low FPS and visual correctness.
5. Reject changes that increase severe chunkgen stalls or degrade biome/structure integrity; do not modify a cherished existing survival world to benchmark generated-terrain density.

Build checks verify candidate ZIP overrides against pinned native JAR SHA256 and the manifest, but they cannot demonstrate actual TREK/CREATE rarity or TPS/FPS changes in Minecraft.
