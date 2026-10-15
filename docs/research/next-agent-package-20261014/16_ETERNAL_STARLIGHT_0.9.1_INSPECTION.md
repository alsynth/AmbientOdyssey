# Eternal Starlight 0.9.1+1.21.1+neoforge: direct jar inspection (14 October 2026)

Source: `eternalstarlight-0_9_1_1_21_1_neoforge.jar` uploaded by the owner (mod id `eternal_starlight`, MIT, author LeoLezury, 11,066 files). Replaces "never scanned". The earlier upload `eternal_starlight_delight` was a different mod (a Farmer's Delight addon).

## Dimension and structures
- Own dimension `eternal_starlight:starlight` (+ dimension type). 8 structures, 8 structure sets, 9 template pools, 24 structure templates, 23 biomes.
- **Biome tags decide where each structure generates:**
  - `golem_forge`, `cursed_garden` (landmark placement, tag `boss_landmarks`) and `stranghoul_den` generate **only in Eternal Starlight biomes**: not in the Overworld.
  - `portal_ruins_cold|common|desert|forest|jungle` generate in the **Overworld** (tags `#c:is_cold/overworld`, `#c:is_plains` + `#c:is_savanna`, `#c:is_desert` + `#c:is_badlands`, `#c:is_forest`, `#c:is_jungle`). Native placement 36/30; **AO's Cristel config sets 45/32** (all eight structures are enabled).

## Boss to structure map (from the template block palettes)
| Boss | Spawner block | Found in | Dimension |
|---|---|---|---|
| The Gatekeeper | `the_gatekeeper_spawner` | all 5 `portal_ruins` templates | **Overworld** |
| Starlight Golem | `starlight_golem_spawner` | `golem_forge/room/boss` | Eternal Starlight |
| Permafrost | `permafrost_spawner` | `golem_forge/room/permafrost` | Eternal Starlight |
| Lunar Monstrosity | `lunar_monstrosity_spawner` (block exists) | **in no template**: placed by code, so the Cursed Garden is an inference | Eternal Starlight |
No template contains placed entities; bosses are placed by these custom spawner blocks. `tangled` is an ordinary mob, not a boss. The portal block is `starlight_portal`, the Gatekeeper has trade logic and a `challenge_gatekeeper` advancement: the Overworld ruins very likely gate entry to the dimension (not verified in game).

## AO live config (`config/eternal_starlight.json`)
Gatekeeper HP 175 / armor 15; Starlight Golem 200 / 10 (`attackDamageScale` 1.0); Permafrost 120 / 10 (`attackDamageScale` 1.0); Lunar Monstrosity 200 / 12 (`attackDamageScale` 1.0). **`enableBossRespawn` true, `bossRespawnCooldown` 36000 ticks (30 minutes)**: bosses can be re-fought, relevant to the repeatable-reward concern. `spawnInEternalStarlight` and `respawnInEternalStarlight` are false.

## What "boss respawn" does (read from the class constants of `ESBoss` and `ESConfig`; not run in game)
When a boss is defeated (`ESBoss.bossDefeat`), and `enableBossRespawn` is true, the game looks up the boss's own **spawner block** (`getBossSpawnerForRespawn`) and sets its spawn cooldown to `bossRespawnCooldown` ticks (36000 = 30 minutes), after which that spawner can produce the boss again. The kill also increases the player's boss challenge count, triggers the kill advancement and rolls the boss loot table (`bosses/<boss>`), so **each respawn is another reward roll.** Not known from the constants: whether the cooldown only runs while the chunk is loaded or a player is near. It is a config value, applied when a boss dies: it does not affect world generation and can be changed after pregeneration. (`spawnInEternalStarlight` and `respawnInEternalStarlight` are about players, not bosses.)
