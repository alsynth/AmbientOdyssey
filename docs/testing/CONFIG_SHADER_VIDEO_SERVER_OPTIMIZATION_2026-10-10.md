# Ambient Odyssey — mod-config, shader, video and server optimization roadmap

**2026-10-10.** Optimize via configs/settings as well as module choice; never advertise unmeasured FPS/TPS. Benchmark cold and warm chunks separately. Profile 5–7 player server with Spark before changing FTF/Streams worker/fallback behavior.

## Config-level work

- FTF + Streams Reflowing + RoadWeaver: profile height fallback and chunk generation separately from rendering; verify actual keys from installed configs before editing, and postpone global pregeneration until roster/worldgen freezes.
- Wildlife, villages, Create, XP: measure entity/pathfinding/block-entity ticks, tune real spawn and machine options; Clumps now staged for XP orbs. Preserve deliberately disabled gorillas/flies/cockroaches.
- Waves + Atmosfera + Sound Physics: compare over canopy/under leaves, rain, shores and caves; Waves volume already source-pinned 0.25, new-player weather 0.2 and blocks 0.4. Don't add AmbientSounds atop Atmosfera. Control reverb/reflections rather than turning everything up.
- Particular/AAA/Subtle Effects/Cave Dust/Cosy: cap density, draw distance and particle lifetimes per effect **after source settings are confirmed**, especially shader shadows High. Avoid redundant particles.
- Structure/biome config: Farmers Structures modded biome eligibility, WDA major-vs-minor density, structure clashes. Do not modify without same-seed evidence.

## Optional client profiles (NOT globally enforced)

| Video/shader option | Performance starting point | High-quality starting point |
|---|---|---|
| Render distance | 10–12 chunks | 16–20 if measured stable |
| Simulation distance | 6–8 chunks | 8–10 if server TPS allows |
| Entity distance | 75% | 100% |
| Particles | Decreased | All if frametimes allow |
| Shadow quality (Solas/Complementary) | Low or Medium | High, matching intended foliage visuals |
| Volumetrics, clouds, godrays | Off/Low | Medium/High after GPU comparison |
| Reflective water and SSR | Low/Off | Medium/High in ocean scenes |
| VSync and cap | User preference, cap to a sustainable rate | Refresh-rate cap where appropriate |

Existing Default Options **new-profile** configuration is GUI scale 3, VSync false, max FPS 160; shader packs currently official Solas/Complementary references, **disabled by default**. Do not copy edited shader binaries or invent settings keys; first inspect exact installed shader option menus. Benchmark shader OFF / Performance / High-foliage in the same world, daytime/dusk/rain, forest interior, cave, ocean and village. Distant Horizons vs Voxy only as separate renderer tests; never stack or silently replace Embeddium+NeOculus.

## Dedicated server acceptance

- Tune server view/simulation distances from measured MSPT/TPS rather than client render distance; confirm network/chunk/login spikes and memory/GC, keep room for OS cache.
- Add backups and test restore, then safe pregeneration only after locked final mod/worldgen roster. Retain 30% sleep and no-fire-spread gamerules. Note `mobGriefing=false` affects villagers' farming.
- Every config edit requires confirmed option, before/after file, comparable benchmark, source version/ownership and rollback. Content first → post-content bugs/keybinds → config/worldgen/performance → boss/loot balance → quests.
