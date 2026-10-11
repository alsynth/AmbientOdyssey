# Ambient Odyssey — Dungeon, Encounter & Boss Editability Audit
**Date:** 11 October 2026  · **Baseline:** `experimental/v041-streams-minecells-questlog-combined-20261011` (source and historic resource census) · Minecraft 1.21.1 / NeoForge 21.1.252

> **Important status distinction:** Research and source/config scan, **not** a complete per-JAR mechanic/NBT runtime test. The older `INSTALLED_MOD_STRUCTURE_SCREENING.csv` has 66 structure/template resource providers from a historic Test5 inventory; the active v0.4.1 release lock adds content and removes some historical projects. The accompanying catalogue marks origin explicitly, rather than falsely calling every one installed. The 119 release-lock additions also contain non-encounter dependencies and client assets, not 119 dungeon mods. Build/imported manifest plus runtime jar list remain authoritative.

## Deliverable and scale

The machine-readable [encounter feasibility catalogue](./V041_ENCOUNTER_EDITABILITY_MATRIX.csv) records **103** historical or current structure, mob, boss, dimension, wave and combat-system leads, each with a control grade, possible editing route, limits/unknowns, and provisional tier ceiling. Encounter-family counts: boss 10; boss-arena 5; framework 4; infrastructure 2; mixed 32; mobs 8; prefab 4; realm 14; settlement 7; spawner 16; wave 1.

**Grade legend (potential engineering route, not verified fix):** P0 non-combat infrastructure; P1 peripheral settlement/mixed architecture; P2 encounter is plausibly editable through datapacks/NBT/spawn/loot overrides and location-scalers; P3 known native boss config or boss/wave/integration system, with source inspection still needed for hard-coded mechanics. These grades do **not** mean every individual boss feature works with a given scaling mod.

## 1. Native config proofs (real paths in the active source)

| System | What the actual committed config exposes | Implication |
|---|---|---|
| Dungeon Crawl | `config/dungeon_crawl.toml`: `custom_spawners=true`, `spawner_entities=6` (equipment variety), `spawner_activation_range=12`, `natural_despawn=true`, and `overwrite_entity_loot_tables` | **High encounter-reauthoring potential.** A custom equipped-mob spawner is an advantage, but a config controlling variety is not automatically a per-room equipment editor |
| Bosses of Mass Destruction | `config/bosses_of_mass_destruction.json5`: Lich HP 300; Obsidilith HP 300 / armor 14 / attack 16; Gauntlet HP 250; Void Blossom HP 350; individual attacks, regeneration and drops | **High direct boss-stat control**; keep phase mechanics and time-to-kill separately measured |
| L_Ender's Cataclysm | `config/cataclysm-common.toml`: broad bosses, abilities, attacks, equipment parameters | **High native control**, but scripted immunity/animation windows and special damage types require dedicated tests |
| Iron's Spells 'n Spellbooks | `config/irons_spellbooks-server.toml`: Dead King and Tyros `additionalHealth` / `additionalAttackDamage` | **High confidence** in direct HP/damage adjustments; spell cast timings and arena logic require separate verification |
| Ice and Fire | `config/iceandfire/iaf-common.json`: dragon HP and elemental attack damage, spawn odds, some loot flags, other mob stats | **High mob and dragon tuning**; rare-dungeon cave/dragon states still need live verification |
| Mowzie's Mobs | `config/mowziesmobs-common.toml`: boss health/attack multipliers, has-boss-bar and reset-on-respawn flags | **High direct control**; test AI patterns and equipment access |
| F.D. Bosses | `config/fdbosses/bosses.json`: Chesed, Malkuth, Geburah damage, mechanics, phase HP caps, difficulty multipliers | **High precision**, test effects that scale based on current HP or number of participants |
| Block Factory's Bosses | `config/block_factorys_bosses-server.toml`: Sandworm/Yeti/Dragon/Knight/Kraken HP, armor and base attack | **High direct control**; arena and mechanics may be code-defined |
| Eternal Starlight | `config/eternal_starlight.json`: per-entity HP/armor/damage, boss respawn and loot-chest flags | **High flexibility** for the realm's fights, distinct from a blanket high-tier dimension |
| Brutal Bosses | `config/brutalbosses.json`: health multiplier, damage multiplier, boss spawn chance | Broad normal-mob miniboss pressure; check entity compatibility and scaling overlap |
| Apotheosis / Apothic Spawners | `config/apotheosis/apotheosis.cfg` / `config/apothic_spawners.cfg`: boss/affix/loot and spawner-related rules | **High system control** but stacking Apotheosis affixes, Dungeon Difficulty and custom equipped spawner NBT can overbuff mobs |
| Remnant Bosses | `config/remnant/bosses/*.json`: per-boss named files | Strong config entry point; precise stat keys must be read before claiming specific tunability |
| Mutant Monsters | `config/mutantmonsters-common.toml`: spawn weights 0.01 | Rarity proven; boss stats not proven by this config |

