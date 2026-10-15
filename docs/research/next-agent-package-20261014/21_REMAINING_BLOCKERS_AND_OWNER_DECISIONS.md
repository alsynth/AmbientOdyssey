# Remaining blockers and owner decisions (DRAFT, 14 October 2026)

Only genuinely open items. Everything the owner has decided is in `00_HANDOFF_PACKAGE_INDEX.md`.

## A. Owner decisions
| Item | State |
|---|---|
| Geburah | **TBD** (owner: leave for later) |
| Eternal Starlight family members, boss respawn | **TBD** (owner: can wait); respawn is config only |
| Unnamed 'comparable strong Tier 6 boss' | open; must not be invented |
| Brutal Bosses global factor | open (x3 is a placeholder; set both keys equal) |
| Reward pacing, Rage Glove boss (proposal: Netherite Monstrosity), the high-grade gem gap | open |
| **A player-power reference per tier** | open, and it **blocks the difficulty curve**: without it any target is arbitrary |
| Damage-scaling addon | deferred by the owner; can be added after pregeneration |

## B. Checks only the owner can run in game
1. `/datapack list enabled` (Integrated versus original arena precedence).
2. `/function aoa:start` in the final world preset, log back (Overworld arena check, 87 searches); `/function aoa:start_other` later.
3. Walk to located arenas and record how each boss appears (template provided).
4. The server-config check (the 29 `-server.toml` files): decides whether Iron's and Bosses'Rise values apply.
5. Optional: the Scylla spin and lightning-storm test (configs ready); the measurement run for unmeasured bosses.

## C. Technical gaps
- **Never measured (5):** Ignited Revenant, Coralssus, Kobolediator, Ender Golem, Ice and Fire Hydra.
- **Health measured, damage not (needs the special interaction):** Eternal Starlight: The Gatekeeper, Eternal Starlight: Starlight Golem, Ancient Remnant, Bosses'Rise: Yeti.
- **Arena not identified:** Tyros, Captain Cornelia, Ender Golem, Ignited Revenant, Coralssus (the Cataclysm and Iron's jars would settle these statically). Lunar Monstrosity's arena is inferred; Last of Deepslate's dimension is unknown; Scylla's Acropolis is missing from the v3 catalogue and counted zero curated biomes in Test 5.
- **Unverified:** runtime precedence of Integrated arenas; whether Eternal Starlight's portal ruins are the only way in (and AO made them sparser, 36/30 to 45/32); SERVER-config location.
- **No lever found:** Scylla's wave; Aquamirae and Archaion have no config file.
- **Unconfirmed:** Scylla's spin and lightning storm (the first test ran the wrong chain).
- **Owner assumption:** Ancient Remnant edits like the other Cataclysm bosses (its health was measured; damage needs its interaction).
- **Cap:** health stops at 1024 on every boss; armor, effects or the deferred addon are the options.
- **Not assessed:** Apotheosis affix interactions, party-wipe health retention, summon exploits, performance, player-count scaling.

## D. Not started (by design, waiting on A)
Deliverable 1 (the implementation package), deliverable 3 as a real report, and deliverable 5's experimental build.

## E. Closed on 14 October
Third Tier 9 boss (Obsidilith); Ignis, Maledictus and Leviathan at Tier 8; Mother of Maze is not a boss; Ancient Remnant entity; Overworld pregeneration first; Remnant Bosses and Eternal Starlight inspected (no blocked rows); Bosses'Rise is the same mod as Block Factory's Bosses.
