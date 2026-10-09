# Ambient Odyssey — Structure Test 6 implementation specification (reconciled)

This **updates** the 9 October initial handoff. The current starting source is **Test 5 audit1**, not the earlier incomplete baseline. The original user handoff is preserved in `06_ORIGINAL_TEST6_HANDOFF.md`. All implementation requires evidence-backed source changes and a reproducible export.

> **Status after implementation:** This file preserves the original *specification*, but the WDA patch and all eight addon installs (plus AAA Particles) are now committed on `structure/test6`. Do not repeat steps as unimplemented. Start from [current state](../status/CURRENT_STATE.md) and [runtime acceptance](../testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md). See `release_030/release-lock.json` for approved live pins; superseding user decisions below take precedence over older preparatory notes.

## Goals and guardrails

Structure Test 6 remains the *structures/biome eligibility* pass. Do NOT combine with biome and terrain Test 7. Keep FreeTerraForged the sole primary Overworld terrain generator, Biolith, existing Streams, Tan's Huge Trees, TRMT and the exact 40 Overworld + 2 Nether curated donor roster until Test 7. Keep the multiplayer exploration-first RPG identity. Preserve boss landmarks' rarity and appropriate Overworld/Nether/End separation.

## 0 — Baseline and source hygiene

- Keep original Test 5 unchanged, including original import and validation evidence. The newer audit1 had already statically reproduced pristine Test 5 (76 original gates; byte-identical rebuild). Independently check that audit1 sources rebuild to the bundled audit1 import before edits.
- Inspect `SOURCE_CHANGES.csv` for repairs already completed; do not overwrite these by starting from Test 4/Test 5. Branch from audit1 and name new outputs unambiguously `structure-test6`.
- No direct edits solely to generated Paxi/datapack outputs. Update authoritative JSON and Python source inputs, then compile.

## 1 — Eight approved structure mods, all mandatory unless blocked

YUNG's Extras; YUNG's Bridges; Structory: Towers; Archaion; Explorify; Additional Structures; Create: Structures Arise; Create: Easy Structures.

`APPROVED_STRUCTURE_ADDITIONS.csv` carries project/file IDs and file-page URLs; two selections were updated since the initial handoff: Structory: Towers **783522:8396885 (v1.0.17, expressly approved 9 Oct)** and Explorify **698309:8082824**. Older **5800614** and **5482463** are historical candidates, not the currently chosen entries. Acquire exact original mod binaries from legitimate distribution, verify SHA-256, dependencies, mod metadata, pack compatibility and registry/worldgen/feature code. All eight were ABSENT from audit1.

Inspect regular structures/sets, template pools, configured/placed features, dimension and biome selectors, code-generated routes, and config-driven replacements. Avoid double ownership, density blowouts, repeated salts, heavy rewards, duplicate Create loot or unintentional major boss proliferation. Test big buildings against FreeTerraForged terrain and Bridges against steep or winding rivers.

**Archaion:** AAA Particles is a reported missing dependency; identify the precise version/API requirement from Archaion's mod metadata and check for existing conflicts. Availability of an AAA Particles 1.21.1 NeoForge file alone does not prove compatibility.

**Explorify (later user-approved supersession, 9 Oct):** keep Nether **Black Spiral enabled provisionally**. Check natural spawning and interactions with the rest of the Nether stack in a fresh world; disable only for an evidenced conflict. The correct registry ID/disable strategy must be derived from inspected assets/code.

## 2 — WDA major structures

Target a *modest* Overworld major candidate increase for `dungeons_arise:major_structures`: frequency from native `27/38` (~0.710526) to **0.80**. Its shared native set includes original End-only Heavenly entries: prove that the change does NOT raise End candidate density. If a split is required, create proper dimension-scoped owner sets and disable old duplicate owners; no inadvertent additional candidate grids. If a safe separation is complex, STOP, report and preserve End rarity rather than applying a blind global edit.

**Bathhouse:** unchanged at **112/48, frequency 0.5** in its rare, single AO placement route. Its difficulty/loot rebalance is later. Preserve complete removal from natural generation of WDA **Small Blimp** and **Coliseum**.

## 3 — NEW since the initial handoff: WDA Mushroom Village

The user confirmed actual `dungeons_arise:mushroom_village` should be **Mushroom Fields-only**, **rare**, and under a **dedicated placement owner**. Remove it from any general/shared placements that let it appear in non-Mushroom-Fields biomes. Audit its native set/member registration and original exclusion mechanics before changing. Prevent duplicate grids or jigsaw references and verify natural generation exclusively in `minecraft:mushroom_fields` in a fresh world. Do NOT invent an arbitrary high spawn frequency.

