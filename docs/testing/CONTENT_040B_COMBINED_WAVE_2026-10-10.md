# Ambient Odyssey 0.4.0-b1 — single substantial content-expansion test wave
**Date:** 10 October 2026 · **Status:** private pre-release / static CI candidate, in-game runtime not yet verified. **Source:** [nine-theme audit](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/audits/CONTENT_EXPANSION_NINE_THEME_PRIORITIES_2026-10-10.md), [cross-mod risks](../audits/CONTENT_EXPANSION_ROUND2_INSTALLED_MOD_COMPAT_PREFLIGHT_2026-10-10.md), [user's 19 visual proposals](../audits/CONTENT_EXPANSION_VISUAL_FAUNA_ADDENDUM_2026-10-10.md).

## New operating rule requested by the user — **larger batches, fewer game tests**

Earlier 0.4.0-a offered only Controlling + FTB XMod Compat, which was too slow to warrant its own launch/testing loop. **Don't require the user to separately playtest that release.** It becomes the preserved parent commit of this combined Content 0.4.0-b1 wave, where **20 additional official CurseForge references** are added at once: 15 native NeoForge mods/libraries + 5 CurseForge platform-delivered resource packs. That brings **267 Test8.10 refs → 269 first trial → 289 combined refs**, while keeping the tested FTF/Biolith/Paxi/structure config and exact 273 template NBT fixes unchanged.

A/B isolates are **exception-only**, not normal work. Only separate if there is:
1. A real documented incompatibility, incompatible MC 1.21.1/NeoForge loader or unmet dependency;
2. Two mods competing for the same engine (e.g., Atmosfera vs AmbientSounds, distinct seasons schedules);
3. A change preventing meaningful tests (e.g., CTM texture pack with no working CTM loader, Easy NPC editing UI without runtime Core);
4. A genuine reproducible crash or severe regression **after the combined run** requiring binary search.

Aim for **one substantial 60–90-minute client/multiplayer test** for the complete stable branch instead of repeated minor runs. This does *not* license hiding failures or claiming 20 items individually tested from a static ZIP check.

## Contents: **15 new mod/dependency projects** with real file IDs

| Category | Exact CurseForge project : file | What it adds / integration |
|---|---|---|
| Living villages | Guard Villagers **360203:8767509** | Protective patrollers; check CTOV/T&T/Integrated/Luki villages, pathfinding and raid AI |
| Custom NPC/story | Easy NPC Core **1308987:9039094** + Config UI **1214728:9039106** | Exact matched 7.14.0 NeoForge pair, no separate bundle stub or mass auto-spawning; three small dialog prototypes later |
| Cave ecology | Galosphere **631098:8242886** | Crystal/Lichen/Pink Salt cave mechanics and Forgotten Ruins; natural FTF/Biolith encounter eligibility |
| Archaeology | Better Archeology **835687:9099893** | Brushable finds/ruins; check duplicate sites with Galosphere and installed Archaeology Ruins |
| Required dependency | Resourceful Config **714059:6467772** | Missing **mandatory Better Archeology config** dependency, version 3.0.11 NeoForge (native mods.toml requires ≥3.0.3). Architectury already installed |
| Wildlife | Naturalist **627986:9004373** | More species/ecology; GeckoLib already installed. Avoid unbearable passive spawn density alongside Alex's Mobs/Hybrid Aquatic and custom BOP/BWG/RU biomes |
| Named inhabitants | Villager Names **345854:9032258** + Collective **342584:9060865** | Exact v8.7 + required Collective v8.42, paired for successful class-loading; preserve authored Easy NPC custom names |
| Fauna ambience (user priority) | Cosy Critters & Creepy Crawlies **1182393:8390081** | Original PigCart v0.3.3 **client-side** atmospheric animals/particles, not the older unofficial fork and not Critters & Companions |
| Resource-pack support | Polytone **958094:9103491** | 1.21.1 NeoForge 5.0.3: Rainbow's foliage color/material and Polytone-only sound/foliage effects |
| Dense flora | Foxified Dense Flowers **1413643:7384220** | NeoForge 1.21.1 v1.0.0 port adds local flower render density; no new biome/worldgen |
| Asset browser | Resourcify **870076:9001238** | Client 1.21.1 v1.8.7; can browse official pack choices but should not alter locked modpack files silently |
| Dynamic lantern | Swinging Lanterns **1477733:9116978** | 1.21.1 v2.0.4; check Amendments, NeOculus shadows, resource-pack models |
| Client ambient sound | Atmosfera Neo **1499605:8313373** | NeoForge 1.21.1 1.0.2; **chosen over AmbientSounds 6** to avoid duplicate always-on soundscapes; YACL required but present in Test8.10 roster |

**Inherited and unmodified:** Controlling 19.0.5 (250398:6368976), FTB XMod Compat 21.1.12 (889915:8909889), all existing 267 CF references, manual NeoReefRedux and its SHA1, Better Bastions, Luki Woodland Mansions, all FTF/Biolith terrain and source-derived jigsaw repairs.

## Five officially referenced resource packs (NO source ZIP redistribution)

| Pack | CurseForge project:file | What to inspect |
|---|---|---|
| Rainbow's Foliage **Polytone edition v2.1** | **1363585:9092152** | Specific Polytone-dependent foliage version supports **1.21.1**, Euphoria/Complementary renderer and tree models |
| Os' Colorful Grasses **Mix** | **1690239:8936929** | User-requested colorful/fluffy ground; selected Mix among official variants. **All Rights Reserved** author assets delivered only by CurseForge app; do not repack manually |
| Bushy Pink Petals + Wildflowers + Leaf Litter | **1321476:8493563** | Vanilla flower models + Polytone foliage priority; cherry/wildflower render |
| Torches Reimagined v1.8 | **531730:8048795** | Animated handheld/placed fire, not a new server fire mechanics mod |
| Extended Illumina 1.21.x | **380413:6021451** | 3D held torch/lantern transforms; texture layering with Torches Reimagined |

**Installer caveat:** these are **official CurseForge project/file references in manifest**, not bundled asset bytes. Confirm on first import that CurseForge actually installs each to `resourcepacks/` and does not drop ZIP files in `mods/`; confirm they are **enabled as desired** in Resource Packs. If CurseForge import/pack state misbehaves, fix the pack installer/asset references or provide a single clearly labeled compatible client overlay rather than forcing 5 extra Minecraft test cycles. Polytone first, then Rainbow, Os Mix, Bushy Petals, Torches, Extended with clear override order. User requests shader real-time shadows **High** for the preferred look: screenshot/benchmark High versus a lower setting; do not force everyone to use expensive settings.

## What was excluded **because of real compatibility or clean-test constraints**

- **AmbientSounds 6** not added alongside Atmosfera Neo — same continuous ambient audio role. Can switch only if Atmosfera proves unusable.
- **Serene Seasons** not included with Euphoria visual seasonal plan — world-changing season clock, crop/snow/biome effects and FTF seasonal climate risk; not just a cosmetic addition. Test if genuinely wanted *real* gameplay seasons.
- **Euphoria Patches** is a local **Complementary shader patcher**, not a normal mod JAR/resource pack; requires legal installed shader patch and verified NeOculus 1.21.1 compatibility. Park separate shader preset application, not an extra gameplay beta.
- **Connected Bricks/Paths/Rocks** require compatible Continuity/OptiFine connected textures. Current Embeddium+NeOculus stack has no proven native CTM engine. Resourcepack alone won't make them work.
- **LambdaBetterGrass, Tightfire** officially Fabric/Quilt only; **Fairer Phantoms** official releases not native 1.21.1 NeoForge. No blind Connector build.
- **Night Lights** and new physically changing lantern/lighting systems held pending swinging lantern integration, to avoid conflicting block/chain render updates.
- **MCA Reborn/MineColonies** overhaul villagers' social/AI systems and could conflict with Guard Villagers + Easy NPC model. Not part of first living-world trial.
- **Mine Cells/Blue Skies/Big Globe** modloader/version/worldgen uncertainty/experimental dimensions, not part of current stable 1.21.1 release.
- **A second full farming, particle or ocean wildlife stack** overlaps installed content; the current additional fauna focuses on Naturalist plus client-only Cosy.
- User's unspecified **ambient particle** and extra fire-animation mod remain identity-unverified; existing AAA Particles/Particular/torch animation already occupy their role. No invented project IDs.

## ONE combined acceptance route

**Before:** import whole pack to a new CurseForge profile, preserve Test8.10 as rollback. Use a fresh world for new cave biomes/archaeology; test same graphics preset (NeOculus + Complementary, shadows High vs lower).

1. **Load/main menu (10 min)**: resolve all 289 CF refs (15 new mod/deps, 5 resourcepacks, 2 inherited QoL), launch NeoForge 21.1.252, stable shader window, no missing dependency popup. Confirm five resource packs in `resourcepacks/`. Server-side mod export must not force **client-only** Cosy/Resourcify into a dedicated server.
2. **Living towns (15–20 min)**: find vanilla + CTOV/T&T villages, inspect Guard Villagers' count, villager names, pathfinding, villager POIs and raids. Spawn/create a small Easy NPC through its config UI as an authoring **proof**, verify exact Core/UI matching, dialogue and persistence. Don't claim FTB quest integration until a specific task event/command works.
3. **Caves/archaeology (20–25 min)**: natural caves and one existing ruin; identify Galosphere cave access and Better Archeology sites, dig/brush a real object, check Archaeology Ruins coexistence, no repeat generation-pool warnings, ruined room clipping or spawner crashes. **Both are deliberately in same combined build**; if one clearly misbehaves, isolate *then*, not before the first test.
4. **Fauna/visual/audio (10–20 min)**: spot Naturalist and existing Alex's Mobs in forest/coast, note duplicates and aggressive counts, check Cosy Critters (client ambience and configurable Hat Man), Polytone foliage, Dense Flowers, swinging lantern and Torches Reimagined model position. Toggle Atmosfera soundscape volume with voice chat, no need for separate Minecraft launch.
5. **Quest/QoL (10 min)**: Controlling searchable keys, JEI recipe clickthrough to FTB, one broad gem task, Lootr and solo-vs-team reward. No questbook redesign in this batch yet.
6. **Performance and evidence**: sample server MSPT, FPS and RAM in inhabited town, lush flower field, dense animal area and first cold-generated cave; compare to known Test8.10 slow Streams height fallback (not a controlled same-route baseline). Send **one combined latest.log** plus five short observations/screenshots if available rather than separate logs per item.

**Stop/revert criteria:** startup crash/missing mandatory deps, worldgen-registry load failure, serious guard or Naturalist AI pathfinding stall, catastrophic shader/cave render, per-player quest duplication, core resourcepack install corruption, or modded biome/cave generation preventing reaching content. Minor sound levels, colors, too many passive animals, huge-shadow FPS drop or some texture seams can be config-tuned **without another pack ZIP**.

## Verification boundaries

CI can verify exact CF file pins/versions, old 273 NBT fixes, release manifest integrity and deterministic output. It **cannot** prove CurseForge resourcepack download/install path, server-side client-only mod omission, actual FTF cave reachability, Minecraft startup, GUI behavior, creature counts, sound overlap or multiplayer state. Mark runtime untested honestly until the single combined test.
