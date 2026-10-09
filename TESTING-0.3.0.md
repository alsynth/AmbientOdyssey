# Ambient Odyssey 0.3.0-pre1 — test build

This is a reproducible world-generation test export, not a runtime-certified release. Minecraft 1.21.1, NeoForge 21.1.252, recommended memory 8192 MB. Import the ZIP itself into a separate CurseForge profile. The ZIP has `manifest.json` at its root and a root `overrides` directory. Use a new world.

## What changed

The exact v0.2.10 manifest is the baseline. Tectonic is removed; every other baseline file ID is preserved, including its five performance additions. Farmers Structures was already installed. The supplied working v0.2.9 export added eight projects and omitted seven baseline projects; shared project file IDs were identical. AOconfigs.zip carries the same 222-project manifest as that working export.

Added: FreeTerraForged, Streams Reflowing, Tan's Huge Trees, The Roads More Travelled, BWG, Nature's Spirit, Nature's Compass, MTR, YUNG's Better Mineshafts, YUNG's Better Witch Huts, Antique Trading Ship, CorgiLib, Oh The Trees You'll Grow and NeoForge Paxi. Ember's Floating Islands and Moog's Structure Lib already existed on the baseline pins and are retained. The resulting base manifest has 234 projects. Amaranth and its unused Twigonometry dependency are removed at the user's request after the latest confirmed startup failure.

The base export excludes Integrated Patches. The separate `-integrated-patches` export changes only that single manifest entry. Crazy Chambers and the rejected alternatives remain out. DH and overlap-control mods wait for later tests. TRMT creates paths through walking/erosion; it does not generate a connected road network.

## Working-export settings recovered

Carried forward 620 config/asset files before adding the release's own files, including the WDA FTB Quests chapter/rewards, keybinds and client settings, IDAS/Integrated Villages/Towns and Towers/structure configs, TRMT erosion settings, and the Tan main tree asset pack with its tree rules. Personal voice-chat state, search caches, backups and generated Tan development extraction are excluded. The main Tan asset ZIP is retained intact. Its automatic update check is disabled so A/B profiles use the same assets.

MTR replaces vanilla desert/jungle temples. Both its stronghold replacement and `mtr:stronghold` are disabled, leaving Integrated Stronghold as owner. Its ocean-monument replacement stays off. IDAS's vanilla-desert-pyramid suppression is switched off so it does not compete with MTR's replacement. Other imported structure frequency values are retained; no new density claim is made without the same-seed survey.

## Exact curated donor roster

| Donor | Enabled biome paths | Count |
|---|---|---:|
| Regions Unexplored | ashen_woodland, cold_deciduous_forest, fen, flower_fields, frozen_pine_taiga, grassland, hyacinth_deeps, blackstone_basin, grassy_beach, icy_heights, maple_forest, marsh, muddy_river, orchard, redwoods, rocky_meadow, rocky_reef, spires, infernal_holt | 19 |
| BWG | lush_stacks, bayou, crag_gardens, sakura_grove, ebony_woods, prairie, redwood_thicket, maple_taiga, skyris_vale, weeping_witch_forest, zelkova_forest, shattered_glacier, frosted_coniferous_forest | 13 |
| BOP | auroral_garden, highland, hot_springs, ominous_woods, pumpkin_patch, snowblossom_grove, volcano | 7 |
| Nature's Spirit | alpine_clearings, floral_ridges, windswept_sugi_forest | 3 |

Prefixes are respectively `regions_unexplored:`, `biomeswevegone:`, `biomesoplenty:`, `natures_spirit:`. Total: 42, including 40 Overworld biomes and two Nether biomes. Ars Nouveau's Archwood Forest and other independent biome providers are preserved.

| Original label | Config decision |
|---|---|
| Blackstone Basic | `regions_unexplored:blackstone_basin`; Nether alongside Infernal Holt |
| Spikes | `regions_unexplored:spires`, confirmed by user |
| Cherry Blossom Forest | `biomeswevegone:sakura_grove` |
| Snowblossom Forest | `biomesoplenty:snowblossom_grove` |
| BWG Amaranth Forest / Autumnal Valley | Deleted as requested; absent from selected BWG version |
| Mindless Rosery / Anthocyanin Forest | Removed with Amaranth at the user's request |
| RU Cold Deciduous Forest / Rocky Meadow | Retired by RU 0.6.2, but resources remain; explicit native RU placements restore them for testing |

Unlisted biomes from these four donor mods are disabled, including BOP's unlisted cave/Nether/End biomes. Native configuration is used throughout. The two retired RU placements use snowy taiga and meadow as targets, each weight 30; these placement choices require in-game approval. Other RU placement weights/climate parameters are preserved.

## Compatibility handling

