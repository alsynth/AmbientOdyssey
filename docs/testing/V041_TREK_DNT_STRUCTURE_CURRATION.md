# Trek + Dungeons & Taverns: v0.4.1 experimental structure replacement

**Branch:** `experimental/v0.4h-trek-structures-20261010`. Runtime untested.

## Approved selection

- **Remove** Repurposed Structures NeoForge (CurseForge project 368293), plus its RS-only Farmer's Delight compatibility addon (project 1071336). Preserve normal Farmer's Delight and unrelated structure mods.
- **Add** Trek B0.6.2 server-side structure mod (CurseForge project 1418999). Its particular 1.21.x file needs binary/header verification before treating the pin as final.
- **Keep** Dungeons & Taverns v4.4.4 NeoForge, but disable *routine Overworld clutter*:
  - all `nova_structures:remnant_*` except the special `remnant_taiga_castle`;
  - `nova_structures:village_*` settlements (Trek, CTOV and other village authors already cover this role);
  - `ruin_town`, `wild_ruin`, `jungle_ruins`, `desert_ruins`.
- **Retain** all vanilla/Nether/End DnT content and major forts, castles, crypts, boss dungeons, Shrines, pillager mansions, taverns, watchtowers, wells, etc. No planned alterations to their spacing/salts.
- Existing world chunks cannot retroactively change; test worldgen in fresh worlds and keep the current Q1 pack as rollback.

## Important technical constraint

Most ordinary DnT debris/village variants share the **`nova_structures:remnants` weighted structure-set** with the taiga castle. Removing entries naively would promote rare castle generation to an extremely high frequency, so **do not** blindly override the shared structure set. The selected approach copies the exact native DnT structure JSON and changes *only* its biome holder-set to an intentionally empty `#ambient_odyssey:dnt_trek_disabled` tag. Unwanted structures become biome-ineligible, leaving untouched all native structure-set entries, weights, spacing, separation, biome rules for retained content, and IDs.

Source: official DnT 1.21.1 NeoForge version `BYUUUeZA`; `tools/derive_dnt_trek_curation.py` verifies its SHA512 and writes the override datapack and audit report from actual native JAR assets. **The Minecraft runtime still needs to verify Paxi's datapack priority and the empty-biome-tag behavior**. If jar version doesn't match the installed DnT, stop instead of guessing.

## Required testing before acceptance

1. Check Trek's exact 1.21.1 release binary metadata and mod/data-pack namespaces, structure registries and biome tags.
2. Verify selected DnT structures can no longer locate or spawn; `/locate structure nova_structures:remnant_graveyard` should not find new structures. Existing world sections unaffected.
3. Check special DnT castles, monster encounters, all Nether and End structures at expected rarity, and tavern maps.
4. Inspect Trek villages replacing/overlapping vanilla/CTOV/Towns & Towers/Integrated Villages, including Waystone spawns and fresh-world portal paths.
5. Check compatibility with modded biomes and FTF terrain transitions, clipped structures, overlap/exclusion radius, generation time and chunk pregeneration.
6. Verify client/server, 2-player quests, and 5–7-player server MSPT separately. **Static tests do not establish playable worldgen.**

Source files and generated packs never redistribute DnT's complete JAR. The selected edited structure JSON is produced for local compatibility; the original game content stays mod-provided.
