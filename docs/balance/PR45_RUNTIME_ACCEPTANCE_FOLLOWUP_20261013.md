# PR45 runtime acceptance and scattered mod reconciliation

Branch: `experimental/pr45-runtime-rpg-acceptance-20261013`, based on PR45 commit `43034ccba85194b5ede1d8a9f5ebc95d3645f72f`. This follow-up changes evidence and test tools only. The PR45 candidate, rollback, production profiles, stable branches, loot and quests remain unchanged.

## Reproduction and baseline

The PR45 kit rebuilt byte-identically: SHA256 `67f329b011eb4b9b541f07de98a958d2369f37724aea5b5dec64278680c2102a`. Candidate SHA256 `a189b392296f6d368a194e107f7da4fd454aa3b490000fd3ab6ede8f3ee15016`; original rollback `fd277736f1c6b4c2d517b2d480b15586696f49e5f17e324e33eb6746a9e6a010`. Ten PR45 safety tests and three inherited difficulty tests pass.

A disposable copy of the original 332-JAR profile launched with the exact installed Minecraft 1.21.1 / NeoForge 21.1.252 production launcher, joined a new flat integrated world, exported native registries and saved/exited with code 0. The separate test addon is additional instrumentation and is excluded from all production packaging.

The real profile later contained 337 physical JARs. All original 332 hashes still match. Frozen 337-JAR rehearsals keep this later context distinct from PR45. The copied existing save was not played; runtime checks create a new disposable flat world. A successful fresh-world test is not existing-save migration, natural generation, combat, performance, dedicated-server or multiplayer acceptance.

## Scattered additions

`pr45-acceptance-evidence/FOLLOWUP_MOD_RECONCILIATION.json` records exact hashes and embedded metadata for Armored Foes 21.1.0, Eternal Nether 21.1.3, Fantastic Wings 21.1.2, Overflowing Bars 21.1.1 and Skeleton AI Fix 21.1.1.

