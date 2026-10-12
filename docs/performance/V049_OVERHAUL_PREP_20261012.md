# Ambient Odyssey v049 performance overhaul preparation

Prepared 12 October 2026. **No FPS/TPS improvement claimed; no active modpack/profile changed.** Base is the latest fetched GitHub branch `content/v0484-r19-full-pack-20261012` at `92575dffe2ae7319c5f8abfc7fc0132dc0327719`, exact full import SHA256 `10fe2562ac0f584dbdc1372ff2542b2224a939cf67f5b7fd116934cec4511fd1`. r19, Q/E, trims, tooltips and Subtle Effects removal are the comparison baseline. Performance work is now authorized; outstanding gameplay checks continue alongside it.

## Deployment target

Logs verify **Ryzen 5 7600 / RTX 4070**. Owner specifies 32 GB system RAM, 2560×1440 / 144 Hz, 10–11 GB client heap and **Complementary Reimagined + Euphoria Patches**. Friends span somewhat weaker/stronger PCs, so prepare Performance / Balanced / Quality profiles. Server is a separate rented machine, reportedly 12 GB; actual CPU, disk and provider heap limits remain unknown. Keep 10 GB client heap for initial comparable runs, test 11 only with memory/GC evidence.

Owner intends 10,000+ block-radius pregeneration before launch. It removes first-generation work from early travel; saved chunk IO, network transfer, meshing, shader rendering and entity ticks still need benchmarking. Choose final worldgen before long production pregen. A 10k circle is roughly 1.23 million chunks: completion time and disk growth need a pilot, not a one-day promise.

## GitHub and artifact review

