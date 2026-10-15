# Ambient Odyssey — 14 Oct 2026 full-import reconciliation for Work mode

**Status: documentation-only packaging handoff. No release assembled, no merge, no gameplay/runtime acceptance of the combined loot overlay.** Minecraft **1.21.1**, NeoForge **21.1.252**. Repository `alsynth/AmbientOdyssey`.

Use the companion **[20261014_EXACT_CHANGE_INVENTORY.json](20261014_EXACT_CHANGE_INVENTORY.json)** as the canonical *machine-readable complete ledger*, including all source path additions/modifications/removals across the recent relevant branches, all exact CF file/project IDs and SHA1 values, the 338 expected physical JAR filenames, and the log-to-manifest comparison. The summary below distinguishes **already in PR #50**, **new in PR #51**, **only present in a local player's test**, and **still proposed**.

## 1. Baseline to preserve — PR #50, not main

| Field | Pinned source |
| --- | --- |
| Head | `experimental/pr45-runtime-rpg-acceptance-20261013`, draft PR **#50** |
| Exact client import | `Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip` |
| SHA256 | `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f` |
| Bytes | 154,378,233 |
| Official manifest refs | **338 = 331 mod + 7 resource/shader** |
| Bundled original private mods | **7** exact unchanged JARs |
| Physical production mod JARs | **338** |
| Quest and manual | **52 Questlog quests**, **13 referenced chapters**, **32 Field Manual pages** |

This is the latest **known native-tested full-import payload**. Client startup/fresh flat world/save-exit passed, as did 11 synthetic difficulty checks. It is **NOT** a CurseForge UI acceptance, natural exploration, elite stacking, multiplayer, existing-save migration or dedicated-server acceptance. `main` remains a historical rollback, not the release base.

Exact official CurseForge roster and bundled private JAR SHA256: `docs/balance/pr45-acceptance-evidence/FULL_IMPORT_INPUTS.json` **on PR #50**, reproduced in the companion JSON. Preserve every manifest pin and unchanged payload member.

## 2. Mod JARs newly included or updated in PR #50

These are **already part of the PR #50 full-import ZIP**. **Do not add them a second time.** All 10 added references and the 1 updated reference have explicit projectID/fileID/SHA1 in `20261014_EXACT_CHANGE_INVENTORY.json`.

**10 added to the complete v049 export:**
- Armored Foes `ArmoredFoes-v21.1.0-mc1.21.1-NeoForge.jar`
- Reliquified Ars Nouveau `reliquified_ars_nouveau-1.21.1-0.6.1.jar`
- Fantastic Wings `FantasticWings-v21.1.2-1.21.1-NeoForge.jar`
- Skeleton AI Fix `SkeletonAIFix-v21.1.1-1.21.1-NeoForge.jar`
- Overflowing Bars `OverflowingBars-v21.1.1-1.21.1-NeoForge.jar`
- Ars Delight `arsdelight-2.2.5.jar`
- Eternal Nether `EternalNether-v21.1.3-1.21.1-NeoForge.jar`
- Ars Sophisticated Storage compatibility `arssophisticatedstoragecompat-0.3.0.jar`
- Ars Sophisticated Backpacks compatibility `arssophisticatedcompat-0.3.0.jar`
- Celestisynth `celestisynth-1.21.1-1.3.9.jar`

**1 updated official artifact:** Remnant Bosses `remnant_bosses-neoforge-1.21.1-2.7.0.jar`, CF **1225026:9145897**.

**No other original frozen mod JAR was removed or updated** in PR #50's hash-verified 332 → 337 → 338 reconciliation. The nine non-Celestisynth additions were already installed in the later reconciled local context; Celestisynth is the added tenth. Its GeckoLib and PlayerAnimator requirements were checked in the installed profile. Do not mistake a separate **mod update** for a whole new mod.

## 3. Other already-included changes leading up to PR #50

