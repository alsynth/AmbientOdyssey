# Ambient Odyssey curated climate replacement prototype

Status: implemented as a Biolith 3.0.14 datapack in the 0.3.1 test build; awaiting runtime testing. The old conceptual pools below are superseded by `biome-pools.json` and `TESTING-0.3.1.md` and must not be used as runtime configuration.

## Goals

- Preserve the complete curated biome roster and its native TerraBlender placements.
- Replace most vanilla Plains, Forest, Birch Forest, Savanna and Jungle fallback results.
- Retain approximately 5% vanilla results as a deliberate safety/variety layer.
- Keep climate compatibility: oceans remain oceans, wetlands remain wet, mountains remain mountainous, and cold biomes remain cold.

## Planned replacement categories

- plains_open: BWG Prairie, RU Grassland, RU Flower Fields, BOP Grassland, BWG Skyris Vale
- temperate_forest: BWG Ebony Woods, BWG Redwood Thicket, BWG Zelkova Forest, BWG Weeping Witch Forest, RU Maple Forest, BOP Highland
- birch_deciduous: BWG Zelkova Forest, BWG Ebony Woods, BWG Sakura Grove, RU Maple Forest, RU Cold Deciduous Forest
- warm_woodland: Nature's Spirit Floral Ridges, Nature's Spirit Windswept Sugi Forest, BOP Highland, BOP Hot Springs, BWG Skyris Vale
- tropical_lush: BWG Crag Gardens, BWG Lush Stacks, BWG Weeping Witch Forest, BOP Highland, BOP Hot Springs
- wet_transition: BWG Bayou, RU Marsh, RU Fen, BOP Hot Springs, Nature's Spirit Floral Ridges

## Required implementation work

1. Extract exact BWG/BOP climate parameter points from the 1.21.1 JARs.
2. Identify vanilla fallback points for each replacement category.
3. Choose the least invasive implementation: datapack/config if supported; otherwise an isolated compatibility patch.
4. Preserve the existing curated biome enable/disable decisions.
5. Test biome distribution, rivers, oceans, caves, structures and FTF terrain on fresh seeds.

## Separate terrain target

- Test FreeTerraForged continent scale 6500 instead of the default 4000.
