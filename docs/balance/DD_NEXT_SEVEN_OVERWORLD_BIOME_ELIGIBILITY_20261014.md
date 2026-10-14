# PR56 — Seven other historical zero-curated-biome Overworld structures (14 Oct 2026)

**Stage:** native-source triage, not a final worldgen decision. The original Test5 registry is historical: `curated_ow_test5_count=0` means zero *documented curated-mod-biome* intersection, **not** proof a structure cannot generate in surviving vanilla biomes, another dimension, an integrated API, or a dynamically populated external biome tag. Do not auto-repair.

## Exact seven source IDs

| Registered structure | Historical selector | Assessment | Next evidence gate |
|---|---|---|---|
| `adventuredungeons:underground_camp` | `#minecraft:has_structure/pillager_outpost` | Vanilla pillager-outpost tag may be populated by other packs; cannot infer failure from curated Test5 zero | Resolve effective current `minecraft:has_structure/pillager_outpost` contents and matching placement set, without broad edits to pillager outposts |
| `bettermineshafts:mineshaft_oak` | `#bettermineshafts:has_structure/better_mineshaft_oak` | Native PR50 pinned JAR lists vanilla meadow/plains/sunflower_plains/swamp, old projectvibrantjourneys/Terralith, and an external `#c:plains`. No **direct** curated-roster IDs. `#c:plains` not resolved by the native JAR; AO Paxi source has `c:is_plains`, which is **NOT the same tag** | First check whether other installed mods populate `c:plains` and whether vanilla plains survive Biolith in the real profile; avoid global `c:plains` rewrite |
| `bettermineshafts:mineshaft_spruce_snowy` | `#bettermineshafts:has_structure/better_mineshaft_spruce_snowy` | Native pinned JAR uses vanilla jagged_peaks/snowy_plains/snowy_slopes/snowy_taiga plus inactive-or-unverified Terralith IDs. None are in the 42-modded curated snapshot, but these vanilla snowy biomes are **not direct Biolith replacement targets in the recorded file** | Verify vanilla snow biomes remain in current terrain. No patch from name-based zero alone |
| `minecraft:village_plains` | `#minecraft:has_structure/village_plains` | Luki's Grand Capitals source refers to the vanilla village set. AO Biolith actively replaces plains toward curated grassland/prairie; some vanilla fallback may remain. No proven defect | Confirm actual vanilla-village placement/fallback balance; do not re-enable vanilla plains or alter village frequency as a side effect |
| `minecraft:village_snowy` | `#minecraft:has_structure/village_snowy` | Snowy vanilla biomes may remain. No actual generation evidence here | Inspect active tags and small fresh-world samples if needed |
| `pasterdream:fourleaf_clover_plant` | `plains` (native historical selector) | Pasterdream world/dimension/biome behavior not established by old Overworld-style source label; may be mod-native conditions | Check Pasterdream native source and intended dimension before changing selectors |
| `pasterdream:picnic_basket_structure` | `plains` and four Pasterdream-namespaced biome selectors | Pasterdream-specific biome IDs appear by native source. Old curated Overworld count cannot decide generation | Verify intended Pasterdream dimensions and active tagged biome roster; do not add it blindly to AO Prairie |

## Source evidence completed

The exact installed PR50-pinned YUNG Better Mineshafts NeoForge JAR was downloaded into an isolated GitHub Actions runner, SHA-1 verified as `6a14e1d8201f068ca87ef8333e471c5378955906` (CurseForge project `1015096`, file `5812193`; mod version `5.1.1`). It has **13 native biome tag JSONs, 16 native structure definitions and one native structure set**. Two exact source definitions and their tag contents are persisted at [`DD_YUNGS_MINE_SHAFT_NATIVE_BIOME_SOURCE_20261014.json`](DD_YUNGS_MINE_SHAFT_NATIVE_BIOME_SOURCE_20261014.json). [CI run 38604294893](https://github.com/alsynth/AmbientOdyssey/actions/runs/38604294893) passed all four jobs (catalogue, pinned D&T source, PR50 Paxi source parity/test datapack and YUNG native probe).

## Conclusion and next owner gate

**0 new gameplay/worldgen changes authorized from these seven static cases.** The other five are unproven and need effective tags or native source work before any patch. The YUNG results show why names and zero-curated snapshots are insufficient: `oak` is a plains/swamp-tagged mineshaft and `spruce_snowy` permits vanilla snowy locations.

**Owner needed now: nothing.** Later, on an exact-version disposable Minecraft world, a few representative generated YUNG mineshaft variants and intact vanilla snowy biomes can be sampled while already doing the firewatch test. Avoid expanded testing if the real build already demonstrates generation in those zones. No live DD, worldgen, mobs, loot, boss balance, rollback or large Chunky pregen is changed.
