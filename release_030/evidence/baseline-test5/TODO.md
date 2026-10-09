# Ambient Odyssey — Working TODO

Updated: 8 October 2026
Current stage: v0.3.1 Structure Test 5 export and updated sources are built from reconciled inputs. All 76 scoped static gates pass; archive integrity and a byte-identical clean source rebuild pass as recorded in STRUCTURE_TEST5_VALIDATION.md. The audit covers 177 complete JARs. Full transfers of mods1.zip/mods3.zip failed HTTP 403, leaving 60 logged JARs uninspected; their checks remain open. Test 5 has not been gameplay-tested.
Minecraft 1.21.1 • NeoForge 21.1.252 • recommended RAM 8 GB • intended group 5–7 players.

## Structure Test 5 — implemented static work and remaining coverage

### Completed implementation
- [x] Read both handoffs; extract/diff Test 4 and the editable sources; preserve unrelated configuration and the pinned mod manifest.
- [x] Reconcile Test 4 toggles, Dungeon Crawl 22/9 and placement changes into source inputs; delete stale compiler-owned sets before regeneration.
- [x] Audit 177 complete JARs by actual resources, CRC and SHA-256; catalogue 908 native structures, 584 sets and 3,488 pools. Publish the 911-row structure catalogue and 52-biome-column matrix, including three declared AO sky clones.
- [x] Resolve nested provider selectors, NeoForge AND/NOT holder sets and tag removals against the curated roster. Keep unresolved native/base-game/optional references visible.
- [x] Repair RU Blackstone Basin's mistaken Overworld membership; correct Alpine Clearings/Maple Taiga snowy classification and native-temperature-related cold/hot mistakes.
- [x] Add 145 editable provider/sky/optional biome-tag patch entries; keep surface buildings/sky grids separate from caves, oceans, Nether and End.
- [x] Remove Small Blimp and Coliseum from all inspected placement paths; disable native toggles and add the class-verified Integrated API disabled tag safeguard.
- [x] Separate Bathhouse into its own 112/48, frequency-0.5 grid; compensate the remaining minor pool so the reduction is independent.
- [x] Give ordinary WDA buildings and fourteen IDAS houses/inns/farms their own placement supply; remove duplicate boosted major/rare/village grids and preserve large-landmark rarity accounting.
- [x] Set the verified native Dungeon Crawl owner to 20/9, with its own salt and corrected donor eligibility.
- [x] Split Heavenly Challenger/Conqueror/Rider into OW-only declared template clones with independent settings; preserve original WDA IDs on the End-only native grid without extra End candidates.
- [x] Keep Sky Villages eligible over vanilla/RU rivers and the registered Streams stream biome; add land coverage and remove its ocean preference. Treat the visible-channel/land-biome explanation as an untested interpretation.
- [x] Make general Sky Whale variants land-eligible, constrain Frozen Whale to appropriate cool forests/taigas, and retain existing native heights/frequencies.
- [x] Audit Moog's actual selector graph; patch verified direct gaps only, retaining the existing frequency tuning.
- [x] Remove the known IDAS small/ocean sunken-ruins duplicate. Use directed candidate exclusions for ordinary buildings; do not add StructureOverlapless or enable a new global cave/surface distance rule.
- [x] Inspect Integrated API 1.9.0 bytecode: disabled tag is enforced at generation HEAD; unskippable tag is declared but no enforcement use was found in this JAR. Do not rely on it as a global overlap system.
- [x] Create four nonempty asset-backed pools: Foundry gears, Mechanical Nest library decorations, Cabin villagers and Cabin fisherman lecterns. Validate 33 real template connectors.
- [x] Empty unavailable Aether addon collections and obsolete required BYG collections. Keep BYG lumber variants disabled because their palettes still contain byg:* blocks.
- [x] Restore Artifacts native all/belt/hands slot memberships removed by RAR-Compat, keeping its extra routes and the existing Enigmatic overlay.
- [x] Diagnose the Streams bridge as timing/terrain-unavailability fallback; confirm actual FTF package/mod-ID support rather than changing class names speculatively.
- [x] Override Simply More's malformed matterbane_clean recipe with identical contents and valid JSON.
- [x] Prepare a concrete Tan open-field tuning plan as a separate, unapplied stage.
- [x] Build the final Test 5 CurseForge export and source archive; pass 76 scoped gates, ZIP CRC/path checks and a byte-identical rebuild from the extracted source ZIP. Include the updated TODO, audit, changelog, validation, installation notes, Tan plan, three CSV catalogues and reusable offline evidence/scripts.

