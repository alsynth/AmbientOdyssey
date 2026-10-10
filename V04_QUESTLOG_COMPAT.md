# Ambient Odyssey v0.4h — Questlog compatibility trial

**New candidate branch:** `experimental/v0.4-preflight-hardening-20261010` · Minecraft 1.21.1 · NeoForge 21.1.252 · **331 pinned CurseForge references**.

## Precisely what is included

- **Questlog 3.4.1 native NeoForge:** CurseForge project `1202066`, file `8952784`, `questlog-neoforge-1.21.1-3.4.1.jar`. Do not use the different Fabric build even though Sinytra Connector is installed for Mine Cells.
- Already inherited **Cloth Config 15.0.140 NeoForge:** project `348521`, file `5729127`; verified in the original binary dependency audit. No redundant library installation.
- Existing **FTB Quests, FTB Solo Quests, FTB libraries and the FTB Field Manual plans** remain in the build. Questlog complements those systems; it is not replacing them.
- **No quests, progression tasks, chapters, rewards or archaeology campaign are shipped.** This mod's empty journal is intentional until quest writing comes after content selection.
- Mine Cells/Connector/FFAPI, the previous 12 0.4f/g additions, 273 native NBT corrections, curated worldgen and server gamerules remain unchanged.

## The inventory button can be moved without rebuilding the inventory GUI

The official [Questlog 1.21.1 source](https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/config/QuestlogConfig.java) defines `button.enabled`, `button.relativeToInventory`, `button.x`, `button.y`, the notification badge and offsets. The [button renderer](https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/client/gui/components/QuestlogOpenButton.java) subtracts 18 from X and Y and optionally adds the inventory's position.

A source-grounded **trial**, not a verified visual fit, is supplied in `overrides/config/questlog-client.toml`:

```toml
[button]
enabled = true
showBadge = true
relativeToInventory = false
x = 38
y = 38
badgeX = 24
badgeY = 0
bobbingBadge = true
```

This aims to render the journal button near screen coordinates **20,20**, independent of whether the modded inventory screen extends above or to the side of the usual panel. The default Questlog inventory-relative position would put its icon *above the inventory*, which could be obscured by modded UI. Exact clickability and any overlap must be inspected in the actual game.

**Backup access:** Questlog's original 1.21.1 source maps `key.questlog.open` to the grave-accent/backtick key (` ` `); check Options → Controls if a keyboard layout or another mod consumes it. The pack does not silently force a replacement binding.

**When reviewing the GUI on a real client:**
1. Open `E` inventory at GUI scales 3 and 2. Take screenshots with Questlog, Curios/Accessories, JEI panels and the usual player inventory visible.
2. Verify the icon remains within the window and can be clicked; make sure notification badges are readable and nothing else is covered.
3. Use the backtick shortcut even if the icon is hidden. Check FTB Quests separately so the two systems do not fight over controls.
4. Try changing `[button].x`, `y` or `relativeToInventory` in `config/questlog-client.toml`. Restart to confirm persistence.
5. Test player inventory with status effects, crafting, JEI search, various resolutions, and in multiplayer. Final position is pending those actual screenshots.

## Static verification and open risks

The source checks verify the exact project/file pins, inherited Cloth Config, valid TOML values, bridge integrity, 331 unique references, and that no Questlog quest campaign is shipped. The complete experimental ZIP and clean deterministic rebuild are validated through GitHub Actions. These tests cannot establish Minecraft runtime startup, InventoryScreen mixin interactions, empty journal sync, icon clickability, FTB Quests coexistence, or server-side safety.

If the journal disappears in a customized inventory, it may be an inventory mod that replaces vanilla `InventoryScreen` and bypasses the Questlog mixin; changing X/Y alone would not fix that. Examine the startup log and screenshot first rather than guessing a global mixin fix. Questlog should be installed on **both client and dedicated server**, based on the mod author's published environment.
