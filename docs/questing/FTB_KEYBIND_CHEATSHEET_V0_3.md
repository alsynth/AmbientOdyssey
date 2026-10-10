# Ambient Odyssey — FTB Field Manual: Keybind Cheatsheet (draft v0.3)

**Status:** ready-to-edit educational page copy, **NOT yet an imported FTB Quests page**. Written for Minecraft 1.21.1 NeoForge. **Keys can be customized in Options → Controls → Key Binds**; the current player's game settings take precedence over listed defaults. The final published version must be generated or audited against the *actual released AO default controls*, including `defaultoptions`, Keybind Overrides, added Origins/Questlog/QoL mods and user-rebind support.

## 00. Five controls you'll actually use

| Action | Default / current AO baseline | Why it matters |
|---|---|---|
| **Show how to make an item** | Hover item → **R** (JEI default) | Recipe and machine input |
| **Show what an item is used for** | Hover item → **U** (JEI default) | Figure out why a strange boss drop or material matters |
| **Find a location on your full-screen map** | **M** (Xaero's World Map default) | Avoid losing a dungeon or portal |
| **Mark a discovery** | **B** (Xaero's Minimap default) | Create a waypoint before entering danger |
| **Open accessories** | **O** (AO-distributed Keybind Overrides / DefaultOptions setting) | Manage rings, charms and Curios/Accessories layout |

**Important:** The AO overrides currently define **J = mute microphone**, **O = accessories screen**, and **FTB Chunks map = unbound**. They are present in:
- `release_030/overrides/config/defaultoptions/keybindings.txt`;
- `release_030/overrides/config/keybindoverrides-client.toml`.

**Caution:** `keybindoverrides-client.toml` presently has `applyOverrides = false`, meaning that source config **will not currently force those overrides on next launch**. DefaultOptions may still apply them to new profiles. Never call these controls guaranteed for an existing player's customized client until tested. The map keys above are **Xaero defaults**, not explicit AO overrides.

## 01. Basic inventory and combat

| Key / interaction | Action | Tip |
|---|---|---|
| `E` | Open inventory | Access equipment, crafting grid and JEI item list |
| `Q` | Drop one held/hovered item | Be careful near lava, void or other players |
| `Ctrl + Q` | Drop a full hovered stack | Especially dangerous near a boss arena; verify selected/hovers |
| `F` | Swap selected hotbar item with off-hand | Great for quickly switching torches, shield or Totem-style utility |
| `Shift + Click` | Quick-move an item stack to/from container | Often much faster than dragging |
| `1–9` while hovering an inventory item | Exchange it with the chosen hotbar slot | Useful when reorganizing mid-expedition |
| `Double Left Click` (inventory) | Gather matching items onto the cursor | Behavior depends on inventory screen/mods |
| `Right Click` when holding shield | Raise shield/use off-hand (context-dependent) | Does not block all magic, AoE or modded special attacks |
| `Shift` | Sneak / reduce edge risk | Useful for ledges, farming and danger signs |
| `Ctrl` while moving | Sprint in vanilla controls | Can be remapped; sprint can also be toggled or double-tapped |
| `F5` | Cycle third-person and first-person views | Useful for seeing boss positioning and armor appearance |
| `F1` | Toggle interface visibility | Good for screenshots, not for fights |

*Minecraft Java defaults.* MouseTweaks is installed; AO config enables drag/scroll inventory interactions, so the inventory may support additional click-and-drag or scroll movement depending on screen. Those exact actions need a visual example and final GUI conflict test.

## 02. JEI — the built-in encyclopedia

| Key / pattern | Action | Why this is powerful |
|---|---|---|
| Hover + `R` | See recipes that **produce** the hovered item | Answers “how do I get this?” |
| Hover + `U` | See uses/recipes that **consume** that item | Answers “what is this for?” |
| `Ctrl + F` | Focus JEI search (default) | Find items from almost any inventory screen |
| `Ctrl + O` | Show or hide JEI item panel (default) | Clear screen space |
| `@modname` search | Narrow to a particular mod | Example: `@ars` or `@apotheosis` |
| `#word` search | Search tooltip text (when enabled) | Useful for special effects and item descriptions |
| `-word` search | Exclude a search term | Filter very large mod lists |
| `A` over a JEI item | Bookmark a frequently used item (default if enabled) | Saves trips back through long recipe chains |
| JEI `+` button in recipes | Move eligible ingredients into a crafting grid | Requires the real ingredients and compatible screen |
| Recipe navigation arrows / scroll | Navigate alternate recipes | One item can have several sources or machines |

Defaults sourced from the [JEI developer's 1.21.1-compatible mod page](https://modrinth.com/mod/jei) and need an AO GUI regression check. **JEI showing a recipe does not guarantee AO allows it**: KubeJS, datapacks, Paxi and mod configurations can change recipes/loot. Ask the Field Manual about special machines when a recipe shows a non-standard category.

## 03. Maps, exploring, waypoints

| Key or action | Status | What to learn |
|---|---|---|
| `M` full map | **Xaero's World Map default; verify AO** | See explored terrain at a larger scale |
| `B` new waypoint | **Xaero's Minimap default; verify AO** | Create a marker for home, portals and dangerous discoveries |
| `Y` minimap settings | **Xaero's Minimap default; verify AO** | Change waypoint rendering and minimap preferences |
| FTB Chunks map | **AO overrides: deliberately unbound** | Use the supported menu/button if you need claims; don't accidentally open a second competing map |
| World map / dimension switching | **Find in Controls → Xaero; not yet pinned** | Map previews of Nether/End depend on map setup and discovered chunks |
| Waystone menu | **Interact with a Waystone** | Teleport rules, fuel and restrictions depend on configured server |
| Explorer's Journal and return markers | **Future content, no key yet** | Personal discovery progress and visited-location bookmarks |

*Default map keys verified via [Xaero Minimap FAQ](https://blog.curseforge.com/xaeros-minimap-mod-frequently-asked-questions/). Map mods and FTB Chunks may overlap in UI; AO intentionally unbound the FTB Chunks map in its config.* Do not reveal undiscovered structure coordinates as a “tip”.

## 04. Modded combat, backpacks, RPG and voice

This is the **action lookup table**, not a guessed keyboard layout. Fill the final key and tooltip from AO's actual `options.txt` / DefaultOptions export after the modpack's content roster is frozen.

| Mod/system | Important action | Current AO value | How to find/test it |
|---|---|---|---|
| **FTB Ultimine** | Hold mining modifier; cycle area/shape | **Unverified binding** | Options → Controls → Key Binds → FTB Ultimine; AO config enables **hold Ultimine + sneak** for shape menu; holding Ultimine required to cycle |
| **Sophisticated Backpacks** | Open equipped backpack; trigger enabled backpack upgrades | **Unverified** | Controls → Sophisticated Backpacks; check worn versus handheld action and conflicting number keys |
| **Iron's Spells 'n Spellbooks** | Cast spell, next/previous equipped spell, radial spell wheel | **Unverified** | Controls → Iron's Spellbooks; spell wheel **toggle** was introduced unbound by default in 1.21.1 mod version 3.12.1, so do not promise an assigned key |
| **Ars Nouveau** | Cast/spellbook action, open or cycle spell slots and spell shortcuts | **Unverified** | Controls → Ars Nouveau and in-game spellbook help; many effects are context sensitive |
| **Relics / Artifacts** | Trigger active relic or accessory ability | **Depends on item/mod; unverified** | Inspect tooltip and Controls. Many support items trigger passively and have *no keybind* |
| **Origins (future)** | Primary/secondary active Origin ability | **Not configured/installed as approved backend** | Add after Origin selection; ensure no overlap with spell casting or backpack toggle |
| **Questlog (future)** | Open Adventure Journal | **Not installed / final key unverified** | Prefer an easy non-conflicting shortcut or inventory button; engine must be tested |
| **FTB Quests** | Open Field Manual / questbook | **AO final binding unverified** | Provide persistent menu access; distinguish from Questlog journal |
| **Accessories** | Open accessory GUI | **AO distributed suggestion: O** | Confirm `O` survives profile first-launch and Curios/Accessories integration |
| **Simple Voice Chat** | Mute/unmute microphone | **AO distributed suggestion: J** | Confirm works in multiplayer and cannot accidentally mute during combat |
| **Simple Voice Chat** | Push-to-talk / voice GUI / settings | **Unverified** | Controls → Simple Voice Chat; set privacy and preferred activation style |
| **Better Combat / Simply Swords** | Special weapon actions and any alternate attacks | **Weapon/mod specific, verify** | Controls + item tooltip; no universal special-ability key |
| **Cosmetic Armor / transmog** | Toggle vanity appearance UI | **Unverified** | Inspect actual inventory GUI; don't confuse visual layer with stats |
| **Backpack + Curios** | Any UI launch shortcut collision | **Not resolved** | Check `O` against custom backpack, Trinkets/Accessories and Inventory screens |

Developer documentation: [Iron's Spells changelog](https://iron.wiki/changelog/) records a new **unbound-by-default Spell Wheel Toggle** keybinding in 3.12.1. This does not prove its final 3.16.x AO binding.

## 05. Debug and visibility — advanced, optional

| Key | What it does | Use responsibly |
|---|---|---|
| `F3` | Debug screen (coordinates and technical data, permission dependent) | Look up the dimension, biome ID and performance metrics during tests |
| `F3 + G` | Chunk borders | Useful when troubleshooting chunk boundaries and claims |
| `F3 + B` | Entity hitboxes and facing direction | Useful for combat testing; turn off after |
| `F3 + H` | Advanced item tooltips | Useful for durability, IDs and debugging gear |
| `F3 + Q` | List supported debug shortcuts | Version and keyboard dependent |
| `F2` | Screenshot | Share a discovery or reproduce a broken UI (never automatically upload private maps) |

Some laptop keyboards require `Fn` for function keys. Only show debug keys in an **Advanced** subsection, not as initial must-learn controls.

## 06. Keybind conflicts: quick fix

1. Open **Options → Controls → Key Binds** and search for the **action name**, not only the letter. In large modpacks many mods compete for `G`, `R`, `V`, `B`, `Z`, the side mouse buttons and spell wheel controls.
2. Check whether the conflict is active **in the same context**: an inventory-only JEI `R` is not necessarily a collision with world-only gameplay `R`, but overlapping actions can still misfire.
3. Choose an easy-to-remember key for actions you use during combat, then move rarely used menus to distant keys or modifier combinations. Keep familiar Minecraft actions whenever practical.
4. For AO, start by **checking** `O` Accessories, `J` voice mute, Xaero `M`/`B`, and FTB Chunks map unbound—not by guessing the options on an old profile match the packaged defaults.
5. After adding Questlog, new Origins, Traveler's Titles, backpack mods or other expansion content, re-run **all keybind screenshots** and publish the result here.
6. If a key mysteriously does nothing: confirm it is bound, no screen is intercepting it, the item must be equipped if required, you're not sneaking / riding / swimming, and the mod is actually loaded.

## 07. Production checklist for the final published page

- [ ] Capture a successful **freshly imported AO instance** and `options.txt` with all `key_*` lines, plus DefaultOptions startup behavior and any KeybindOverrides one-shot flag; do not treat custom tester settings as universal defaults.
- [ ] Mark every row **AO-confirmed / mod default / unbound / player customizable / future candidate** and resolve real conflicts.
- [ ] Confirm keybinds in inventory, combat, while riding, with spellbooks, with backpack upgrades, and with the accepted Questlog/Origins implementation.
- [ ] Keep a **one-screen quick reference** at the top and fold-out/topic sections underneath in FTB Quests. Prefer item/action icons and very short examples, not a 50-row dense single screen.
- [ ] Offer an optional printable/exportable one-page reference in AO website; do not hardcode unverified shortcuts.
- [ ] Publish a version label and update when changes affect players.

**No server JAR, keybind, mod config or FTB SNBT is changed by this Markdown draft.**
