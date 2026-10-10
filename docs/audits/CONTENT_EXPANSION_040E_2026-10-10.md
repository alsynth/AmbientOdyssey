# Ambient Odyssey 0.4e — prior-audit expansion and comparable-modpack review

10 October 2026. **Draft branch, NOT launched, not gameplay-tested.** The user's instruction is to add the maximum compatible value from previously researched candidates first and then use comparable packs to find genuine gaps.

## Newly pinned official 1.21.1 NeoForge project files — six

| Role | Mod | CurseForge project:file | Why selected |
|---|---|---|---|
| Client only; debug HUD | BetterF3 11.0.3 | [401648:5873258](https://www.curseforge.com/minecraft/mc-mods/betterf3/files/5873258) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |
| Client pickup UX; Puzzles Lib available | Pick Up Notifier 21.1.1 | [351441:6409785](https://www.curseforge.com/minecraft/mc-mods/pick-up-notifier/files/6409785) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |
| Client spawnlight overlay | Light Overlay 12.0.0 | [325492:5553811](https://www.curseforge.com/minecraft/mc-mods/light-overlay/files/5553811) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |
| Client cave particle ambiance; benchmark/adjust overdraw | Cave Dust Rethinking 3.3.0 | [1617531:8740321](https://www.curseforge.com/minecraft/mc-mods/cave-dust-rethinking/files/8740321) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |
| Client biome and dimension names; discovery UI not persistent progress | Traveler's Titles 5.1.3 | [1015155:6294123](https://www.curseforge.com/minecraft/mc-mods/travelers-titles-neoforge/files/6294123) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |
| Ambient details; conservative tested baseline instead of brand-new 1.15; avoid duplicated sound/particles | Subtle Effects 1.14.1 | [1023913:7853614](https://www.curseforge.com/minecraft/mc-mods/subtle-effects/files/7853614) | Verified same major MC version and NeoForge build; no known duplicate exact project in source lock |

These complement the seven 0.4d content experiments, eight preceding 0.4d + Athena pins, and retained larger worldgen content. Expected **302 CurseForge manifest references** after the importer rebuild (formerly 296). Exact official file IDs checked from individual CurseForge file pages. The six are not replacements for core mods or renderers.

## Conflicts, intentional omissions, and conditional choices
- **Client environmental effect overlap:** Cave Dust and Subtle Effects can duplicate Particular, AAA Particles and Better Smoke. Keep these on the experimental branch as a single measured visual bundle. Tune individual categories in the later bug/compat phase if needed; drop an effect if not configurable. Do not ship as verified visuals yet.
- **Discoveries:** Traveler's Titles offers biome/dimension text only, **not** a per-player discovered structure list or FTB quest/Questlog integration. Those remain explicitly separate.
- **Map Distance Fix** version spans were verified but its correct 1.21.1 NeoForge exact file ID was not independently established; left out to avoid incorrect pin. **Explorer's Compass** is a good genre idea but possibly present in baseline; do not duplicate/repin until comparison against baseline CF manifest is completed.
- **Connected Bricks/Paths/Rocks and Continuity** remain parked pending proven Embeddium/NeOculus CTM support. No BBE/Sodium swap, no Voxy/DH stack.
- **Better Advancements versus Paginated Advancements** remains a one-of-two decision, not both. **Serene Seasons** could radically affect large multi-biome climates/crop balance; no addition before compatibility review.
- **MCA Reborn** after quests, **MineColonies** excluded, **Galosphere** excluded, **Big Globe** parked, no more random structure density.

## Other modpacks — screening method rather than guessing a curated roster
Compared intended gameplay pillars commonly associated with [Craft to Exile 2](https://www.curseforge.com/minecraft/modpacks/craft-to-exile-2), [Cisco's Fantasy Medieval RPG](https://www.curseforge.com/minecraft/modpacks/ciscos-fantasy-medieval-rpg-ultimate), [Prominence II](https://www.curseforge.com/minecraft/modpacks/prominence-2-rpg) and [RAD2](https://www.curseforge.com/minecraft/modpacks/roguelike-adventures-and-dungeons-2): purposeful exploration/navigation, rewarding long-tail character progression, richer settlements, world landmarks, collectible cosmetics and accessible onboarding. **No claim of exact versions or mod inclusion was made from these broad pack references**; those require actual downloadable manifests, because most comparable packs target different Minecraft/loaders.

**Two useful cross-pack genre ideas to screen (not pinned yet):** Explorer's Compass for structure discovery (only if absent from baseline, and if it doesn't trivialize rare structure exploration), and thoughtful player-owned collectible systems rather than unbalanced universal dungeon loot drops. This audit avoids the tempting but erroneous tactic of copying entire foreign mod lists without version checks.

## Release gate
New pins are curated based on official file pages; automated baseline collision, manifest count, existing native 273 repaired pool checks and ZIP determinism are mandatory. **Only in-game startup and client/server/shader tests can establish practical compatibility.** Source tests alone never prove performance or lack of animation/audio overlap.
