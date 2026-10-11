# Ambient Odyssey v0.4.6 — Claude handoff

Prepared 12 October 2026. This is a continuation of an incomplete native
Minecraft mod port, not a finished release. The user requested this handoff
because only 23% of the current Codex five-hour allowance remains. That
percentage cannot predict task capacity; the remaining implementation and
gameplay verification are too extensive to promise completion within it.

## Start here

Repository: https://github.com/alsynth/AmbientOdyssey

Working branch: `experimental/v046-wetsand-apotheotic-ports-20261011`

Last code/evidence checkpoint before this handoff:
`9307493940279dff48fd81d316030aa2781b27e3`

https://github.com/alsynth/AmbientOdyssey/commit/9307493940279dff48fd81d316030aa2781b27e3

Original porting base: `60f3760f97832a1e7c896cf92e313023ad87bf62`.
Fetch the branch and inspect its latest head; later handoff-only commits may
follow the code checkpoint. Check for local changes before switching branches.
Do not reset, clean or force-push a user's checkout.

Read `AGENTS.md`, `docs/status/CURRENT_STATE.md`,
`docs/status/AGENT_WORKFLOW.md`, `docs/maintainers/REPO_MAP.md`, `TODO.md`, then
`docs/ports/V046_RESUME.md`. The latter is chronological: later checkpoints
supersede earlier statements such as “no upstream art” or “no affixes installed.”
This handoff summarizes the latest verified state, without erasing history.

## User's requirements — retain all of them

1. Finish Wet Sand first and verify its NeoForge mechanics. Its standalone
   mechanics milestone is tested; remaining full-pack gameplay checks still
   prevent calling the whole Wet Sand port finished.
2. Port Apotheotic Additions feature by feature, retaining Artifact, Heirloom
   **and Esoteric**, gems, affixes, bosses and other major upstream systems.
3. Compile and run automated tests after each subsystem. Preserve evidence.
4. Never confuse compilation, a successful process exit, a title screen or
   static validation with full in-game compatibility.
5. Preserve the working v0.4.5 release. Keep experimental ports isolated.
6. Produce a complete CurseForge test build only after relevant port checks
   pass. Intermediate prototype JARs are not that build.
7. Keep GitHub tightly updated: small subsystem commits, evidence, inventories
   and continuation notes. Do not leave substantial work only on the local disk.

Protected: `main`, `experimental/v045-custom-integrations-20261011`, existing
working v0.4.5 packages and player profiles/saves. Do not inject prototypes into
`release_030` or the live CurseForge profile. Old active-candidate branch pointers
in general docs are not instructions to abandon this v0.4.6 branch.

## Verified state

| Area | Actual evidence | What it does not establish |
|---|---|---|
| Wet Sand | 18 native mechanics tests; packaged resource checks | Natural terrain generation or complete full-pack gameplay |
| Wet Sand persistence | Two separate server JVMs; 19 tests per write/read phase; real archaeology loot saved and brushed once | Two real players on a dedicated server |
| Client | Production launcher, all 327 copied original mod JARs plus both prototypes; title screen and 18 Wet Sand baked models/sprites; clean exit | World join, gem use, brush animation or gameplay compatibility |
| Apotheotic rarity foundation | Artifact/Heirloom/Esoteric registry, materials, ordering, rule counts, serialization, zero-weight native rolls and resource reload | Complete drops, reforging or loot integration |
| Apotheotic attributes | 25 converted affixes; original stepped ranges; stock-rarity exclusion; actual equipped Artifact damage and serialization | Remaining affixes or complete affix generation |
| Apotheotic gems | Five converted gems; original supported nine-tier values; item/network round trips; native socketing; unique restriction across different tiers; real Esoteric +5 health | Upper-tier upgrading, complete recipes, extraction, art or all socket paths |

Apotheotic has **nine required native GameTests**, not nine plus the earlier
four/seven. Registry totals: 8 rarities, 124 affixes (99 stock + 25 ported),
25 gems (20 stock + 5 ported). All custom rarity and ported gem natural weights
remain zero. Do not enable drops simply because this batch passes.

The five gems are `crafted/cornelia`, `crafted/monstrosity`, `crafted/warden`,
`modded/armor` and `modded/hearty`.

Complete inventories record **118 source attribute affixes**, of which 25 are
ported and 93 pending; another **146 non-attribute affixes** remain pending.
There are **71 actual source gem JSONs**, of which 5 are ported and 66 pending.
Some older audits counted roughly 82 gem paths, including directories; use 71
for the JSON inventory. Remaining systems also include bosses, gear, loot,
crafting/reforging, trades, dependencies and other upstream behavior.

