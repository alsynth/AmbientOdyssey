# Ambient Odyssey — Q1 Questlog playable-content pilot (10 October 2026)

**Experimental source branch:** `experimental/v0.4h-questbook-q1-20261010`  
**Compatible pack:** Minecraft 1.21.1, NeoForge 21.1.252, **331 unchanged pinned CurseForge mod projects**, Questlog 3.4.1, existing FTB Quests.

## What's actually written and installed

**50 JSON quest definitions across 13 chapter JSON tabs**, not merely suggestions or a quest list. They are installed as configuration overrides at `config/questlog/quests/*.json` and `config/questlog/chapters/*.json`. Questlog's 1.21.1 official examples demonstrate this layout, `questlog:quest_complete`, `questlog:read`, `questlog:item_obtain`, `questlog:or`, `questlog:stat`, `questlog:visit_biome` and `questlog:visit_dimension`.

| Chapter | Actual JSON quests | Concept |
|---|---:|---|
| The First Pages | 13 | Welcome, JEI, journal versus manual, shield, useful armor, provisions, maps, loot, equipment slots |
| The Open Road | 12 | Walking, scouting different biomes, landmark discovery, cave supplies, travel gear, journey-home planning |
| Trial by Steel | 7 | **Optional** vanilla diamond preparation benchmarks, flexible enchantment, weapon choice, defense reading; not a requirement to progress elsewhere |
| Rumours of the Wild | 5 | Spyglass, boat, fishing, optional Nether passage and preparation lights |
| Unearthed Histories | 3 | Brush, optional sherd discovery, preservation ethics; concrete modest reward for scarce archaeology finds |
| The Relic Scholar | 2 | Normal uncursed Enigmatic Legacy route invitation |
| The Seven Curses — Opt In | 2 | Carefully worded **information only**; no cursed ring granted or activated |
| Dreamseeker's Notes | 1 | Optional NeoPasterDream introduction; no fabricated biome/dimension ID |
| Frozen Seas | 1 | Aquamirae expedition preparation, not false proof of maze visit |
| The Arcane Academy | 1 | Ars Nouveau introduction, actual glyph/item IDs later |
| The Spellwright's Journey | 1 | Iron's Spells introduction |
| The Twilight Path | 1 | Twilight Forest travel introduction |
| The Eyes of the End | 1 | End Remastered eye-system introduction |

The 42 earlier short narrative entries were selected/reworked from `docs/questing/WRITTEN_QUEST_DRAFTS_V0_2.json`, preserving their stable seed-derived IDs. Eight further original expedition and archaeological field notes were authored for Q1.

**Explicit constraints:** All task IDs in this pilot are Questlog-defined task types; referenced items, biomes, dimensions, structures and statistic identifiers are restricted to known vanilla Minecraft names, not unverified modded registry IDs. Many tutorial/prologue entries use a `questlog:read` completion objective and state clearly they record acknowledgment, NOT practical proof of claiming a waypoint, defeating a boss, equipping a modded Curios item or clearing a dungeon. Some optional vanilla landmark and biome checks remain natural-generation tests.

## Reward and progression integrity

- All main opening chapters are flexible invitations. Completing a cursed route, rare structure, enchantment, diamond armor set, archaeological sherd or Nether visit is never a prerequisite of the opening journey.
- No Questlog quest is repeatable or global; rewards are small, vanilla items or experience only, with no unconditional loot-table grant or commands.
- FTB Quests and the existing WDA questline remain untouched; the extensive future FTB Field Manual is still original text drafts until its SNBT articles can be tested.
- Q1 chapter tabs deliberately reveal optional reading introductions rather than dumping hundreds of modpack-wide subtasks onto a new player.
- Archaeology is a meaningful optional activity rather than busywork; the first pottery sherd awards eight emeralds and experience, subject to actual balance testing. There are no unknown-mod items given as rewards.

## Static evidence required before gameplay testing

Run `python tools/validate_v04_quest_campaign.py` for **exactly 50 unique quest JSON files**, 13 valid chapters, valid prerequisite targets, cycle-free dependencies, restricted real vanilla objectives, reward limits and no required cursed prerequisites. Run all inherited v0.4 content and worldgen gates, rebuild the private and reference-only CurseForge ZIPs and compare private clean repeat bit-for-bit.

**No full game runtime success has been achieved for this questbook.** Questlog's authoring format and Java parser were inspected, but opening the actual journal, reading quests, reward attribution, client/server sync, player save migration and FTB Quests coexistence must still be tested. Use the earlier successful 331-mod pack as a fallback. Do not force this Q1 source into a permanent server or overwrite an existing `world/playerdata` save.

## Q1 playtest acceptance

1. Open inventory and journal, verify the button position from v0.4h and 13 chapter labels/icons. Confirm only `A New Page` is initially active, with later introductory entries available after reading.
2. Read the first page, then inspect Field Manual and JEI learning entries; ensure read progress updates once per player and across restart.
3. Collect a shield and provisions, complete a vanilla travel activity, verify XP/items only when explicitly claimed, and ensure no duplicated rewards when reopening or reloading.
4. Confirm archaeology and curse tabs are genuinely optional, and the normal Enigmatic route has no cursed prerequisites or forced ring effect.
5. In a disposable dedicated server, have two players independently complete distinct quests; compare their journal states, drops and save/reload persistence. Check FTB Quests and FTB Solo Quests separately.
6. Audit latency with multiple players. There are only a few vanilla `visit_biome`/`visit_structure` tasks, not hundreds of polling trackers; source-only checks cannot establish TPS cost.

**Future writing:** replace preliminary read-only intros with exact modded objective IDs *after installed JAR registry audit and runtime evidence*, expand rich dimension/boss arcs, add FTB Field Manual pages, review high-value archaeology rewards, and make an extensive, curated cross-mod questbook. See `QUEST_CAMPAIGN_ARCHITECTURE.md` for target depth and postponed choices.