### Input coverage and asset gaps — static tasks still open
- [ ] Finish the complete installed-profile JAR audit when the 60 unretrieved logged JARs are accessible. `release_030/evidence/jar-audit-coverage-test5.json` is the exact list. This is an input-transfer limitation, not an in-game-test prerequisite.
- [ ] Inspect Cristel Lib 3.1.7's actual placement/toggle processing to corroborate its handling of overridden native membership and frequency fields; generated data/config correspondence is validated, runtime library handling remains unverified.
- [ ] Audit CTOV's actual missing `village/waystone/sand` and `pillager_outpost/mountain/towers` pools and present templates before repairing them.
- [ ] Complete Seven Seas, Dungeons and Taverns, Towns and Towers, TotW and missing End/dimension-provider selector/placement audits. Their unchanged settings are preserved.
- [ ] Find asset-backed repairs for IDAS Dread Citadel `dread_citadel5`/`dread_citadel12` and Ancient Mines `ancient_mines_entrance2`. The inspected JAR has no matching assets; do not invent empty pools or self-recursive aliases.
- [ ] Investigate blank `minecraft:` jigsaw references and the separate Cook pool references in the supplied log; preserve coordinate/template evidence.
- [ ] Identify the fourth Nature's Spirit Overworld entry reported by the runtime (curation names only three). Do not guess an additional biome ID from the namespace count.
- [ ] Complete the native Minecraft/base-game tag graph from authoritative 1.21.1 resources; current matrices retain unresolved base-game/optional references and do not infer failure from zeros alone.
- [ ] Inspect Traveloptics 4.4.0.1 resources/registry code before fixing stale tags/models. Its JAR was not recovered.
- [ ] Inspect Cataclysm Spellbooks 1.1.14 registry/recipes. Logged missing keys include mechanical_weapon_parts, gauntlet_of_gattling, the_combuster, mechanical_scrap, engineers_power_glove, excel_upgrade_cooldown/mana/resistence/resistence_max; inspect exact recipe IDs before replacing items. No invented registry fix is included.
- [ ] Resolve Streams' preparation-time terrain/cache availability with bounded profiling/lifecycle evidence. Keep the current FTF + Streams stack for this test.

### Later runtime acceptance — not required to finish the build
- [ ] Import the exact Test 5 ZIP into a separate profile and create fresh chunks/world; record seed, biome IDs, preset and coordinates.
- [ ] Confirm no natural Small Blimp/Coliseum generation and inspect a retained, rarer Bathhouse.
- [ ] Confirm ordinary IDAS/WDA buildings and Dungeon Crawl across Prairie, Flower Fields, Sakura, forests and cool/snowy donor biomes.
- [ ] Check Sky Villages above land and rivers/Streams channels. Record the actual underlying biome ID, not just the visible terrain feature.
- [ ] Check the three `ambient_odyssey:heavenly_*_overworld` variants and original End branches; use the new IDs for Overworld locate commands.
- [ ] Check repaired Foundry/Mechanical Nest/Cabin assemblies and unresolved IDAS/CTOV cases.
- [ ] Check Artifacts restored slots; the earlier Enigmatic overlay has user-observed basic success, with individual omitted-item checks still available.
- [ ] Observe candidate exclusions, large-landmark rarity, terrain clipping and overlaps. Static weighted-candidate accounting does not establish real density.
- [ ] Measure ordinary generation separately from locate searches and Streams work. Preserve biome/terrain/tree/wildlife changes as separate stages.

## Current status and settled decisions

