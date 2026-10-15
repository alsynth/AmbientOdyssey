# Brutal Bosses: findings (13 October 2026)

**Evidence.** Read from the author's source, branch `neo1.21` of `someaddons/dungeonbosses` (version **8.5**, 20 Feb 2026) and his creation guide (gist, revised 19 Feb 2026). The installed jar is **8.6** (`brutalbosses-1.21.1-8.6.jar`), which I could not read. **Nothing here has been run in Minecraft.** Where behaviour matters I say so and give a two-minute test.

## 1. How it works
- Every boss is **one JSON file in `data/brutalbosses/bosses/`**; a datapack with a same-named file overrides it. 29 default bosses plus `dummyboss` (a placeholder that spawns nothing and only dilutes spawn weights).
- Each boss is a **vanilla (or modded) entity** with a boss bar, custom stats, gear and extra AI goals. `/brutalbosses spawnboss <file>` spawns one at the command's position; `all` and `random` also exist.
- **Spawning:** when a structure generates a lootable container whose loot table appears in a boss's `spawnatchest`, the global chance (default **30%**) is rolled, then a boss is picked by weight among the bosses listed for that table. A boss will not spawn within `minDistance` (default **100** blocks) of another.
- **Loot:** the boss drops items from the loot table of the chest it spawned beside (`droppeditemamount`, default 3), plus gear if `dropgear` is set, plus `experience`.

## 2. What is editable (all by datapack, per boss)
`attributes` (health max 1024, attack damage max 2048 and melee only, armor, speed, follow range, knockback resistance), `effects` (permanent potion effects), `customattributes` (`attack_speed`, `projectile_damage_bonus`, `dropgear`), `gear`, `experience`, `visualscale`, `name`, `showbossbar`, `protect_treasure`, `droppeditemamount`, `entitynbt`, `spawnatchest` (tables and weights) and the AI goals with their parameters, each limitable to health phases (`healthinterval`, e.g. `"100-50;30-0"`).
**Damage levers per attack** (from the guide and the defaults): melee = `generic.attack_damage` (only set on 11 of 29 bosses; the others use the entity's vanilla value, and the attribute can be added); `meleehit.damage`, `whirlwind.extradamage`, `jumpattack.extraDamage` (extra on top of melee); `itemshootgoal.damage` (magic damage of thrown items); `projectile_damage_bonus` for thrown projectiles. The fireball/skull goals have projectile counts, intervals and distances but no damage field (their damage is the vanilla projectile's).
Ability spelling: use **`brutalbosses:whirlwind`** (the shipped defaults); the guide's `whirldwind` is a typo.

## 3. Global config (`config/brutalbosses.json`, AO ships the defaults)
| Key | Default | What the 8.5 source does |
|---|---|---|
| `damageMultiplier` | 1.0 | adds a transient multiplier `damageMultiplier - 1` to **max health AND attack damage** of every boss (a copy-paste in `BossType`), and multiplies **thrown-projectile** damage (`itemshootgoal` and the thrown damage event) |
| `healthMultiplier` | 1.0 | **read but never used** anywhere in the code: it does nothing |
| `globalBossSpawnChance` | 30 | percent chance per eligible chest |
| `minDistance` | 100 | blocks between bosses |
| `printChestLoottable` | false | prints the loot table of each chest you open (for adding spawns) |
So there is **no independent global health lever**, and the one global "damage" lever also changes health. This is the 8.5 source; 8.6 may have fixed it.

## 4. The 29 default bosses (`BRUTAL_BOSSES_DEFAULTS.csv`)
All have **40 to 150 max health (median 80)**; melee attack is explicit only on 11 (3 to 10). Abilities most used: `aftercombatregen` (20 bosses), `whirlwind` (10), `chasetarget` (7), `charge` (7), `itemshootgoal` (6), `shootwitherskulls` (5). Toughest: `skeletonshieldboss` 150, `irongolemboss` 140, `witherskeletonshieldboss` 120. These are an **early to mid dungeon-boss layer**, far below Cataclysm's 390 to 1024.

