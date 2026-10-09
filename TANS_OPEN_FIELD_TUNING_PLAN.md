# Tan's Huge Trees — staged open-field tuning

Status: prepared only; **not applied in Structure Test 5**. The native `config.txt`, `config_world_gen.txt` and `custom_packs/#main.zip` remain byte-identical to Test 4. This plan addresses excessive Prairie/open-field vegetation separately from structure placement and FTF/Biolith climate or biome-area changes.

The supplied native configuration establishes that lower `rarity` means rarer, `/` means OR, `,` means AND, `!` negates a biome/tag predicate, and `[LOCK]` preserves edited settings. `group_size` controls additional trees of the same species; large groups can increase density and scan work. `min_distance` is between trees, not between groups; the native notes warn that high values can slow region pre-location.

## Proposed first pass

| Area | Rarity | Group size | Minimum distance |
|---|---|---|---|
| Prairie, Grassland, Flower Fields, Pumpkin Patch, Alpine Clearings, Floral Ridges | Multiply applicable tree-rule rarity by 0.25 | Cap tree groups at 1–2 | Keep native value initially |
| Other ordinary land | Retain initially | Retain initially | Retain |
| Dense exceptions | Retain native forest/taiga settings | Retain deliberately dense groups | Retain |

The known requested dense example is `minecraft:taiga`; the second forest remains a later selection. Do not globally reduce `multiply_rarity`/`multiply_group_size` and describe that as a biome-specific change. Retain global multipliers at 1.0 for the staged design.

Native rules such as Walker and Wayfarer currently use broad plains/forest/taiga/swamp expressions and groups of 10–20. Waterside bushes/shrubs can use 20–100. Reducing tree groups alone will not necessarily clear all open-field vegetation. Audit tree families first, then explicitly decide whether bush/shrub clutter is part of the separate pass; preserve the rock family unless changed deliberately.

## Authoring method

Use separate native custom-preset/rule variants for open fields and the remaining biomes, sharing the existing shape assets. Inspect the installed custom pack's rule identity and paths before assigning clone IDs; the following is a selector/value proposal, not a drop-in full native preset.

```text
biome = biomeswevegone:prairie / regions_unexplored:grassland / regions_unexplored:flower_fields / biomesoplenty:pumpkin_patch / natures_spirit:alpine_clearings / natures_spirit:floral_ridges
group_size = 1 <> 2
```

Set each open-field clone's numeric rarity to one quarter of the native source value (for example, Walker 0.1 → 0.025 and Wayfarer 0.01 → 0.0025). Keep `spawn_type`, shape settings, ground predicates and minimum distance. Mark each edited native entry `[LOCK]`.

Remove the same six biomes from **every OR branch** of the retained counterpart. For example, a two-branch selector must exclude them in both branches:

```text
biome = #c:is_plains, !biomeswevegone:prairie, !regions_unexplored:grassland, !regions_unexplored:flower_fields, !biomesoplenty:pumpkin_patch, !natures_spirit:alpine_clearings, !natures_spirit:floral_ridges / #minecraft:is_forest, !biomeswevegone:prairie, !regions_unexplored:grassland, !regions_unexplored:flower_fields, !biomesoplenty:pumpkin_patch, !natures_spirit:alpine_clearings, !natures_spirit:floral_ridges
```

This prevents both original and open-field variants from placing in the same target biome. Use the complete native selector, not just the two example branches above. Explicit exceptions also need disjoint counterpart membership if assigned separate rules.

The machine-readable staged proposal is `release_030/staged/tans-open-field-tuning.json`. It is outside runtime overrides, and no compiler installs it. Native rule-clone implementation belongs in a later tree-focused build with its own source diff and rollback copy.

Before that later build is delivered, validate custom-pack/config paths, numeric bounds, locked identities and selector disjointness statically. A later same-seed fresh-area comparison can assess tree/group counts, Prairie openness, the chosen dense exceptions and generation timing; it is not a prerequisite for Structure Test 5.
