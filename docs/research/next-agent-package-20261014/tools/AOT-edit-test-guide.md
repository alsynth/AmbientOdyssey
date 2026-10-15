# AOT boss edit test: guide

Purpose: for each boss, measure whether a +300% max-health and +300% attack-damage attribute modifier really changes its health and the damage it deals. This is the route Dungeon Difficulty, Gateways to Eternity and Apotheosis use, so it answers "can the pack edit this boss's stats". It does not test mod config keys or scripted phases/abilities.

**Not tested by the author in game** (no Minecraft here). The command logic was checked with a simulator and static tests only. Expect a possible first-run fix; send the log either way.

## Before you start
1. **Remove immortality / cheat-death / health-changing items and gear.** Your first log showed 135 'death event canceled by another mod' warnings: lethal hits were being cancelled, which can stop them being counted.
2. After starting, chat must show `AOT|PLAYER|max=1024|hp=...` and `AOT|SELFTEST|...ok=1`, and **numbers after every `=`** in the `AOT|BASE` lines. Blank values mean the pack did not load: check `logs/latest.log` for `Failed to load function aot:` and send it to me.
3. Control mob is a **husk** (a zombie burned to death in daylight in the first real run).

## Built-in self-test (new)
About 2 seconds after you start, the pack damages you once (50 HP) and checks three things: your max health held, the hit was counted, and healing brought you back. Chat shows `AOT|SELFTEST|max=1024|dmg10=500|hp=...|ok=1`. If `ok=0`, a red "AOT self-test FAILED" message appears and **the run does not start** (this is what an immortality item or a health-resetting mod would cause). The first boss begins about 5 seconds after you type the command.

## Install
1. Single Player > Create New World. **Game tab:** Allow Commands = ON. **World tab:** World Type = Superflat, Generate Structures = OFF. Create the world with the full AO instance.
2. Put `AOT-edit-test-datapack.zip` into the world's `datapacks` folder (`saves/<world name>/datapacks/`; open the world once, quit, copy the zip, reopen). Run `/reload`.

## Run
- **RECOMMENDED: `/function aot:start_needed` (42 bosses + control, about 46 minutes).** Runs only the bosses whose baseline is not yet cross-checked against config or source (everything except Bosses of Mass Destruction, Block Factory's Kraken and Infernal Dragon, Eternal Starlight, Remnant's first three and the Dead King), plus the three Ice and Fire dragons at full size (125 days) and Captain Cornelia with their NBT printed to chat as `AOT|NBT|...` lines. Azazel is left out until his fight can be started.
- **SCYLLA DIAGNOSTIC: `/function aot:start_scylla`** (control + Scylla three times, about 5 minutes). Resolves why her baseline was 390 / 18 in runs 1 and 5 but 1024 / 32 in run 4. For each spawn it prints, as `AOT|ENV|` and `AOT|NBT|` chat lines, the weather, time, dimension, player and boss positions and her full `attributes` NBT (which shows every modifier and which mod added it), active effects and NeoForge attachments. Use a **fresh Superflat world**, stand still at spawn, use your normal (not the TEST) Cataclysm config, and send the whole `latest.log`. `aot_parse_log.py` prints a DIAGNOSTICS section and says whether the three baselines are STABLE or VARY.
- **SCYLLA LONG: `/function aot:start_scylla_long`** (control + Scylla twice, 60-second phases, about 7 minutes): same diagnostics as `aot:start_scylla` with a longer window for rare abilities (the spin, the lightning storm). Paired with `cataclysm-common-TEST-scylla-spin.toml` (see `AOT_SCYLLA_ABILITY_TEST.md`).
- **FOCUS: `/function aot:start_focus`** (Scylla, Tyros = `fire_boss`, Obsidilith; about 5 minutes). Used for the config-route test described in `AOT_FOCUS_SCYLLA_TYROS_OBSIDILITH.md`.
- **Everything (18 mods, 55 bosses + control): `/function aot:start`, about 59 minutes.**
- **Quick sample (20 bosses, about 22 minutes): `/function aot:start_quick`**.
- **Investigation run (about 6 minutes): `/function aot:start_rerun`**: Ice and Fire dragons grown to 125 days (full size) plus Captain Cornelia. It prints each boss's Attributes, Health, AgeTicks and other NBT fields into chat (`AOT|NBT|...` lines). Send me the whole `latest.log`.
- **One mod at a time** (each run includes the husk control first, so about 1 minute of overhead):

| Command | Mod | Bosses | About |
|---|---|---:|---:|
| `/function aot:start_twilight` | Twilight Forest | 8 | 10 min |
| `/function aot:start_aether` | The Aether + Deep Aether | 2 | 3 min |
| `/function aot:start_undergarden` | The Undergarden | 1 | 2 min |
| `/function aot:start_alexscaves` | Alex's Caves | 5 | 6 min |
| `/function aot:start_aquamirae` | Aquamirae | 1 | 2 min |
| `/function aot:start_graveyard` | Graveyard | 2 | 3 min |
| `/function aot:start_arsnouveau` | Ars Nouveau | 1 | 2 min |
| `/function aot:start_azazel` | Cult of Azazel (Azazel; may need a ritual) | 1 | 2 min |
| `/function aot:start_cataclysm` | L_Ender's Cataclysm (+ Spellbooks) | 7 | 8 min |
| `/function aot:start_archaion` | Archaion | 1 | 2 min |
| `/function aot:start_fdbosses` | F.D. Bosses | 3 | 4 min |
| `/function aot:start_mowzies` | Mowzie's Mobs | 3 | 4 min |
| `/function aot:start_bomd` | Bosses of Mass Destruction | 4 | 5 min |
| `/function aot:start_blockfactory` | Block Factory's Bosses | 4 | 5 min |
| `/function aot:start_irons` | Iron's Spells 'n Spellbooks | 3 | 4 min |
| `/function aot:start_remnant` | Remnant Bosses (4) | 4 | 5 min |
| `/function aot:start_iceandfire` | Ice and Fire (dragons, 125 days) | 3 | 4 min |
| `/function aot:start_eternalstarlight` | Eternal Starlight | 2 | 3 min |

