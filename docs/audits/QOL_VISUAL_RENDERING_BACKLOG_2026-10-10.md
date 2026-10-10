# Ambient Odyssey — post-worldgen QoL / visuals / rendering audit backlog
**Added:** 10 October 2026 · **Target:** Minecraft 1.21.1 NeoForge · **Status:** candidate research only; **no modifications to active Test8.2 modpack or release lock**.

## Scope and integration order
User requested all items below be added to the **later** QoL audit while Test8.2 startup/worldgen testing continues. No approval to install all, and no exact CurseForge file pins committed. First get Test8.2 to the main menu, finish the worldgen freeze, then stage QoL in separate A/B waves so client/rendering crashes are attributable. Always honor the default `main` rollback and active `structure/test6` branch.

Legend: **P1** = attractive low-risk audit; **P2** = test alongside overlapping installed mods; **P3** = gameplay/performance/renderer potentially impactful; **Unknown** = identify exact project first. Verify actual Minecraft 1.21.1 NeoForge **file**, required dependencies, sidedness, licenses, and CurseForge app import path before pinning.

## Explicit candidate inventory (user's order, every item preserved)

| Candidate | Priority | Why / exact later audit |
|---|---|---|
| **Ambient Sounds / AmbientSounds** | P2 | Richer contextual audio and biomes. Assess CreativeMD AmbientSounds native 1.21.1 NeoForge build + CreativeCore dependency and content sounds; check performance with FTF's high biome turnover, sound spam and game volume |
| **BetterF3** | P1 | Customizable F3, coordinates, chunk/TPS data; useful for Minecraft/tester debugging. **Official NeoForge 1.21.1 v11.0.3 exists**: https://www.curseforge.com/minecraft/mc-mods/betterf3/files/all?page=1&pageSize=20&version=1.21.1 . Test F3 screen alongside existing Embeddium, NeOculus, Xaero, Spark and debug metrics |
| **Fadeless** | P1 | Reduce annoying GUI/loading fade delay, not necessarily load time. Native NeoForge appears supported: https://modrinth.com/mod/fadeless . Test FTB Quests and Better Inventory overlays; respect accessibility and shader menu blur workaround |
| **Dynamic Lights** | P2 | Add held/dropped light sources, measure FPS/CPU and emissive shader conflict. Existing Ars Nouveau bundles **`lambdynlights_api` only**, which does **not prove a complete Dynamic Lights client mod is installed**. Identify one proper client renderer implementation for NeOculus/Embeddium; don't stack multiple dynamic-light engines |
| **Lanterns Belong on Walls** | P1/P2 | Wall mounting/lantern attachment parity. Test against installed **Supplementaries / Amendments**, which already change many placement/decorative interactions, and other wall/chain/lantern mods. Confirm duplicate mechanics and 1.21.1 NeoForge |
| **APPA resource texture pack?** | **Unknown** | Preserve user's label verbatim, **exact project identity/link unresolved** after initial search; no source or author safely identified. Ask for a CurseForge/Modrinth link or screenshot during future audit. Check license, custom models, BBE and shader interactions before offering as default texture pack |
| **Simple Fog Control** | P2 | Adjustable fog for render-distance visibility and performance; test with NeOculus shaders, Vanilla fog, FreeTerraForged distance, Distant Horizons/Voxy LOD fog and dimension-specific moods. Don't blindly disable atmospheric fog in unique dimensions |
| **Smooth Swapping** | P2 | Item movement/swapping animation; test with Better Inventory and Backpacks **1.3.2**, Mouse Tweaks, Sophisticated Backpacks and server-authoritative inventory; make animation optional if it obscures JEI/creative controls |
| **Controlling** | P1 | Search/filter keybind list and conflict handling. **Searchables** currently installed (library), plus Keybind Overrides; neither automatically proves Controlling's full UI is present. Check matching Controlling/Forge port and keybind collision/tooltip behavior |
| **Better Statistics / Better Statistics Screen** | P1 | Searchable, grouped progress statistics; official multi-loader project lists NeoForge/1.21.x https://modrinth.com/mod/better-stats . Confirm mod counts and one-player vs FTB Teams stats remain personal |
| **RightClick Harvest** | P2 | Harvest and replant; compare Farmer's Delight/crop addon/right-click behavior and claimed land interactions. Do not double-trigger crops, fertilization or create infinite resource interactions |
| **Zoomify** *only if needed* | P2 | Assess current zoom from Xaero's Minimap, NeOculus/Embeddium keybinds, spyglass/other installed mods and controls; install **only if no satisfactory zoom exists**. Check zoom conflicts and shader/UI camera stutter |
| **Status Effect Bar** | P1/P2 | More legible timed status effects; may overlap Better Inventory, existing UI overlay mods, Shadow Drop and FTB HUD. Preserve effect duration and accessibility |
| **Cut Through** | P2 | Prevent grass/leaves from interfering with hits/interaction; test Better Combat, Simply Swords, Ice and Fire/other hitboxes; may change intended reach/combats. Verify native NeoForge file |
| **Light Overlay** | P1 | Spawnable-area illumination overlay; useful for beginners and builders. Verify 1.21.1 NeoForge F7/keybind, dynamic lighting vs actual vanilla spawnlight rules, server claims and performance while on |
| **Crops Love Rain** | P2/P3 | Crops accelerate under rain; alters world mechanics/balance (not base terrain). Test Farmer's Delight/farming additions and Server TPS, avoid enormous automated farms. Needs multiplayer server-side config, unlike pure client QoL |
| **Screenshot Viewer** | P1/P2 | Browse screenshots in-game; inspect hotkeys, storage/memory use, GUI overlays and accidental exposure of local screenshots on multiplayer. Client-only preferred |
| **Paginated Advancements & Custom Frames** | P1 | Larger scrolling/tabbed advancement screen; **NeoForge 1.21.1 supported**: https://modrinth.com/mod/paginatedadvancements . Also test huge mod advancement trees against FTB Quests UI (different screen) |
| **Reach Around** | P2 | Easier placement across block edges/in the air; validate 1.21.1 NeoForge and anti-cheat/claims/server checks. Can meaningfully reduce traversal/building difficulty |
| **Visual Snowy Leaves** | P2 | Snow-covered vegetation and winter aesthetics; avoid duplicate snow overlays from ambient/weather mods, Biome snow features and visual particles. Profile leaf rendering/resource pack/shader compatibility and snowy-biome visual consistency |
| **Map Distance Fix** | P1/P2 | Player heading remains on vanilla maps when outside bounds. Official NeoForge **1.21.1** build exists: https://www.curseforge.com/minecraft/mc-mods/map-distance-fix . Examine overlap with Xaero World Map/Minimap (separate maps), treasure maps and server/client deployment |
| **Better Block Entities (BBE)** | **P3 performance/A-B** | **Not the Fabric-only mod Enhanced Block Entities.** Native **BBE NeoForge 1.21.1 release v1.3.4 file 8888765** exists: https://www.curseforge.com/minecraft/mc-mods/better-block-entities/files/8888765 . **BBE's own docs require Sodium**; current AO is **Embeddium 1.0.15 + NeOculus 1.8.7**, so do not assume it will work unchanged. Test only with compatible renderer or coordinated Sodium/Iris trial; profile modded chest/sign/bed/lectern/entity models and resource packs; no synthetic FPS promises |

