# v0.3.1-structure-test5-audit1 — existing-stack audit and repairs

Expanded JAR resource evidence to 196 binaries, repaired verified Cristel/CTOV/D&T resources, tuned all 20 Farmers candidate grids, added curated CTOV/Rustic selectors and verified Traveloptics/Cataclysm Spellbooks repairs. The 237 mod pins and terrain settings are unchanged. Eight approved additions remain staged pending binary/dependency audits; gameplay acceptance is pending. See STRUCTURE_TEST5_CHANGELOG.md and MOD_STRUCTURE_SCREENING.md for evidence and scope.

# Ambient Odyssey — Changelog

## v0.3.1-structure-test2 — biome eligibility and compatibility test

- Add the `ao_compatibility` Paxi datapack. It classifies the active Regions Unexplored, Oh The Biomes We've Gone, Biomes O' Plenty and Nature's Spirit Overworld donors in the common `minecraft`, `c`, and `forge` biome tags used by the installed structure providers.
- Add focused entries for providers that use direct vanilla-only lists: Bosses' Rise dragon/yeti structures, Bosses of Mass Destruction cold structures, Dungeons Arise open-field landmarks, and Ice and Fire mausoleums.
- Add a Curios bridge for Enigmatic Legacy+ 1.1.2. It repeats the fork's coloured and named amulets in `curios:amulet`, adds the fork-only `the_necklace`, and adds the omitted `darkest_scroll` to `curios:scroll`.
- Keep the structure-test1 placement increases and the current biome pools unchanged. This test isolates whether modded biomes were being rejected by structure biome selectors.
- Static archive validation is required; fresh-world generation and Curios slot behavior remain runtime checks. See `BIOME-COMPATIBILITY-TEST2.md`.

## v0.3.1-structure-test1 — first structure density test

- Include Integrated Patches 1.2.0 by default, Integrated Mowzie's Mobs 1.3.2, Integrated Bosses of Mass Destruction 1.0.0 and their required Amendments 2.1.10 dependency. Other existing mod pins are retained.
- Remove Companions! and Modern Companions from the export and remove their imported configs.
- Disable Alex's Mobs seal fishing rewards using an empty loot-table override.
- Increase 140 selected placement settings across 35 config files and apply 103 scoped Moog frequency multipliers. Apotheosis towers move from 26/18 to 12/6 spacing/separation, about 4.69 times the candidate density. Most selected land/sky groups increase about two to three times.
- Add extra land/sky candidate sets for the mixed WDA, IDAS rare and Integrated Villages groups while retaining their original mixed sets. Original structure definitions, biome selectors, weights and copied exclusion fields are retained.
- Carry forward the current FTF preset, biome pools and climate/tree settings. Frequency testing comes first; wildlife, eligibility/spawning defects, overlaps, Traveloptics and Cataclysm Spellbooks repairs are deferred.
- Static export validation is required; runtime launch and actual placement remain user test gates.

## v0.3.1 — Biolith and FTF worldgen test

- Working sources now exclude Companions! and Modern Companions and remove their imported configs. Existing test exports will receive these removals in the next requested build.

- Add Biolith 3.0.14 for NeoForge 1.21.1, pinned to CurseForge project 852512/file 8435635.
- Supply a Paxi-loaded datapack with 43 weighted replacement rules for 12 vanilla surface biomes and 20 temperature guards. Native curated outputs remain intact; all replacement outputs belong to the existing curated roster.
- Retain nominal vanilla weights of 5% for the selected plains/flower/forest/birch targets and 0.5% for savanna/jungle targets. These are configurable pool weights, not measured global biome-area percentages.
- Include the named Ambient Odyssey 0.3.1 FTF user preset: continent scale 6500 and river count 15, based on the pinned 4000-scale/10-river template. Select this preset in Customize when creating a fresh world.
- Carry forward the 0.3.0.2 biome settings: vanilla Overworld region weight 1, BWG region weights 12/12/12, RU Orchard weight 30. Oceans/caves/Nether/End are outside the new replacement layer.
- Include previously requested Born in Chaos removal, NeOculus and video defaults in the full export. The small worldgen update only adds Biolith and worldgen settings to an existing instance.
- Static validation passed. Runtime launch, biome distribution, structure access and cave/ocean review remain user test gates. See TESTING-0.3.1.md.

## v0.3.0-pre1 — worldgen test

