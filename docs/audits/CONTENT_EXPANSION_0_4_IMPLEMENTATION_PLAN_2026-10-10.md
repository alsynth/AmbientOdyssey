# Ambient Odyssey — 0.4.x Content Expansion master implementation plan
**Planning date:** 10 October 2026 · **Authoritative theme source:** [Nine-Theme Content Expansion Gap & Mod Audit](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/audits/CONTENT_EXPANSION_NINE_THEME_PRIORITIES_2026-10-10.md) by the parallel review; **additional baseline check:** [installed-mod compatibility preflight](CONTENT_EXPANSION_ROUND2_INSTALLED_MOD_COMPAT_PREFLIGHT_2026-10-10.md).

**Current work:** Design, conflict analysis, dependency screening and release planning only. **No mod install, mod removal, config/worldgen edits, release-lock change, or claim of tested candidate compatibility.** Branch: `content/expansion-round2-compat-preflight`, based on **Test8.10** proven playable client run. Target **Minecraft 1.21.1, NeoForge 21.1.252, 5–7 players**.

## 0. The governing decision

The *nine-theme audit* diagnoses **interaction and inhabitedness**, not a lack of absolute number of boss/gear/structure mods. We should build a 15–30-minute **optional exploration narrative** out of **existing structures + a small NPC cast + meaningful archaeology + appropriately populated habitats + a personal journal reward**. **No mandatory guild, large new settlement hierarchy, public timed events, compulsory profession progression, or blanket boost to structure density.**

Original theme priority is retained verbatim:

| Gap rank | Official audit theme | Score /5 | Primary expansion lever | Initial decision |
|---:|---|---:|---|---|
| 1 | **Life & Settlements** | 5 | Guard Villagers + curated Easy NPC actors/dialogues, optional naming and Bountiful | **First content tranche** |
| 2 | **Structures & Discoveries** | 5 | Galosphere *vs* Better Archeology prototype, clue/loot/journal on existing ruins | **Second tranche** |
| 3 | **Underground Exploration** | 4 | Galosphere-style cave ecosystem; habitat/reachability; no extra generic labyrinth | **Paired with archaeology trial, separate toggles** |
| 4 | **Wildlife & Living World** | 4 | Existing wildlife distribution audit, selective Naturalist 2.0.x only if gap persists | **Third tranche** |
| 5 | **Ocean Exploration** | 3 | Existing diving→wreck→ruin→encounter/return loop; FTB Ocean Mobs loot | **Quest/content design first, no new ocean mod** |
| 6 | **Quality of Life** | 3 | Controlling immediately; optional inventory sorting after A/B | **Short pre-wave before content** |
| 7 | **Decoration & Ambience** | 2 | Atmosphere A/B (AmbientSounds) then conditional seasons/decor | **Late, independently switchable** |
| 8 | **Dimensions** | 2 | Completion/portal/journal/rewards in existing realms | **No new realm in first 0.4 release** |
| 9 | **Food, Farming & Professions** | 1 | Optional thematic cook/angler/alchemist/field camp content via installed systems | **Integration/quests, no big new food roster** |

**Order nuance:** a tiny QoL pre-wave happens first because improving controls benefits every subsequent content test. This is implementation ROI, not a re-ranking of the original content audit.

## 1. Exact active baseline and critical source discrepancies

