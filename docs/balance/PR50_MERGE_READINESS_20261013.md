# PR #50 merge-readiness report — 2026-10-13

**Decision: HOLD. Do not merge.** PR #50 remains open and draft. Its head branch is `experimental/pr45-runtime-rpg-acceptance-20261013`; its exact base/target is `experimental/structure-difficulty-v3-20261013` at `43034ccba85194b5ede1d8a9f5ebc95d3645f72f`. The PR is not merged. The PR #45 candidate, rollback configuration, full-import ZIP, and existing rollback artifacts remain intact.

The acceptance record separates native production-client results from controlled engine fixtures and static/source analysis. No result below certifies behavior outside its stated test scope.

## Verified runtime behavior

The 338-mod production roster, including Celestisynth 1.3.9 and Eternal Nether 21.1.3, started with Minecraft 1.21.1 / NeoForge 21.1.252 in a disposable client copy, created and joined a new flat integrated world, saved and exited with process code 0. The full import SHA256 is `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f` (154,378,233 bytes). The probe found all 382 queried structure registrations and all 192 selected resources; the three queried Celestisynth entity registrations were present. This was not a CurseForge UI import or an existing-save migration.

In the same full roster, 11 test fixtures exercised Minecraft entity-join processing and Dungeon Difficulty in synthetic structure bounding boxes: ordinary zombies at tiers 0–6, passive pig and Wither exclusions at tier 6, an ordinary zombie outside structures, and an ordinary zombie at an unsupported tier-7 site. All 11 expected attribute outcomes passed after 50 ticks. This was an engine-level rule simulation using test-created entities and structure starts, not natural generation, elite initialization, or combat. The exact cases are in `pr45-acceptance-evidence/337_ORDINARY_RULE_TESTS.json` for the 337-JAR rehearsal; the full-import run summary is `pr45-acceptance-evidence/FULL_IMPORT_RUNTIME_RESULTS.json`.

The full import ships 338 production mod JARs. Its one extra test-only instrumentation JAR was excluded from the import and is not part of the roster or downloadable package.

## Acceptance gates

| Gate | Evidence and status | Merge requirement |
|---|---|---|
| Natural encounters | **Search attempted; no encounter verified.** A disposable normal-terrain survival world was created with the full 338-mod roster. On seed `48127`, the native search found no Catacomb, Citadel or Piglin Manor start within 32 Nether chunks. The probe exited 0, but a single 40,001 ms integrated-server tick was logged inside Eternal Nether's Catacomb placement check during the bounded locate search. No mobs, spawners, elite initialization or encounter were observed. Details are in `pr45-acceptance-evidence/NATURAL_ENCOUNTER_RUNTIME.json`. | Run a targeted candidate-placement test that avoids broad locate scans, generate each actual start, and inspect its mobs, equipment/modifiers, spawners and structure-specific encounter behavior. Review the locate-search stall separately. |
| Difficulty and elite stacking | **Ordinary-mob simulation passes; elite safety unresolved.** The 53 DD zones are 46 Overworld, 2 End and 5 Nether. The maximum configured ordinary-mob bonuses are +50% max health, +25% attack damage and +2.5 armor at tier 6. The filters match vanilla hostile entity IDs; the simulation does not initialize Apotheosis affixes or Brutal Bosses. There is no demonstrated combined cap or elite exclusion. | Test initialized Apotheosis and Brutal elites in representative tiered structures; measure their final attributes and damage. Set and verify a safe combined ceiling or add a proven elite exclusion before lifting the hold. |
| Eternal Nether tiers | **All three remain unassigned.** See evidence-based comparison below. No tier, DD zone, loot override or quest gate was added for these structures. | Observe natural layouts and initialized encounters, compare player-facing strength to the existing tier anchors, then make an explicit tier decision. |
| Celestisynth combat | **Not runtime-verified.** The exact artifact and dependencies passed static checks, the full client loaded, and the three queried entities registered. No weapon was acquired, used, or tested against a target. | Test normal attacks, special activations, damage sources/effects, and interactions with Apotheosis, Iron’s Spells ’n Spellbooks, Mowzie’s Mobs and other active combat mods. Include the known Simply More stun/fatal-flicker issue in the combat review. |
| Dedicated server and multiplayer | **Not tested.** Existing evidence covers a single-player integrated server only; there was no dedicated-server startup, second-client join, player-to-player session, server save/restart, or reconnect test. | Run the server-compatible roster on a disposable dedicated server; join from two clients, exercise a representative encounter, save, restart, reconnect and check world/player state. |
| Changed files and target | **Reconciled.** The current PR diff is 43 files against `experimental/structure-difficulty-v3-20261013` at `43034ccba85194b5ede1d8a9f5ebc95d3645f72f`. This continuation adds six files (the report, probe, and four evidence files) and updates two test-support files. No pack mod, candidate/rollback configuration, quest, loot, or worldgen payload was changed. The PR branch’s candidate and rollback bytes retain their recorded hashes. | Review the exact PR diff against the target branch and retain the draft status until all runtime gates above pass. |