- Remove Amaranth and its unused Twigonometry dependency after a confirmed config-lifecycle startup failure. Remove the obsolete Amaranth ordering override and config; keep TerraBlender for the remaining biome mods. Runtime verification of this revised export is pending.
- Retain the early-window workaround. The latest user launch passed OpenGL/Embeddium initialization and reached mod construction; the reported anticheat conflict remains unconfirmed.

- Preserve v0.2.10 pins; replace Tectonic with FreeTerraForged and add the selected terrain/biome/structure wave.
- Apply the remaining 42-biome donor roster (40 Overworld, two Nether) and import working AOconfigs settings, quests and Tan assets.
- MTR temple replacements enabled; MTR stronghold disabled in favor of Integrated Stronghold.
- Use native Create/BWG milling plus 18 global datapack extensions.
- Supply a separate Integrated Patches A/B export and reproducible locked builder.
- FTF defaults were accepted in prior tests; retain them while verifying the current combined mod set. Terrain and structure tuning follow once the set works as intended. See TESTING-0.3.0.md.

## v0.2.10

- Performance wave A: added Noisiumed, AllTheLeaks, Smooth Chunk Save, FastSuite and Clumps while freezing the v0.2.9 content baseline.

## v0.2.9

- Locked in Astrological + BetterEnd: New Dawn for continued End testing; restored T.O. Magic via the original mod plus the approved Ambient Odyssey registry fix.

## v0.2.8

- Added Astrological as the first post-Phantasm End-worldgen replacement test.

## v0.2.7

- Restored Ice & Fire CE and removed End's Phantasm after the v0.2.6 worldgen A/B.

## v0.2.6

- Diagnostic A/B: temporarily removed Ice & Fire CE and corrected the FTB Chunks map-unbind identifier.

## v0.2.5

- Diagnostic A/B: removed Chunk Sending entirely after 3.9 and 4.1 showed no meaningful improvement to chunk/teleport stalls.

## v0.2.4

- Diagnostic patch: updated Chunk Sending to 4.1, made the FTB/voice/accessory keybind defaults reliable, and removed the Accessories inventory-button clutter while keeping Ice & Fire + Phantasm unchanged for controlled worldgen testing.

## v0.2.3

- Updated the Simply Swords/More tooltip stack, added clean pack defaults for narrator/FTB Chunks, and disabled Bosses'Rise's extra dodge roll and oversized boss bars.

## v0.2.2

- Fixed the Simply More tooltip crash, raised NeoForge to 21.1.252, removed JEBr, and added working CurseForge RAM/icon metadata plus an Accessories button offset.

## v0.2.1

- Updated Cataclysm Spellbooks + JEI for registry/search testing; reduced JEI search indexing overhead.

## v0.2.0

- First major content wave: restored donor exploration/RPG/QoL content, Ars Nouveau integration, and a patched 1.21.1 T.O. Magic build.

## v0.1.12

- Replaced Sodium with Embeddium 1.0.15 to resolve the Supplementaries/Sodium startup conflict.

## v0.1.11

- Downgraded Sodium 0.8.13 → 0.6.13 to fix the early OpenGL startup stall.

## v0.1.10

- Added Sodium, ImmediatelyFast, and Lithium as the baseline performance stack.

## v0.1.9

- Parked JET, Dungeon Now Loading, Crazy Chambers, and Desire Paths/GSTools after log-confirmed initialization/worldgen errors.

## v0.1.8

- Chunk-performance diagnostic pass: added Structure Essentials, Chunk Sending, and ServerCore; capped Just Enough Threads at 4 workers.

## v0.1.7

- Fixed Ice & Fire CE's vanilla-menu toggle and added Just Enough Threads for JEI startup/world-entry performance.

## v0.1.6

- Performance/isolation pass: parked Cobblemon + Shine, added ModernFix/FerriteCore, and pinned Desire Paths/GSTools to matching v1.40 builds.

## v0.1.5

- Restored vanilla UI/loading visuals; added JEI and exploration/QoL JEI addons.

## v0.1.4

- Parked Celestial Artifacts/Core due to their broken 1.21.1 L2Tabs compatibility; removed the temporary Accessories pin.

## v0.1.3

- Tried an Accessories beta.49 pin for the L2Tabs crash; it did not resolve it.

## v0.1.2

- Removed T.O Magic 'n Extras: its deprecated 1.21.1 build crashes during mod registration.

## v0.1.1

- Updated NeoForge to 21.1.248.
- Added the missing Cupboard dependency.