- Retain `earlyWindowControl = false` to bypass NeoForge's early loading window. Earlier native exits affected other modpacks too; Windows reported a stack overflow in NVIDIA's `nvoglv64.dll`. In `latest(20261007-221724).log`, OpenGL and Embeddium initialized successfully and startup reached mod construction. The user had closed another game with active anticheat; its involvement remains unconfirmed.

- Create 6.0.10 supplies 78 native BWG milling recipes. The AO integration datapack adds only the 18 inputs absent from that native set. Paxi supplies it globally. The standalone Create/BWG addon is omitted because its embedded Minecraft version range excludes 1.21.1.
- Nature's Compass's published NeoForge file also declares `[1.21,1.21.1)`. The supplied FML config applies the narrow native override `naturescompass = ["-minecraft"]`; original JAR bytes remain untouched. This removes only the erroneous Minecraft constraint. Actual Compass use must be verified before promoting the build.
- Amaranth 1.3.1 failed during construction even after its TerraBlender ordering override was recognized: `IllegalStateException: Cannot get config value before config is loaded` in `terrablender.api.Regions`. Amaranth, its config, the ordering override and its unused Twigonometry dependency are removed. No companion fix is included. Keep TerraBlender and Kotlin for Forge because other installed mods require them. For an existing profile, delete `amaranth-neoforge-1.21.1-1.3.1.jar` and, if present, `mc1.21.1-0.1.2-neoforge.jar` (Twigonometry); remove the `amaranth` entry from `config/fml.toml` while preserving the Nature's Compass override. A fresh import already contains this cleanup.
- The CurseForge TRMT metadata lists Fabric API, but the NeoForge JAR requires only NeoForge/Minecraft. Fabric API is not added.
- New required libraries are pinned. Existing TerraBlender, YUNG's API, Integrated API, Kotlin for Forge, Create and GeckoLib remain on their baseline pins.

## Current verification, then tuning

1. Launch the base profile without Amaranth and check `latest.log` for dependency, registry, recipe and config decoding failures. Confirm all four donor toggle files survive startup with the intended enabled set. Check the WDA quest chapter and existing keybinds.
2. **Use FTF with its default settings.** The previous tests used those defaults and the user accepted the terrain. No custom preset is missing or needs recovery. Select FTF for new test worlds and keep its settings unchanged while verifying the combined mod set.
3. Record `/seed`, preset, render/simulation distances and graphics settings. Create fresh worlds for each variant. Test biome discovery (especially both restored RU biomes, Sakura Grove and Snowblossom Grove), marine/coastal transitions, Streams rivers, and Tan trees against steep terrain/structures. Confirm Compass searches work.
4. Confirm MTR desert/jungle temples, Integrated Stronghold, YUNG mineshafts/witch huts, trading ships and floating islands. Inspect giant structures and boss landmarks for clipping. Preserve each tested world's preset and seed.
5. At 8/6 render/simulation distance, time world creation, spawn settling, a 5–10k fresh-chunk teleport, Nether round trip and End entry/teleport. Then repeat at 14/12. Record generation/settling separately from comparable-scene FPS. Avoid comparing two profiles with different generated chunk histories.
6. Put `AO-Benchmark-0.3.0.zip` into the new test world's `datapacks` folder and run `/reload`. Run it manually with `/function ao_benchmark:start`. It logs 180 locate results (nine points × the same 20 structure IDs seen in latest(10).log). `/function ao_benchmark:stop` stops future steps. This is a nearest-structure survey, not a density or overlap measurement; pair it with actual terrain inspection. Large search distances may stall the game.
7. Repeat with the Integrated Patches variant, same seed/preset/settings, and compare launch noise, search failures, structure placement and timings. Promote only after this separate A/B passes.

The FTF defaults were tested previously and accepted by the user. The current priority is verifying that the selected mods and curated biomes work together as intended. After that passes, adjust FTF terrain settings alongside structure frequency and placement tuning.

Static ZIP integrity, manifest locks, donor resource IDs, native config schema names, TOML parsing, AO JSON and recipe input/output IDs were checked. The latest user launch passed graphics initialization and failed during Amaranth construction. The rebuilt set without Amaranth awaits a user launch and has not been launched in this environment. No structure rarity retuning, pregeneration or release publishing is claimed complete.

## Rebuild

Extract the source bundle, then run `python3 build_curseforge_pack.py`. For the isolated variant run `python3 build_curseforge_pack.py --integrated-patches`. The builder resolves nothing online and fails on unexpected baseline drift. `release_030/release-lock.json` records exact project/file IDs and the config import provenance. `requests.json` remains a human-readable inventory; the lock, not live project resolution, controls these builds. Do not promote `pre1` to stable without the runtime gates above.
