# Ambient Odyssey — R3 Grand Treasure mapped-source review
**15 Oct 2026 · Draft mapping audit, not gameplay approval or tested effective resources**

## Findings from committed R2 candidate list
The current R2 policy includes **14** T3+ Grand Treasure contexts at the approved **5% per eligible chest** rate. Of these, **6** draw from a pool in the triggering chest's own table; **8** draw from a different loot table. The latter is not automatically wrong: the owner chose the structure's best existing native loot pool, even when that is elsewhere within the same structure. But the **specific chosen pools were scored heuristically, not confirmed as the best native source by the owner or a live loot audit**.

The issue is not that a bonus uses a different native chest table. The issue is **verification** that that source really belongs to this structure, is an appropriate best pool, and preserves native treasure behavior. Do not silently replace any of these with homemade generic rewards.

## All 14 current contexts

| # | Structure | Triggering chest table path | Selected native source path + pool | Review |
|---:|---|---|---|---|
| 1 | `adventuredungeons:murkydungeon` | `chests/murkydungeon/murky_chest_reward` | `chests/murkydungeon/murky_chest_reward` #0 | Self-table |
| 2 | `dungeons_arise:illager_fort` | `chests/illager_fort/illager_fort_normal` | `chests/illager_fort/illager_fort_normal` #2 | Self-table |
| 3 | `dungeons_arise:infested_temple` | `chests/infested_temple/infested_temple_room_normal` | `chests/infested_temple/infested_temple_room_normal` #3 | Self-table |
| 4 | `dungeons_arise:infested_temple` | `chests/infested_temple/infested_temple_room_supply` | `chests/infested_temple/infested_temple_room_normal` #3 | Cross-table: review |
| 5 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_garden_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Self-table |
| 6 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_library_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 7 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_library_treasure` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 8 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_normal` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 9 | `dungeons_arise:keep_kayra` | `chests/keep_kayra/keep_kayra_treasure` | `chests/keep_kayra/keep_kayra_garden_normal` #1 | Cross-table: review |
| 10 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_rooms` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Cross-table: review |
| 11 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_top_rooms` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Cross-table: review |
| 12 | `dungeons_arise:thornborn_towers` | `chests/thornborn_towers/thornborn_towers_top_treasure` | `chests/thornborn_towers/thornborn_towers_top_treasure` #4 | Self-table |
| 13 | `irons_spellbooks:catacombs` | `chests/catacombs/hidden_trough_treasure` | `chests/catacombs/hidden_trough_treasure` #3 | Self-table |
| 14 | `irons_spellbooks:catacombs` | `chests/generic_magic_treasure` | `chests/catacombs/hidden_trough_treasure` #3 | Cross-table: review |

**Note:** This table is generated from `docs/handoffs/loot-update-20261015/grand-treasure-candidates.json`; per-source original expected SHA256 values reside in that JSON. It does **not** establish which datapack definition wins at runtime.

## Binding source proof / acceptance for each mapping
1. Extract from the **exact installed JAR** (not generic online documentation). Match source-resource SHA256; verify the triggering loot table exists and its structure/template NBT actually references it; verify owner/structure association and dimension.
2. List selected pool's original entries/weights, conditions, functions, table-level functions, optional gated items and any recursion/unique trophies. `getRandomItemsRaw` must represent exactly one extra native-source draw and must not reproduce guaranteed unique boss rewards.
3. For each **cross-table** mapping, state why the selected pool is the best suitable existing native treasure pool in that structure. A room chest pulling from top treasure can be intentional; a garden-normal pool from a library-treasure chest needs justification. If not defensible, hold that trigger or identify its own verified native treasure pool instead.
4. Confirm exact installed Paxi / data resource precedence and loot-modifier timing, including Lootr conversion and individualized loot generation. `replace:false` is insufficient to establish Java append behavior; explicitly assert original list contents remain intact.
5. Mark entries **SOURCE VERIFIED / REVIEW HELD / STATIC UNKNOWN / RUNTIME ACCEPTED** separately. No automatically promoted reward pool or invented item IDs.

## Reproducible evidence tool added to PR #63
After installing the **actual** modpack locally via CurseForge, run on Windows:

```powershell
python tools/audit_r3_native_reward_sources.py --mods "C:\Minecraft\Instances\Ambient Odyssey\mods" --paxi "C:\Minecraft\Instances\Ambient Odyssey\config\paxi\datapacks" --out build\r3-reward-source-audit.json
```

Substitute actual profile path. Script reads JARs, checks source and trigger tables, expected SHA256, pool index and entries, and detects matching Paxi overrides. It also scans all Regalia catalogue candidates for *static* item-model/recipe clues and honors exclusions; **it does not prove item registration or approve new Regalia**. It never mutates modpack files.

### Important packaging boundary
The public GitHub Git tree does **not** contain official installed JARs; R2's CurseForge import ZIP has 337 manifest refs plus 10 custom JARs, not the other ~330 official mod binaries. Therefore this document and CI synthetic tests cannot substitute for a real installed-mod/JAR source audit.

Until those artifacts are audited, **do not claim all 14 are verified or expand beyond them**. Reuse R2 only as an experimental source, and keep R3 archive separate.
