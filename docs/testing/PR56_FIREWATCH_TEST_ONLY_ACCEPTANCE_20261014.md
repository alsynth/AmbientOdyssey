# PR56 — D&T firewatch four-tower isolated acceptance plan
**14 October 2026 — not approved for any active release or production world**

## What actually exists
- **TEST ONLY** datapack ZIP, built by GitHub Actions as artifact `pr56-four-tower-worldgen-TEST-ONLY`, with an included `pr56-firewatch-four-towers-TEST-ONLY.zip` and JSON SHA-256 manifest. Artifact reference: https://github.com/alsynth/AmbientOdyssey/actions/runs/38603628576 . Actions artifacts expire after 14 days; re-run the source-pinned workflow if needed.
- Deterministic exact ZIP SHA-256: `a797057bfe057a88212a56a3462ee8df6b1e9108e72a6e78ece485bd411b2db6`. Rebuilt **twice**, byte-for-byte identical in GitHub CI, **nine total datapack members** (pack.mcmeta, four native structure JSON overrides, four private tags). The ZIP contains **no mod JARs, executable code, rollback file, or Minecraft world**.
- Pinned native JAR: Dungeons & Taverns NeoForge 1.21.1 v4.4.4, CurseForge project `853794`, file `5768823`, verified SHA-1 `249a5bdd0e8622b8a11f88758e6f5fd5fda036a3`.
- Four targeted structures: `nova_structures:firewatch_tower_birch`, `_cherry`, `_forest`, `_savanna`. Each exact JAR definition retained all properties **except `biomes`**, now pointing to `#ambient_odyssey:firewatch_compatible/<suffix>`.
- Source-only Paxi comparison across 14 datatpacks on PR50 and PR56: **no preexisting target-resource conflicts**, both intentional D&T disabled entries preserved. Full machine-readable evidence: `docs/balance/DD_PR56_PR50_PAXI_SOURCE_PARITY_20261014.json`.
- **NOT** a complete CurseForge client import or confirmation of a live Paxi resource winner. Active profile and server compatibility remain untested.

## Safety before testing
- Use **two disposable NEW game profiles/worlds**, with *the exact same modpack, NeoForge, Paxi, worldgen/biome-replacement files, world seed and server configs*. Leave existing saves, real multiplayer worlds and rollback/profile files untouched.
- **Baseline/control**: do not install the candidate ZIP. **Candidate/test**: enable the ZIP only in the isolated test profile **before creating its new world**, e.g. via the new world's datapack selection UI; or place in that *test profile's* Paxi `config/paxi/datapacks/` folder before launching if that is the method used for the pack. Do not put it in the real/default AO profile. Confirm `/datapack list enabled` shows the candidate pack and no duplicate resource pack has won the same tower definitions.
- The ZIP is a **datapack**, not a CurseForge modpack ZIP; don't attempt to import it as a CurseForge profile or put it in `mods/`.
- On initial start, check the log for missing biome tag entries, registry or JSON validation failures. Any failure: **stop test, do not copy over working profile configs**, attach a log excerpt.

## Focused test matrix
| Check | Baseline (no ZIP) | Isolated candidate (ZIP) | Evidence needed |
|---|---|---|---|
| World load on same seed + pack | Start and save | Start and save | Loaded datapack list, pack version, no JSON/registry errors |
| Birch tower | Recorded vanilla eligibility | Added Sakura Grove/Zelkova/Maple | Biome + structure ID; check jigsaw piece completion |
| Cherry tower | Recorded original cherry eligibility | Added Sakura Grove/Snowblossom | Biome + structure ID; structure layout |
| Forest tower | Original direct `minecraft:forest` | Added Ebony/Redwood/Zelkova/Maple/RU Redwoods | Biome + structure ID; structure layout |
| Savanna tower | Recorded original savanna eligibility | Added Prairie/Grassland/Floral Ridges | Biome + structure ID; especially Prairie oversaturation |
| Other D&T structures | Unchanged | Should not receive expanded D&T `collections/*` tags | Spot-check taverns, wells, shrines and previously disabled jungle village/birch graveyard |
| Native tower set | 9-member original set | Same 9 entries, weights, spacing 50/separation 15 | No changed config, exclusion or collision behavior |
| Baseline without ZIP afterward | Loads | Remove ZIP only in disposable profile | No residual pack dependency/crash |

Using `/place structure <ID>` in an appropriate target biome can check whether the ID exists and the jigsaw assembles, but **it does NOT prove natural worldgen eligibility**. Natural placement requires a fresh-world bounded sample with an identical baseline and candidate seed/config; record what actually generated, not only manually placed structures. Avoid unbounded `/locate` on live servers; the earlier PR50 broad Nether scan caused a 40-second tick.

**A 1,000-block pregenerated radius is a useful smoke test, NOT a statistically sufficient sample to prove the absence or frequency of each variant.** The entire nine-variant firewatch set is sparse (native random-spread spacing 50 chunks); failure to encounter a specific variant within one small seed is inconclusive. For actual density acceptance use a handful of bounded test seeds/regions and compare towers, collisions and biome types. Do NOT scale up to planned 10k–20k Chunky pregen until worldgen is frozen.

## Compact observations to return — later, not now
- Exact test version/commit or ZIP manifest SHA, seeded world, dimension, and datapack enabled list.
- Each tested tower suffix, ambient biome, naturally generated vs `/place`, whether complete, and any misplacement/collision.
- Control-vs-candidate natural placements in comparable tested regions (including other D&T structures), and client/server TPS abnormalities.
- Any console/launcher errors including resource precedence or unknown biome IDs.

## Release gate
**Assistant owned:** pinned-JAR source validation, PR50 branch source parity, exact-field diff, deterministic ZIP, static regression checks. **DONE — all current CI gates green.**

**Still needs owner-side runtime acceptance when convenient:** actual full-client/full-server profile datapack order; four-tower generation and shared-set density; multiplayer/world persistence; no weird builds, tile entities, mobs or biome visuals. Never mark these runtime-certified from CI alone.

No live modpack settings, worldgen, loot, boss, Dungeon Difficulty, registry or server files were edited for this test-only experiment. PR #56 remains draft and unmerged.
