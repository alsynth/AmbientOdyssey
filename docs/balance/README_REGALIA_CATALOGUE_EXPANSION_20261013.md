# Ambient Odyssey — Regalia item catalogue expansion (13 October 2026)
**Research catalogue only · no loot, item stats, recipes, mods or quest files modified**

## Why this belongs under Regalia
Use **Regalia** as the AO Gear Atlas umbrella for *distinctive ability-bearing items* — Relics, Artifacts, cursed/enchanted uniques, spellstones, special accessories, and signature Unique weapons. A source mod label such as **Relics** or **Artifacts** is not the Regalia category itself. Regalia is **not** a new rarity tier, nor the Apotheosis gem ladder (`Perfect → Ancient → Artifact → Heirloom → Esoteric`). "Artifact" as a gem grade and "Artifacts" as a mod are unrelated terminology.

**Do not replace or duplicate existing Regalia items from Relics/Artifacts.** Treat `REGALIA_ITEM_CATALOGUE_EXPANSION_2026-10-13.csv` as an **item-level expansion overlay**. Merge into the canonical Gear Atlas by normalized `source_mod + registry_id`; if ID is unverified, hold by `source_mod + display_name` until installed-JAR registry scan.

The previously discussed Gear Atlas references **two grade-A combat-support items as the T2 combat-readiness benchmark** and distinguishes passive/activatable powers, slots, scaling and interactions. The exact earlier item-by-item *Regalia* source was not located in the accessible GitHub/Library searches, so this document does not claim it has overwritten the original catalogue.

## Sources and audited roster
At PR #45's **v0.4.9 Client Performance TEST**, physical JAR audit includes:
- `enigmaticlegacyplus-1.21.1-1.1.2.jar`
- `morerelics-1.7.7-1.21.1.jar`
- `relics-1.21.1-0.10.7.8.jar`
- `artifacts-neoforge-13.2.5.jar`
- `simplyswords-neoforge-1.70.2-1.21.1.jar`
- `reliquified_lenders_cataclysm-1.21.1-0.1.1.jar`, `reliquified_ars_nouveau-1.21.1-0.6.1.jar`, `irons_jewelry-1.21.1-2.0.2.jar`, `FlightRings-neoforge-2.0.0.jar` — *follow-up providers requiring exact individual item ID/effect audit*.