## Important implementation facts and hazards

### Wet Sand

Module: `ports/wet-sand-neoforge`.

Six ordinary moisture blocks (normal/red), three suspicious stages; moist sand
falls, wet/soaked are stable, soaked collision is 14/16. Wet/soaked support cane;
moist uses vanilla nearby-water requirements. Hydration uses loaded-only 3D
Chebyshev radius 3, flowing/source water and adjacent wetter sand propagation.
No automatic drying: glass-bottle extraction lowers moisture, matching upstream.
Dry shoreline conversion samples eight positions per Overworld player/second
near feet, not all generated shorelines. Each scan is bounded; it does not force
chunk loads or replace vanilla worldgen.

Bottle handling runs at LOWEST priority and respects cancelled events and
spectator/adventure/protection restrictions. Suspicious transitions preserve
block-entity item/components/table/seed; DUSTED > 0 blocks conversion during
active brushing. Native brushable registration uses
`BlockEntityTypeAddBlocksEvent`. Six ordinary loot tables and 16 concrete recipes
are included. Original upstream textures have recorded hashes and GPL notices.

Open checks: full-pack world join and play; natural FreeTerraForged shorelines
and bounded-conversion performance; live client hand prediction and actual brush
rendering; two-player dedicated-server persistence/interactions; actual protection
mods; remaining codec round trips. The terrain-mod test world was flat.

### Apotheotic Additions

Module: `ports/apotheotic-additions/neoforge`.
Converters: `tools/port_v046_core_attribute_affixes.py` and
`tools/port_v046_core_attribute_gems.py`. Both require pinned upstream source.
Manifests: module `src/main/resources/assets/ao_apotheotic_port/`.
Each manifest preserves original data or ranges and explicit pending reasons.
Do not remove unsupported cross-mod systems from the inventory.

Rarity rule counts retain Artifact 8 / Heirloom 4 / Esoteric 16, sort indices
750/800/850 above stock Mythic 700. The three material item models currently use
temporary vanilla textures. Esoteric's intentionally unavailable natural-drop
policy must remain; retain its intended supported acquisition paths.

Original gems use nine tiers: Common, Uncommon, Rare, Epic, Mythic, Ancient,
Artifact, Heirloom, Esoteric. Apotheosis 8.9.0 has only six fixed Purity values.
Its gem registry **rejects custom Gem subclasses/codecs**. A compiled attempt
failed at runtime; the abandoned approach is not active.

Current approach: ordinary native Gem definitions plus `LegacyAttributeBonus`
and persistent/networked `legacy_gem_tier` integer component (0..8).
`LegacyGem` is a helper, not a Gem subclass. Use
`LegacyGem.toLegacyStack(gem, tier)` for exact upper-tier creation. Upper tiers
back onto native PERFECT but retain their separate values in the component.
For upper-only gems created through stock code without that component, current
bonus evaluation defaults to the lowest supported upper tier. This fallback and
the generic lower-case custom name need explicit production design/review.

Native `UnsocketedGem.equals` ignores the new component. Stock gem-cutting
upgrades stop at PERFECT and cannot reach Artifact/Heirloom/Esoteric. Dedicated
recipes/validation must preserve exact tiers; do not flatten the three upper
tiers or globally alter stock gems. Ancient stock item rarity is also absent in
the newer rarity API: the remaining affix migration needs an explicit decision.

Next gem checks: exact-tier validation in every socket path; invalid/missing
components; extraction and re-socketing; component/cache identity; dedicated
upgrade/downgrade behavior; visual names/tiers; conditions and dimensions;
original crafting and acquisition requirements. Network round trips and native
unique-gem rejection already pass and need not be reimplemented.

**Failure detection:** a loader crash returned Gradle BUILD SUCCESSFUL while
zero GameTests ran. Apotheotic `runGameTestServer` now requires a fresh
`All 9 required tests passed :)` log. Increase the expected count deliberately
when adding tests. Verify actual log evidence for other launch tasks too.

## Exact versions and source provenance

- Minecraft 1.21.1; NeoForge 21.1.252; Java 21; Gradle 9.2.1;
  ModDevGradle 2.0.148.
- Apotheosis 1.21.1-8.9.0; Placebo 1.21.1-9.9.2;
  Apothic Attributes 1.21.1-2.11.0; Patchouli 1.21.1-93-NEOFORGE.
  First three downloaded library JARs match the installed profile hashes.
  Dependencies are not embedded into the port JAR.
- Wet Sand upstream: https://github.com/HearthianDev/wet-sand
  at `0e0707813ce811884a51a2614418b4a841d38699`.
