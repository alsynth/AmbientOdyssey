# Ambient Odyssey — Structure Test 5 JAR and biome audit

Date: 8 October 2026. Baseline: v0.3.1 Structure Test 4. Minecraft 1.21.1 / NeoForge 21.1.252.

## Evidence and coverage

This audit reads actual uploaded JAR resources and selected class bytecode, not just exported spacing configs. **177 complete JARs were CRC-checked and SHA-256 recorded**, yielding **908 native structure definitions, 584 structure sets, 3,488 template pools and 1,094 biome-tag definitions**. The installed JAR resource snapshot is included in the sources as `release_030/evidence/jar-resource-index-test5.json.gz`.

**Full collection coverage is incomplete.** Full transfers of `mods1.zip` and `mods3.zip` repeatedly failed HTTP 403. `mods2.zip`, both project ZIPs and the seven individually supplied JARs were available. Only complete, individually CRC-verified JAR members of the interrupted ZIP prefixes were recovered; incomplete members were rejected. The supplied runtime lists 235 mod-folder JARs; 60 of those names remain unretrieved, and two supplied JARs were not listed in that log. The precise inventory is in `jar-audit-coverage-test5.json`. Important gaps include CTOV, Cristel Lib 3.1.7, WDA Seven Seas, Traveloptics, Cataclysm Spellbooks, Dungeons and Taverns, Towns and Towers, and several End/dimension providers. No claim of a complete installed-profile audit is made.

`STRUCTURE_REGISTRY_CATALOG.csv` gives every inspected structure's source JAR/path, selector, placement sets, generation step, height settings, inferred category, before/after curated eligibility and unresolved tag references. `STRUCTURE_BIOME_MATRIX.csv` gives one eligibility cell per biome. `STRUCTURE_SET_CATALOG.csv` gives all 590 effective inspected sets, their members/weights, native placement JSON overlaid with supplied Cristel config values, and Moog per-set multipliers. Config presence is not proof of library execution; that column is explicitly uncertified. A zero means no membership was found in the inspected/overlaid graph; unresolved references remain explicit. Default Minecraft tag files and unavailable JARs are not silently invented. NeoForge AND/OR/NOT holder sets and `remove` entries are applied during resolution; optional built-in packs are inventoried separately and not assumed active. Cached Test 4 tag and asset-hash evidence allows the source archive's reports and static comparisons to be rerun without the original Test 4 ZIP.

The curated roster is **40 Overworld + two Nether biomes**. Ars Nouveau's Archwood Forest is included separately where appropriate. Quark Glimmering Weald and the six Alex's Caves biomes are identified as cave content; they are not added to surface-house or sky tags. The TerraBlender deferred placeholder is not treated as usable terrain. The runtime's fourth Nature's Spirit entry is not identified by that log's namespace-count summary; it remains a roster/source discrepancy to inspect, rather than an invented biome ID.

## Source reconciliation

The extracted editable sources matched Test 4's unrelated overrides. Differences were confined to Dungeon Crawl placement, WDA toggles, WDA extra-grid membership, the shared Heavenly extra grid and historical notes. Test 4's 22/9 Dungeon Crawl setting and disabled native Blimp/Coliseum toggles were incorporated into authoring inputs before Test 5 tuning. The generated grids are compiler-owned and cleared before regeneration, preventing deleted Test 3/4 grids from surviving a second build. Locked mod project/file pins remain unchanged.

## Verified eligibility problems and fixes