## Voxy vs Distant Horizons — separate client-rendering architecture audit

### Current AO constraints
- Pack **currently installs Embeddium 1.0.15, NeOculus 1.8.7**, heavy FreeTerraForged + Streams Reflowing worldgen, shaders **Solas** and **Complementary Reimagined** and 5–7-player server goals. Do not silently replace shaders/renderer inside the worldgen test.
- User previously found new-chunk loading slow/poor FPS and very slow first dimension transfers. **Neither Distant Horizons nor Voxy fixes FreeTerraForged's actual chunk-generation TPS**. LOD rendering can additionally consume GPU/CPU/RAM while building its cache; compare warm vs cold cache.

### Distant Horizons (DH)
- **Official** multi-loader NeoForge 1.21.1 builds, mature distribution and server/client LOD synchronization, supports saved/unexplored terrain via server sharing with settings; https://modrinth.com/mod/distanthorizons?loader=neoforge&version=1.21.1
- Shader support requires an Iris/compatible port and **a shaderpack expressly supporting DH rendering**. The existing Solas/Complementary shader IDs have **not been individually confirmed in this AO NeOculus/DH combination**; A/B per exact shader build.
- Prefer DH for **first stable baseline** because it has upstream NeoForge support and fits current architecture more conservatively; **not a guarantee** it works flawlessly with NeOculus, shaders, Incendium, FreeTerraForged.
- Client-only can draw LODs from locally seen terrain, and optional server-side DH can distribute recorded LODs; pregen on the server may reduce client cold discovery but actual LOD pipeline needs verification.

