# Ambient Odyssey 0.4.0-c0 — user playtest, sound balancing, ecology curation, rules and content direction
**10 October 2026.** Source: user-provided complete `latest(20261010-143535).log` (21,271 lines, private log NOT committed), plus user observations on the actual **0.4.0-b1** combined 289-ref importer. **Changes are next larger patch**, not a micro-test; preserve successful Test8.10 FTF/Biolith worldgen repairs.

## User acceptance & technical reality

User confirms categories **1 / 2 / 3** of the combined test (launch, settlements, caves/archaeology) **work to their satisfaction**; cannot reliably tell duplicate wildlife by direct observation. **Controlling works perfectly** and UI reveals many conflicting keybinds. Rough client performance with shaders at **render 12 / simulation 12** is **50 FPS**, **40 FPS in rain**; user perceives **no material decline from previous build**. These are **self-reported experience estimates, not controlled percentile FPS benchmarks**.

Exact source log:
- Launch MC 1.21.1 / NeoForge 21.1.252, player joined 16:02:36 and left 16:34:50; saved and shutdown normally ~16:35:15, no client crash.
- **6,116 chunks generated** (FTF shutdown report), **18 server** `Can't keep up!` warnings; **18.600 seconds** worst single incident; combined millisecond debt ~103.9 s across warnings. Real-world client FPS and server main-thread load are distinct.
- **0** `No starting jigsaw`, **0** `Couldn't find template pool`, **0** `Failed to create valid structure` in this route. **Nine** vanilla `POI data mismatch: already registered` errors, not attributable to a specific mod/biome yet. No broad structural rewrite.
- Streams Reflowing again reports **ReTerraForged terrain unavailable while preparing streams; fast terrain mode OFF**, which may contribute to cold generation time. Not confirmed to cause audio: **Streams Reflowing is worldgen**, while flowing-water sounds may come from the water block audio category, the **Waves** mod or **Atmosfera** audio layer.
- Other log warnings: Naturalist optional `fieldguide` mixin target classes absent; Galosphere registered missing sound files; Traveloptics malformed tag; Iron's Jewelry test loot; repeated FTB Library invisible entity icon complaints; resource reloads. They did not prevent successful play. Removing Galosphere may remove its own errors but other mods' conditional recipes must still be checked.
- Native wildlife audit: [all-source species and duplicates](../audits/CONTENT_040C_ALL_WILDLIFE_AND_FRIENDLY_MOB_CATALOG_2026-10-10.md), [JAR enumeration CI](https://github.com/alsynth/AmbientOdyssey/actions/runs/38060841765).

## Sound fix — four practical controls and attribution

User says **Streams Reflowing stream/water sounds are overpowering**, rain also too loud relative to bird/insect/forest soundscape. Some Atmosfera bird/insect sounds are audible when standing above treetops but seem to disappear beneath leaf canopy. **No claim of intentional canopy logic without examining the actual Atmosfera biome/sky exposure rule.**

What 0.4c **actually changes**:
1. [`config/waves-common.toml`](../../release_030/overrides/config/waves-common.toml): `waveVolume: 1.0→0.25` (−75% engine volume multiplier), and `waveBreakingSoundChance: 40→120` (wave breaking sound becomes ~3× rarer *when other spawn conditions equal*). **This targets Waves coastal sounds specifically; NOT necessarily all Streams Reflowing river sounds**.
2. [`config/defaultoptions/options.txt`](../../release_030/overrides/config/defaultoptions/options.txt): new-profile **Weather** slider `0.5→0.2` and **Blocks** slider `0.7→0.4`. Retain **Ambient** `1.0` and other audio mix; avoid turning off the forest atmosphere. These defaults touch non-water block sound effects too; do not falsely claim water-specific sound-event remapping.
3. **Existing profiles:** DefaultOptions is a *new/default preferences* delivery mechanism. Players who have modified `options.txt` may need to adjust Weather to **20%**, Blocks to **40%** manually. Test a storm, a real stream and a coast; don't apply volume change twice by accident.
4. **Canopy sound issue:** leave Atmosfera Neo 1.0.2 installed pending native conditions/config audit. If the engine checks direct sky, consider allowing subtler bird/insect bed beneath treetops without constant sound above canopy; A/B only if config supports it. Don't install AmbientSounds 6 in parallel. Review resource-pack volume/style and category effects before any codec patch.

## Requested global game rules — implemented, not merely documented

Independent Paxi 1.21.1 pack [`ao_server_rules`](../../release_030/overrides/config/paxi/datapacks/ao_server_rules/pack.mcmeta) (pack format **48**) supplies a standard vanilla `minecraft:load` tag referencing a vanilla function:
```mcfunction
gamerule playersSleepingPercentage 30
gamerule doFireTick false
gamerule mobGriefing false
```
The datapack load function runs at world load / datapack reload, **no administrator manual chat command** normally needed when Paxi includes enabled datapacks. `ceil(6×0.30)=2`, so 2 of 6 can skip a night.

**Critical caveat of requested `mobGriefing=false`:** it blocks vanilla creeper explosion terrain damage / ghast and Enderman changes, but **also disables normal villager crop harvesting/replanting** and changes some friendly mob terrain interactions. Some boss/mod explosions can ignore vanilla gamerules; FTB Chunks claims still deserve testing. If the group later values farming, use a *verified* creeper-block-damage-only alternative instead of pretending this rule has no downside. `doFireTick=false` prevents vanilla natural fire spread but modded magic/flamethrower griefing can ignore the rule. Confirm on a test world and after restart.

## Immediate content decisions — locked in source for 0.4c

- **Galosphere**: **remove its only new-CurseForge addition (631098:8242886)**, keeping original cave/biome generator and **Better Archeology**; no new cave biome should be removed from an already saved final server world (we are not at permanent server pregen yet).
- **MineColonies**: **not wanted**; do not add it in content expansion.
- **MCA Reborn**: **defer; user may revisit in later vision audit**, no automatic install/removal of current village systems.
- **Better Archeology** only makes sense when it leads to *rare, genuinely surprising and high-value discoveries*, integrated with specialist quests. Do not substitute 20 mundane pottery-shard tasks for meaningful content.
- **Alex's Mobs** `gorillaSpawnWeight=0`, `flySpawnWeight=0`, `cockroachSpawnWeight=0` implemented, keeping entities/items/mod installed. Other pests (Naturalist rats/ants; overlapping Ben's/Hybrid shark) need native spawn-controller checks before modifying JSON arbitrarily. **Creature exists ≠ naturally spawns**; some FTB Ocean Mobs never spawn naturally unless configured.
- **Controlling**: user confirmed success. Next action is systematic comprehensive keybind conflict redesign; do **not** repin/update or re-test this single mod.

