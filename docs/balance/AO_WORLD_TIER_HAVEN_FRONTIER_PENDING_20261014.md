# World Tier rarity follow-up — 14 Oct 2026 (owner request)

Overrides proposed on top of AO draft PR #53; **not implemented**, since remaining weights are not specified.

| Tier | Rarity | Existing AO PR53 | New owner target | Delta (percentage points) |
|---|---|---:|---:|---:|
| Haven | Common | 60% | **45%** | -15 |
| Haven | Uncommon | 36% | **28%** | -8 |
| Frontier | Common | 29% | **25%** | -4 |
| Frontier | Uncommon | 60% | **42%** | -18 |

**Unallocated probability:** Haven 23 percentage points; Frontier 22 percentage points, relative to their earlier 100% rarity distributions if Rare/Epic/Mythic weights remain unchanged. Decide where these are allocated before modifying JSON. Do **not** normalize silently, set implicit drop chance, or assume Rare/Epic/Mythic destinations.

The original Haven Rare was 4%; original Frontier Rare 10%, Epic 1%. New requested Common/Uncommon plus unchanged higher-rarity weights total 77% Haven and 78% Frontier. This is *rarity conditional on an affix roll*, not the chance loot includes an affix item. PR53 pinned-JAR validation must rerun after finalized weight values, with all rows summing 100. This note does not change gameplay configs or PR53.