1. **Nether leakage:** the old compiler excluded `biomeswevegone:blackstone_basin`, which is not the roster ID. The actual `regions_unexplored:blackstone_basin` is Nether content. Test 5 keeps both RU Nether donors out of curated Overworld and sky tags.
2. **Climate errors:** native JSON temperatures show Alpine Clearings is 0.7, Maple Taiga is 0.25, Hot Springs is 0.17 and Ashen Woodland is 2.0. Alpine Clearings and Maple Taiga are no longer authored as snowy biomes; Alpine Clearings is removed from cold tags. Hot Springs is removed from the warm/hot collection, while Ashen Woodland is recognized as hot. Cool BWG forests receive cold membership without being mislabeled snowy. These are biome eligibility corrections; no terrain generator, climate scale or biome-pool weights are changed.
3. **Direct vanilla leaves:** many IDAS house tags, Integrated Villages' plains/taiga/forest collections, Cataclysm's Frosted Prison selector and assorted Repurposed Structures selectors enumerate vanilla biome IDs instead of using the generic tag names patched in Test 2. Test 5 follows each actual selector graph and adds explicit AO climate/landform analogues to the relevant provider tags. Desert/badlands structures receive no invented forest or grassland replacement when the curated roster lacks a suitable desert/badlands donor. Native generation steps and terrain constraints remain intact.
4. **Dungeon Crawl:** `dungeoncrawl:dungeon` uses `#dungeoncrawl:has_structure/dungeon`, and its native owner is `dungeoncrawl:dungeons`. The tag already supports common forest/mountain/taiga selectors, but direct plains/swamp entries missed several curated donors. Explicit provider membership is now supplied. Its registered placement config is changed from Test 4's 22/9 to 20/9 with an independent salt.
5. **IDAS legacy BYG collections:** two malformed required old-BYG collections are replaced with empty collections. The BYG redwood/mahogany lumber templates themselves contain `byg:*` block palettes, so their two variants are disabled instead of being enabled by a biome-only alias. Valid oak/spruce/birch/jungle variants receive current biome coverage.
6. **Aether Villages:** its Ancient Aether and Aether Redux collections contain required references to unavailable providers. These optional collections are explicitly empty; ordinary Aether village content remains present.

The generated provider additions are editable in `release_030/structure-compatibility.json`. The older common classifications remain in `compile_compatibility_031.py`; the native-temperature evidence is in the offline JAR snapshot. These mappings are deliberate AO analogues, not a claim that names or temperature alone guarantee a flat, unclipped placement.

## Flying structures and the river correction

**Sky Villages' native tag explicitly includes oceans and rivers**, plus forests and jungles. It does not have a land-only selector. Test 5 replaces that selector with a land-and-river collection that includes vanilla River/Frozen River, RU Muddy River, the actual registered `streamsreflowing:stream` biome and a broad suitable land roster. Ocean biomes are excluded from this village collection to address the observed ocean concentration. Streams' channel/land-biome explanation remains a plausible interpretation; the runtime count does not show its stream biome in that particular Overworld source, and no observation of river placement is claimed.

**Sky Whale Ship** has five independent native sets. Four structures use `#minecraft:is_overworld` and therefore allow oceans; Frozen Whale uses `#minecraft:is_taiga`. The first four now use explicit land eligibility and Frozen Whale uses a cool taiga/snowy-forest subset. Existing height ranges (180–220 or 180–240) and the previous spacing increases are preserved.

**The WDA Heavenly trio** uses Y=200, native jigsaw templates, and selectors containing both Overworld and End biome IDs. Test 4's shared 42/22 extra grid supplied one candidate for the trio and also applied in the End. Test 5 removes that grid. Each Overworld variant now has its own declared native-template clone and grid: Challenger 72/32, Conqueror 84/40, Rider 64/28. The three original WDA IDs retain an End-only selector on the existing native major grid, whose spacing stays 50/45 and whose compensated frequency cannot increase its candidate supply. New AO clone definitions differ from the inspected native structure definitions only in `biomes`; they reuse the same template pools, height and other settings. The clones are declared new registry entries, not falsely described as preexisting JAR IDs.

Moog's Soaring Structures already routes its main family through `#minecraft:is_overworld` plus optional common/provider tags. It does not need another global frequency boost. Only verified direct-selector gaps such as mangrove membership receive additions; the 103 preexisting Moog per-set multipliers are preserved. Its explicitly ocean-themed Palm Island remains ocean content.

## Placement ownership, rarity and overlap

- Small Blimp and Coliseum are removed from every inspected effective set and disabled in native toggles. Integrated API 1.9.0's actual `DisableStructuresMixin` injects at `ChunkGenerator.tryGenerateStructure` HEAD and returns false for `integrated_api:disabled_structures`; that tag supplies an additional global safeguard.
- Mushroom House, Greenwood Pub, the ordinary campsites and Illager Windmill move from the native major pool to one ordinary-land grid (28/14). The old duplicate mixed WDA extra grid is removed. Remaining native major entries use weighted-candidate frequency compensation (27/38), preserving nominal rarity accounting instead of giving boss landmarks a second boosted grid.
- Bathhouse has one owner at 112/48 and frequency 0.5. This is about 19% of its former nominal 28-chunk, six-way weighted candidate density. The other five native minor entries keep their 28/18 grid with frequency 5/6 compensation. The JAR's root-level minor `exclusion_zone` is placed inside `placement`, where the placement codec can consume it.
- Fourteen ordinary IDAS house/inn/farm variants move to an independent 16/8 grid. The remaining native common buildings retain 15/8 with weighted-candidate compensation, so house candidates no longer compete with castles/towers. The duplicate AO rare-landmark grid is removed. The native sunken-ruins duplicate in the small pool is removed while its ocean owner remains.
- Integrated Villages' duplicate AO land-village grid is removed; its native regular-village owner is set to 22/14 and keeps the native advanced exclusion scheme. Native air-village tuning remains unchanged.
- New ordinary WDA/Bathhouse grids use directed Integrated API candidate exclusions against the inspected major/rare/native-village sets. The house grid also avoids remaining native common IDAS buildings. These are candidate-distance controls, not a guarantee against all cross-mod bounding-box overlaps. Dense exclusion graphs are deliberately avoided.

