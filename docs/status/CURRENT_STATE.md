# Ambient Odyssey — Current state

**15 October integration continuation:** use [Implementation progress](IMPLEMENTATION_PROGRESS.md) for the current source/package/test/blocker ledger on draft PR64. Historical entries below describe earlier baselines, not the active integration status.

## 14 October — full PR54 campaign experiment

Isolated branch experimental/full-pack-through-pr54-20261014. Full test ZIP uploaded before combined tests: 338 CF references, 10 custom JARs / expected 341 physical mods; 153 journal entries / 20 chapters, preserved 32 manual pages. Broad deferred-design request is partly implemented. See [scope and evidence](../testing/FULL_PR54_CAMPAIGN_20261014.md). Do not call it complete or runtime accepted.


**As of 10 October 2026.** This page is the current handoff, not a chronological log. Previous 64 KB handoff preserved in [full historical status](../archive/history/CURRENT_STATE_full_2026-10-10.md).

## Current working source

- **Content candidate:** `experimental/v0.4h-q1-ftb-field-manual-20261010`, verified packaging source `9a5db8ea0ac16b8b55a6929e6819e6b8479178a0`.
- **Repository housekeeping only:** `maintenance/repo-organization-20261010`. Docs/archive/workflows cleanup is isolated from the content candidate and should **not be called a new tested modpack**.
- **Target:** Minecraft 1.21.1, NeoForge 21.1.252, 5–7 players. **331 exactly pinned CurseForge project/file refs** in `release_030/release-lock.json`.
- **Content:** Mine Cells via Fabric-to-NeoForge Connector, 50 Questlog Q1 quests / 13 chapters, 32 FTB educational reference pages / 3 chapters, inherited WDA quests and worldgen repairs including 273 terminal jigsaw fixes.
- **Architecture:** Questlog = narrative / objectives / light rewards; FTB Quests = detailed reference manual, original WDA campaign retained, FTB Solo Quests preserved.

## Last successful source/package checks

[GitHub Actions run 38080830259](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259) **success**, [full artifact 11680318532](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259/artifacts/11680318532).

| Package within the artifact | Exact SHA-256 |
| --- | --- |
| `Ambient-Odyssey-v0.4h-Q1-FieldManual-PRIVATE.zip` (70,913,371 bytes) | `c7493ce19dc7833b5bf06fb322159689eebe3629d0bc001bff4617a50d3d33ca` |
| `Ambient-Odyssey-v0.4h-Q1-FieldManual-CF-References.zip` (70,840,821 bytes) | `c4b7fa1595a4aa99f6cc9a504266c5acaf6518c7a47b67186cc69473a6fbd88b` |

The private package was rebuilt twice byte-identically; FTB/Questlog/ZIP/331-ref/worldgen static validators passed. **This is not a Minecraft runtime PASS.** The private test-only optional NeoReefRedux JAR must not be treated as permission for public CurseForge redistribution.

## Blockers / next acceptance gates

1. **Client boot**: actual 331-mod instance, no fatal loading/mixin failures. Earlier restricted or inaccessible native binaries leave 23 metadata audit gaps until exact installed jars are scanned.
2. **UI**: Questlog journal/inventory button at trial (38,38), 50 quests/13 chapters; FTB 32 reference pages; JEI, Curios/Accessories, default GUI scales and keybinds. No collision or stale text. See [admin guide](../questing/QUESTLOG_ADMIN_GUIDE.md).
3. **Content mechanics**: Questlog `read`, item objectives, rewards once only, FTB empty-task page behavior and WDA rewards unaffected. Test separate per-player states and restart persistence.
4. **Worldgen**: modded vs vanilla biome structure eligibility, Farmers Structures spawning, overlapping/clipped WDA/Iron's structures, Mine Cells portals/return, Dimensional Dungeons, 30% sleep rule, loot/recipes.
5. **Performance/ambience**: water and rain overpowering wildlife, missing under-canopy nature sounds, high modded chunk generation time, FPS/MSPT, shaders and 5–7 player server benchmarking.
6. **Quest expansion**: do not invent modded boss/entity/structure/item IDs. Verify installed content before authoring Q2 adventure triggers; no mandatory curse, Origin or inaccessible structure gates.

## Pointers