- [x] Build the locked pre1 base (234 projects) and separate Integrated Patches variant (235 projects).
- [x] Preserve the v0.2.10 baseline pins and its five performance additions.
- [x] Recover 620 working config/asset files, existing quests, keybinds and Tan assets. This is an import count, not a count of newly tuned configs.
- [x] Use FreeTerraForged as the sole Overworld terrain generator; remove Tectonic.
- [x] Retain accepted FTF defaults while testing the combined stack.
- [x] Apply 42 curated donor biomes: 40 Overworld and two Nether. Independent biome providers remain separate.
- [x] Remove Amaranth and unused Twigonometry; remove the obsolete ordering override/config. Keep TerraBlender and Kotlin for Forge.
- [x] Keep earlyWindowControl=false and the narrow Nature's Compass Minecraft-bound override.
- [x] Complete startup after Amaranth removal: latest supplied log records about 79 seconds, without a fatal startup error. World loading, stability and performance acceptance remain unverified.
- [x] Add global Create/BWG milling integration: 78 native recipes plus 18 missing inputs through Paxi.
- [x] Set temple ownership: MTR desert/jungle temples enabled; MTR stronghold disabled, Integrated Stronghold retained; MTR ocean-monument replacement off; IDAS desert-pyramid suppression off.
- [x] Keep Streams Reflowing, Tan's Huge Trees, TRMT, YUNG's Better Mineshafts/Better Witch Huts, Antique Trading Ship and Ember's Floating Islands in the current test build.
- [x] Keep Crazy Chambers parked after earlier initialization/worldgen errors.
- [x] Remove Companions! (1300341) and Modern Companions (1391597) from the locked build sources; remove their imported configs. Rebuild exports only when requested.
- [x] User reports biome replacement is working as intended in 0.3.1; climate ratios may be recalculated later.
- [ ] Verify the retained biome roster using Nature's Compass, especially restored RU Cold Deciduous Forest and Rocky Meadow.
- [x] Add the `ao_compatibility` Paxi datapack: extend common `minecraft`, `c`, and `forge` biome selector tags to the active curated Overworld roster and patch the audited direct vanilla-only structure lists.
- [x] Add the Enigmatic Legacy+ 1.1.2 Curios overlay: explicit amulet assignments, fork `the_necklace` in `curios:amulet`, and omitted `darkest_scroll` in `curios:scroll`.
- [ ] Runtime-test structure eligibility in curated forests, open fields, Sakura/Prairie, cold biomes, coasts and oceans; record exact biome IDs and structure groups.
- [ ] Runtime-test the Curios overlay with a coloured amulet, named amulet, The Necklace and Darkest Scroll; record any remaining rejected item ID.

TRMT produces walked/eroded paths, not a generated road network. The first structure density pass is now applied to the test sources; actual building density still needs a fresh-world test. The reported anticheat involvement in earlier NVIDIA native exits remains unconfirmed.

## Latest field feedback — 8 October 2026

User observations from about 40 minutes of flying in the current test world. These are qualitative observations, not an area-normalized density survey; seed, coordinates, route, flight speed and effective generated area were not supplied.

### Recorded observations
- The new log identifies `dungeons_arise:monastery` at (-1598, 145, -793), `ctov:small/village_mountain_alpine` at (-1572, 106, -785), and `apotheosis:tower_main` at (-1572, 142, -764). All three logged positions lie within 39 blocks horizontally, supporting the reported collision/close cluster.
- About one village, five medium houses and five to eight Dungeon Crawl sites were seen. No large buildings were seen, and small surface details were sparse.
- Prairie and Flower Fields felt empty of buildings; Prairie also had too many Tan trees.
- Flying structures were almost absent during the route.
- Prairie, Sakura Grove and vanilla `minecraft:taiga` appeared too often. Sakura Grove also appeared poorly served by structures.
- Vanilla Snowy Slopes, Jagged Peaks and Frozen Peaks looked too basic; Stony Shore is unwanted.
- Climate groups covered too much distance before changing; the world did not feel sufficiently alive.

