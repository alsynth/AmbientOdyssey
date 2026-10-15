# Scylla ability test: which config key controls which ability

## What run 6 showed (one log with two attempts: 122 hits in total across both, player 1024 max HP, armor 0)
*Correction:* the log contains an interrupted first attempt and a complete second one; per-slot verdicts use the second, the hit-size clusters use both (both are default-config samples). The lightning-area ticks and the 71-sized hit came from the first attempt.

Her baseline was identical in all three spawns (390 HP, attack 18, armor 12, no modifiers from any other mod, clear weather). Hit sizes fall into three groups:

| Group | Sizes in phase A (attack 18) | Sizes in phase B (attack x4 = 72) | Reading |
|---|---|---|---|
| Scaled by the attack attribute | 32-54 (mostly 36 = 18 x 2) | 112-156 (mostly 123) | melee-style hits; grew about x3.4 |
| Fixed absolute damage | 16 (8 hits), 14, 9, 4, 2 | 16, 14, 9, **4 (16 hits)**, 2 | match `snake_damage`/`anchor_damage` 16, `spear_damage` 14, `lightning_area_damage` 4 (a damage-over-time tick); **unchanged by the attribute** |
| Percent of the target's max HP | 71 (1 hit), 51 (2 hits) | none | match `spin_hp_damage` 0.07 (7% of 1024 = 71.7) and `hp_damage` 0.05 (51.2) |

## Why the spin "often skipped dealing damage"
Vanilla invulnerability frames: for about 10 ticks after a hit, a new hit only counts if it is **larger** than the last one. With the attribute at x4 the melee hits are about 123, so the smaller percent-of-HP spin hit (about 72) arriving inside that window is ignored. The log fits this: phase B has 65 hits and **no hit between 20 and 100 except one**, while phase A has the 51 and 71 hits. This is an inference from the hit sizes, not a proven mechanism. Also note that these hits are percent of the *target's* maximum health, so their size depends on who is hit.

## Test config: every ability damage doubled
`cataclysm-common-TEST-scylla-abilities.toml` (your live file; exactly these 8 keys under `[mobs.scylla]` differ, verified):
`spear_damage` 14 to 28, `lightning_storm_damage` 10 to 20, `lightning_area_damage` 4 to 8, `snake_damage` 16 to 32, `anchor_damage` 16 to 32, `hp_damage` 0.05 to 0.10, `spin_hp_damage` 0.07 to 0.14, `lightning_storm_hp_damage` 0.04 to 0.08. `attack_multiplier` and `health_multiplier` are untouched on purpose.

Expected in **phase A** (no AOT modifier, so the clusters are clean) if each key controls its ability: 16 becomes 32, 14 becomes 28, 4 becomes 8, 9 (probably lightning storm) becomes about 18, 71 becomes about 143, 51 becomes about 102, while the 36-family (melee) stays at 36.
Anything that does not move is not controlled by these keys (then `attack_multiplier` is the next candidate).

## Run it
1. Back up and replace `config/cataclysm-common.toml` with the test file (renamed). Restart the game (it is a normal config file).
2. Fresh Superflat world, stand at spawn, `/function aot:start_scylla` (about 5 minutes), send `latest.log`.
3. Put `cataclysm-common-ORIGINAL.toml` back afterwards.

## Results of the doubled-config run (run 7, 3 Scylla spawns)
Exact hit sizes, default config (run 6) against every ability doubled (run 7). Attack-attribute scale is irrelevant in phase A.