Later separate balancing phase: greatly increase the Mushroom Village Piglin/Piglin Brute encounter difficulty and rebalance reward loot. **Do not accidentally implement that combat/loot overhaul inside the Test 6 worldgen patch.**

## 4 — WDA ordinary buildings

Investigate `ambient_odyssey:wda_ordinary_land` (currently 28/14; total weighted selection 11). Members: Illager Campsite, Illager Windmill, Merchant Campsite, Mushroom House, Greenwood Pub. Check source and native config enablement, biome tags, placement retries, six-chunk exclusion, density and FTF terrain validity before raising rates. No blind numerical increase.

## 5 — Farmers Structures

**A later audit1 already implemented a native-dimension-preserving ~2x candidate density across ALL 20 variants**, via bounded spacing/separation, unique salts, native member/weight/height/biome preservation, and repair of Undergarden salt. Six previously tuned grids were not doubled again; see `FARMERS_STRUCTURE_CATALOG.csv`, `evidence/farmers-density-evidence.json`, and audit1 changelog. This **supersedes** the old wording 'apply 20-variant tuning'. Do not repeat the multiplier.

Remaining: inspect obsolete tags and actual eligible biomes, verify real natural generation in the relevant intended dimensions, check collisions, clustered farms, coasts, underground, Nether, Aether, Undergarden, Bumblezone. Cooks Moss initially remains around its native 11/10 candidate grid as reported in early handoff; read the *actual audit1 native/current values* before applying any new numeric change. Do NOT add FDstructure.

## 6 — Preserve already implemented repairs

Preserve audit1 static fixes: Cristel native WDA/IDAS extraction toggles; proper CTOV tower alias and asset-backed Waystones connector/NBT migration; valid Dungeons & Taverns illager basement JSON; four earlier AO pool repairs; Create: Rustic and CTOV 32-route curated biome eligibility; Traveloptics tag / Cataclysm Spellbooks remnant registry repairs; 33 client model fixes; conditional skipping of 11 absent-item Cataclysm Spellbooks recipes; real native loot modifier alias; Simply More recipe, Enigmatic/Curios repairs; exclusions and biome/sky rules from Test 5. Do not create fake missing items or placeholder empty template pools.

Still investigate with evidence: IDAS Dread Citadel and Ancient Mines missing real references, blank `minecraft:` jigsaw targets, other leftover CTOV/template problems, 70 recorded native resource collisions, live Cristel-vs-Paxi pack priority and AO-only exclusion fields.

## 7 — Biome-structure eligibility and sky rules

Regenerate AO compatibility tags from real selected mod registries, native OR/AND/NOT selectors and curated donors. Prevent the previous vanilla-biome structure monopoly: Prairie, Grassland, Flower Fields, Sakura, Pumpkin Patch, mountains, snowy, woods, wetlands, coasts and streams need reasonable appropriate candidates. Do not globally whitelist alien biomes to unrelated structures.

Sky Villages: preserve land, river, frozen river, RU muddy river and Streams river eligibility at existing 44/32; ocean excluded. The prior 'only above oceans' observation is unproven as an actual ocean biome: record the exact biome at coordinates. Keep Heavenly Overworld clones distinct from End. Test WDA sky and Sky Whale land/climate eligibility.

## 8 — Verification, outputs and stop conditions

Run current source build, continuation static validator and updated Test 6 regression tests; regenerate native inventory, placement catalogue, biome matrix and collision/ownership checks. Assert current mods and exclusions, no duplicated members/owners, Bathhouse invariance, Mushroom Village exclusivity, End rarity, Farmers sets' members/biomes/salts, all archive CRC/safe paths, **exact uploaded CurseForge ZIP root manifest**, and two clean deterministic rebuilds. Preserve original baseline. Deliver *source ZIP, CurseForge import ZIP, changelog, validation report, SHA-256 list*.

Fresh-world acceptance: exact biome IDs at each found structure, generation seed/preset, mod versions, coordinates, natural-vs-locate distinction, terrain clipping, entrances, bridges, density across donor vs vanilla biomes, major WDA counts, Dungeon Crawl, ordinary land buildings, Farmers discoveries, End/Nether separation, pack loading and new-chunk generation costs. A /locate hit is not proof of natural terrain quality. No success label for unchecked runtime behavior.

**Stop and report:** audit1 clean reproduction failure; incompatible approved mod/dependency; inability to disable Black Spiral safely; End-frequency split cannot preserve rarity; Farmers variant dimension uncertain; asset-less template repairs; failed export validation; major Test 5 regression. No substitute mods, no silent skips. Report Implemented / Verified statically / Verified at runtime / Not tested / Blocked separately.
