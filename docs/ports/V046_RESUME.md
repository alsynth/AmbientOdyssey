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

## 12 October archaeology/recipes checkpoint

Compilation and **all 12 required mechanics GameTests PASS**, both alone and
with the exact installed FreeTerraForged 1.0.0, Biolith 3.0.14 and TerraBlender
4.1.0.8 JARs copied into a disposable workspace. Evidence:
`docs/testing/v046-evidence/wet-sand-twelve-terrain-gametests.log`.
The terrain mods loaded and their compatibility mixins initialized. The test
world is flat: **natural FTF terrain/shoreline generation is not tested**.
Development JAR SHA-256:
`d55e279e07d397ec75108daccf2205633b3f2af0eb2a04a90c86256d82246611`.

Three suspicious-sand stages now preserve saved item/loot-table/seed across
moisture changes and NBT reload; active brushing prevents replacement.
Completed brushing leaves the corresponding ordinary sand and drops one
treasure in the tested case. Vanilla brushable entity registration uses the
NeoForge `BlockEntityTypeAddBlocksEvent` extension. Full process restart and
client brush rendering remain unverified.

Added all sixteen hydrated-sand concrete recipes, verified by actual recipe
matching/assembly, and exact single-item loot from all six ordinary variants.
Matched upstream plant policy: wet/soaked stages support cane without adjacent
water; moist ordinary sand uses vanilla water requirements.

The installed v0.4.5 preview was found read-only in the standard CurseForge
Instances folder: 327 top-level JARs, 324 recognized top-level metadata,
no duplicate top-level mod IDs. Embedded/bridge dependencies still require
their own resolution. Neither its JARs nor its saves/configs were modified.
User-provided Actions run `38177729206` is the earlier **v046 prototype**
preflight at `60f3760`, not a v045 full-pack export.

## Remaining Wet Sand gates before Apotheotic feature implementation

- Suspicious-sand: complete actual process restart, client rendering, bottle
  interactions during brushing and real structure treasure testing.
- Compare upstream hydration/propagation policy and document intentional
  AO deviations: current prototype uses same-height source-water Manhattan
  radius 3 and dry regression; upstream uses other neighborhood semantics.
- Shoreline conversion currently samples near players, rather than all
  natural shorelines. Decide and test the terrain-safe placement policy.
- Verify creative and inventory-full bottle paths, client hand prediction,
  protection integration, red falling physics and codec round trips.
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
