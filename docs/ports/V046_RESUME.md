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

## 12 October hydration/art checkpoint (latest)

Native compilation and **all 14 required GameTests PASS**, alone and with
the three terrain mods. Hydration now uses loaded-only 3D Chebyshev radius 3,
source or flowing water, and adjacent wetter sand propagation, capped by
water distance. Missing water no longer automatically dries the block:
glass-bottle extraction decreases humidity, matching upstream behavior.
Tests cover vertical flowing water, propagation and distance ceiling.
Each sampled dry-sand candidate visits at most 343 loaded positions plus
six neighbors. No worldgen replacement or chunk-load request is installed.

Original upstream textures are now included byte-for-byte, with checked-in
hash provenance, attribution and **GPL-3.0-only** module/artifact licensing.
This supersedes the original MIT/no-upstream-assets prototype policy for
this module only. License and notice are bundled in the JAR. The packaged
resource checker passed: 9 blockstates, 27 models, 19 verified textures,
all item/loot resources present, no vanilla worldgen replacement.

Final development JAR SHA-256:
`47444f1e1b30271fef0cb43652a43bd15f870bdc7d2d4a47864dafc3e8df7c47`.
Evidence: `docs/testing/v046-evidence/wet-sand-fourteen-terrain-gametests.log`.
Run packaged validation with:

```text
python tools/validate_v046_wetsand_resources.py ports/wet-sand-neoforge/build/libs/ao-wet-sand-prototype-0.0.1-source-prototype.jar
```

## 12 October persistence/client checkpoint (latest)

Compilation and **18 required mechanics tests PASS**. Added full-inventory
water-bottle drops, cancelled protection events, bottle rejection during
active brushing and red-sand falling identity. Bottle handling now runs at
LOWEST event priority and ignores already-cancelled events, allowing earlier
protection listeners to veto it. This tests the native event contract, not
every third-party claim mod.

**Actual two-process save/restart PASS**: writer JVM saves soaked suspicious
sand with vanilla desert-well loot table and seed, plus wet red sand; reader
JVM loads the same generated world, validates the stored values, extracts
water, resolves real archaeology loot, then brushes it out exactly once.
Each explicit phase runs 19 tests (18 ordinary + persistence fixture).
Evidence: `wet-sand-persistence-write.log` and
`wet-sand-persistence-read.log` under `docs/testing/v046-evidence/`.

**Actual isolated native client startup/model bake PASS**: Java 21 / NeoForge
21.1.252 / LWJGL / OpenGL 4.6 reached the title screen; 6 ordinary and 12
dusted archaeology block models resolve their exact texture atlas sprites.
The opt-in smoke hook closes only its disposable development client. It
skips first-launch onboarding in that test instance and does not alter a
real CurseForge profile. Evidence: `wet-sand-native-client-smoke.log`.
This checks actual client resource loading; it does not test in-world brush
animation, player movement, full-pack shaders or multiplayer interactions.

All three checks are required in the updated port CI workflow, with logs
preserved on failure. Re-run the separate save phases with:

```text
gradle -p ports/wet-sand-neoforge --no-daemon -PaoPersistencePhase=write runGameTestServer
gradle -p ports/wet-sand-neoforge --no-daemon -PaoPersistencePhase=read runGameTestServer
gradle -p ports/wet-sand-neoforge --no-daemon runClientSmoke
```

Development JAR SHA-256:
`8c0e0a6b86b7f9999236cfc9b08483bfada9e2328d1f696c96685bdcea87a722`.
Packaged resource/license validation PASS. The client and persistence test
hooks are dormant in an ordinary installation.

## 12 October production-launch integration checkpoint

**Production client startup/model check PASS** with all 327 top-level JARs
copied from the installed v0.4.5 preview, plus the Wet Sand development JAR
`8c0e0a6b86b7f9999236cfc9b08483bfada9e2328d1f696c96685bdcea87a722`.
Repository `release_030/overrides/config` was copied into that disposable
instance. Original profile, configs and saves were not edited. This was a
menu/model check, not a world join or multiplayer gameplay test. Evidence:
`docs/testing/v046-evidence/wet-sand-production-full-roster-client.log`.

The ModDevGradle full-roster launch failed before the test hook: Connector
could not find the clean Minecraft artifact, and a Formations **development**
mixin referenced an absent helper. Using the installed **production** NeoForge
21.1.252 launcher metadata/libraries resolved those failures. Do not treat
the failed development launch as a proven regression of the working profile.