These entries prove *some* tunability, not unlimited mathematical balance. Geometry, waves, scripted attack phases, resistances and damage caps remain separate variables.

## 2. Structure-specific feasibility — do not mistake 'spawn rate config' for difficulty support

**High-priority structure family:** When Dungeons Arise + Seven Seas, Dungeon Crawl, Adventure Dungeons, Dungeons and Taverns, IDAS, Integrated Stronghold, YUNG fortresses/mineshafts/monuments, Better Bastions, Luki's Mansions, Trek, Archaion, Apotheosis towers, and Mine Cells.

Recommended engineering order for each **named structure ID** (not a whole mod):
1. Classify encounter *source*: JSON-defined structure + template pool, legacy NBT template, trial spawner, vanilla mob spawner with embedded `SpawnData`, command/loot-table spawn, entity AI, or generator code.
2. Inventory exact `SpawnPotentials` / equipment NBT, `minecraft:trial_spawner` normal/ominous configurations and `minecraft:vault` reward modes as applicable. **Never assume** a vanilla spawner or trial spawner appears in every structure.
3. Identify `data/<namespace>/worldgen/structure/*.json`, template pools, processor lists, entity NBT and chest loot table IDs, plus any built-in datapacks. Validate overrides have identical registry paths and are actually activated via AO's Paxi pipeline.
4. Adjust enemy population/equipment, ability support, localized difficulty and vault rewards independently; keep a boss fight's scripted phase count sensible.
5. Check target mobs' active registry attributes, armor cap, damage type handling, and any per-entity attributes that third-party difficulty scalers **do not affect**.
6. Spawn and repeat the structure with one, two and three geared players. Compare completion time, wipe risk, ammo/food consumption, loot progression, lag and server spawn caps.

**Tier ceiling rule:** If a dungeon cannot change *wave composition, effective enemy capabilities or encounter geometry* beyond a simple HP multiplier, it should not be promoted to the top combat tiers. If the entire structure is decorative/peaceful, it stays T0–T2 rather than being forcibly balanced upward. Every high-tier dungeon needs a repeatable challenging combat loop, not just a high-level entity somewhere nearby.

## 3. Nine-tier policy to preserve

**Previously accepted anchor placements:**
- **T4:** Mine Cells (midgame); the Wither was suggested at roughly T4.
- **T6:** Ignis; Iron's **Dead King** currently T6.
- **T7:** Maledictus.
- **T8:** Scylla and Tyros.
- **T9:** reserved for genuinely bespoke superboss-level tests; assigning an existing boss here requires proof, not bigger HP numbers.

Other modded dimensions should **not** be lumped into one difficulty tier (Aether may be treated as an exception). A boss is generally intended to be soloable, with only the rarest 1–3 bosses per tier designed as deliberate team challenges. The established progression concept uses roughly **90% tier completion** rather than requiring every optional rare boss.

**Provisional structure ceilings**, not assertions about current gameplay:
- Decor and lightly guarded locations: T0–T2.
- Standard equipped-spawner dungeons and varied small strongholds: T1–T4.
- Large purpose-built spawner/trial/vault gauntlets: T3–T5, possibly T6 only after encounter redesign.
- Native named bosses and special arenas: match individually accepted boss-tier placement.
- Top scripted multi-phase encounters: T6–T9 only with actual combat mechanics and party tests.

## 4. Dungeon Difficulty — recovered, still NOT on active lock