Multiple structure sets referring to one structure expose that structure to multiple candidate placements; there is no automatic single-owner registry rule. Independent set salts avoid identical AO grids. Shared salts across different dimensions or mutually exclusive biome sets are not automatically errors. Dungeon Crawl's old salt shared the monuments/End-city number, but those separate dimension/biome relationships alone did not prove a collision; its new salt nevertheless removes that unnecessary correlation.

Two native Moog Voyager memberships remain deliberately unchanged: `mvs:rare_well` and `mvs:small_tower_well` each occur in `mvs:other_wells` and their own set. They use different native grids and salts; neither is an accidentally retained AO boost. The complete effective membership list and 11 shared-salt groups are in `duplicate-placement-membership-test5.json` and `shared-placement-salts-test5.json`. New AO targeted groups have one owner and unique salts; this is not a claim that every native mod uses a single-owner design.

The installed Integrated API JAR declares an `unskippable_structures` tag, but the inspected classes contain no use beyond tag initialization. It is not relied upon as a global overlap control. Structure Essentials' existing `minimumStructureDistance` switch is disabled in the supplied configuration; it remains disabled because its own documented cave/surface suppression and retry costs need a separate controlled test. StructureOverlapless is not added.

Weighted compensation describes nominal candidate accounting. Biome eligibility, invalid-selection fallback, config-library handling and successful jigsaw assembly can change observed density. Large boss-landmark grids are not multiplied. Runtime rarity and collisions remain acceptance tests.

## Assembly repairs and remaining missing assets

Four nonempty pools are compiled from actual native assets:

| Broken reference | Test 5 repair |
|---|---|
| WDA `foundry_corridor_gears` | Two existing Foundry gear templates from the native decoration pool; both have the requested gear connector. |
| WDA singular `mechanical_nest_decoration` | Existing library-decoration templates with the exact tower connector. |
| Cabin Village `cabin_village/villager_random` | Alias of the existing native `cabin_village/mobs/villager_random` pool, retaining its original weights. |
| Cabin Village `house/fisherman_lecturn` | Seven existing native fisherman lectern templates, all with matching `lecturn` connectors and native processor settings. |

The NBT reader checked **33 native templates** for these repairs. No empty pool was invented to hide a warning.

IDAS's Dread Citadel giant template contains references to `dread_citadel5` and `dread_citadel12`, but the inspected JAR ships only its monolithic Dread Citadel template and no corresponding modular pools/templates. Ancient Mines has an `ancient_mines_entrance2` reference with no matching second entrance asset. These are documented dangling/legacy references; arbitrary substitutions or self-recursive aliases are not created. CTOV's missing waystone and outpost pools are confirmed by the runtime log, but its JAR remained unavailable, so an asset-backed repair is not certified. Blank `minecraft:` and Cook-related warnings in the log remain separately listed; they are not conflated with a missing structure registration.

## Independent compatibility/performance findings

**Streams Reflowing:** actual `RTFBridge` bytecode recognizes both `raccoonman.reterraforged` and `etcodehome.freeterraforged`, including both mod IDs and flow-field method names. Thus the warning is not evidence that the bridge simply forgot the FTF namespace. The warning is emitted when an installed generator's terrain is unavailable during stream preparation, causing slow height sampling. The supplied log records this fallback. A correct fix needs lifecycle/cache evidence; no speculative class-name replacement or worldgen-stack removal is made.

**RAR-Compat:** its real tag files use `replace: true` for Artifacts `slot/all`, `slot/belt` and `slot/hands`, clearing several native items. Test 5 adds the complete native memberships back while keeping RAR's extra charm/head routes. The existing Enigmatic Legacy+ amulet/scroll overlay is preserved.

**Simply More:** the installed `matterbane_clean.json` has an extra trailing `}`. A valid JSON override reproduces the recipe contents with that stray brace removed. This is the sole malformed native recipe found in the readable resource scan; other missing-item recipe errors cannot be established from JSON syntax alone.

