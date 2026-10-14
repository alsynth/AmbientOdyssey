# Draft: four D&T firewatch structure-only curated-biome overrides

**NOT DEPLOYED.** This Minecraft 1.21.1 datapack is staged at `experiments/structure-biome-compatibility/firewatch-structure-only-draft/`. It is **not** in `release_030/overrides/config/paxi/`, the PR50 full-import profile, any playable CurseForge ZIP, or the multiplayer server. Do not ship until approved runtime checks are complete.

## Why this replaces the first shared-tag draft

The first `firewatch-tag-bridge-draft/` is **SUPERSEDED** and must **not** be installed. Its `nova_structures:collections/birch_forests`, `cherry_forests` and `savannas` tags affect other Dungeons & Taverns structures **directly**, and all three feed the shared `nova_structures:collections/land` tag. Verified from the exact CurseForge **v4.4.4 NeoForge JAR** (project `853794`, file `5768823`, PR50 SHA-1 `249a5bdd0e8622b8a11f88758e6f5fd5fda036a3`):

| Source tag | Direct structure consumers | Transitive native structure consumers |
|---|---:|---:|
| `birch_forests` | 5 | **22** |
| `cherry_forests` | 2 | **19** |
| `savannas` | 3 | **20** |

The shared `collections/land` tag alone directly controls 17 structures including D&T combat shrines and remnant sites. **Changing D&T's shared tags would therefore broaden additional encounter placement**; the original bridge must stay inert. Exact evidence: `docs/balance/DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json` (from PR56 successful native source audit).

## Scope of the replacement candidate

Exactly four native structure JSON definitions are copied **field-for-field from the hash-verified v4.4.4 JAR**, except for their `biomes` selector. Each now references a **separate AO-owned biome tag** that preserves its original biome/collection tag eligibility and adds appropriate biomes from the curated roster:

| D&T firewatch tower | AO-owned biome tag | Extra eligible curated biomes |
|---|---|---|
| Birch | `#ambient_odyssey:firewatch_compatible/birch` | Sakura Grove, Zelkova Forest, RU Maple Forest |
| Cherry | `#ambient_odyssey:firewatch_compatible/cherry` | Sakura Grove, BOP Snowblossom Grove |
| Forest | `#ambient_odyssey:firewatch_compatible/forest` | Ebony Woods, Redwood Thicket, Zelkova Forest, RU Maple Forest, RU Redwoods |
| Savanna | `#ambient_odyssey:firewatch_compatible/savanna` | BWG Prairie, RU Grassland, Natures Spirit Floral Ridges |

Each custom tag includes the original `#nova_structures:collections/...` as a reference (or `minecraft:forest` for the Forest tower), so the draft is *additive*. No other D&T structure references the new `ambient_odyssey:firewatch_compatible/*` names in the verified native JAR. The native nine-member tower structure set, spacing, separation, weights, exclusion and frequency are unchanged. Placement success/rarity **may** change because more biomes can qualify; this requires owner smoke and natural-worldgen testing before enabling. In particular, BWG Prairie is common in AO and should be sampled.

**Not included:** D&T's dark-oak, jungle and taiga towers (historical positive curated-biome intersections); swamp and mangrove towers (vanilla source biomes not directly Biolith-replaced); intentionally disabled D&T structures; AO RPG tiers, DD attributes, mobs, loot, spawners, set weights and other worldgen definitions.

## Reproducible TEST ONLY ZIP

[Actions run #38603628576](https://github.com/alsynth/AmbientOdyssey/actions/runs/38603628576) produces the artifact `pr56-four-tower-worldgen-TEST-ONLY`, containing `pr56-firewatch-four-towers-TEST-ONLY.zip` and the matching SHA-256 manifest. It contains **9 datapack members** and was built twice with **identical SHA-256 `a797057bfe057a88212a56a3462ee8df6b1e9108e72a6e78ece485bd411b2db6`**. Source PR50/Paxi parity: [persistent report](../../../docs/balance/DD_PR56_PR50_PAXI_SOURCE_PARITY_20261014.json). [Disposable-world-only test sheet](../../../docs/testing/PR56_FIREWATCH_TEST_ONLY_ACCEPTANCE_20261014.md).

This ZIP is a standalone Minecraft datapack, NOT a CurseForge modpack import, and is not installed anywhere by the build. Do not install into the production profile. Runtime resource-winner, natural generation and density still need testing.

## Required verification before an ACTIVE integration

1. Pass the new PR56 GitHub static guards **and** the SHA-1-pinned native diff gate. Every field other than `biomes` must match the actual v4.4.4 JAR, and all added biome IDs must be present in the curated source roster. **No claims of full effective live registry or natural generation from static checks.**
2. Compare against the final **actual client/server PR50/profile** Paxi datapack overrides and biome replacement rules; this PR56 staging folder is based on a repository snapshot, not a complete active profile. Resolve any winning structure JSON resource conflict before activation.
3. Deploy only to a **disposable world** / isolated worldgen test branch. Check `/datapack list enabled`, `/place structure` for registration/placeability, and then a bounded fresh-world natural-generation test for all four + a vanilla fallback. Do not do broad `/locate` on the live server.
4. Once natural generation is confirmed and unwanted structure density/collisions excluded, seek owner acceptance before enabling this pack in the intended release and freezing Chunky pregen. If the game rejects biome tag or jigsaw syntax, revert the experimental pack without touching live worlds.

## How to audit
`python -m unittest discover -s tests -p 'test_pr56_*.py' -v` checks inert file layout and ledger invariants. The PR56 native source job downloads the exact official JAR, SHA-1-checks it against PR50, then runs `tools/audit_pr56_dnt_firewatch_source.py` to verify the source-faithful override.

**Owner needed now: nothing.** The only later owner involvement is a representative controlled client/server worldgen smoke test and acceptance of density/appearance.