- [Next actions](../../TODO.md), [Agent handoff](AGENT_WORKFLOW.md), [Repository map](../maintainers/REPO_MAP.md).
- [Q1 quest implementation](../questing/QUESTLOG_Q1_IMPLEMENTATION.md), [FTB Manual implementation](../questing/FTB_MANUAL_Q1_IMPLEMENTATION.md).
- [Q1 runtime matrix](../questing/QUESTLOG_Q1_RUNTIME_TESTS.md), [full first-test field sheet](../testing/V04H_TEST_SESSION_FIELD_SHEET.md).
- Historical Q1-only candidate [38079305682](https://github.com/alsynth/AmbientOdyssey/actions/runs/38079305682), launch-ready 331-mod no-quest candidate [38077302870](https://github.com/alsynth/AmbientOdyssey/actions/runs/38077302870), and Test6/8 historical reports remain accessible in Git history and the archive.

## 12 October � two-addon fixes

Isolated branch `fix/affix-trims-questlog-placement-20261012`, based on v045 `6228a5a`. Armor trim addon 0.1.1: eight native tests PASS (factory, old drops/chests, preservation). Questlog bridge 0.1.5: actual native client screenshots and click/return PASS at GUI scales 2/3/4. Separate update kit and v045.1 test import, all 330 original pins unchanged. Full AO overlays/multiplayer remain pending. See [evidence and install instructions](../testing/ARMOR_TRIMS_QUESTLOG_FIX_2026-10-12.md). v046 ports remain separate.

## 12 October - current full-pack diagnostic build

`content/v048-consolidated-whaleborne-test-20261012`: exact v045.1 full base plus supplied Apotheotic 0.4.8 prototype, available Wet Sand prototype and official Whaleborne 1.2.5. 331 CF pins; armor/Q fixes retained. Production full-roster client/world join/save PASS; Depths and Aether gems fail their missing-ID lookups. Prototype is intentionally unfinished. See [full build and findings](../testing/V048_CONSOLIDATED_FULL_PACK_2026-10-12.md). User accepts Malkuth/Mine Cells; dungeon spawners wait for next playtest log; keybinds and other repairs follow consolidation.

## 12 October - tooltip and startup compatibility fix

v048.1 uses SimplyTooltips as the single scrollable renderer, with tabs off so affixes remain in the same view. Legendary Tooltips borders/previews and Equipment Compare panels are temporarily disabled through configs. WorldWeaver welcome/update popups are skipped. Actual full-roster UI and native wheel checks passed at scales 2/3/4; prototype gem errors are recorded and deferred. No pins or bundled mods changed. See [UI patch evidence](../testing/V048_TOOLTIP_STARTUP_FIX_2026-10-12.md).

## 12 October - r8 integrated manual-test build

v048.2 replaces only the Apotheotic prototype with supplied r8 SHA 05639f00... and refreshes test notes. Full-roster client/world/save PASS; 60 gems now load and the two old gem parse failures are absent. One Cornelia crafting recipe has a missing Aquamirae ID; recorded without modifying the JAR. Latest UI fixes and all 331 pins retained. See [r8 checks](../testing/V0482_R8_FULL_PACK_2026-10-12.md).

## 12 October - current v0483 test candidate

v0483 adds Seven Curses Ender Chest access below Better Inventory tool slots, gated by equipped ring and native config. Actual full-roster client layout/equip/original chest packet/unequip checks PASS at scales 2/3/4. Subtle Effects and its exclusive End Remastered patch removed after user crash testing; 329 CF pins. Q now sits above the right armor panel as requested; existing r8, trims, Whaleborne and tooltip/startup fixes preserved. Manual edge cases and crash-mob regression remain. See [checks](../testing/V0483_RING_INVENTORY_2026-10-12.md).

## 12 October - current r19 diagnostic candidate

v0484 replaces the supplied r8 port JAR with verified r19; owner compiled/all 30 GameTests PASS. Actual full-roster client/world/save PASS, 60 gems and no observed port parsing or mixin failure; Cornelia error absent. Latest Q/E positions and all 329 pins preserved; Subtle Effects remains removed. Manual gem/full-server/multiplayer acceptance pending. See [r19 evidence](../testing/V0484_R19_FULL_PACK_2026-10-12.md).

## 12 October - performance overhaul preparation

Owner authorizes performance work on latest r19 base. Target: Ryzen7600/RTX4070, 32GB, 1440p144Hz, client10-11GB; separate rented12GB server and planned10k+ pregen. Prioritize Complementary Reimagined/Euphoria, particles, culling and warm-chunk multiplayer. Sodium/Iris swap has exact metadata blockers. Candidate presets/benchmark tools prepared; active pack unchanged and no measured gain claimed. [Runbook](../performance/V049_OVERHAUL_PREP_20261012.md).