## 5. Where they appear in AO (`BRUTAL_BOSSES_AO_CHEST_COVERAGE.csv`)
The defaults list **462 loot tables in 52 namespaces** (vanilla, Dungeons Arise, Repurposed Structures, IDAS, Philip's Ruins, Dungeons Enhanced, Nova Structures and others). Of the **1,266 chest tables in the 93 mods I scanned**, **146 (about 12%)** have a Brutal Boss. Covered: vanilla dungeons, Dungeons Arise (48 of 141), IDAS (16 of 162), Graveyard (18 of 44), Dungeons and Taverns (29 of 136). **Not covered:** Integrated Villages (1 of 151), Aether (0 of 21), Dimensional Dungeons (0 of 23), Adventure Dungeons (0 of 21), the Moog structures, Iron's Spellbooks and Artifacts chests. New structure mods added to AO (Create, Archaion, Explorify, Additional Structures and so on) have none either until their tables are added.

## 6. Not verified
- Whether 8.6 still has the `damageMultiplier` health coupling and the dead `healthMultiplier`.
- That the 1.21.1 jar behaves as the 8.5 source (gear strings use the `{id: "...", Count: 1b}` form there).
- Real damage numbers per attack (this research has no hit measurements for these bosses; vanilla-entity attributes are known to scale, as the husk control shows ×4).

## 7. Two-minute check of the global multipliers (manual, no datapack)
1. In `config/brutalbosses.json` set `damageMultiplier` to **2.0** and `healthMultiplier` to **3.0**; restart the game.
2. Creative Superflat: `/brutalbosses spawnboss zombieboss` (default 100 HP, attack 10).
3. `/attribute @e[type=minecraft:zombie,limit=1,sort=nearest] minecraft:generic.max_health get` and the same with `minecraft:generic.attack_damage`.
Reading: **200 and 20** means `damageMultiplier` scales both and `healthMultiplier` is dead (as in 8.5); **300 and 20** means health is fixed in 8.6; **100 and 10** means the config is not applied at all. Restore the defaults afterwards.

## 8. Owner decisions (13 October 2026)
- **`globalBossSpawnChance` 30 to 70** and **`minDistance` 100 to 30.** Recorded here, **not applied to the release source** (`release_030/overrides/config/brutalbosses.json` is unchanged on this research branch); a ready file with only those two values changed (comments and line endings kept) was handed over as `brutalbosses.json`.
  Effect to expect: a boss roll per eligible chest rises from 30% to 70% (about 2.3 times as many), and with 30 blocks of spacing a large multi-chest dungeon can hold several bosses (one per 30-block radius). The check compares only the last 20 spawns, so the spacing is not strict. Since these bosses have 40 to 150 HP the density is mainly a loot and pacing question, not a danger one.
- The owner reported the two-minute multiplier check from section 7 **worked**; the readings were not given, so the question of whether 8.6 still couples `damageMultiplier` to health stays open until they are.
- **Coverage is enough** (owner): no loot tables will be added; the roughly 12% of AO chest tables that have a boss stay as they are.
- **Multiplier check result (owner):** with a factor of **10** set in `config/brutalbosses.json` the zombie boss (default 100 HP) came out at **1000 HP**. This fits two different explanations and the report did not say which key was set to 10 nor what the attack damage read: (a) `healthMultiplier` works in 8.6, or (b) `damageMultiplier` still scales health as in the 8.5 source. **Open until the owner says which key it was and the attack reading.**
- **Cap to remember:** max health is limited to 1024, so a factor of 10 reaches the cap on any boss above 102 HP (the toughest default, `skeletonshieldboss`, has 150, so it caps at about x6.8).

### Multiplier check, final reading (owner)
Both `healthMultiplier` and `damageMultiplier` were set to **10**: the zombie boss came out at **1000 HP** and its damage was scaled correctly too (about x10). This is **consistent with both explanations** (an independent `healthMultiplier` in 8.6, or the 8.5 coupling of health to `damageMultiplier`), because the two give identical numbers when both keys are equal. **Practical rule: always set both keys to the same value; the result is then the same under either version.** Only if HP and damage must be scaled by different global factors does the difference matter (a re-run with `damageMultiplier` 2 and `healthMultiplier` 5 would show it: 200 HP means coupled, 500 HP means independent).

### What a global factor does (health capped at 1024)
| Factor | Weakest (40 HP) | Median (80) | Toughest (150) | Bosses at the cap |
|---|---|---|---|---|
| x1 | 40 | 80 | 150 | 0 of 29 |
| x2 | 80 | 160 | 300 | 0 |
| x3 | 120 | 240 | 450 | 0 |
| x4 | 160 | 320 | 600 | 0 |
| x5 | 200 | 400 | 750 | 0 |
| x6 | 240 | 480 | 900 | 0 |
| x8 | 320 | 640 | 1024 | 2 |
| x10 | 400 | 800 | 1024 | 5 |
Up to x6 no boss reaches the cap and the ordering between bosses is kept.
**Damage:** the factor multiplies the boss's attack-damage attribute (which melee, `meleehit` and `jumpattack` add to their own fixed extra, so those scale only in their attribute part) and thrown-projectile damage. It does **not** scale the fixed extras (`extradamage`, `meleehit.damage`) or the vanilla damage of fireballs and wither skulls. Bosses without an explicit attack value use their entity's vanilla attack, which the factor also multiplies.

## 9. What decides how strong a Brutal Boss is (source + AO config; nothing random per spawn)
1. **Which boss:** random, weighted by the loot table of the chest (a boss listed with weight 5 against one with weight 3 is chosen 5/8 to 3/8). The `dummyboss` is part of that pool and means "no boss", so the **real chance per chest is lower than `globalBossSpawnChance`**: at 70% the median table gives about **20%** (mean 22%, range 3 to 70%); only tables without a dummy entry (for example Woodland Mansion, End City, Bastion) reach the full 70%. At the old 30% the median was 9%. Overriding `dummyboss.json` with fewer entries is the lever.
2. **The boss file:** fixed stats (health, attack, armor, effects, gear, abilities). Nothing in the code scales them by difficulty, player count, depth, distance or randomness.
3. **The global multipliers** in `config/brutalbosses.json` (see section 3).
4. **Dungeon Difficulty (AO config), only in six structures:** `dungeoncrawl:dungeon` (ao_dungeon level 2), `adventuredungeons:trialrooms` (ao_trial 2), `dungeons_arise:illager_fort` (ao_patrol 2), `keep_kayra` (ao_dungeon 3), `plague_asylum` (ao_dungeon 3), `irons_spellbooks:catacombs` (ao_dungeon 2). Per level the rules add +10 to 14% max health, +5 to 8% damage and +0.4 to 0.5 armor. Their entity pattern lists vanilla types (zombie, husk, vindicator, evoker, witch, piglin_brute and others) that Brutal Bosses are built from, so a boss spawned inside one of those zones is probably scaled too (**not verified in game**; the attribute modifiers of such a boss would show it).
5. **The game difficulty setting** (Easy/Normal/Hard) changes how much damage mobs deal to players, as for any mob.

## 10. Going past the 1024 health cap
The cap is the game's own limit on the max-health attribute; Apothic Attributes does not lift it (the Cataclysm tests also stopped at 1024). Options, cheapest first:
- **Armor, using AO's formula.** Apothic Attributes replaces the vanilla armor rule with `a / (a + armor)` (configurable in `apothic_attributes.cfg`), where `a` is 10 for hits under 20 damage and `10 + (damage - 20) / 2` above. Effective-HP multiplier of the boss:

| armor | hit 10 | hit 30 | hit 60 | hit 100 | hit 200 |
|---|---|---|---|---|---|
| 10 | x2.0 | x1.7 | x1.3 | x1.2 | x1.1 |
| 20 | x3.0 | x2.3 | x1.7 | x1.4 | x1.2 |
| 30 | x4.0 | x3.0 | x2.0 | x1.6 | x1.3 |
| 50 | x6.0 | x4.3 | x2.7 | x2.0 | x1.5 |
| 100 | x11.0 | x7.7 | x4.3 | x3.0 | x2.0 |
  Armor is strong against small hits and weak against the big hits of a high-tier player, **by design of that formula**, and the vanilla armor cap is 30 (whether it is lifted here is unverified; check with `/attribute <boss> minecraft:generic.armor base set 100` then `get`).
- **Potion effects in the boss file:** `resistance` (vanilla 20% per level, so level 3 to 4 is 60 to 80% less damage, a flat x2.5 to x5 at any hit size) and `absorption` (an extra health pool that is not capped by max health). The `temppotions` ability can re-apply them in health phases as a shield that comes back. The level-versus-amplifier numbering in the guide is unclear: test it.
- **Regeneration:** `aftercombatregen`, the `regeneration` effect.
- **A small addon (not built) that reduces incoming damage to chosen bosses by a factor:** the only way to get a true effective HP above 1024 at every hit size, and the same addon could scale boss damage that no attribute or config reaches (Scylla's wave, Hydra, Ur-Ghast). The boss bar would still show 1024.

## 11. Owner observation (13 Oct 2026)
The owner reports that the global settings seem to respond **only to what is changed** (health to the health setting, damage to the damage setting). That points to `healthMultiplier` being independent in 8.6, but the details were not given, so it is recorded as an observation, not as verified.

## 12. Owner decisions (13 Oct 2026, later)
- The dummy boss dilution is **accepted**: no override of `dummyboss.json`. The intent of raising the chance was only to see these bosses somewhat more often.
- Dungeon Difficulty also scaling Brutal Bosses inside its six zones is **accepted**.
- Open question from the owner: would a damage-scaling addon, added to an existing world after a boss already exists, still affect that boss? Answer given: yes if the addon works on damage events, which act on every hit regardless of when the boss was created; only changes applied once at spawn would miss it (not built, not tested).

## 13. What must be frozen before world pregeneration (source reading of 8.5, not run in game)
A Brutal Boss is **created during world generation**: a mixin on `RandomizableContainerBlockEntity.setLootTable` (and `applyImplicitComponents`) rolls the spawn when a structure's chest gets its loot table, and the boss entity is added to the world right then.
- **Baked in by pregeneration (freeze first):** `globalBossSpawnChance` (owner: 70), `minDistance` (30), every boss's `spawnatchest` tables and weights, the `dummyboss` entries, and the boss file names/ids (an existing boss whose id no longer exists logs `Could not find boss for id` and is not initialised).
- **Can still be changed after pregeneration:** health, attack, armor, effects, gear and ability parameters in the boss files, and the global `damageMultiplier` / `healthMultiplier`. When a saved boss is loaded, its capability is deserialised and `initForEntity` re-applies gear, stats and AI from the current definitions (config multipliers are read at startup, so a restart is needed). Changing a boss's `entity` type does not change entities that already exist.
- A damage-event addon (not built) adds nothing to world generation and can be added after pregeneration.
