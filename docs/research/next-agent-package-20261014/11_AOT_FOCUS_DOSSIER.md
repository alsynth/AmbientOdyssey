# Focus dossier: Scylla, Tyros, Obsidilith (editability)

13 October 2026. Evidence letters: C = live config key and value, S = upstream source read, J = real JAR scan, R = in-game AOT run. **Nothing about the mods' own config routes has been run in game yet**; the focus test below does that.

**Which entity is Tyros?** `irons_spellbooks:fire_boss`. The Tyros config (`Boss Config.Tyros.*`) is read in `FireBossEntity` (source). The Citadel Keeper is a different mob and is not Tyros.

| | Scylla (`cataclysm:scylla`) | Tyros (`irons_spellbooks:fire_boss`) | Obsidilith (`bosses_of_mass_destruction:obsidilith`) |
|---|---|---|---|
| **Base HP** | 1024 at spawn (R, run 4; the old unset-up summon read 390) | 1000 (R; matches source) | 300 (C and R, equal) |
| **HP edit routes** | config `combat_config.health_multiplier` (1.0) (C); attribute route is already at the 1024 cap, so it can only lower HP (R) | config `additionalHealth` (0.0), applied as an attribute modifier at spawn (S); the 1024 cap leaves +24 | config `obsidilithConfig.health` (300.0) (C); attribute route works up to 1024 (R) |
| **Damage edit routes** | config `attack_multiplier` (1.0) and five absolute per-attack keys: spear 14, lightning storm 10, lightning area 4, snake 16, anchor 16 (C) | config `additionalAttackDamage` (0.0) and `additionalSpellPower` (0.0) (S); attribute route works: attack attribute 20 to 80, exactly x4 (R) | config `obsidilithConfig.attack` (16.0) and `anvilAttackExplosionStrength` (4.0) (C); attribute route works: attack 16 to 64, hits x4.28 (R) |
| **Measured attribute result** | **Attack attribute stuck at 32 after +300%** (32 to 32); hits only x1.36, PARTIAL. Ignis and the Ender Guardian also ended at exactly 32: probably a Cataclysm ceiling (unverified). An older run showed x3.97 but on a boss that had skipped spawn setup | Hits x2.44 (mixed attacks) | Hits x4.28 WORKS; HP 300 to 1024 (capped, needs 1200 for x4) |
| **Abilities / phases** | `weather_change` toggle, `nature_heal` 25, `ignore_mobgriefing`, `respawner`; percent-of-HP attacks `hp_damage` 0.05, `spin_hp_damage` 0.07, `lightning_storm_hp_damage` 0.04 (C) | damage derives from the attack attribute (eruptions x1, x2, x3; fireball x12) and spells from spell power (S); experimental `tyrosOminousEnabled` ominous fight (C) | `idleHealingPerTick` 0.5, `armor` 14, `spawnPillarOnDeath` (C) |
| **Multiplayer** | caps `damage_cap` 21 and `dps_cap` 13 limit damage taken by the boss per hit and per window (C; semantics from the key names) | built in: extra HP of 40% per extra player plus 10% per extra player squared within 60 blocks (S). At 5 to 7 players that asks for x4.2 to x7, **but base HP 1000 is already at the 1024 cap, so it has almost no effect here** | none found |
| **Drops** | data loot table `cataclysm:entities/scylla`: Essence of the Storm, Lacrima, music disc (J); datapack override | four data tables: `fire_boss`, `_ominous`, `_per_player`, `_per_player_ominous` (J), plus per-participant loot in code (S) | arena chest `bosses_of_mass_destruction:chests/obsidilith` (obsidian heart, obsidian, purpur) (J); XP `experienceDrop` 1000 (C) |

## Update after the Scylla diagnostic (run 6), replacing the earlier caveat
Her baseline is **stable at 390 HP / attack 18 / armor 12** across three clean spawns and runs 1 and 5, with no modifiers from any other mod and clear weather. The 1024 / 32 read in run 4 is an **unexplained outlier**; the statements above about a ceiling of 32 and a base HP at the cap should be read as describing run 4 only.
The attribute route **does work** on her (attack 18 to 72 in every spawn), **but only for part of her damage**: melee-style hits grow about x3.4, while the absolute-damage abilities (16, 14, 9, 4: matching `snake_damage`, `anchor_damage`, `spear_damage`, `lightning_area_damage`) stay fixed and the percent-of-max-HP hits (`spin_hp_damage`, `hp_damage`) are not scaled either. So Scylla is **mixed** (confirmed in run 7: spear, snake/anchor, lightning-area and `hp_damage` each follow their own config key exactly; the melee family is exactly 2 x the attack attribute; the spin and lightning storm are still unconfirmed; her **wave** (a constant 9.0 hit in pulses 0.5 s apart) has no known lever so far): attribute for the melee part, config keys for the rest (`AOT_SCYLLA_ABILITY_TEST.md`, the next test, checks that mapping).

## Verdict so far
- **Obsidilith: best supported.** Both routes exist and the attribute route measured cleanly; only HP is limited by the 1024 cap.
- **Tyros: strongly editable**, with the best evidence (source). Damage and spell power are editable; HP is effectively fixed at its cap, and the mod's multiplayer HP scaling is neutralised by that cap. Scale it through damage and spell power, not HP.
- **Scylla: editable through her config, not through attributes.** Her attack attribute does not move past 32 and her base HP is already the cap. HP can only go down; damage needs `attack_multiplier` or the per-attack keys. **Untested.**

## Design consequence
All three sit near or at the 1024 HP ceiling, so a harder fight has to come from damage, spell power, mechanics and add-ons, not HP, unless a mod raising the attribute cap (AttributeFix style) is added.

## Focus test (about 10 minutes of play, two runs)
Files: `cataclysm-common-TEST-scylla.toml` (Scylla health x0.5, attack x2), `irons_spellbooks-server-TEST-tyros.toml` (Tyros additionalHealth -500, additionalAttackDamage +10), `bosses_of_mass_destruction-TEST-obsidilith.json5` (Obsidilith health 600, attack 32), each with an `-ORIGINAL` copy, and `focus_expect.json`.
1. **Run A (default configs):** `/function aot:start_focus` (4 slots, about 5 minutes). Quit; copy `logs/latest.log` as `focus_default.log`.
2. **Swap configs** (game closed): put the three TEST files in `config/` under the original names (`cataclysm-common.toml`, `irons_spellbooks-server.toml`, `bosses_of_mass_destruction.json5`). **Iron's server config:** if `saves/<world>/serverconfig/irons_spellbooks-server.toml` exists, replace that one too (NeoForge normally reads server configs from there; AO ships the file in `config/` and `defaultconfigs/` holds only one other server file).
3. **Run B:** start the game, same world, `/function aot:start_focus`. Quit; copy `latest.log` as `focus_changed.log`.
4. **Restore** the three ORIGINAL files.
5. `python tools/aot_compare_runs.py focus_default.log focus_changed.log --expect-json focus_expect.json`, or send me both logs.
Expected if a config route works: Scylla base HP 1024 to 512 and hits about x2; Tyros base HP 1000 to 500 and attack attribute +10; Obsidilith HP 300 to 600 and attack 16 to 32. **If Tyros does not change, the file in `config/` is being ignored** and the world's `serverconfig/` copy is the one that counts.