**Traveloptics/Cataclysm Spellbooks:** the runtime identifies stale Traveloptics resource/tag/model issues and Cataclysm Spellbooks recipes whose referenced item keys are absent. Their JARs are among the unavailable tail files. The exact missing items/recipe IDs are recorded in TODO; item substitutions or invented registry entries are not applied.

**Tan's Huge Trees:** its supplied native config supports OR/AND biome expressions, inverse predicates, numeric rarity, minimum distance, group size and `[LOCK]` persistence. Lower rarity means fewer trees; large group sizes can make the world denser and increase scan work. A concrete staged plan is provided in `TANS_OPEN_FIELD_TUNING_PLAN.md`. No tree settings, wildlife spawns, biome sizes or climate scales are applied in Structure Test 5.

The Test 2 locate benchmark (164 searches, median 3.122s, mean 8.552s, worst 141.631s) measures command search work, not ordinary chunk-generation speed or area-normalized density.

## Per-provider catalogue summary

The table counts inspected native resource definitions. “Changed OW coverage” compares resolved curated membership with Test 4. “No curated OW” includes correctly Nether/End/cave/desert-specific content and disabled variants; it is not a failure count. AO clones are separately declared.

| Provider | Native structures | Changed OW coverage | No curated OW after |
|---|---:|---:|---:|
| `adventuredungeons` | 8 | 6 | 1 |
| `aether` | 4 | 0 | 4 |
| `aether_villages` | 1 | 0 | 1 |
| `alexscaves` | 14 | 0 | 13 |
| `ambient_odyssey` | 0 | 3 | 0 |
| `antiquetradingship` | 1 | 0 | 1 |
| `apotheosis` | 4 | 1 | 1 |
| `archaeology_ruins` | 11 | 0 | 11 |
| `ars_nouveau` | 3 | 0 | 0 |
| `betterend` | 14 | 0 | 14 |
| `biomeswevegone` | 18 | 0 | 12 |
| `block_factorys_bosses` | 5 | 2 | 3 |
| `bosses_of_mass_destruction` | 4 | 1 | 3 |
| `cataclysm` | 16 | 4 | 12 |
| `dungeoncrawl` | 1 | 1 | 0 |
| `dungeons_arise` | 40 | 12 | 10 |
| `enigmaticlegacyplus` | 1 | 1 | 0 |
| `eternal_starlight` | 8 | 0 | 4 |
| `explore_ruins_aether` | 7 | 0 | 7 |
| `farmers_structures` | 20 | 7 | 9 |
| `fdbosses` | 3 | 0 | 1 |
| `floating_islands` | 17 | 15 | 0 |
| `formationsoverworld` | 30 | 18 | 3 |
| `friendsandfoes` | 4 | 1 | 1 |
| `graveyard` | 17 | 7 | 5 |
| `iceandfire` | 13 | 9 | 0 |
| `idas` | 84 | 51 | 24 |
| `illagerwarship` | 1 | 0 | 1 |
| `incendium` | 9 | 0 | 9 |
| `integrated_stronghold` | 1 | 1 | 0 |
| `integrated_villages` | 12 | 5 | 4 |
| `irons_spellbooks` | 9 | 4 | 2 |
| `mes` | 25 | 0 | 25 |
| `minecraft` | 8 | 0 | 4 |
| `mns` | 52 | 0 | 52 |
| `mowziesmobs` | 4 | 0 | 0 |
| `mss` | 35 | 3 | 4 |
| `mtr` | 6 | 0 | 3 |
| `mvs` | 130 | 16 | 14 |
| `natures_spirit` | 4 | 0 | 4 |
| `pasterdream` | 115 | 0 | 113 |
| `philipsruins` | 17 | 12 | 4 |
| `repurposed_structures` | 107 | 35 | 47 |
| `sky_whale_ship` | 5 | 5 | 0 |
| `skyarena` | 2 | 1 | 1 |
| `skyvillages` | 1 | 1 | 0 |
| `structory` | 15 | 5 | 2 |
| `supplementaries` | 2 | 0 | 2 |

## Runtime acceptance remains separate

The source build and scoped static validation are complete independently of gameplay. A later fresh-world check should verify river/land sky villages, the three AO Heavenly IDs, houses and Dungeon Crawl across recorded curated biomes, Bathhouse rarity, disabled structures, pool assembly and cross-mod overlap. Use explicit biome IDs; a visible stream does not establish the biome selector underneath it. Record generation timing separately from `/locate` timing. No gameplay pass is claimed.
