# Ambient Odyssey — Structure-provider screening, Test 5 audit1

Updated 9 October 2026. The current master TODO authorizes eight additions; they remain staged because their exact binaries are unavailable. This export repairs the audited existing stack. It does not install unselected Create addons or promote the project to 0.4.0.

## Evidence and coverage

- 196 complete binaries are represented by CRC/SHA/resource evidence: the preserved 177-JAR baseline plus 19 newly recovered binaries.
- 26 unique complete binaries were available for direct inspection this continuation: those 19 plus 7 re-supplied baseline JARs. Their class-reference screen is recorded in `evidence/new-jar-screen.json` and `evidence/new-jar-details.json.gz`.
- 41 exact logged JAR filenames remain unavailable. `MISSING_JARS.txt` is the manual-upload list; these are separate from the eight new additions.
- The old large-archive transfer record is historical. The current full `mods2.zip` transfer returned HTTP 403; old resource evidence is retained without claiming a new binary inspection.
- `INSTALLED_MOD_STRUCTURE_SCREENING.csv` has one row per audited JAR with SHA, resource counts and evidence scope. Zero structure JSON is not proof of zero worldgen.

## Newly recovered existing-profile binaries

| JAR | Screen | Structures | Sets |
|---|---|---:|---:|
| `DungeonsAriseSevenSeas-1.21.x-1.0.4-neoforge.jar` | STRUCTURE_PROVIDER | 5 | 1 |
| `YungsApi-1.21.1-NeoForge-5.1.9.jar` | WORLDGEN_DATA_OR_CODE_REVIEW | 0 | 0 |
| `YungsBetterEndIsland-1.21.1-NeoForge-3.1.2.jar` | WORLDGEN_DATA_OR_CODE_REVIEW | 0 | 0 |
| `YungsBetterMineshafts-1.21.1-NeoForge-5.1.1.jar` | STRUCTURE_PROVIDER | 13 | 1 |
| `YungsBetterNetherFortresses-1.21.1-NeoForge-3.1.5.jar` | STRUCTURE_PROVIDER | 1 | 1 |
| `YungsBetterWitchHuts-1.21.1-NeoForge-4.1.1.jar` | STRUCTURE_PROVIDER | 2 | 2 |
| `[Neoforge]ctov-3.6.3.jar` | STRUCTURE_PROVIDER | 78 | 0 |
| `cataclysm_spellbooks-1.1.14-1.21.jar` | NO_STRUCTURE_ROUTE_DETECTED | 0 | 0 |
| `create_rustic_structures-1.0.1-neoforge-1.21.1.jar` | STRUCTURE_PROVIDER | 4 | 4 |
| `cristellib-neoforge-1.21.1-3.1.7.jar` | WORLDGEN_DATA_OR_CODE_REVIEW | 0 | 0 |
| `curios-neoforge-9.5.1+1.21.1.jar` | NO_STRUCTURE_ROUTE_DETECTED | 0 | 0 |
| `dungeons-and-taverns-v4.4.4 [NeoForge].jar` | STRUCTURE_PROVIDER | 97 | 34 |
| `echoes_of_the_end__structures NeoForge Fabric 1.21.1 -12.00.13.jar` | STRUCTURE_PROVIDER | 9 | 9 |
| `end_villager_outpost-1.0.0-neoforge-1.21.1.jar` | STRUCTURE_PROVIDER | 1 | 1 |
| `t_and_t-fabric-neoforge-1.13.11.jar` | STRUCTURE_PROVIDER | 60 | 3 |
| `totw_modded-neoforge-1.21-1.0.9.jar` | STRUCTURE_PROVIDER | 22 | 9 |
| `traveloptics-4.4.0.1-1.21.1.jar` | NO_STRUCTURE_ROUTE_DETECTED | 0 | 0 |
| `underwater_village-1.0.2-neoforge-1.21.1.jar` | STRUCTURE_PROVIDER | 17 | 17 |
| `waystones-neoforge-1.21.1-21.1.46.jar` | WORLDGEN_DATA_OR_CODE_REVIEW | 0 | 0 |

CTOV has 78 native structure definitions and zero native structure-set JSON files. Its inspected Java/config route adds 63 enabled village entries and 11 outpost entries to vanilla placement sets through Lithostitched. The 74 routes are in `CODE_GENERATED_PLACEMENT_ROUTES.csv`; actual runtime application remains untested.

YUNG's Better End Island changes End generation through EndDragonFight/spike/gateway/platform code rather than standalone structure JSON. Waystones has feature, pool and Lithostitched village integration routes. Both must remain in worldgen screening even when the standalone structure-definition count is zero. Cristel Lib and YUNG's API are frameworks; framework class references alone do not make them independent landmark providers.

