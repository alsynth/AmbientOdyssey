# Ambient Odyssey PR56 — What the owner actually needs to do (14 October 2026)

> **Additional source checks completed:** The five non-YUNG cases (Adventure Dungeons camp, two Luki villages, two Pasterdream structures) now have [exact pinned-native and AO Paxi source evidence](DD_ADVENTURE_LUKI_PASTERDREAM_PINNED_NATIVE_20261014.json), with [seven-case conclusion](DD_NEXT_SEVEN_OVERWORLD_BIOME_ELIGIBILITY_20261014.md). The AO `minecraft:villages` Paxi set **36 spacing / 8 separation** deliberately differs from Luki native **50 / 35**; regression tests protect against reverting it. All four Pasterdream picnic biome IDs have native biome files, but runtime generation is unknown. **No additional owner decisions or test chores now**: these can be sampled opportunistically in the existing later disposable-world session if the active pack suggests trouble, rather than requiring a new separate test run. CI run [38607408019](https://github.com/alsynth/AmbientOdyssey/actions/runs/38607408019) passed all five jobs.


> **14 Oct — packaged isolated test candidate ready (NOT for production):** [GitHub Actions test artifact](https://github.com/alsynth/AmbientOdyssey/actions/runs/38603628576) named `pr56-four-tower-worldgen-TEST-ONLY` includes a standalone 9-member datapack ZIP + SHA-256 manifest. **ZIP SHA-256** `a797057bfe057a88212a56a3462ee8df6b1e9108e72a6e78ece485bd411b2db6`. Byte-for-byte reproducible on two CI builds. Source-only PR50-vs-PR56 Paxi comparison 14/14 folders identical for targeted resources, no collisions; [retained provenance](DD_PR56_PR50_PAXI_SOURCE_PARITY_20261014.json). **No live Paxi/worldgen changed**. [Later disposable-world acceptance guide](../testing/PR56_FIREWATCH_TEST_ONLY_ACCEPTANCE_20261014.md); no user action immediately required.

> **Current source resolution:** The exact pinned D&T v4.4.4 NeoForge JAR has been verified by SHA-1 and audited. The first shared-tag candidate was **cancelled for scope risk** (up to 22/19/20 native structures affected through `collections/land`). The new [four-tower structure-only candidate](../../experiments/structure-biome-compatibility/firewatch-structure-only-draft/README.md) passes offline and fresh-JAR source-diff checks; it is **NOT ACTIVE**. Owners do **not** need to manually verify any of this static work. The later in-game task, **only after** an approved playable test ZIP exists, is bounded natural generation of birch/cherry/forest/savanna firewatch variants in representative preserved curated biomes and comparison with original controls. Do not run broad `/locate` on the production server.
>
> **GitHub source evidence:** [Pinned JAR consumer + structure JSON report](DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json); [full firewatch research](DD_FIREWATCH_CURATED_BIOME_BRIDGE_RESEARCH_20261014.md). Exact code change from original per tower: `biomes` field only, leaving source pools, size, terrain adaptation, step and shared structure-set untouched. Runtime density/priority remains unknown.


**Working principle:** Continue all static/source/catalogue work autonomously. Do **not** ask the owner to repeat decisions or test the entire 1,240-ID tier map. PR56 remains RESEARCH-ONLY and draft. Screenshots or logs of a manually placed structure are **not** proof of its *natural generation*.

## Confirmed owner decisions: no more owner input needed

| Decision | Authoritative instruction | State |
|---|---|---|
| 26 previously protected source-spawner IDs | **All Tier 0**; do not disable native spawners; no DD buffs | Recorded in all core ledgers. No need to re-review the 26 |
| `dungeoncrawl:dungeon` | **Tier 3 across the entire dungeon**; **no** floor split/addon | Core ledgers and 34-ID audit agree |
| Tier 0–1 DD | No attribute-based DD scaling | Retain in candidate design |
| Tier 7–9 encounters | Prefer native boss/mechanic controls, not generic DD stacking | Keep as research/verification gate |
| Twilight Hydra boss | **Tier 7 boss plan already recorded** | Do not ask again; old `twilightforest:hydra_lair` Tier 4 catalogue still needs non-gameplay reconciliation (boss tier vs whole-lair structure tier) |

## WHAT IS NEEDED FROM YOU — minimal next manual session (NOT required to continue research)

**When:** after the next complete playable client/temporary server candidate and before committing to irreversible large Overworld pregen; **not** on the main multiplayer world. Use the exact intended modpack version and selected worldgen datapacks. Keep an unmodified control profile if comparing configs.

1. **Exact profile evidence (one time).** Record pack version/commit, launcher modlist or reproducible client ZIP checksum, Minecraft/NeoForge versions, and `/datapack list enabled` output. This determines which Paxi resource overrides are actually active. If the source profile already exposes the exact data, no need to provide it twice.
2. **Overworld structure smoke test in disposable world.** Choose a representative curated forest/savanna/birch biome. Try `/place structure nova_structures:firewatch_tower_forest` with cheats. **Do not spend time testing CTOV Mesa yet**: new [Mesa-vs-Badlands source triage](DD_CTOV_MESA_BADLANDS_SOURCE_TRIAGE_20261014.md) found the historical config enables the Badlands outpost ID and leaves Mesa without a linked structure set; effective PR50 registration remains to be investigated from source. Note whether command accepts the registered ID, whether visible construction appears, and the exact error if any. Capture `F3` biome and seed/coordinates (test world only). These are **registration/place** smoke tests: passing does not prove the structure naturally appears; failing could have biome/placement reasons.
3. **Nether worldgen smoke test only if testing the Nether now.** In a disposable Nether world, use `/place structure eternalnether:piglin_manor` and `/place structure eternalnether:catacomb` (and `eternalnether:citadel` if convenient). Capture exact errors, visible structures, and whether ordinary/spawn-override entities actually appear. Don't assume that lack of immediately visible enemies disproves source mob features. Natural placement must later be checked with a *bounded* seed/sample experiment.
4. **Send only compact evidence:** version/commit, successful/failed command, biome/dimension, screenshot if useful, and log excerpt when a command fails. This should be enough to target further source changes. Do not use unlimited-radius `/locate` on the live server—PR50 documented a 40,001 ms Nether tick during broad placement scanning.

**Priority:** An exact active profile/override manifest is more useful than hundreds of manually inspected structures. If you have not installed the next candidate yet, **there is nothing to test immediately**; source audits can proceed without you.

## Later, after we have an isolated DD v4 candidate

- Verify Dungeon Crawl's single Tier 3 scaling at both shallow/deep floors (not a floor split), ordinary hostiles vs Apotheosis elite mobs, and controls just outside the structure.
- Sample one naturally generated representative of each significant Overworld family before huge pregeneration, not every cosmetic variant. Record seed + coordinates + version.
- For boss arenas, check native scripts and elite double-stacking independently from DD; never add generic Tier7–9 multipliers solely because the catalogue has those numbers.
- Two-person/dedicated-server runtime tests still matter before public/multiplayer promotion.

## Assistant-owned work — continue without owner interruption

- **D&T firewatch source work completed:** exact native JAR + shared-tag consumers + four scoped selector overrides staged in inactive experiment. Remaining assistant-owned step: reconcile winning Paxi/current PR50 resource pack precedence, prepare an isolated acceptance build, then record bounded real-generation tests. Do not enable the superseded shared-tag pack. See [source report](DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json).
- Resolve `ctov:pillager_outpost_mesa` vs the **enabled** `ctov:pillager_outpost_badlands` based on the source triage; do not ask owner to test the likely orphan Mesa ID unless current build evidence differs.
- Resolve Eternal Nether `piglin_manor` source `definition.type=eternalnether:citadel`, pool reachability, and source mob features. Registration is already confirmed in a **scoped PR50 client** query; natural placement remains unproven.
- Split ordinary vanilla DD-compatible mob sources from trial-spawner mechanics and scripted/modded boss entities; do not widen regex blindly.
- Reconcile Hydra `Tier7 boss` vs historic `Tier4 lair` semantics as a *catalogue-only* issue; ask owner only if a **new** gameplay design choice genuinely arises.
- Preserve 26 approved Tier0 records, 15 source-only family research holds, 107 historic-but-absent Repurposed IDs, and three unverified generated clones from deployment.

## Explicit blocking vs non-blocking

| Task | Owner required **now**? | What blocks |
|---|---|---|
| Static source catalogue and tier consistency | **No** | None |
| Active Paxi and current JAR source inspection | **No**, if profile artifacts are already available | If only the player's local installation has the active override, request exact archive later |
| Overworld 10k–20k Chunky pregen freeze | **Yes, later** | A final worldgen profile/version and bounded worldgen acceptance; do not interpret first-pass mapping as sufficient |
| Nether / Pasterdream structure validation | **Yes, later for runtime proof** | Separate from Overworld pregen until cross-dimensional evidence |
| Production DD v4 / boss difficulty | **Yes, later for acceptance**, not for source research | Dedicated profile, elite behavior and owner approval of final proposed tier/specific encounter effects |

No settings, mobs, loot tables, structure definitions, active DD rules or world files were changed by this document.