### Next tuning priorities
- [x] Audit the installed structure JAR biome selectors and apply a first compatibility layer for the vanilla-versus-modded eligibility gap. Check exact biome lists, common tags and direct selectors in the runtime test. Include open fields, Prairie, Sakura Grove and cold biomes explicitly.
- [ ] After the compatibility pass, verify actual fresh-world placement and refine any provider-specific selectors that still reject curated biomes. Check spacing/separation, exclusions and config switches.
- [ ] Increase overall land-surface structure presence: villages, small landmarks, houses/farmsteads, medium buildings and large buildings. The earlier general instruction to reduce ordinary/medium structure clutter is superseded by this field test.
- [ ] Make Apotheosis towers deliberately frequent enough to offer an accessible early gearing route in the difficult pack. Verify their eligibility in the curated biome pool as well as spacing.
- [ ] After the density test, address the reported WDA–CTOV–Apotheosis cluster and inspect overlap controls.
- [ ] Audit Overworld sky-structure eligibility and vertical placement over ordinary curated biomes. This is an additional requested sky audit; Nether, End, sea and underground density remain separate.
- [ ] Reduce Tan tree density overall and substantially in Prairie/open field biomes. Preserve deliberately dense trees in one or two chosen forests; vanilla Taiga is the user's example. Reducing the total area of vanilla Taiga is compatible with keeping its remaining patches densely wooded.
- [ ] Adjust Tan through its native biome/group rules and global controls while preserving the chosen dense exceptions. Its imported config supports biome IDs/tags, rarity, minimum distance and group size; lower native rarity values mean rarer trees.
- [ ] Reduce Prairie and Sakura Grove dominance; increase other retained field options, explicitly including BOP Pumpkin Patch. Keep the rest of the curated roster and prior rarity decisions unless the user changes them.
- [ ] Reduce vanilla Taiga and distribute its cold forest opportunities among the retained modded taiga/coniferous options; verify exact climate matches before selecting weights.
- [ ] Add modded replacements for `minecraft:snowy_slopes`, `minecraft:jagged_peaks` and `minecraft:frozen_peaks`, checking the existing curated roster first. Preserve their mountain terrain role and verify the modded surface/features rather than merely renaming biome IDs.
- [ ] Set `minecraft:stony_shore` retention to exactly 0% in newly generated Overworld terrain; choose an appropriate retained coastal replacement. Existing generated chunks are unaffected.
- [ ] Increase the presence of genuinely large mountain terrain through FTF terrain controls, separately from snowy mountain biome replacements. Exact values need a controlled test.
- [ ] Make climate groups smaller so temperature/moisture groups change sooner. Audit FTF temperature/moisture scale separately from biome patch size, region sizing and replacement noise. Keep the selected 6500 continent scale and river-count changes separate from this goal.
- [ ] Audit wildlife compatibility against the actual installed profile: animal/ambient spawn selectors, curated biome tags, biome spawn tables and fresh-world observations. Include Alex's Mobs and other retained wildlife providers; retain the request to disable flies and similar unwanted insects.
- [ ] Verify whether Critters & Companions is installed in the user's current profile before auditing it. It is still recorded as a future candidate in the saved TODO and is a separate mod from the removed Companions! and Modern Companions.
- [ ] Retest a recorded fresh-chunk route for buildings, towers, wildlife, tree density, mountain presence and climate transitions after the changes; record the seed, coordinates and route length.

Current source check: the Biolith rules target twelve plains/forest/birch/savanna/jungle biome IDs. They do not yet target vanilla Taiga, Stony Shore or the three mountain biome IDs above. No generation settings were changed when recording these notes.

## Structure-test1 changes and deferred log issues — 8 October 2026

- [x] Remove Companions! and Modern Companions from the new export, including their imported configs.
- [x] Disable `alexsmobs:gameplay/seal_reward` completely through an empty high-priority loot table. Seals and their separate entity loot remain installed.
- [x] Apply 140 selected placement entries across 35 config files and 103 individual Moog set frequency multipliers. Apotheosis towers: spacing/separation 26/18 → 12/6; nominal candidate density ×4.69.
- [x] Add three extra placement sets for WDA land/sky landmarks, IDAS rare land landmarks and Integrated land villages. Keep each original mixed set and native eligibility; exclude boats/ocean, mine/cave groups and explicitly End-eligible WDA variants from the extra sets.
- [ ] Run the new full test export in a fresh world and inspect its new log. Static checks do not establish runtime success.
- [ ] After placement testing, investigate IDAS old `byg:` biome references, missing Integrated Villages villager/fisherman pools, missing Graveyard crypt pool and absent Guard Villagers entity references.
- [ ] Investigate Malkuth's arena starting-jigsaw error during the later boss/ocean generation audit.
- [ ] Investigate Traveloptics resource/tag/model failures and Cataclysm Spellbooks recipe/loot-modifier failures later, as requested.
- [ ] Perform the wildlife/insect audit later. Critters & Companions was absent from the supplied log.

The supplied 8 October exploration log loaded Biolith placement data and saved/shut down normally. It recorded 15 server lag warnings and a 90% memory warning (9230 MB), later falling to 5623 MB; that alone does not establish a persistent leak. This recorded run still had both companion mods and lacked Integrated Patches/Mowzie's/BOMD addons. Those findings are about that run, not the newly prepared profile.

## 1. Immediate: thoroughly inspect base 0.3.0-pre1