- Apotheotic Additions upstream: https://github.com/Bryce792/ApotheoticAdditions
  at `822ecf6993ceaada1504e8dd10a8fea727a6235d` (metadata 2.2.2).
  This source repository has top-level `data/` and `assets/`, not the usual
  `src/main/resources/` layout.
- Apotheosis reference checkout: 1.21 branch at
  `802ce7a83655c84c499e94ec5141ed5cc57e290e`. Reference source uses Placebo
  9.9.3; the actual tested dependency is installed 9.9.2. Prefer exact binaries
  and tests when that distinction matters.
- Terrain snapshot: FreeTerraForged 1.0.0, Biolith 3.0.14,
  TerraBlender 4.1.0.8.

Wet Sand module/artifact is GPL-3.0-only with copied upstream textures.
Apotheotic ported data/names are AFL-3.0 with bundled license and attribution;
original integration code is marked MIT. Preserve notices and extend provenance
when adding source/assets. Native prototype metadata and names remain clearly
experimental. Do not bundle old incompatible mod JARs as a shortcut.

## Local Windows workspace — optional, not needed for a fresh clone

Repository:
`C:/Users/headq/Documents/Codex/2026-10-11/i-d-use-the-existing-v0/work/AmbientOdyssey`

Sibling source checkouts: `upstream-wet-sand`, `upstream-apotheotic-additions`,
`upstream-apotheosis-121`. Sibling Gradle installation:
`gradle-runtime/gradle-9.2.1/bin/gradle.bat`.

Working profile (read/copy only):
`C:/Users/headq/curseforge/minecraft/Instances/Ambient Odyssey v0.4.5 - Custom Integration PREVIEW`

Minecraft installed libraries/version JSONs:
`C:/Users/headq/curseforge/minecraft/Install`.

Disposable copied full roster/configs:
`ports/wet-sand-neoforge/build/client-smoke-runtime` (327 originals + two
prototype JARs). This folder and Gradle caches/source siblings are ignored local
state; they do not come with a GitHub clone. Reconstruct them from actual user
profile or exact authorized pack sources in another environment. The user's
original Actions link, run 38177729206, was a v046 prototype preflight, not a
v045 full-pack export; it cannot substitute for the real roster.

Development full-roster launch encountered Connector clean-Minecraft detection
and Formations development mixin failures. Production launch using installed
Minecraft/NeoForge JSON and 107 installed library files succeeds. Do not
misreport these dev-launch failures as a regression in the working pack.
`tools/run_v046_production_client_smoke.py` reproduces that launch in an isolated
folder. It uses dummy offline credentials and never reads account credentials.
It tracks/terminates only its own test process. Do not kill all Java processes.

## Reproduce native checks

From repository root on this Windows machine:

```powershell
$env:GRADLE_USER_HOME = 'C:/Users/headq/Documents/Codex/ao-gradle-cache'
$env:CI = 'true'
$gradle = '../gradle-runtime/gradle-9.2.1/bin/gradle.bat'
& $gradle -p ports/wet-sand-neoforge build runGameTestServer --console=plain
python tools/validate_v046_wetsand_resources.py ports/wet-sand-neoforge/build/libs/ao-wet-sand-prototype-0.0.1-source-prototype.jar
& $gradle -p ports/wet-sand-neoforge -PaoPersistencePhase=write runGameTestServer --console=plain
& $gradle -p ports/wet-sand-neoforge -PaoPersistencePhase=read runGameTestServer --console=plain
& $gradle -p ports/apotheotic-additions/neoforge build runGameTestServer --console=plain
```

Set `CI=true` for the documented binary-patch mode: default Minecraft source
recompilation failed on this machine with an output-write error. Do not remove
the workaround without evidence. On another machine install Java 21 and Gradle
9.2.1; use `gradle` in place of the local path. Network access to dependency
repositories is required on a fresh environment.

Terrain batch: add `-PaoRuntimeMods=<copied-terrain-JAR-folder>` to Wet Sand.
This selects `run-terrain`. Standalone client: Wet Sand `runClientSmoke`.

Production full-roster startup, only after populating the disposable folder:

```powershell
python tools/run_v046_production_client_smoke.py --install C:/Users/headq/curseforge/minecraft/Install --game-dir ports/wet-sand-neoforge/build/client-smoke-runtime --mod-jar ports/wet-sand-neoforge/build/libs/ao-wet-sand-prototype-0.0.1-source-prototype.jar --timeout 240 --heap 6G
```

The helper copies only the supplied Wet Sand JAR. Copy the tested Apotheotic
prototype into disposable `mods/` separately if checking both ports. Current
model/title marker is Wet Sand-specific; it does not inspect new gem art or
prove Apotheotic gameplay. Require exit 0 and `WETSAND_CLIENT_SMOKE_PASS`.