## Planned player-facing archaeologist arc — specialized, difficult tasks, extraordinary but bounded rewards

**Design direction (not yet executable FTB Quest SNBT):** optional *Archaeologist's Field Commission* beginning at a curated Easy NPC (same client 7.14.0):
- **Commission I — Forgotten Traces:** brush/explore a **real naturally found** Better Archeology site; deliver an actual validated archaeological item or report. **Reward** stronger than a typical beginner loot chest (e.g., several diamonds and archaeology compass/map plus XP). Single award per player, not repeatable.
- **Commission II — Rare Reconstruction:** collect **multiple distinct site-specific relics**, not 10 generic shards, and verify an actual rare dungeon/structure discovery. **Reward** one valuable midgame upgrade (e.g., one netherite upgrade smithing template, rare equipment or carefully constrained Apotheosis-quality gem; exact item ID/rarity to validate). Requirement should take meaningfully longer than normal world exploration.
- **Commission III — Lost Civilization:** multi-region evidence, puzzle/field-journal step and dangerous expedition to curated existing ruins with Lootr independence. **Reward** one genuinely memorable late midgame prize (e.g., a hard-to-get unique artifact/cosmetic trophy + substantial resources, no infinite repeatable OP item farm). Test reward tags and quest progression against FTB Solo Quests; no mass kill quests; story remains optional.

