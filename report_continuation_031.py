"""Deterministic prose for the expanded offline structure catalogue."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
E = ROOT / 'release_030/evidence'


def audit_report(snapshot, summary, table):
    coverage = json.loads((E / 'jar-audit-coverage-test5.json').read_text())
    return f'''# Ambient Odyssey — Structure and biome audit, Test 5 audit1

Updated 9 October 2026. Source version: `0.3.1-structure-test5-audit1`. This is a statically validated continuation candidate; gameplay and release acceptance remain pending.

## Reproducibility and audit scope

The untouched original Test 5 source rebuild matched its original import ZIP byte for byte, passed its 76 scoped gates, and regenerated its audit and three catalogues identically. Original evidence is retained under `evidence/baseline-test5`; `evidence/baseline-reproduction.json` records the rollback hashes.

The expanded audit represents {summary['inspected_jars']} complete binaries: 177 from that original resource snapshot plus 19 newly recovered. There are {coverage['current_session_complete_jars']} directly available unique binaries in this continuation, including seven re-supplied baseline JARs. Resource inventories, CRC and SHA evidence are retained; class-reference and extra resource-category inspection are scoped to the supplied binaries. Older binaries have not been freshly re-inspected. {len(coverage['unretrieved_logged_jars'])} logged JAR filenames remain unavailable, listed in `MISSING_JARS.txt`.

| Recorded inventory | Count |
|---|---:|
| Native structure IDs | {summary['native_structures']} |
| Native structure-set IDs | {summary['native_structure_sets']} |
| Native template-pool IDs | {len(snapshot['resources']['worldgen/template_pool'])} |
| Native biome-tag IDs | {len(snapshot['resources']['tags/worldgen/biome'])} |
| Catalogue structure rows, including three declared AO sky clones | {summary['catalogue_rows']} |
| Set catalogue rows, including AO sets and code-only vanilla route | {summary['effective_structure_sets']} |
| Curated donor biomes | {summary['curated_ow_biomes']} Overworld + 2 Nether |
| Eligibility matrix biome columns | {summary['matrix_biome_columns']} |

No mod count or JSON count establishes successful natural spawning. Candidate grids, weighted members, exclusion zones, dimension restrictions and successful assembly are separate concerns.

## Eligibility catalogue

`STRUCTURE_REGISTRY_CATALOG.csv` records each effective definition's native JAR/path, selector, generation step, height, terrain adaptation, inferred dimension and placement routes. `STRUCTURE_BIOME_MATRIX.csv` has one column per curated/independent diagnostic biome. `STRUCTURE_SET_CATALOG.csv` records placement JSON, spacing, separation, salt, frequency, weights and Moog multipliers. Nested tags, NeoForge AND/OR/NOT selectors and tag removals are resolved from recorded evidence; unnamespaced vanilla biome IDs are normalized to `minecraft:`.

Unresolved Minecraft/base-game and optional tag references remain explicit. The snapshot is not the complete Minecraft 1.21.1 native tag registry. A zero curated-Overworld count can mean a legitimate End/Nether/other-dimension structure, an optional inactive provider or an unresolved tag; it is not an automatic failure. Dimension labels are evidence-based inferences, not extra dimension overrides. The “before” columns use Test 4's saved graph with the newly supplied native provider tags added for comparison.

| Namespace | Native definitions | Changed known curated eligibility | No known curated OW eligibility |
|---|---:|---:|---:|
{table}

## Placement routes and resource collisions

CTOV's actual Java/config registration adds 63 enabled village entries and 11 outposts to vanilla sets via Lithostitched. Its 78 native definitions do not require new independent CTOV grids: three underground villages and the mesa outpost are inactive in the preserved config. `CODE_GENERATED_PLACEMENT_ROUTES.csv` and its class/config evidence enumerate all 74 selected routes. The uncaptured base-game outpost grid is left unknown rather than assigned guessed spacing.

`NATIVE_RESOURCE_COLLISIONS.csv` enumerates 70 IDs supplied by more than one JAR across structures, sets and pools. Snapshot selection order is recorded evidence, not proof of the running pack's priority. In particular, Luki's Grand Capitals and Nature's Spirit both supply `minecraft:villages`, while Luki and Dungeons & Taverns supply `minecraft:village_taiga` with different starts. No arbitrary new winner is forced in this continuation.

The effective membership report records {summary['remaining_native_duplicate_structures']} structures with more than one recorded route; `evidence/duplicate-placement-membership-test5.json` contains IDs. There are {summary['shared_salt_groups']} remaining shared-salt groups in `evidence/shared-placement-salts-test5.json`. Shared salts and membership are review signals; neither alone establishes physical overlap.

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
'''
