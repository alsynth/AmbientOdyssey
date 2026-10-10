# Ambient Odyssey — Repository-wide state

> **CURRENT DEVELOPMENT (10 October 2026):** `main` remains the preserved Test 5 Audit1 rollback. Active work lives on `structure/test6`, now at **v0.3.7-prefreeze-dev3**. The user confirmed Dev2 loads, Dimensional Doors removal resolves the Creative inventory crash and Shader Packs screen works. Dev3 source adds Iron's Jewelry 2.0.2, recommends 10 GiB RAM, corrects first-launch narrator defaults and pins Solas + Complementary Reimagined as official CurseForge shader references. Dev3's shareable ZIP preview is only statically checked; fresh launcher/shader tests are pending. **Ocean expansion is under review** (Aquamirae + Upgrade Aquatic shortlist) before freezing worldgen. Read [live branch current state](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/status/CURRENT_STATE.md), [Dev3 polish](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/testing/RELEASE_POLISH_SHADER_PRESETS_2026-10-10.md) and [Ocean Review](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/testing/OCEAN_EXPANSION_PREFREEZE_REVIEW_2026-10-10.md). Do not treat these development changes as merged to `main` or runtime-certified.

**Updated:** 9 October 2026. **Minecraft:** 1.21.1 / NeoForge 21.1.252.

## Which branch is current?

- **`main`** is still the stable **Test 5 Audit1 rollback baseline**. No Test 6 gameplay release or Test 7 terrain modifications are approved on main.
- **`structure/test6`** contains the **full committed Test 6 *source candidate***: WDA major Overworld/End split, rare Mushroom Fields-only Mushroom Village, eight approved structure addons, AAA Particles, curated structure/biome selectors and the original Claude patch provenance. Import push verified starting at commit `ba8551200f803a37dd8450c1a80da13ebc913967`.
- **Test 6 scoped static checks passed** (247 continuation and 35 focused checks, 246 projects, 1,081 archive entries), **but Minecraft/CurseForge runtime acceptance is not yet performed**. Do not merge Test 6 to main or start Test 7 until real testing is complete.

## Read the active documentation on the Test 6 branch

- [Development status](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/status/CURRENT_STATE.md)
- [Runtime acceptance checklist](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md)
- [Build and verification workflow](https://github.com/alsynth/AmbientOdyssey/blob/structure/test6/docs/handoff/04_BUILD_AND_VERIFY.md)
- [Test 6 work tracker](https://github.com/alsynth/AmbientOdyssey/issues/1)

**User-approved 9 Oct decisions:** Explorify Black Spiral remains **enabled provisionally**, pending Nether compatibility tests; Structory: Towers **v1.0.17, CurseForge 783522:8396885**, replaces prior v1.0.14. These choices are settled; runtime verification is not.

**For every new agent or ChatGPT chat:** If working on Test 6, check out **`structure/test6`** and read its `AGENTS.md` plus the linked current-state and runtime documents. Do not rely on outdated Test 5 prep text on main, old external importer ZIPs or conversation history. Update the active branch's status and source/test artifacts with every change.