## Eternal Nether comparison against the current tier model

The current mapping has user-approved Tier 4 for the Nether Fortress and Tier 5 for Bastion Remnant; major end-of-campaign End structures occupy Tier 6. These are comparison anchors, not automatic assignments to new structures.

* **Catacomb — hold, between the known Nether anchors pending a real encounter.** The source graph reaches 19 templates and includes one ordinary Wither Skeleton spawner template. Native feature code also selects weighted Catacomb mobs (Corpor, Wither Skeleton Knight, Wraither and vanilla Wither Skeleton); a template-only spawner count would miss that path. The active mob count, equipment, elite modifiers, damage and assembled structure variation were not observed in game.
* **Citadel — hold, likely a Nether combat site but not tierable from current evidence.** Five templates form its traced structure graph. It has no ordinary spawner in those templates; native code adds a configured Warped Enderman feature. Actual spawn frequency, attributes, modifiers and player exposure remain unknown.
* **Piglin Manor — hold, compare against Tier 4–5 Nether sites after a natural run.** Two templates trace indoor weighted Piglin/Piglin Hunter spawns and an outdoor mounted encounter path. The structure reuses vanilla Hoglin Stable loot, so that shared table is not evidence for a global loot change or a distinct reward tier. Encounter count, rider behavior, gear and initialized strength remain untested.

The exact provider hash, definitions, pool/template reachability, feature references and NBT template scan are recorded in `pr45-acceptance-evidence/ETERNAL_NETHER_ENCOUNTER_GRAPH.json` and `ETERNAL_NETHER_NATIVE_MOB_FEATURES.txt`. They are source/JAR evidence, not world-generation results.

## Remaining manual and runtime checks

The next acceptance run should use disposable worlds and the exact 338-mod import. A broad native `findNearestMapStructure` search stalled the test integrated-server tick at 40 seconds without finding a start; use a targeted candidate-placement approach and record the resulting natural coordinates/seed, structure pieces, actual spawner contents, spawned entities, equipment, and final health/attack/armor with modifier sources. Repeat in a representative tier-5 site with Apotheosis and Brutal Bosses active to check combined strength and elite stacking.

For Celestisynth, acquire and test at least Solaris, Rainfall Serenity and Frostbound: basic hits, right-click and shift-right-click skills, and the weapon-specific projectile/mark/area effects against a controlled target. Capture damage source, health loss, status effects, cooldown/resource changes and any crash or visual/screen-effect issue. Repeat relevant target interactions with the installed spell and combat mods. Static language descriptions are test ideas, not results.

For multiplayer, prepare a dedicated-server roster from the exact import, launch it, join from two clients, save, stop and restart the server, then reconnect and verify player/world persistence. Record server/client logs, exact roster hashes, exit codes and the seed. No manual test result should be entered as passed without the recorded run evidence.

## Merge disposition

The client-load, fresh-world and ordinary-rule checks are useful but do not satisfy natural encounters, elite stacking, combat or multiplayer acceptance. Keep PR #50 draft and unmerged. Keep Catacomb, Citadel and Piglin Manor unassigned, and do not claim full merge readiness until the remaining checks are recorded and reviewed.
