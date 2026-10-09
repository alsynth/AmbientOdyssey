# Ambient Odyssey — Structure and biome audit, Test 5 audit1

Updated 9 October 2026. Source version: `0.3.1-structure-test5-audit1`. This is a statically validated continuation candidate; gameplay and release acceptance remain pending.

## Reproducibility and audit scope

The untouched original Test 5 source rebuild matched its original import ZIP byte for byte, passed its 76 scoped gates, and regenerated its audit and three catalogues identically. Original evidence is retained under `evidence/baseline-test5`; `evidence/baseline-reproduction.json` records the rollback hashes.

The expanded audit represents 196 complete binaries: 177 from that original resource snapshot plus 19 newly recovered. There are 26 directly available unique binaries in this continuation, including seven re-supplied baseline JARs. Resource inventories, CRC and SHA evidence are retained; class-reference and extra resource-category inspection are scoped to the supplied binaries. Older binaries have not been freshly re-inspected. 41 logged JAR filenames remain unavailable, listed in `MISSING_JARS.txt`.

| Recorded inventory | Count |
|---|---:|
| Native structure IDs | 1216 |
| Native structure-set IDs | 666 |
| Native template-pool IDs | 4294 |
| Native biome-tag IDs | 1254 |
| Catalogue structure rows, including three declared AO sky clones | 1219 |
| Set catalogue rows, including AO sets and code-only vanilla route | 673 |
| Curated donor biomes | 40 Overworld + 2 Nether |
| Eligibility matrix biome columns | 52 |

No mod count or JSON count establishes successful natural spawning. Candidate grids, weighted members, exclusion zones, dimension restrictions and successful assembly are separate concerns.

## Eligibility catalogue

`STRUCTURE_REGISTRY_CATALOG.csv` records each effective definition's native JAR/path, selector, generation step, height, terrain adaptation, inferred dimension and placement routes. `STRUCTURE_BIOME_MATRIX.csv` has one column per curated/independent diagnostic biome. `STRUCTURE_SET_CATALOG.csv` records placement JSON, spacing, separation, salt, frequency, weights and Moog multipliers. Nested tags, NeoForge AND/OR/NOT selectors and tag removals are resolved from recorded evidence; unnamespaced vanilla biome IDs are normalized to `minecraft:`.

Unresolved Minecraft/base-game and optional tag references remain explicit. The snapshot is not the complete Minecraft 1.21.1 native tag registry. A zero curated-Overworld count can mean a legitimate End/Nether/other-dimension structure, an optional inactive provider or an unresolved tag; it is not an automatic failure. Dimension labels are evidence-based inferences, not extra dimension overrides. The “before” columns use Test 4's saved graph with the newly supplied native provider tags added for comparison.

| Namespace | Native definitions | Changed known curated eligibility | No known curated OW eligibility |
|---|---:|---:|---:|
| `adventuredungeons` | 8 | 6 | 2 |
| `aether` | 4 | 0 | 4 |
| `aether_villages` | 1 | 0 | 1 |
| `alexscaves` | 14 | 0 | 13 |
| `ambient_odyssey` | 0 | 3 | 0 |
| `antiquetradingship` | 1 | 0 | 1 |
| `apotheosis` | 4 | 1 | 1 |
| `archaeology_ruins` | 11 | 0 | 11 |
| `ars_nouveau` | 3 | 0 | 0 |
| `betterend` | 14 | 0 | 14 |
| `betterfortresses` | 1 | 0 | 1 |
| `bettermineshafts` | 13 | 0 | 9 |
| `betterwitchhuts` | 2 | 0 | 0 |
| `biomeswevegone` | 18 | 0 | 12 |
| `block_factorys_bosses` | 5 | 2 | 3 |
| `bosses_of_mass_destruction` | 4 | 1 | 3 |
| `cataclysm` | 16 | 4 | 12 |
| `create_rustic_structures` | 4 | 4 | 0 |
| `ctov` | 78 | 32 | 28 |
| `dungeoncrawl` | 1 | 1 | 0 |
| `dungeons_arise` | 40 | 12 | 10 |
| `dungeons_arise_seven_seas` | 5 | 0 | 0 |
| `echoes_of_the_end__structures_` | 9 | 0 | 9 |
| `end_villager_outpost` | 1 | 0 | 1 |
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
| `minecraft` | 8 | 0 | 6 |
| `mns` | 52 | 0 | 52 |
| `mowziesmobs` | 4 | 0 | 0 |
| `mss` | 35 | 3 | 4 |
| `mtr` | 6 | 0 | 3 |
| `mvs` | 130 | 16 | 14 |
| `natures_spirit` | 4 | 0 | 4 |
| `nova_structures` | 96 | 0 | 41 |
| `pasterdream` | 115 | 0 | 111 |
| `philipsruins` | 17 | 12 | 4 |
| `repurposed_structures` | 107 | 35 | 47 |
| `sky_whale_ship` | 5 | 5 | 0 |
| `skyarena` | 2 | 1 | 1 |
| `skyvillages` | 1 | 1 | 0 |
| `structory` | 15 | 5 | 2 |
| `supplementaries` | 2 | 0 | 2 |
| `totw_modded` | 22 | 0 | 17 |
| `towns_and_towers` | 60 | 0 | 40 |
| `underwater_village` | 17 | 0 | 17 |

## Placement routes and resource collisions

