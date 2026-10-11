# v0.4.6 port continuation contract

User requirements accepted on 11 October 2026. Work on
`experimental/v046-wetsand-apotheotic-ports-20261011` only. Preserve
`experimental/v045-custom-integrations-20261011`, its working packages, and
`main`. Do not install these prototypes into `release_030`.

## Required order and acceptance

1. Finish Wet Sand first and verify native NeoForge mechanics.
2. Port Apotheotic Additions subsystem by subsystem. Retain Artifact,
   Heirloom **and Esoteric**, gems, affixes, bosses, crafting/reforging,
   loot and other major upstream systems. Inventory omissions explicitly.
3. Compile and run automated checks after each subsystem. Record failures
   as failures; successful compilation does not prove in-game compatibility.
4. Verify native client, dedicated server, data reload, save/restart,
   two-player interactions and compatibility with AO's terrain and mod roster.
5. Produce a complete CurseForge test build only after relevant port checks
   pass. Keep intermediate JARs clearly marked as development artifacts.
6. Push small, reviewable progress commits with test evidence and this resume
   document updated, so exhausted credits cannot strand the work locally.

## Current checkpoint

Base: `60f3760`. Existing prototypes are incomplete. No full port or
combined v0.4.6 CurseForge build is certified.

Wet Sand ordinary-block work now includes loaded-chunk-only moisture scans,
native sugar-cane support, six self-drop loot tables, shovel/sand tags,
translations, wet/soaked block codecs, lowered soaked collision and spectator/
spawn-protection/adventure restrictions for bottle extraction. No upstream
textures or source files copied. Upstream behavior reference inspected at
`HearthianDev/wet-sand` commit `0e0707813ce811884a51a2614418b4a841d38699`.

Seven NeoForge GameTests exercise normal/red moisture transitions, range,
sugar cane, collision, actual falling physics, survival offhand bottle
consumption and spectator rejection. Run:

**Local result: compilation PASS, all seven required GameTests PASS** on
Java 21.0.12.1 / NeoForge 21.1.252. Evidence:
`docs/testing/v046-evidence/wet-sand-seven-gametests.log`.
Local invocation used `CI=true` (ModDevGradle's documented binary-patch mode)
after the default Minecraft recompilation failed with an output-write error.
Shortening the Gradle cache path did not resolve that error; its cause remains
unconfirmed. This did not require altering Minecraft or the mod's API target.

```text
gradle -p ports/wet-sand-neoforge --no-daemon build runGameTestServer
```

The native-materials CI job now waits for Wet Sand compilation/mechanics.
CI always preserves available mechanics logs. This isolated test server
does not certify the full AO client or multiplayer integration.

## Remaining Wet Sand gates before Apotheotic feature implementation

- Suspicious-sand moisture variants: preserve brush progress, treasure/loot
  table, seed and save/restart across every transition; never overwrite
  archaeology with ordinary sand. Currently suspicious sand is untouched.
- Compare upstream hydration/propagation policy and document intentional
  AO deviations: current prototype uses same-height source-water Manhattan
  radius 3 and dry regression; upstream uses other neighborhood semantics.
- Shoreline conversion currently samples near players, rather than all
  natural shorelines. Decide and test the terrain-safe placement policy.
- Verify creative and inventory-full bottle paths, client hand prediction,
  protection integration, recipes, red falling physics and codec round trips.
- Distinct art is still missing: models currently reuse vanilla textures.
- Full pack client, FTF shoreline generation and two-player dedicated server
  persistence/performance tests remain required.

## Apotheotic continuation after Wet Sand

Start with the source inventory and schema reports in `ports/apotheotic-additions`
and `docs/ports/APOTHEOTIC_ADDITIONS_1211_PORT_AUDIT_2026-10-11.md`.
The three rarity JSONs and material registrations are development scaffolding,
with drop weights zero. They are not verified loot integration. Implement and
test exact Apotheosis 8.9.0 codecs and real drop/reforging semantics before
enabling them. Esoteric must remain retained with its intended obtainability.
Do not discard cross-mod boss/gem/affix systems silently when dependencies
are unavailable; record compatibility requirements and test each batch.
