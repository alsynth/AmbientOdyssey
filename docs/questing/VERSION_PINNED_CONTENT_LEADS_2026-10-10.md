# Version-pinned Quest Content Leads — NeoPasterDream 0.9.6 / Enigmatic Legacy Plus 1.1.2

**Date:** 10 Oct 2026. **Purpose:** high-value quest beats that often get missed when a mod looks minor. **Status:** published release-note evidence, not runtime / actual JAR registry verification. All named items and systems require real ID/recipe/entry-condition checks before Questlog JSON.

## NeoPasterDream 0.9.6 — much more than a new dimension

**Exact historical AO source JAR:** `pasterdream-0.9.6.jar`. [Upstream version-specific 0.9.6 release notes](https://modrinth.com/mod/neopasterdream/version/0.9.6) offer enough evidence to separate actual early features from the evolving [current project overview](https://modrinth.com/mod/neopasterdream), which advertises four dream realms and fourteen biomes but warns the mod is still in development. Do **not** assume every advertised realm or late chapter is accessible in 0.9.6.

### Specific thematic quest tracks

| Track | Documented version evidence | Proposed original AO journal milestone | Gate |
|---|---|---|---|
| **Opening a Dream** | Dyedream cracks are worldgen features, explicitly configurable/toggleable; origin crack at (0,0) configurable | Discover a naturally generated crack and record your first view of Dyedream | Inspect AO config for crack generation; never require if disabled |
| **Paster's Guide** | Patchouli guidebook exists, 0.9.6 fixes recurring distribution on player death | Read the guidebook before accepting the first dangerous dream challenge | Check ID and acquisition, avoid false required auto-give |
| **Dyedream's Canopies** | Twelve tree variants imported, including giant conifer, aspen, palm, blossom and others | Document one unusual tree type; later optional environmental collection of several shapes | Discovery may need manual/advancement; no auto-detect of arbitrary trees |
| **The Cultivated Dream** | Dyedream Farmland has hydration, proper trampling, **2× crop growth** in 0.9.6 | Try growing food on the dream soil; optional return-home farming trick | Verify survival availability; life-skill cameo, not major quest |
| **Lights in the Pink Mist** | Dyedream Lantern v0.9.6 new block, light level 15 | Craft or find a dream lantern; bring reliable light to an expedition | Exact recipe/ID required |
| **The Garden Decryption** | Ported flower puzzle: correct arrangement around a Dyedream Desk and interaction with Flower 11 to unlock Flower 12 | Solve the flower arrangement puzzle without giving the answer in quest title | Exact block/detection check; may need advancement or custom trigger |
| **The Snow Golem and Allay** | Ported puzzle places a Snow Golem and Allay within range of flower formation to transform Flower 16 to 17, involving sacrifice | Optional puzzle for experienced Dreamseekers with explicit warning | Ethical/pacing choice: do not require for mainline; check reliable completion |
| **A Bloom that Freezes** | Flower 17 freezes nearby water / accumulates snow | Observe the resulting Frozen Flower effect | Need verification whether detectable by item obtain, block interact, advancement |
| **An Unfamiliar Forge** | Project page advertises multi-station weapon workshop: anvil, forge, basin, grindstone; version-specific 0.9.6 feature presence unconfirmed | Investigate workshop and create a native weapon | Verify multiblocks, GUIs, recipe input/output, exact 0.9.6 presence |
| **Dream Energy** | Project page advertises energy resource for staves/rings; exact 0.9.6 function unverified | Learn that spell energy is a separate resource | FTB reference and UI test, do not demand arbitrary recharge count |
| **Accessories of Sleep** | Project page advertises numerous Curios accessories; AO user previously disliked its custom inventory GUI | Pick an equipment piece that works in AO's Curios/Accessories slot layout | Respect chosen GUI and custom slot compatibility, no forced screenshots |
| **Cold Domain Arrival** | **New frozen dimension in 0.9.6** with own biomes, trees, snow ground, sky and fog | Enter the Cold Domain and record a frost-region discovery | Portal/accessibility and actual dimension ID must be verified |
| **The Cold Domain's Ecology** | New Cold Domain logs/leaves/dirt and snow-themed grass, stripping | Recover natural Cold Domain material, document its unique environment | Low stakes, optional. Confirm blocks obtainable with correct tool |
| **The Twin Hands** | **Aaroncos** initial boss 0.9.5, extensively revised 0.9.6: melee Left Hand and ranged Right Hand, each 7 skills in 0.9.5 | Prepare for a two-opponent fight requiring different responses to melee and ranged pressure | Actual summoning ritual/arena, tier, spawn and kill attribution unknown |
| **Shadow Tune Totem** | Listed as boss ultimate in 0.9.5; 0.9.6 danger/mechanics reworked | Optional lore/hazard dossier before Aaroncos encounter | Don't claim exact telegraphs or damage values without runtime |
| **Recovering from the Dream** | 0.9.6 overhauled crashes, worldgen, shaders, and guidebook persistence | Optional expedition recap: bring back a distinct dream item | No forced boss defeat to exit realm |
| **Talent Choice** | Main project page advertises Light vs Shadow irreversible choice; no confirmation from 0.9.6 changelog | A *locked optional* choice chapter, only if implemented in installed build | Explain permanence, do not auto-select, do not gate progression |
| **Dreamseeker's Notes / Kael Cards** | Current overview advertises 0–14 notes and 0–9 cards; version-specific counts/accessibility unknown | Recover a single authentic collectible, then introduce optional collecting | Do not require collecting all if missing/unobtainable |

### Editorial guidance
- A convincing **first 15–25 quest arc** could be built from *entry, book, environment, a puzzle, workshop, first specialized combat, Cold Domain exploration, Aaroncos* once verified.
- Avoid a long mandatory sequence of *all twelve trees* or *all cards*: reserve collections for optional completionism.
- **Question for the 0.9.6 binary audit:** which named realms/dimensions are registered vs accessible; which puzzles have advancements; which bosses spawn naturally vs through commands/summons; which worldgen toggle AO has set; and whether original custom GUI/Curios slots conflict with our current inventory.
- Source shows version mechanics clearly, but actual in-game achievement hooks/IDs remain unverified. Don't accidentally mix in future 0.10 preview content.

## Enigmatic Legacy Plus 1.1.2 — independent standard and cursed paths

**Historical AO source JAR:** `enigmaticlegacyplus-1.21.1-1.1.2.jar`. [Official 1.1.2 release notes](https://www.curseforge.com/minecraft/mc-mods/enigmatic-legacy-plus/files/9066975) list considerable new equipment, new advancements and specific behavioral updates, reinforcing that this is more than one ring gimmick. Some item access is conditioned on cursed state: **do not assign route ownership without validating real recipes and checks**.

### Concrete 1.1.2 content hooks

| Item/system mentioned by upstream | Proposed original Questlog content | Likely educational FTB topic | Pending verification |
|---|---|---|---|
| **Decision of Annihilation** | Uncover a relic whose purpose deserves careful preparation | Combat conditions, obtaining/upgrade restrictions | Exact item ID, acquisition, cursed availability |
| **Proof of Dimness** | Investigate a mysterious proof and the benefit it can provide | Trigger and slot | Exact item source and any required quest milestone |
| **Flawless Forging Gem** | Learn which forging choices are truly worth perfecting | Forge/crafting and stat cap reference | Recipe, stacking and irreversible use |
| **Amulet of Radiance** | Assemble a survivable relic setup that uses light-related mechanics | Curios amulet slot conflicts | Actual slot and buff |
| **Pseudo-Sacred Chalice** | Examine an unconventional survival artifact | Consumable/passive and recovery rules | Trigger and curse flag |
| **Resonator of Spell** | Explore an item that may interact with spellcasting | Iron's and Ars compatibility audit | Does it actually affect either system? Not inferred from its name |
| **Potion of Purification** | Obtain and investigate a new potion with unusual implications | Potion/brewing and status mechanics | **Do not claim it reverses Seven Curses** without source verification |
| **Starlight Ingot** | Acquire a rare forging material for higher-tier equipment | Material progression and JEI alternatives | Actual dimension/resource source; do not link to Eternal Starlight by name alone |
| **Charming Insignia** | Evaluate a subtle accessory for a specialist build | Curios equip requirement | Exact passive and source |
| **Tome of Void** | Discover an expanded Void tome ability | Ability description, costs and activation | Changed in 1.1.2; verify actual implementation |
| **Antique Book Bag** | Examine multiple books and compare their described buffs | Buff book descriptions | Confirm how effects stack; no mandatory full collection |
| **The Architect's Favor** | Use an artifact geared toward creative building or placement | Configuration and balance | Release notes say effects adjusted; identify actual ones |
| **Purified Ichor Spirit** | Face or study a source of advanced Ichor | Combat or companion logic | AI was improved; exact encounter/loot unclear |
| **Hearts of the Abyss** | Discover how advanced abyssal resources appear in multiplayer | Multiplayer loot fairness | 1.1.2 improved acquisition; validate source and per-player handling |
| **Enigmatic advancements** | Use verified native advancements as objective bridges, including curse-state milestones if any | Advancement screen vs Questlog | Inspect shipped advancements; no invented predicates |

### Route separation (non-negotiable)

- **The Relic Scholar**: non-cursed route with accessible equipment, recipe research and artifact mastery. Startable and finishable without accepting the curse.
- **The Seven Curses**: opt-in after a clear warning, with a *reliable actual curse-state detector* before advanced objectives become available. The quest itself must never equip the ring or trigger a permanent curse.
- **Shared neutral field manual**: explains artifacts, slots, iconography, and risks, *without spoiling the results of cursed-only mechanics* unless player opts in.
- No advancement/unlock that secretly demands finishing both branches; two friends can take different routes and maintain separate saves.
- Confirm whether multiplayer mechanics create a different reward route from singleplayer; the upstream specifically changed acquisition of Hearts of the Abyss.

### Practical next source inspection
Read `data/**/advancements`, item registries, recipe conditions, loot tables, Curios/Accessories tag assignment, achievement triggers and config curse flags from the **exact** 0.9.6/1.1.2 binaries in the final AO build. Only after that promote these leads into implemented Questlog `item_obtain`, `advancement`, `entity_kill` or external-custom objectives. No current JAR inspection or runtime verification is claimed.

## Source references
- [NeoPasterDream 0.9.6 notes](https://modrinth.com/mod/neopasterdream/version/0.9.6)
- [NeoPasterDream evolving overview](https://modrinth.com/mod/neopasterdream)
- [Enigmatic Legacy Plus 1.1.2 official release](https://www.curseforge.com/minecraft/mc-mods/enigmatic-legacy-plus/files/9066975)

**End state:** quest-content research only. No JSON quest definitions or modpack source changes.
