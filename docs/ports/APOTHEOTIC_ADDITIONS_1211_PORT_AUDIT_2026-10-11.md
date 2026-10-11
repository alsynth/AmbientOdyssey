# Apotheotic Additions -> Ambient Odyssey 1.21.1: Port audit

**Status: port source identification and feasibility audit. No ported mod is installed in the v0.4.5 preview. Do not claim implementation.** 11 October 2026.

## Original project, version and license
- Original project identified: [Bryce792/ApotheoticAdditions](https://github.com/Bryce792/ApotheoticAdditions), version **2.2.2** according to `META-INF/mods.toml`.
- The original repository contains **2,406 tracked paths**, with a mixture of MCreator Java class source/artifacts, assets and a large number of data-driven entries.
- Original metadata: Minecraft **exact 1.20.1**, legacy Forge loader [47,), Apotheosis **7.4.3+**. Current AO: MC **1.21.1**, NeoForge **21.1.252**, Apotheosis **8.9.0**. Cannot just edit `mods.toml` or copy old data files into 1.21.1.
- Original `mods.toml` says **Academic Free License v3.0**; review actual permissions and attribution of original assets/dependencies before distributing a derivative. Preserve credits and license notices; don't assume separately sourced art is unrestricted.
- Original README: adds **Artifact**, **Heirloom**, **Esoteric** rarities (Esoteric intentionally unobtainable), 33 jewels, rogue spawners, apotheotic coins/trades, custom boss affix loot, shelves, crafting/salvaging and large cross-mod compat.
- Upstream tracked category sizes (approximate file entries, including directories):
  - 723 affix loot entries, 315 affixes, 249 recipes, 135 bosses, 112 wanderer trades;
  - 99 minibosses, 85 gear sets, 82 gems, 26 rogue spawners, 31 enchanting stats;
  - 47 old `net/mcreator/apotheoticadditions` class paths.
- AO already includes native Apotheosis 8.9.0, Apothic Combat 1.2.1, Apothic Attributes 2.11.0, Apothic Enchanting 1.6.3 and other 1.21.1 components. This is *not* equivalent to Apotheotic Additions.

## Safe port phases

1. **Registry/schema diff**: compare original 1.20.1 Apotheosis 7.4 data formats (affixes/loot rarities/gear sets/gems/bosses) to pinned 1.21.1 8.9; inspect licensing and original custom code to identify items requiring real Java port vs structured data conversion.
2. **Minimal prototype on isolated branch**: original Artifact / Heirloom rarities + a tiny sample of compatible affixes and gems using 1.21 native codecs; no Esoteric as a natural drop. Compile minimal custom items if absolutely required. Verify datapack reload and JEI.
3. **Integrated cross-mod pass**: migrate only actual AO-installed addon integrations (Aether, Alex's Caves/Mobs, Aquamirae, Ars Nouveau, Cataclysm, Create, Forbidden Arcanus, Ice & Fire, Iron's Spellbooks, Mutant Monsters, Twilight Forest, Undergarden), filtering out absent dependencies.
4. **Gameplay balance and server checks**: ensure rarity unlock/drop tiers, forge/reforge/salvage, gems, trading, rogue spawners and multiplayer progression do not bypass AO balance. Preserve user-selected high-end rarity concept.
5. **Whole-port acceptance**: only label as Apotheotic Additions port when expected major systems function. A tiny subset with renamed loot is not a full port. CI binary compile and in-game cold+warm launch needed.

**Do not include broken data or untested MCreator JAR in the main CurseForge ZIP.** The v0.4.5 armor-trim addon is an independent narrow feature and must not be misrepresented as the Apotheotic Additions port.
