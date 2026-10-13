# Handoff B — Claude: isolated engineering tasks from PR #45
**Ambient Odyssey · 13 October 2026 · Code/source-validation tasks only. No automatic edits to live client/server or Work-mode branch.**

## Mission and coordination
Use **[PR #45](https://github.com/alsynth/AmbientOdyssey/pull/45)** as the **authoritative current structure-difficulty engineering baseline**, **[PR #44](https://github.com/alsynth/AmbientOdyssey/pull/44)** for provisional boss/gear/quest intent. Produce independent, targeted patches/tests that Work mode can review and merge *after* its runtime acceptance work, instead of rewriting the entire `difficulty_v2.json`.

**PR #45 head:** `experimental/structure-difficulty-v3-20261013`, audited profile **v0.4.9 Client Performance TEST**, 332 physical JARs. Source baseline `performance/v049-visual-ecology-20261013`; baseline exact `b387dc0` in report. Current test candidate: `experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json`. Rollback under matching `rollback/`. Installed config target: **`config/dungeon_difficulty/difficulty_v2.json`** (not guessed `config/dungeon_difficulty_v2.json`). **53 zones = 28 attribute pilots + 25 natural rules; 374 deliberately held.** Do not lift holds en masse.

### Mandatory source documents
- `docs/balance/STRUCTURE_DIFFICULTY_V3_IMPLEMENTATION.md`
- `docs/balance/v3-evidence/{VALIDATION.json,INSTALLED_JARS.json,ENCOUNTER_CONTROL_GAPS.csv,TRIAL_AND_LOOT_RESOURCES.json,LOOT_TABLE_INDEX.csv,TEMPLATE_RESOURCE_LINKS.csv,RESOURCE_COLLISIONS.json,RESOURCE_ERRORS.json,ENCOUNTER_NBT.errors.json,SKY_ARENA_NATIVE_CONTROLS.json,REMNANT_COMPATIBILITY.json}`
- `tools/structure_difficulty_v3.py`, `tools/audit_encounter_nbt_041.py`, `tests/test_structure_difficulty_v3.py` (on PR #45 branch)
- `docs/balance/V050_ENCOUNTER_MULTIPLAYER_REPLAYABILITY_PROVISIONAL.md`, `V050_BOSS_ROSTER_AND_GATES_PROVISIONAL.md` (on PR #44 design branch)

## Task 1 — P0: Elite/affix stacking exclusion feasibility and proof
**Problem:** Installed Dungeon Difficulty 3.9.2 entity-filter bytecode permits only `attitude` and `type`. A *vanilla* mob carrying Apotheosis affixes, or a Brutal Boss definition, may still match the ordinary vanilla ID allowlist and receive a secondary tier multiplier. The PR #45 pilot must not be promoted until there is a measured combined cap or a **source-backed exclusion**, not just “excluded named bosses” by namespace.

**Work to do:**
1. Inspect **exact binary/source code** for applied attribute hooks and timing: DD, Apotheosis/Apothic combat/affixes, Brutal Bosses and any mod that writes persistent modifiers to spawned mobs.
2. Document a reproducible event order (spawn attribute creation, modded elite rewrite, saved modifier refresh, load/reload), and test candidate detection against **actual** data components/attributes/mod markers; never rely on display name / color.
3. First consider a config-only limit if it can provably keep ordinary+elite combined budget. If not, prototype an AO-owned NeoForge compatibility addon **on a new isolated branch** with tests that avoids double-application and does not strip legitimate Apotheosis affixes.
4. Preserve vanilla survival mobs outside tracked structures. Handle spawn eggs, command spawns, chunk reload, portals and entities already spawned. Safe rollback and migration are mandatory.
5. Provide a small acceptance test matrix: T2 ordinary, T6 ordinary, T6 affixed, T6 Brutal Boss, T6 combined affixed+Brutal if possible, outside structures, multiplayer; record final HP, damage, armor, active modifiers and special attack damage separately.
6. If impossible without deep invasive hooks, report a controlled **hold** and measured combined cap option; no speculative mixins in production.

**Deliverable:** `docs/engineering/V050_DD_ELITE_STACKING_INVESTIGATION.md` + optional isolated addon patch and reproducible static tests. No “verified gameplay fix” without real Minecraft test.

## Task 2 — P0: Sky & Ice Arena native wave budget and stale IDs
**User-approved:** **Sky Arena T3; Ice Arena T3**. These are **wave-based arenas**, not template-spawner combat dungeons.

Evidence: `docs/balance/v3-evidence/SKY_ARENA_NATIVE_CONTROLS.json` exports `config/sky_arena.json`. The config has `mobGroups` with **`born_in_chaos_v1:*` mob IDs**; the audited `INSTALLED_JARS.json` contains **no Born in Chaos JAR** (removed earlier). That proves the config references a noninstalled mod, **not** that the game crashes. There may be other stale IDs; test all.

**Work to do:**
1. Extract **every arena's** mob-group pool IDs, points/budget, level ranges, native enemy stat coefficients, reward sources and boss/miniboss rules. Distinguish real playable `sky_arena` and `ice_arena` from sample/example presets.
2. Reconcile entities with the **actual mod registry**, not only JAR-name guesses. Determine how the Sky Arena mod handles missing entity IDs: skip, fallback, exception or silently block wave. Verify behavior in source/decompile before authoring changes.
3. Write a **minimal reversible config patch** removing/replacing invalid entries with **real existing mob IDs**, preserving encounter theme and native progression. Do not spawn global Bosses'Rise/Remnant/other Tier 7–9 enemies merely because they are registered.
4. Design Tier 3 **entry/early-wave** difficulty around existing native scale; never flatten all high wave levels to T3 and never stack DD on top. Allow escalating optional replayable waves, with separate rewards after a meaningful checkpoint.
5. Preserve existing arena level progression/rewards unless specific measured imbalance; Sky Arena currently has ranges 1–10 / 11–20 / 21–40 / 41+, per-player stats, `disableMobItemDrop:true`, and native reward tables (`skyarena:battle_rewards/ice_key` in sample). Audit whether these table IDs exist and whether repeated rewards are exploitable.
6. Produce source tests for every listed ID and a diff to native JSON; Work mode handles in-game wave/quest/lag acceptance.

**Deliverable:** `docs/engineering/V050_SKY_ICE_ARENA_NATIVE_REVIEW.md`, an optional **standalone config overlay**, invalid-ID ledger, test vectors and rollback. Do not edit PR #45 active prototype without coordination.

## Task 3 — P1: Encounter/NBT parser edge-case repair
PR #45 scanned **18,417** root mod templates; **18,415** decoded. Two Archaion `ancient_keep/misc_room.nbt` and `misc_room_x.nbt` produce **NBT `End` instead of Compound root** in static parser. One **Dungeons & Taverns v4.4.4** `data/minecraft/worldgen/template_pool/illager_mansion/illager_mansion_room_basement.json` yields Python JSON `Expecting value: line 9 column 23`. Neither error alone proves the mod crashes in-game.

- Inspect raw bytes, gzip framing/NBT type and exact JSON syntax/source; test whether these are intentional dummy/alternate grammar/pool passthroughs.
- Make the static audit **total and honest**: classify unsupported resource formats; retain original bytes; don't patch JARs or change generation unless real runtime error established.
- Add regression fixtures for `End`-root, truncated gzip, JSON variant; keep recovered-template statistics separate from normal decode.
- Report whether key templates are reachable in actually enabled structures, with evidence rather than assumptions.

**Deliverable:** minimal audited parser patch to `tools/audit_encounter_nbt_041.py` or corresponding v3 script + focused tests and before/after counts. Coordinate with Work before touching its tests in PR #45.

## Task 4 — P1: Native encounter, trial spawner and vault capability adapters
PR #45 deliberately did not edit equipment, special mobs, spawner delays, trials or vaults. Propose a **small design+code proof for one verified combat site** (T4 Trial Chamber or a proven T5 WDA/IDAS piece) where exact effective resource paths are known.

1. Use `TRIAL_AND_LOOT_RESOURCES.json` and `TEMPLATE_RESOURCE_LINKS.csv` to select source-authoritative `normal_config` / `ominous_config`, mob potentials, limit fields and loot/vault tables.
2. Prove what DD can and cannot control (no trial-spawner mixin in audited build); author **datapack-native overrides** when supported with migration-safe namespace/path and precedence checks.
3. Equipment mods: preserve native weapon/armor NBT, avoid re-rolling enchanted boss armor or doubling affix rolls.
4. Limit mobs alive, range, per-player increments, TTL, arena-grief protection and farm potential; prefer varied tactics over higher population.
5. Isolated small pack only; do not globally rewrite `minecraft:trial_chambers` or every shared `simple_dungeon` loot table without a source-targeting guard.
6. Ensure Lootr interactions and per-player rewards are tested by Work at runtime.

**Deliverable:** optional narrow proof-of-concept datapack, exact resource ID list, static tests and rollback, no full catalogue rollout.

## Task 5 — P2: Boss-specific source editability probes (research first)
- Prioritize **F.D. Bosses Geburah** (tier **unassigned**, do not choose one), Cataclysm **Maledictus T7 `cataclysm:frosted_prison`**, **Scylla T9 Acropolis** vs **Leviathan T7 Sunken City**, **Iron's Dead King** (provisional stronger T6 gate) and Tyros T9; Remnant **Ossukage/Kotsukage T7 and Umbrakar T8**, now 2.7.0 installed in PR #45 profile.
- **Bosses' Rise is not Block Factory's Bosses**. Scan both before claiming a configurable damage or boss-specific loot path.
- Collect HP, armor, phases, damage sources, summons, multipliers, hit counters, invulnerability/DPS caps, native per-player scaling, reset/repeat and loot outputs **from exact JAR/binary**. No new tier overrides, especially Geburah and third T9 End boss.
- Return a capability table `control: direct config / datapack override / isolated addon needed / hardcoded / unverified`, with a one-boss vertical slice recommendation. It must not override Work mode's present DD tests.

## No-clobber & reporting rules
- Claude's patch belongs in **separate isolated source branch** (e.g. `engineering/v050-elite-arena-compat-<date>`), reviewed/cherry-picked by Work later. Don't edit PR #45 branch or original full-pack/rollback in place.
- Do **not** change client/server mod files, the 332-JAR roster, installed Remnant 2.7, or quest progress saves.
- Every delivered claim has a provenance/evidence/status. Source/decompile/static test ≠ real gameplay.
- Prefer the smallest two code patches (elite safety and stale arena IDs) over many speculative implementations.
- Supply test logs, original vs changed config hashes, exact files, compatibility/dependency assumptions, rollback, and any blocker that requires the owner.

## Priority order
**1. Elite stacking safety; 2. Sky/Ice Arena stale IDs + native Tier3 wave budget; 3. Parser limitations; 4. one trial-spawner/equipment datapack proof; 5. boss mechanics capability survey.** Work mode owns full client/dedicated/multiplayer acceptance, rollout and Questlog/loot integration.
