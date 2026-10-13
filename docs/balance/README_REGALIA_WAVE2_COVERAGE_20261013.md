# Ambient Odyssey — Regalia catalogue expansion, Wave 2
**13 October 2026 · Research only · Minecraft 1.21.1 / NeoForge**

## Status
This expands the **same** Regalia catalogue established by [Wave 1 / PR #47](https://github.com/alsynth/AmbientOdyssey/pull/47). It does **not** invent a separate item-rarity class or change game balance.

**Primary file:** `docs/balance/REGALIA_ITEM_CATALOGUE_EXPANSION_2026-10-13.csv`
**Separate jewelry-pattern support file:** `docs/balance/REGALIA_JEWELRY_PATTERN_POWER_AUDIT_20261013.csv`

### Current coverage
| Source | Rows | Evidence |
|---|---:|---|
| Enigmatic Legacy Plus | 123 | Source `EnigmaticItems`; item names; AO configuration for selected items |
| More Relics | 29 | Official location/evolution list; many 1.7.7 numeric IDs not verified |
| Simply Swords Uniques | 54 | Official Unique documentation index, individual details for nine |
| Native Relics | 28 | Source `ItemRegistry`, exact `relics:*` IDs; original catalogue reconciliation |
| Artifacts | 48 | Source `ModItems`, exact `artifacts:*` IDs; original catalogue reconciliation |
| Reliquified Ars Nouveau | 19 | Source `ItemRegistry`, exact IDs (upstream *current* branch may exceed installed 0.6.1) |
| Reliquified L_Ender's Cataclysm | 9 | Source `RECItems`, exact IDs; installed 0.1.1 still requires comparison |
| Flight Rings | 2 | Exact upstream `flight_rings:basic_ring`, `flight_rings:advanced_ring` and published recipes |
| Alex's Caves | 8 | Selected registered active-tool classes; installed 2.0.3 exact recipe data pending |
| **L_Ender's Cataclysm** | **48** | Matching **MC1.21.1 / mod 3.33** source registry, boss gear and special-effect armor |
| **Mowzie's Mobs** | **24** | Public 1.21 source item registry: masks, powers, boss gear, phase variants |
| **Eternal Starlight** | **27** | Official item wiki, **IDs left blank** pending installed v0.9.1 check |
| **Total** | **419** | **Not 419 newly invented items** |

The original **Relics** and **Artifacts** rows above are **reconciliation records**; deduplicate/merge against the earlier Gear Atlas rather than double-counting. The earlier canonical source file could not be found in current GitHub or accessible Library searches. Until located, **do not overwrite an original catalogue**.

### Important version distinction
The audited **PR #45** physical client profile has 332 installed mod JARs and identifies the exact AO mod versions. Public upstream `main` or `1.21.1` repositories can be **ahead of** the installed version. A registered upstream ID is **source-grounded**, *not* yet proven to exist in installed binary, be player-obtainable, have its anticipated loot source, or perform as current source describes.

In the CSV, an empty `candidate_registry_id` means deliberately **unverified**, not missing data to guess. The previous 54 Simply Swords Uniques and most More Relics items still have unresolved exact ID/version checks. Some EL+ registry entries may be dev/creative-only. Don't claim every 419 item is realistically obtainable.

## Late added source-backed boss gear (after initial Wave 2)
- **Cataclysm:** branch `lender544/new1.20.1@1.21` declares `minecraft_version=1.21.1` and `mod_version=3.33` — **the exact version** in the audited AO profile. The 48 added items are unique boss weapons, special defense/Curios items and armor with distinct abilities, not generic ingots or decorative blocks. Source: [ModItems 1.21](https://github.com/lender544/new1.20.1/blob/1.21/src/main/java/com/github/L_Ender/cataclysm/init/ModItems.java).
- **Mowzie's Mobs:** 24 source-registered masks, phase/ability items, Wroughtnaut/Umvuthi/Frostmaw/Geomancer equipment and specialized boss items. [Mowzie ItemHandler main](https://github.com/BobMowzie/MowziesMobs-Public/blob/main/src/main/java/com/bobmowzie/mowziesmobs/server/item/ItemHandler.java). Not yet matched binary v1.8.2.
- **Eternal Starlight:** 27 *named* exceptional weapons, boss trophies and active-use tools from the [official item wiki](https://github.com/LeoMinecraftModding/eternal-starlight-wiki/tree/main/items/weapons). Source records provide candidate ability and acquisition information, **not authoritative installed item registry IDs**. They have intentionally blank ID cells and are not all known to be present in installed v0.9.1. Some "Regalia" candidates may be reclassified as ordinary special weapons upon power audit.

**Updated structural catalogue tally:** 419 entries, with **320 nonblank candidate IDs** and **99 unresolved IDs**; this count includes 28 Relics and 48 Artifacts *reconciliation entries* and other item-level candidates. Source names/IDs have different confidence levels. No active loot config changes.

## 15 additional Iron's Jewelry patterns — separate from item count
A **second CSV** registers the exact 15 generated patterns from `iron431/irons-jewelry` `1.21.1` source, with full `pattern_id`, bonus type, default-unlock flag, quality multiplier and part material costs.

Examples:
- `irons_jewelry:amulet_of_protection`: `on_take_damage_bonus`
- `irons_jewelry:bane_ring`: `on_attack_bonus`
- `irons_jewelry:tearstone_ring`: `effect_immunity_bonus`
- `irons_jewelry:piglin_signet_ring`: `piglin_neutral_bonus`
- `irons_jewelry:sharpshooter_loop`: `on_projectile_hit_bonus`
- `irons_jewelry:stalwart_ring`: `on_shield_block_bonus`

**These are pattern resource identifiers, not registered item IDs.** They create modular gear and may power up Regalia builds, but should not be counted as 15 separate fixed unique items. Validate exact active source and data-driven patterns in installed `irons_jewelry-1.21.1-2.0.2.jar`.

## Findings worth balancing early
1. **Flight Rings creative flight:** upstream `basic_ring` shaped recipe needs **3 gold ingots + 1 quartz**, while `advanced_ring` requires **3 netherite ingots + 1 nether star**. Source also exposes durability or hunger/XP penalties. If current AO uses the upstream cheap basic recipe without meaningful penalties, it can bypass exploration well before T4. **Check actual AO recipe/config before changes.**
2. **EL+ exceptional combat/mobility**: The Infinitum, Chaos Elytra, Eldritch Amulet, Non-Euclidean Cube and Golem Heart need **effect/math and combination audits**, then acquisition/evolution decisions.
3. **Relics + Reliquified**: inspect levels, passives, skill triggers, proc chance and multiple-equipped-item handling; Reliquified Cataclysm boss items must not duplicate existing Cataclysm signature rewards by accident.
4. **Artifacts utility and defense**: Cross Necklace, Scarf of Invisibility, Cloud in a Bottle, Crystal Heart, Warp Drive, Vampiric Glove and retaliation items create power through utility/stacking, not ordinary item damage.
5. **Simply Swords**: keep surprise Unique finds possible; balance Runic Tablet / awakening unlock and max-effect interactions rather than blanket-restricting vanilla chests.
6. **Iron's Jewelry**: high-grade materials and scroll-locked patterns can create substantial passive power. Evaluate **pattern availability, material quality and hidden bonus stacking**, not 10,000 individual rolls.
7. **Upgrade resources and gems**: keep in the later economy ledger as *paths to power*, not Regalia themselves. The five gem grades from the custom Apotheotic port aren't 5 new unique items in this catalogue.

## Source references
- [Relics ItemRegistry 1.21.0](https://github.com/Octo-Studios/relics/blob/1.21.0/src/main/java/it/hurts/sskirillss/relics/init/ItemRegistry.java)
- [Artifacts ModItems 1.21.1](https://github.com/ochotonida/artifacts/blob/1.21.1/common/src/main/java/artifacts/registry/ModItems.java)
- [Reliquified Ars Nouveau ItemRegistry 1.21.1](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/1.21.1/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/init/ItemRegistry.java)
- [Reliquified Cataclysm RECItems 1.21.1](https://github.com/Octo-Studios/reliquified-lenders-cataclysm/blob/1.21.1/src/main/java/it/hurts/octostudios/reliquified_lenders_cataclysm/init/RECItems.java)
- [Flight Rings ModItems](https://github.com/tired9494/flight-rings/blob/1.21.1-architectury/common/src/main/java/tired9494/flight_rings/registry/ModItems.java)
- [Alex's Caves item source](https://github.com/AlexModGuy/AlexsCaves/blob/main/src/main/java/com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.java)
- [Iron's Jewelry source pattern folder](https://github.com/iron431/irons-jewelry/tree/1.21.1/src/generated/resources/data/irons_jewelry/irons_jewelry/pattern)
- Previous [Regalia Wave 1](README_REGALIA_CATALOGUE_EXPANSION_20261013.md)

## Remaining catalogue areas (not silently treated as complete)
- **Cataclysm 3.33**: 48 source IDs now mapped from its actual `1.21` branch declaring Minecraft 1.21.1 and Cataclysm 3.33. Actual loot/recipe/ability runtime and complete coverage still need validation.
- **Mowzie's Mobs 1.8.2**: 24 source-registered signature entries now mapped; exact JAR/loot/effect verification still needed. **Ice and Fire 2.1.3**, **Aquamirae**, **Eternal Starlight**, **Twilight Forest**, **Iron's Spellbooks 3.16.3**, **Goety**, **Pasterdream**, and other world/boss mods with unusual equipped items — audit installed JAR item registry and actual special powers, not every ordinary armor set or material.
- **Eternal Starlight** 27 wiki candidates are unresolved at item-ID level and are not proven in the v0.9.1 native registry.\n- **More Relics 1.7.7** and **Simply Swords 1.70.2**: finish exact binary registry ID/effect version matching; distinguish dev-only items and prerequisites.
- **Other modular accessories**: Craft tiered power interactions without enumerating each run-of-the-mill gear component.
- Reconcile original Gear Atlas with 28 native Relics + 48 Artifacts. Record original A/B combat-support grades and current IDs, don't duplicate.
- Verify whether any enhanced unique rewards in the installed 332 JARs are **quest-only**, **boss-only**, **loot-only**, **craft-only**, **trader-only** or **unobtainable**.

## Data quality and implementation
This branch only adds research CSV/Markdown. Do not change loot, recipes, Curios slots, bosses, gems or client/server config. A balance recommendation in a CSV is **not approval**. Use Work/Claude to confirm the *exact installed JAR and effective datapacks* before engineering.

**Recommended next batch:** locate original Regalia file; scan all installed item registries and recipe/loot tags; mark which of 419 are truly obtainable; audit boss-signature sources; then create source-backed item-by-item acquisition changes. This is discovery, not a finished loot economy.
