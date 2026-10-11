# Ambient Odyssey v0.4.4 — Pre-performance candidate test handoff

**11 October 2026. Status:** independently built, source-validated private **experimental candidate**. The exact v0.4.3 tested ZIP and rollback branches remain untouched. Full Minecraft client, quest reward and multiplayer runtime checks are still necessary.

## Changes included in the actual packaged ZIP

1. **Questlog UI:** `overrides/config/questlog-client.toml` now disables the standalone/native floating Q button. The existing AO Better Inventory bridge 0.1.4 (from the tested v0.4.3 baseline) remains installed and is intended to display the single Q tab immediately RIGHT of Settings. This explains prior duplicated/wrong-side display, but GUI runtime confirmation is still pending.
2. **Starter quests (52 instead of 50):**
   - `A Door Beyond the World` — `questlog:visit_structure` with actual `minecells:overworld_portal` registry ID verified against Mine Cells 1.21.1 source. Reward: 12 torches and 4 bread. Must reach naturally generated structure; simply crafting/placing a doorway does not fulfill the objective.
   - `Your First Victory` — OR group with six Questlog `questlog:entity_kill` objectives (zombie, skeleton, creeper, spider, drowned, enderman), each one kill; reward 8 torches, 3 cooked beef. This is an **early pilot for six common vanilla hostile types**, NOT universal detection of every modded monster. Questlog's native matcher has no guaranteed 'all hostile mobs' class filter in these JSON entries. Both quests are non-repeatable and unlocked after Welcome. Rewards and repeatability statically checked, not client/multiplayer tested.
3. **Dragon Tower:** CristelLib placement spacing 96 -> 104, separation 48 unchanged. This lowers theoretical per-area grid attempts by ~15%, not a measured in-game frequency promise.
4. **Villages:** overrides vanilla `minecraft:villages` structure-set placement spacing 36, separation 8 with all five normal village structures still referenced, to modestly reduce vanilla/CTOV-associated village grid attempts. Other independent village mods and their structure sets are not changed. Test CTOV's effective worldgen selection under this override; relative CTOV small/medium/large weights 10/4/1 intentionally unchanged.
5. **Malkuth arena:** source-verified narrow datapack override of `fdbosses:malkuth_arena` template pool to select the part 1 template exclusively as the starting piece. Finderfeed FDBosses' Java requires a starting jigsaw named `fdbosses:malkuth_arena_part_1`; NBT binary audit verified that jigsaw is present in part 1, while the unpatched start pool offered other pieces without it. The structure still links its other pieces through jigsaw targets. This is a targeted fix and needs one in-game worldgen pass to verify it removes `No starting jigsaw` errors without damaging arena assembly.

## Unresolved issue (do not falsely mark fixed)

**Invalid ItemStack data:** supplied v0.4.3 `latest(20261011-192535).log` has 313 lines containing `minecraft:air`, 4 `redeco:hammer`, and one `quark:frog_leg` during chunk generation. The current log doesn't name the owning structure/template and the manifest-only CurseForge ZIP does not contain all third-party JAR asset binaries. Replacing missing IDs globally, or turning unknown items into arbitrary drops, would violate source-owner-backed repair policy. Need an installed-JAR offline NBT/source audit to attribute exact templates/loot tables, then patch only actual offending assets. No such fix is shipped in this candidate.

## Tests performed

- CI runs `tools/validate_v04_quest_campaign.py` for 52 quests, basic JSON validation, and `tools/package_v044_delta.py` with CRC, root CurseForge manifest, unique paths, byte-for-byte unchanged archive assets other than specified overrides, unchanged 330 third-party file pins, and reproducibility check.
- `tools/package_v044_delta.py` starts from the exact downloadable v0.4.3 GitHub Actions package; it is not a new unverified mod selection.
- Malkuth NBT audit inspected the official source template and its exact named jigsaw. No live Minecraft execution has been conducted for this v0.4.4 candidate.

## Minimal user test

1. Launch new v0.4.4 profile; open inventory and verify only one Q tab, RIGHT of Settings, click and reopen.
2. Welcome quest -> kill one listed common hostile mob -> collect basic supplies once; check restart persistence.
3. Walk into a natural Mine Cells Overworld portal **structure** -> see quest completed -> collect supplies once.
4. Explore newly generated terrain: check Dragon Towers and villages feel somewhat rarer without losing CTOV varieties.
5. With throwaway world, generate/find Malkuth arena and verify no starting-jigsaw failure; capture `latest.log` if it persists.
6. Ordinary survival travel on the unchanged worldgen/pregen plan; do not benchmark admin `/locate` spam as player experience.

**Next before final performance freeze:** trace invalid item IDs to exact mod/JAR/template, fix only confirmed sources, then perform grouped static and Minecraft acceptance. Avoid rerunning 5-7 player campaign checks for every small preflight build.
