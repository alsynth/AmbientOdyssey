# AMBIENT ODYSSEY
> **RUNTIME GATE PASSED, 10 Oct: Test8.2** loaded the client, entered a new integrated world and shut down/saved with no fatal Minecraft crash. The previous My Picture Frame/TwelveMonkeys module collision is no longer present. **Not all content validated:** 2952 FTF chunks, **7.14 generated chunks/sec**, five integrated server stalls (up to 18.932 s); invalid Flight Rings smelt recipe definitions, invalid Additional Structures `minecraft:pale_garden` biome tag, 25 shared structure salts (not all actual collisions), old `byg:` item errors. **Test8.3 source + optional private ZIP** stage two Flight Ring salvage recipe codec fixes and split a *confirmed Create Arise/Easy Structures windmill identical salt* while retaining Arise's 90/10 grid; 265 CF refs unchanged. Source/ZIP static preflight pass, Test8.3 Minecraft runtime pending. **All remaining biome/ocean/bridge/Nether/End gameplay quality tests and solo quests multiplayer still open.** Full evidence: [Test8.2 runtime and last worldgen audit](docs/testing/TEST8_2_RUNTIME_AND_LAST_WORLDGEN_AUDIT_2026-10-10.md). Existing Test8.2 working game/save must not be overwritten for testing.

> **LATEST 0.3.8 TEST8.2 — CRASH FIX BEFORE WORLDGEN (10 Oct).** User's Test8.1 failed before main menu due to Java module duplicate package between `mpf` (My Picture Frame) and `com.twelvemonkeys.common.image`, not a confirmed Iron's Jewelry bug. Source removes My Picture Frame (CF 1582023), pins HAPI `883374:9063597`, Atlas API `1145462:6880789`, Flight Rings `401229:7782196` and required MidnightLib `488090:7318664`, bringing import to **265** CF refs. Paxi overrides **both Flight Rings recipes** with Nether-era and boss-gated ingredients. **PRIVATE** ZIP additionally bundles user-uploaded Better Bastions and NeoReefRedux JARs and ORIGINAL Ambient Odyssey icon in overrides. **Not yet game-launched or CurseForge-public-approved.** Full test handoff: [Test8.2 report](docs/testing/TEST8_2_CRASH_FIX_FLIGHT_ICON_AND_PACKAGING_2026-10-10.md). Other Test8.1 worldgen changes remain preserved. 

> **LATEST Test 8.1 (10 October):** Replaces Test 8 preview, with **no new CurseForge project pins** (still 262). Dragon skeleton chance 0.003333→0.0015; Paxi `ao_dragon_caves` data overrides widen **underground fire/lightning dragon caves** to all Overworld biomes while allowing **ice caves** only in cold/snowy Overworld biomes, leaving surface roost tags unchanged; Create Rustic barn, windmill, smithy and well grid opportunities reduced to limit structure overlaps. [Test8 checklist](docs/testing/TEST8_COMBINED_WORLDGEN_ONE_PASS_CHECKLIST.md) now includes explicit dragon and Rustic checks. Still manually install the **user-uploaded Better Bastions** and **NeoReefRedux** JARs. [Pre-End/midgame flight audit](docs/testing/MIDGAME_FLIGHT_OPTIONS_2026-10-10.md) compares existing Angel Wings, Ars Glide, Hippogryphs, flight rings, Create anchors and craftable Elytra. No flight mods installed yet; worldgen freeze NOT accepted.

> **ACTIVE 0.3.8 COMBINED TEST, 10 Oct:** The source lock now stages **11 new CurseForge projects** (including 10 ocean/dependency additions and FTB Solo Quests), total **262** including Solas and Complementary shader file references from 0.3.7. Curated BWG/BOP biomes, Prairie distribution, independent WDA/IDAS rare lighthouse grids, rarer Eternal Starlight/Dragon Tower and BWG Dacite Shore are staged. Separate **test ZIP** has static CRC/manifest pass, not runtime verified. **Two manual mods not in ZIP**: Better Bastions exact NeoForge 1.21.1 file and NeoReefRedux Modrinth port. Read **[one-pass combined test checklist](docs/testing/TEST8_COMBINED_WORLDGEN_ONE_PASS_CHECKLIST.md)** before any single-player or server test. Worldgen is NOT frozen, bridge/Streams Reflowing physical placement remains unresolved. The previously frozen Test5 history below is not the live status.

> **ACTIVE STATE, 10 October 2026:** User **runtime-confirmed** v0.3.7 Dev2 Minecraft/world startup, removal of Dimensional Doors fixed creative-mode crash, new mods load, and NeOculus Shader Packs menu works. GitHub source has since advanced to **v0.3.7-prefreeze-dev3**, with Iron's Jewelry 2.0.2, **10 GiB** recommended RAM, narrator onboarding fix and two official CurseForge shader-project references. **Dev3 has not been freshly exported/played.** See `docs/status/CURRENT_STATE.md` and `docs/testing/OCEAN_EXPANSION_PREFREEZE_REVIEW_2026-10-10.md`. This live status supersedes historic Test5/Test6 blocked lines below.

> **Latest Test 6 runtime result (9 Oct 2026):** Source/build is statically verified but the first clean CurseForge client startup **FAILED**: NeoForge 21.1.252 rejected `Structory_Towers_26.2_v1.0.17.jar` with `InvalidModFileException: Missing ModLoader`. Awaiting live test of official v1.0.14 fallback `783522:7078283` before changing locked manifest or regenerating Test 6 ZIP. See `docs/testing/TEST6_RUNTIME_FINDINGS_2026-10-09.md` and `docs/status/CURRENT_STATE.md`. The original checkboxes and Black Spiral exclusion below are historical and superseded by more recent approved decisions.

# Master Development TODO — 0.3.x → 0.4.0

**Created:** 9 October 2026  
**Preserved baseline:** original v0.3.1 Structure Test 5  
**Current static candidate:** v0.3.1 Structure Test 5 audit1  
**Minecraft:** 1.21.1  
**Loader:** NeoForge 21.1.252  
**Target:** 5–7-player exploration-first RPG modpack  
**Recommended client RAM:** 10 GB (10,240 MiB; launcher manifest recommendation, adjust to machine)  
**Planning status:** Living master document

---

## 9 October 2026 continuation — current verified state

- [x] Reproduce the untouched original Test 5 import exactly and pass its 76 gates; preserve original source/import archives and report evidence as rollback.
- [x] Complete the available binary audit and source repairs described in `STRUCTURE_TEST5_CHANGELOG.md`. Expanded evidence is 177 + 19 = 196 binaries; 26 complete unique binaries were directly inspected this continuation.
- [x] Build the `structure-test5-audit1` import and source archives, validate scoped source/export gates, check ZIP CRC/safe unique paths, and confirm a byte-identical rebuild from a clean source extraction. Final counts/hashes are in `release-validation-summary.json` and `SHA256SUMS.txt`.
- [x] Rebuild structure and screening catalogues from the saved evidence, update this master TODO, and preserve earlier handoffs/backlog as evidence.
- [ ] BLOCKED: complete the installed-profile audit with the 41 exact files in `MISSING_JARS.txt`.
- [ ] BLOCKED: audit/install the eight approved additions from `APPROVED_ADDITION_JARS.txt`; selected file metadata is saved, but binary checksums, dependency closure and Black Spiral control remain unverified.
- [ ] TEST: live registry loading, pack priority, repaired assembly, natural distribution, client models and performance. No gameplay pass or 0.4.0 promotion is claimed.

The user's latest instruction explicitly allows completion of static work before an in-game test. W1 is a later acceptance track, not a prerequisite for this audit/source/build delivery. Sky Villages may spawn above rivers; land and all four explicit river/Streams biome IDs remain eligible. The reported ocean-only observation is preserved as an unresolved runtime observation.

This master supersedes older install preferences. The 6 October 166-candidate registry is screened for future worldgen risk, not an install list. The original 8 October TODO is retained under `evidence/baseline-test5/TODO.md`; its unique later-stage controls/QoL/boss/performance tasks remain in the master backlog. The original supplied master is retained under `evidence/handoffs/master-todo-source-2026-10-09.md`.

# PART I — Project rules and current state

## 1. Purpose of the 0.3.x phase

Version 0.3.x is primarily the **world generation, exploration foundation, compatibility, and performance phase**.

Before entering 0.4.0, Ambient Odyssey should have:

- An attractive, sufficiently varied and coherent world.
- A well-distributed set of structures that meaningfully rewards exploration.
- Correctly integrated modded biomes.
- Good coverage across Overworld, caves, oceans, Nether, End and other major dimensions.
- No major known structure-generation or registry problems.
- Reliable multiplayer and dedicated-server operation.
- Acceptable chunk-generation performance.
- Reasonably controlled memory use and client performance.
- A tested and reproducible CurseForge build.
- A stable enough foundation that adding content or designing quests will not require repeatedly rebuilding worldgen.

**Important:** Completing 0.3.x does not mean every mod is perfectly balanced, every quest is finished, or the final GUI is ready. Those are separate future phases.

## 2. Task status conventions

Every task should eventually have one of these states:

- `[x]` Completed and verified at its stated level.
- `[ ]` Pending.
- `BLOCKED` — Cannot proceed without another prerequisite.
- `TEST` — Implemented, awaiting actual gameplay validation.
- `DECISION` — Requires an explicit user choice.
- `DEFERRED` — Intentionally outside the current development phase.

Do not mark a change completed merely because a configuration file has been edited.

A task involving gameplay behavior is not fully verified until the corresponding runtime test succeeds.

## 3. Authoritative project files

### Main source of truth

`Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip`

### Existing packaged build

`Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip`

### Supporting information

- `TODO.md`
- `README-0.3.1.md`
- `STRUCTURE_BIOME_AUDIT.md`
- `STRUCTURE_TEST5_CHANGELOG.md`
- `STRUCTURE_TEST5_VALIDATION.md`
- `STRUCTURE_TEST5_INSTALL.md`
- `STRUCTURE_REGISTRY_CATALOG.csv`
- `STRUCTURE_SET_CATALOG.csv`
- `STRUCTURE_BIOME_MATRIX.csv`
- `jar-audit-coverage-test5.json`
- `TANS_OPEN_FIELD_TUNING_PLAN.md`

The source archive contains the editable configuration inputs and build scripts.

**Source files must be updated first; generated datapacks should then be rebuilt.**

### Baseline validation

The untouched original Structure Test 5 was reproduced this session and passed:

- 76/76 scoped static validation checks.
- Archive CRC and safe-path validation.
- Root CurseForge manifest validation.
- Byte-identical clean rebuild.
- Audit/catalogue regeneration checks.

177 complete JARs were audited.

Originally, 60 installed JARs remained unavailable to that audit. Seventeen handoff JARs plus previously supplied Curios and Traveloptics have now been audited, leaving 41 exact logged filenames unavailable. Expanded resource evidence covers 196 binaries; direct current-session class/resource screening covers 26 complete unique binaries, including seven re-supplied originals.

All 19 newly recovered JARs have completed the expanded scoped binary audit. The unavailable 41 existing-profile JARs and eight approved additions remain BLOCKED.

**Structure Test 5 has not yet passed its intended fresh-world runtime acceptance tests.**

---

# PART II — Non-negotiable project decisions

These decisions are already established and should not be reopened casually.

## 4. Core modpack identity

- [x] Ambient Odyssey remains exploration-first with RPG, combat and boss progression.
- [x] Multiplayer is designed for approximately 5–7 players.
- [x] Primary distribution is CurseForge.
- [x] Target Minecraft 1.21.1, using NeoForge.
- [x] Preserve the established extensive mod roster, rather than reducing the pack to a lightweight vanilla+ experience.
- [x] Preserve the goal of a large, polished FTB Quests book in a later development phase.
- [ ] Continue to judge mods by exploration, gameplay and integration value, not simply mod count.
- [ ] Avoid redundant mods that provide virtually identical structures or progression systems without a clear purpose.

## 5. World generation decisions

- [x] FreeTerraForged is the sole primary Overworld terrain generator.
- [x] Tectonic was removed from the chosen stack.
- [x] Biolith is retained for biome replacement.
- [x] The curated roster includes 40 intended Overworld donor biomes and two Nether donors.
- [x] TerraBlender remains installed where required.
- [x] Streams Reflowing remains part of worldgen.
- [x] Tan's Huge Trees remains part of worldgen.
- [x] TRMT remains the desired walked/eroded path system.
- [x] FTF's named AO preset uses continent scale 6500 and river count 15.
- [ ] Avoid modifying all terrain, biome, structure and tree systems in a single untestable patch.
- [ ] Keep Big Globe outside the main build; experiment with it separately if revisited.
- [ ] Keep the exact curated biome roster unless the user approves additions or removals.

