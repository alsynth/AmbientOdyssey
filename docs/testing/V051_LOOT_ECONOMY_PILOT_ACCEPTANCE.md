# v0.4.9.1 Loot Economy pilot — real client / dedicated-server acceptance

Status: executable acceptance checklist, NOT certification. Source branch: `experimental/loot-economy-first-pass-20261013` / draft PR #51. Never test on the main survival world.

## Build / import
1. Obtain exact PR50 full import `Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip` (SHA256 `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f`).
2. Obtain GitHub Actions `ao-starter-chest-compiled-experimental` artifact from the PR51 loot CI success; extract `ao-starter-chest-0.1.0-experimental.jar`.
3. From a checkout of PR51, run:
   `python tools/package_ao_loot_economy_pilot.py --base <PR50-FULL-IMPORT.zip> --starter-jar <ao-starter-chest-0.1.0-experimental.jar> --output Ambient-Odyssey-v0491-LOOT-PILOT.zip`
4. Verify generated `.report.json` and import the new ZIP into a disposable CurseForge profile (do not overwrite any live profile). Pinned CF references remain 338; one extra custom mod is bundled.
5. Export a disposable server copy only after client acceptance. No server build is claimed or supplied by PR51.

## Starter chest in an isolated fresh world
- Create a new world, **Bonus Chest ON**. Verify that the actual spawn chest converts to Lootr before any player opens it (visible type/appearance; or inspect server block entity). `loot_table_forced_whitelist` is enabled for that specific chest table but does not prove conversion.
- Two separate non-OP accounts A and B: A opens, receives rewards and empties; B opens same physical chest and still receives independent rolled rewards.
- Each player should receive **exactly one** of these five items from `enigmaticlegacyplus`: `blazing_core`, `golem_heart`, `ocean_stone`, `angel_blessing`, `lost_engine`.
- Each gets **exactly one real Apotheosis affix item**, Common 55%, Uncommon 30%, Rare 15% over many rolls. Inspect actual generated rarity and affix data components; fake rarity lore doesn't count.
- Each gets **32–48 torches** and **16–48** one type of cooked beef/pork/chicken/mutton. No additional Apotheosis affix or gem drops from native random-injection hooks.
- Eligible affixed armor has one cosmetic random trim; weapons and ordinary armor do not get unintended trims. Affixed armor should not have rerolled affixes.
- Both can save, quit, relog and reopen without rerolling a looted inventory. Late joiner gets their first independent roll. Verify bypass_spawn_protection but no unintended chunk changes.
- Create a second world with Bonus Chest OFF: no guaranteed supply chest, no new special spawn items. No changes to standard dungeon chests.
- If Bonus Chest fails to convert, report it explicitly: do NOT claim per-player Lootr rewards. Consider separate `/lootr custom` fallback *only with owner approval*.

## Recipe and trader checks
- JEI Basic Flight Ring recipe uses 1 Nether Star in center; no diamond.
- Advanced Flight Ring includes Basic Ring, 2 Eyes of Ender, 2 Netherite Ingots, 1 `irons_spellbooks:cinder_essence`, 2 `irons_spellbooks:arcane_ingot`, 1 `ars_nouveau:air_essence`; no Echo Shard or redundant Nether Star.
- Craft both on a disposable creative/test world. Confirm no additional alternative cheap recipes bypass the revised requirements.
- Spawn fresh overworld Goblin Traders until the four epic tuned chainmail offers appear. Verify each costs 32 diamonds + 4 Cinder Essence (one purchase per generated offer), and keeps the original `+0.5 ADD_MULTIPLIED_BASE` armor modifier and 10x durability.
- Verify the other 18 epic trader offers still work and the original Vein Goblin trades remain unchanged. Older spawned traders might retain cached offers, so start with newly generated traders.

## Accept/reject gates
- Reject for startup crash, broken datapack reload, missing five spellstones, one missing/fake affix item, duplicate affixes/gems, shared first-player chest, wrong quantities, wrong price/modifier or regression in existing structures/quests/world tiers.
- The CI-only source tests and native affix GameTests are useful but do NOT replace the two-player combined-modpack scenario.
- Rage Glove remains an unimplemented deferred gate to a Tier 7 Nether boss, pending Claude's tier selection.
