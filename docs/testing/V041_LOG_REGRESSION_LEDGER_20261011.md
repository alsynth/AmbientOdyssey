# Ambient Odyssey v0.4.1 — latest runtime triage and next gates

**Observed source:** user-shared `latest(20261011-121133).log`, 8,953 lines, Minecraft 1.21.1 NeoForge 21.1.252 with three AO experimental addons. This is log-based evidence, not a replay or in-game patch verification. Do not publish the raw log: it contains local launcher and account metadata.

## Observed messages

| Signal | Count | Priority | Workstream |
|---|---:|---|---|
| `Item must not be minecraft:air` | 504 | High | Native structure NBT source attribution, no blanket item replacements |
| `Tried to add entity minecraft:zombie but it was marked as removed already` | 103 | High | Hominid 1.3.4 upstream FinalizeSpawnEvent lifecycle, opt-in prototype only |
| Server `Can't keep up` | 10 (worst 6,671ms) | High | Spark spike analysis, NOT p95 MSPT |
| Unknown item registry keys | 7 | Medium | Source-specific outdated item IDs from Supplementaries and vanilla aliases |
| POI data mismatch | 2 | Medium | Check structure placement and village POI registration under worldgen |
| Hominid/Tan's previously logged off-thread add signature | 0 this session | Monitor | Prior worldgen-safety addon; absence does not confirm test coverage |
| Missing Luki mansion template-pool signature | 0 this session | Monitor | Existing patch not conclusively playtested |
| Dungeon Crawl spawner missing-block-entity signature | 0 this session | Monitor | Requires a targeted physical Dungeon Crawl spawn test |

## Source-backed error ownership

**Hominid:** [upstream HominidClientEvents.java](https://github.com/Alganaut/Hominid/blob/main/src/main/java/com/alganaut/hominid/registry/event/HominidClientEvents.java) calls `event.getEntity().discard()` inside a `FinalizeSpawnEvent` listener before the original zombie is inserted. Official [NeoForge 1.21.1 FinalizeSpawnEvent](https://github.com/neoforged/NeoForge/blob/1.21.1/src/main/java/net/neoforged/neoforge/event/entity/living/FinalizeSpawnEvent.java) says cancelling the event does not suppress actual spawning; `setSpawnCancelled(true)` does. This is a strong match to the repeated removed-zombie warnings, but there is no stack per warning attributing every instance to Hominid. An isolated source-compiled AO prototype uses official cancellation and deferred TickTask insertion, preserves native rare mob types and leaves off-thread structure zombies untouched. **Do not call it runtime fixed before Minecraft tests.**

**Invalid air:** historical [native source scan CI 38105277049](https://github.com/alsynth/AmbientOdyssey/actions/runs/38105277049) identified `minecraft:air` inside structures from multiple mods, including When Dungeons Arise, IDAS, Archaeology Ruins, Iron's Spellbooks, Floating Islands and Dungeons & Taverns. Some locations were empty Count=0/optional villager offer slots, others Count=1 in block-entity display/filter tags. The scan covered an older Test6 SHA index (65 mapped of 72 candidate JARs), not all current 329 CurseForge references. **Do not mutate all occurrences**; prioritize exact game-generated structure and template, owner, non-default item semantics and full data preservation. The 7 IDAS old Create crushed-iron IDs are addressed separately by the pinned exact two-template compatibility overlay, not equivalent to the 504 air errors.

**Quest progression:** prior FTB Field Manual, Tips and Keybind chapters had 32 `tasks: [ ]` pages. The newest TREK+Manual candidate restores 32 previous distinct deliberate checkmark task IDs, zero new rewards and unchanged WDA/Questlog. Source and ZIP checked; new disposable world required for test because existing quest NBT remains completed. Native Questlog `questlog:read` objective [upstream source](https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/core/quests/objectives/misc/ReadObjective.java) listens for player reading the particular quest, not world login. Do not disable those intended manual-read objectives.

**Questlog inventory tab:** Existing v0.1.2 native Better Inventory source-atlas Q tab is in the installed ZIP, but user reports the visual problem persists. Need full Better Inventory GUI screenshot at GUI scale 2/3 showing fifth backpack tab, gear and Questlog icon before changing placement. Any future source fix must keep keyboard access and avoid duplicated native InventoryScreen button.

## Performance and worldgen gates

- User reports TREK/Create tuned structures generate acceptably; no perceptible performance difference. **Keep accepted density settings**, do not claim FPS or TPS improvement.
- Spark profile 2 showed last-minute 41.55ms mean, 26.76ms median and 5,994.88ms maximum; other samples median 25–26ms with intermittent spikes. [Spark source audit PR #25](https://github.com/alsynth/AmbientOdyssey/pull/25) contains the sampled thread report. Not evidence that TREK/Create controls affect lag.
- Do not add further speculative optimization mods or broad worldgen edits until a profile captures the slow cold chunks.
- Xaero map apparent loss: chunk unload outside simulation/view distance is normal, but missing persistent map tiles require checking Xaero's map dimension, cave/height layer, disk cache and re-entry. No confirmed world corruption in log. Never delete map files without backup.
- Swinging Lanterns explicitly warned it has no Embeddium suppression hook and may double-render lanterns; investigate as a separate visual/render compatibility workstream rather than changing it inside quest/hominid test ZIPs.
- Preserve rollback build and newly generated world testing. No public release until dungeon compatibility and multiuser Mine Cells/Streams regressions are tested.
