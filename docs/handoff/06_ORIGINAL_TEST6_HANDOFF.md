# Original Structure Test 6 handoff supplied by the user (historical snapshot)

**Date:** 9 October 2026. **Baseline:** v0.3.1 Structure Test 5. **Target:** Structure Test 6 before terrain/biome Test 7.

**Objective:** Build reproducible Test 6 with eight approved mods, ordinary-land discovery, WDA major change, Farmers tuning, and evidence-backed compatibility fixes. Do not redo research or reopen settled choices.

**Original input location:** ChatGPT Library `Minecraft/Ambient_Odyssey_Handoff_2026-10-09/`; `01_Baseline/Ambient-Odyssey-v0.3.1-sources-test5.zip`, import equivalent, `02_Reports/` (TODO, structure/biome audit, Test5 changelog/validation, registry/set/matrix CSV, JAR audit coverage), `03_Recent_JARs/` (17 newly supplied), latest Oct 9 Test5 runtime log if accessible.

**Original phases:**
- A: Extract/reproduce original Test 5, check Python, run `build_release_030.py` and original validation; preserve untouched baseline. Do not modify until build success.
- B: Audit remaining JARs and exact 8 additions. Prioritized Cristel Lib, CTOV, Dungeons & Taverns, Towns & Towers, Seven Seas, Cataclysm Spellbooks, YUNG's structures, Create: Rustic Structures, End/dimension structures. Check registries/sets/pools/biomes/feature code and configuration.
- C: Set WDA major Overworld frequency 27/38 -> 0.80 **without** changing End; Bathhouse stays 112/48 0.5. Inspect WDA ordinary 28/14 five-member set, not blindly raise it. Improve Farmers all variants with dimension safety; keep Cooks Moss at 11/10 initially and no FDstructure. Install eight addons only after compatibility/dependency verification; Explorify Black Spiral disabled. Repair CTOV/IDAS jigsaw and Cataclysm Spellbooks only with genuine assets/IDs.
- D: Run validators, regenerate 3 catalogues and biome matrix, test tags, disabled membership, ownership, salts, mods/dependencies, ZIP integrity, root manifest, deterministic source build; deliver ZIPs and reports.
- E: Fresh-world tests of WDA majors, Bathhouse, WDA ordinary, Farmers, eight addons, land/river/mountain/modded biomes, bridges, collisions/clipping, Heavenly dimension split, no Small Blimp/Coliseum/Black Spiral, jigsaw assemblies, chunkgen performance. Log seed/preset/coords/IDs/settings/timing/screenshots.

**Original stop conditions:** Cannot reproduce Test5; addon incompatible NeoForge 1.21.1; dependency conflict; End separation nontrivial; Farmers dimension unknown; template repairs lack real assets; Test5 regression; export cannot validate. Never substitute other mods or silently omit additions.

**Important supersessions:** audit1 subsequently completed many static repairs and Farmers tuning; current 41 missing binary list replaces the old 60/17 count; exact two mod file IDs updated; **new** Mushroom Village requirement; Test 7 biome queue. Use `01_TEST6_IMPLEMENTATION_BRIEF.md` as the controlling continuation.
