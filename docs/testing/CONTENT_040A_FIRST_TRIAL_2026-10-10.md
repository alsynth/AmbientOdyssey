# Ambient Odyssey 0.4.0-a0 — first small implementation trial

**Status:** experimental full CurseForge importer being built in GitHub Actions; not Minecraft runtime-certified. **Parent:** exact successful Test8.10 version 0.3.8-worldgen-prefreeze-test1.10, user-proven playable. User's original extra visual/fauna list and separate Cosy Critters priority is tracked in [visual addendum](../audits/CONTENT_EXPANSION_VISUAL_FAUNA_ADDENDUM_2026-10-10.md); **the visual packs and Cosy Critters are intentionally not included in this first two-mod quest/controls A/B**, to isolate diagnostics.

## Exactly changed mod pins

| New | Project/file ID | Role |
|---|---|---|
| **Controlling** NeoForge 1.21.1 **19.0.5** | CurseForge **250398:6368976** | Search keybinds and highlight collisions in massive existing mod list; installed Searchables dependency already present |
| **FTB XMod Compat** NeoForge 1.21.1 **21.1.12** | CurseForge **889915:8909889** | Documented FTB Quest integration with JEI item/recipe/fluid ingredient and other FTB mod interactions. Doesn't automatically bridge to future separate Questlog GUI or solve all bad item filters |

Manifest target **269 pinned CurseForge file refs (267 original + 2 additions)**, exact original NeoForge **21.1.252**, all original stable Test8.10 worldgen, 273 native jigsaw NBT aliases, Better Bastions, Luki Woodland Mansions and checksum-pinned NeoReefRedux JAR unchanged. Does not edit FTF, Streams, terrain, biome selectors, loot or item recipes. No dependency auto-update/repin. Trial manifest version **0.4.0-a0-qol-quest-trial**.

## Automated build result — PASS, 10 October 2026

[GitHub Actions run **38055582819**](https://github.com/alsynth/AmbientOdyssey/actions/runs/38055582819) succeeded. GitHub's source and packaged archive checks found:

- **269 CurseForge file references**, including exactly Controlling `250398:6368976` and FTB XMod Compat `889915:8909889`, plus the original two manually important CurseForge files and the original checksum-matched NeoReefRedux embedded JAR.
- **28/28** Test8.4 terrain, **31/31** Test8.6 source-backed jigsaw repair checks and all **273** native terminal NBT replacements retained and parsed from the final archive; Graveyard, Swiss village, beach lighthouse and city checks passed.
- Full ZIP CRC/manifest validation passed. Two complete rebuilds were **byte-identical**.
- **Inner CurseForge importer ZIP:** `Ambient-Odyssey-0.4.0-a0-QOL-Quest-TRIAL-PRIVATE.zip`, **70,814,387 bytes**, **1,386 ZIP members**.
- **SHA-256:** `d2cdb358ee739447998123cce4e875d5cd6485b6f12ffbb35fa99d329ff9e70e`.

The CI download is an outer wrapper around the **inner** importer ZIP; import only the inner one. **CI is not a successful Minecraft runtime test.** No guarantee of JEI clickthrough, hotkey GUI compatibility, Questlog integration, solo-task correctness or multiplayer success until the dedicated trial steps below pass.

## Safe usage and actual functional gates

1. Import the **inner** full CurseForge manifest ZIP to a new **disposable CurseForge instance**, not over the working Test8.10 profile; do not start the final multiplayer server world.
2. Confirm all expected mods resolve to official exact 1.21.1 NeoForge files. Launch main menu and load a copy/new world, then exit normally. Check startup log for missing deps and mixin conflicts, especially Searchables, FTB Quests, JEI and existing inventory mods.
3. Open **Controls → Key Binds**; Controlling search must filter and identify duplicates, without losing prior mappings. Test one deliberate duplicate, then restore original user settings.
4. Open **JEI** and an existing FTB Quest with an item or recipe task. Verify compatibility integration actually renders clickable recipe references and interactions. Questbook must not crash when selected JEI item has components/tags or when viewing modded items.
5. Make **one sample FTB Quest** to verify any Apotheosis gem broad-match filter accepts appropriate variants, rather than inferring FTB XMod Compat repairs broken filter SNBT automatically. Try player A/B independent completion using FTB Solo Quests before making the final questbook.
6. Test existing Better Inventory/Curios/Accessories screens, hotkey overlays, shader menu and one multiplayer join; there should be no novel UI focus/hitbox collision.
7. Capture **latest.log** and any failed task/recipe details only if needed; do not assert runtime success based on GitHub CI.

## Build safeguards and rollback

CI [run link from the latest trial workflow](https://github.com/alsynth/AmbientOdyssey/actions/workflows/content040a-qol-trial-build.yml) verifies new exact pins, 269 CF refs and all 273 previous worldgen NBT fixes, native initial room/biome/regression scripts, CRC, NeoReef checksum and **bit-identical dual full builds**. The source-builder output is independent of developer-machine filenames. CI **cannot** simulate actual player controls, JEI focus, solo quest item matching, server start or shader GUI.

**Rollback:** the original [Test8.10 known-playable branch](https://github.com/alsynth/AmbientOdyssey/tree/worldgen/test8.10-all-documented-pools) and exact SHA256 **0bfec2560337369fed08fc70329e00f337ee6281a8676a0e4e2ccb9f6751d71f** are untouched. Do not merge content trial to main until actual playtesting and user approval.
