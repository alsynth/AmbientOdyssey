# Ambient Odyssey — Structure tier/registry mapping v3 (13 October 2026)

**Research-only mapping. Not implemented, not a worldgen scan of the current AO profile, not gameplay-tested.**

## Contents

- [Approved provisional tier catalogue v3 (CSV)](./AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv): **427 records**, including **326 inherited v2** and **101 new individually named entries**.
- [Entire historical GitHub structure registry crosswalk (CSV)](./AO_HISTORICAL_STRUCTURE_REGISTRY_CROSSWALK_2026-10-13.csv): **1,219 historical native structure IDs** matched against catalogue v3. **361 unique native IDs** have a direct catalogue match; the other 858 are not necessarily combat dungeons (many are decorative variants, structures in removed mods, or unreviewed content). Do not infer they all need balance rules.
- **41** hidden reference rows: 35 original family placeholders, 5 YUNG structures absent from the checked AO client mod list, and 1 superseded Maledictus location alias. None is an independent active balance rule.
- **386 individually named active-candidate rows now have mapped structure IDs** (including ten Twilight Forest source-verified IDs and YUNG's Better Ocean Monument). Mapping against the current installed build is **still pending**.
- **96** newly proposed tier placements remain provisional; **Sky Arena and Ice Arena are user-approved Tier 3**, while **Geburah Arena alone remains unassigned**. Existing v2 tier values remain user-approved *provisional*, not runtime verified.

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

## Resolved mapping corrections (13 October 2026)

- **Maledictus**: real site is **Frosted Prison**, registered `cataclysm:frosted_prison`, **Tier 7**. The old “Cursed Graveyard — Maledictus” row 98 is an archived non-actionable alias; `Frosted Prison — Maledictus` row 359 is canonical. Validate precedence of Integrated Cataclysm resource overrides in the effective current datapack.
- **Sky Arena** (`skyarena:sky_arena`) and **Ice Arena** (`skyarena:ice_arena`): **Tier 3**, explicitly user-confirmed.
- **Geburah Arena** (`fdbosses:geburah_arena`): **tier undecided**; preserve null, do not infer Tier 7 from Chesed/Malkuth.
- **Ten Twilight Forest structures**: the 1.21.1 upstream generated structure JSON files provide exact IDs `twilightforest:naga_courtyard`, `lich_tower`, `labyrinth`, `hedge_maze`, `dark_tower`, `knight_stronghold`, `aurora_palace`, `hydra_lair`, `troll_cave`, `final_castle`. Source: [TeamTwilight 1.21.1 generated structure folder](https://github.com/TeamTwilight/twilightforest/tree/1.21.1/src/generated/resources/data/twilightforest/worldgen/structure). A source ID is not evidence of current AO runtime.
- **YUNG's Better Ocean Monuments**: mapped `betteroceanmonuments:ocean_monument`; confirmed upstream [YUNG-GANG 1.21.1 structure JSON](https://github.com/YUNG-GANG/YUNGs-Better-Ocean-Monuments/blob/1.21.1/Common/src/main/resources/data/betteroceanmonuments/worldgen/structure/ocean_monument.json). Logged as installed in AO's **11 October** v0.4.1 client.
- **YUNG's Better Nether Fortresses**: logged in AO's **11 October** client; its historical `betterfortresses:fortress` Tier 4 mapping remains. Do not incorrectly claim both vanilla fortress and its replacement spawn independently.
- **Not listed in inspected AO 11 October client log**: **YUNG's Better Dungeons**, **Better Desert Temples**, **Better Jungle Temples**. Their original entries are archived reference only, not live dungeon scaling targets. The Better Dungeons mod itself has real dungeons but should not be treated as installed without a newer JAR manifest.
- YUNG's **Better Mineshafts**, **Better Witch Huts**, **Better Ocean Monuments**, and **Better Nether Fortresses** *were* seen in that log. Exact latest v0.4.8/r19 JAR roster still must be checked.

### Remaining identity limitations
There are **no blank registry-ID cells among the 386 named active candidates**, but the following are not solved by this alone: 1) Overworld WDA Heavenly variants share source IDs with End listings without proof separate Overworld variants exist; 2) multiple structures may share native IDs or replace vanilla definitions; 3) historic candidates may be absent in the current import; 4) some code-defined or integrated structures have different loaded-asset precedence.

## Must check before implementation

1. Enumerate the exact active client/server JARs from the newest full-pack release (not old `main` or a branch-only release lock), note removed projects and integrated arena resource precedence.
2. Verify mapped upstream Twilight/YUNG IDs against the exact currently installed client/server JARs; Maledictus location is resolved to Frosted Prison.
3. Confirm source biome tags, actual generated dimension, merged datapack overrides, WDA Heavenly variants, Luki's replacement and structure-set placement.
4. Inspect spawner and trial-spawner NBT, boss triggers, entity AI, vaults and loot tables per real structure. Dungeon Difficulty attribute scaling alone does not guarantee full boss/spawner/loot control.
5. Have the user approve *new* v3 tier suggestions separately; don't modify approved v2 tier values without new instructions.
6. Preserve rollback and performance branches. This documentation-only branch must not alter the active pack.

**Provenance:** historical `STRUCTURE_REGISTRY_CATALOG.csv` from GitHub `main` (1,219 names); v2 user-approved provisional structure tier list captured on 13 October; v3 technical identity/dimension reconciliation. Historical registry is not an effective current runtime inventory.