| Ability | Config key | Before | After doubling | Verdict |
|---|---|---|---|---|
| Spear | `spear_damage` 14 | 14.0 | **28.0** (3 + 3 hits) | confirmed |
| Snake / Anchor | `snake_damage`, `anchor_damage` 16 | 16.0 (8 hits) | **32.0** (5 + 3 hits), no 16 left | confirmed (both keys were doubled, so they cannot be told apart) |
| Lightning area (damage-over-time ticks) | `lightning_area_damage` 4 | 4.0 (16 ticks) | **8.0** (7 ticks) | confirmed |
| Percent hit | `hp_damage` 0.05 | 51.0 | **101.9** (exactly x2) | confirmed |
| Melee family | the attack attribute, not a config key | 36 = 18 x 2 (x0.9..1.1) | 144 = 72 x 2, exactly x4 | **fully attribute-driven**: the earlier "x3.4" came from mixing in the fixed hits |
| Spin (7% hit) | `spin_hp_damage` 0.07 | 71.3 (1 hit in 57) | not seen | **unconfirmed**: it almost never lands in a 30 s sample |
| Lightning storm | `lightning_storm_damage` 10, `lightning_storm_hp_damage` 0.04 | not seen | not seen | **unconfirmed**: never observed in either run |
| The wave (a constant 9.0 hit, pulses 0.5 s apart; identified by the owner's description) | none of the eight keys | 9.0 | 9.0 | **no known lever so far**; unchanged by the doubling and by the attribute x4 |

Also unexplained: one of the three spawns read attack 22 instead of 18, with identical saved NBT, attachments and effects and clear weather: a transient modifier that leaves no trace in the data.

## Next test: make the spin and lightning storm unmistakable
`cataclysm-common-TEST-scylla-spin.toml` (your live file with exactly three keys changed): `spin_hp_damage` 0.07 to **0.4** (about 408 on the 1024-HP test player), `lightning_storm_hp_damage` 0.04 to **0.25** (about 255), `lightning_storm_damage` 10 to **100**. These sizes are far above anything else Scylla deals, so they cannot be mistaken for another ability and cannot be hidden behind a larger hit. `/function aot:start_scylla_long` samples **60 seconds per phase, twice** (about 7 minutes) so rare abilities get a chance to land.
Reading it: a hit near 408 is the spin, near 255 the lightning-storm percent hit, exactly 100 the lightning storm. If none appears, the ability does not trigger in this arena (it may need conditions that an empty Superflat does not provide), and that is itself the answer.
Same swap procedure as before: close the game, back up your `cataclysm-common.toml`, rename the test file to `cataclysm-common.toml`, restart, fresh Superflat, send the log, restore your file.

## Result of the `attack_multiplier` 3.0 test (run 8)
The config loaded: her attack baseline read **54 (18 x 3)** in all three spawns although the saved NBT base stayed 18 with no modifiers, so the multiplier is an unsaved modifier applied at spawn. HP stayed 390. Phase A hit sizes:

| Hit | Before (x1) | With `attack_multiplier` 3.0 | Reading |
|---|---|---|---|
| melee family | 36 (x0.9..1.1) | 97 to 111 (97.2 is exactly 54 x 2 x 0.9) | scaled by the multiplier |
| **wave** | 9.0 | **9.0** (10 hits in A, 5 in B, **none at 27**) | **not scaled** |
| snake/anchor 16, spear 14 | 16, 14 | 16, 14 | not scaled |
| 5% and 7% percent hits | 51.0, 71.3 | 51.0, 71.3 | not scaled |
| a constant 20.0 (5 hits) | not seen before | 20.0 | unexplained |

**Conclusion: the wave has no known lever.** It did not change with the attack attribute x4, with the general multiplier x3, or with the eight ability keys doubled, and the config has no wave key for Scylla.

## Still open: the spin and lightning-storm test, version 2
Run 9 ran the 30-second chain by mistake and showed none of the markers, so it settled nothing. Version 2 of `cataclysm-common-TEST-scylla-spin.toml` changes four keys (verified): `spin_hp_damage` 0.07 to **0.4**, `lightning_storm_hp_damage` 0.04 to **0.25**, `lightning_storm_damage` 10 to **100**, and a **canary** `snake_damage` 16 to **25**. Snake hits occur in nearly every phase, so if hits of 25 appear the file is certainly loaded even if the spin never lands. It also separates snake (now 25) from anchor (still 16).
Run `/function aot:start_scylla_long`; the log must contain the line `AOT|CHAIN|scylla_long|phase_ticks=1200`. Markers (damage, chat shows tenths): spin about 408 (4080), storm percent hit about 255 (2550), storm 100 (1000), snake 25 (250).
