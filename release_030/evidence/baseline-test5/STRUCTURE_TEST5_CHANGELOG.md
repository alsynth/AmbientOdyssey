# Ambient Odyssey — Structure Test 5 changelog

8 October 2026 · Minecraft 1.21.1 · NeoForge 21.1.252 · based on Structure Test 4.

Test 5 moves the structure changes into editable source inputs, repairs verified biome eligibility gaps and separates ordinary buildings from rare landmarks. Sky Villages explicitly remain eligible above rivers, including Streams' registered biome. The locked mod list is unchanged: 237 project/file pairs. Static validation and source rebuilds are recorded separately from later gameplay acceptance.

## Placement changes from Test 4

Spacing/separation are in chunks. Frequency is a placement probability, not a count of successful structures.

| Group | Test 5 placement | Ownership and purpose |
|---|---|---|
| Small Blimp, Coliseum | Disabled | Removed from native/effective membership and all AO grids; native toggles false; class-verified Integrated API disabled tag also applied |
| WDA ordinary buildings | 28/14; salt 1984010501 | One new grid for Illager Campsite (weight 3), Merchant Campsite (3), Mushroom House (2), Greenwood Pub (2), Illager Windmill (1); extracted from the native major pool |
| Bathhouse | 112/48; frequency 0.5; salt 1984010502 | One independent owner; approximately 19% of its previous nominal weighted candidate density |
| Other WDA minor structures | 28/18; frequency 5/6 | Five entries remain; compensates for removing Bathhouse from their pool |
| Remaining WDA major structures | 50/45; frequency 27/38 | No second boosted major-landmark grid; nominal weight compensation after extracting ordinary buildings and removing the two disabled structures |
| Fourteen IDAS houses/inns/farms | 16/8; salt 1984010520 | One independent grid, total weight 59; approximately 1.61 times the former nominal house candidate supply before exclusions/fallback |
| Remaining IDAS common structures | 15/8; frequency 49/108 | Castles, towers and other entries retain nominal weighted rarity accounting |
| IDAS small sites | 18/12; frequency 70/79 | Remove two unusable legacy BYG lumber variants and duplicate Sunken Ship Ruins; keep the native ocean owner |
| Integrated regular villages | 22/14, native owner | Remove the duplicate AO land-village grid; retain native advanced exclusions |
| Dungeon Crawl | 20/9; salt 1984010530 | Verified native `dungeoncrawl:dungeons`; Test 4 was 22/9, giving about 1.21 times nominal candidates |
| Heavenly Challenger OW clone | 72/32; salt 1984010510 | Independent Overworld grid and declared `ambient_odyssey:heavenly_challenger_overworld` structure |
| Heavenly Conqueror OW clone | 84/40; salt 1984010511 | Independent Overworld grid and declared `ambient_odyssey:heavenly_conqueror_overworld` structure |
| Heavenly Rider OW clone | 64/28; salt 1984010512 | Independent Overworld grid and declared `ambient_odyssey:heavenly_rider_overworld` structure |
| Original Heavenly WDA IDs | Existing native major grid, End-only | Remove Test 4's shared extra grid; no extra End candidate supply |

The IDAS ordinary group contains Abandoned House, Bearclaw Inn, Hermit's Hollow, Hunter's Cabin, Brick House, Beekeeper's House, Farmhouse, Fisherman's Lodge, Botanist, Mason House, Abandoned Vineyard, Tudor Pub, Wacky Wares and Pumpkin Cafe. Exact weights are editable in `release_030/structure-density.json`.

The WDA ordinary and Bathhouse grids avoid candidates from native WDA major, IDAS rare and Integrated regular-village sets within six chunks. The IDAS house grid uses its native common-avoid collection plus the remaining IDAS common set within two chunks. These directed candidate exclusions do not establish a global guarantee against bounding-box collisions.

The earlier selected placement tuning is retained where not replaced above: the compiler contains 143 selected placement entries and 103 Moog per-set multipliers. Sky Villages stays 44/32; Integrated air villages stays 65/45; existing Sky Whale set tuning remains. No new global overlap mod or distance rule is enabled.

Nominal comparisons use weighted candidates per grid area (`frequency × weight / total weight / spacing²`). Minecraft's invalid-candidate fallback, biome acceptance, config-library behavior and assembly success affect actual density. In particular, the compensation does not claim measured boss rarity or observed spawn rates.