CTOV's actual Java/config registration adds 63 enabled village entries and 11 outposts to vanilla sets via Lithostitched. Its 78 native definitions do not require new independent CTOV grids: three underground villages and the mesa outpost are inactive in the preserved config. `CODE_GENERATED_PLACEMENT_ROUTES.csv` and its class/config evidence enumerate all 74 selected routes. The uncaptured base-game outpost grid is left unknown rather than assigned guessed spacing.

`NATIVE_RESOURCE_COLLISIONS.csv` enumerates 70 IDs supplied by more than one JAR across structures, sets and pools. Snapshot selection order is recorded evidence, not proof of the running pack's priority. In particular, Luki's Grand Capitals and Nature's Spirit both supply `minecraft:villages`, while Luki and Dungeons & Taverns supply `minecraft:village_taiga` with different starts. No arbitrary new winner is forced in this continuation.

The effective membership report records 2 structures with more than one recorded route; `evidence/duplicate-placement-membership-test5.json` contains IDs. There are 16 remaining shared-salt groups in `evidence/shared-placement-salts-test5.json`. Shared salts and membership are review signals; neither alone establishes physical overlap.

## Implemented continuation changes

- Cristel Lib 3.1.7 is bytecode-inspected. It reads native modfile structure-set JSON and builds a runtime pack, updating salt/spacing/separation/frequency and filtering members through per-set toggles. AO's extracted WDA/IDAS members are now also disabled in those native per-set configs, so they cannot be reintroduced by that runtime pack. Bathhouse's native route is off while its separate rare AO route remains enabled. Runtime pack priority and retention of AO-only exclusion fields still need launch evidence.
- All 20 Farmers Structures sets now have bounded spacing/separation and independent signed-32-bit salts. Spacing is `floor(native spacing / sqrt(2))`, with separation scaled proportionally: roughly two times native candidate attempts, not a measured natural-spawn increase. The six already tuned sets are not doubled again. Native members, weights, biome selectors, dimensions, height and exclusions are retained. The invalid native Undergarden salt is repaired. `FARMERS_STRUCTURE_CATALOG.csv` preserves every variant and optional dimension status.
- CTOV's mountain `towers` alias uses its actual singular tower pool/template. Its sand-waystone connector and canonical common pool use the supplied Waystones desert template with legacy jigsaw NBT/orientation migrated to the current connector schema. Geometry, block palette and entities are retained. No arbitrary empty whole-pool workaround is used.
- The malformed Dungeons & Taverns illager-mansion basement pool is strict JSON. Its weight-20 nonexistent “minecraft/empty” template is a real empty element; all 49 real basement room templates, native weights and processors remain. The original four AO pool repairs and their 33 connector proofs are preserved; the continuation contributes 52 template provenance rows.
- Create: Rustic Structures' four direct vanilla selectors and 32 enabled CTOV village/outpost definitions gain appropriate curated donor eligibility through NeoForge OR selectors. Other structure fields and placement ownership remain native.
- Traveloptics' malformed fire tag is repaired; three stale Ancient Ancient Remnant references use the actual `cataclysm_spellbooks` registration. Native entities missing from the installed route are optional. Thirty-three client model JSON repairs correct the NeoForge loader and verified texture/parent paths. Missing developer-test augment models are not fabricated.
- Cataclysm Spellbooks' eleven recipes referring to demonstrably absent own registered items are skipped using a false NeoForge condition while retaining their native payloads. Its missing prison loot-modifier resource gets an asset-backed alias to the existing native cursed-pyramid modifier. No replacement items are invented.

## Preserved Test 5 behavior

Small Blimp and Coliseum remain disabled through native toggles plus the class-verified Integrated API tag. Bathhouse remains 112/48 with frequency 0.5 on its independent owner. Ordinary WDA buildings, 14 IDAS house/farm/inn members and Dungeon Crawl retain their intended supply; Dungeon Crawl is 20/9. Heavenly Overworld clones remain separate from their original End branches. General Sky Whale land coverage and the Frozen Whale climate restriction remain.

Sky Villages retain land, `minecraft:river`, `minecraft:frozen_river`, RU muddy-river and `streamsreflowing:stream` eligibility at 44/32. Oceans remain excluded by the existing Test 5 decision. The user's observation of villages only above oceans does not establish whether the cause was Streams, biome eligibility or placement success. A visible river channel can retain a land biome; runtime observations should record the actual biome ID.

The 40 Overworld + 2 Nether donor roster, FTF preset, Biolith pools, Streams, Tan and TRMT settings are preserved. Born in Chaos remains removed. Artifacts/Enigmatic slot repairs, Simply More's valid-JSON recipe, native ocean/cave/End restrictions and the staged, unapplied Tan open-field plan are retained. No terrain or tree tuning is introduced.

## Staged additions and limits

The eight master-approved additions have primary file metadata selected in `APPROVED_STRUCTURE_ADDITIONS.csv` but are not installed. Exact binary SHA/dependencies/native placement remain unavailable. Explorify's Nether Black Spiral ID and disable mechanism are specifically blocked on its binary. `MOD_STRUCTURE_SCREENING.md` and the installed/future/Create screening CSVs account for other potential providers without treating description triage as a JAR audit or adding unselected mods.

Unresolved IDAS missing templates, Cook/blank jigsaw references, native tag gaps, resource priority and live generation acceptance remain in TODO. Static completion does not depend on an in-game test. Later fresh-world checks must distinguish forced assembly from natural candidates, record actual biome IDs and assess terrain fit, frequency, client models and multiplayer behavior.
