# Ambient Odyssey — Test8.10 comprehensive documented worldgen defects audit

**Date:** 10 October 2026. **Minecraft / NeoForge:** 1.21.1 / 21.1.252. **Branch:** `worldgen/test8.10-all-documented-pools`. **Release lock:** `0.3.8-worldgen-prefreeze-test1.10`. **Purpose:** address all *source-identifiable* open worldgen issues from Test8.3–8.6 logs, plus subsequent native source audits, with independent checks and honest remaining limitations. **No further user-led Minecraft test required for this implementation task.**

## Actual fixes and changes beyond already source-verified Test8.8

| Issue | Owner and exact native evidence | Change | Outcome certainty |
|---|---|---|---|
| Beach lighthouse `kaisyn:village/beach_lighthouse/villager_lighthouse_master` missing | Towns and Towers 1.13.11 pinned SHA `270fc0d1...`. Native meeting-point NBT points to absent pool; original 1×3×1 lighthouse-master NBT with matching `minecraft:bottom` exists and has **zero embedded entities** | Add exact master start pool using original 1×3×1 template; stop its internal child pool safely | Strongly predicts missing-pool warning gone; *does not guarantee actual NPC spawns*. |
| Meadow Swiss village `kaisyn:village/meadow_swiss/villagers` missing | Same native T&T JAR missing pool; other native village pools use nitwit/baby/unemployed weight ratio **1:1:10** | Restore pool using existing vanilla plains nitwit/baby/unemployed villager NBTs in T&T's 1:1:10 pattern, `minecraft:legacy_single_pool_element`, empty processor | Valid compatibility **reconstruction** rather than original recovered asset; likely removes missing-pool warnings, exact NPC layout not runtime-certified. |
| Graveyard `graveyard:large_walled_graveyard/small_crypt_pool` missing | Exact Graveyard 2.6.2 SHA `69dd4501...` stores `crypt_pool.json` with internal `name` declaring missing `small_crypt_pool`. Has original single crypt NBT, original processor and weight. | Put the **unmodified native pool** under its declared registry path, preserve all native templates and processors. | Strong source-backed missing ID repair. |
| Repurposed Structures City Overworld intermittently fails required `fat_tower_top` | RS 7.5.22 pinned SHA `64e64109...` already includes correct top NBT and pool; structure `size=5` while city can branch through multiple tower segments. Original failure only once in Test8.3 at `(-4360,93,3176)`. | Override **only** city `size 5→7`; no frequency, biome or geometry changes. | **Mitigation only**, not guaranteed: terrain collision, piece overlap, layout and engine limits can still reject required top. |
| Traveloptics missing required legacy `#forge:tools` | Original pinned Traveloptics tag `traveloptics:can_cast_reversal` references `#forge:tools`; no such registered tag in exact installed-resource index. | Add non-replacing `forge:tools` bridge to optional `#c:tools` + optional vanilla tool family tags, maintained as **canonical** `release_030/structure-compatibility.json:item_tags` so `compile_compatibility_031.py` reliably emits the file after its normal datapack reset. | Direct source-backed missing-tag bridge; not a fix for Traveloptics' other malformed tags or missing item models. |
| Previously 214 Lithostitched blank `minecraft:` + Farmer's angler pool warnings | Test8.8 verified 273 malformed native jigsaw terminals across four mods, source SHA-pinned and roundtrip verified; plus Farmer's nine-piece cook/angler alias | **Retained entirely, no modifications** to geometry. | High static confidence, runtime zero-warning not yet measured. |