**Best fit:** [Dungeon Difficulty](https://www.curseforge.com/minecraft/mc-mods/dungeon-difficulty/files/9110961), **3.9.2+1.21.1 NeoForge**, file **9110961**, published 9 October 2026. Source [DungeonDifficulty README](https://github.com/ZsoltMolnarrr/DungeonDifficulty/blob/1.21.1/README.md).
- Difficulty resolution priority: **structure → biome → dimension**. Config `config/dungeon_difficulty_v2.json`.
- Explicit tag / exact ID / regex matching; location-adjusted mob attributes, spawner behavior, loot scaling, optional player debuffs and player-count effect. Per-player difficulty is **multiplayer scaling**, not proof that cleared dungeons inherently get harder with exploration count.
- **Key limitation:** An external boss may have scripted attacks or resistances bypassing attribute modifiers. Built-in loot scaling can yield permanent item power inflation that compounds with Apotheosis, Cataclysm, spell/Curios gear and player progression. **Disable or tightly constrain automatic equipment power scaling initially**, keep hand-authored high-value boss rewards.
- Use custom structure tags in AO Paxi for fixed tier zones. Need source-backed mapping from *exact current registry IDs*, not file/display names.
- The mod also offers a `no_mining` location effect, but intrusive anti-mining in vanilla-like structures should be deliberately selected and must not break quest access or repairs.
- **Different mechanic:** [Difficulty by Distance](https://modrinth.com/mod/difficulty-by-distance) makes danger grow with distance; [Dynamic Difficulty](https://www.curseforge.com/minecraft/mc-mods/dynamic-difficulty-mod) adds area/mob/player dependent levels. They overlap with Dungeon Difficulty: **choose one central scaler**, not several uncontrolled multipliers.
- [Difficulty+](https://github.com/KevzCz/DifficultyPlus) is an optional add-on for Dungeon Difficulty offering per-structure randomized levels and in-game editing. First validate its exact 1.21.1 NeoForge version/dependency closure; no automatic install.

## 5. Missing / forgotten research candidates versus today's release lock

| Candidate | Historical source | Current decision |
|---|---|---|
| **Dungeon Difficulty** | Original 166, #117 | **Highest-priority new balance system for controlled trial**, not yet installed |
| **Boss Ultimatum** | #100 | **High priority** for restoring boss health/despawning after party wipes; prevents infinite suicide attrition |
| **Multiplayer Bosses** | #101 | **Alternative A** for nearby-player boss HP/loot scaling; do not count all online players |
| **Multiplayer Boss Attribute Modifier** | #102 | **Alternative B** for HP/damage/armor scaling; choose A or B, not both |
| **AttributeFix** | #90 | Research for extreme boss attributes / caps; cap changes do not change armor damage math |
| **Iron's Spellbooks Tweaks** | #109 | Relevant to both player magic runaway and spell power/rarity; high priority research |
| **Apothic Ascension** | #37 | Late-game Apotheosis expansion, only after elite/superboss tier budget |
| **EpicQuestDungeoning** | #21 | Replayable keyed/group dungeon design with AO-authored content; high-priority repeatable endgame research, not drop-in combat balance |
| **The Birth of Steve** | #115 | Rare/procedural dungeon/endgame content; user left boss tier **unranked** pending research |
| **Nether Trials & Chambers** | #5 | Direct match to the intended harder trial/vault reward loop; version/binary verification needed |
| **ArcadiaDungeon** | #20 | Dedicated-server-oriented wave/difficulty framework; earlier identified as poor fit for solo-first AO |
| **DungeonZ / AdventureZ** | #17/#18 | Fabric/Connector experimental alternatives; no automatic add |
| **Savage Ender Dragon** | #23 | End boss mechanics audit when final End progression is balanced |
| **Ancient Remnants: Monoliths** | #4 | Do not assume it is identical to the installed `Ancient Remnants` mod: verify exact identity |
| **Born in Chaos** | Source lock `remove_projects` | **Explicitly removed** in current source; do not pretend it is still installed |
| **Repurposed Structures** | Source lock `remove_projects` | **Explicitly removed** in current source despite older structure census listing |
| **Sunken Spires** | Historic backlog | Deferred ocean content; do not auto-install |

Other previously evaluated candidates to preserve for the later expansion backlog: Dimensional Dungeons (now added in 0.4g), Ancient Remnants (0.4g), Archaion (Test6), Integrated Mowzie's and Integrated BOMD (already source-added), plus repeatable trials/structure authorship.

## 6. Balancing guardrails and tests

- Boss HP is only one axis: build a threat budget for telegraphed damage, punishable attack windows, phase changes, healing, control, projectile speed and area denial.
- Spawner-heavy structures need explicit maximum active mobs, mixed ranged/melee/magic composition, equipped-mob loot gating, and player protection from farmable overpowered spawner drops.
- Trial chambers/vaults require stronger wave compositions **and** substantially better rewards, per the earlier pack decision; audit keys/ominous modes and trapped-door access as well.
- Two or more scalers multiplying HP/attack independently are **not acceptable** without a mathematical cap table. Cross-test Apotheosis elites, Brutal Bosses, native boss configs, and trial spawners.
- Separate **AO–Combat** and **AO–Structures** modular test packs so users need not regenerate a FreeTerraForged/Streams world for every boss iteration; run a full-content client/server regression checkpoint before acceptance.
- Retain the currently working Mine Cells / Streams Reflowing addon; avoid changes to dungeon structure generation, salts and Connector dependencies while evaluating balance.
- Preserve original/rollback. **No mod installed, no balance config edited, no world generation changed** by this research-only branch. Actual per-structure trial spawner registry inspection, full binary NBT audit, and 5–7-person multiplayer performance testing remain undone.

## 7. Source provenance

- `INSTALLED_MOD_STRUCTURE_SCREENING.csv` — 66 historical resource-level structure/template contributors, **not all still installed**.
- `release_030/release-lock.json` — active source-level additions/removal intents and exact file pins.
- `release_030/evidence/CANDIDATE_REGISTRY_2026-10-06.md` — original 166 candidate descriptions and constraints.
- `docs/audits/EARLIEST_MOD_LIST_RECONCILIATION_2026-10-10.md` — previous staged reconciliation.
- `release_030/overrides/config/...` — directly inspected committed native config files above.
- Public Dungeon Difficulty / Dynamic Difficulty / Difficulty by Distance / Difficulty+ official pages linked above.

**Next implementation package** should be a reversible `AO Balance Lab 0.1` using Dungeon Difficulty alone, a small structure-tag tier sample, existing boss configs, conservative loot rules and scripted acceptance checks. Do **not** reclassify all structures into tiers on resource data alone.