The [latest main note](https://github.com/alsynth/AmbientOdyssey/blob/6a01951e415c784f134147284200863fddadaf6e/docs/testing/V049_LOCAL_MOD_CHANGES_CRASH_20261013.md) is documentation, not a resolved new manifest. All 27 filenames extracted from its candidate/warning bullets already occur in PR45. Its 423 loader-discovered records are not a verified physical top-level JAR count. The note explicitly rejects Mob Plaques and queues Simply More stun and flashing fixes; those fixes are not implemented by this branch.

[PR47](https://github.com/alsynth/AmbientOdyssey/pull/47), [PR48](https://github.com/alsynth/AmbientOdyssey/pull/48) and [PR49](https://github.com/alsynth/AmbientOdyssey/pull/49) add research catalogue rows, not installed mod files. The examined repository releases endpoint returned an empty list. Historical Celestisynth references say deferred/unknown; the owner's current request supersedes that deferral.

**Celestisynth is requested for the next experimental build.** The official NeoForge 1.21.1 port's [1.3.9 file](https://www.curseforge.com/minecraft/mc-mods/celestisynth-1-21-1/files/8867800) is project `1672331`, file `8867800`, `celestisynth-1.21.1-1.3.9.jar`. The actual downloaded JAR passes ZIP CRC and metadata inspection, SHA256 `03225d0ac3789f8cd1df90df1793f080ab36c4c1143a4f15b622f88bb41bd9de`. Required ranges NeoForge `[21.1.0,)`, Minecraft `[1.21.1,1.22)`, GeckoLib `[4.9,)` and PlayerAnimator `[2.0,)` are satisfied by this profile's 21.1.252, 1.21.1, 4.9.3 and 2.0.4 respectively; optional JEI `[19.21.0.247,)` is also met. This is STATIC PASS for artifact/dependency metadata only, not client/server compatibility or progression certification. It is absent from both frozen rosters. Do not report the 337-JAR tests as Celestisynth tests. Material worldgen uses configured/placed features, so crater names must not be fabricated as structure registry IDs.

Eternal Nether introduces three source-verified structures: `eternalnether:catacomb`, `eternalnether:citadel`, `eternalnether:piglin_manor`. All three register in the final client; their three structure definitions, three structure sets and 24 pools resolve to `mod/eternalnether`. Their tiers are unassigned and separate holds preserve the original approved mapping. Native templates, encounters, loot and natural Nether generation need review. Armored Foes changes native mob equipment; synthetic `addFreshEntity` tests do not exercise natural/spawner equipment initialization.

## Native findings

The original 332-JAR client loaded all 53 DD zones and seven difficulty types. All 379 unique structure IDs queried from the reconciled catalogue were registered. Registration is not generation proof. All 153 targeted resources existed; 152 raw hashes matched audited providers. BOMD's `lich_tower` structure set instead came from `cristellib:runtime_pack`, demonstrating why static JAR order is insufficient.

Verified winners include Integrated BOMD for `bosses_of_mass_destruction:lich_tower`, Integrated Cataclysm for `cataclysm:frosted_prison` and `cataclysm:sunken_city`, and `ao_structure_density` for `dungeons_arise:heavenly_challenger`.

Sky Arena and Ice Arena each reference 190 unique native wave entity IDs; 113 per arena were unregistered in the tested roster. Example/unused presets are kept distinct. This proves stale references, not their execution or a crash. It does not authorize automatic deletion or native wave tuning.

`irons_spellbooks:tyros` is unregistered. The later frozen client registered `irons_spellbooks:fire_boss`; installed language assets call it Echo of Tyros, First Flamebearer. Neither this registry check nor the name proves equivalence to the intended T9 encounter or approves a quest gate.

## Controlled rule and rollback rehearsals

Final results and exact probe hashes are recorded in `pr45-acceptance-evidence/ACCEPTANCE_RESULTS.json`. Tests use transient synthetic structure bounding boxes and NoAI/invulnerable ordinary mobs in a new flat world, then remove fixtures before save. They exercise real Minecraft entity join/deferred DD processing, not located natural structures or combat.

The final frozen 337-JAR candidate starts/joins/saves/exits with code 0. All 11 checks pass: one ordinary zombie for each T0–6, passive pig and Wither excluded in T6, an ordinary zombie outside structures and an ordinary zombie in an unsupported T7 site. All 382 queried structure IDs register and all 192 selected resources exist, including the nine native T3/T5 loot tables, which resolve to `mod/dungeons_arise`.

Installed DD/Gson rewrites the candidate copy on load by omitting null-valued object fields. Prepared bytes retain the pinned candidate hash; post-runtime copy SHA256 is `3cd291a4ff26b27dcf7866807ed804404da02d2ec678971ee0dff37d11b4f843`. Parsed configuration matches every effective field after null elision and float tolerance; no runtime semantic tuning occurred. The rollback copy retains its original byte hash and parsed configuration. The original PR45 files are unchanged.

The first fixture attempt exposed a test-helper cleanup error: chunk getters returned unmodifiable maps. The next attempt exposed ordinary unloading/despawning in distant control chunks. Both are recorded as instrumentation failures, not production pack regressions; the final helper copies maps through native setters, forces only its temporary chunks, restores force state and gives control mobs persistence. Failed expectations now emit the launcher's failure marker.

The rollback rehearsal loads the original DD bytes in a separate frozen copy and exports the native parsed configuration. Fresh-world startup plus config restoration is not existing-save or multiplayer rollback proof.

## RPG/loot integration remains gated

The elite safety gate remains unresolved: DD's type/attitude filters cannot distinguish ordinary-ID Apotheosis or Brutal elites. No actual elite stacking encounter was tested, and no combined cap/exclusion is added here. PR45 must remain experimental. Dedicated-server, multiplayer, natural T0/T1/T2/T4/T6 encounters and representative boss/combat acceptance remain pending.

Read-only loot feasibility checks cover three Illager Fort T3 tables (`barrels`, `normal`, `treasure`) and six Foundry T5 tables (`chains`, `lava_pit`, `normal`, `passage_exterior`, `passage_normal`, `treasure`). Their exact IDs and effective resources are included in the final input/export. No wrapper, ratio, currency, recipe or loot chance is changed. The five design roles remain Scrap, Supply, Equipment, Treasure and Grand Treasure; design ratios are not per-roll probabilities.

An optional T3 discovery prototype can use the existing `questlog:visit_structure` objective with registered `skyarena:sky_arena` or `skyarena:ice_arena`. A T5 alternate milestone is feasible as structure discovery, but discovery must not be presented as boss completion. Boss/OR objective codecs, credit semantics, final T5/T6 route choices and owner approvals still require validation. No quest prototype is installed before acceptance. Preserve 52 quests, 13 referenced chapters and 32 FTB pages; the physical local quest directory also contains one unreferenced chapter file.

Keep Scylla/Acropolis T9, Leviathan/Sunken City T7, Tyros T9 and Maledictus/Frosted Prison T7. Geburah and the third T9 End route remain unassigned. Newly discovered Eternal Nether sites require explicit tier decisions after encounter review. No early Mine Cells or Tier0–2 loot changes are made.

## Repeating the check

1. Build `tools/pr45-runtime-probe` with Java 21 and NeoForge 21.1.252. This is a client-only test addon, never a deployment dependency.
2. Use `tools/prepare_pr45_runtime_snapshot.py` on a closed source save. It refuses changed/missing PR45 pins; `--allow-added-mods` records separate additions. Keep the source save exclusively closed during copy.
3. Copy the versioned `RUNTIME_CHECK_INPUT.json` into the snapshot as `PR45_CHECK_INPUT.json`. Use `tools/prepare_pr45_frozen_rehearsal.py` for candidate repeats or `--rollback` without touching the live profile. The helper adds new structure holds and read-only T3/T5 resource checks.
4. Run `tools/run_full_pack_log_probe.py` with the actual launcher install, Java 21, a game directory under repository `build/`, and the test addon. The launcher requires exit 0, world-join evidence and absence of the probe failure marker. Inspect `all_pass` in the synthetic rule report independently.
5. Read the native exports and status ledger. Do not promote or publish a complete playable release on these limited checks.
