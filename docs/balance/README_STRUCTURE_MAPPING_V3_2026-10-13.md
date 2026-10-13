# Ambient Odyssey — Structure tier/registry mapping v3 (13 October 2026)

**Research-only mapping. Not implemented, not a worldgen scan of the current AO profile, not gameplay-tested.**

## Contents

- [Approved provisional tier catalogue v3 (CSV)](./AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv): **427 records**, including **326 inherited v2** and **101 new individually named entries**.
- [Entire historical GitHub structure registry crosswalk (CSV)](./AO_HISTORICAL_STRUCTURE_REGISTRY_CROSSWALK_2026-10-13.csv): **1,219 historical native structure IDs** matched against catalogue v3. **361 unique native IDs** have a direct catalogue match; the other 858 are not necessarily combat dungeons (many are decorative variants, structures in removed mods, or unreviewed content). Do not infer they all need balance rules.
- **35** old family placeholders retained for provenance; hidden from ordinary catalogue views, **not** independent registered structures.
- **17** individually named entries lack a provable distinct structure ID and require current mod JAR/code examination.
- **98** extra proposals have new v3 tier values requiring explicit user review. **3** newly identified boss arenas/structures are deliberately unassigned pending tier decisions. Existing v2 tier values remain user-approved *provisional*, not runtime verified.

## Binding user decisions

- WDA Aviary: The End **Tier 6** (native `dungeons_arise:aviary`).
- Vanilla Nether Fortress: **Tier 4** (`minecraft:fortress`).
- All Bastion Remnant layouts (Bridge, Housing, Hoglin Stables, Treasure Room): **Tier 5**; these are **one registry ID**, `minecraft:bastion_remnant`, not four IDs. Per-variant balancing needs template/piece recognition.
- WDA Keep Kayra: **Tier 6** (`dungeons_arise:keep_kayra`).
- Twilight Forest Hydra Lair: **Tier 4** (distinct from Ice and Fire Hydra). No trustworthy distinct registered ID from historical JSON list.
- Luki's Ancient City: **Tier 7 provisional**; vanilla Ancient City **Tier 6** if separately active. Resolve replacement to avoid double-counting.

## Source-derived dimension corrections

- `idas:necromancers_spire` — Nether, not Overworld.
- `irons_spellbooks:ancient_battleground`, `irons_spellbooks:citadel` — Nether, not Overworld.
- `eternal_starlight:portal_ruins_common`, `portal_ruins_cold`, `portal_ruins_forest`, `portal_ruins_jungle` — Overworld entrances.
- The `dungeons_arise:heavenly_challenger`, `heavenly_rider` and `heavenly_conqueror` IDs are listed as End dimension structures. Distinct historical *Overworld* registrations are **not evidenced**; preserve user-intended logical variants but don't implement a phantom Overworld tier rule.

## Named entries with no proved distinct ID (17)

- `YUNG’s Better Dungeons`: **Spider Cave** (AO T2)
- `YUNG’s Better Dungeons`: **Zombie Dungeon** (AO T2)
- `YUNG’s Better Dungeons`: **Skeleton Dungeon** (AO T2)
- `YUNG’s Better Desert Temples`: **Better Desert Temple** (AO T3)
- `YUNG’s Better Jungle Temples`: **Better Jungle Temple** (AO T3)
- `YUNG’s Better Ocean Monuments`: **Better Ocean Monument** (AO T3)
- `Cataclysm`: **Cursed Graveyard — Maledictus** (AO T7)
- `Twilight Forest`: **Naga Courtyard** (AO T2)
- `Twilight Forest`: **Lich Tower** (AO T3)
- `Twilight Forest`: **Labyrinth** (AO T3)
- `Twilight Forest`: **Hedge Maze** (AO T3)
- `Twilight Forest`: **Dark Tower** (AO T4)
- `Twilight Forest`: **Goblin Knight Stronghold** (AO T4)
- `Twilight Forest`: **Aurora Palace** (AO T4)
- `Twilight Forest`: **Hydra Lair** (AO T4)
- `Twilight Forest`: **Highlands Troll Cave** (AO T5)
- `Twilight Forest`: **Final Castle** (AO T5)

## Must check before implementation

1. Enumerate the exact active client/server JARs from the newest full-pack release (not old `main` or a branch-only release lock), note removed projects and integrated arena resource precedence.
2. Scan code-generated Twilight Forest/YUNG structures and Maledictus site rather than guessing IDs from display names.
3. Confirm source biome tags, actual generated dimension, merged datapack overrides, WDA Heavenly variants, Luki's replacement and structure-set placement.
4. Inspect spawner and trial-spawner NBT, boss triggers, entity AI, vaults and loot tables per real structure. Dungeon Difficulty attribute scaling alone does not guarantee full boss/spawner/loot control.
5. Have the user approve *new* v3 tier suggestions separately; don't modify approved v2 tier values without new instructions.
6. Preserve rollback and performance branches. This documentation-only branch must not alter the active pack.

**Provenance:** historical `STRUCTURE_REGISTRY_CATALOG.csv` from GitHub `main` (1,219 names); v2 user-approved provisional structure tier list captured on 13 October; v3 technical identity/dimension reconciliation. Historical registry is not an effective current runtime inventory.
