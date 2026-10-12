# Enigmatic Legacy+ / Better Inventory bridge

Client-only optional addon for Minecraft 1.21.1, NeoForge 21.1.252, Enigmatic Legacy+ 1.1.2 and Better Inventory 1.3.2. No changes to either original JAR, inventories or packets.

The 24x20 E tab uses Better Inventory's installed atlas and native normal/hover rows. Its preferred position is below the left tool slots. Bounds, existing visible widgets and active inventory slots are checked before placement, with safe fallbacks. Questlog's Q tab is centered above the right armor panel, as requested. A mouse-pre event routes only the visible ring tab hitbox before the native container can consume that lower area.

Visibility requires the actual `CURSED_RING` Curio and `CursedRing.enableEnderRing`. A stored `SevenCursesBearing` flag or the separate Ring of Ender does not show this Seven Curses tab. The original mod's other screens are unchanged. The button delegates to the native `EnderChestInventoryButton.getInstance(...).onPress()`, including carried-stack handling and server validation. Equip/config state is checked before rendering and clicking. Reflection failures disable the integration and log one error.

Build with the repository's cached Gradle 9.2.1 runtime and `CI=true`; run `build`. Runtime QA source is separate in `tools/ring-probe`, never included in the import.
