# Grand Treasure: per-table evidence for the five pending assignments

**Status:** Approved: **no, all five PENDING**. Every approval flag in `R5_GRAND_FIVE_DECISIONS_DRAFT_NOT_APPROVED.json` is `false` (20 flags, status `DRAFT_NOT_APPROVED`, SHA256 `041d2b27…23d5`; never edited). Implemented: no. Statically verified: yes, see below. In-game tested: no. Multiplayer tested: no.

**Correction:** this supersedes the blanket "approve all five" line in `GRAND_FIVE_POOL_NATIVE_ACCEPTANCE_20261015.md`. Two of the five now have reasons to reject or hold.

**Sources:**
- installed JARs (local profile, 338);
- the **restored R4 ZIP** (SHA256 `31b037a7…6c6d`, verified against the receipt) for overrides;
- structure NBT scans of all installed JARs.

Grand draws **one** roll from the chosen pool (`GrandTreasure.java:58-59`: `rolls=1`, `bonus_rolls=0`), keeping the pool's own functions.

## 1. `adventuredungeons:chests/murkydungeon/murky_chest_reward` (T3), pool 0 → 2
- **Native source:** `adventuredungeons-neoforge-1.21-1.3.1.jar`, `data/adventuredungeons/loot_table/chests/murkydungeon/murky_chest_reward.json`, SHA256 `6cd05c74…c212` (matches the recorded hash).
- **Effective source:** no override in R4 (any path) or in the local Paxi folder. Single provider JAR.
- **Proposed pool entries:** Wild trim template (w2), Sentry trim template (w1), disc 11 (w1), disc Otherside (w2). No functions or conditions.
- **Reward category:** cosmetic and collectible.
- **Conflicts:** none found. Used only by `murky_room2` and `murky_room3`. No unique or progression items.
- **Recommendation: approve.** It replaces a one-ingot draw with a rarer collectible. Value is subjective; you might prefer materials.

## 2. `dungeons_arise:chests/keep_kayra/keep_kayra_library_treasure` (T6), pool 2 → 1
- **Native source:** `DungeonsArise-1.21.1-2.1.68-release.jar`, SHA256 `ee7e3983…0084f` (matches).
- **Effective source:** no override in R4 or Paxi.
- **Proposed pool entries (total weight 106):**
  - book w40 (`enchant_with_levels` 28, treasure);
  - bow w8 (20–39);
  - crossbow w1 (25–39);
  - diamond sword, helmet, chestplate, leggings and boots, w8 each (20–25);
  - Netherite Helmet w2 (no function);
  - ender pearl w15 (1–2).
- **Reward category:** equipment and enchanting.
- **Conflicts:** no uniques. Brutal Bosses lists this table as a **boss-spawn trigger** (`evokerboss`, `evokersummoner`, `dummyboss`). That's unrelated to Grand, just noted.
- **Recommendation: approve.** It fits T6. About 14% of draws are a low-value ender pearl.

## 3. `dungeons_arise:chests/keep_kayra/keep_kayra_treasure` (T6), pool 2 → 1
- **Native source:** same JAR, SHA256 `8bf79cee…a0be` (matches).
- **Effective source:** no override in R4 or Paxi.
- **Proposed pool entries (total weight 114):** as #2, but Netherite Boots w2 instead of the helmet, plus blaze powder w8 (1–4).
- **Reward category:** equipment and enchanting.
- **Conflicts:** no uniques. Also a Brutal Bosses spawn trigger (`zombieboss`, `skeletonshieldboss`, `evokersummoner`, `dummyboss`).
- **Recommendation: approve.** Same pearl note (about 13%).

## 4. `irons_spellbooks:chests/catacombs/hidden_trough_treasure` (T4), pool 3 → 1
- **Native source:** `irons_spellbooks-1.21.1-3.16.3.jar`, SHA256 `23372ec8…6ce8` (matches).
- **Effective source:** no override in R4 or Paxi.
- **Proposed pool entries:** spell scroll w2 (`irons_spellbooks:randomize_spell`, quality 0.3–1.0) and blank rune w1.
- **Reward category:** magic.
- **Conflicts:**
  - Used only in `catacombs/room/dormitories_2` and `ravager_prison`.
  - Quality up to 1.0 can produce top-rarity scrolls at T4. That's native behaviour, but it becomes more frequent.
- **Recommendation: approve with a note.** Test scroll rarity in game. Reject if T4 legendary scrolls are too strong for you.

## 5. `irons_spellbooks:chests/generic_magic_treasure` (T4), pool 6 → 1
- **Native source:** same JAR, SHA256 `f3f8c946…b776` (matches).
- **Effective source:** no override in R4 or Paxi. **But `irons_jewelry-1.21.1-2.0.2.jar` adds a loot modifier on this table** (`chest_loot/gems/compat_wealthy_gems`).
- **Proposed pool entries:** spell scroll w1 (`randomize_spell`, quality 0.0–0.6).
- **Reward category:** magic.
- **Conflicts:**
  - **This is a shared generic table.** Structure NBT in Iron's JAR places it in 7 structures: catacombs, citadel, evoker fort, ice spider den, mangrove hut, mountain tower, pyromancer tower.
  - The R4 context maps it as **catacombs T4**, so a Grand trigger keyed on this table fires in all 7, including small ones like the mangrove hut. That breaks the owner rule against shared tables outside mapped structures.
  - **This is an existing R4 issue** (R4 already triggers here with pool 6). It isn't caused by the proposed pool change, which only changes what the extra roll gives.
  - Whether Iron's Jewelry's modifier also acts on Grand's extra roll is unverified.
- **Recommendation: reject (hold)** until the trigger is scoped to catacombs only. Also report the existing R4 context for your review.

## Summary

| # | Table | Tier | Recommendation |
|---|---|---|---|
| 1 | murky_chest_reward | T3 | approve |
| 2 | keep_kayra_library_treasure | T6 | approve |
| 3 | keep_kayra_treasure | T6 | approve |
| 4 | hidden_trough_treasure | T4 | approve with note (scroll rarity) |
| 5 | generic_magic_treasure | T4 | **reject / hold** (shared across 7 structures) |

All approvals stay with you. Nothing is enabled.
