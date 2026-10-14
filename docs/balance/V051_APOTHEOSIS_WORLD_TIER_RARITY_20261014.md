# Ambient Odyssey — Apotheosis 8.9.0 World Tier rarity tuning

**Date:** 2026-10-14  
**Status:** owner-approved isolated experimental datapack; pinned native-data static CI verification required; **not merged into an existing experimental import ZIP**.

## Approved distribution

These figures are relative rarity weights **when a rarity is selected** at zero additional Luck. They are **not** the per-chest probability of finding an affixed item. Nonzero player Luck changes the weights according to each original rarity definition's `quality` values; these quality coefficients remain unmodified.

| Apotheosis World Tier | Common | Uncommon | Rare | Epic | Mythic |
| --- | ---: | ---: | ---: | ---: | ---: |
| Haven | 60% | 36% | 4% | 0% | 0% |
| Frontier | 29% | 60% | 10% | 1% | 0% |
| Ascent | 10% | 35% | 50% | **5%** | 0% |
| Summit | 0% | **15%** | **50%** | **30%** | 5% |
| Pinnacle | 0% | 0% | **20%** | **65%** | **15%** |

To obtain valid 100%-sum distributions without altering additional named percentages, redistribute unused shares only to **lower** rarity categories: Ascent Epic 10→5 gives Uncommon 30→35; Summit Epic 54→30 and Rare 29→50 gives Uncommon 12→15; Pinnacle Mythic 25→15 gives Rare 10→20. These three remainder allocations can be changed after owner feedback; the explicitly requested Epic/Rare/Mythic percentages are exact.

## Modified data only

New Paxi datapack: `release_030/overrides/config/paxi/datapacks/ao_world_tier_balance/`.

Overrides only four native objects at `data/apotheosis/rarities/<rarity>.json`:
- `uncommon`: Ascent 300→350, Summit 120→150
- `rare`: Summit 290→500, Pinnacle 100→200
- `epic`: Ascent 100→50, Summit 540→300
- `mythic`: Pinnacle 250→150

Unchanged: Common definition; remaining weights; all rarity colors, loot/affix rules, socket rolls and base item pools; each rarity's `quality`/Luck coefficient; 5 vanilla Apotheosis world tier names and unlock advancements; per-tier monster/player augments; invader natural spawn rules; chest affix-generation/affix-conversion chances; starter Bonus Chest dedicated 55/30/15 distribution; all dungeon tiers and difficulty settings; boss drops/loot.

The starter Bonus Chest's custom 55/30/15 affix roll is intentionally **unchanged**, because it has its own independent generator. Ordinary early/midgame structure loot is unchanged.

## Invader and Dungeon Difficulty policy

Owner accepts the existing overlapping scaling, noting invaders usually appear outside combat structures or in normal subterranean dungeons rather than higher-tier structured encounters. No additional invader protections, global dungeon nerfs, or boss-stat patches in this scope. World Tier augments can affect other monsters too, but that is a separate possible stacking behavior and not a reason for an unrequested nerf.

## Validation

Run pinned-data consistency gate:
```sh
python3 tools/validate_ao_world_tier_rarity.py /path/to/Apotheosis-1.21.1-8.9.0.jar
```
GitHub Actions: `.github/workflows/ao-world-tier-rarity-pinned-validation.yml`. This asserts:
1. All five original JAR rarity weights equal the expected reference baseline.
2. The four staged override JSONs equal **the pinned JAR versions, with ONLY the seven allowed weight integer edits**; all other fields match exactly.
3. Each of the five intended rarity weight columns sums to 1000.
4. The new datapack contains only four rarity overrides plus `pack.mcmeta`, which uses Minecraft 1.21.1 format 48.

Then in **a disposable full-modpack profile** verify:
- Paxi loads the datapack and its priority overrides Apotheosis's built-in data.
- The World Tier screen displays the intended percentage distribution (at zero Luck) and no missing rarity errors on datapack reload.
- Sampling repeated generated rarity outcomes across all five tiers matches distribution within statistical tolerance; also test bonus chest unchanged.
- World Tier advancements work, monster augments are unchanged, and existing Dungeon Difficulty rules remain intact.
- Test server and two clients; reject only upon measured faults, and keep this draft isolated from the unpublished combined ZIP until tested.

**Important:** Do not silently include this balance experiment in Work mode's as-yet-undelivered PR #50 + #51 full import. It needs its own explicit build version/acceptance so source changes do not invalidate its SHA256.
