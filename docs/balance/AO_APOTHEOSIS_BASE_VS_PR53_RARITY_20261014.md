# Apotheosis 8.9.0 base vs Ambient Odyssey proposed World Tier rarity — 2026-10-14

**Source:** official Apotheosis rarity weights, plus AO draft PR #53 (`https://github.com/alsynth/AmbientOdyssey/pull/53`, pinned-JAR validator run 38491462040). AO values are an **approved proposal validated in CI**, not confirmed present in a user runtime build; PR53 explicitly says not to merge without Paxi/runtime acceptance.

| World tier | Base Common | AO Common | Base Uncommon | AO Uncommon | Base Rare | AO Rare | Base Epic | AO Epic | Base Mythic | AO Mythic |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Haven | 60 | 60 | 36 | 36 | 4 | 4 | 0 | 0 | 0 | 0 |
| Frontier | 29 | 29 | 60 | 60 | 10 | 10 | 1 | 1 | 0 | 0 |
| Ascent | 10 | 10 | 30 | 35 | 50 | 50 | 10 | 5 | 0 | 0 |
| Summit | 0 | 0 | 12 | 15 | 29 | 50 | 54 | 30 | 5 | 5 |
| Pinnacle | 0 | 0 | 0 | 0 | 10 | 20 | 65 | 65 | 25 | 15 |

**All percentages conditional on rolling an affix rarity at zero bonus Luck**, not the absolute chance that loot includes an affixed item. Source interpretation: original general chest/mob affix conversion and loot injections are separate from rarity selection. AO PR53 preserves those base injection/conversion tables. Exact AO currently-running datapack requires in-game /datapack check; PR53 is unmerged.

Separately, AO PR #51 starter Bonus Chest native affix generator is **55% Common / 30% Uncommon / 15% Rare** and is an exception only for that chest, not a World Tier-wide change. No new loot edits by PR56.

Research note only; this is not a change to gameplay or PR53.
