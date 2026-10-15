# Grand Treasure: five-pool native acceptance audit (deliverable C, 15 October 2026)

**Result:** all five proposed R5 pools pass the static checks. The native table hashes match, the pools exist, only one installed JAR provides each table, and nothing in AO's Paxi packs or source overrides them. I recommend approving all five **for an experimental R5 test only**. The approval form is generated with every approval `false`. You fill it in; I haven't.

**Status:** static evidence from the installed JARs only. Not engine-tested, not two-player Lootr tested. The R4 ZIP isn't on disk now, so steps 4–5 (patch and package) weren't run.

## What was run
Run from `status/grand-five-pool-audit` (tools identical to PR64 `3806fa1`), following `CLAUDE_R4_TO_R5_LOCAL_EXECUTION.md` steps 1–3:
1. `preview_r5_grand_from_r4.py`: 5 of 14 pool indices proposed; the rest of the policy is unchanged.
2. `audit_r3_native_reward_sources.py` against the local profile: **338 JARs** and its `config/paxi/datapacks`. Result: 14/14 contexts direct, 0 cross-table, 0 blocked, every status `SOURCE_STATIC_VERIFIED_NOT_RUNTIME_APPROVED`, no blockers.
3. `patch_r5_grand_from_r4.py --mode draft`: review form created, all approvals `false`.

Evidence: [GRAND_FIVE_POOL_AUDIT_EVIDENCE.json](GRAND_FIVE_POOL_AUDIT_EVIDENCE.json), with the preview and audit SHA256 and all 14 contexts. The full outputs are in `build/r5-grand/` (not committed, regenerable).

**Profile caveat:** the local profile is pre-R4 (v0.4.9.1). That's acceptable here because each table's SHA256 matches the pinned native hash, so the bytes are the ones R5 targets. AO's source (= R4 Paxi content) has no override for any of the five tables. Recheck on an R4 install (checklist D1).

## How Grand uses a pool
`GrandTreasure.java:58-59` copies the chosen native pool and forces `rolls=1`, `bonus_rolls=0`. So each Grand hit gives **one** draw from that pool, with the pool's own item functions (enchanting, counts, spell randomizing) kept.

## The five pools (old R4 index → proposed index)

| Table | Tier | Old pool (R4) | Proposed pool | Static verdict |
|---|---|---|---|---|
| `adventuredungeons:chests/murkydungeon/murky_chest_reward` | T3 | 0: iron, gold, emerald or diamond (one item) | 2: Wild or Sentry trim template, disc 11 or Otherside | **Pass.** Fits a treasure category and doesn't duplicate base materials |
| `dungeons_arise:chests/keep_kayra/keep_kayra_library_treasure` | T6 | 2: gold, emerald or diamond | 1: enchanted book (40/106), diamond gear and bows with functions, Netherite Helmet (2/106), ender pearl (15/106) | **Pass.** Note: about 14% of draws are a low-value ender pearl |
| `dungeons_arise:chests/keep_kayra/keep_kayra_treasure` | T6 | 2: gold, emerald or diamond | 1: same gear and book pool, Netherite Boots (2/114), blaze powder (8/114), ender pearl (15/114) | **Pass.** Same ender pearl note (about 13%) |
| `irons_spellbooks:chests/catacombs/hidden_trough_treasure` | T4 | 3: emerald or diamond | 1: spell scroll (`randomize_spell`) 2/3, blank rune 1/3 | **Pass** |
| `irons_spellbooks:chests/generic_magic_treasure` | T4 | 6: copper, iron, gold, emerald or diamond | 1: spell scroll only (native 1–2 rolls, Grand gives 1) | **Pass** |

Each table's checks: native SHA256 matches, pool index exists, no pool conditions, one source JAR, `potential_paxi_overrides: []`.

## What only you can do
1. Approve or reject each pool in `build/r5-grand/R5_GRAND_FIVE_DECISIONS_DRAFT_NOT_APPROVED.json` (status `APPROVED_FOR_EXPERIMENTAL_TEST_ONLY`, four checkboxes per chest, with reasons).
2. Make the exact R4 ZIP available locally for steps 4–5. The R5 packager now also installs the Cornelia Pinnacle gate (`feature/r5-gate-safeguard`).
3. After building: two-player Lootr test (reopen, restart) and natural chests.

## Not tested
Engine loading of the patched policy, Paxi load order at runtime, Lootr per-player generation, and real chest frequency.