### Launch and basic functionality
- [ ] Confirm repeat launches and successful entry into a fresh FTF-default world.
- [ ] Check logs for config decoding, registry, recipe and dependency failures.
- [ ] Investigate GeckoLib animation parsing and Traveloptics item-model errors from the latest log; do not assume these caused the temporary startup freeze.
- [ ] Verify donor config files retain the intended enabled biome roster after launch.
- [ ] Test Nature's Compass searches and Create/BWG milling recipes.
- [ ] Verify inherited WDA quests, rewards, icons and existing keybinds.

### Terrain and biome inspection
- [ ] Record seed, FTF preset, graphics settings and render/simulation distances.
- [ ] Verify the curated donors actually generate, especially restored RU Cold Deciduous Forest/Rocky Meadow, BWG Sakura Grove and BOP Snowblossom Grove.
- [ ] Inspect biome size, repetition, climate transitions, marine/coastal transitions and uncommon biome availability.
- [ ] After the biome replacement pass, audit cave and ocean generation separately, including cave variety, ocean biome coverage, coast transitions and underwater structures.
- [ ] Inspect FTF mountains, valleys, coastlines and Streams Reflowing river integration.
- [ ] Check Tan trees for terrain clipping, floating roots, structure conflicts and excessive frequency; keep fixed assets for comparisons.
- [x] User verified TRMT paths develop correctly through walking/erosion.
- [ ] Increase TRMT erosion/path formation speed and effectiveness; test gradual changes so paths appear faster without excessive terrain degradation.
- [ ] Check the retained Nether and End stack alongside the Overworld changes.

### Structure inspection
- [ ] Tune Overworld above-ground structures on land first; the user wants many structures to be more common. Account for Integrated overhauls and audit explicit vanilla-biome eligibility, particularly Bosses' Rise.
- [ ] Verify MTR temples, Integrated Stronghold, YUNG mineshafts/witch huts, trading ships and floating islands.
- [ ] Inspect Integrated Villages, IDAS, WDA/Seven Seas, Moog structures, Towns and Towers, Dungeon Crawl, Dungeons Enhanced and other installed structure providers.
- [ ] Inspect boss landmarks, especially Cataclysm, Iron's Spells, Ice & Fire and applicable giant structures.
- [ ] Record buried entrances, floating pieces, clipping, blocked paths/puzzles, tree interference and overlaps with coordinates/screenshots.
- [ ] Audit exact installed Integrated API/Cataclysm/Patches files for disabled-structure tags, replacements and exclusion rules. Check other contributing mods/datapacks too; documentation alone does not establish the effective blacklist.
- [ ] Inspect End structures for biome eligibility and vertical placement, including TotW reportedly spawning too low around Y=28.
- [ ] Run the optional AO locate survey only when useful. It measures nearest-structure search results, not actual density/overlap; searches may stall the game.

### Performance baseline
- [ ] Test at 8 render / 6 simulation, then 14 / 12.
- [ ] Time fresh-world creation, spawn settling, 5–10k fresh-chunk teleports, Nether round trip, End entry and long End teleport.
- [ ] Record generation/settling separately from comparable-scene FPS and stutters.
- [ ] Use the installed Spark for bounded profiling when needed; do not add a duplicate.
- [ ] Preserve the seed, route, settings and generated-chunk history so comparisons remain meaningful.

## 2. Integrated addons — included in the next density test

- [x] Promote Integrated Patches into the main test build by user instruction.
- [x] Add Integrated Mowzie's Mobs 1.3.2 and Integrated Bosses of Mass Destruction 1.0.0, with required Amendments 2.1.10.
- [ ] Verify all three addons in the new launch log and inspect representative overhauled landmarks after the placement-density test.
- [ ] Keep a Patches A/B comparison available as a later diagnostic if a specific problem justifies it; it is no longer the immediate prerequisite.

Already-generated chunks retain their original structures. Use a fresh world for this revision.

## 3. After compatibility passes: 0.3.0 configuration and integration

