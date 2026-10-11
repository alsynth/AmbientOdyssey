# Current development (11 October 2026)

**This older 10 October snapshot is superseded for active engineering.** Read [v0.4.1/v0.4.2 live source and regression ledger](V042_ACTIVE_DEV_20261011.md). The latest private combined experiment is **329 CurseForge references** (not the 331-reference historical Q1 candidate below), with approved TREK/Create rarity and a separate FTB Manual task completion hotfix. Hominid's newer 0.1.1 source remains a **runtime-untested** experimental prototype, and Curios amulet-slot compatibility is a separate test candidate. Do not promote any of these to stable based on source/ZIP CI alone.

---

# Ambient Odyssey — Current state

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
