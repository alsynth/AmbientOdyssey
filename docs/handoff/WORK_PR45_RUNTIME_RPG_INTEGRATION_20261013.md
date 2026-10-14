# Handoff A — ChatGPT Work mode: PR #45 runtime/implementation integration
**Ambient Odyssey · 13 October 2026 · Read-only planning handoff; no gameplay changes in this branch**

## One-sentence mission
**Finish acceptance of the reversible, narrow structure-difficulty pilot already built in [draft PR #45](https://github.com/alsynth/AmbientOdyssey/pull/45), then integrate the RPG/loot design of [draft PR #44](https://github.com/alsynth/AmbientOdyssey/pull/44) in small, tested slices — do not replace or reimplement PR #45.**

### Required source order and integration boundary
1. `AGENTS.md` and latest consolidated release source.
2. **PR #45 head** `experimental/structure-difficulty-v3-20261013` (base `performance/v049-visual-ecology-20261013`). Read:
   - `docs/balance/STRUCTURE_DIFFICULTY_V3_IMPLEMENTATION.md`
   - `docs/balance/v3-evidence/SUMMARY.json`, `VALIDATION.json`, `CURRENT_PROFILE.json`, `INSTALLED_JARS.json`
   - `RECONCILED_CATALOGUE.csv`, `APPROVED_TIER_MAPPING.csv`, `ENCOUNTER_CONTROL_GAPS.csv`, `RESOURCE_COLLISIONS.json`
   - `TRIAL_AND_LOOT_RESOURCES.json`, `LOOT_TABLE_INDEX.csv`, `TEMPLATE_RESOURCE_LINKS.csv`, `SKY_ARENA_NATIVE_CONTROLS.json`
   - `experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json` and exact `rollback/` equivalent.
3. **PR #44 design branch** `research/rpg-boss-loot-campaign-design-20261013`. Read `docs/balance/README_V050_RPG_DESIGN_20261013.md`, `V050_IMPLEMENTATION_HANDOFF.md`, `V050_OWNER_DECISION_REGISTER.csv`, and quest plan `docs/questing/V050_QUEST_CAMPAIGN_BLUEPRINT_PROVISIONAL.md`.
4. This handoff; refer to [Claude handoff](CLAUDE_PR45_ENCOUNTER_ENGINEERING_20261013.md) for low-level, code-oriented problems. Do **not** edit the same overlay/config simultaneously.

**Avoid blind branch merges.** PR #44 and PR #45 descend from different research/performance bases; reconcile desired files against the **effective latest tested runtime import**, preserve independent progress, and isolate modifications in a fresh implementation branch. Keep PR #45 draft, the current server/profile, stable r19 rollback and performance branch unchanged.

## What Work mode already completed in PR #45 — do NOT redo
- Physical audit of **332 installed JARs** in `Ambient Odyssey v0.4.9 - Client Performance TEST` (332 vs original 328 manifest pins).
- Historical 427-row catalogue reconciled: **386 named candidates** have root resources; 41 archived/reference rows. Current resources: 351 unambiguous, 33 provider-precedence conflicts, 2 disabled vanilla replacements.
- All **282 approved T0–T6** rows evaluated; **53 eligible experimental rules**: **28 attribute pilots + 25 natural-preservation rules**, **374 held** deliberately.
- `Dungeon Difficulty 3.9.2` candidate source at the **exact installed path** `config/dungeon_difficulty/difficulty_v2.json`; type levels kept at 1 and ordinary vanilla mob HP/attack/armor tier bonuses are bounded. No spawner/loot/player-count scaling.
- Source evidence includes **18,415 decoded NBT templates**, 15,163 loot-table provider records, potential collision/placement leads, native Sky Arena wave controls and Remnant 2.7.0 static compatibility probes.
- Native Gson schema, 10 new tests, 3 inherited tests and legacy quest/manual checks passed statically. **No Minecraft runtime, multiplayer, effective datapack precedence or server acceptance.**
- **Remnant Bosses 2.7.0 is already physically installed in the audited profile** (not merely pending): `remnant_bosses-neoforge-1.21.1-2.7.0.jar`, hash `db153190…2207a`, declared dependency compatibility passed. Still requires real startup and boss/phase tests.
- Installed YUNG configs disable **vanilla** fortresses and monuments; effective replacement rules must target YUNG's actual structures, not double-apply vanilla rules.
- WDA **Aviary End T6** and **Keep Kayra T6**, **Foundry/Mechanical Nest T5**, YUNG Nether fortress T4 are among pilots; **Sky/Ice Arena T3 held** for native wave settings. Twilight Forest boss/landmark mechanics and T7–9 bosses remain held.

## Deliver in four non-overlapping, gated slices

### A. Reproduce the candidate faithfully (highest priority)
1. Reconcile latest v0.4.9 mod JARs, hashes, current configs, and any changes newer than PR #45. Do not substitute old `release_030/release-lock.json` or assume 328-pin import identifies installed 332 JARs.
2. Re-run builder and exact DD Gson/schema, regression, 53-zone, kit hash and rollback checks described in PR #45; capture generated kit path and SHA-256.
3. Prepare a **cloned disposable CurseForge profile and cloned save**; candidate requires replacing **one** DD file at `config/dungeon_difficulty/difficulty_v2.json`. Keep client and server copy synchronized while stopped. Never overwrite only user's real server/saves.
4. If capable of running Minecraft, actually launch client and dedicated server using the exact JAR roster and inspect loaded resource IDs. If Minecraft cannot run in Work's environment, stop short and supply a precise user-executable test pack/checklist; **do not mark runtime PASS**.
5. Test T0/T1/T2/T4/T6 representative natural and located structures, mob attribute stacking for vanilla, **Apotheosis elites** and **Brutal Boss** variants, modded attacks, reload, exiting/entering structure boundaries, and T7–9 exclusion. Test rollback with cloned save too.

**Do not promote** the candidate while elite stacking is unbounded. PR #45 explicitly says DD 3.9.2 lacks a boss/elite NBT filter (only `attitude` and `type`). Claude should research a compatible modifier exclusion or combined cap independently.

### B. Resolve the high-value held entries, not all 374
- Verify **native Sky and Ice Arena wave progression**, reward tables and actual mod IDs; Tier 3 is approved, but **do not give them a second DD attribute multiplier**.
- Runtime proof for **YUNG ocean monument** active replacement, **Bastion T5 variant-level shared-ID targeting**, major **Nether/End** source and integrated Cataclysm/Mowzie/BOMD override precedence.
- Check **Aviary, Keep Kayra, Foundry, Mechanical Nest** at final difficulty; a mere mob HP multiplier cannot establish a high-tier structure's encounter quality.
- Investigate the 33 resource-provider overlaps with **targeted tests** and record effective-winner evidence; avoid assuming historical root resource always wins.
- Collect 2 Archaion NBT decode exceptions and 1 Dungeons & Taverns parser exception for Claude; don't conflate static parsing limitation with in-game crash.

### C. Build small loot and RPG slices after acceptance
- Keep **T0–T2 and early Mine Cells loot untouched**.
- Implement **two isolated sample loot-role mappings**, one verified T3 and one verified T5 structure, choosing their effective actual template/loot table IDs from PR #45's `LOOT_TABLE_INDEX.csv` / `TEMPLATE_RESOURCE_LINKS.csv`. Roles are **Scrap, Supply, Equipment, Treasure, Grand Treasure**; do not interpret proposed class ratios as per-roll loot odds. Preserve native thematic drops and Lootr player state. First-clear boss rewards and farmable drops are separate.
- Current r19+ has **52 live Questlog quests / 13 chapters + 32 FTB manual pages** (verify newest source). The v0.5 plan's **101 beats are authoring seeds**, not an instruction to replace 52 live quests. Prototype *one optional T3 arena discovery* and *one T5 alternate milestone* with real validated objectives only.
- T5 BOMD Lich or Void Blossom and T6 Dead King as Pinnacle primary are **design proposals**, not source-validated user final approvals. Before enabling gates: exact entity/spawn/loot IDs, encounter availability, and **a second comparable strong T6** alternative.
- Keep Geburah boss tier **unset**, third T9 End superboss **unset**, and never manufacture entities/loot components. Preserve **Maledictus Frosted Prison T7**, **Scylla Acropolis T9**, and **Leviathan Sunken City** as independent encounter-site assumptions pending binary confirmation.

### D. Conclude with a clean acceptance report
For each rule/feature state **DESIGN**, **SOURCE VERIFIED**, **STATIC PASS**, **CLIENT RUNTIME PASS**, **DEDICATED SERVER PASS**, or **MULTIPLAYER PASS**. Deliver exact branch/commit, mod/JAR hashes, kit/rollback files, source diffs, test logs, encounter evidence, and explicit remaining blocker list.

### Hard preservation rules
- Structure tiers are **not** boss tiers; do not blanket scale named bosses by structure location.
- No overlapping Dungeon Difficulty / party/native/APO scaling without measured caps.
- No universal LOOT table override on a shared chest name without provenance.
- No forced single scarce boss gate, Origin, cursed ring, unique spell school, large party, or rare-only dimension.
- No global increase in spawners/elite population merely to make T6 dungeons harder.
- Don't change user-approved Tiers, PR #45 source roster, current server, Questlog IDs, or shader/performance settings without evidence and rollback.

## Concrete next reply to the user
Report (a) reproduced or not, (b) which of 28+25 rules passed actual Minecraft checks, (c) elite stacking result, (d) T3/T5 loot sample status, (e) whether the two prototype quest milestones are technically feasible, and (f) exactly which unverified user decisions remain.