The **206 candidate rows** are:
- **123 Enigmatic Legacy Plus**: exact IDs + class links from [upstream `EnigmaticItems`](https://github.com/Auviotre/Enigmatic-Legacy-Plus/blob/main/src/main/java/auviotre/enigmatic/legacy/registries/EnigmaticItems.java) and [English item names](https://github.com/Auviotre/Enigmatic-Legacy-Plus/blob/main/src/main/resources/assets/enigmaticlegacyplus/lang/en_us.json), excluding identified commodity materials and the basic Etherium armor/tool family. Some items may be uncraftable/creative-only or changed in installed v1.1.2. Item behavior/source details especially depend on installed version.
- **29 More Relics**: named items, acquisition biome/chest families and evolution chains from the [official 1.21.1 location list](https://www.curseforge.com/minecraft/mc-mods/more-relics). Exact item namespace ID is **intentionally blank** for 27 entries until installed v1.7.7 JAR verification; two IDs appear in AO config examples.
- **54 Simply Swords Unique weapons**: [official 1.21 item index](https://github.com/Sweenus/SimplySwords/blob/Architectury-1.21/docs/unique-weapons/_meta.json), per-weapon direct docs links; 9 highest-priority entries have parsed combat/ability details from actual individual pages. IDs remain blank where per-weapon docs were not read; do not infer them from filenames. Installed v1.70.2 still needs registry validation.

Every row contains source JAR, candidate exact ID (where proven), subfamily, effect/evidence, acquisition, evolution, slot, *two distinct provisional power/access concepts*, risk category, balance action, source/class URL and verification priority/status.

## Important philosophical correction from user
Ordinary discovered equipment does **not** define the final power ceiling. A basic armor piece or sword can become strong by **enchanting, Apotheosis affixes, gems, reforging and combinations**.

Therefore:
1. **Do not aggressively nerf ordinary chest equipment** by Tier.
2. **Do balance unique Regalia acquisition, their persistent abilities, evolution/leveling and interactions**, plus upgrade materials and powerful gems.
3. A strong early-found **Simply Swords** Unique can be acceptable if it appears unawakened: official docs say natural loot begins at Awakening 0 and later unlocks abilities using **Runic Tablets / Runic Forge**. Balance *tablet availability, forge costs and activations* before removing exciting finds. The installed source `config/simplyswords/loot.toml` has unique weighting and per-player pity settings, including soft-pity start 25 and hard-pity 75; check exact gameplay semantics before rewriting.
4. **More Relics** has evolved forms: Slumbering → Whispering → Made in Heaven, Tyrant Mask → King Crimson, Depleted Spool → Weavers Spool, Converging Orb → Wonder of U. Preserve those journeys instead of assigning all forms to the same tier.
5. **Enigmatic Legacy Plus** has parallel **normal / curse / bless / abyss** routes. The Ring of Seven Curses must remain optional. Do not balance *every* unusual item by assuming cursed progression is mandatory.
6. **Relics/More Relics** advanced configuration is disabled in AO `relics.yaml`. The installed `morerelics-common.toml` warns advanced stat-file generation can break when the mod updates. Prefer loot/recipes/progression design first.

## First high-impact Regalia reviews
| Item | Mod | Source-grounded reason for priority | Initial proposed action |
|---|---|---|---|
| The Infinitum | EL+ | Installed server config has special-damage boost 200 and lifesteal 10 | Inspect actual percent/unit semantics and Abyss acquisition before balancing |
| Testament of Contempt / Eldritch Amulet | EL+ | Damage 20, lifesteal 15 and `keepInventory=true` setting | Survival/dupe and cross-item stacking audit |
| Arrogance of Chaos / Chaos Elytra | EL+ | Config shows resistance 80 and flight enhancements | Balance upgrade/flight access; avoid accidental invulnerability |
| Non-Euclidean Cube | EL+ | Combined-spellstone route and `damageLimit=100`, `autoTrigger=true` | Verify stacking / defensive mechanics |
| Heart of the Golem | EL+ | Armor/armor-toughness bonuses and protection config | Armor cap + status mitigation review |
| Lost Engine | EL+ | Crit multiplier and vulnerability tradeoff | Crit + Apotheosis affix combination audit |
| Hell Blade Charm | EL+ | Very large attack/armor-debuff config values | Confirm exact formula and actual attack effect |
| Ring of Seven Curses | EL+ | Opt-in curse equipment path | Preserve separate blessed/noncursed routes |
| Mass Gauntlet | More Relics | Default cap near double max and non-melee effect enabled | Inspect true effect and source; trial restrictions only if exploitable |
| King Crimson / Made in Heaven | More Relics | Evolved from other Regalia and not normal chest loot | Preserve evolved-only progression |
| Mjolnir / Storm's Edge / Caelestis | Simply Swords | Powerful lightning/dash/summon effects in official Unique docs | Let items appear early unawakened; tune higher-level activation cost |
| Other Relics + Artifacts already catalogued | Original Regalia | Existing support-item grades were designed previously | Merge existing rows rather than resetting them |

A value from a TOML file is **not** automatically a percentage or effective combat multiplier. Treat the exact field as source evidence and validate source math.

## Five acquisition/economy tags per item (future full integration)
- **First obtain:** source rarity, dimension/location, craft chain, trades and boss exclusivity
- **Persistent effect:** passive/active, cooldown, equipment/Curios slot, damage type, immortality/flight/utility
- **Scaling:** XP/level/evolution, materials, sacrifice/crafting, hidden damage caps, multiplayer interaction
- **Synergy:** ring stacking, multiple equipped copies, Apex Apotheosis affixes/gems, Iron's spells / Ars / Origins
- **Reward role:** first-clear boss unique, rare exploration item, repeatable resource sink, noncombat utility, prestigious endgame form

Avoid assigning a permanent tier solely by rarity text; use **earliest fair acquisition tier** and **full-power tier** separately.

## Next technical pass, delegated only when engineering is available
1. Scan actual installed `enigmaticlegacyplus-1.21.1-1.1.2.jar` item registry + recipes/loot and resolve what is obtainable/creative-only. Compare against the official upstream main source.
2. Extract exact `morerelics-1.7.7` registry IDs, descriptions, slots, passive/active effects and evolution conditions; verify published 1.21.1 loot locations against actual v1.7.7 source.
3. Extract `simplyswords-1.70.2` registered Unique IDs/effects, upgrade resource quantities, pity/drop rates, and official doc alignment; do not interpret `uniqueLootTableWeight` as an item type's final chance without source math.
4. Extend the **same Regalia catalogue** with Reliquified L_Ender, Reliquified Ars Nouveau, Iron's Jewelry truly singular items, Flight Rings and boss-specific relics **only with exact current installed IDs**. Modular jewelry's thousands of combinations are not 10,000 separate Regalia entries; catalog meaningful patterns/exceptional effects instead.
5. Compare with existing Relics / Artifacts items (original Gear Atlas) and dedupe by ID/name/version.
6. Assess power vs Tier2 enchanted-diamond + two Grade-A support items, then measure T4/T6/T8 representative builds and update source/acquisition power bands.
7. Only after a factual audit propose **item-specific** loot and craft balancing (e.g. acquisition, upgrade mat scarcity, mutually exclusive Curios stacks), never blanket-nerf every Relic.

### Status
**DESIGN/SOURCE INDEX ONLY.** No executable loot/reward item changes, boss balance, installed mod changes or actual Minecraft validation. The expansion deliberately leaves uncertain IDs blank instead of fabricating them.
