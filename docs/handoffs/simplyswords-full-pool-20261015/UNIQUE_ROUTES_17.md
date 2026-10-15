# How the 17 non-lootable Simply Swords uniques are obtained (15 October 2026)

**Result:** none of the 17 has a recipe or loot table. All are progression forms. Six are **legacy IDs** that the mod converts, in a player's slots, back into the base weapon with its awakening level preset. Dropping any of the 17 directly from a boss **skips the mod's own progression**. All 17 are in the current 133-ID pool (`2067e4a`); nothing was changed or excluded.

**Owner decision (15 Oct, supersedes the options below):** keep all 17. Don't exclude any for being a legacy ID. Don't add them to Grand pools or boss-drop tables. Boss assignment and R5 vs R6 placement are still open. Audit: [UNIQUE_17_ALIAS_AUDIT.md](UNIQUE_17_ALIAS_AUDIT.md).

**Status:** static only (JAR data + `javap` bytecode constants). Not engine-tested. Levels and routes are read from bytecode constants, not observed in game.

## Source
- JAR: `simplyswords-neoforge-1.70.2-1.21.1.jar` (R4 pin, same as `SIMPLYSWORDS_FULL_POOL.md`).
- Classes read: `api/AwakeningFormRegistry`, `util/LegacyUniqueMigration`, `mixin/ServerPlayerEntityMixin`, `item/custom/DormantRelicSwordItem`, `util/ModLootTableModifiers`, `api/AwakeningApi`.
- Data read: the 17 advancements, `en_us.json`, tags `lootable_uniques` and `conditional_uniques_type_2`, recipes `runic_forge`, `contained_remnant`, `unique_melting`.
- AO config (R4 source): `loot.toml` `enableContainedRemnants = true`, `disabledUniqueWeaponLoot = []`; `general.toml` `enableUniqueWeaponAwakening = true`.

## How progression works
- Base uniques drop from chests (`#simplyswords:lootable_uniques`).
- They gain **awakening** levels, then change form at a **Runic Forge** (craftable: smithing table + Runic Tablet + gold, obsidian, amethyst).
- A **route** component picks the branch (for example sun or harbinger for the Dormant Relic).
- A second chain runs through remnants: any unique smelts into an **Empowered Remnant**; three of those craft a **Contained Remnant**; that changes form while carried.

## The 17

| # | ID | Route (base → form) | Base lootable? | Legacy ID converted on pickup? | Risk if AO drops it directly |
|---|---|---|---|---|---|
| 1 | `waking_lichblade` | Slumbering Lichblade, awakening 4, lichblade route | yes | **yes** → slumbering_lichblade at awakening 4 | skips 4 levels |
| 2 | `awakened_lichblade` | Slumbering Lichblade, awakening 8 (LEGENDARY) | yes | **yes** → slumbering_lichblade at awakening 8 | skips the whole lichblade chain |
| 3 | `righteous_relic` | Dormant Relic, awakening 4, sun route | yes | **yes** → dormant_relic, awakening 4, route 1 | skips 4 levels |
| 4 | `tainted_relic` | Dormant Relic, awakening 4, harbinger route | yes | **yes** → dormant_relic, awakening 4, route 2 | skips 4 levels |
| 5 | `sunfire` | Dormant Relic, awakening 8, sun route (LEGENDARY) | yes | **yes** → dormant_relic, awakening 8, route 1 | skips the whole relic chain |
| 6 | `harbinger` | Dormant Relic, awakening 8, harbinger route (LEGENDARY) | yes | **yes** → dormant_relic, awakening 8, route 2 | skips the whole relic chain |
| 7 | `ionbound_stormscale` | Stormscale → awakened stormscale → ionbound route (LEGENDARY) | yes (stormscale) | no, separate item | end-of-route item |
| 8 | `the_devourer` | Watcher Claymore → awakened → devourer route (LEGENDARY) | yes (watcher_claymore) | no | end-of-route item |
| 9 | `wraithmaw` | Wraithfang → spectral wraithfang → wraithmaw route (LEGENDARY) | yes (wraithfang) | no | end-of-route item |
| 10 | `gloampiercer` | Wickpiercer → spectral wickpiercer → gloampiercer route (LEGENDARY) | yes (wickpiercer) | no | end-of-route item |
| 11 | `soulstalker` | Soulrender → spectral soulrender → soulstalker route (LEGENDARY) | yes (soulrender) | no | end-of-route item |
| 12 | `dreadwhisper` | Whisperwind → spectral whisperwind → dreadwhisper route (LEGENDARY) | yes (whisperwind) | no | end-of-route item |
| 13 | `decaying_relic` | Contained Remnant, carried (lang hint: with a Runic Tablet in the End) → Tampered Remnant → Decaying Relic; order inferred from mixin constants + lang, not observed | no (remnant chain) | no | skips the remnant chain |
| 14 | `magiblade` | Decaying Relic, carried; reacts to a specific block underfoot | no | no | skips remnant + relic chain |
| 15 | `magiscythe` | Decaying Relic, carried; triggered when hit (code checks `sonic_boom` damage, i.e. a Warden) | no | no | skips remnant + relic chain |
| 16 | `magispear` | Decaying Relic, carried; reacts to darkness | no | no | skips remnant + relic chain |
| 17 | `enigma` | Ribboncleaver, carried; changes form under a condition in the player tick (advancement "Weather Controller"; exact condition not decoded) | yes (ribboncleaver) | no | skips one transformation |

Notes:
- The levels in rows 1–6 come from `LegacyUniqueMigration.convertStack` and match the advancements (for example `harbinger` requires dormant_relic with awakening 8 and relic_attunement 2).
- In `AwakeningFormRegistry`, the stormscale and watcher families have an awakening-4 stage. The four spectral families register their stages with level constant 0, so their exact unlock gate isn't proven statically.
- The in-game hints for rows 13–17 come from the mod's own lang text, for example "Try keeping this in your inventory while exploring the deepest, darkest depths of the Overworld."

## Options (superseded)
The earlier options and the recommendation to drop the 6 legacy IDs are **withdrawn**. The owner keeps all 17. Nothing had been applied.

## Not tested
- Whether `convertStack` also runs on items delivered by AO's boss-reward code (it runs on player slots, so delivery to the inventory should trigger it).
- Every in-game trigger in rows 13–17.
