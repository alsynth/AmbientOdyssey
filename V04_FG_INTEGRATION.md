# Ambient Odyssey v0.4 — Mine Cells + 0.4f/0.4g integration

**Date:** 10 October 2026 · **Current experimental branch:** `experimental/v0.4-minecells-fg-integration-20261010` · **Minecraft:** 1.21.1 · **NeoForge:** 21.1.252 · **330 pinned CurseForge references**.

## Baselines and provenance

- Source baseline: `experimental/v0.4-complete-20261010` commit `9639af07d891e8f132325dc21290d54ca66a792f`. The 318-reference Mine Cells candidate had a passing Github Actions build and generated two ZIPs; its exact old hashes remain in `docs/testing/v04-evidence/release-validation.json`.
- Added native content from `content/0.4.0d-content-first-expansion` commit `797b55420015c5c4211f8f54871eab753ed0a546`: seven 0.4f and five 0.4g projects, whose branch CI previously passed.
- Retained Mine Cells 2.0.3 + Sinytra Connector beta.17 + FFAPI 2.3.5, inherited owo-lib, and Iceberg/JamLib. No change to the 273 inherited NBT patches, FTF/biome selectors, all 0.4e projects, 30% sleep, rarity defaults, or earlier environmental data repairs.
- Kept Subtle Effects 1.14.0 from the Mine Cells candidate instead of silently adopting an unrelated 1.14.1 repin from the 0.4g branch.

## Newly integrated native NeoForge additions

**0.4f:** Armor Trim Item Fix, Shulker Box Tooltip, Crafting Tweaks, Chat Heads, Sound Physics Remastered, Polymorph, and Brewin' And Chewin'.

**0.4g:** Dimensional Dungeons, Ancient Remnants: Monoliths, TarotCards: Remastered, Aquaculture Delight, and End Remastered Additions.

Exact project and file IDs are in `release_030/release-lock.json`; integration gates `tools/validate_v04_fg.py` verify them. Retained source/audit analyses under `docs/audits/CONTENT_EXPANSION_040F_2026-10-10.md`, `CONTENT_EXPANSION_040G_2026-10-10.md`, and `CONTENT_FUTURE_DECISIONS_040G.md`.

## Validation and next checks

GitHub Actions `.github/workflows/v04-experimental.yml` is configured to build a private NeoReefRedux developer ZIP and a CurseForge reference-only ZIP, validate root manifest, exact pins, NBT/JSON worldgen repairs, 4 Mine Cells negative bridge regressions, and identical repeat build. **GitHub CI is not client, gameplay, or full dedicated server runtime evidence.** Check the actual run conclusion and downloadable artifact before declaring build success.

Perform `V04_TESTING_CHECKLIST.md` in a fresh disposable world. Pay special attention to Sound Physics/Atmosfera/Streams ambience layering, Polymorph's recipe selector, Curios/Tarot card stacking, all dimension transitions, Ancient Remnants' biomes, extra End Remastered eyes and new server-side dependencies.

Neither experimental branch nor ZIP should overwrite the earlier preserved 318-ref artifact or a working test instance. Quests, worldgen freeze, optimization, multiplayer acceptance and publication permission remain separate later gates.