## 6. Structure decisions

- [x] Integrated Stronghold is the intended stronghold system.
- [x] Moog's Temples Reimagined stronghold replacement is disabled.
- [x] MTR desert/jungle temple generation stays enabled.
- [x] MTR ocean monument replacement stays disabled.
- [x] YUNG's Better Mineshafts remains retained in the latest Test 5 source decisions.
- [x] YUNG's Better Witch Huts remains retained.
- [x] Moog's Mineshafts Reimagined is not selected.
- [x] WDA Small Blimp is disabled.
- [x] WDA Coliseum is disabled.
- [x] WDA Bathhouse is intentionally rare.
- [x] Dungeon Crawl is configured at 20/9.
- [x] Existing Heavenly structures have separate Overworld and End branches.
- [x] Do not add StructureOverlapless alongside the present Integrated API arrangement.
- [ ] Avoid accidental duplication of village, stronghold, temple, ocean monument or major dungeon ownership.

## 7. Explicit mod decisions

### Approved for the next structure expansion

- [ ] YUNG's Extras.
- [ ] YUNG's Bridges.
- [ ] Structory: Towers.
- [ ] Archaion.
- [ ] Explorify.
- [ ] Additional Structures.
- [ ] Create: Structures Arise.
- [ ] Create: Easy Structures.

These eight mods are **approved additions, explicitly not installed in audit1; exact binary/dependency audits remain BLOCKED**.

### Preserved existing addition

- [x] Create: Rustic Structures is already part of the intended build.

### Special restrictions

- [ ] BLOCKED: disable Explorify's Nether Black Spiral after its exact native ID/placement route is audited. Explorify is not installed in audit1.
- [x] Implement a dimension-preserving candidate-density increase for all 20 Farmers Structures variants. TEST: natural discoverability and terrain fit; optional absent dimensions remain inactive.
- [ ] Do not add FDstructure.
- [ ] Do not add unselected Create structure addons merely because they exist.
- [ ] Keep Luki's Crazy Chambers parked due to previous initialization/worldgen errors.
- [ ] Keep Sunken Spires deferred for the ocean expansion.
- [ ] Keep Big Globe deferred for a separate experiment.
- [ ] Do not reintroduce Companions! or Modern Companions.
- [x] Verify that queued Born in Chaos removal has actually propagated through the next built export.
- [ ] Preserve the intended default Minecraft-style menu rather than re-enabling unwanted custom menus or inventory UI replacements.

---

# PART III — Development sequencing

## 8. Recommended work order

The following sequence should be the default. Changes to the release source are integrated by one owner.

| Wave | Focus | Required outcome |
|---|---|---|
| W0 | Baseline preservation | Reproducible untouched Test 5 |
| W1 | Existing runtime smoke test | Verify Test 5 can launch and generate structures |
| W2 | JAR and structure-provider audit | Close major unknowns before tuning |
| W3 | Eight structure additions | Add and verify selected content |
| W4 | Structure compatibility and density | Fix biome gaps, placement and rarity |
| W5 | Terrain, biome, trees and paths | Improve landscape variety and ecology |
| W6 | Dimension and worldgen cleanup | Check caves, oceans, Nether, End and portals |
| W7 | Independent compatibility cleanup | Resolve recipes, assets, slots, loot and GUI issues |
| W8 | Performance and multiplayer | Measured client/server stability |
| W9 | Full QA and release packaging | Validated 0.3.x final build |
| GATE | Transition to 0.4.0 | Worldgen/content foundation accepted |

Do not proceed directly to large-scale terrain tuning while the basic structure system remains unverified.

---

# PART IV — W0: Baseline preservation and reproducibility

## 9. Source and build hygiene

- [x] Extract the exact Test 5 source ZIP into a fresh working directory.
- [x] Preserve an unchanged archive copy.
- [x] Run the current build script without modifications.
- [x] Confirm Python version and required build dependencies.
- [x] Reproduce the known Test 5 import archive.
- [x] Run all original 76 static checks.
- [x] Regenerate the three structure catalogues from cached audit evidence.
- [x] Compare results with existing validation hashes and reports.
- [x] If rebuild hashes differ, identify the exact cause before making changes. Original rebuild was byte-identical; no divergence to resolve.
- [x] Verify that the source archive has no missing editable authoring inputs.
- [x] Verify that generated Paxi datapacks correspond to their source files.
- [x] Identify all compiler-owned directories that are cleared during a build.
- [x] Confirm obsolete Test 3/4 grids are not resurrected.
- [x] Confirm Minecraft and NeoForge versions remain pinned.
- [x] Record the current mod manifest's project/file IDs.
- [ ] Record actual installed mod versions from a current runtime log.
- [ ] Compare installed JAR names with the locked manifest.
- [ ] Check for manually installed mods missing from the manifest.
- [ ] Check for duplicate JARs or conflicting mod versions.
- [ ] Check for manually patched mod JARs that would not be reproduced by a normal CurseForge import.
- [x] Verify the exact Paxi directory and datapack layout.
- [ ] Check datapack priority and resource-pack order.
- [x] Confirm existing configs and assets survive a clean rebuild.
- [x] Preserve existing quest data, default options, keybinds and GUI assets.
- [x] Prepare a rollback strategy for every later work wave.

### Failure scenarios

- Build script still references obsolete source inputs.
- A manual edit in generated datapacks disappears on rebuild.
- CurseForge downloads a different JAR than the user's installed copy.
- A supposedly disabled mod remains in the exported manifest.
- A dependency changes versions without an intentional update.
- A local configuration appears to work but was never included in the export.
- Rebuild passes, but its output differs from the exact profile that was tested.

### W0 acceptance

A fresh source extraction can rebuild the untouched Test 5 archive, and its static checks pass without needing undocumented manual edits.

---

# PART V — W1: Initial in-game verification

## 10. Test profile preparation

- [ ] Create a separate CurseForge profile from the untouched Test 5 export.
- [ ] Keep the older profile for comparison.
- [ ] Start Minecraft without shaders.
- [ ] Use a documented render/simulation distance.
- [ ] Record allocated RAM and JVM arguments.
- [ ] Record client GPU, CPU, Java runtime and operating system.
- [ ] Save a clean launch log.
- [ ] Confirm the main menu appears.
- [ ] Confirm correct mod count and loader version.
- [ ] Check the Mod List for missing dependencies.
- [ ] Verify the expected custom main-menu and inventory settings.
- [ ] Create a new world with World Type Default.
- [ ] Select the Ambient Odyssey 0.3.1 FTF preset.
- [ ] Check continent scale and river count.
- [ ] Record world seed.
- [ ] Time world creation and first spawn stabilization.
- [ ] Wait until chunk generation and memory use settle before recording performance.
- [ ] Verify correct AO datapack activation.
- [ ] Save the full post-world-creation log.
- [ ] Check basic Overworld movement, combat, block breaking and saving.
- [ ] Save, exit, relaunch and load the same world.
- [ ] Verify the save loads without new datapack/registry errors.
- [ ] Generate several new areas on a repeatable route.
- [ ] Check basic Nether and End access in a disposable test world.
- [ ] Record every crash, registry warning and structure error separately.

## 11. Existing Test 5 regression checks

- [ ] Confirm Small Blimp cannot naturally generate.
- [ ] Confirm Coliseum cannot naturally generate.
- [ ] Confirm Bathhouse remains enabled but rare.
- [ ] Locate and inspect representative WDA ordinary buildings.
- [ ] Locate and inspect representative IDAS houses/inns/farms.
- [ ] Confirm Dungeon Crawl generates using its intended settings.
- [ ] Check Apotheosis tower generation.
- [ ] Check sky villages over land.
- [ ] Check sky villages above rivers/Streams channels.
- [ ] Check Sky Whale Ship behavior.
- [ ] Test the three `ambient_odyssey:heavenly_*_overworld` IDs.
- [ ] Check original Heavenly versions remain on the intended End side.
- [ ] Inspect Foundry gear decorations.
- [ ] Inspect Mechanical Nest decorations.
- [ ] Inspect Cabin Village villager pools.
- [ ] Inspect Cabin fisherman lecterns.
- [ ] Test RAR-Compat/Artifacts native slots.
- [ ] Test Enigmatic Legacy+ amulets and scrolls in Curios.
- [ ] Confirm the Simply More repaired recipe loads.

### Important test distinction

A successful `/locate` result is evidence that the registry/search recognizes a structure, not proof that structures are generating naturally at the desired density.

A forced `/place structure` test is useful for assembly, but it does not prove native placement success.

### W1 acceptance

Test 5 launches, creates and reloads a world, and does not show a newly introduced fatal issue. Representative structure and equipment tests are recorded; untested rare content remains explicitly pending rather than being marked successful.

---

# PART VI — W2: Complete installed-mod and structure audit

## 12. Recover missing JAR coverage

Audit1 coverage: 196 resource-audited binaries, 26 available for current binary/class screening, 19 newly recovered, 41 existing-profile binaries still BLOCKED. `MISSING_JARS.txt` names every missing file. The eight approved additions have a separate request list, `APPROVED_ADDITION_JARS.txt`. New binary metadata and class/resource evidence are retained; original evidence is preserved without claiming fresh inspection of unavailable binaries.

- [x] Start from the original `jar-audit-coverage-test5.json`.
- [x] Account for all 19 newly recovered individual JARs (17 handoff + Curios + Traveloptics).
- [x] Verify every newly uploaded archive is intact.
- [x] Record SHA-256, mod ID, version and filename.
- [x] Audit all 19 new JARs; preserve original 177-JAR evidence separately.
- [x] Update the previously incomplete coverage report.
- [x] Separate inspected JARs from JARs merely available.
- [ ] Determine which of the remaining 41 require full inspection for the current worldgen pass.
- [ ] Prioritize the remaining uninspected worldgen/structure libraries.
- [ ] Retrieve the exact authoritative Minecraft 1.21.1 biome-tag resources.
- [ ] Complete previously unresolved native tag-graph references where evidence permits.
- [ ] Keep unresolved optional tags visible rather than assuming missing tags are empty.

## 13. For every structure provider

Current recorded inventory: 1,216 native structure IDs, 666 native sets, 4,294 pools and 1,254 biome tags; catalogues contain 1,219 definitions including three AO clones, 673 set/route rows and 52 biome columns. CTOV's 74 Java/Lithostitched routes are explicit. The generic checklist below remains open for unavailable providers and for assembly/behavior beyond the scoped snapshot; it does not undo the completed recorded inventories.