**Implementation gate:** Obtain actual Better Archeology item IDs/suspicious-block loot evidence and test FTB Quests 2101 item/advancement/dimension task syntax; independent co-op rewards exactly once per character. No speculative JSON-generated items, invalid any-gem SNBT filters, impossible rare-site coordinates, or massive per-player gems without balance. Build this as substantive future quest content integrated with other 0.4 expansion features; user requested fewer/bigger tests.

## Keybind overhaul — planned, not falsely claimed deployed

Existing `DefaultOptions` ships only three intentional override lines: disables FTB Chunks redundant map key and the Accessories GUI key, keeps known microphone mute key at J. **Do not add fictitious key IDs to the file.**

Use Controlling's conflict filter to collect **actual resolved conflicting binds** after all core mods are in, then construct one reproducible `defaultoptions/keybindings.txt` profile (for new installs) grouped by:
- Vanilla movement/inventory/hotbar; keep default `WASD`, `E`, `Q`, `Shift`, `Space`, `T`, `F5` and preserve player chat/voice.
- Mapping/navigation and exploration: *one* world map, one minimap, guidebook/Questlog, Waystones.
- Combat/magic: combat stance/dodge, spell wheel/cast, relic activation, Curios/Accessories; avoid collisions and avoid defaulting any destructive action to ordinary inventory key.
- Create/engineering, farming/building, team/chunks/admin utilities: secondary keys or **unbound by default** for rare operations.
- Reserve a future configurable **Questlog inventory button** near JEI/Curios; don't claim it is installed. Keep access to keybind search and a beginner Tips & Tricks section with unusual controls.

**Required input for a true modpack-wide conflict-free profile:** actual set of keybindings after the selected mods register, ideally Controlling export/screenshots or a known loaded `options.txt`. The latest client log contains mod JAR registrations but **not actual user keyboard assignments**, so exact collision elimination cannot be honestly completed from it.

## CI-verified private candidate: source/integrity success, not Minecraft runtime proof

[**GitHub Actions build 38061358812 — PASS**](https://github.com/alsynth/AmbientOdyssey/actions/runs/38061358812). Ran old **28 terrain + 31 structure source checks**, native Graveyard/Swiss lighthouse repairs, all **273 binary roundtrip native NBT** fixes, source checks for 30% sleep/fire/mob grief global load tag, new wave/weather/block levels, Alex's gorilla/fly/cockroach spawn weights, **288** official CurseForge references, absent Galosphere and preserved Better Archeology, exact private NeoReef jar SHA, independent ZIP CRC/manifest. Two **byte-identical** builds.

- Exact inner CurseForge importer: `Ambient-Odyssey-0.4.0-c0-World-Rules-Wildlife-AUDIO-PRIVATE.zip`
- **70,816,743 bytes** · **1,389 ZIP members** · SHA256 **`d56db4003161a9f6f93f0ac29f694f5b3a434ec370f6da10faddb22ba0b252d1`**
- Independently extracted GitHub artifact **outer ZIP** and inspected **inner ZIP** in container: correct sha/size, `manifest.json` at root, verified three commands in exact datapack, `waves-common.toml` new values. Import only the **inner** ZIP.
- There has been **no Minecraft gameplay launch of 0.4c**. Gamerules still require normal new world / server-restart acceptance. This pack contains a broad user-feedback repair slate but **does not include playable archaeology quest lines or completed keybind profile**. In keeping with the user's anti-micro-test policy, no separate test session is requested merely for this build.

## Next release rule

Single **substantial** next pack (0.4c or larger) containing Galosphere removal, curated wildlife/audio/gamerules, archaeology quest prototype when IDs are confirmed, and keybind profile when resolved. Do **not** ask for separate human Minecraft test for each small sound/config change. Validate archive, source invariants and load-trigger presence in GitHub CI; user can verify all at next substantial gameplay session.