## Important generator/build lesson (caught automatically)
The compatibility compiler **deletes the entire `ao_compatibility/data` directory on each build**. Merely committing `data/forge/tags/item/tools.json` fails because compiler erases it. Early Test8.9 CI run [#38026865186](https://github.com/alsynth/AmbientOdyssey/actions/runs/38026865186) correctly **failed** its post-build `forge:tools` check. The canonical fix was to register the item tag in `release_030/structure-compatibility.json`, the actual generator source. Test8.10 reruns both the pre- and post-compiler tag gates and inspects the final private ZIP. **Only the latest successful Test8.10 CI should count as evidence.**

## Explicitly unresolved or requiring a code patch / live evidence

### Dungeon Crawl mob spawner block entities
Actual Test8.3 log says `[Dungeon Crawl] Failed to fetch a mob spawner` three times, near `(-896,36,95)`. [Official author's NeoForge 1.21 source `Spawner.java`](https://github.com/xyroc/DungeonCrawl/blob/neoforge/1.21/src/main/java/xiroc/dungeoncrawl/dungeon/block/Spawner.java) confirms the mod calls `setBlock(SPAWNER)` then immediately `getBlockEntity`; in WorldGenRegion a spawner's block entity may not be created yet. This is a **race/order-of-initialization issue in Java code**, not a datapack error. Switching `custom_spawners=false` does not fix the early block-entity read. A safe code-level fix requires patched Java and server/game runtime testing. We have **not** changed Dungeon Crawl, disabled it, or pretended it was fixed.

### POI mismatches / WorldGenRegion block entities
Nine POI mismatch errors in Test8.6, generic vanilla/NeoForge `WorldGenRegion` early block entity warnings. Without world seed, block state, reproducing stack and ownership, any patch (deleting POI region data, remapping POIs, removing structure mods) would be irresponsible. **Unresolved**; potentially transient given clean saved and exited worlds.

### Invalid ItemStacks, mod source tags and loot
Test8.6 `minecraft:air`, `redeco:hammer`, `traveloptics:blood_echo`; previous `meadow:alpine_salt`, `create:crushed_iron_ore`. Native installed-JAR JSON resource index has **zero** of the named custom item IDs in 408 JSON loot tables, suggesting embedded NBT/chest data or dynamic runtime generation. Do not silently replace rare drops or forge nonexistent items. A separate exact-JAR native NBT item provenance audit was started in [CI](https://github.com/alsynth/AmbientOdyssey/actions/runs/38026555895). Traveloptics source `element_fire` malformed JSON may require upstream asset repair; unrelated to structure pool definitions. The `forge:tools` tag is specifically source-fixed, not all Traveloptics defects.

### Physical worldgen and dimension acceptance
Rare large YUNG bridges on Streams Reflowing banks, Archaion/farmer/RS physical room clipping, dragons below Y−180, deep oceans, Nether and End, dimension transitions and dedicated server/chunk pregeneration all ultimately require representative real-world generation. Static JSON/structure-NBT checking cannot simulate the engine's biome selection, structure collisions, rotations, bounding box placement, loot population and mob AI. Retain a later acceptance checklist instead of inventing a success rate.

## Strict independent verification before user ZIP

Candidate on branch `worldgen/test8.10-all-documented-pools`; [CI](https://github.com/alsynth/AmbientOdyssey/actions/runs/38027173155) must show **all required steps PASS**:
1. 28 original Test8.4 biome/mountain/dragon checks.
2. 31 Test8.6 Archaion, Farmers and Create jigsaw assertions.
3. Test8.9 source SHA-pinned Towns Towers beach lighthouse original template mapping and RS city **exact size-only change**; Traveloptics tool bridge survives canonical compiler.
4. Test8.10 SHA-pinned Graveyard native one-piece crypt pool exact equality plus 1:1:10 Swiss pool native style.
5. 273 exact native pinned JAR replacement structure NBT roundtrip checks; 1 Farmers angler alias.
6. ZIP CRC, full 267 CF mods, original private NeoReef SHA, final `forge:tools` and both extra native aliases.
7. Build twice, **exact binary byte-for-byte match**, hash the importer ZIP (not GitHub's outer artifact wrapper).

## Final CI and exact importer outcome

**PASSED:** [Test8.10 complete GitHub Actions pipeline](https://github.com/alsynth/AmbientOdyssey/actions/runs/38027173155), including source-gate before and after compile, original 273 invalid terminal connector NBT repairs, native T&T/RS/Graveyard/Swiss pool assertions, final generated `forge:tools` item tag, all three private mods, archive integrity, and byte-identical second build.

- Importer: `Ambient-Odyssey-v0.3.8-Test8.10-Pool-Repair-PRIVATE.zip`.
- Exact 1.21.1 / NeoForge private pack: **70,810,381 bytes**, **1,386 ZIP members**, **267 CF references**, SHA256 **`0bfec2560337369fed08fc70329e00f337ee6281a8676a0e4e2ccb9f6751d71f`**.
- The outer GitHub Actions artifact is a ZIP *containing the importer ZIP*; import only the inner file into CurseForge. The final importer was independently extracted and ZIP CRC checked in the working container.
- Build byte identity was verified twice on the same pinned source JARs. **This is a static-source and archive validation, not a Minecraft runtime check.** Previous Test8.9 packs don't contain both Graveyard and Swiss aliases plus canonical Traveloptics bridge; use this Test8.10 candidate in preference to Test8.9 if trying the updated changes.

The user explicitly requested no more tests now. This is a **source-verified release candidate** pending any future normal gameplay evidence, **not proof of complete worldgen freeze**. Keep Test8.6 actual-run rollback and Test8.8 private source-verified rollback. No changes to performance optimization, mod roster, early-game bonus chest or Questlog GUI.