`tools/run_v046_production_client_smoke.py` reproduces this Windows production
launch against a caller-prepared snapshot under the Wet Sand build directory.
It uses an offline test identity, does not read account tokens, validates the
production loader metadata and library paths, requires an explicit PASS log
marker, and controls/terminates only its own child process on timeout. Supply
`--install`, `--game-dir` and `--mod-jar`; optional `--java`, `--heap`, `--timeout`.
The client hook now has a timeout and a configurable heap for larger snapshots.
This does not export a CurseForge ZIP or install either port in the real pack.

## Remaining Wet Sand integration gates

- Suspicious-sand: in-world brush rendering and actual generated structure
  treasure testing. Native bottle rejection and real desert-well loot after
  process restart are now verified.
- Benchmark the loaded-only propagation budget and confirm wet shorelines
  during natural FTF generation; no full-world conversion is implemented.
- Shoreline conversion currently samples near players, rather than all
  natural shorelines. Decide and test the terrain-safe placement policy.
- Verify live client hand prediction, specific full-pack protection mods
  and codec round trips. Full-inventory drops and red falling physics pass.
- Verify upstream textures, lowered soaked collision and brush animations
  on the actual client; packaged resource validation does not render them.
- Full-pack **world join/gameplay**, FTF shoreline generation and two-player
  dedicated-server persistence/performance tests remain required. Full-roster
  native client startup/model resolution now passes under the production launcher.

## 12 October Apotheotic rarity subsystem checkpoint (latest)

After native Wet Sand mechanics, process persistence and full-roster production
client startup passed, verified the first Apotheotic subsystem against the
exact installed library versions: Apotheosis 8.9.0, Placebo 9.9.2,
Apothic Attributes 2.11.0, and Patchouli 1.21.1-93-NEOFORGE. Maven downloads
of the first three match the installed JAR SHA-256 hashes byte-for-byte.
No third-party dependency JARs are embedded in the development port artifact.

**Compilation + four native GameTests PASS**:

- All Artifact, Heirloom and Esoteric definitions load through Apotheosis's
  actual rarity registry (8 total rarities = 5 built-in + 3 additions).
  Material reverse lookup, ordering and original rule counts 8/4/16 pass.
- All three materials are in the non-replacing rarity-materials ingredient
  tag and exposed in the ingredients creative tab. Added names and temporary
  vanilla-texture item models; original Additions art is not included.
- Natural weights remain zero, including high luck and all five world tiers.
  500 actual native rarity rolls continue to produce only stock rarities.
  Artifact/Heirloom stay disabled pending affix/gem/loot completion; Esoteric
  retains its intentionally unobtainable natural-drop policy.
- All three rarity item components survive native item/NBT serialization.
- A real server data reload rebinds all three definitions and their material
  maps; rarity components remain usable afterward.

Evidence: `docs/testing/v046-evidence/apotheotic-four-rarity-gametests.log`.
Development artifact SHA-256:
`e288619744c4e8f8f6a524cb3a6d7e79b0cefe78ae6f0b5b9b49c4935a2dfe3e`.
CI now runs these native integration tests after the Wet Sand checks.
Including the installed Patchouli version also closes the stock Apotheosis
Chronicle recipe parse error seen in the initially narrower test context.

This validates the rarity foundation; it is **not a functioning complete
Apotheotic Additions port**. No legacy Additions affixes, gems, bosses, loot
tables, trades or other major systems have been installed by this checkpoint.

## Apotheotic continuation

Start with the source inventory and schema reports in `ports/apotheotic-additions`
and `docs/ports/APOTHEOTIC_ADDITIONS_1211_PORT_AUDIT_2026-10-11.md`.
The three rarity JSONs and material registrations now pass native codec,
registry, component and reload checks, with drop weights zero. They are not
verified affix generation or loot/reforging integration. Port attribute affixes
first, preserving stepped roll semantics and all three custom-rarity keys;
then gems, ability affixes, bosses/gear/loot, recipes/reforging and other major
systems with subsystem checks before enabling real drops. Esoteric must remain
retained with its intended obtainability.
Do not discard cross-mod boss/gem/affix systems silently when dependencies
are unavailable; record compatibility requirements and test each batch.