- [ ] Tune FTF terrain scale/coherence alongside structure placement using same-seed fresh worlds.
- [x] Package the named FTF 0.3.1 user preset with continent scale 6500 and river count 15, based on the pinned 4000-scale/10-river template. Select it in Customize for a fresh world; land fraction is unchanged independently of scale.
- [x] Implement editable Biolith pools for twelve vanilla fallback biomes, with 5% nominal vanilla retained in plains/forest/birch pools and 0.5% in savanna/jungle pools; add temperature guards limited to vanilla-origin replacements.
- [ ] Finish testing the 0.3.1 FTF preset, climate boundaries and structures in fresh worlds; initial biome replacement is user-confirmed. Do not equate pool weights with world-wide biome area.
- [ ] Balance biome weights/distribution while retaining the curated roster unless observations justify a change.
- [ ] Climate replacement rarity decisions: keep Volcano rare; treat Skyris Vale, Snowblossom Grove and Floral Ridges as uncommon; preserve the rest of the curated roster.
- [x] Apply the first frequency increase to the 0.3.1 structure test: prioritize Apotheosis towers, surface villages/houses/farms/landmarks and sky structures.
- [ ] Test actual density, then check biome eligibility/spawning failures and overlaps in the requested order.
- [ ] Retest the implemented directed exclusion controls. The inspected Integrated API 1.9.0 does not establish a working global unskippable overlap system; assess existing controls before adding anything else.
- [ ] Do not add StructureOverlapless alongside Integrated API: the documented incompatibility supersedes the old TODO candidate. Audit existing controls first.
- [ ] Audit MES configuration for Astrological upper/middle/lower End-layer distribution.
- [ ] Audit Cataclysm × BetterEnd: New Dawn compatibility and End biome/layer tags; fix verified placement problems.
- [ ] Audit Integrated Stronghold–End Remastered integration and End Remastered Additions; assess the eye hunt's breadth versus tedium.
- [ ] Compare End City overhaul options and keep one; leave loot balancing for the later balance pass.
- [ ] Consider Sunken Spires via Paxi after the current stack passes; validate before including it in the release.
- [ ] Add Distant Horizons after the base generation benchmark; measure its LOD generation/cache work separately and start conservatively.
- [x] Queue complete Born in Chaos removal in the saved build sources; supersedes its individual Infested Diamond/flies/maggots configuration task.
- [ ] Audit dependencies, recipes, quests, loot and structure references affected by Born in Chaos removal before the next export.
- [ ] Disable flies and similar unwanted insect mobs across installed mods, explicitly including Alex's Mobs Fly. Audit the actual mob roster and native spawn toggles; broader insect choices should be listed explicitly rather than silently removing bees/butterflies or unrelated creatures.
- [ ] Verify natural and structure-driven spawning for disabled insects in a fresh world.
- [ ] Investigate stale structure-template entity NBT, invalid-air stacks and obsolete attributes where present; identify responsible templates before editing.
- [ ] Recheck the previously logged Remnant Bosses/JAUML Windows config-save errors before tuning those bosses.

## 4. Later controlled performance and server tests

- [ ] Evaluate additional client optimization changes individually, including Entity Culling/BadOptimizations where not already active and Create Better FPS.
- [ ] Keep the existing ModernFix/FerriteCore/Embeddium/ImmediatelyFast/Lithium/ServerCore baseline; avoid duplicate optimizers.
- [ ] Consider Nitro Performance only as an isolated startup/JEI test.
- [ ] Test Connectivity/login robustness separately from generation speed; assess Login Protection.
- [ ] Keep Chunk Sending rejected unless its implementation changes materially; earlier 3.9/4.1 tests did not fix invisible terrain.
- [ ] Consider SeamlessChunks only if delivery/render settling remains poor after generation pressure improves.
- [ ] Profile 5–7 players spreading across chunks/dimensions and test long-session memory growth.
- [ ] Audit FTB Backups 3 before shared-server play.
- [ ] Freeze worldgen before serious pregeneration. Choose the tool, centre, shape and radius based on measured generation speed/storage; no 20k-radius requirement is committed.

## 5. Future RPG progression, quests and balance