- [x] Publish installed-mod screening (196 rows), Create-addon screening and all 166 future registry candidates with explicit evidence scopes.
- [x] Enumerate 70 native structure/set/pool resource collisions in `NATIVE_RESOURCE_COLLISIONS.csv`.
- [ ] TEST: establish runtime winners for `minecraft:villages` (Luki/Nature's Spirit) and `minecraft:village_taiga` (Luki/Dungeons & Taverns); snapshot ordering is not live priority.

- [ ] Enumerate native structure JSON definitions.
- [ ] Enumerate structure-set JSON definitions.
- [ ] Enumerate all template pools.
- [ ] Enumerate biome eligibility tags.
- [ ] Follow nested and conditional tags to actual members.
- [ ] Respect NeoForge AND/OR/NOT semantics and removals.
- [ ] Record dimension restrictions.
- [ ] Record generation step.
- [ ] Record generation height and terrain adaptation.
- [ ] Record spacing, separation, frequency, salt and weights.
- [ ] Record exclusion zones.
- [ ] Identify disabled variants.
- [ ] Identify duplicate placement owners.
- [ ] Identify unavailable external asset dependencies.
- [ ] Identify obsolete biome IDs.
- [ ] Identify required template pools missing from the installed JAR.
- [ ] Identify jigsaw references whose targets are nonexistent.
- [ ] Identify malformed JSON, NBT or invalid structure processors.
- [ ] Identify unusual generation-time behavior or global scanning.
- [ ] Record existing AO overrides affecting the provider.
- [ ] Distinguish candidate frequency from successful-generation frequency.
- [ ] Assign each structure a size and function category.
- [ ] Update the structure catalogue and compatibility matrix.

## 14. Provider-specific investigations

### Cristel Lib 3.1.7

- [x] Mirror extracted AO membership in Cristel's native per-set toggles, including Bathhouse's native route; preserve its enabled independent AO route.
- [ ] TEST: verify live Cristel/Paxi pack priority and retention of AO-only exclusions. The runtime pack ID is not exposed as a selectable disabled builtin default in the inspected code; do not claim it is disabled by config.

- [x] Inspect how placement configuration is loaded.
- [x] Verify how spacing/separation overrides are processed.
- [x] Verify frequency field interpretation.
- [x] Verify placement ownership and native membership changes.
- [x] Verify whether runtime config processing can override AO datapack settings. Native-file/runtime-pack behavior confirmed in bytecode; live pack priority and AO-only exclusions remain TEST.
- [x] Check supported toggle behavior.
- [x] Check exclusion-zone handling. Native-file/runtime-pack behavior confirmed in bytecode; live pack priority and AO-only exclusions remain TEST.
- [ ] Compare actual runtime results with static Test 5 assumptions.

### CTOV

- [x] Compile asset-backed mountain tower alias and desert waystone pool repairs; migrate the supplied Waystones template's legacy connectors while preserving geometry/palette/entities. TEST: village/outpost assembly and visual fit.
- [x] Add curated eligibility to 32 enabled village/outpost definitions without creating new independent CTOV grids.

- [x] Inspect `ctov:village/waystone/sand`.
- [x] Inspect `ctov:pillager_outpost/mountain/towers`.
- [x] Locate actual referring jigsaw NBT and matching assets.
- [x] Determine whether Waystones integration changes available pools.
- [x] Avoid arbitrary empty-pool repairs.
- [ ] Verify village formation after repairs.
- [ ] Inspect CTOV structures on steep FTF terrain.
- [ ] Check village conflicts with Integrated Villages, IDAS and other village providers.

### Other audited providers

- [x] Dungeons and Taverns.
- [x] Towns and Towers.
- [x] WDA Seven Seas.
- [x] Towers of the Wild: Modded.
- [x] YUNG's Better Mineshafts.
- [x] YUNG's Better Nether Fortresses.
- [x] YUNG's Better Witch Huts.
- [x] YUNG's Better End Island.
- [x] Echoes of the End.
- [x] Underwater Village.
- [x] End Villager Outpost.
- [x] Create: Rustic Structures.
- [ ] Sky Villages.
- [ ] Sky Whale Ship.
- [ ] Moog's structure families.
- [ ] Farmers Structures.

### Known existing asset issues

- [ ] IDAS Dread Citadel `dread_citadel5`.
- [ ] IDAS Dread Citadel `dread_citadel12`.
- [ ] IDAS Ancient Mines `ancient_mines_entrance2`.
- [ ] Blank `minecraft:` jigsaw pool references.
- [ ] Cook-related jigsaw/pool references.
- [ ] Graveyard crypt pool warnings.
- [ ] Malkuth arena start-jigsaw issue.
- [ ] Missing Guard Villagers entity references where applicable.
- [ ] Stale structure-template entity NBT.
- [ ] Missing attributes and invalid-air stack warnings.

### W2 acceptance

The important worldgen providers have a documented effective registry and placement graph. Critical unresolved assets are identified exactly, and speculative repairs are not substituted for evidence.

---

# PART VII — W3: Eight approved structure mods

## 15. Acquisition and dependency checks

For each of the eight additions:

- [ ] Identify the exact 1.21.1-compatible file.
- [ ] Verify the loader is NeoForge or demonstrably compatible.
- [ ] Record CurseForge project/file IDs.
- [ ] Record version and checksum.
- [ ] Inspect JAR dependency metadata.
- [ ] Check required versus optional dependencies.
- [ ] Check overlap with existing installed libraries.
- [ ] Check compatibility with FreeTerraForged.
- [ ] Check compatibility with Biolith and modded biomes.
- [ ] Check Paxi/datapack compatibility.
- [ ] Check availability of native config toggles.
- [ ] Check whether its structures require blocks from another content mod.
- [ ] Check whether its structure placement requires custom code or is data-driven.
- [ ] Add to source manifest only once verified.
- [ ] Launch a smoke-test profile with the additions before density tuning.

## 16. Per-addon investigations

### YUNG's Extras

- [ ] Catalogue all added landmarks.
- [ ] Identify small versus medium structures.
- [ ] Check eligibility in curated biomes.
- [ ] Prevent needless duplication of other small ruins.
- [ ] Verify generation at different elevations.

### YUNG's Bridges

- [ ] Inspect biome selectors and bridge placement constraints.
- [ ] Check FTF river geometry.
- [ ] Check Streams Reflowing compatibility.
- [ ] Check steep riverbanks and wide valleys.
- [ ] Check floating or buried bridge ends.
- [ ] Check bridges interfering with buildings and villages.
- [ ] Verify a naturally generated bridge before increasing frequency.

### Structory: Towers

- [ ] Catalogue tower variants.
- [ ] Check forest, mountain and open-terrain eligibility.
- [ ] Compare frequency with Apotheosis towers.
- [ ] Check overlap with TotW and existing tower providers.
- [ ] Avoid excessive tower clustering.
- [ ] Inspect high-elevation tower clipping.

### Archaion

- [ ] Verify actual mod/version and native structure categories.
- [ ] Classify minor ruins, major sites and encounters separately.
- [ ] Check biome/dimension compatibility.
- [ ] Check whether any structures contain powerful loot or difficult combat.
- [ ] Assign major discoveries appropriate rarity.
- [ ] Check structure terrain adaptation and connected template pools.

### Explorify

- [ ] Catalogue structures and size categories.
- [ ] Verify appropriate biome eligibility.
- [ ] Identify the exact Nether Black Spiral structure ID.
- [ ] Disable Black Spiral using a valid configuration or datapack mechanism.
- [ ] Confirm it is absent from the effective placement graph.
- [ ] Preserve other wanted Explorify structures.
- [ ] Check compatibility with existing small-landmark providers.

### Additional Structures

- [ ] Verify actual 1.21.1 dependencies.
- [ ] Catalogue its large structure roster.
- [ ] Categorize decorative, small, medium and major structures.
- [ ] Check placement duplication with current ruins.
- [ ] Check default spawn frequency.
- [ ] Add curated biome eligibility.
- [ ] Avoid disproportionately filling vanilla biomes.
- [ ] Keep rare landmarks meaningfully rare.

### Create: Structures Arise

- [ ] Verify compatibility with installed Create version.
- [ ] Catalogue industrial and machinery structures.
- [ ] Check large factory/worldgen templates.
- [ ] Check included Create blocks and mechanisms.
- [ ] Check whether machinery becomes active immediately on generation.
- [ ] Test large structures on steep terrain.
- [ ] Assign larger sites appropriate rarity.
- [ ] Check whether generated machines provide unintended early-game shortcuts.
- [ ] Inspect loot and material quantities.

### Create: Easy Structures

- [ ] Verify Create dependency compatibility.
- [ ] Catalogue structures.
- [ ] Compare directly with existing Rustic Structures.
- [ ] Prioritize accessible small Create discoveries.
- [ ] Check loot and functional contraptions.
- [ ] Ensure it does not flood the world with identical structures.
- [ ] Check configuration and biome eligibility.

## 17. Integration rules

- [x] Select primary file metadata for all eight approved additions; record project/file IDs and exact filenames in editable `release_030/approved-structure-additions.json`.
- [ ] BLOCKED: acquire their exact binaries and audit checksums, dependencies, structures/features/code routes and Explorify's Black Spiral disabling mechanism.
- [ ] BLOCKED: add these eight to the locked manifest only after the above audits. Audit1 installs none of them; no unrelated addon was substituted.

- [ ] Add approved mods as a controlled content wave.
- [ ] Keep a before/after source diff.
- [ ] Confirm all required dependencies resolve on CurseForge.
- [ ] Avoid adding unrelated recommended mods.
- [ ] Verify no unwanted menus or resource packs activate.
- [ ] Verify no changes to the FTF preset are required just to load the new mods.
- [ ] Build a fresh test export.
- [ ] Confirm launch and registry loading before applying major frequency tuning.
- [ ] Update the modpack manifest and changelog.
- [ ] Add the new structures to catalogues and test matrices.

### W3 acceptance

All eight approved mods are installed in the test build with verified dependencies and successfully load. Any incompatible candidate is clearly identified as blocked rather than silently omitted or replaced.

---

# PART VIII — W4: Structure generation and distribution

This is one of the largest priorities of 0.3.x.

## 18. Main design goals

- Plenty of meaningful discoveries during normal exploration.
- Less empty-feeling Prairie, Grassland, Flower Fields and Sakura.
- A healthy variety of small, medium and significant buildings.
- Villages present but not dominating every suitable location.
- Apotheosis towers accessible enough for early gear progression.
- Sky structures genuinely discoverable above ordinary land.
- Large dungeons and boss landmarks impressive and appropriately rare.
- Structure spacing that avoids obvious clustering and clipping.
- Good representation in modded biomes, not just vanilla ones.

## 19. Biome selector compatibility

- [ ] Recheck all common `minecraft`, `c` and `forge` tags used by structure mods.
- [ ] Recheck direct vanilla-biome-only selectors.
- [ ] Recheck provider-specific nested tags.
- [ ] Check Prairie.
- [ ] Check RU Grassland.
- [ ] Check RU Flower Fields.
- [ ] Check BWG Sakura Grove.
- [ ] Check BOP Pumpkin Patch.
- [ ] Check other retained open landscapes.
- [ ] Check selected deciduous forests.
- [ ] Check redwood and coniferous forests.
- [ ] Check cool/mountain forests.
- [ ] Check snowy biomes.
- [ ] Check wetlands and swamps.
- [ ] Check beaches and coasts.
- [ ] Check rivers and Streams.
- [ ] Check ocean-specific structures.
- [ ] Check cave-specific structures.
- [ ] Verify forbidden dimensions remain excluded.
- [x] Confirm direct selector patches are included in the generated datapacks.
- [ ] Check optional tags that have empty or missing provider collections.
- [ ] Recompute effective eligibility after new mods are installed.

## 20. Structure density categories

Use the following categories for systematic tuning:

| Category | Intended treatment |
|---|---|
| Environmental details | Common, but not overwhelming |
| Small camps and cabins | Fairly common |
| Farms and houses | Common enough to notice consistently |
| Medium ruins and buildings | Regular exploration rewards |
| Villages | Distinctive, appropriately spaced |
| Towers | Accessible but not visually repetitive |
| Sky structures | Discoverable across normal landscapes |
| Large landmarks | Uncommon |
| Boss dungeons | Rare enough to remain meaningful |
| Major multi-stage structures | Individually balanced |
| Ocean structures | Separate ocean-specific distribution |
| Nether/End structures | Separate dimension-specific tuning |

These are qualitative targets. Numeric frequency targets must be calibrated using measured baseline generation and player feedback rather than invented percentages.

## 21. Farmers Structures comprehensive pass

Static policy: approximately two times native candidate attempts using `floor(native spacing / sqrt(2))` and proportional bounded separation for all 20 native variants. Six previously tuned grids are not doubled again. Unique signed-32-bit salts replace native correlations and an out-of-range Undergarden salt. Native membership, weights, selectors, height and exclusions are unchanged. `FARMERS_STRUCTURE_CATALOG.csv` records the dimension evidence; Honey Cake belongs to Bumblezone, not ordinary Overworld farms. Runtime acceptance and absent optional dimensions remain pending.

- [x] Catalogue all 20 variants.
- [x] Keep their biome and dimension meanings intact.
- [x] Check their actual native placement grids.
- [x] Check repeated structure salts.
- [ ] Fix relevant obsolete biome tags.
- [ ] Identify variants with no eligible curated biome in their intended dimension.
- [x] Increase ordinary surface farm frequency. Static candidate settings implemented; natural-generation acceptance remains TEST.
- [x] Increase appropriate coastal and aquatic variants. Static candidate settings implemented; natural-generation acceptance remains TEST.
- [x] Tune underground farms separately. Static candidate settings implemented; natural-generation acceptance remains TEST.
- [x] Tune Nether variants separately. Static candidate settings implemented; natural-generation acceptance remains TEST.
- [x] Tune Aether/Undergarden variants in their own dimensions. Static candidate settings implemented; natural-generation acceptance remains TEST.
- [x] Check existing dense structures before further increasing their candidate rate.
- [x] Preserve intended proximity restrictions.
- [ ] Ensure increased frequency does not cause identical structures to appear in clusters.
- [ ] Confirm representative farms actually generate in fresh worlds.
- [ ] Record variant counts by region.
- [x] Preserve all variants where feasible; do not add FDstructure.

## 22. Existing structure families

### WDA

- [ ] Verify medium houses and camps after Test 5.
- [ ] Confirm Bathhouse remains rare.
- [ ] Confirm Coliseum and Small Blimp remain disabled.
- [ ] Check Foundry, Mechanical Nest and other large assemblies.
- [ ] Check major dungeon rarity.
- [ ] Check giant structures against terrain.
- [ ] Verify coastal/ocean sites use suitable tags.

### IDAS and Integrated Villages

- [ ] Check normal farm/house coverage.
- [ ] Check castles and large structures separately.
- [ ] Check duplicate village grids.
- [ ] Check structure placement on FTF slopes.
- [ ] Inspect villager spawning and professions.
- [ ] Check connected template pools.
- [ ] Check overlap with CTOV and Towns and Towers.
- [ ] Check underground and ocean variants independently.

### Dungeon Crawl

- [ ] Preserve 20/9 until measured.
- [ ] Record natural cave-dungeon frequency.
- [ ] Check entry accessibility.
- [ ] Check clipping with underground terrain.
- [ ] Check conflicts with caves and cave decorations.
- [ ] Confirm special biomes are neither accidentally excluded nor overrepresented.

### Apotheosis

- [ ] Preserve the intentional tower frequency increase during baseline testing.
- [ ] Verify curated biome compatibility.
- [ ] Check actual tower candidate success.
- [ ] Measure overlap with nearby villages/towers.
- [ ] Check tower difficulty relative to early player equipment.
- [ ] Avoid making Apotheosis towers the only useful early gearing destination.

### Iron's Spells and Spellbooks

- [ ] Investigate mountain-tower embedding and poor terrain adaptation.
- [ ] Record exact structure ID and affected FTF biome.
- [ ] Determine whether issues come from start height, terrain adaptation or jigsaw behavior.
- [ ] Test modifications at multiple mountain elevations.
- [ ] Confirm tower entrances remain accessible.
- [ ] Ensure towers don't become disproportionately concentrated in vanilla mountain biomes.

### Moog structures

- [ ] Preserve verified provider selector fixes.
- [ ] Avoid blanket frequency inflation across all Moog sets.
- [ ] Check medium structures and small landmark distribution.
- [ ] Check sky/floating content.
- [ ] Keep explicitly ocean-themed variants in appropriate locations.
- [ ] Inspect structure-set duplication and intentional multi-owner cases.

### Sky structures

- [ ] Verify Sky Villages above land.
- [ ] Verify Sky Villages above rivers.
- [ ] Verify Sky Whale placement.
- [ ] Verify Frozen Whale placement.
- [ ] Check the three Heavenly Overworld clones.
- [ ] Check excessive sky height or visual invisibility.
- [ ] Check whether high structures become impractical to access at their intended progression stage.
- [ ] Check flying structures against tall FTF peaks.

## 23. Overlap and clipping investigation

- [ ] Reproduce or inspect the logged WDA monastery / CTOV alpine village / Apotheosis tower close cluster.
- [ ] Catalogue other known overlap screenshots and coordinates.
- [ ] Determine which providers actually caused candidate collisions.
- [ ] Separate overlapping placement candidates from overlapping physical bounding boxes.
- [ ] Inspect exclusion zones and their exact referenced sets.
- [ ] Check exclusion-zone directionality.
- [ ] Check shared salts only where eligible regions overlap.
- [ ] Avoid unnecessary global exclusion chains.
- [ ] Check structures partially inside mountains.
- [ ] Check floating foundations.
- [ ] Check entrances blocked by terrain.
- [ ] Check jigsaw pieces intersecting other structures.
- [ ] Check bridges and roads terminating into terrain.
- [ ] Check tall trees penetrating structures.
- [ ] Check waterlogged or submerged structures.
- [ ] Check snow/ice deposition over entrances.
- [ ] Identify whether terrain adaptation actually works with FTF heights.
- [ ] Create targeted fixes rather than globally reducing all structure generation.
- [ ] Regression-test candidate density after adding exclusions.

## 24. Measuring structure density correctly

- [ ] Use multiple fixed seeds or repeatable worlds.
- [ ] Record the actual generated area.
- [ ] Record structure category counts.
- [ ] Record counts per sampled area.
- [ ] Record vanilla versus modded biome distribution.
- [ ] Compare the same settings across versions.
- [ ] Record collisions, clipping and unsuccessful candidates where detectable.
- [ ] Keep `/locate` benchmarks separate from natural generation measurements.
- [ ] Measure ordinary chunk generation separately from structure-search time.
- [ ] Record if a structure was naturally generated, force-placed or only found by locate.
- [ ] Collect screenshots of representative successful and failed structures.

### W4 acceptance

A repeatable world survey demonstrates improved variety and representation in modded biomes without unacceptable collision rates, severe terrain clipping or excessive landmark spam. The user approves the resulting qualitative balance.

---

# PART IX — W5: Terrain, biomes and landscape composition

## 25. Curated biome verification

- [ ] Verify all intended curated donor biomes are present.
- [ ] Identify exact Nature's Spirit runtime biome IDs.
- [ ] Resolve the fourth Nature's Spirit Overworld-entry discrepancy.
- [ ] Verify RU Cold Deciduous Forest.
- [ ] Verify RU Rocky Meadow.
- [ ] Verify BOP Snowblossom Grove.
- [ ] Verify BWG Sakura Grove.
- [ ] Verify BOP Pumpkin Patch.
- [ ] Verify intentionally rare biomes remain accessible.
- [ ] Check Nature's Compass biome detection.
- [ ] Check biome availability through natural generation, not just registry existence.
- [ ] Check temperature/category classification.
- [ ] Verify Nether-only donors do not appear in Overworld compatibility tags.
- [ ] Verify cave biomes remain cave-specific.

## 26. Distribution and repetition

- [ ] Measure Prairie prevalence across multiple regions.
- [ ] Reduce excessive Prairie dominance.
- [ ] Measure Sakura Grove prevalence.
- [ ] Reduce excessive Sakura Grove dominance.
- [ ] Increase representation of other field biomes.
- [ ] Pay particular attention to Pumpkin Patch.
- [ ] Check overrepresentation of vanilla Taiga.
- [ ] Reduce vanilla Taiga area while preserving dense trees within remaining patches.
- [ ] Redistribute cold forest opportunities among curated appropriate biomes.
- [ ] Check whether large stretches repeat the same two biomes.
- [ ] Check for abrupt inappropriate biome transitions.
- [ ] Check wet-to-dry and cold-to-hot transition coherence.
- [ ] Preserve rare Volcano behavior.
- [ ] Keep Skyris Vale, Snowblossom Grove and Floral Ridges uncommon as previously intended.
- [ ] Avoid solving repetition by indiscriminately increasing biome count.
- [ ] Compare native biome sources with Biolith replacement contribution.
- [ ] Determine actual generated biome distribution rather than equating it with JSON weights.

## 27. Mountain and snowy biome overhaul

- [ ] Inspect current FTF mountain terrain.
- [ ] Identify why sufficiently large mountains seem uncommon.
- [ ] Examine mountain frequency, amplitude and shape controls separately.
- [ ] Avoid changing continent scale as a substitute for mountain tuning.
- [ ] Identify suitable curated replacements for vanilla Snowy Slopes.
- [ ] Identify suitable replacements for vanilla Jagged Peaks.
- [ ] Identify suitable replacements for vanilla Frozen Peaks.
- [ ] Check replacement biome surface blocks and decorations.
- [ ] Check snow and ice climate compatibility.
- [ ] Check vertical biome bands.
- [ ] Check mountain structure placement after replacements.
- [ ] Ensure peaks remain imposing rather than merely reskinned hills.
- [ ] Preserve usable pathways and valleys.
- [ ] Test mountain generation in multiple regions and seeds.

## 28. Coastline and ocean interface

- [ ] Disable vanilla Stony Shore from newly generated Overworld distribution.
- [ ] Choose suitable retained coastal replacements.
- [ ] Verify no missing biome IDs in the new replacement rule.
- [ ] Check cliff-to-ocean transitions.
- [ ] Check beaches at river mouths.
- [ ] Check large cliffs without awkward surface seams.
- [ ] Check stony shores are not silently reintroduced by a different biome source.
- [ ] Check ocean depth and underwater terrain variety.
- [ ] Check if land fraction remains appropriate after FTF changes.
- [ ] Check structure generation on unusual coastal terrain.

## 29. Climate zones and terrain scale

- [ ] Measure distance between climate transitions on fixed routes.
- [ ] Identify the actual FTF temperature scale settings.
- [ ] Identify moisture/humidity scale settings.
- [ ] Distinguish climate-zone size from individual biome patch size.
- [ ] Reduce oversized climate regions in controlled increments.
- [ ] Preserve coherent neighboring biome groups.
- [ ] Avoid temperature oscillation that produces visually nonsensical adjacent regions.
- [ ] Check continent-scale interactions.
- [ ] Keep river count separate from climate tuning.
- [ ] Compare multiple world seeds before declaring improvement.
- [ ] Measure effects on structure eligibility after changing biome distribution.

## 30. Biolith replacement integrity

- [ ] Verify active `ao_biome_replacement` datapack.
- [ ] Verify target format for installed Biolith version.
- [ ] Review existing twelve targeted vanilla fallback IDs.
- [ ] Verify intended 5% or 0.5% vanilla retention parameters.
- [ ] Verify temperature guards.
- [ ] Extend replacement rules for Taiga if required.
- [ ] Extend replacement rules for mountain biomes if approved.
- [ ] Extend replacement rules for Stony Shore.
- [ ] Check replacement order and competing mod placement.
- [ ] Check new biome rules don't break structure selectors.
- [ ] Rebuild from `release_030/biome-pools.json` and source scripts.
- [ ] Confirm the rule file survives restart.
- [ ] Avoid relying on `/reload` for worldgen validation.
- [ ] Test actual generated biomes in fresh chunks.

### W5 terrain acceptance

The world contains noticeably better diversity, fewer repetitive regions, improved climate transitions, larger appealing mountains, appropriate coastlines and the intended biome roster—without destabilizing structures or generation performance.

---

# PART X — Vegetation and environmental systems

## 31. Tan's Huge Trees

The existing staged plan is a starting point, not an applied change.

- [ ] Inspect actual Tan custom rule identities and installed assets.
- [ ] Check native global rarity/group controls.
- [ ] Audit all large tree families.
- [ ] Audit tree groups spawning in Prairie.
- [ ] Audit tree groups spawning in Grassland.
- [ ] Audit tree groups spawning in Flower Fields.
- [ ] Audit tree groups spawning in Pumpkin Patch.
- [ ] Audit Alpine Clearings and Floral Ridges.
- [ ] Reduce open-field tree rarity substantially.
- [ ] Reduce open-field tree grouping.
- [ ] Keep one or two chosen dense forest exceptions.
- [ ] Preserve dense remaining vanilla Taiga if desired.
- [ ] Check that excluded biomes are removed from every retained rule branch.
- [ ] Avoid duplicate rule variants simultaneously applying to a biome.
- [ ] Test `[LOCK]` persistence behavior.
- [ ] Preserve existing shapes, tree palettes and ground predicates.
- [ ] Check root/leaf clipping.
- [ ] Check trees spawning into villages, towers and bridges.
- [ ] Check group behavior on mountains and cliffs.
- [ ] Measure actual tree counts before and after.
- [ ] Measure whether reduced groups improve generation performance.
- [ ] Audit large shrubs separately from large trees.
- [ ] Preserve intended rock generation unless evidence justifies changes.

## 32. Other vegetation and environment

- [ ] Check BWG and BOP tree collisions with Tan trees.
- [ ] Check excessive vegetation in visually open biomes.
- [ ] Check feature clutter near rivers.
- [ ] Check reeds, grasses, flowers and shrubs for appropriate biomes.
- [ ] Check unusual underwater plants.
- [ ] Check tall vegetation interfering with structures.
- [ ] Review any duplicate tree variants added by multiple biome providers.
- [ ] Preserve distinctive dense and magical forests.

## 33. TRMT paths

- [x] Earlier testing confirmed that walking can develop visible TRMT paths.
- [ ] Inspect path progression speed.
- [ ] Determine whether paths appear too slowly during normal play.
- [ ] Increase effectiveness in controlled increments.
- [ ] Check paths in forests.
- [ ] Check paths across open fields.
- [ ] Check snowy and wet terrain.
- [ ] Check interaction with village paths and roads.
- [ ] Check block changes near player-built areas.
- [ ] Prevent excessive ground degradation.
- [ ] Measure server-side block update cost.
- [ ] Test behavior with multiple players repeatedly using the same route.

---

# PART XI — W6: Caves, oceans, Nether, End and dimensions

## 34. Cave systems

- [ ] Verify Alex's Caves biome generation.
- [ ] Check compatibility with FTF caves.
- [ ] Verify cave biome selectors.
- [ ] Check underground dungeon eligibility.
- [ ] Check Dungeons Crawl and other cave structures.
- [ ] Check subterranean structures at different depths.
- [ ] Check cave structure clipping with FTF terrain.
- [ ] Check cave ambience and visibility.
- [ ] Check mining/resource distribution remains sensible.
- [ ] Check mob density and pathfinding in large caves.
- [ ] Check structure entrances from the surface.
- [ ] Check caves intersecting strongholds and ancient cities.

## 35. Oceans and marine exploration

- [ ] Verify actual ocean-biome variety.
- [ ] Check ocean depth and terrain.
- [ ] Audit WDA Seven Seas.
- [ ] Audit Underwater Village.
- [ ] Audit Antique Trading Ship.
- [ ] Audit ocean-themed Moog structures.
- [ ] Check underwater ruins, ships and coastal settlements.
- [ ] Check ocean structure placement near coastline transitions.
- [ ] Check marine mob distribution.
- [ ] Check underwater loot balance.
- [ ] Check ocean structures are not accidentally treated as ordinary land buildings.
- [ ] Review Sunken Spires later, without automatically adding it.
- [ ] **Before WORLDGEN FREEZE, review/select final ocean expansion** from [researched compatibility shortlist](docs/testing/OCEAN_EXPANSION_PREFREEZE_REVIEW_2026-10-10.md). Ocean options must be settled before optimizing and selecting the permanent server seed.
- [ ] Trial **Aquamirae 7.2.10** NeoForge 1.21.1 (CF 536254:8931374) on a separate fresh seed: Ice Maze / Ship Graveyard, mob challenge, gear-difficulty option, Aquaculture/Seven Seas compatibility.
- [x] **Decision:** omit Upgrade Aquatic (Hybrid Aquatic chosen as primary ecology addition).
- [ ] **Deeper Oceans 2.0.1 is NOW INCLUDED IN COMBINED TEST**; decide keep/remove after FTF, shipwrecks, monuments and Aquamirae terrain/height tests.
- [ ] Record explicit *install/reject/park* decisions, two seeded worldgen runs, performance and oceans/coasts approval before calling the worldgen roster frozen.
- [ ] Keep significant ocean expansion separate if it threatens 0.3.x stability.

- [ ] **Combined Test 8 mandatory full checklist:** [TEST8_COMBINED_WORLDGEN_ONE_PASS_CHECKLIST.md](docs/testing/TEST8_COMBINED_WORLDGEN_ONE_PASS_CHECKLIST.md) — all new aquatic mods + dependency checks, new land biomes, coastlines, lighthouses, boss towers, bridges, Nether bastions, quest-team separation, shaders, server performance
- [ ] **Manual Better Bastions**: add exact NeoForge 1.21.1 JAR from official CurseForge project `1713723`; not yet in import manifest because exact CF file ID is unresolved. Test with Incendium, Black Spiral and Nether fortresses in fresh chunks
- [ ] **Manual NeoReefRedux**: add native NeoForge 1.21.1 Modrinth release; no confirmed CurseForge ID. Test coral terrain and Hybrid Aquatic overlaps
- [ ] Ocean loot progression: FTB Ocean Mobs offers NO default loot; write custom datapack loot tables and tune spawn/boss balance after basic registration test
- [ ] Native and custom bridges with Streams Reflowing: test generation next to both river types; fix physical height/terrain mismatch rather than doubling frequency without evidence
- [ ] Compare fresh-seed cliffs and beaches after BWG Dacite Shore replaces `minecraft:stony_shore`; watch sea structures / waterline seams

- [ ] **Dragon skeleton corpses:** sample surface chance after 0.0033333→0.0015 reduction on 2 fresh seeds; leave skeletons enabled
- [ ] **Underground cave biome testing:** verify fire and lightning caves in formerly unavailable Overworld biomes, ice caves only in cold/snowy. Surface Ice & Fire roost tags must remain native; inspect structure/worldgen logs and physical lair placement
- [ ] **Create Rustic spacing:** test barn 36/24, windmill 32/20, smithy 28/18, well 20/12 against other structure mods and villages. Lower frequency cannot guarantee no intersections
- [ ] **Midgame flight selection** (after this test): review [flight shortlist](docs/testing/MIDGAME_FLIGHT_OPTIONS_2026-10-10.md) and choose limited-flight ring, craftable Elytra, Create Flight Anchor or existing spell/mount progression without wrecking exploration balance

- [ ] **Test 8.2 P0 startup:** verify My Picture Frame `1582023` is NOT installed after importing fresh profile; check if duplicate `com.twelvemonkeys.image` Java module crash is resolved. If not, send latest.log and crash report before worldgen testing
- [ ] **Four newly pinned projects:** Hybrid API HAPI `883374:9063597`, Atlas API `1145462:6880789`, Flight Rings `401229:7782196`, MidnightLib `488090:7318664`; verify clean install and client load without Iron's Lib regression
- [ ] **Flight Ring recipe gating:** Paxi AO Flight Balance basic ring requires blaze rod, ender pearl, phantom membrane and diamond; advanced upgrade Nether Star, Netherite, Eyes of Ender, Echo Shard; verify JEI, crafting, configuration cost, multiplayer `allow-flight`
- [ ] **Private JAR inclusion:** Better Bastions and NeoReefRedux supplied JARs are now `overrides/mods` in Test8.2; verify BOTH installed once and server receives them, no duplicate files from user's old profile
- [ ] **Before PUBLIC CurseForge upload:** remove override Better Bastions JAR and reference official CF project `1713723` at correct NeoForge 1.21.1 file ID; obtain CurseForge non-CF approved-list clearance for NeoReefRedux GPL-3 before bundling, then export via CurseForge desktop
- [ ] **Original icon** supplied at `overrides/Ambient-Odyssey-Icon.png`; select manually as local CurseForge profile avatar and separately configure project artwork on website; don't assume ZIP icon is auto-applied
- [ ] **Source reproducibility:** Test8.2 private ZIP built independently from GitHub source builder, so record user-supplied JARs + icon as external input assets, rerun source generator/static validators and test actual CurseForge import first

- [x] **Actual Test8.2 runtime success:** Minecraft/NeoForge client reaches world, player joins, clean save/shutdown; duplicate Java module from My Picture Frame resolved in this instance
- [ ] **Test8.3 data corrections:** confirm in game no failed parsing for `flight_rings:smelt_basic_ring` / `smelt_advanced_ring` and JEI still shows chosen crafting recipes, plus Create Arise windmill `salt=1543892757` while Easy Structures remains native `353987075`. New world/chunks only
- [ ] **Worldgen tag blocker:** Additional Structures `skeleton_skull` tag illegally requires `minecraft:pale_garden` on MC 1.21.1; retrieve authoritative 6.3.2 tag and make value optional while preserving all other biome selections
- [ ] **Incomplete/legacy loot/visual resources:** source owner for many invalid `byg:snowdrops`, `supplementaries:quark/hanging_sign_blossom` and ItemStack `minecraft:air`; repair only proven mismatches. Iron's Jewelry loot test table, Astrological block atlas, traveloptics malformed tag, GeckoLib animations and Bumblezone trade also need technical audit
- [ ] **Structure salt triage:** do not randomize all Structure Essentials duplicate salts; only patch proven same-dimension overlap/eligibility pairs, re-evaluate Aquamirae+vanilla shipwreck shared salt and Structory three sets with source rationale
- [ ] **Performance prefreeze baseline:** FTF 2952 chunks / 7.14 real chunks/sec / 12.5% parallel efficiency; five integrated `Can't keep up` spikes up to 18.932 sec. Compare Streams Reflowing presets/prefetch, FTF, dedicated pregeneration and warm cache; preserve natural streams and final worldgen quality
- [ ] **Critical next natural worldgen feedback:** prairie/baobab/tropical/dryland, Dacite Shore and ocean floor, Deeper Oceans vs FTF, bridge-on-stream geometry, windmill/rustic overlaps, lighthouses, dragon caves, Better Bastions/End transitions. Do not declare worldgen frozen based on successful client startup

## 36. Nether

- [ ] Check Incendium and existing Nether biome systems.
- [ ] Check Nether biome compatibility with retained mods.
- [ ] Verify Nether-specific structure placement.
- [ ] Verify YUNG's Better Nether Fortresses.
- [ ] Check Nether-only Farmers Structures variants.
- [ ] Check structure accessibility in extreme terrain.
- [ ] Check fortress/bastion replacement ownership.
- [ ] Verify Explorify Black Spiral is disabled after integration.
- [ ] Check mob and boss difficulty.
- [ ] Check portal generation and return positions.
- [ ] Check Nether chunk-generation performance.

## 37. End

- [ ] Audit BetterEnd and installed End expansions.
- [ ] Check End biome/layer configurations.
- [ ] Audit Astrological upper/middle/lower layer distribution.
- [ ] Check Moog's End Structures.
- [ ] Check Echoes of the End.
- [ ] Check End Villager Outpost.
- [ ] Check YUNG's Better End Island.
- [ ] Check TotW structure heights; investigate earlier very-low-Y behavior.
- [ ] Check End City overhaul ownership and duplicates.
- [ ] Check Cataclysm End structures.
- [ ] Check End structures intersecting void areas or wrong heights.
- [ ] Check End Remastered eye-hunt integration.
- [ ] Check eye/portal progression is achievable without excessive forced grinding.
- [ ] Check natural structures after long-distance End travel.
- [ ] Check End chunk-generation performance.
- [ ] Keep dragon fight balance for the later combat phase unless a technical failure blocks progression.

## Later major ocean-themed content and dimensions (NOT part of worldgen freeze Test 8)

- [ ] **Beyond the Ocean**: user-approved for a **later content/dimension expansion audit**; evaluate the two dedicated oceans, post-End progression, leviathans, bosses, vehicles and performance only after current worldgen freezes. Do NOT add it to the 0.3.8 manifest or claim it has been tested
- [x] **Explicit exclusions from 0.3.8 ocean roster:** Tide 2, Sea Myths, Create: Deep Seas and Upgrade Aquatic. Keep Create Aeronautics / Sable physics and Sunken Spires deferred

## 38. Other dimensions

For each installed significant dimension:

- [ ] Verify portal/entry method.
- [ ] Verify return travel.
- [ ] Verify biome generation.
- [ ] Verify natural structures.
- [ ] Verify mob spawning.
- [ ] Verify loot/item registration.
- [ ] Verify structures do not reference unavailable blocks.
- [ ] Verify dimensional spawn protection.
- [ ] Check quest and progression access.
- [ ] Check dimension unload/reload.
- [ ] Check performance and persistent memory after returning to Overworld.

Especially check existing Aether, Twilight Forest, Bumblezone, Undergarden, Pasterdream and other installed major dimensions.

Do not assume that candidate dimensions such as Mine Cells or Blue Skies are already installed.

---

# PART XII — W7: Technical compatibility and cleanup

## 39. Recipes and item registries

- [x] Inspect Cataclysm Spellbooks 1.1.14 recipes.
- [ ] Identify every missing registry key.
- [ ] Determine whether items are absent, renamed or incorrectly gated.
- [ ] Check its Mechanical Weapon Parts recipes.
- [ ] Check Gauntlet of Gatling references.
- [ ] Check Combuster references.
- [ ] Check Excel upgrade recipes.
- [ ] Check relevant loot modifiers.
- [ ] Apply valid fixes rather than fabricating items.
- [ ] Confirm no recipe parsing errors after reload.
- [ ] Check JEI visibility.
- [ ] Confirm the fixed Simply More `matterbane_clean` recipe still loads.
- [ ] Check other invalid recipes in the runtime log.
- [ ] Test Create/BWG milling integration.
- [ ] Confirm the existing 78 native + 18 custom milling inputs remain available.
- [ ] Check missing outputs from removed mods.
- [ ] Check recipe conflicts across Farmer's Delight addons.
- [ ] Check recipe outputs requiring nonexistent items or blocks.

## 40. Loot and reward hygiene

- [ ] Confirm the disabled Alex's Mobs seal_reward table behaves as intended.
- [ ] Confirm seals themselves remain available.
- [ ] Check unwanted loot from removed mods.
- [ ] Check structure chest loot registration.
- [ ] Check loot modifiers for invalid item keys.
- [ ] Check boss drops exist.
- [ ] Check rare loot isn't accidentally made common by new structures.
- [ ] Check treasure maps and structure locators.
- [ ] Check Lootr compatibility with generated modded containers.
- [ ] Check empty or broken chest loot pools.
- [ ] Preserve major loot-economy balancing for the RPG progression phase.

## 41. Curios, Artifacts and Enigmatic Legacy+

- [ ] Verify all native Artifacts Curios slot memberships.
- [ ] Verify RAR-Compat does not erase them at runtime.
- [ ] Verify Enigmatic coloured amulets.
- [ ] Verify named amulets.
- [ ] Verify `the_necklace`.
- [ ] Verify Darkest Scroll.
- [ ] Verify the intended scroll slot.
- [ ] Check duplicated Curios slot categories.
- [ ] Check missing items or invalid slot acceptance.
- [ ] Check slot behavior after relog.
- [ ] Check multiplayer synchronization.
- [ ] Check tooltip descriptions.
- [ ] Check interaction with cosmetic armor and other accessory systems.
- [ ] Preserve existing successful overlay behavior while fixing individual failures.

## 42. Mod removals and dangling references

- [ ] Confirm Companions! absence from manifest and installed mod folder.
- [ ] Confirm Modern Companions absence.
- [ ] Remove any orphaned configs from those mods.
- [x] Confirm Born in Chaos removal has been incorporated into the next export.
- [ ] Search questbook for Born in Chaos items and entities.
- [ ] Search loot tables for removed-mod IDs.
- [ ] Search recipes for removed-mod IDs.
- [ ] Search structure templates for required missing blocks/entities.
- [ ] Search tags for removed-mod required references.
- [ ] Check optional resource packs relying on removed mods.
- [ ] Avoid deleting harmless legacy config files if they have no effect unless cleanup is intentional and documented.

## 43. Rendering, resources and client-side warnings

- [x] Compile four verified Traveloptics entity-tag repairs, 33 model JSON repairs and a format-34 Paxi client resource pack.
- [ ] TEST: Traveloptics dynamic rendering/visual appearance; absent `augment_test_wild` and `test_augment` models remain unresolved.
- [x] Gate eleven Cataclysm Spellbooks recipes referencing absent registered items and provide the existing cursed-pyramid loot modifier at the missing prison reference ID; preserve native payloads.
- [ ] TEST: recipe/loot registry loading and remaining animation/loot-function warnings.

- [x] Inspect Traveloptics missing models/tags.
- [ ] Inspect Cataclysm Spellbooks animation warnings.
- [ ] Inspect GeckoLib unsupported geometry versions.
- [ ] Identify warnings that are merely cosmetic.
- [ ] Identify warnings affecting actual gameplay.
- [ ] Check main menu rendering.
- [ ] Keep unwanted Pasterdream inventory GUI disabled.
- [ ] Check modded inventory background/resource layers.
- [ ] Check JEI rendering, search and recipe overlays.
- [ ] Check missing texture/pink-and-black models.
- [ ] Check shader compatibility only after baseline rendering works.
- [ ] Check audio and ambience reload warnings.
- [ ] Check incorrect resource-pack priority.
- [ ] Check dimension-change resource reload behavior.
- [ ] Check whether resource errors worsen load time.

## 44. Wildlife and unwanted mobs

- [ ] Inventory every installed wildlife/ambient mob provider.
- [ ] Check Alex's Mobs biome-spawn tags.
- [ ] Identify actual Fly entity/config toggles.
- [ ] Disable flies as requested.
- [ ] Identify any similarly unwanted insects.
- [ ] Keep harmless bees and butterflies unless explicitly rejected.
- [ ] Check entity spawning from natural biomes.
- [ ] Check spawning from structures and spawners.
- [ ] Check eggs, summons and alternate spawn routes where important.
- [ ] Check mob density in curated biomes.
- [ ] Check ocean and cave fauna.
- [ ] Check flying mobs and pathfinding cost.
- [ ] Check animation/AI crashes.
- [ ] Check biome wildlife variety.
- [ ] Check spawn limits when several mob mods overlap.
- [ ] Test wildlife performance under long exploration sessions.

## 45. Existing questbook and keybind smoke checks

This is not the final 0.6.x questbook overhaul.

- [ ] Confirm FTB Quests opens.
- [ ] Confirm inherited quests remain present.
- [ ] Check missing icons.
- [ ] Check recipe/item task references to removed mods.
- [ ] Check known Apotheosis gem filter problems.
- [ ] **REQUIRED: Individual quest completion for every player, even when members share an FTB Teams party.** Player A completing a task must NOT complete it for player B. Preserve FTB Chunks shared claims/party collaboration. Test with two real players on a dedicated server.
- [ ] Do not mistake `default_reward_team:false` in `config/ftbquests/quests/data.snbt` for private progress: it only controls team reward distribution; vanilla FTB Quests shares progress in teams. No proven built-in switch.
- [ ] Evaluate **Solo Quests 1.1.2** (NeoForge 1.21.1, CurseForge `1644371:8614631`): separate progress for party members, `teamSyncEnabled=false` prevents voluntary resync, **but author reports it does not work in integrated/LAN worlds**. Test API compatibility with FTB Quests 2101.1.36 and backup world quest data before any migration. Do not install to the current public build before dedicated-server acceptance.
- [ ] Alternative if per-quest mixed shared/solo progression is wanted: research NoreQuests + NoreTeams, **not** a trivial setting—it replaces/hides FTB Teams controls and may alter FTB Chunks workflows.
- [ ] Check group/team quest synchronization under the final chosen individual-progress implementation.
- [ ] Check rewards that grant invalid items.
- [ ] Check WDA questline integration.
- [ ] Check starter chapters don't force missing content.
- [ ] Check all major required menu keybinds are usable.
- [ ] Check combat and spellbook keybind conflicts.
- [ ] Check map and JEI search interaction.
- [ ] Preserve future detailed tutorial work for 0.6.x.

---

# PART XIII — W8: Performance, stability and server readiness

## 46. Establish a proper benchmark baseline

Test at consistent render/simulation settings, including:

- 8 render / 6 simulation.
- 14 render / 12 simulation, where hardware allows.

Record:

- [ ] Cold startup duration.
- [ ] Warm startup duration.
- [ ] Main-menu stabilization.
- [ ] First world creation.
- [ ] Fresh-world initial spawn stabilization.
- [ ] Save/reload duration.
- [ ] New terrain generation.
- [ ] Previously generated terrain traversal.
- [ ] Fresh Nether generation.
- [ ] Fresh End generation.
- [ ] Dimension return and memory recovery.
- [ ] Stable-scene FPS.
- [ ] Frame-time spikes.
- [ ] Garbage-collection pauses.
- [ ] CPU utilization.
- [ ] GPU utilization.
- [ ] Heap/RAM usage.
- [ ] Server tick time.
- [ ] Disk/cache growth.
- [ ] Structure locate duration separately.

Use identical seeds and repeatable routes for comparison wherever possible.

## 47. FreeTerraForged and Streams performance

- [ ] Reproduce the Streams terrain-height fallback warning.
- [ ] Determine the phase during which FTF terrain/cache data is unavailable.
- [ ] Profile terrain preparation and stream scanning.
- [ ] Compare first generation with cached generation.
- [ ] Identify unusual synchronous work.
- [ ] Check whether Streams creates large early generation stalls.
- [ ] Check river layout correctness.
- [ ] Check FTF height calculations in tall mountains.
- [ ] Check whether a configuration change can solve measured issues.
- [ ] Avoid replacing the bridge based solely on class-name speculation.
- [ ] Verify no fix changes terrain determinism unintentionally.

## 48. Structure performance

- [ ] Measure generation cost with existing structures.
- [ ] Measure after adding the eight new mods.
- [ ] Profile large jigsaw assemblies.
- [ ] Check excessive structure-search retries.
- [ ] Check very dense exclusion graphs.
- [ ] Check rare giant structures.
- [ ] Check memory pressure from simultaneous structure generation.
- [ ] Check `/locate` performance independently.
- [ ] Check crashes/timeouts from particularly problematic structures.
- [ ] Check entity/NBT-heavy generated buildings.
- [ ] Check if significant generation slowdown occurs in specific biomes or dimensions.
- [ ] Compare performance with the Test 5 baseline.

## 49. Optimization stack

Current intended foundation includes ModernFix, FerriteCore, Embeddium, ImmediatelyFast, Lithium and ServerCore.

- [ ] Verify their installed versions.
- [ ] Check overlap and redundant features.
- [ ] Review actual runtime optimization warnings.
- [ ] Profile before adding more optimization mods.
- [ ] Evaluate Entity Culling only if not already installed and useful.
- [ ] Evaluate BadOptimizations separately.
- [ ] Evaluate Create Better FPS separately.
- [ ] Consider Nitro Performance only in an isolated test.
- [ ] Avoid stacking optimizers with overlapping mixins without compatibility evidence.
- [ ] Avoid inferring better performance from higher FPS alone.
- [ ] Retest startup, rendering and generation after each optimization change.
- [ ] Remove candidates that worsen stability.

## 50. Memory and client behavior

- [ ] Revisit the older 90% / ~9.2 GB memory warning as an investigation, not proof of a leak.
- [ ] Measure settling after large generation bursts.
- [ ] Measure garbage collection.
- [ ] Test recommended 8 GB allocation.
- [ ] Test whether 8 GB is sufficient over long sessions.
- [ ] Check excessive allocation versus system RAM.
- [ ] Test lower-end PCs.
- [ ] Test very powerful PCs with unexpected stutters.
- [ ] Investigate client-specific rendering stalls separately from server TPS.
- [ ] Check shader activation/deactivation.
- [ ] Check biome-specific particle load.
- [ ] Check large entity gatherings.
- [ ] Check inventory/menu-induced frame stalls.
- [ ] Avoid declaring memory leaks based on temporary heap peaks.

## 51. Distant Horizons

- [ ] Establish stable base worldgen benchmark first.
- [ ] Verify DH and current rendering mod compatibility.
- [ ] Test DH enabled without shaders.
- [ ] Test shader integration separately.
- [ ] Test LOD generation load.
- [ ] Test LOD cache growth.
- [ ] Confirm distance rendering is actually visible.
- [ ] Check terrain seams and missing LODs.
- [ ] Check DH generation versus normal chunk-generation competition.
- [ ] Determine sensible defaults for lower-end players.
- [ ] Consider server-side LOD approaches only if useful and supported.

## 52. Dedicated server

- [ ] Build a dedicated NeoForge server profile from the actual locked pack.
- [ ] Identify client-only mods and assets.
- [ ] Confirm server startup.
- [ ] Confirm mod registry agreement.
- [ ] Confirm datapack consistency.
- [ ] Confirm player joining.
- [ ] Confirm correct server-side structure generation.
- [ ] Check chunk loading and unloading.
- [ ] Check different dimensions.
- [ ] Check death/relogin.
- [ ] Check inventories and accessories.
- [ ] Check FTB Teams/Chunks/Quests synchronization.
- [ ] Check Lootr multiplayer behavior.
- [ ] Check Waystones across players and dimensions.
- [ ] Check voice chat where configured.
- [ ] Check multiplayer permissions and commands.
- [ ] Check server crash recovery.

## 53. Pregeneration and multiplayer load

- [ ] Freeze worldgen settings before final pregeneration.
- [ ] Choose a compatible pregeneration tool.
- [ ] Determine initial generation radius from observed performance/storage.
- [ ] Do not assume a 20,000-block radius is required.
- [ ] Estimate disk size.
- [ ] Test safe interruption and resumption.
- [ ] Check pregeneration impact on memory/CPU.
- [ ] Confirm already-generated chunks remain consistent.
- [ ] Check server startup after pregen.
- [ ] Test one player exploring new terrain.
- [ ] Test two players exploring separate directions.
- [ ] Test 5–7 players spread across different regions.
- [ ] Test multiple dimension exploration.
- [ ] Test combat while other players are generating terrain.
- [ ] Check TPS and chunk delivery.
- [ ] Check network bandwidth and join/login stability.
- [ ] Check simultaneous world saves.
- [ ] Confirm backup creation.
- [ ] Test recovery from a deliberately stopped test server.
- [ ] Verify FTB Backups or the chosen backup mechanism.

### W8 acceptance

The pack demonstrates repeatable, acceptable performance and stability on representative hardware and a dedicated server. Any known limitations are documented, and recommended settings match measured behavior.

---

# PART XIV — W9: Quality assurance and release preparation

## 54. Mandatory final regression

- [ ] Fresh installation from the exact proposed export.
- [ ] Minecraft launches without fatal errors.
- [ ] New world creates successfully.
- [ ] World reloads successfully.
- [ ] Curated biome pool operates.
- [ ] Important structure categories generate.
- [ ] No unwanted Coliseum/Blimp.
- [ ] No unwanted Explorify Black Spiral.
- [ ] Farmers Structures appear appropriately.
- [ ] Sky structures remain functional.
- [ ] Caves and major dimensions work.
- [ ] Major portals work.
- [ ] Basic combat works.
- [ ] Basic crafting works.
- [ ] JEI works.
- [ ] Create recipes work.
- [ ] Curios and Artifacts work.
- [ ] FTB Quests opens and saves.
- [ ] Maps and Waystones work.
- [ ] Inventories and backpacks work.
- [ ] No severe missing textures.
- [ ] No major unexpected recipe-loading errors.
- [ ] No missing required registries.
- [ ] No repeated fatal worldgen warnings.
- [ ] No major unacknowledged structure corruption.
- [ ] No unacceptable new performance regression.
- [ ] Dedicated server starts and players can connect.
- [ ] Fresh-chunk generation is acceptable.
- [ ] A save/restart/rejoin cycle works.

## 55. Technical packaging

- [ ] Verify exact Minecraft version.
- [ ] Verify exact NeoForge version.
- [ ] Verify all mod project/file pins.
- [ ] Verify dependencies.
- [ ] Verify no obsolete mod entries.
- [ ] Verify no unapproved extra mods.
- [ ] Verify intended configs are shipped.
- [ ] Verify scripts and generated datapacks are in the correct paths.
- [ ] Verify only intended default options and GUI settings are active.
- [ ] Verify no temporary test files are included.
- [ ] Verify export ZIP CRC.
- [ ] Verify unique safe ZIP member paths.
- [ ] Verify `manifest.json` at ZIP root.
- [ ] Verify `overrides/` directory.
- [ ] Verify no unintended bundled third-party mod JARs.
- [ ] Verify correct CurseForge metadata.
- [ ] Verify source archive rebuilds the exact export.
- [ ] Generate final SHA-256 checksums.
- [ ] Record mod count and installed versions.
- [ ] Produce final changelog.
- [ ] Produce source/version history.
- [ ] Produce installation notes.
- [ ] Produce known-issues list.
- [ ] Produce server-specific instructions.
- [ ] Check licenses and distribution permissions.
- [ ] Verify that the exact ZIP intended for upload is the one tested.

## 56. User experience acceptance

Before closing 0.3.x, evaluate the following subjectively but with recorded examples:

- [ ] Exploring the Overworld feels worthwhile.
- [ ] Biomes have distinct visual identities.
- [ ] Prairie and Sakura no longer dominate the experience.
- [ ] Modded biomes are not barren of buildings.
- [ ] Structures feel varied rather than duplicated.
- [ ] Large landmarks remain special.
- [ ] Mountains and coastlines look attractive.
- [ ] Forest/open-field vegetation is appropriately distributed.
- [ ] Sky structures are meaningfully discoverable.
- [ ] Rivers feel natural.
- [ ] There are few obviously broken generation artifacts.
- [ ] Players can understand the basic survival and early gearing loop.
- [ ] Major UI problems are not intrusive.
- [ ] Multiplayer exploration remains enjoyable.
- [ ] Performance problems do not dominate the experience.

**User feedback on the overall experience is an explicit acceptance input.**

---

# PART XV — Failure-response playbook

## 57. If the game crashes during startup

1. Preserve the complete log and crash report.
2. Identify the first causal error, not only the final shutdown exception.
3. Determine whether it is a dependency, missing registry, class-loading issue, mixin conflict, config decode or resource load.
4. Compare against the untouched Test 5 baseline.
5. Isolate newly added mods or changes in small groups if required.
6. Do not remove multiple unrelated mods simultaneously.
7. Apply the smallest evidence-backed fix.
8. Relaunch and check the full log for remaining issues.
9. Preserve a record of the exact fix and file/version involved.

## 58. If the world takes extremely long to generate

1. Determine whether the game is still processing rather than crashed.
2. Check CPU activity, memory and watchdog messages.
3. Identify chunk-generation phase.
4. Separate terrain work from structures, streams, decoration and entities.
5. Use Spark or bounded profiling where possible.
6. Check large synchronous scans.
7. Check whether the problem occurs only during first generation.
8. Repeat in the untouched baseline.
9. Avoid removing the entire terrain stack before identifying the bottleneck.

## 59. If structures are missing

1. Confirm the mod loads.
2. Confirm structure registry entry exists.
3. Confirm structure-set membership.
4. Confirm enabled toggles.
5. Confirm dimension.
6. Confirm actual biome eligibility.
7. Confirm generation height.
8. Confirm spacing/frequency.
9. Confirm exclusions.
10. Confirm terrain adaptation.
11. Confirm the template pool and assets are valid.
12. Confirm the target area contains fresh chunks.
13. Use locate as a diagnostic, not a density result.
14. Conduct natural-generation testing.
15. Only then adjust frequency.

## 60. If structures overlap

1. Record exact structures and coordinates.
2. Identify native and AO placement owners.
3. Inspect actual bounding boxes.
4. Inspect structure-set salts.
5. Inspect exclusions and generation priority.
6. Check whether conflicts occur in the same biome/dimension.
7. Check whether a terrain adaptation problem mimics overlap.
8. Apply targeted exclusions or placement changes.
9. Ensure the fix does not suppress ordinary building variety.
10. Retest with multiple seeds.

## 61. If custom biomes are too frequent or rare

1. Confirm biome ID.
2. Confirm native mod generation.
3. Confirm Biolith replacement settings.
4. Confirm climate constraints.
5. Confirm FTF terrain/climate source.
6. Measure actual generated area.
7. Compare multiple seeds.
8. Change one responsible subsystem at a time.
9. Regenerate new areas/worlds.
10. Recheck structure eligibility after adjustment.

## 62. If FPS or TPS collapses

1. Identify client FPS versus server tick slowdown.
2. Determine whether fresh chunks are being generated.
3. Separate GPU, CPU, Java heap and disk activity.
4. Check shaders and resource effects.
5. Check entities and mob AI.
6. Check synchronous structure or terrain work.
7. Compare with the known baseline.
8. Profile rather than guessing.
9. Apply one optimization at a time.
10. Repeat identical tests.

## 63. If a fix causes new problems

1. Revert to the previous known-good source state.
2. Identify the exact change that caused the regression.
3. Reproduce it in a minimal test.
4. Keep test logs and diff.
5. Amend the patch rather than layering additional speculative fixes.
6. Add a regression check for the failure.
7. Document the incident in the development log.

---

# PART XVI — Test matrix and evidence standards

## 64. Test types

Every subsystem should receive the tests relevant to it.

| Test | Purpose |
|---|---|
| Static JSON/metadata | Verify syntax and declared references |
| Source build | Verify reproducibility |
| Registry load | Confirm actual Minecraft loading |
| Forced placement | Inspect template assembly |
| Natural generation | Verify placement behavior |
| Biome coverage | Confirm eligibility in actual biome IDs |
| Density survey | Measure distribution rather than nearest examples |
| Collision survey | Observe overlap and clipping |
| Fresh-world test | Validate current worldgen rules |
| Save/reload test | Catch persistence/registry issues |
| Dedicated-server test | Verify server compatibility |
| Multiplayer test | Verify concurrent behavior |
| Performance benchmark | Compare measured generation and gameplay cost |
| Regression test | Ensure existing behavior remains intact |

## 65. Minimum test record

For each significant issue or fix, record:

- Test ID.
- Date.
- Build identifier.
- Mod/configuration versions.
- Seed.
- Dimension.
- Biome ID.
- Coordinates.
- FTF preset.
- Relevant game settings.
- Expected behavior.
- Actual behavior.
- Steps to reproduce.
- Screenshot/video where useful.
- Log excerpt or full log filename.
- Pass/fail/untested status.
- Fix applied.
- Retest result.

## 66. Test integrity rules

- [ ] Never mix observations from two builds without naming them.
- [ ] Never compare fresh worldgen against an already generated area as if both used current settings.
- [ ] Never report intended probabilities as actual observed density.
- [ ] Never report a static check as a gameplay success.
- [ ] Never claim a missing-JAR audit is complete without inspecting that JAR.
- [ ] Never claim a mod addition is installed because it was approved.
- [ ] Never silently alter the biome roster.
- [ ] Never hide warnings by inventing meaningless empty assets.
- [ ] Never lose the exact package that produced a test log.
- [ ] Never overwrite the known-good baseline without a rollback.

---

# PART XVII — Dependency map

## 67. Work that can happen in parallel

**Independent workstreams:**

- Auditing available JAR resources.
- Researching the eight approved mod versions.
- Reviewing CTOV and other missing asset references.
- Reviewing Cataclysm Spellbooks registry errors.
- Designing benchmark routes.
- Preparing wildlife-spawn inventories.
- Reviewing current quest/keybind problems.
- Maintaining build validation scripts.

**Work that should remain sequential:**

1. Source reproducibility before editing release outputs.
2. Initial runtime smoke test before claiming Test 5 accepted.
3. Mod dependency verification before adding new mods.
4. Structure registry audit before large-scale density changes.
5. Biome and terrain tuning before final structure density acceptance.
6. Content/configuration freeze before serious pregeneration.
7. Server benchmark after the current candidate build is assembled.
8. Final validation after the final source changes.
9. Release packaging only from the accepted candidate.

If later worldgen changes affect previously tested structure placement, repeat the relevant structure acceptance checks.

---

# PART XVIII — Exit gate: 0.3.x → 0.4.0

## 68. Mandatory conditions

### Worldgen

- [ ] FTF preset accepted.
- [ ] Curated biome roster functioning.
- [ ] Biome distribution accepted.
- [ ] Mountain and coastal composition accepted.
- [ ] Climate transitions accepted.
- [ ] Open-field tree distribution accepted.
- [ ] Rivers/Streams behavior accepted.
- [ ] No critical terrain generation errors.

### Structures

- [ ] Eight approved additions integrated or individually documented as blocked by a real incompatibility.
- [ ] Farmers Structures density work completed.
- [ ] Major modded-biome structure gaps addressed.
- [ ] Small/medium structure variety accepted.
- [ ] Large landmark rarity accepted.
- [ ] Sky structure generation accepted.
- [ ] Known severe CTOV/IDAS asset issues resolved where possible or explicitly documented.
- [ ] No unacceptable recurring structure collisions.
- [ ] No critically broken major structures.
- [ ] Nether/End and ocean structure systems are functional at the current scope.

### Technical integrity

- [ ] Critical registry failures resolved.
- [ ] Important recipe and item errors resolved.
- [ ] Important Curios/Artifacts issues resolved.
- [ ] Unwanted removed mods absent from the release.
- [ ] Datapacks and manifest consistent.
- [ ] Reproducible build.
- [ ] Passed full static validation.
- [ ] Passed launch/world/reload smoke tests.

### Performance

- [ ] Client performance acceptable in normal gameplay.
- [ ] Fresh chunk generation acceptable.
- [ ] Memory behavior acceptable for the target recommendation.
- [ ] Dedicated server launches.
- [ ] Concurrent player testing completed at representative load.
- [ ] No known severe persistent tick or chunk-generation blocker.
- [ ] Server backup strategy tested.

### Release preparation

- [ ] Accepted exact CurseForge export.
- [ ] Correct `manifest.json`.
- [ ] Source/archive hashes recorded.
- [ ] Changelog completed.
- [ ] Known issues documented.
- [ ] Installation and server instructions available.
- [ ] User approves overall worldgen/exploration experience.

**0.4.0 entry rule:** All critical gates pass. Noncritical issues may carry forward only if explicitly documented, assigned a future version and judged acceptable.

---

# PART XIX — 0.4.x preview (not required before entering 0.4.0)

Once the foundation passes:

### Living world and ecology

- Wildlife and ecosystems.
- Marine life and cave fauna.
- Settlement NPC behavior.
- More meaningful professions and villages.
- Farming, cooking and fishing exploration rewards.

### Content expansion

- Additional caves and ocean encounters.
- Selected structure/dimension content after testing.
- Environmental puzzles and secrets.
- Archaeology and collectibles.
- Distinctive late-game locations.

### Quality of life

**Confirmed 10 Oct discovery feature approval:** Every feature proposed in the prior exploration discussion is approved for the **future design backlog**, including title overlays, silent personal journal, segmented percentages, found-versus-cleared state, explorer ranks, rare discoveries, expedition history, optional screenshots, private/team records, bookmarks, safety and preparedness tools, family/dimension collections, and atlas integration. Exact mod installs, datapacks, and UI choices are NOT automatically approved. [Full inventory and new brainstorming candidates](docs/audits/EXPLORATION_DISCOVERY_SYSTEM_PROPOSAL_2026-10-10.md).
- [ ] **NEW expedition gameplay research queue:** Explorer's Guild optional contracts; rumors, treasure charts and clue chains; scenic Natural Wonders; Discovered → Conquered → Mastered system; themed regional collections; biome ecology notes; boss tier reconnaissance; group expedition itinerary; exploration trophies/museum; linked lost-expedition lore; limited Explorer's Compass; privacy-preserving atlas export; world-first memorial; return markers and expedition condition checklists. These new ideas await prioritization, are NOT approved releases.
- [ ] **Structure locator balancing:** Nature's Compass already installed (252848:7892954) to locate biomes. Explorer's Compass NeoForge 1.21.1 (491794:7892943) is only a candidate; gate/blacklist rare bosses if trialed to preserve exploration.

**10 Oct exploration discovery/QoL concept — audit only:** [Exploration title and journal system design](docs/audits/EXPLORATION_DISCOVERY_SYSTEM_PROPOSAL_2026-10-10.md). Do not install into Test8.3 or alter the current frozen-by-process Test8.2 working profile.
- [ ] **Discovery titles:** research Traveler's Titles native NeoForge 1.21.1 for biomes/dimensions; audit exact 1.21.1 NeoForge First Steps structure-title file and multiplayer reliability; tune high-level structure vs biome title precedence, border debouncing, sounds, accessibility and disabling repeat toasts.
- [ ] **Player exploration checklist:** prototype FTB Quests 1.21.1 built-in **Visit Biome** and **Find Structure** tasks (two vanilla + two modded) and verify per-player data with FTB Solo Quests in a two-player test. Separate biome type visits, major structure type discovery and dungeon clear completion; record dimension.
- [ ] **Tracking engine decision:** compare mature built-in FTB Quests progress, silent `minecraft:location` advancements from an AO registry-generated datapack, and **Explorer's Journals** 1.0.0 NeoForge prototype (new/low adoption). Prefer native components if complete; no bespoke Java mod until limitations are proven.
- [ ] **Explorer percentage and UI:** list only reachable active biome/major-structure IDs, exclude inactive/duplicate/decorative templates; optional rare feats separate; persistence after restart/pack updates; spoiler-safe filters; per-player vs team; configurable notifications; no automated coordinate leak to public site.
- [ ] **Explorer upgrades:** revisit bookmarks for *already found* POIs without duplicating Xaero, optional first-discovery attribution, region-based milestones, lore/field notes, recap and eventual wiki integration. Never make exploration completion a forced prerequisite to main progression.



**10 Oct post-worldgen QoL/visual audit:** [Complete candidate list and exact Voxy/DH/BBE renderer comparison](docs/audits/QOL_VISUAL_RENDERING_BACKLOG_2026-10-10.md). **Research only: none approved for Test8.2 installation.**
- [ ] **Convenience/UI shortlist:** AmbientSounds, BetterF3, Fadeless, Lanterns Belong on Walls, Smooth Swapping, Controlling, Better Statistics Screen, RightClick Harvest, Status Effect Bar, Cut Through, Light Overlay, Screenshot Viewer, Paginated Advancements, Reach Around, Map Distance Fix
- [ ] **World visuals and agriculture:** Dynamic Lights (not merely `lambdynlights_api`), Simple Fog Control, Visual Snowy Leaves, Crops Love Rain; measure weather/crop/spawn changes and integrated-server tick costs
- [ ] **NEW 10 Oct QoL candidate batch (research only, no install):** Armor GUI [exact mod identity TBD]; Cave Dust / Cave Dust Rethinking; Subtle Effects; Continuity for connected glass [Embeddium/NeOculus A/B]; Pick Up Notifier; Better Advancements; Allmobheads / likely All The Heads. Detailed candidate identities, 1.21.1 references and overlap gates: [QoL/visual audit](docs/audits/QOL_VISUAL_RENDERING_BACKLOG_2026-10-10.md).
- [ ] **Advancement UI choice:** compare Better Advancements against already-listed Paginated Advancements. Pick at most one vanilla advancement screen overhaul and separately verify FTB Quests.
- [ ] **HUD and visual overlap:** Armor GUI identity vs Better Inventory/Cosmetic Armor/Curios; Pick Up Notifier vs pickup/status overlays; Cave Dust plus Subtle Effects vs Particular/Better Smoke; Continuity glass vs Embeddium/NeOculus/shaders. Profile FPS, VRAM, keybinds and UI stacking.
- [ ] **Mob-head collectibles:** confirm whether the intended Allmobheads is Fuzs' All The Heads; assess loot-table changes, Lootr, heads from modded mobs, server requirement and collection balance. Treat as content/gameplay addition, not client-only decoration.
- [ ] **Zoomify conditional:** first inspect installed Xaero/NeOculus/Embeddium controls and any existing zoom key; only add Zoomify if actually missing
- [ ] **APPA resource/texture pack:** exact project unknown; get canonical link/name before deciding or redistributing
- [ ] **BBE native NeoForge 1.21.1 (not Fabric-only Enhanced Block Entities):** official v1.3.4 file `1434533:8888765`, but requires matching Sodium API/render path. **Do not simply install onto current Embeddium 1.0.15 / NeOculus 1.8.7**. Benchmark alongside shader/texture compatibility after freeze
- [ ] **Voxy vs Distant Horizons A/B:** official DH on NeoForge 1.21.1 vs specific community Voxy fork with Sodium 0.8.x/Iris where required; shader-by-shader Solas and Complementary tests, cold/warm cache, GPU extension support, FTF/Streams and Nether/End visuals. **Never mix DH and Voxy by default**
- [ ] Post-worldgen QoL install waves: (1) UI/accessibility, (2) minor mechanics/ambience, (3) heavyweight rendering/LOD/BBE only after benchmarks, with 1.21.1 NeoForge file ID/licence/sidedness checks and CurseForge export gate


- Inventory handling and sorting.
- Searchable keybind menu.
- Keybind-conflict cleanup.
- Improved maps and navigation.
- Improved multiplayer convenience.
- Container and backpack integration.
- Accessible tooltips and interaction feedback.

### Later phases still separate

- Main RPG skill-tree architecture.
- Full boss/superboss balance.
- Apotheosis/Relics/Artifacts equipment economy.
- Complete FTB Quests architecture.
- Extensive keybind tutorial questline.
- Full GUI/HUD overhaul.
- Final public-release branding and documentation.

---

# PART XX — Operating procedure for future ChatGPT sessions

## 69. Before starting work

1. Read this master TODO.
2. Read the latest development TODO and changelog.
3. Identify the current source archive and exact build.
4. Check whether any tasks were completed since this document's last update.
5. Distinguish user-approved changes from suggestions.
6. Identify which systems the planned task touches.
7. Identify relevant dependencies and regression tests.
8. Create a backup/source checkpoint.

## 70. During implementation

1. Work from editable source inputs.
2. Preserve unrelated settings.
3. Make changes in controlled groups.
4. Record the reason for every nontrivial change.
5. Update source-specific tests.
6. Check generated outputs.
7. Record evidence.
8. Avoid marking runtime work complete before testing.
9. Note newly discovered dependencies or risks.
10. Maintain an exact list of changed files.

## 71. After implementation

1. Rebuild.
2. Run static validation.
3. Perform the relevant runtime tests.
4. Compare against baseline behavior.
5. Verify no related regression.
6. Update status checkboxes.
7. Update changelog.
8. Update outstanding issues.
9. Save new artifact hashes.
10. Decide whether the next development wave is unblocked.

## 72. Session progress entry template

**Date:**  
**Build/source version:**  
**Wave:**  
**Task IDs addressed:**  
**Files changed:**  
**New mods added/removed:**  
**Configuration changes:**  
**Tests performed:**  
**Passed tests:**  
**Failed tests:**  
**Problems discovered:**  
**Items still unverified:**  
**Next recommended action:**  
**Rollback available:** Yes / No

---

# PART XXI — Immediate next-session action plan

Current completed work supersedes the original next-session sequence below: W0 reproduction, the available W2 JAR audit, expanded catalogues, Farmers candidate settings and verified compatibility repairs are complete at the static level. Next, supply/audit the 41 missing existing binaries and eight staged additions, resolve placement/resource priority, then perform fresh-world acceptance before larger terrain/content changes. Static work may continue while runtime acceptance is pending.

Original broad sequence (retain later stages and apply the current statuses above):

1. **Re-establish the original Test 5 source build and validation.**
2. Run Test 5 in a clean world and collect the first proper runtime evidence.
3. Inspect the newly available Cristel, CTOV, Dungeons and Taverns, Towns and Towers, Seven Seas and Cataclysm Spellbooks JARs.
4. Verify and acquire exact versions of the eight approved structure additions.
5. Integrate the eight additions in a controlled test candidate.
6. Expand the effective structure catalogue and curated-biome compatibility matrix.
7. Apply the Farmers Structures frequency pass.
8. Test ordinary, medium, major, sky and dimension-specific structure distribution.
9. Resolve major overlaps and terrain clipping without undoing good density.
10. Proceed to biome weights, climate regions, mountains, coasts and Tan's Huge Trees.
11. Perform independent cave/ocean/Nether/End cleanup.
12. Complete cross-mod technical error cleanup.
13. Benchmark client and server operation.
14. Build the release candidate and run the full QA matrix.
15. Evaluate the 0.4.0 exit gate.

---

## Final project principle

Ambient Odyssey should feel **abundant, distinctive and rewarding to explore**, not merely overloaded with structures or mods.

The objective is a coherent world where exploration continually reveals interesting biomes, buildings, enemies, rewards and opportunities—while preserving strong performance, logical progression and enough stability for a long-running multiplayer server.

**This document is the master planning reference for the remaining 0.3.x development work and the transition into 0.4.0.**


## Session progress — 9 October 2026, Test 5 audit1

Wave: W0 reproducibility, available W2 audit, W4 source repairs and independent W7 resource cleanup. No new mod projects were installed; the 237 locked project/file pairs are preserved. Born in Chaos remains excluded from the export.

Files changed: `SOURCE_CHANGES.csv` records every changed/new source file with before/after SHA-256. Editable sources, generated overrides, code/NBT provenance, audit reports, all catalogues, validation and installation notes are included in the source/support archives. Archive hashes stay external to avoid self-reference.

Passed: original 76 gates; continuation source/export gates; strict generated JSON; preserved donor roster; placement/member ownership checks; asset-backed repair provenance; client model payload checks; ZIP integrity; clean source rebuild and report regeneration. Exact final gate count is in the validation summary. No gameplay tests performed.

Problems still open: 41 unavailable existing binaries, eight unavailable approved additions, authoritative base-game tags, 70 native resource collisions, live Cristel/Paxi priority, IDAS absent templates, Cook/blank jigsaws, developer-test models, successful natural density and performance. Rollback: original Test 5 archives and hashes in baseline reproduction evidence.
