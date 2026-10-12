# v0.4.9 visual and ecology follow-up — 13 October 2026

Experimental follow-up to PR #41 commit `19f399f5c1bb8657ced90e6623439c1f37aef974`. No new native runtime measurements. Preserves r19, all 328 consolidated pins, Euphoria presets, renderer, Streams/audio settings, culling with tick culling OFF, quests, boss stats, loot, structures and Tan's Huge Trees. Do not merge to a release before scene and multiplayer checks.

## Applied changes and expected effects

| Supported config | Before | Candidate | Reason / limitation |
|---|---:|---:|---|
| Particular falling-leaf spawnChance | 60 | 90 | Larger inverse chance means fewer leaf particles; leaves, ripples, colors and fireflies retained. Nominal attempts about two-thirds at equal eligible block activity, not an FPS prediction. |
| Particular cave-dust spawnChance | 700 | 1000 | Lower dust emission; preserves the effect. Cave Dust Rethinking also supplies dust, but actual overlap needs cave QA. |
| Particular cave-dust baseMaxAge | 200 | 160 | Shorter base lifetime reduces concurrent particles and update work. Fade stays 20. Actual lifetime/population is implementation dependent. |
| Alex's Mobs blobfish weight | 30 | 20 | Shares species with Naturalist/Hybrid Aquatic; retains Alex's gameplay and all registries. |
| Alex's Mobs elephant / tiger weights | 30 / 30 | 20 / 20 | Reduce pressure from duplicate large fauna; keep distinctive creatures and biomes. |
| Alex's Mobs rhinoceros weight | 24 | 16 | Same conservative reduction for overlapping large fauna. |

Weights are relative selection weights, not density caps or guarantees of one-third fewer mobs. No existing entities are deleted. Changes affect future spawning; old-world populations and other providers may mask the effect. These species were selected from the source-verified wildlife audit, not attributed as measured tick hotspots. Other mobs, including predators/bosses, retain their settings. Existing gorilla/fly/cockroach exclusions remain.

## Current stack and configuration audit

Exact inherited installed-JAR metadata is in `v049-followup/MOD_AUDIT.json`: Embeddium 1.0.15, NeoOculus 1.8.7, Lithium 0.15.4, FerriteCore 7.0.3, ModernFix 5.27.24, ImmediatelyFast 1.6.14, AllTheLeaks 1.1.13, SmoothChunk 4.1. PR41 adds EntityCulling 448233:9100286 and Euphoria 1.10.5 (915902:8884680), matching Complementary Reimagined r5.9.3. Source-lock and consolidated import differ historically; use consolidated import pins as release truth.

Lithium config has no manual overrides. ModernFix remains GA/default; FerriteCore and ImmediatelyFast remain as inherited. No unsupported mixin overrides, new optimization mods or renderer migration. EntityCulling tracing128, safeMode true, tickCulling false; this targets rendering, not client entity tick listeners. Streams retains bubbles1/debrisfalse/density0.5/per-tick cap250/scan64. This is a spawn-per-tick cap, not a maximum live-particle cap.

AAA Particles 2.3.3 is an Archaion dependency; keep it. Particular Reforged 1.5.7, Cave Dust Rethinking 3.3.0 and Polytone 5.0.3 are present in inherited metadata. Better Smoke has no independently identified JAR in that audit: inspect current instance/resource packs before assuming another configurable producer. No committed supported config found for Cave Dust Rethinking or a dynamic-light owner; do not invent option names. Particular and Streams both cover waterfall effects; retain both until same-waterfall visual trials demonstrate duplication. Do not disable Polytone, foliage assets, smoke, combat particles or resource packs without finding their actual effect owner.

Naturalist 2.0.5, Alex's Mobs 1.22.9, Hybrid Aquatic 1.7.4 and Ben's Sharks 1.2.6 remain. Cosy Critters 0.3.3 is visual ambience, not server wildlife AI. Naturalist custom `add_animals` needs exact per-species spawn-rule extraction before broader cleanup; do not replace the entire modifier. Further rat/ant/isopod and ocean overlap cleanup is pending, not completed by this patch.

AO Performance/Balanced/Quality are inherited unchanged. Balanced shadow quality2/distance128, water reflection2, lightshaft1, SSAO2. Quality is the inherited higher preset, not a guarantee every shader option is maximized. Preserve Balanced until separate shadow-distance/entity-shadow/volumetric trials identify a low-impact improvement. Optional Euphoria mixin warning remains untouched; dimension QA stays open.

## Server review and profiling

