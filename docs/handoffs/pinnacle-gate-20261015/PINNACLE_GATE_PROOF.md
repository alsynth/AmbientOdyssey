# Pinnacle gate — grant-chain proof and source fix (15 October 2026)

> **SUPERSEDED IN PART (owner decision, 15 Oct 2026, branch `feature/pinnacle-cornelia`):** Pinnacle = the native five epic gear pieces **plus a Captain Cornelia kill**, which replaces the native Ender Dragon kill. The "delete the gate, native unlock stays in charge" fix below is replaced by a new `ao_campaign_gates` override. See **[Cornelia Pinnacle requirement](#cornelia-pinnacle-requirement-15-oct-2026)** at the end. The R4 grant-chain proof below remains valid history. The R5-toolchain gate removal was never done, so there is nothing to adjust there.

**Result:** In R4, Apotheosis Pinnacle **cannot be earned in normal play**. The only route is an operator running `/advancement grant … apotheosis:progression/pinnacle`. Source fix removes the gate so the native Apotheosis requirement applies again. Status: **SOURCE IMPLEMENTED + STATIC TEST PASS**. Not packaged, not engine-tested, not multiplayer-tested.

## Evidence (R4 ZIP SHA256 `31b037a7…6c6d`, installed Apotheosis 8.9.0 = R4 pin)

| Source | What it says |
|---|---|
| R4 `overrides/config/paxi/datapacks/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json` (SHA256 `9de71607…2bad`) | Replaces all criteria with one `strong_t6: minecraft:impossible`. Text: "Defeat the Dead King or the experimental alternate Kobolediator to unlock Pinnacle." |
| Native `Apotheosis-1.21.1-8.9.0.jar` → `data/apotheosis/advancement/progression/pinnacle.json` | Requires epic+ affixed helm, chest, legs, feet, hand (`apotheosis:equipped_item`) **and** `kill_ender_dragon`. Same pattern as haven → frontier → ascent → summit. |
| Native `Apoth$Advancements.class` | World Tier unlocks are keyed to `progression/haven…pinnacle` advancements. |
| R4 campaign 0.3.2 JAR (SHA256 `802461a6…39b7`) | No class or resource references `progression/pinnacle`, `PINNACLE` or `getUnlockAdvancement`. `grant()` is only called for `ao_campaign:milestones/*`. |
| Campaign source `AOCampaign.java` | Comment: "native World Tier unlocks remain authoritative." Unused `import …tiers.WorldTier` left over. |
| Other 9 R4 custom JARs, all 330 installed CF mod JARs, all R4 config/quest files | No override of, or reference to, `apotheosis:progression/pinnacle`. Only R4 config file containing `minecraft:impossible` is the gate itself. |

## History (why it broke)
1. `ed1a299` (PR57, 14 Oct) added **both** the Paxi gate and a code grant: on a T6 boss kill, `AOCampaign` awarded `WorldTier.PINNACLE.getUnlockAdvancement()`.
2. `01c2c58` (15 Oct) removed the code grant per the owner decision (native unlocks authoritative), but **left the Paxi gate**. R2, R3 and R4 all shipped it.

Grant chain in R4: **none.** `minecraft:impossible` is satisfied only by `/advancement grant` (operator) or code; no code grants it.

## Intent check
- Superseded intent: `docs/balance/V050_BOSS_ROSTER_AND_GATES_PROVISIONAL.md`, `V050_LOOT_GEAR_ECONOMY_PROVISIONAL.md`, `docs/questing/V050_QUEST_CAMPAIGN_BLUEPRINT_PROVISIONAL.md` (13 Oct, "provisional") describe a strong-T6 Pinnacle unlock.
- Binding latest: canonical handoff §5 item 11 ("PR57 automated Pinnacle unlocking … superseded/disabled. Do not restore"), §4 Gems row ("no … automatic Pinnacle unlock in R3/R4"), R2–R4 package notes ("Pinnacle auto-unlock … removed"), and the owner instruction of 15 Oct: native Apotheosis unlocks stay in charge.
- So the gate contradicts the latest decision. It is not intentional in R4.

## Fix (this branch)
- Deleted `release_030/experimental_overlays/v050/overrides/config/paxi/datapacks/ao_campaign_gates/` (2 files). The overlay copy loop in `tools/package_ao_full_pr54.py` now copies no Paxi pack from that overlay.
- Added both paths to `docs/handoffs/integration-20261015/removed-source-paths.json`, so `tools/package_master_integration.py` also pops them from any inherited payload.
- New `tests/test_no_impossible_tier_gates.py` (5 tests):
  - No source overrides `apotheosis:progression/*`.
  - Every advancement with `minecraft:impossible` must be granted in `AOCampaign.java`; the 9 campaign milestones pass.
  - The campaign doesn't use `WorldTier.`/`getUnlockAdvancement`.
  - The gate files are gone and recorded as removed.
- Other gates checked: the 9 `ao_campaign:milestones/*` files use `minecraft:impossible` **intentionally**. Each is granted by code: `tier_<n>` and `tyros`/`scylla`/`obsidilith` on a boss kill, `heirloom_upgrade` by `/ao_mastery upgrade`. No other gate file exists.

## Rollback (exact)
`git revert <this commit>`, or restore the two files byte-exact from `3806fa1`:
- `…/ao_campaign_gates/pack.mcmeta` SHA256 `df2d65815abd6c30dbb3cd632e5a638581e3c5655eb3f1965222efea9027603c`
- `…/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json` SHA256 `9de71607ca79fd3e063ed1c48b6b0982dda48a1642a7b54a4123a685ea562bad`

and remove the two added lines from `removed-source-paths.json`. R4 ZIP itself is unchanged.

## Remaining
- **Engine test:** in a fresh world from the next build, confirm `/advancement` shows native Pinnacle criteria and that equipping five epic affixed pieces plus a dragon kill unlocks the Pinnacle World Tier.
- **R5 packager:** `tools/package_r5_grand_from_r4.py` copies all R4 bytes except the campaign JAR and manifest, so an R5 built with it would still contain the gate. It needs an owner OK to drop these two members there too.
- The unused `WorldTier` import can be removed at the next real Java build. It was left untouched because nothing can be compiled here (no Gradle).

---

## Cornelia Pinnacle requirement (15 Oct 2026)

**Result:**
- Pinnacle now needs the native five epic-or-better gear pieces plus a kill of `aquamirae:captain_cornelia`.
- The override is generated from the native file, and only 3 lines differ.
- No `minecraft:impossible` remains anywhere in the shipped config.
- Status: **SOURCE IMPLEMENTED + STATIC TEST PASS** (13/13). A packager dry run includes it. Not engine-tested, not multiplayer-tested.

### 1. Native requirement (Apotheosis 8.9.0, JAR SHA256 `23a8b4a2…872e`, file SHA256 `d456b49d…9f62`)
- `data/apotheosis/advancement/progression/pinnacle.json`, parent `apotheosis:progression/summit`.
- Five criteria `epic_helm|epic_chest|epic_legs|epic_feet|epic_hand`:
  - `"trigger": "apotheosis:equipped_item"`
  - `"conditions": {"items": {"predicates": {"apotheosis:item_with_rarity": {"rarities": ["apotheosis:epic", "apotheosis:mythic"]}}}, "slots": "head|chest|legs|feet|hand"}`
- Dragon criterion `kill_ender_dragon`:
  - `"trigger": "minecraft:player_killed_entity"`
  - `"conditions": {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "minecraft:ender_dragon"}}]}`
- `"requirements": [["epic_helm"],["epic_chest"],["epic_legs"],["epic_feet"],["epic_hand"],["kill_ender_dragon"]]`: all six are required (AND).
- Native text: "Entering the Pinnacle requires freeing the End, and acquiring a full set of Epic gear".

### 2. Captain Cornelia
- **ID:** `aquamirae:captain_cornelia`.
  - Mod `aquamirae-neoforge-1.21.1-7.2.10.jar` (an R4 pin, SHA256 `d6269491…8710`).
  - Registered in `dev/obscuria/aquamirae/registry/AquamiraeEntityTypes.class` (literal `captain_cornelia`).
  - Has her own loot table and spawn egg. Display name "Ghost of Captain Cornelia". Evidence: `CORNELIA_EVIDENCE.json`.
- **How she appears:** she isn't placed by a structure.
  - The **Shell Horn** summons her. Its tooltip: "Summons Captain Cornelia. Can be used near water in the Ice Maze."
  - R4 `config/obscuria/aquamirae-common.toml`: `shell_horn_usage_mode = "ICE_MAZE"`, `shell_horn_search_radius = 12`, `shell_horn_cooldown = 5`, `ice_maze_biomes = ["minecraft:deep_frozen_ocean", "minecraft:deep_cold_ocean"]`.
  - She's in `#aquamirae:ice_maze_creatures`.
- **Shell Horn source:**
  - Guaranteed drop of loot table `aquamirae:entities/maze_captain`.
  - That table belongs to one embedded mob per `aquamirae:pirate_ship` structure. It's a raider with 24 HP holding the horn (`PersistenceRequired`), so likely a pillager.
  - No recipe or chest loot found. The horn is used up per use (`ItemStack.shrink`, skipped in creative).
  - Pirate ships: biomes `#aquamirae:ice_maze`, placement `aquamirae:configurable_random_spread`, spacing **35** / separation **10** chunks (R4 config, unchanged by AO). Their spawn overrides add pillagers and vindicators, but those don't carry the horn.
- **Dimension:** Overworld only. No AO config removes or replaces `deep_frozen_ocean` or `deep_cold_ocean`; they only appear in AO dragon-cave biome tags.
- **What R4/docs say:**
  - Canonical handoff §4: "Dead King/Cornelia T6 *loot* with T7 *combat* targets".
  - §5.3: "Dead King / Cornelia retain T6 category/loot, but aim for T7 combat scaling; unimplemented native Cornelia route remains explicit."
  - Packager note: "Cornelia combat has no verified native config and remains BLOCKED".
  - `02_BOSS_ARENA_INVENTORY_T6_T9.csv`: "ARENA UNKNOWN".
  - Campaign maps her as boss tier 6 (`AOCampaign.BOSSES`, `ao_loot_policy.json`).
- **Corrections found:**
  - She needs no arena; any Ice Maze water works.
  - R4 does ship a native combat config, `captain_cornelia_attributes = ["generic.max_health set(300)", "generic.armor set(16)", ...]`, so "no verified native config" is out of date. Not changed here.

### 3. Override (source, generated)
- `tools/compile_pinnacle_cornelia_gate.py` reads the pinned native file and swaps only the dragon criterion block and its requirement key.
- It writes:
  - `release_030/experimental_overlays/v050/overrides/config/paxi/datapacks/ao_campaign_gates/{pack.mcmeta, data/apotheosis/advancement/progression/pinnacle.json}`. Same path as R4's bad gate, so a new build replaces it.
  - A lang resource pack `.../config/paxi/resourcepacks/ao_campaign_gates_lang/` with the criterion name "Slay the Ghost of Captain Cornelia" and an updated description. Without it, the criterion would show a raw lang key and the old "freeing the End" text.
- `--check` mode verifies the committed files are current.
- The gate paths were taken back off `removed-source-paths.json`, which is now byte-identical to R4. Otherwise the packager would strip the new pack.
- Diff vs native: 3 lines (`kill_ender_dragon` -> `kill_captain_cornelia` twice, `minecraft:ender_dragon` -> `aquamirae:captain_cornelia`).

### 4. Grant paths
- **Campaign code:** grants only `ao_campaign:milestones/*`. There's no `WorldTier`/`getUnlockAdvancement` use, and the T6 Pinnacle grant removed in `01c2c58` has not come back (tested).
- **Everything else:** none of the 10 R4 custom JARs, 330 installed mod JARs or R4 config/quest files references `apotheosis:progression/pinnacle`.
- **Bypasses, operator only:** `/advancement grant` and Apotheosis `WorldTierCommand` (`set_world_tier`, calls `setTier`). Normal players can't bypass.
- **Existing worlds:** players who already unlocked Pinnacle keep it. Apotheosis stores unlocked tiers (`UnlockedTiers`).

### 5. Multiplayer (analysis, not tested)
- Vanilla `LivingEntity.die` fires `player_killed_entity` only for the entity's kill credit (`getKillCredit()`: the last player who damaged it, within the recent-damage window).
- **Assists and shared kills get nothing.** Credit goes to the last player who damaged her within 100 ticks (5 s), not strictly the final blow. The native dragon criterion had the same rule.
- **Compounding factor:** each horn is used up and each ship has one horn. So 5-7 players each need their own Cornelia kill, which means 5-7 horns from 5-7 pirate ships.
- **Withdrawn (owner rule 15 Oct: credit only to the player credited with the kill; no proximity or party credit).** Never applied. Deterministic credit policy: `docs/handoffs/r5-corrections-20261015/CORNELIA_KILL_CREDIT_POLICY.md` (branch `status/r5-corrections-20261015`). Original proposal, kept for history:
  - In the campaign addon, track players who damaged Cornelia (e.g. `LivingIncomingDamageEvent`, with a minimum damage share and same dimension/range).
  - On her death, award only the Pinnacle criterion: `player.getAdvancements().award(pinnacle, "kill_captain_cornelia")` for each contributor.
  - The five gear criteria stay required per player. No `minecraft:impossible` is needed.
  - Needs owner approval of the contribution rule.

### 6. Reachability (static, not tested)
- **Rarity:** one pirate-ship attempt per 35x35-chunk cell (560x560 blocks). It succeeds only if the start position is deep frozen or deep cold ocean.
  - Example: a 10k-radius pregen holds about (20000/560)^2 = **~1,275 cells**.
  - The share of cells in those biomes under the FTF preset is unknown without biome sampling.
- **Respawn:**
  - Cornelia isn't tied to a structure, so every new horn summons her again.
  - The horn carrier is a one-time structure mob and doesn't respawn.
- **Permanent miss:**
  - **Possible inside a fixed world border.** Total horns there = total pirate ships, and each summon uses one.
  - Outside a border, new ocean exploration produces new ships.
  - **Pinnacle is unreachable for everyone if FTF never generates those ocean biomes.**
  - Unknown: whether a failed summon ("Nothing happened...") also uses up the horn.

### Rollback
`git revert <this commit>`. That returns to the gate-deleted state of `9643b17`. The R4 ZIP is unchanged.

### Remaining
- **Engine:**
  - `/locate biome minecraft:deep_frozen_ocean` and `/locate structure aquamirae:pirate_ship` in a NORMAL FTF world.
  - Summon and kill Cornelia, then confirm the criterion and the Pinnacle unlock.
  - Check whether a failed summon uses the horn.
  - Check the lang text shows.
- **Multiplayer:** two-player fight, to confirm only the credited killer gets the criterion.
- **R5 toolchain:** it copies R4's impossible gate unchanged. To carry this override, `package_r5_grand_from_r4.py` must be allowed to replace these 2 files and add the 2 lang files. Needs your OK. Not changed.
- **Pregen/world border:** confirm the horn supply covers 5-7 players.
