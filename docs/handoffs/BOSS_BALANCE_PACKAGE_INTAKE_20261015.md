# Boss-balance handoff intake — 15 October 2026

Status: **documentation and decision reconciliation only**. The source package is `NEXT_AGENT_PACKAGE.zip` (14 Oct), containing files 00–21, tools and 39 rollback-baseline config files. This intake is **not** an indication that the source archive, binaries, baseline tree or boss values have been imported into GitHub, nor that tests were run in game.

## Authoritative owner decisions (newer than the package)

1. **Brutal Bosses before Overworld pregeneration:** `globalBossSpawnChance=70`, `minDistance=30`, `healthMultiplier=4.0`. Earlier owner direction required `damageMultiplier` and `healthMultiplier` to remain equal, so use **`damageMultiplier=4.0`** as well. The package's `06_brutalbosses.json` has 70/30 but both multipliers still at **1.0**; do **not** deploy that file unchanged. The package index describing multiplier x3 as a placeholder is outdated. Do not touch `dummyboss.json`, boss files or spawn tables. Verify live config and exact client/server deployment before marking implemented. Spawn chance/spacing must be applied before terrain pregeneration.
2. **Dungeon Difficulty Category B Batch 2:** retain all explicitly accepted entries unchanged; change only `dungeons_arise_seven_seas:corsair_corvette` to **Tier 4**. This is a **draft review-ledger** decision, not production. Do not infer decisions about remaining dimension-uncertain entries.
3. Distinct multiplayer player builds are still to investigate; most build work can follow worldgen. Boss-encounter special tuning will be handled by the owner's addon; boss loot overhaul and Quest Atlas are planned. Optional dimension-specific quests planned; snow effects should be checked against Euphoria patches first. Custom AO menu can follow worldgen. Tier 9 superbosses are intended as far-future goals; do not rush to make them immediately defeatable.
4. Preserve all earlier accepted decisions in file 00: T9 Tyros/Scylla/Obsidilith; Ignis/Maledictus/Leviathan T8; Geburah TBD; Mother of Maze is not a boss; Ancient Remnant's entity is valid; Eternal Starlight boss family/respawn choice remains TBD. Overworld pregeneration first.

## Package inventory and evidence

- 00–04: index, worldgen freeze draft, arena inventory (34 rows), arena check guide, encounter results template.
- 05–06: Brutal Bosses findings and pregen config draft.
- 07–11: editability and measured results, Scylla tests and boss focus dossier.
- 12–16: reward routing, capability catalogue/matrix, Remnant Bosses 2.7.0 and Eternal Starlight 0.9.1 inspections.
- 17–21: balance ledger (35 rows), baseline progression report, compatibility evidence, test/rollback protocol, unresolved blockers.
- rollback-baseline: 39 byte-exact configuration snapshots plus SHA256SUMS; keep separate from live config.
- tools: arena discovery / stat measurement datapacks and parsers.
- Six separate user attachments (17–21 and 17 ledger CSV) duplicate the packaged editions and should be compared for byte differences rather than silently treated as additional decisions.

## Baseline findings, not target values

Native HP medians from file 18: Tier 6 300, Tier 7 525, Tier 8 410, Tier 9 390. This is **not** an agreed target curve. Health caps at 1024 in testing; HP alone is not boss difficulty. Dungeon Difficulty rules matched **0/34** tested Tier 6–9 entity IDs (file 19), but may apply to vanilla-mob Brutal Bosses. Apothic Attributes changes armor/protection handling on all fights. Tyros has the Stronger Fire Boss addon, and original vs Integrated arenas require runtime precedence checks. No combined fights or multiplayer scaling tests were performed.

## Open gates — do not invent or mark complete

- Tier-relative player-power model / DPS, EHP and fight targets; the implementation package and real progression consistency model are not ready without these.
- Five never-measured boss records (the sources inconsistently count five while file 18 names four: Ignited Revenant, Coralssus, Kobolediator, Ender Golem; file 21 also names Ice and Fire Hydra). Track the discrepancy explicitly, do not infer measurements.
- Damage interaction-locks (Gatekeeper, Starlight Golem, Ancient Remnant, Yeti); arena/portal precedence, SERVER-type config placement and runtime verification.
- Reward pacing and high-tier affix loot, Rage Glove routing, player-count scaling, party-wipe/repeat farming effects, addon damage scaling.
- Worldgen freeze is a draft, not signed off. Arena checks and measurements require in-game work; static validation cannot establish runtime behavior.

## Safe next sequence

1. Import/archive the **actual** 00–21 documents, raw CSVs, tools and the immutable rollback baseline into a dedicated research directory/branch. Keep baseline checksums intact.
2. Reconcile duplicate attachments and preserve a manifest with hashes. Keep latest accepted owner overrides clearly separate from historical package text.
3. Apply 70/30 and 4x/4x to the **active** Brutal Bosses config on a separate experimental/pregen branch, confirm the effective file, diff and parsability, and preserve rollback material.
4. Verify arena and SERVER-type config worldgen requirements before Overworld pregen; do not call freeze signed until runtime checks.
5. Only propose per-boss HP/damage targets once player kit reference is grounded. Keep loot changes independently reviewable and avoid prematurely tuning Tier 9.

This intake note is a committed decision artifact, **not** a claim that the full archive was uploaded or deployed.
