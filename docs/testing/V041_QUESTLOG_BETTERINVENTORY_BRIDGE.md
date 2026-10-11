# AO Questlog / Better Inventory bridge — v0.4.1 experimental

User request: integrate Questlog 3.4.1's inventory access into Better Inventory 1.3.2 on NeoForge 1.21.1, with notifications. Keep both mods and existing Mine Cells working configuration.

Source: `addons/ao-questlog-betterinventory/`. This is an original AO-authored client-only addon built by ModDevGradle (Java 21, NeoForge 21.1.252). It must be compiled before packing; **do not write class files by hand or claim a runtime test from CI**.

- Detect `dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen` by exact runtime class name and loaded mod IDs.
- On NeoForge `ScreenEvent.Init.Post`, add a proper clickable `Button` ("Q", top right of screen, tooltip `questlog.gui.open`). Better Inventory's `mouseClicked` forwards unhandled clicks to vanilla container screen logic, so this avoids patching either original mixin.
- Click dynamically creates Questlog's own `QuestlogScreen(Screen previous)` via reflection. This is the public Questlog 1.21.1 constructor, unlike the existing `QuestlogOpenButton(InventoryScreen)` which only accepts vanilla InventoryScreen. Do not substitute Questlog's own existing button.
- Notification badge uses Questlog's public `mostRecentNotificationQuest` and the same fallback logic as its own inventory button (`QuestlogClient.getLocal().getAllQuests(): isCompleted() && !isRewarded()`), checking rewards at most once per 20 world ticks. It draws a compact yellow exclamation overlay, **not an identical implementation of Questlog's custom badge sprite**. Respects Questlog's `button.showBadge`; never touches quest state/rewards.
- Client-only `@Mod(dist=Dist.CLIENT)`, no server dependency, no source-level Questlog or Better Inventory class imports. Optional graceful no-op outside BetterInventory screens.
- Pack integration: the build tool adds **only the self-authored compiled mod JAR** at `overrides/mods/ao-questlog-betterinventory-0.1.0.jar` after constructing the 328-CurseForge-ref working Mine Cells control candidate. This preserves the previous exclusion of Streams Reflowing, Noisiumed and Structure Essentials and retains the Luki + Dungeons & Taverns key model merge.
- Loader pin and exact affected source versions: Better Inventory project 1618019 file 9099710; Questlog 1202066 file 8952784.
- User must test on client: visible Q button at upper-right with BetterInventory inventory E, click opens Questlog; return preserves Better Inventory function; hover tooltip; recent quest notification and unclaimed reward badge; GUI scale 2/3/4, JEI right edge; multiplayer client, dedicated server with the client-only addon packaged. Other inventory screens should not receive an extra button.

Known limitation: top-right is not configurable yet. If that overlaps JEI UI, reposition later with screenshot-based evidence. If integration constructor / class changes on future versions, the button logs an error and gracefully remains on screen.

Sources:
- https://github.com/falling-colud/better-inventory/blob/main/src/main/java/dev/fallingcloud/betterinventory/client/screen/BetterInventoryScreen.java
- https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/client/gui/screen/QuestlogScreen.java
- https://github.com/infernalstudios/Questlog/blob/1.21.1/common/src/main/java/org/infernalstudios/questlog/client/gui/components/QuestlogOpenButton.java
- https://github.com/neoforged/NeoForge/blob/1.21.1/src/main/java/net/neoforged/neoforge/client/event/ScreenEvent.java
