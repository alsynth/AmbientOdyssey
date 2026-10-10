# Ambient Odyssey — consolidated candidate register (content first)
**Updated:** 10 October 2026. **Source branch:** `content/0.4.0d-content-first-expansion` (draft, do not auto-merge). **Purpose:** preserve all prior user mod/resource-pack nominations before proposing more unrelated mods. Candidate ≠ installed; staged ≠ gameplay-verified. The user chooses content; do not treat research suggestions as implicit authorization to install.

## Official intake documents / truth hierarchy
1. [Original nine-theme content priorities](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/CONTENT_EXPANSION_0_4_IMPLEMENTATION_PLAN_2026-10-10.md): life/settlements, structures/discoveries, underground, wildlife, ocean, QoL, decoration/ambience, dimensions, food/farming. This was the original expansion strategy, not merely a cosmetic checklist.
2. [19-item user visual/fauna nominations](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/CONTENT_EXPANSION_VISUAL_FAUNA_ADDENDUM_2026-10-10.md): every original phrase recorded below and original project/license/loader research preserved.
3. [Both user QoL/render candidate batches](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/QOL_VISUAL_RENDERING_BACKLOG_2026-10-10.md): exact names and conflict research below.
4. [Structure source screens](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/FUTURE_MOD_STRUCTURE_SCREENING.csv), [installed structure screens](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/INSTALLED_MOD_STRUCTURE_SCREENING.csv), [Create addon choices](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/CREATE_ADDON_STRUCTURE_SCREENING.csv): historic structure candidates and carefully limited additions, **not** an invitation to automatically reintroduce rejected providers.
5. [Exploration titles and discovery journal](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/EXPLORATION_DISCOVERY_SYSTEM_PROPOSAL_2026-10-10.md), [expanded source/compatibility matrix](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/CONTENT_EXPANSION_ROUND2_INSTALLED_MOD_COMPAT_PREFLIGHT_2026-10-10.md), [complete 0.4c wildlife list](https://github.com/alsynth/AmbientOdyssey/blob/content/0.4.0d-content-first-expansion/docs/audits/CONTENT_040C_ALL_WILDLIFE_AND_FRIENDLY_MOB_CATALOG_2026-10-10.md).

## Confirmed status of the current intake
- **Already staged in 0.4b:** Guard Villagers, Easy NPC Core/UI, Better Archeology, Naturalist, Villager Names/Collective, Cosy Critters, Polytone, Foxified Dense Flowers, Resourcify, Swinging Lanterns, Atmosfera Neo, plus 5 resource packs (Rainbow's Foliage Polytone, Os' Colorful Grasses Mix, Bushy Pink Petals, Torches Reimagined, Extended Illumina). Controlling and FTB XMod Compat were inherited from 0.4a. **0.4b was user-playtested; 0.4c newer tuning is not yet Minecraft-tested.**
- **Removed by user decision:** Galosphere. **Rejected:** MineColonies, FDstructure, Easy Anvils, unapproved Create structure/rail additions. **Deferred until after quests:** MCA Reborn and more bridges. **Experimental, parked:** Big Globe, Blue Skies without native verified target, Fabric-only Mine Cells/Connector and renderer-switch dependent LOD/CTM.
- **0.4d draft is NOT a user-approved final roster:** seven content/compat proposals (Mutant Monsters, Illager Invasion, Chipped, Handcrafted, Dusty Decorations, Night Lights, Apothic Combat) plus Athena library. **Only Mutant Monsters is expressly accepted by the user at this checkpoint, conditional on substantially rare natural spawns**. Other six remain experimental candidates, not decisions to ship.
- **Resource-pack caution:** having CurseForge resource-pack references in manifest does not prove CurseForge put the files into `resourcepacks/` or that players enabled them. Verify when doing a consolidated content test.

## User visual/fauna/resource-pack nominations (original 20 rows incl. seasonal alternatives)
| Original nomination / topic | Registry decision as of 10 Oct |
|---|---|
| Fairer Phantoms | Park: official NeoForge 1.21.1 not demonstrated |
| rainbows foliage politone edition; shaders real time shadows High | Staged in 0.4b; enable/test resource-pack layering |
| Os colorful grasses | Staged in 0.4b; enable/test color/grass layering |
| The dense flowers mod | Staged in 0.4b: Foxified Dense Flowers port |
| Bushy pink petals | Staged in 0.4b; enable/test resource pack |
| connected bricks | Defer until compatible connected-texture renderer |
| connected paths | Defer until compatible connected-texture renderer |
| seasons: Euphoria Patches vs Serene Seasons vs other snow mods | Conditional: Euphoria visual seasons vs Serene Seasons; do not synchronize blindly |
| connected rocks | Defer until compatible connected-texture renderer |
| lambda better grass | Park: Fabric/Quilt only |
| a mod for fire animation? | Identity unresolved; existing Torches Reimagined is already staged |
| definitely cosy critters | Staged in 0.4b; user explicitly prioritized |
| similar mod mentioned before | Candidate: native real-mob ecology trial, distinct from Cosy |
| athmosphera | Staged Atmosfera Neo in 0.4b; do not stack AmbientSounds |
| ambient particle | Identity unresolved; existing particle mods overlap |
| torches reimagined | Staged in 0.4b; verify resourcepack install/enable |
| extended illumine | Staged in 0.4b; verify resourcepack install/enable |
| tighfire | Park: Fabric-only |
| swinging lanterns | Staged in 0.4b; verify moving light/rendering |
| resourcify | Staged in 0.4b; optional client utility |

## User QoL / rendering nominations (both batches; 29 rows)
| Candidate as supplied | Current decision / next gate |
|---|---|
| Ambient Sounds / AmbientSounds | Deferred alternate to Atmosfera; don't stack audio engines |
| BetterF3 | Candidate, good low-risk UI batch |
| Fadeless | Candidate, test inventory/menu integration |
| Dynamic Lights | Conditional: shader/renderer ownership; no competing engines |
| Lanterns Belong on Walls | Candidate, compare Amendments/Supplementaries |
| APPA resource texture pack? | Identity unresolved: cannot pin |
| Simple Fog Control | Conditional: visual/fog/shader ownership |
| Smooth Swapping | Candidate, check inventory GUI conflicts |
| Controlling | Already staged and user-tested working; full keybind remap AFTER content expansion |
| Better Statistics / Better Statistics Screen | Candidate, low-risk UI batch |
| RightClick Harvest | Conditional: check Farmer's Delight duplicate activation |
| Zoomify only if needed | Conditional: check installed zoom function first |
| Status Effect Bar | Candidate, review existing HUD overlap |
| Cut Through | Conditional: affects combat interaction |
| Light Overlay | Candidate, low-risk UI batch |
| Crops Love Rain | Conditional: changes farming mechanics/ticks |
| Screenshot Viewer | Candidate, low-risk client utility |
| Paginated Advancements & Custom Frames | Choice: compare Better Advancements; only one |
| Reach Around | Conditional: easier placement and server validation |
| Visual Snowy Leaves | Conditional: seasonal/foliage visual overlap |
| Map Distance Fix | Candidate, low-risk QoL |
| Better Block Entities (BBE) | Renderer-risk hold: requires Sodium vs current Embeddium |
| Armor GUI | Exact intended mod identity unresolved |
| Cave Dust | Candidate: Cave Dust Rethinking; particle density audit |
| Subtle Effect | Candidate: Subtle Effects; avoid duplicate particle/sound layers |
| Continuity? (glass) | Conditional: CTM port and Embeddium/NeOculus verification |
| Pickup notifiyer | Candidate: Pick Up Notifier; Puzzles Lib present |
| Better Advancements? | Choice: compare Paginated Advancements; only one |
| Allmobheads | Candidate: All The Heads; drops/loot and mob support audit |

## Further nominated cross-category work NOT reducible to the two lists
| Area | Candidates / existing systems | Decision |
|---|---|---|
| Discoveries | Traveler's Titles, First Steps, WITS, Explorer's Journals | Evaluate discovery titles and player-visible journaling now as content/UI if desired; implementation of **FTB quests/Questlog chapters** remains final phase. Avoid doubling two title overlays or exploration trackers. |
| Rendering and distant terrain | Distant Horizons vs Voxy, shader compatibility | Hold replacement/LOD engine decisions to performance phase; not a fix for slow FreeTerraForged cold worldgen. |
| Extra wildlife | Critters & Companions, Naturalist/Hybrid Aquatic/Ben's/Alex's duplicates | Critters & Companions is distinct from Cosy, remains a candidate; keep thoughtful species and low server AI burden. |
| Ocean | Existing Aquamirae, NeoReefRedux, Deeper Oceans, Hybrid Aquatic, ships/ruins; Beyond the Ocean later | Build with existing content first; avoid adding redundant aquatic creatures; quest line only at end. |
| New worldgen/structures | All original installed/future/structure and Create spreadsheets | Follow settled selections; no immediate extra YUNG bridges, no rejected Create rail/aeronautics or FDstructure. |
| Mechanics/decorative extras | Inventory Sorter, Serene Seasons, Dusty Decorations, Night Lights, All The Heads | Candidate/conditional by exact role and ecosystem. No forced gameplay winter clock, no duplicate chest/recipe systems. |
| Other QoL | Optional vanilla Bonus Chest loot, Status/UI, armor displays, exploration overlays | Keep queued as content/UX features; Bonus Chest loot and value tuning after balance if adopted. |

## Mutant Monsters rarity — accepted source implementation
- Official Minecraft 1.21.1 source (`Fuzss/mutant-monsters`, maintained `1.21.1` branch) exposes four **common** natural spawn-weight keys, defaults 0.05. AO sets all to **0.01** in `release_030/overrides/config/mutantmonsters-common.toml` (one-fifth numerical spawn-weight factor).
- **Rarity semantics caveat:** native `BiomeModificationsHandler` uses `Math.max(1, (int)(baseMobWeight × multiplier))`. Where default already rounded down to the minimum weight **1** (notably Enderman, depending on biome), 0.01 does **not** reduce its rarity further. This is rare-by-weights, not a globally guaranteed fivefold reduction for every variant. Do not invent an extra config to bypass the minimum.
- Vanilla-like monster spawn conditions still apply; modded-biome eligibility depends on whether the vanilla counterpart can spawn there. Chemical X conversions remain available; spawning only is adjusted. Future stricter rarity needs a source-backed targeted biome restriction or spawn filtering mod, not fake `spawnChance` keys.
- Source: https://github.com/Fuzss/mutant-monsters/blob/1.21.1/Common/src/main/java/fuzs/mutantmonsters/config/CommonConfig.java and native biome-modification handler.

## How to resume content expansion (new workflow; supersedes old pre-quest trial sequencing)
1. **Work from the existing reviewed lists, not newly invented handfuls of mods**: shortlist high-value candidate groups from these tables, confirm the current manifest overlap, verify exact 1.21.1 NeoForge files and dependencies, and avoid redistributing unlicensed resource packs.
2. Prefer large **compatible** content batches (building/decor and client QoL; exploration/discovery UI; combat/encounters; visuals/assets) while keeping truly competing renderers, audio engines, advancement GUIs and seasons mutually exclusive.
3. Record small problems now and fix them in the separate post-expansion compatibility phase. Fatal launch/data corruption/destructive incompatibility remains an immediate blocker.
4. **After content:** keybind overhaul, content bug fixes → worldgen/performance optimization → balance → FTB Quests, archaeology missions and Questlog **last** → optional MCA Reborn/more bridges.

**Scope note:** Table statuses derive from the original saved audits and currently pinned source. They are not proofs of runtime support. Do not mark items accepted simply because a link existed in an older research document.