- [ ] Choose one main player-wide skill-tree approach; Pufferfish currently leads. Compare Adventurer Skills as a reference with an AO-owned tree.
- [ ] Compare Iron's Spells skill-tree/progression integrations without duplicating systems.
- [ ] Audit NeoOrigins with one curated Origins/class approach; compare Classes Extended versus Classes ISS rather than stacking frameworks.
- [ ] Audit TarotCards rarity/gating, Armor Set Bonuses and gear identity; avoid unconditional stat inflation.
- [ ] Audit Better Combat–Apotheosis range compatibility, Apothic Compats/Category Compat and Apotheosis–Iron's Spells integration.
- [ ] Avoid more generic weapon packs until the existing gear economy is balanced; Fantasy Armor remains a visual/transmog candidate.
- [ ] Build the rich AO FTB questbook once content topology stabilizes; inherited chapters are not the finished AO progression.
- [ ] Make true bosses stronger than stock; design around 1–3 simultaneous fighters, even with 5–7 server members.
- [ ] Define superboss tiers for Maledictus, Scylla, Iron's Spells scythe boss and suitable Remnant Bosses encounters.
- [ ] Use gentle/sublinear party scaling while preserving equipment gaps and gear gates; audit one multiplayer scaling route.
- [ ] Test Bosses'Rise encounters with Better Combat for dependence on removed dodge/parry mechanics.
- [ ] Audit boss heal/reset behavior to prevent respawn brute force, plus Ender Dragon mechanics and stats.
- [ ] Check AttributeFix caps and armor behavior when designing high stats; consider Apothic Ascension/L2 Hostility/Dungeon Difficulty only with a coherent scaling plan.
- [ ] Balance structure/boss/End City loot, Apotheosis, Relics/Artifacts, Tarot, skill rewards and Goblin Traders economy.

## 6. Optional future content — candidates, not committed additions

- [ ] Controlled structure/dimension audits: Ancient Remnants, Nether Trials & Chambers, Archaion and Dimensional Dungeons.
- [ ] Audit EpicQuestDungeoning for repeatable/keyed endgame runs; Natyheim remains an archaeology/puzzle candidate.
- [ ] Test Integrated Dungeons Arise as a possible substitution for WDA, never blindly stack both. Integrated Mowzie's Mobs is now included by user instruction.
- [ ] Revisit Crazy Chambers only in an isolated diagnostic test.
- [ ] Build a tiny isolated Connector profile for Mine Cells first; consider Oblivion afterward, then exceptional DungeonZ/AdventureZ content if stable.
- [ ] Keep Wet Sand and Apotheotic Additions native ports as separate later development tasks.
- [ ] Keep desire-path alternatives parked while evaluating TRMT; avoid stacking redundant implementations.
- [ ] Audit selected animal/pet additions: Critters & Companions, Adorable Hamster Pets/Companion and at most a justified smaller animal pack.
- [ ] Later ambience/resource-pack pass: AmbientSounds, Sound Physics, BiomeBloom, Benigamer visuals, Musgo and Sunbathing Godrays.
- [ ] Revisit Dusty Decorations, Nightlights and Serene Seasons; compatibility/gameplay value remains to be assessed.
- [ ] QoL audits: Polymorph, Controlling, Lootr/container/mimic integration, Xaero/Waystones/FTB map compatibility and multiplayer sleep behavior.
- [ ] Finish UI/bossbar polish; keep Accessories button hidden/access by keybind unless intentionally redesigned, and assess north-up Xaero defaults.
- [ ] Big Globe stays a separate future major-overhaul experiment.
- [ ] Grow content breadth in controlled waves after stabilization; Ascendra-class breadth is a direction, not a mod-count quota.

## Dedicated later QoL, interface and controls workstreams

- [ ] 0.4.x QoL expansion audit: review usability across the installed profile, including searchable keybind settings, conflicts, inventory actions, search/filter behavior, navigation and multiplayer conveniences.
- [ ] GUI/UI overhaul: make menus, HUD, inventory, questbook, accessibility and mod interfaces consistent; retain current pack defaults during Structure Test 5.
- [ ] 0.6.x questbook controls audit: inspect every vanilla/mod keybind, identify non-obvious actions and conflicts, and build a comprehensive FTB Quests tutorial chapter explaining each control's purpose and examples. Coordinate it with searchable keybind settings.

## 7. Final release gates

- [ ] Repeat performance testing after content/configuration work, including lower-end PCs and multiplayer.
- [ ] Verify narrator, audio, keybinds, defaults and intended 8 GB recommendation.
- [ ] Complete dependency/license/distribution checks.
- [ ] Inspect the exact CurseForge upload ZIP for manifest.json at archive root; do not submit a sources or wrong export ZIP.
- [ ] Publish only the exact accepted build; provide a concise changelog and server setup notes.

This replaces obsolete instructions to promote 0.2.9 unchanged, add Amaranth, or stack StructureOverlapless. TESTING-0.3.0.md still supplies the detailed benchmark procedure, but its startup-pending wording is superseded by the latest successful startup log. Neither runtime acceptance nor release publishing is complete.
