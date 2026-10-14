# PR56: curated-biome / Dungeons & Taverns firewatch audit (14 Oct 2026)

**Status: source-level risk screen + INERT experimental datapack ONLY.** No active `release_030`/Paxi/structure_set/DD/worldgen payload was changed. The older Test5 source/catalogue and AO curated-roster documents may not equal the effective PR50 338-mod profile; validate deployment precedence and dynamic biome availability before any live change.

## Verified source boundaries
- Pinned prior source mod: `dungeons-and-taverns-v4.4.4 [NeoForge].jar`. Historical `STRUCTURE_REGISTRY_CATALOG.csv` records all 9 D&T `nova_structures:firewatch_tower_*` definitions and the shared `nova_structures:firewatch_towers` structure set. Historical `STRUCTURE_SET_CATALOG.csv`: **spacing 50, separation 15**, nine equally weighted variants; exclusion 10 chunks around the village set. **Do not change** this.
- AO curated snapshot `docs/audits/CURRENT_BIOME_ROSTER.json`: 42 enumerated modded biome IDs across listed providers (NOT all necessarily Overworld or proof of all possible biomes). `docs/audits/CURRENT_BIOLITH_PLACEMENT.json` explicitly replaces most **forest, birch, savanna, jungle** candidates; it **does not list `minecraft:swamp` or `minecraft:mangrove_swamp` as replacement targets**. Therefore historic Test5 zero-curated-biome hits for swamp and mangrove are **not evidence they are missing**.
- AO `release_030/overrides/config/paxi/datapacks/ao_compatibility/data/minecraft/tags/worldgen/biome/` already adds modded biomes to common `minecraft:is_* ` tags, but **the Nova structure collection namespace is separate**. In particular, adding to `minecraft:is_birch_forest` alone does NOT prove that `#nova_structures:collections/birch_forests` contains those biomes.
- `release_030/overrides/config/paxi/datapacks/ao_dnt_trek_curation/data/nova_structures/worldgen/structure/remnant_birch_graveyard.json` explicitly replaces the graveyard's selector with `#ambient_odyssey:dnt_trek_disabled`. Its historical zero-biome result is **intended curation** and must **not** be repaired. The same curation pack disables additional D&T sites; review those exclusions before broad tag edits.
- `#nova_structures:collections/...` values in this audit are read from the historical *structure selector*. Installed/current JAR source collection-tag contents and active worldgen precedence are **not yet fully enumerated**. The stage below is a proposed additive bridge, not demonstrated runtime necessity.

## Nine D&T firewatch variants — correct distinctions

| Native structure ID suffix | Historical selector | Test5 curated hits | Biolith replacement pressure | Action |
|---|---|---:|---|---|
| birch | `#nova_structures:collections/birch_forests` | 0 | birch forest replaced | Stage additive curated tag candidates |
| cherry | `#nova_structures:collections/cherry_forests` | 0 | cherry not in listed Biolith direct-replacement targets; custom Sakura available | Stage additive curated tag candidates; verify natural cherry availability |
| dark_oak | `#nova_structures:collections/spooky_forests` | 3 | forest replacement | Already has historical curated hits; no immediate fix |
| forest | **literal `minecraft:forest`** | 0 | **forest replaced** | Risk of fallback-only generation; changing collection tags CANNOT fix. Needs original pinned JAR structure JSON and narrowly scoped complete override before implementation |
| jungle | `#nova_structures:collections/jungles` | 3 | jungle replacement | Already has historical curated hits; no immediate fix |
| mangrove | **literal `minecraft:mangrove_swamp`** | 0 | **not** listed as replaced | Retain; zero hits only means not in the modded curated snapshot; verify vanilla natural presence |
| savanna | `#nova_structures:collections/savannas` | 0 | savanna replaced | Stage additive curated tag candidates |
| swamp | **literal `minecraft:swamp`** | 0 | **not** listed as replaced | Retain; verify vanilla natural presence |
| taiga | `#nova_structures:collections/any_taiga` | 1 | no explicit taiga replacement target in inspected Biolith file | Already has a historic curated hit; verify prevalence later |

## Experimental opt-in tag bridge — **DO NOT DEPLOY**
`experiments/structure-biome-compatibility/firewatch-tag-bridge-draft/` is a standalone Minecraft **1.21.1 datapack (format 48)**, not inserted into any active Paxi path or release ZIP. The three `replace:false` tag files would **append**:
- `birch_forests`: `biomeswevegone:sakura_grove`, `biomeswevegone:zelkova_forest`, `regions_unexplored:maple_forest`.
- `cherry_forests`: `biomeswevegone:sakura_grove`, `biomesoplenty:snowblossom_grove`.
- `savannas`: `biomeswevegone:prairie`, `regions_unexplored:grassland`, `natures_spirit:floral_ridges`.

All proposed IDs are present in the documented curated roster. **Caveat:** Nova's `collections` biome tags can be used by other D&T structures, not only towers. Enabling them can increase placement eligibility even without changing structure-set spacing, so this proposed patch must first be screened for *all consumers* and village/landmark impacts. `prairie` in particular is common in AO; assess its effect before activation. This patch deliberately does **not** touch `minecraft:forest`, `minecraft:swamp`, `minecraft:mangrove_swamp` selectors, worldgen weights, creature spawners or any disabled curation.

## Stale AO common-tag entries — **not equivalent to structure breakage**
The legacy Paxi `ao_compatibility` tag files reference IDs omitted from `CURRENT_BIOME_ROSTER.json`:
- `biomeswevegone:dacite_shore` in `minecraft:is_beach` and `minecraft:is_overworld`.
- `biomeswevegone:tropical_rainforest` in `minecraft:is_jungle` and `minecraft:is_overworld`.
- `biomeswevegone:baobab_savanna` and `biomesoplenty:dryland` in `minecraft:is_plains` / `minecraft:is_overworld`.

This is *roster drift*, not proof these names are unregistered or that any concrete structure breaks. Many tags still include valid curated alternatives and are `replace:false`. Avoid blanket deletion until the exact active Paxi pack and all resource references are reconciled.

## Next assistant-owned verification
1. Obtain/extract **exact installed v4.4.4 NeoForge JAR's** collection tags and nine structure definitions (or use PR50's pinned SHA-validated input if accessible). Enumerate **all consumers** of the three proposed collection tags and the current effective Paxi overrides.
2. Check biome overlap with final worldgen roster plus any actual vanilla fallbacks; direct vanilla-specific towers need a *full source-faithful structure JSON override*, not generic tags.
3. Run fast test in a disposable exact-profile world: `/place structure` verifies registration/placeability ONLY; bounded natural generation checks actual eligibility; screenshots/seed/coordinates/active datapacks if client runtime needed. Avoid expensive global `/locate`.
4. Only after verifying no other structure's placement is unintentionally widened, move reviewed bridge into a candidate build on a dedicated worldgen branch, run the static and runtime checks, and request owner acceptance before large Chunky pregen.

**Owner needed now: NONE.** Core PR56 owner decisions (26 Tier0 spawner-positive, Dungeon Crawl Tier3 all floors) and no-DD-deployment gates remain untouched.
