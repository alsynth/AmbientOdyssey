# Compatibility evidence (DRAFT)

Static evidence only (the live config snapshot, the installed jars and earlier measurements). **Nothing here was run as a combined fight.**

## 1. Dungeon Difficulty

Its three AO rules (`ao_patrol`, `ao_dungeon`, `ao_trial`) match hostile entities by a pattern that lists **vanilla** mob types (zombie, husk, drowned, skeleton, blaze, piglin_brute and others) plus a few named mods, and **excludes any name containing boss, king, queen, lord, guardian, monarch, chieftain or warlord**. I tested every Tier 6 to 9 entity id against it: **34 of 34 do not match, so Dungeon Difficulty does not scale them**; the exceptions would be listed below.
Matching entities: none. Vanilla-type Brutal Bosses and minions that are vanilla zombies or skeletons *can* match inside its zones (accepted by the owner for Brutal Bosses).
Zones with a level: `dungeoncrawl:dungeon` (ao_dungeon 2), `adventuredungeons:trialrooms` (ao_trial 2), `dungeons_arise:illager_fort` (ao_patrol 2), `keep_kayra` and `plague_asylum` (ao_dungeon 3), `irons_spellbooks:catacombs` (ao_dungeon 2). Per level the rules add 10 to 14% max health, 5 to 8% damage and 0.4 to 0.5 armor.

## 2. Apotheosis and Apothic Attributes

- Apotheosis's own `bosses` settings concern its **own invading bosses** (spawn cooldown 3600 ticks, announcement range 140); they do not scale other mods' bosses. Apothic Spawners does not touch bosses.
- **Apothic Attributes' combat rules apply to every damage event**, including boss fights: armor, protection and crit formulas are replaced. Quoted from the live file:

```
combat_rules {
    # The protection damage reduction formula.
    # Computed after Prot Pierce and Prot Shred are applied.
    # Arguments:
    #     'protPoints' - The number of protection points the user has after reductions.
    # Output:
    #     The percentage of damage taken after protection has been applied, from 0 (no damage taken) to 1 (full damage taken).
    # Reference:
    #     See https://github.com/ezylang/EvalEx#usage-examples for how to write expressions.
    # 
    # Default: 1 - min(0.025 * protPoints, 0.85)
    S:"Protection Formula"=1 - min(0.025 * protPoints, 0.85)
    # The a-value formula, which computes an intermediate used in the armor formula.
    # Arguments:
    #     'damage' - The damage of the incoming attack.
    # Output:
    #     The a-value, which will be supplied as an argument to the armor formula.
    # Reference:
    #     See https://github.com/ezylang/EvalEx#usage-examples for how to write expressions.
    # 
    # Default: if(damage < 20, 10, 10 + (damage - 20) / 2)
    S:"A-Value Formula"=if(damage < 20, 10, 10 + (damage - 20) / 2)
    # The armor damage reduction formula.
    # Computed after Armor Pierce and Armor Shred are applied.
    # Arguments:
    #     'a' - The a-value computed by the a-value formula.
    #     'damage' - The damage of the incoming attack.
    #     'armor' - The armor value of the user after reductions.
    #     'toughness' - The armor toughness value of the user.
    # Output:
    #     The percentage of damage taken after armor has been applied, from 0 (no damage taken) to 1 (full damage taken).
    # Reference:
    #     See https://github.com/ezylang/EvalEx#usage-examples for how to write expressions.
    # Note:
    #     The vanilla formula is: 1 - min(max(armor - damage / (2 + toughness / 4), armor / 5), 20) / 25
    # 
    # Default: a / (a + armor)
    S:"Armor Formula"=a / (a + armor)
    # The armor toughness formula.
    # This is used to determine how armor toughness impacts enemy Armor Pierce / Armor Shred.
    # Arguments:
    #     'damage' - The damage of the incoming attack.
    #     'armor' - The armor value of the user after reductions.
    #     'toughness' - The armor toughness value of the user.
    # Output:
    #     The percentage by which enemy armor pierce/shred will be reduced, from 0 (no change) to 1 (preventing it completely).
    # Reference:
    #     See https://github.com/ezylang/EvalEx#usage-examples for how to write expressions.
    # 
    # Default: min(toughness * 0.02, 0.6)
    S:"Armor Toughness Formula"=min(toughness * 0.02, 0.6)
    # T
```

- *Not assessed:* how Apotheosis-affixed player gear interacts with each boss's damage types, and any Apotheosis scaling of boss loot (the reward work covers loot).

## 3. Tyros already has an addon layer

The **Stronger Fire Boss** addon (`strongerfireboss-2.0.0`, config/strongerfireboss-common.toml) buffs the Fire Boss: soul-mode damage limiter True (cap 0.01 of max health per hit, overflow multiplier 0.3), Sharpness V on his weapon True, Rend on dagger attacks True. Any Tyros balance must account for it.

## 4. Original and Integrated arena variants

63 resources of the Tier 6 to 9 arenas are defined by both an original mod and its Integrated variant (Cataclysm vs `integrated_cataclysm`, BOMD vs IBOMD). The snapshot picks the Integrated one, the handoff says to keep it, **runtime precedence is unverified** (`/datapack list enabled`).

## 5. Limits and caps

- Health: every boss that was raised stopped at **1024** (measured). Armor: the Bosses'Rise config states a maximum of 30; whether Apothic Attributes lifts it is unverified.
- Melee damage scales with the attack attribute; fixed-damage and percent-of-health abilities do not (Scylla measured; assumed for other Cataclysm bosses by owner decision).

## 6. Respawn, repeatability and exploits

- **Eternal Starlight:** boss respawn on, 36000 ticks; each kill rolls the loot table (from class constants, not run).
- **Remnant Bosses:** ritual summon with materials; no respawn mechanism found in the jar.
- **F.D. Bosses:** `bossesDespawn` false; damage multipliers by game difficulty (0.5 / 0.75 / 1.0 / 1.25).
- **Brutal Bosses:** created at world generation (see its findings).
- *Not assessed:* boss health regained after a party wipe, summon exploits, and performance of particles, summons and projectiles.

## 7. Configuration caveats

- `irons_spellbooks-server.toml`, `block_factorys_bosses-server.toml` and `cataclysm_spellbooks-server.toml` are **SERVER-type** files: whether AO's values in `config/` apply in a newly created world is unverified (the owner's check is pending). The measured Sandworm and Underworld Knight baselines equal the shipped config values, which suggests they apply, but that is not proof.
- Remnant Bosses saves its config through JAUML into `config/remnant/`; one Windows file-lock error at startup was seen once and is local.

## 8. Multiplayer

No native player-count scaling was found in the configs read. Scaling by nearby players is **not assessed**.
