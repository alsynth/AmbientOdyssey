# Scylla field guide: recognising her attacks from the chat lines

**What is verified and what is not.** Verified: each *hit size* below, how often it appears and how it is timed (from three runs), and which config key controls it (the doubling test). **Not verified: which animation each one is.** I found no written description of her animations and have not seen them. The ability names in the last column are guesses from the config key names.

While the AOT test runs, every hit you take prints a chat line `AOT|HIT|slot|phase|N`. **N is the damage in tenths** (N = 360 means 36.0, and the wave's `90` is 9.0 damage per pulse on this 1024-HP, armor-0 test player). Phase 1 (A) is her normal attack value, phase 2 (B) has the attack attribute x4, which only changes the melee family.

| Chat shows (N) | Damage | What it looks like in the data | Controlled by | Guessed ability (from the key name) |
|---|---|---|---|---|
| 324, 360 or 396 (phase B: about 1160 to 1300 and 1440) | 36 (x0.9 / x1.0 / x1.1) | the most frequent hit, spread through the fight | the attack attribute x2, no config key | basic swings |
| 160 | 16 | single hits, seconds apart | `snake_damage` and `anchor_damage` (both 16, cannot be told apart) | snake or anchor |
| 140 | 14 | single hit | `spear_damage` | spear |
| 40, **many in a row** | 4 | about 16 identical hits at **0.5 s intervals** (about 8 s) | `lightning_area_damage` | a lightning zone that zaps you every half second while you stay in it |
| 510 | 5% of your max HP | rare, one early hit about 1.6 s into a phase | `hp_damage` | an attack that scales with your health |
| 713 | 7% of your max HP | seen **once** in two attempts | probably `spin_hp_damage` | probably the spin |
| 90 (chat) = 9.0 damage | 9 | **the wave** (owner's observation: she sends out waves that kept doing the same damage). In the data: pulses at **exactly 0.5 s spacing**, e.g. +7.4, +7.9, +8.4, +8.9 s, 9.0 each (one 9.6) | **no known lever**: unchanged when all 8 ability keys were doubled, when the attack attribute went x4 and when `attack_multiplier` went x3; no wave key exists for Scylla in the Cataclysm config | the wave |
| (never seen) | 10 / 4% of max HP | not observed | `lightning_storm_damage`, `lightning_storm_hp_damage` | the lightning storm |

A hit can be **missing from the list on purpose**: for about half a second after you are hit, a new hit only registers if it is larger than the last one, so fast follow-ups, and a smaller spin hit after a big melee hit, vanish. The one 0.99 s gap in the lightning ticks is such a masked tick.

## How to turn this into an animation guide
Run the next test (`/function aot:start_scylla_long` with `cataclysm-common-TEST-scylla-spin.toml`). It makes the three unseen abilities unmistakable: the spin shows as **N about 4080**, the storm's percent hit as **about 2550**, the storm itself as **1000**. Watch the chat while you fight: whenever a line like that appears, note which animation just played. Send me the notes together with the log and I will complete the last column from observation instead of guesswork.

**Owner decision (13 Oct 2026): the wave is let go.** It is not necessarily a damage spell, it has no known lever, and it is not part of the editability work for Scylla.