## Evidence and CI

Checked-in evidence: `docs/testing/v046-evidence/`. Key files:

- `apotheotic-nine-rarity-affix-gem-gametests.log`
- `two-ports-production-full-roster-client.log`
- Wet Sand mechanics/persistence/client logs in the same directory.

Latest server-tested Apotheotic JAR SHA-256:
`15120a5acd36f6bde0156914ebe08adee058a4a82ea6901e0d4a7b3379424af7`.
The two-port client used the preceding JAR:
`d9bc6bc9cbc9e57dec3244626cfadcefebee9fa94bb01c32dc7245f4271b9d90`.
Changes afterward added GameTest assertions, not gameplay code. Do not claim
the latest byte-identical artifact was client-tested. Build hashes can vary in
another environment; inspect that environment's actual JAR.

Workflow: `.github/workflows/v046-two-mod-port-preflight.yml`.
Wet Sand build, resources, mechanics, write/read persistence and native Linux
client precede the Apotheotic native job. A separate source/schema audit is
fail-closed preview data, not the loadable port.

Confirmed successful prior runs: 38180616748, 38182303322, 38184782219.
Latest code checkpoint run:
https://github.com/alsynth/AmbientOdyssey/actions/runs/38185590697
At handoff inspection its schema audit passed; Wet Sand compilation was still
running; Apotheotic had not completed. **Latest checkpoint CI is not yet
certified successful.** Recheck the latest head/run after handoff docs are pushed.
Frequent pushes cancel older runs via workflow concurrency.

Git shell push hit Windows credential-helper errors here. Authenticated GitHub
API tree/commit/ref writes worked, followed by fetch/rebase. Use ordinary push
if it works in your environment. Never force a protected branch. Compare the
expected remote head before API updates. A large inline upload was silently
truncated; the full gem manifest was repaired with chunked base64 blob upload.
For large files verify exact Git blob hashes. Correct manifest blob:
`c6fcf9e0bd88390ed0972fa6ce6fd57cae704bba`.

## Recommended continuation and completion gates

1. Inspect current branch/run and local changes, read this handoff and resume
   contract, and preserve the verified milestone. Resolve any real current CI
   failure before adding subsystems.
2. Close the remaining Wet Sand full-pack world, shoreline, client and
   multiplayer checks first. Use copied profiles/worlds. Record limitations and
   actual evidence rather than marking unsupported checks PASS.
3. Complete the gem tier bridge/recipes/socket extraction in a bounded batch;
   address native equality, missing-component fallback, identity/cache and
   upper-tier naming. Test exact values, unique behavior, save/restart and real
   acquisition. Preserve all original upper-tier requirements.
4. Continue remaining attributes with explicit Ancient/stock rarity mapping
   and installed cross-mod dependencies, then bonus/ability affixes and gems.
   Keep complete inventories and port batches without silently dropping systems.
5. Port bosses/gear/loot, crafting/reforging, trades and the other major systems
   against real installed IDs. Enable Artifact/Heirloom generation only when
   their connected systems and balance checks pass. Preserve intended Esoteric
   acquisition without granting it unintended natural drops.
6. Run full-pack client/world and dedicated-server/two-player checks, resource
   reload and save/restart checks. Confirm no data/recipe/mixin failures and no
   known major upstream systems omitted. Full-pack startup alone is insufficient.
7. Only then produce a complete isolated CurseForge test ZIP with correct mod
   manifest/dependencies, source/config/resources, licenses and installation
   instructions. Run packaged validators and repeat relevant gameplay checks
   on that actual exported build. Do not replace or publish over working v0.4.5.
8. Push each verified subsystem with evidence and a refreshed handoff, so another
   credit limit can be handled without losing work.

## Prompt to give Claude

Continue the Ambient Odyssey v0.4.6 native NeoForge port from the GitHub branch
and checkpoint in this document. Read the repository instructions and this
handoff first. Preserve working v0.4.5 and main, finish remaining Wet Sand
verification first, then complete Apotheotic Additions feature by feature,
retaining Artifact, Heirloom, Esoteric and all major gems/affixes/bosses/systems.
Compile and run meaningful native tests after each subsystem; never equate
compilation or title-screen startup with gameplay compatibility. Keep frequent
GitHub checkpoints with evidence and explicit pending inventories. Produce a
complete isolated CurseForge test build only when its relevant checks pass.
Resume autonomously from the verified work; do not restart or silently omit
unported cross-mod behavior. The current prototypes and zero-weight drops are
deliberately incomplete.