## Biome eligibility and dimension boundaries

- Add 145 editable provider/sky/optional biome-tag patch entries, backed by native resource IDs and nested selector analysis. Open fields, Prairie, Flower Fields, Sakura, appropriate forests and cool/snowy donors receive targeted coverage.
- Correct the mistaken Overworld exclusion key to `regions_unexplored:blackstone_basin`. Keep it and Infernal Holt out of general Overworld/sky tags. Fix native-temperature classification errors for Maple Taiga, Alpine Clearings, several cool forests, Hot Springs, Highland and Ashen Woodland.
- Replace Sky Villages' native ocean-heavy broad tag with land plus River, Frozen River, RU Muddy River and `streamsreflowing:stream`. Rivers are intentionally allowed. A visible channel may still carry a land biome; that explanation remains untested.
- Give the four general Sky Whale variants land selectors and Frozen Whale a cool taiga/snowy-forest selector; preserve native heights.
- Clone the three exact native Heavenly definitions, changing only their biome selector. Preserve Y=200, native jigsaw pools and all other fields. Make original WDA definitions End-only; keep the new AO copies Overworld-only.
- Patch verified Moog direct-selector gaps while retaining existing frequency tuning. Explicit ocean-themed content stays separate.
- Replace obsolete required IDAS BYG collections and unavailable Aether addon collections with empty optional collections. BYG lumber variants stay disabled because their template palettes use absent `byg:*` blocks; a biome alias would not repair them.
- Keep cave biomes, oceans, Nether, End and the TerraBlender deferred placeholder out of ordinary surface/sky additions where inappropriate.

## Verified asset and compatibility repairs

| Repair | Evidence |
|---|---|
| Foundry corridor gears pool | Two shipped gear templates and matching connectors |
| Mechanical Nest singular decoration pool | Twenty-three shipped library templates and matching tower connectors |
| Cabin Village villager alias | Shipped native villager pool; weights and its legitimate empty outcome retained |
| Cabin fisherman lectern pool | Seven shipped lectern templates with matching connectors and native processors |
| Artifacts all/belt/hands slots | Restore native item memberships cleared by RAR-Compat `replace: true`; preserve extra slot routes and Enigmatic overlay |
| Simply More `matterbane_clean` recipe | Remove the verified extra closing brace; recipe contents unchanged |

No empty repair pools or self-recursive substitutions were invented. Dread Citadel 5/12 and Ancient Mines entrance 2 have no matching assets in the inspected IDAS JAR. CTOV assets could not be inspected. Those repairs remain open with evidence in TODO.

Actual Streams bridge bytecode supports FTF's package/mod ID; the fallback reflects unavailable preparation-time terrain rather than a missing namespace. No speculative binary patch is included. Traveloptics and Cataclysm Spellbooks diagnostics are recorded but await their unavailable JARs. Tan open-field tuning is prepared in a separate staged plan; tree, terrain, biome-size, climate, wildlife and QoL tuning are not applied here.

## Sources, reports and scope

The full builder runs the worldgen, density, compatibility and repair compilers. Compiler-owned folders are regenerated, clearing deleted Test 3/4 grids. Sorted ZIP entries and fixed metadata support byte-for-byte reproducible exports. The source archive includes the locked baseline, editable inputs, compiled overrides, reusable audit/validation scripts, native resource snapshots, JAR hashes, class/NBT evidence and cached Test 4 comparisons.

The actual audit inspected 177 complete CRC-verified JARs: 908 native structures, 584 sets, 3,488 template pools and 1,094 biome tags. The catalogue includes three new declared AO clones, for 911 rows. The biome matrix has 52 biome columns; the effective set catalogue has 590 rows. Two native Moog well duplicate memberships and 11 shared-salt groups remain documented rather than silently rewritten.

**Coverage is incomplete:** full `mods1.zip`/`mods3.zip` transfers failed HTTP 403, leaving 60 JAR names from the supplied runtime unavailable. CTOV, Cristel Lib, Seven Seas, Traveloptics, Cataclysm Spellbooks and other missing providers remain explicitly uncertified. Static success does not establish a registry load, in-game placement, real density or performance. No gameplay test was required or performed to finish this static work.
