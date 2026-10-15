# CTOV Mesa vs Badlands Pillager Outpost — source-only triage (PR56)

**Research status 2026-10-14:** Additional exact repository source evidence indicates the historical `ctov:pillager_outpost_mesa` may be an *unreferenced legacy or alternate structure definition*, not a broken active outpost. **Do not silently enable, spawn-test as a required gameplay site, or write a Tier2 DD rule for Mesa** until current PR50 effective worldgen set/registry is checked. This document is not proof of runtime absence.

## Crosschecked repository evidence

| Artifact | Badlands ID | Mesa ID |
|---|---|---|
| Historical `STRUCTURE_REGISTRY_CATALOG.csv` | `ctov:pillager_outpost_badlands` | `ctov:pillager_outpost_mesa` |
| Historical native structure file | `data/ctov/worldgen/structure/pillager_outpost_badlands.json` | `data/ctov/worldgen/structure/pillager_outpost_mesa.json` |
| Historical biome selector | `#minecraft:is_badlands` | `#minecraft:is_badlands` |
| Historical linked set | `minecraft:pillager_outposts` | **empty / no linked set** |
| Release030 local `ctov-common.toml`, `[structures].enabledpillageroutpost` | **contains `"badlands"`** | **does not contain `"mesa"`** |
| Release030 AO Paxi `ao_compatibility/data/ctov/worldgen/structure/` overrides | no Badlands override visible | no Mesa override visible |

The installed local `release_030/overrides/config/ctov-common.toml` also has `generatePillagerOutpost = true`, and its complete enabled list is: `beach`, `dark_forest`, `desert`, `jungle`, **`badlands`**, `mountain`, `plains`, `savanna`, `snowy`, `swamp`, `taiga`. The CTOV Paxi worldgen overrides there target dark_forest, plains, snowy, swamp and taiga (not Mesa or Badlands). This is concrete repository evidence rather than inference from names.

## Interpretation and next gate

- The two **different native structure IDs** both had `#minecraft:is_badlands` in historical source definitions; only Badlands has a historical set reference and enabled-config name. Thus mapping Mesa to Tier2 from the vanilla-outpost analogue was only a numeric first-pass heuristic, **not a confirmed active encounter**.
- A structure JSON *existing in a JAR* does not mean an active `structure_set` chooses that ID or that it naturally generates. The historical absence of Mesa from the enabled config and source set is a good reason **not to make the user spend time on it as a top-priority worldgen problem**.
- This does **not** establish effective **PR50** server registry/resource precedence, CTOV's current code-driven injection, or whether the current build changed the CTOV config. Those remain source/runtime follow-ups.
- Next **assistant-owned** action: compare the intended 338-mod build's exact CTOV common config, Paxi structure_set overrides and CTOV native registrations; verify `minecraft:pillager_outposts` membership in the *effective* active data, including possible Savage & Ravage assets.
- Next **owner action: none for Mesa specifically now**. Only ask for a disposable-world `/place structure ctov:pillager_outpost_mesa` check if the effective current profile presents a genuine ambiguity. Even a successful `/place` would prove registry/placeability, **not** natural generation.
- Preserve `ctov:pillager_outpost_badlands` Tier2 as a **provisional** archetype until its actual hostile spawn and selector behavior are checked; do not auto-create or broaden DD to all CTOV variants.

No source file, CTOV settings, worldgen selector, spawn count, tier, or live DD config was altered.