## Eight approved additions — metadata selected, installation pending

| Mod | CurseForge project / file | Exact proposed JAR |
|---|---|---|
| YUNG's Extras | 1015146 / 5812546 | `YungsExtras-1.21.1-NeoForge-5.1.1.jar` |
| YUNG's Bridges | 1015149 / 5812553 | `YungsBridges-1.21.1-NeoForge-5.1.1.jar` |
| Structory: Towers | 783522 / 7078283 | `Structory_Towers_1.21.x_v1.0.14.jar` |
| Archaion | 1620396 / 8983496 | `archaion-1.21.1-1.4.4.jar` |
| Explorify | 698309 / 8082824 | `Explorify v1.6.5.mod.jar` |
| Additional Structures | 297680 / 6584803 | `AdditionalStructures-1.21-(v.6.3.2-NEO).jar` |
| Create: Structures Arise | 1010066 / 8837992 | `Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar` |
| Create: Easy Structures | 949158 / 6344382 | `create_easy_structures-0.2a-neoforge-1.21.1.jar` |

Primary file URLs and verification date are in `APPROVED_STRUCTURE_ADDITIONS.csv` and editable `release_030/approved-structure-additions.json`. All eight have `enabled=false`, `binary_audited=false`, `dependencies_verified=false` and no invented SHA-256. They are absent from the locked candidate manifest. `APPROVED_ADDITION_JARS.txt` provides the separate upload list.

For each binary, inspect native definitions, placement sets, pools/NBT, tags, features, biome modifiers, builtin packs and registration/mixin code; verify dependencies against the exact installed pins. Select native placement owners before adjusting candidate density. Explorify must remain out of the export until the exact Nether Black Spiral ID and disabling mechanism are verified; no guessed ID or ineffective empty-tag patch is included.

## Other Create addons

| Candidate | Evidence | Current decision |
|---|---|---|
| Create: Rustic Structures | Actual binary: 4 structures, 4 sets, 4 pools; curated selector repairs included. | Retained; audited and repaired |
| Create: Structures Arise | Approved structure addon; pinned file metadata supports 1.21.1 NeoForge. Native content pending. | Approved; blocked on binary audit |
| Create: Easy Structures | Approved structure addon; pinned file metadata supports 1.21.1 NeoForge. Native content pending. | Approved; blocked on binary audit |
| Create: Structures Overhaul | Official project describes biome-themed natural, locatable structures and optional BOP integration. | Unselected; metadata/version and binary audit required |
| Create: Let The Adventure Begin | Official project describes Create-themed structures; 1.21.1 release metadata was located. | Unselected; binary and dependency audit required |
| Create: structures | Official project describes railway stations and requires several Create addons; latest file title/game-tag mismatch needs resolution. | Unselected; do not select a file from its filename alone |
| Create: The Factory Must Grow / The Factory Must Work | Oil-deposit/worldgen feature routes warrant inspection; this does not establish natural building generation. | Unselected; exact project/version and feature/code audit required |
| Create: Diesel Generators / New Age and other technical addons | No binary absence proof available; machinery descriptions alone do not certify absence of features or structures. | Unselected; screen exact binaries before any future installation |

`CREATE_ADDON_STRUCTURE_SCREENING.csv` includes primary project links. Public project/file descriptions establish a screening priority, not a completed binary audit or permission to install. Structures, worldgen features such as oil deposits, and manually/instance-created content must be recorded separately.

## Future pack candidates

`FUTURE_MOD_STRUCTURE_SCREENING.csv` preserves all 166 numbered candidates from the 6 October registry, with a first-pass description screen. Potential worldgen, village, dungeon, dimension, boss or terrain routes are flagged for binary review. Other descriptions receive “no structure claim in recorded description”, never a certified “adds no structures”. The current master TODO supersedes the registry's old install preferences, particularly StructureOverlapless and competing terrain stacks. The registry is an audit backlog, not an installation list.

## Remaining work

Prioritize the unavailable Create, dimension and worldgen libraries/providers, including Create, CreateOPlenty, Undergarden, Deep Aether, Deeper and Darker, Bumblezone, Twilight Forest, Dimensional Doors, TRMT, Citadel/Zeta/Corgilib/WorldWeaver/Wunderlib and the Cook-related assets. Library status alone does not prove a JAR is irrelevant; dependencies can carry assets or code routes.

The current catalogues cover recorded native definitions and code-derived CTOV routes. They retain unresolved base-game/optional tags and 70 native structure/set/pool resource collisions. Actual runtime resource priority, Cristel/Paxi priority, successful natural generation and fresh-world density remain acceptance tasks. They are not prerequisites for delivering this static repair candidate.