- **Performance and visuals (PRs #40–42):** added entity culling config, Euphoria Patcher settings, Oculus/graphics config, balanced/quality/performance shader note files, Streams Reflowing client sound settings; removed outdated `release_030/overrides/config/equipmentcompare.toml` and `release_030/overrides/config/legendarytooltips.toml` *source config files* (this did **not** mean deleting those mods). Updated `particular-common.toml` (particle frequency/lifetime) and `alexsmobs.toml` (reduced four wildlife spawn weights; exact values in `docs/performance/v049-followup/CHANGES.json`).
- **Structure difficulty (PR #45 and follow-up #50):** authored the **53-rule** Dungeon Difficulty candidate, 46 Overworld + 2 End + 5 Nether. The original config and rollback are preserved. PR #50's complete import already overlays this candidate and includes native source checks; do not replace it with old default `difficulty_v2.json`, another branch's WIP tier mapping, or research-only boss designs.
- **Eternal Nether holds:** Catacomb, Citadel and Piglin Manor are **unassigned** until actual natural encounter/spawner/attribute testing. Do not invent tiers or globally rewrite `minecraft:chests/bastion_hoglin_stable` (shared loot).
- **Preserved systems:** existing worldgen, original structure loot economy, Mine Cells/Connector handling, Questlog, FTB manuals, random-affix armor trims, both experimental content ports and old custom integrations. PR #50 already has **7** exact custom JARs with hashed provenance. Preserve, do not recompile casually.

Full explicit per-path diff since r19: machine ledger key `PR50_from_v049_export.complete_changes_vs_r19` (**127 files**, including documentation/tests, config modifications and two removed config paths). Read exact `status`; don't treat documentation and probes as deployable mods.

## 4. New to package — PR #51 loot economy overlay

Source: `experimental/loot-economy-first-pass-20261013` (draft PR **#51**), **31 changed source paths versus PR #50**. No unrelated early/midgame chest rewrite.

**Add**:
1. Compiled production **`ao-starter-chest-0.1.0-experimental.jar`**, from a successful *latest matching source* GitHub Actions artifact (e.g. [run 38486539260](https://github.com/alsynth/AmbientOdyssey/actions/runs/38486539260)); source under `addons/ao-starter-chest/`. Bundled in `overrides/mods`. Do NOT ship `StarterAffixGameTests.class`, a native test probe or another debug JAR. This increases custom mods **7 → 8**, and physical production mods **338 → 339**, with official CurseForge refs **unchanged at 338**.
2. `ao_goblin_trades` Paxi datapack under `release_030/overrides/config/paxi/datapacks/`: 4 Goblin-Tuned chainmail prices **32 diamonds + 4 Cinder Essence each**. Contains the **complete native 22-offer epic JSON** extracted from official, SHA1-verified Goblin Traders 1.11.2; output armor modifiers, durability and all other offers preserved.
3. `ao_starter_apotheosis_exemptions` Paxi datapack: **only** the Bonus Chest skips native Apotheosis random affix conversion/injection and gem injection. Other ordinary dungeons retain Apotheosis baseline chance rules. Native Apotheosis 8.9.0 diff parity verified.
4. Lootr config `lootr-common.toml`: add `minecraft:chests/spawn_bonus_chest` to `loot_table_forced_whitelist`, keep `randomise_seed=true` and `team_loot=false`.

**Change** existing Flight Rings recipes in existing `ao_flight_balance` Paxi datapack:
- Basic: diamond → **Nether Star**.
- Advanced: **2 Eyes of Ender, Cinder Essence, 2 Netherite Ingots, Basic Ring, 2 Iron's Spells Arcane Ingots, Ars Nouveau Air Essence**; remove **Echo Shard and redundant extra Nether Star**.

**Starter Bonus Chest ONLY**:
- One of Blazing Core / Heart of the Golem / Will of the Ocean / Angel Blessing / Lost Engine, equal **20% each**.
- Exactly one genuine Apotheosis Common **55%** / Uncommon **30%** / Rare **15%** affixed item.
- **32–48** torches; **16–48** one random cooked meat type (beef/pork/chicken/mutton).
- The compiled addon carries a vanilla `minecraft:chests/spawn_bonus_chest` table and real Apotheosis affix generator. Work must test whether actual world-created chest converts to Lootr and lets each player independently roll.

**Build proof:** synthetic packager and JSON tests passed; isolated **600 native affix rolls / 2 GameTests passed**, plus pinned Enigmatic Legacy Plus **1.21.1-1.1.2** native startup/table parse with 2/2 tests passed ([run 38486534096](https://github.com/alsynth/AmbientOdyssey/actions/runs/38486534096)). These are **not full-pack multiplayer proofs**.

**Packaging command from PR #51 checkout:**

```sh
python tools/package_ao_loot_economy_pilot.py \
  --base Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip \
  --starter-jar ao-starter-chest-0.1.0-experimental.jar \
  --output Ambient-Odyssey-v0491-LOOT-PILOT.zip
```

The tool rejects the wrong base SHA256, preserves unrelated payload and manifest pins, writes a sidecar hash report, and outputs a new file. If the original full-import archive is inaccessible, locate the **exact** PR #50 artifact or reconstruct it using `tools/package_pr45_full_import.py` and its own hash-checked original inputs; **do not substitute a similarly named older v049 client ZIP or blindly repack `release_030`**. If exact content cannot be recovered, mark BLOCKED and request the archive.

## 5. October 13 local mod log — additions/removals accurately classified

Input: actual `latest(20261013-182534).log`, previously uploaded; timestamped *player local client*, not an endorsed manifest. The report says **423** `Found mod file` events, which include child JARs, injected Connector names and core runtime JARs; **not 423 top-level installable mods**. Of these, **333** are top-level `mods folder locator` JAR filenames.

Comparison with **338** PR #50 physical JAR filenames:
- **332 exact matches**.
- **Only local-only candidate: `MobPlaques-v21.1.1-1.21.1-NeoForge.jar`**. **REMOVE / EXCLUDE**; owner explicitly rejected Mob Plaques. Do not include merely because it appears in their local test.
- **6 baseline names not seen as direct mods-folder filenames**: 5 have clear transformed/JIJ representations in the same log (Cardinal Components API, Connector, Kotlin for Forge, Mezz Config, Mine Cells); these are **not verified removals**. The sixth, **Celestisynth**, was newly reconciled into PR #50 after the player's logged local instance. See exact six explanations under `LOCAL_OCT13_log_reconciliation.missing_from_direct_mod_folder_entries`.

**Conclusion:** No evidence for an approved extra 80+ mod content expansion. Work should not blindly copy the raw player `mods/` folder or make 423 downloads. Treat the PR #50 hash-verified manifest + PR #51 as the authority. The full **333 exact local filenames** and **338 PR #50 filenames** are in the companion JSON.

## 6. Explicitly remove or defer

| Item | Status for THIS combined ZIP |
| --- | --- |
| Mob Plaques | **Exclude**, explicitly rejected. Do not add a CF reference |
| Old `equipmentcompare.toml` / `legendarytooltips.toml` | Removed **config files** on performance branch; do not accidentally restore |
| Simply More **Stun** client/server crash | **NOT FIXED YET.** Owner wants Stun disabled. Must research/implement reversible safe block separately; do not mark as complete because pack starts |
| Fatal/intense flashing (Simply More Lustrous Moxie among suspects) | **NOT FIXED YET**. Owner requested disabling; visual-only fix preferred |
| Rage Glove Tier 7 Nether boss gate | **Design approved, NOT IMPLEMENTED** until Claude confirms exact boss/source paths |
| v0.5 bosses, quests, Regalia PRs #44, #47–49 | **Research only**, not runtime modifications; don't auto-import gear or quests |
| Origins experiments / other unmerged feature branches | **Not part of this approved baseline** without an explicit separately tested change |
| Entire early/midgame loot system, Simply Swords unique damage, Apotheosis World Tiers | Preserve current loot; latter two are future investigations, not signed-off code |
| Saves, logs, crash reports, player/account metadata, probe/debug JARs | **Never include** |

## 7. Work mode — assembly and acceptance requirements

1. Read `AGENTS.md`, this handoff, exact inventory JSON, PR #50 full-import evidence, PR #51 build/test notes and `docs/testing/V051_LOOT_ECONOMY_PILOT_ACCEPTANCE.md`.
2. Resolve exact PR #50 ZIP (SHA256) plus latest approved starter JAR build. Confirm all official CF refs and 7 original JAR hashes. Do not merge drafts into main.
3. Apply **only** PR #51's explicit deployable changes. Do not pack source Java, CI YAML, research/evidence, Questlog test probes or entire Git branches into player `overrides`.
4. Run `tools/test_ao_loot_first_pass.py`, `tools/test_ao_loot_packager.py`, pinned Goblin/Apotheosis diff validators, verify addon JAR content, 52 quests/13 chapters/32 manual pages, JSON syntax, all ZIP members/CRC and no duplicate paths. Run the builder twice and compare *normalized* contents/hash when reproducibility is intended.
5. New profile import → full client startup → bonus-chest ON/OFF in fresh worlds → inspect JEI and trade offers; then **two distinct non-operator players on a dedicated server** to verify independent Lootr rewards. Confirm no duplicate affix/gem injected and actual affixes/trims. Check original structure/boss/dimension/Questlog behavior survives.
6. Save test results and changed-file inventory, exact final ZIP SHA256, official manifest pin count, custom JAR names and hashes, known issues, and rollback hash as a new draft PR comment or new evidence document. If any gate fails, **keep draft and mark incomplete**.

**Important:** Work mode can assemble and test, but the manifest comparison is NOT consent to arbitrarily include new mods or fixes. The packaging target is PR #50 **plus** fully identified PR #51 changes, excluding Mob Plaques. Current production release remains untouched.