- Latest content is [PR39](https://github.com/alsynth/AmbientOdyssey/pull/39), built on [PR38](https://github.com/alsynth/AmbientOdyssey/pull/38), rather than old main or the v047 source. Do not blindly merge older performance/content branches.
- Recovered the previously tested log-summary/trial tools from [PR23](https://github.com/alsynth/AmbientOdyssey/pull/23). Existing results in older Spark captures describe different rosters/routes; do not label them a current r19 benchmark.
- Reviewed open [issues 1](https://github.com/alsynth/AmbientOdyssey/issues/1), [2](https://github.com/alsynth/AmbientOdyssey/issues/2), [3](https://github.com/alsynth/AmbientOdyssey/issues/3), [4](https://github.com/alsynth/AmbientOdyssey/issues/4): historical structure, spawn-category and terrain acceptance still need current-world observations; several exact patches have since shipped. Do not reinstall removed mods or reapply old fixes solely because issues remain open. Dungeon Crawl spawners remain a current manual gate; Malkuth/Mine Cells already owner-accepted.
- Earlier `performance/v047-pregeneration-first-plan-20261012` confirms staged pilot/5k/10k/optional20k strategy. Latest r19 smoke log generated only 157 flat-world chunks at low render distance: **not a survival/pregen benchmark**.
- Installed: Embeddium 1.0.15, NeoOculus 1.8.7, Lithium 0.15.4, FerriteCore 7.0.3, ModernFix 5.27.24, ImmediatelyFast 1.6.14, AllTheLeaks 1.1.13 and SmoothChunk 4.1. Already enabled core rendering/culling optimizations; default render/simulation 12/6 and cap160. Installing another generic optimizer is not itself evidence of a gain.
- Current CF roster pins Complementary Reimagined r5.9.3 (`627557:8884654`). Euphoria Patcher is not installed in the audited baseline. Outer-JAR native/Fabric dependency declarations and renderer mixin hints are captured in [the audit](v049-prep/MOD_DEPENDENCY_AUDIT.json); hints are not proof of runtime compatibility, and nested providers/code paths still need checking before dependency removal.

## First changes to implement and compare

| Priority | Concrete change / trial | Measurement and acceptance |
|---|---|---|
| 1 | Add the exact **Euphoria Patcher 1.10.5 / Complementary r5.9.3** pair in an isolated current-renderer candidate. Compare shaders off, Reimagined Medium, Euphoria Medium and Euphoria High. Produce weaker-PC Performance plus Balanced/Quality presets. | 1440p same route, weather/time and 12/6 settings; average FPS, 1% lows, frametimes/VRAM. Check forests, water, caves, mobs, Create and UI. No assumed shader gain. |
| 2 | Streams **client-only** particle trial: bubbles 2→1, debris true→false, density 1→0.5, cap1000→250, scan radius256→64. Actual supported options copied from installed 2.14.4 config. [Candidate](v049-prep/STREAMS_BALANCED_CANDIDATE.toml). | Same river/waterfall scene, Euphoria preset unchanged. Check visuals and frametimes. Terrain planning, biome whitelist, waterways and audio unchanged. |
| 3 | Test **EntityCulling 1.11.3 NeoForge 1.21.1**, separately from particle changes. Existing Embeddium culling remains the comparison baseline. | Populated base/caves/structures. Verify boss/magic/projectile/block-entity visibility; use supported exclusions if needed. Tick-culling features start off until assessed. |
| 4 | Dependency-audit removal trial for already-disabled **Equipment Compare and Legendary Tooltips**. Preserve SimplyTooltips, Q/E and affix details. Prism/Iceberg removed only if a complete dependency audit proves exclusivity. | Startup and GUI/hover regressions, then frame measurements; likely cleanup, no large FPS claim. Do not stack this removal into another trial. |
| 5 | Review particle producers AAA/Particular/Shadow Drop, shader shadows/reflections/volumetrics and any actual dynamic-light owner. Keep one-variable trials; tune supported options only. | GPU frame time, entity-rich and rainy scenes. Preserve valued atmosphere unless measured tradeoff is worthwhile. |
| 6 | Existing-chunk server tests with 2 then 5–7 players. Tune view/simulation, FTB forced chunks and entity/block tick hotspots from fresh Spark evidence. Initial test distances 10/6; final values measured. | 20 TPS / p95 MSPT under50ms as a target, no severe pauses. Keep normal chunk tickets, portals, claims and farms working. |
| 7 | Pregeneration pilot after worldgen choice: disposable final-preset 2k–5k, record throughput/disk/GC/error rate/restart, then production 5k→10k→optional20k. | Actual Chunky completion/resume, backups and terrain/structure quality. World border and circular coverage tested separately. |

### Renderer migration: real compatibility gate

A Sodium/Iris swap is a separate experiment, **currently blocked by the inspected release metadata**. Never install Sodium alongside Embeddium, or Iris alongside NeoOculus.

- Current Supplementaries 3.9.9 declares Sodium `<0.8.12-beta.1` incompatible; Create 6.0.10 expects Sodium≥0.6.9 when present.
- Official stable Iris 1.8.12 metadata points to **Sodium 0.6.13**; that pair conflicts with current Supplementaries.
- Official Sodium 0.8.13 exists for NeoForge1.21.1. The inspected Iris 1.8.14-beta.1 artifact advertised for that target instead declares Minecraft `[1.21,1.21.1)`, which excludes the target, and marks Embeddium incompatible. Do not patch its JAR or suppress version checks. Obtain a corrected compatible official build, or assess an upstream-supported alternative, before trial.
- Renderer-sensitive modules include Create/Flywheel, Supplementaries, BorderlessWindow, Dense Flowers, FDBosses, Polytone, Swinging Lanterns, ImmediatelyFast, Streams and particle mods. Full smoke/scene checks required; API listing alone is insufficient.
- [Exact version/source metadata](v049-prep/CANDIDATE_VERSIONS.json). Candidate versions are not yet CurseForge-pack pins. Official projects: [Sodium](https://github.com/CaffeineMC/sodium), [Iris](https://github.com/IrisShaders/Iris), [EntityCulling](https://github.com/tr7zw/EntityCulling), [Chunky](https://github.com/pop4959/Chunky/wiki/Pregeneration). Euphoria author confirms matching [r5.9.3 + 1.10.5 installation](https://www.euphoriapatches.com/how-to-install/) and [loader support](https://www.euphoriapatches.com/faq/); exact NeoOculus pairing still needs our runtime test.

## Measurement and rollback

[39 planned rows](v049-prep/BENCHMARKS.csv) contain **no measured values**. Start with baseline and shader/Streams trials, not all rows at once. Three 120-second repetitions after warmup per condition. Keep hardware, 1440p, Java21, heap, cap160, saves/route, time/weather and resource packs fixed. Record exact import/config hashes and shader profile. Separate shader-off CPU recordings from GPU frame evidence; whole-window Spark sampling and slow-tick-only samples are not interchangeable. Use a representative full FreeTerraForged survival world, not the flat startup probe. Copy an ungenerated save before cold-route trials; a repeated generated route cannot serve as a cold baseline.

Client: `/sparkc profiler start --thread * --timeout 120`. Server: `/spark profiler start --thread * --timeout 120` (confirm installed command help). Record client FPS/1% lows and frame times separately; Spark cannot establish shader GPU FPS. `tools/perf_v041_trials.py` aggregates actual measurements but does not infer cross-variant causality. `tools/perf_v041_log_report.py` summarizes logs without mislabeling lag warnings as p95 MSPT. Extra CSV controls, including config hash and shader options, must be reviewed explicitly.

Retain the r19 import and untouched saves. Each experimental ZIP/config set has a hash and exact diff, and must pass native startup/world/save, Q/E and tooltip checks; renderer/culling variants additionally test enchanted gear, boss attacks, magic, Create animation, water and shader shadows. Proposed acceptance: a repeatable ≥10–15% gain in the targeted FPS-low/frametime metric, or a material stall/MSPT reduction, with no relevant regression. This threshold is a decision rule, not a predicted result. Remove major content only after a current profile identifies the cost and the owner sees the tradeoff. No C2ME, Noisiumed, LOD stack or JVM-flag bundle added blindly.

## Prepared outputs

`build/Ambient-Odyssey-v049-PERFORMANCE-PREP-KIT.zip` contains the runbook, baseline/dependency/version audit, candidate presets, blank benchmark CSV and restored measurement tools. **Not a full pack import or auto-installer.** Active pack/source configs and live profiles are untouched. Static preparation checks and recovered measurement-tool tests are the only new validation in this task; no new in-game performance gain is certified.

Validation: 13 recovered performance-tool regression tests PASS; exact 329-pin archive preflight PASS; 39 planned benchmark rows correctly produce zero measured results. Candidate TOML parses and known option values are checked by the deterministic prep-kit builder.