- **Test8.10 runtime**: 340 detected JAR filenames (includes libraries; **not** 340 CurseForge mods). **267** CurseForge manifest refs, exact 1.21.1 NeoForge. Installed **Searchables 1.0.2**, **JEI**, **FTB Quests 2101.1.36**, **FTB Solo Quests 1.1.2**, **Bountiful**, **Curios + Accessories**, **Mouse Tweaks**, **Better Inventory and Backpacks**, **Lootr**, **Create 6.0.10**, **Alex's Caves + Alex's Mobs**, **Hybrid Aquatic**, **Friends & Foes**, **Hominid**, **Mowzie**, **CTOV**, **Towns and Towers**, **Integrated Villages**, **Repurposed Structures**, **Archaeology Ruins**, **JEArchaeology** and many other existing mods.
- **Absent from exact JAR filename list**: Controlling, Inventory Sorter, Villager Names, **Collective**, Guard Villagers, Easy NPC Core/Config UI, Galosphere, Better Archeology, Naturalist, Serene Seasons, AmbientSounds 6 and **FTB XMod Compat**. Filename inspection isn't a full registry/API audit; verify all IDs when building.
- **Renderer:** Embeddium + NeOculus + ImmediatelyFast; do not install Sodium-only render extensions as routine content dependencies.
- **FTF/Biolith + curated BOP/BWG/RU/Nature's Spirit donors + Streams Reflowing** remain provisionally accepted. Test8.10 FTF generated 4,418 chunks at ~6.76 new chunks/s with nine lag warnings; Streams explicitly logged a **slow height sampling fallback**. A new cave/AI/season provider must not silently incur a major uncontrolled server regression.
- **Contradiction to resolve without automatic edits:** Nine-theme audit says YUNG's Better Mineshafts was previously expressly excluded, whereas **Test8.10 release lock and actual mod list include `YungsBetterMineshafts-1.21.1-NeoForge-5.1.1.jar`**. Preserve the runtime baseline for this content work and get a conscious selection decision later; do not remove a running mod as a side effect of adopting the audit.
- Nine-theme audit researched earlier **`release-lock.json` Test1.3**; Test8.10 now has Test1.10, additional repairs and 267 manifest refs. All historical candidate version claims are research starting points, **not approval**.

## 2. Candidate decision register — 0.4.x initial curation, NOT install consent

Definitions: **PROTOTYPE** = green light to investigate/test in disposable clone, not green light to ship; **CONDITIONAL** = must satisfy a specific acceptance gate; **HOLD** = leave out of first 0.4 content beta; **REJECT FOR FIRST WAVE** = not an automatic addition. Exact project/file references listed when verified with live official pages on planning date.

