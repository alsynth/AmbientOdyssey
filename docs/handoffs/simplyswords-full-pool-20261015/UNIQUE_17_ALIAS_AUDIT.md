# The 17 non-lootable uniques: alias, duplicate and compatibility audit (15 October 2026)

**Owner decision:** keep all 17. Don't exclude any for being an old ID. Don't add them to Grand pools or boss-drop tables. Boss assignment and R5 vs R6 placement are unresolved and not chosen here.

**Status:** Approved: keep all 17. Implemented: no change (the pool still has all 17). Statically verified: yes (installed JAR `simplyswords-neoforge-1.70.2-1.21.1.jar`, the R4 pin; data plus `javap`). In-game tested: no. Multiplayer tested: no.

## Terms
- **Obsolete alias:** the item is still registered, but the mod converts any stack of it in a player's inventory into another item (`LegacyUniqueMigration.convertStack`, called from `UniqueWeaponItem` while the item sits in a player inventory).
- **Duplicate:** after conversion it becomes an item that's already in the pool.
- **Incompatible:** not registered in the installed version, or missing its data. The R4 engine fixture registered 57 of the 58 old uniques; the only missing one was `dreadtide` (not among these 17). All 17 have registry fields, item tags and weapon-attribute files in the JAR.

## Results

| ID | Registered (installed) | Obsolete alias? | Converts to | Duplicate? | Incompatible? |
|---|---|---|---|---|---|
| `waking_lichblade` | yes | **yes** | `slumbering_lichblade`, awakening 4, lichblade route | **yes**, of `slumbering_lichblade` | no |
| `awakened_lichblade` | yes | **yes** | `slumbering_lichblade`, awakening 8 | **yes** | no |
| `righteous_relic` | yes | **yes** | `dormant_relic`, awakening 4, attunement 1 (sun) | **yes**, of `dormant_relic` | no |
| `tainted_relic` | yes | **yes** | `dormant_relic`, awakening 4, attunement 2 (harbinger) | **yes** | no |
| `sunfire` | yes | **yes** | `dormant_relic`, awakening 8, attunement 1 | **yes** | no |
| `harbinger` | yes | **yes** | `dormant_relic`, awakening 8, attunement 2 | **yes** | no |
| `ionbound_stormscale` | yes | no | — | no (its own item, end of route) | no |
| `the_devourer` | yes | no | — | no | no |
| `wraithmaw` | yes | no | — | no | no |
| `gloampiercer` | yes | no | — | no | no |
| `soulstalker` | yes | no | — | no | no |
| `dreadwhisper` | yes | no | — | no | no |
| `decaying_relic` | yes | no | — | no | no |
| `magiblade` | yes | no | — | no | no |
| `magiscythe` | yes | no | — | no | no |
| `magispear` | yes | no | — | no | no |
| `enigma` | yes | no | — | no | no |

Totals: **6 obsolete aliases**, all of which duplicate a pool base item. **0 incompatible.**

## ID migration conflicts (for AO)
1. **What the player ends up holding:** an AO boss reward of an alias ID turns into the base item once it's in the inventory. Delivery itself isn't affected.
2. **Components carry over:** conversion uses `ItemStack.transmuteCopy`, so data components such as Apotheosis affixes survive (static reading; not engine-tested).
3. **Uneven odds:** with a uniform roll over 133 IDs, `slumbering_lichblade` effectively has 3 chances (itself + 2 aliases) and `dormant_relic` 5 (itself + 4). They come out pre-awakened, so they skip upgrade steps.
4. **Records:** AO reward logs and tests record the alias ID, not the item the player keeps. Any later "already owned" or duplicate check that uses IDs would be wrong for these 6.
5. **Registry checks still pass:** `swordPoolIds()` filters by registry + sword tag, and all 6 aliases are registered and tagged.

## Open point for you
These 17 were already in R4's boss unique roll: all 17 are in the shipped R4 campaign `ao_loot_policy.json` `unique_weapons` (58 entries; verified from the restored R4 ZIP). `2067e4a` keeps them in the full boss sword pool. Your instruction "do not add them to boss-drop tables" might mean that existing inclusion is fine, or that they should come out of the boss roll. **I haven't changed anything.** Please say which.
