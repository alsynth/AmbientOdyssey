## Simply Swords full sword pool (15 October 2026, branch feature/simply-swords-full-pool)

- **Source:** boss reward draws one uniform random sword from 133 verified Simply Swords swords (`ao_sword_pool.json`, `BossRewards.swordPoolIds()`), separate from the affixed item and Regalia. `ao_loot_policy.json` unchanged (R5 toolchain pin). Campaign version 0.3.3-experimental. Nothing excluded; 53 owner-review candidates listed in [SIMPLYSWORDS_FULL_POOL.md](../../handoffs/simplyswords-full-pool-20261015/SIMPLYSWORDS_FULL_POOL.md).
- **Static test:** `tests/test_simplyswords_full_pool.py` 7/7 PASS; `javac --release 21` against R4-pinned NeoForge/Minecraft/Apotheosis JARs exit 0. **Packaged:** no. **Engine / multiplayer:** not tested.
