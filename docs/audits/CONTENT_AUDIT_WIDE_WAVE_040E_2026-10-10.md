# Ambient Odyssey — 0.4e expansion from user audits and comparison modpacks
**Staged 10 October 2026:** new experimental branch `content/0.4.0e-audit-first-wide-expansion`, forked from successful 0.4d CI source. **Source/build trial, not runtime-certified; do not merge to main.**

## User-directed priority
Add substantial compatible content before post-expansion fixes, then worldgen/performance, balance and finally all quest authoring. Keep 0.4c/0.4d tested source and rare mutant settings. All eleven additions were drawn from previously nominated audit candidates, except equipment comparison / Legendary Tooltips, included after comparing with the gear-readability emphasis of Cisco's Medieval RPG, RAD3, Craft to Exile 2 and Prodigium. This is an *architecture inspiration*, not a claim that a specific source pack ships the same exact 1.21.1 NeoForge jar.

## Eleven exact CurseForge trial pins
| Requested content | CF project:file | Loader and role | Acceptance/overlap |
|---|---:|---|---|
| BetterF3 v11.0.3 | 401648:5873258 | client, NeoForge 1.21.1 | Debug screen, alt to vanilla F3 |
| Pick Up Notifier v21.1.1 | 351441:6409785 | client, NeoForge 1.21.1 | Small loot pickup notifications |
| Cave Dust Rethinking 3.3.0 | 1617531:8740321 | client, NeoForge 1.21.1 | Subdued environmental cave particles |
| Light Overlay v12.0.0 | 325492:5553811 | client, NeoForge 1.21.1 | Toggleable mob spawn light level visual |
| Inventory Sorter 24.0.18 | 240633:5979614 | both, NeoForge 1.21.1 | Explicit inventory sorting action |
| Subtle Effects 1.14.0 | 1023913:7768631 | both, NeoForge 1.21.1 | Optional particles and sounds; reduce overlap with existing FX |
| Traveler's Titles 5.1.3 | 1015155:6294123 | client, NeoForge 1.21.1 | Biome and dimension entry titles; does not implement journal/quests |
| Legendary Tooltips 1.5.5 | 532127:6400660 | client, NeoForge 1.21.1 | Clear visual rare-item tooltip styling |
| Map Distance Fix 1.1.2 | 1321830:8507645 | both, NeoForge 1.21.1 | Keep vanilla map orientation outside map bounds |
| Equipment Compare 1.3.13 | 502561:6375501 | client, NeoForge 1.21.1 | Compare player-equipped gear against loot stats |
| RightClickHarvest 4.6.1 | 452834:7508749 | both, NeoForge 1.21.1 | Right-click harvesting; Farmer Delight duplicate behavior audit |

Manifest target **296 to 307 unique CurseForge refs**; existing gameplay mods/resource packs and 273 8.10 NBT source repairs remain untouched. Never blindly repin shared baseline projects; abort on mismatches. The builder exports private NeoReef only for developer trials.

## Deliberately not auto-added despite earlier lists
- **AmbientSounds 6:** Atmosfera Neo already chosen, doubling constant audio is counterproductive, and water/rain already loud.
- **Paginated Advancements vs Better Advancements:** one screen replacement, exact native NeoForge 1.21.1 file and FTB UX check needed before adding; known Paginated filtered release appears Fabric only.
- **Dynamic Lights, Continuity CTM/Connected Bricks, Paths and Rocks, Better Block Entities, Voxy:** native Embeddium/NeOculus compatibility unproven or Sodium dependency; do not force core renderer switch.
- **Serene Seasons / Euphoria Patches:** gameplay calendar vs shader visual calendars, user decision necessary; keep current biomes and weather stable for content.
- **Visuality Reforged:** duplicates current Particular/AAA/Subtle particle families; no additional particle renderer in this wave.
- **Crops Love Rain:** farming balance/server tick effect best after RightClickHarvest interactions checked; not a reason to stop content expansion.
- **Critters & Companions:** duplicates some Naturalist/Alex's species, and user requested to trim fauna already. Revisit only after explicit unique-species selection.
- **All The Heads:** hundreds of drop tables and Curios/loot integration, hold for explicit collectibles/rare drop direction.
- **Explorer's Journals:** newly released, full registry/MP persistence unverified; Traveler's Titles is a lighter discovery signal; actual Questlog/FTB stays LAST.
- **APPA, Armor GUI, unnamed Fire/Ambient Particle mods:** no verified exact identity; don't substitute.
- **MCA Reborn/more bridges:** after quests as settled, not part of prelaunch content additions.

## Other pack comparison findings
- **Cisco's Medieval RPG Ultimate (1.19.2 Forge):** relies on strong differentiation of loot, weapons and combat feedback, but its curated origins/skill-tree and combat progression can't be copied into AO unchanged. AO already includes major combat/spell/accessory systems.
- **RAD3 (1.20.1 Forge):** deliberately emphasizes exploration, looting and accessible RPG systems rather than a kitchen-sink list; AO has the dungeons but can improve information/feedback and discovery UX.
- **Prodigium Reforged (1.20.1 Forge):** large authored boss/loot/progression loops; do not transplant its custom boss gates, scripted dimensions or story before AO balance and quest phase.
- **Prominence II (1.20.1 Fabric):** deeply customized story, voiced NPCs and progression modules; not drop-in NeoForge 1.21.1 content. AO's existing Easy NPC and Questlog plans already cover future narrative layer.
- **Craft to Exile 2:** inspirations include comparing stats and equipment across heavy loot, but no assumption of matching native ports. This is a project-independent UI feature, not an imported modpack bundle.

## Safety and next test wave
Static release and repeated deterministic archive builds check package reproducibility, expected CF files, rare mutant weights, exact NBT source repairs and 0.4c gamerules. **Only real Minecraft testing** can verify 5–7-player server performance, duplicate right-click crop handling, HUD/tooltip overlap, map rendering, keybindings and dual cave particle density. Individual game sessions should be **substantial grouped batches**, not micro-tests per 1–2 mods. The user's server opening ~15 October remains a target, not a safety guarantee.