### Voxy
- Voxy uses advanced **GPU/OpenGL LOD** rendering; *community* NeoForge 1.21.1 forks/backports exist, not interchangeable with official Fabric releases. Versions and requirements **differ by fork**.
- Examples: https://github.com/NHblock-Johnsnow/neo-voxy-multiversion/blob/multiversion/README_EN.md describes NeoForge 1.21.1 with **Sodium 0.8.x / Iris 1.8.12+**. https://github.com/steimerbyte/voxy-neoforge-backport-1.21.1 documents render extensions like `GL_ARB_gpu_shader_int64` and admits that its shader/LOD path was not fully tested. Another port https://github.com/adolffurry525/voxy-neoforge advertises Iris shader support but also asks for Sodium and (for its version) Connector/FFAPI. **Pin the exact fork before discussing compatibility.**
- **Voxy compatible with shaders?** **Potentially yes**, when an exact fork implements **Iris shader pipeline compatibility**, and the shaderpack supports its distant terrain integration. **Not universal**; compatibility with the installed **NeOculus + Embeddium** and with **Solas/Complementary Reimagined** is **not yet established**. Do not claim standard NeOculus 1.8.7 works with Sodium/Iris-centric Voxy builds out of the box.
- GPU capability/driver and 64-bit shader integer extension may matter, and Voxy/NVIDIA hardware looks promising, but actual frame-times on the user's GPU are essential.
- **Voxy + DH concurrently:** **NO by default.** Competing LOD/render hooks and separate caches make a combined pack an inappropriate first test. Different duplicated client profiles only.
- Do not turn on any automatic Voxy World Gen or uncontrolled client generation on the final server; test whether it can even represent FTF/Streams (specific client/server synchronized generated chunks may be needed).

### Fair test protocol after worldgen freeze
1. **A:** Baseline no LOD (AO renderer stack), shaders OFF; measure standing-still FPS, frametimes, loading/pregeneration, server TPS.
2. **B:** Official DH NeoForge 1.21.1 on a copied profile using compatible installed graphics stack, shaders OFF, same seed/settings and warmed cache.
3. **C:** DH + Solas, then DH + Complementary, only if exact shader build exposes DH compatibility, run visuals at distance/ocean/fog/dimension.
4. **D:** Voxy exact selected fork using **whatever Sodium/Iris renderer its upstream actually requires**, copied profile, do not remove Embeddium from the only known-good instance; cold/warm cache comparisons.
5. **E:** Voxy + shaders, per shader and renderer, never infer from generic `Iris-compatible`. Check lost leaves/transparent water, biome tint changes, distance fog and LOD geometry.
6. Server impact: 5–7 clients, fresh vs pregenerated terrain, all dimensions, FTF large cliff/river views, Waves, visuals and memory; preserve screenshots/F3/spark logs.
7. Choose DH, Voxy or neither. **Performance is one acceptance criterion, not aesthetics alone**. Only add after resolving first-launch crashes and most worldgen blockers.

## Existing-pack overlap inventory from supplied 10 Oct latest.log
Already installed **Embeddium, NeOculus, Shadow Drop, Particular, Better Inventory and Backpacks, Mouse Tweaks, Sophisticated Backpacks, Searchables, Keybind Overrides, Xaero's Minimap/World Map, Farmer's Delight and Amendments/Supplementaries**. Also present: the *LambDynamicLights API* embedded by Ars Nouveau, **not necessarily the user-facing dynamic lighting implementation**. This is not proof of any candidate being already installed; require an actual current mod list before adding.

## Exit gates / final decision record
- Each candidate: **Accept / Already covered / Skip / Defer**; exact mod name, 1.21.1 NeoForge file ID, dependencies, licensing, client/server and GPU footprint.
- Install in logical 3 groups: **low-impact accessibility & UI**, then **gameplay mechanics/ambience**, then **renderer/LOD/Better Block Entities** alone. Keep shader/texture pack testing in its own controlled wave.
- Prefer optional client-side mods for group convenience; server-required mods need dedicated-server test.
- Do **not** merge this audit into active Test8.2 release lock or overwrites until explicitly approved and tested.