| Candidate and theme | Current decision | Installed overlap / real extra-round compatibility issue | Version/dependency gate and specific next action |
|---|---|---|---|
| **Controlling** — QoL | **PROTOTYPE pre-wave** | Searchables already installed; compare with Keybind Overrides and current key search/Controls GUI; don't overwrite user keybinds | [Official NeoForge 1.21.1 **19.0.5**](https://www.curseforge.com/minecraft/mc-mods/controlling/files/all?page=1&pageSize=20&version=1.21.1), requires Searchables (**present**). Verify search/duplicate key highlighting with AO keybind set |
| **FTB XMod Compat** — quest-integration support | **PROTOTYPE pre-wave / important integration check** | FTB Quests + JEI present, compat absent by filename. Its documented role is JEI recipe display, KubeJS/events and optional integration; **does not automatically implement custom Questlog↔Easy NPC progression, or fix every item-filter issue** | Official [NeoForge 1.21.1 **21.1.12**, CF 889915:8909889](https://www.curseforge.com/minecraft/mc-mods/ftb-xmod-compat/files/8909889). 21.1.12 notes specific JEI API fixes. Verify 1 example JEI quest recipe, broad item filter/Apotheosis gem task, reward receipt and FTB Solo vs team state |
| **Villager Names** — settlements | **CONDITIONAL easy win** | Modded professions, Wandering Traders, Bountiful and named hand-authored Easy NPC actors; duplicate names/notorious repeated names or NPC renamed by other mods | Official [1.21.1 8.4, CF 345854:8021602](https://www.curseforge.com/minecraft/mc-mods/villager-names/files/8021602), **requires Collective** ([author's dependency listing](https://www.curseforge.com/minecraft/mc-mods/villager-names/relations/dependencies)), which **is not installed**. Add/verify an exact compatible 1.21.1 Collective only if selected; ensure authored Easy NPC identities not overwritten |
| **Guard Villagers** — settlements | **PROTOTYPE content #1** | CTOV, T&T, Integrated Villages, Grand Capitals, other POI/trade mods; aggressive Mowzie/Ice & Fire/magic/Alex's enemies; pathfinder count and guard invulnerability/raids | Official [2.4.12, NeoForge 1.21.1, CF 360203:8767509](https://www.curseforge.com/minecraft/mc-mods/guard-villagers/files/8767509); 2.4.12 fixes a Carry On performance issue. Test spawn in **four distinct settlement families**, guard count per village, guard-on-guard aggro, protection balance and TPS/AI |
| **Easy NPC** — settlements/story | **PROTOTYPE content #1, authored not ambient spam** | Trade menus, Bountiful job boards, FTB Quests progression and optional future Questlog GUI; hand-placed NPC persistence and claimed chunks | **Important modular install:** [Bundle](https://www.curseforge.com/minecraft/mc-mods/easy-npc/files/all?page=1&pageSize=20&version=1.21.1) 7.14.0 is a **~25 KB dependency/launcher convenience**, not full NPC code. Verify **Core 7.14.0** + **Config UI 7.14.0** or use bundle only if CurseForge resolves both; test server Core + admin-only UI setup and distribution policy. Make exactly **three authored NPC/dialogue demos**, prove FTB quest triggers and player-specific completion on server before claiming integration. No mandatory guilds |
| **MCA Reborn** — villagers | **HOLD / alternative vision** | Fully changes villagers/relationships/AI, competes with Guard Villagers/name identity and Easy NPC | Do not combine automatically. Isolate only if group votes for strong family/colony sim |
| **MineColonies** — villages | **REJECT FOR FIRST WAVE** | Many persistent citizens/pathfinders/raids, Create logistics and dedicated-server TPS | Only revisit on explicit town-simulator mandate. Not needed for optional archaeological exploration |
| **Galosphere** — archaeology + caves | **PROTOTYPE content #2A, first A/B option** | **Alex's Caves** underground biome routing, FTF/Biolith cave sculpting, Archaeology Ruins/JEArchaeology, Dungeon Crawl, deep mineral economy and biome tags. Potential landscape/worldgen shifts require approval before server pregeneration | Official [NeoForge 1.21.1 v1.5.5, CF 631098:8242886](https://www.curseforge.com/minecraft/mc-mods/galosphere/files/8242886), project [dependency listing shows 0](https://www.curseforge.com/minecraft/mc-mods/galosphere/relations/dependencies). **Test exact native biome/carver/placed-feature/structure registry**, caves visited naturally at several depth bands and controlled worldgen rate |
| **Better Archeology** — archaeology | **PROTOTYPE content #2B; compare, not bundle initially** | Existing Archaeology Ruins and Galosphere's own archaeological sites; spammed minor dig sites, brushable block IDs, WDA/ancient city treasure overlap | Official [NeoForge 1.21.1 v1.3.9](https://www.curseforge.com/minecraft/mc-mods/better-archeology/files/all?page=1&pageSize=20&version=1.21.1). Test **separate clone** vs Galosphere clone: distinct dig mechanics, structure-site density, source loot, archaeology discovery integration; decide one-first, both only with controlled collision/density |
| **Existing-structure clue/treasure datapacks** — discoveries | **PROTOTYPE content #2, no new generic structure mods** | WDA/IDAS/Archaion/Moog/RS maps and source structure loot; unknown permissions and NBT integration, Lootr individual inventories and co-op credit | Start with 1–2 **existing structures only**. A rumor points to an actual located structure; a **non-mandatory** map/field journal records discovery; no fake unexplored coordinates or impossible scripted rarity. Verify player-specific completion and source/asset permissions |
| **Naturalist** — wildlife | **CONDITIONAL content #3** | Alex's Mobs, Hybrid Aquatic, Ben's Sharks, FTB Ocean Mobs, Friends & Foes, Hominid and Ice & Fire already cover many fauna roles; more pathfinding/spawncap contention and fish duplication | Nine-theme source cites **v2.0.3**; **newer compatible** official [NeoForge 1.21.1 v2.0.5 CF 627986:9004373](https://www.curseforge.com/minecraft/mc-mods/naturalist/files/9004373) as of Sep 28, 2026. Changelog specifically improves **wolf mixin compatibility**; still requires in-pack behavioral tests. Audit unique species IDs/config and biome tags first; prefer **low spawn weights and selected species**; disable undesirable flies in existing Alex's Mobs where safely configurable |
| **Existing wildlife spawn/Questlog field guide** | **FIRST before Naturalist install** | All current mob systems, curated biomes and 5–7 players | Spawn/habitat heatmap (surface day/night, cave, coastal ocean, 6+ modded donor biomes); verify missing fauna due biome tags before adding new AI package. Non-lethal observation/sighting tasks, avoid kill-50-passive chores |
| **Ocean expedition progression via existing mods** | **PROTOTYPE content #4, no new ocean mod** | Aquamirae, NeoReefRedux, Deeper Oceans, Hybrid Aquatic, FTB Ocean Mobs, shipwrecks, Aquaculture, Lootr, water breathing and gear | Create simple optional **port→diving tools→wreck chart→reef/deep trench→reward→return** progression. Native FTB Ocean Mobs **has no default loot per source audit**, so test a small loot/integration datapack to reward marine exploration, without brute-force grinding |
| **Beyond the Ocean** — dimension/ocean | **HOLD later content audit** | Existing ocean and dimension routing, portals, server pregeneration and map overlays | Explicitly previously approved for *later evaluation* in original audit, **not automatically installed** now. Gate by completed existing ocean arc and version/dependency check |
| **Inventory Sorter** — QoL | **CONDITIONAL late small QoL A/B** | Mouse Tweaks, Sophisticated Storage/Backpacks, Better Inventory, JEI and container mod GUIs; duplicate sort click bindings can mishandle backpack loot | Official [NeoForge 1.21.1 **24.0.18**, CF 240633:5979614](https://www.curseforge.com/minecraft/mc-mods/inventory-sorter/files/5979614). Must never reorder special/offhand/task slots or bypass server ownership; try one full assortment of storage screens with undo/backups |
| **Serene Seasons** — ambience | **CONDITIONAL late world-state A/B** | FTF + BWG/BOP/RU/Nature's Spirit seasonal biome tags, Tan's Huge Trees/leaf textures, Farmer's Delight crop conditions, Snow Imprints and shader/weather pipeline | Original audit has correct [NeoForge **1.21.1 v10.1.0.3 beta**, CF 291874:6182596](https://www.curseforge.com/minecraft/mc-mods/serene-seasons/files/6182596). Crop/fertility penalties **disabled or significantly softened** unless explicitly desired. Validate all curated donor biomes across season cycle, snow/leaves consistency, world config persistence and dimensions with fixed climate. Decide before server world pregen |
| **AmbientSounds 6** — ambience | **CONDITIONAL client A/B** | Existing Minecraft/biome sound packs, waves, cave ambiences, voice-chat fatigue, audio channels, shader performance | [NeoForge 1.21.1 **6.3.10**](https://www.curseforge.com/minecraft/mc-mods/ambientsounds/files/all?page=1&version=1.21.1), **~81 MB**. Test lowest/highest sound levels in 20-min cave/forest/shore and full server/Discord comms; controls and opt-out. Do not combine with Cave Dust/Subtle Effects new particle burden in same performance measurement |
| **Dusty Decorations 2.2** — decoration | **HOLD unless needed for authored port/village** | Other furniture/lighting models and settlements; author's 1.x→2.x change removes earlier placed blocks | Prefer **before permanent world** only. Test disposable world, player building inspiration and item namespace/migration; not worth forcing if existing décor suffices |
| **Night Lights** — ambience | **HOLD / low ROI** | Existing lighting, Supplementaries/Amendments, dynamic lights and client shader emissives | Only revisit for specific designed settlement build and verified block-state/tick impact |
| **Blue Skies** — dimensions | **HOLD, version unverified** | Existing many dimensions and a potentially missing native 1.21.1 NeoForge release | No automatic Connector port or extra realm |
| **Mine Cells** — dimensions | **HOLD, Connector experiment** | Fabric/Sinytra extra loader/registry burden, dimensions and spawn balancing | Keep isolated, never bundled into main 0.4 wave |
| **Profession-content quests via installed mods** | **PROTOTYPE design only** | Existing many Farmer's Delight/Seafood add-ons, Create, Bountiful, Aquaculture | 3 tiny optional chapters: 1 travel field ration; 1 marine/fishing research; 1 cave botanical delivery; no new ingredient explosion, mandatory cooking grind or artificial guild economy |

## 3. Coherent 0.4.x build roadmap

### `0.4.0-preflight` — copy baseline, *no new worldgen yet*
- Freeze/archive **known-running Test8.10 importer**, its SHA and unmodified mod list. Never update in place or merge worldgen PRs automatically; work on a fresh feature branch.
- Resolve source/lock disagreement **YUNG's Better Mineshafts** by separate user decision, not by stealth removal.
- Derive machine-readable installed registry list from exact Test8.10 log & manifest; record CF file pin, additional dependencies and mod sidedness for each approved trial.
- Benchmark identical **existing** world/seed/route (client FPS/framerate, server main-thread MSPT, P95 tick duration, RAM, active entities, chunks generated) using **Spark**, with cold-generation and pregenerated-area trials kept separate. Test8.10 6.76 chunks/s is historical context, not fixed performance threshold.
- Define **Questlog vs FTB Quests**: source audit uses both terms; **only FTB Quests is installed**. Custom Questlog GUI inventory button is a later concept, not an existing integration/API. Decide whether FTB remains quest backend, whether Questlog is UI shell or independent mod, and how per-player quest triggers actually work. Do not write NPC quest scripts against an assumed API.

### `0.4.0-a` — fast usable control/quest integration pre-wave
**Candidate set:** Controlling → verify existing Searchables and keybind overrides. Test FTB XMod Compat separately with JEI task display and one mixed item task. Villager Names+Collective optional **after** quick NPC naming overlap decision.
**Acceptance:** keybind screen opens, query/filter conflict highlighting works, no click-hijack; FTB quest recipes and reward tasks remain intact; no new renderer/shader conflicts. Separate game-client only vs server-required archive.
**Release guard:** no changes to Overworld generator.

### `0.4.0-b` — living settlements
**First trial:** Guard Villagers **alone**, four settlement types (vanilla plains, CTOV, Towns & Towers, Luki/Integrated) vs no-guard baseline; check guard counts, patrol loops, golem/village POIs, raids, guards fighting player or mod bosses, 5–7 player server TPS.
**Second trial:** Easy NPC 7.14.0 modular runtime. Author **three NPCs** (archaeologist, cartographer/port merchant, cave herbalist), each with at most three dialogue branches plus a trade/task. Test click interaction, chunk reload, NPC ownership and permission to edit, restart persistence, server-to-client synchronization, 2 players receiving **independent progress** and a separately identifiable quest trigger. Avoid spawning hundreds of ambient dialog AI actors into all towns.
**Initial success:** player meets a named individual with a grounded reason to explore; no scripted global guild or forced story. Retain Bountiful as optional jobs.

### `0.4.0-c` — caves, archaeology & actual discoveries
**A/B choice**:
- **A** Galosphere 1.5.5, no Better Archeology. Check *natural* Crystal Canyon/Lichen/Pink Salt biome presence, Forgotten Ruins & mole/altar interactions, nested biome/structure generation, Alex's Caves separation, FTF/Biolith cave carving and weird dimensions.
- **B** Better Archeology 1.3.9, no Galosphere. Check source-native dig site rarity, competition with Archaeology Ruins/JEArchaeology, suspicious block integrity, reasonable brushable treasures and progression integration.
- **A+B** only if each alone succeeds, together demonstrate **meaningful nonduplicate activities**, biome/structure budget stays acceptable and targeted performance test passes.
- Independent **C**: one existing WDA/Archaion/Moog ruin with clue/sighting/treasure journal datapack. Author no new third-party structure geometry without evidence/license.
**Gate:** preserve current worldgen baseline/config and ensure all new biomes/structures spawn in curated donor landscapes before permanent server pregeneration. Check proper caving depths, non-infinite spawn loops, loader errors/priority, and a co-op discoverer vs shared journal.
**Decision:** pick the *mechanically strongest content experience*, not whichever lists more structures.

### `0.4.0-d` — wildlife and field-guide gameplay
1. **Without Naturalist**, tune/configure existing spawn biome tags and AI categories; check surface visibility in open prairie, cold forests, mountains, wetlands, caves and coral/deep oceans.
2. **Optional Naturalist 2.0.5 trial** limited to unique behaviors/species after mapping exact overlaps. Avoid doubling bears, frogs, birds, wolves, sharks, fish and other existing roles; do not count potentially mismatched marketing species totals as facts. Use controlled spawn weights, rarity and biome compatibility.
3. 15–20 passive/wildlife sighting/field-note task prototypes for co-op without mass slaughter; no valuable boss progression gated by animals. Record passive/hostile counts and TPS under 5–7-player equivalent simulated spread.

### `0.4.0-e` — ocean and optional professions; leverage old mods
- No automatic new ocean mobs, deep-sea dimension or generic ruins.
- Author one **non-mandatory** ocean expedition arc: port clue and supplies → ruined shipwreck chart → reef/wreck/discovery → deep dangerous site → fair personal reward and return.
- Configure small bounded FTB Ocean Mobs drop tables only after source item ID/loot and balancing review; ensure no per-player farming exploit, fit Aquamirae + existing gear; test Lootr per-player rewards.
- Add short field ration, angler and herbalist quests through already-installed Farmer's Delight/Modded foods/Bountiful; no repeatable currency mill.
- Later audit **Beyond the Ocean** separately if oceans still feel underdeveloped.

### `0.4.0-f` — sensory environment and GUI polish, *one visual family at a time*
- Client A/B AmbientSounds 6 alone with Discord voice, repeated environmental loops and volume opt-out.
- Decide on Serene Seasons **separately** with fixed-biome climate maps, controlled crop penalties, shaders/leaves and server weather behavior before permanent world.
- Optional Dusty Decorations + Night Lights only for designed village/port encounters; monitor any migration-risk block ID changes.
- Legacy QoL backlog still includes inventory sort, title/discovery journal, pickups, optional Bonus Chest loot, accessible JEI explanations, and user-specified **resource pack/location customizable Questlog inventory quest button**. A/B UI mods; preserve existing style and hotkeys.
- New particle/render mods from unrelated QoL list must have their own A/B profile; **not** silently added alongside sound/seasons/worldgen.

### `0.4.0-rc` — integration, balance and permanent-world gate
- Final quest chapter order combines **entry/tutorial → inhabitants → clues/ruins → caves/ecology → ocean → boss/dimension challenges → optional professions**. Do not gate free exploration or convert every discovery into an unskippable tutorial.
- Balance 3-phase dungeon tiers and rare equipment, ARPG bosses + Apotheosis gems, guards vs high-level enemies, new archaeology treasures vs existing Lootr.
- Test 5–7 player sessions: new world/generation, **pre-generated** sample, co-op quest progress, returning players, NPC survival/reloads, chunk and instance boundaries, item reward once-per-person, portal/dimension return.
- **Only after all worldgen-content choices and seed are locked**, plan the server-side **chunk pregeneration** radius and selected dimensions; pregen ≠ permanent force-loading; backup before launch, track drive/RAM, ensure pregen does not create old/new content seams. Write this explicitly into planned Questlog **Tips & Tricks** for players.
- Only then do full rendering/server TPS/AI/performance tuning; worldgen still has a **Streams slow height-sampling fallback** that requires a separately scoped investigation.
- Final ZIP: exact version/NeoForge 21.1.252, CurseForge-root `manifest.json`, correct mod/file pins and dependencies, required client/server sidedness, reproducible build and all accepted feature tests. Do not ship this phase as "complete" before passing runtime gates.

## 4. Golden vertical-slice acceptance scenario (from original audit, operationalized)

**Goal**: 15–30 min optional adventure on a normal, naturally generated multiplayer map, without admin spawning the structures just to pass.
1. Explore a small real town in CTOV/T&T/Integrated village. Named villager + guard visible, no POI errors, no mass AI stalls.
2. Meet curated archaeologist Easy NPC, read rumor of a reachable already-generated cave/ruin or coordinate-safe map clue. No fabricated structure discovery; avoid map pointing to unloaded impossible loot.
3. Traverse naturally generated reachable cave biome or use already present dungeon structure; encounter nonaggressive animal/plant and interact with actual archaeology mechanic.
4. Reach one **personal Lootr container**; player A and B each have expected independent or explicitly shared quest progress, loot rewards are nonduplicative and no one loses completion credit due only to who got last hit.
5. Recognize nearby dangerous tower as later-tier objective without needing to fight it now; journal records visit and optional future lead.
6. Return to settlement; NPC dialogue updates/reward granted **exactly once per player**. Confirm persists after logout/rejoin, /reload and dedicated-server restart.
7. Repeat with 5–7 players distributed across biome groups and compare server TPS/MSPT/AI counts to pre-expansion baseline.

**A passing custom-NPC spawn is not the same as a complete playable quest chain**; until a trigger API/data route is proven, the NPC can provide dialogue and a compatible FTB quest can use existing advancement/location detection as a fallback.

## 5. Approval gates and what is *not* yet approved

**Okay to investigate/prototype:** Controlling, FTB XMod Compat, Guard Villagers, modular Easy NPC, Galosphere **or** Better Archeology, existing wildlife respawn tuning, selective Naturalist, optional naming with Collective. These are **our proposals grounded in the audit**. **No actual mod installation has been authorized by this planning request.**

**Defer**: MCA Reborn, MineColonies, Blue Skies, Mine Cells/Connector, more generic dungeon structure packs, multiple new dimension generators, worldgen-overhauling replacements, extra full food mods, Easy Anvils (explicitly rejected), Big Globe, FDstructure, heavy seasons before separate A/B, mass NPC spawning. **Do not** change current YUNG bridges or accepted terrain as an incidental consequence.

Before making build 0.4.0-a, present a **precise selection slate** (candidate IDs, additions including required dependencies and expected total count, category role, cross-mod overrides, test/world compatibility, private packaging) for user approval; prototype in an isolated branch and preserve the Test8.10 snapshot. This doc records choices to *test*, not final content selections.

## 6. Source provenance and checks

- **Nine-theme source** (category rank, motivation, candidate list, explicit rejects, target experience): [CONTENT_EXPANSION_NINE_THEME_PRIORITIES_2026-10-10.md](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/audits/CONTENT_EXPANSION_NINE_THEME_PRIORITIES_2026-10-10.md).
- **Second independent compatibility map** (actual installed systems and conflict surfaces): [CONTENT_EXPANSION_ROUND2_INSTALLED_MOD_COMPAT_PREFLIGHT_2026-10-10.md](CONTENT_EXPANSION_ROUND2_INSTALLED_MOD_COMPAT_PREFLIGHT_2026-10-10.md).
- **Official public verification**: [Guard Villagers 2.4.12](https://www.curseforge.com/minecraft/mc-mods/guard-villagers/files/8767509), [Easy NPC Core and Bundle](https://www.curseforge.com/minecraft/mc-mods/easy-npc), [Villager Names + Collective](https://www.curseforge.com/minecraft/mc-mods/villager-names/relations/dependencies), [Galosphere 1.5.5](https://www.curseforge.com/minecraft/mc-mods/galosphere/files/8242886), [Naturalist 2.0.5](https://www.curseforge.com/minecraft/mc-mods/naturalist/files/9004373), [FTB XMod Compat 21.1.12](https://www.curseforge.com/minecraft/mc-mods/ftb-xmod-compat/files/8909889), [Controlling 19.0.5](https://www.curseforge.com/minecraft/mc-mods/controlling/files/all?page=1&pageSize=20&version=1.21.1), [Inventory Sorter 24.0.18](https://www.curseforge.com/minecraft/mc-mods/inventory-sorter/files/5979614), [NeoForge Serene Seasons 10.1.0.3 beta](https://www.curseforge.com/minecraft/mc-mods/serene-seasons/files/6182596).
- Official pages confirm **file/version availability** and documented features/dependencies, **not compatibility with AO's full 340-JAR runtime**. Future binary/metadata CI must check exact dependencies, registries, core classes/mixins, placement tags and source mod interop **before** someone promises fixes or performance.
- No standalone Questlog mod or FTB XMod Compat visible by filename in actual Test8.10 runtime; do not infer API integration without explicit test.
- Research-only source changes. No new pack artifact or temporary performance claims.