No server performance tweak justified yet: healthy integrated TPS does not certify dedicated exploration. Retain Lithium/FerriteCore/ModernFix/AllTheLeaks and existing chunk settings. Obtain dedicated CPU, heap limit and storage details before changing worker counts or view/simulation distances. Keep approximately 12 GB server RAM and 10 GB client heap as supplied comparison conditions; do not allocate all system/provider RAM blindly.

User-reported pregen: 16,129 chunks in 15m19s, around17.6 chunks/s, TPS near20 with some >50ms ticks. This is context, not a new result or multiplayer acceptance. Tan's Huge Trees 1.8.0 BETA shutdown executor fix belongs to Claude; no changes here. Integration gate: obtain reviewed fix commit/JAR hash, test start/pregen/stop/restart on disposable copy; do not send messages to other chats without authorization.

Client `EntityTickPre` is dispatcher time in the call tree; identify self time and listener callers with shader-off `/sparkc profiler start --thread * --timeout 120` before blaming any mod. Server AI/pathfinding requires server profiling separately. Do not enable tick culling based on dispatcher samples.

## Benchmark results and acceptance

New candidate: NOT RUNTIME TESTED; no FPS/MSPT/memory improvement measured. Historical PR41 native report has 18 short sequential synthetic trials and GUI checks, not representative survival A/B. Some recorded frame counts imply less than the claimed 30 seconds of actual captured frame time; capture raw frame timestamps and valid duration in next trials. Do not reuse historical medians as evidence for this candidate.

For each open-terrain, dense-forest/wildlife and structure/combat scene, compare PR41 baseline, particle-only, wildlife-only and combined candidates. Use copied saves: natural-spawn tests need time and population counts, not immediate reload comparisons. Keep camera,1440p, cap, render12/simulation6, heap, shader, weather/time and resource packs fixed; warm120s and measure120s, at least3 runs, alternate A/B order. Record import/config SHA, Java/version/hardware, average FPS, 1% lows (define method), p95/p99 frame times, stalls, memory/GC, particle/entity counts, Spark samples and GPU frame timing when available. Existing benchmark CSV/tools remain useful; blank rows are not results.

Client checklist: startup/world/save/reload; leaves in several biomes and night fireflies; deep/large caves and Cave Dust overlap; waterfalls/rain audio and water readability; shaded/occluded and visible mobs; shadows/magic/boss attacks/Create; modded dimensions; Q/E and tooltip scroll scales2/3/4. Record visual differences as well as timing.

Server checklist: same seed/config and disposable saves; idle, equivalent cold pregeneration, warm and cold exploration with5–7 players; TPS, MSPT median/p95/p99, >50ms count, process CPU/RAM/GC, disk IO, chunk throughput, per-species population and errors; reconnect/save/restart and reviewed Tan fix shutdown. Multi-player cold tests must cover players travelling separately. Reject missing wildlife, invisible mobs, shader errors, audio regression or worse frame stability. Promote only repeatable useful gains with acceptable visuals.

## Delivery and rollback

`tools/package_v049_visual_ecology.py --output <kit.zip>` builds candidate/rollback configs plus this report; it is NOT a full CurseForge import. Copy candidate configs only into a cloned PR41 profile; use rollback files to reverse. Put matching Alex's server config on a disposable server after checking its current file; restart both sides. Particular common config may be loaded server-side: verify observed side behavior, not filename assumptions.

With `--base <exact PR41 import.zip>` the builder requires SHA256 `4dac3f2f2991fb4b92638b97b80d7c0aa4dbf90631aa721c25707937944de6d0`, exact old config bytes and 328 pins, preserving every other existing entry except manifest identity. Original configs are included under AO_TEST_NOTES/v049-rollback. Full experimental build has not been generated here: exact PR41 ZIP and runtime are unavailable. Static config kit can be reviewed now; no CurseForge upload or release promotion.

Evidence: repository configs/comments, inherited `v049-prep/MOD_DEPENDENCY_AUDIT.json`, `BASELINE.json`, `V049_IMPLEMENTATION_20261012.md`, `v049-native-validation/RESULTS.json` and `docs/audits/CONTENT_040C_ALL_WILDLIFE_AND_FRIENDLY_MOB_CATALOG_2026-10-10.md`. Upstream effect inventory: https://modrinth.com/mod/particular-reforged. Existing per-option config comments, rather than a different upstream version, define this patch.

Static validation this session: both TOML configs parse, exact seven-option delta with original byte backups, JSON parse, five-file kit CRC, nine inherited measurement-tool tests, Questlog/FTB/FG validators PASS. No full-import preflight or native Minecraft tests executed.