- Stop at any time: `/function aot:stop`
- **Skip ahead / resume the full run from boss N:** `/function aot:start_from_<N>` (numbers in `AOT_BOSS_INDEX.csv`; the chat lines `AOT|BOSS|N|...|START` show the current number). Example: `/function aot:start_from_33`.
- **Stall watchdog:** if the chain is still on one boss after about 85 seconds, the pack logs `STALL_SKIPPED` and moves to the next boss on its own. It cannot help if the whole game is frozen.

You can split the full run across sessions by doing a few mods per session and sending me each `latest.log` (the game restarts the log each launch, so send it before relaunching).

**Take off any immortality / cheat-death / health-changing items and gear before starting.** They can cancel hits so the pack never counts them, or reset your max health. The pack gives you 1024 max health (the game's cap) and heals you every tick. About 20 ticks after starting it logs `AOT|PLAYER|max=..|hp=..` in chat; max should read 1024.

While it runs: **stay still, stay in survival, do not attack the boss.** The pack makes you very tanky and heals you every tick, and counts each hit you take. **Keep the game window focused** (or press F3+P to turn off pause on lost focus), otherwise the game pauses and the timer stops.

## Not included (on purpose)
No minions, golem or ordinary mobs, and no mini-mobs. Mine Cells and the vanilla bosses (you said unimportant). Mini-bosses I left out of the Cataclysm / Twilight Forest / Alex's Caves lists and the Malkuth warriors. `docs/balance/AOT_ENTITY_CANDIDATES.csv` lists every non-vanilla entity with a drop table in your JARs (724) and whether it is in this test: tell me which ones you consider bosses and I will add them. Unknown ids no longer break the pack (the summon goes through a macro and logs `NO_ENTITY`).

## Finish
When a green "AOT test finished" message appears, quit the game and send me `logs/latest.log` from the instance folder (and a screenshot of any red error text in chat).

## Read the result yourself (optional)
    python tools/aot_parse_log.py "<instance>/logs/latest.log" --csv aot_results.csv
Verdicts per boss: HP = WORKS / CAPPED (rose to the vanilla 1024 limit, health followed) / MAX-ONLY / FAILS / NO-ATTR; DAMAGE = WORKS / SCALES / PARTIAL / FIXED / NO-DATA. The first row is a vanilla zombie control; if it does not show WORKS on both, the whole run is invalid.

## Sampling
The quick run tests 1-3 bosses per mod with different attack styles (all three F.D. Bosses, three Cataclysm bosses). The parser prints a per-mod consistency line; a mod whose samples disagree is marked INCONSISTENT and its other bosses should be tested with the group command. Untested bosses in a consistent mod are recorded as 'sampled', not 'verified'.

## Config-route test (Cataclysm first)
Purpose: show whether a mod's OWN config changes boss stats (separate from the attribute test above). Cataclysm has `health_multiplier` and `attack_multiplier` for all eight bosses, currently 1.0.
1. **Run A (default config):** `/function aot:start_cataclysm` (or reuse the Cataclysm part of `aot:start_needed`). Quit the game and copy `logs/latest.log` somewhere safe as `cataclysm_default.log`.
2. **Swap the config:** with the game closed, replace `<instance>/config/cataclysm-common.toml` with `cataclysm-common-TEST-x2.toml` (renamed to `cataclysm-common.toml`). It is your live file with only the 16 boss multipliers set to 2.0.
3. **Run B:** start the game, same world and datapack, run `/function aot:start_cataclysm` again. Copy `logs/latest.log` as `cataclysm_x2.log`.
4. **Restore** `cataclysm-common-ORIGINAL.toml` as `config/cataclysm-common.toml`.
5. Send me both logs, or run `python tools/aot_compare_runs.py cataclysm_default.log cataclysm_x2.log --hp-mult 2 --atk-mult 2`.
Expected if the config works: base max health x2 (or the 1024 cap), attack attribute x2, hits about x2. The comparison uses only the BASE lines and the pre-modifier hits, so it isolates the config.

## What a verdict means
- **WORKS:** the attribute route edits it; a Dungeon Difficulty rule or Gateways modifier can too.
- **MAX-ONLY (HP):** the attribute moves but the boss's real health does not follow; its code resets or caps health.
- **FIXED / PARTIAL (damage):** some or all attacks use fixed numbers, not the attack-damage attribute.
- **NO-DATA:** the boss never hit you (needs a trigger, ritual or arena): check manually.
- **NO-ENTITY:** the id did not summon (wrong id or mod missing). Boss bars are not measured.
