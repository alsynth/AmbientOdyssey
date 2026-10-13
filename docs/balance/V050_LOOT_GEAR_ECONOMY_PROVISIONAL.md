# Ambient Odyssey — Loot classes, gear bands, and reward economy (provisional v0.5)
**13 Oct 2026 · DESIGN ONLY. Not live odds, recipes, loot tables, or measured drop rates.**

## Approved policy / constraints to preserve
1. **Hybrid approach**: retain recognizable native unique/thematic drops and puzzles; rebalance **generic** loot and create AO-owned additions where useful, never bulldoze an entire mod's loot ecosystem.
2. **T0–T2 mostly unchanged.** Specifically **early Mine Cells loot remains unchanged**. Do not blanket-transform every chest or instantly inflate early progression.
3. Five independently meaningful **container classes**: **Scrap, Supply, Equipment, Treasure, Grand Treasure**. Container class measures value *within its tier*. Structure tier measures encounter difficulty. A T5 Supply chest is not automatically better than T4 Grand Treasure in every dimension, and no major named boss should rely on random ordinary chest rolls.
4. Lootr provides **per-player chest instancing**, not progression scaling; validate per-source tables and reward credit. Minimize incentives for mass farming free high-tier equipment.
5. High-end **Apotheotic gem** grade ladder (names as used in AO port): `Perfect < Ancient < Artifact < Heirloom < Esoteric`. These are **not** identical to Apotheosis affix/item rarities. Data components, tooltip names and gem-case behavior require validation in the exact current compiled port.
6. User intent: **T6 boss-specific Artifact rewards**; **strong T6 unlocks Pinnacle and Ancient world-access**; **T7 bosses may yield Artifact / Heirloom**; **T8 bosses can yield Esoteric**; **T9 expects Heirloom–Esoteric-quality player builds**. The final mastery quest should **upgrade a held item to Heirloom**, but the actual technical route and recipe must be validated, not invented.
7. Goblin-Tuned trade gear remains a prestigious alternative: adjust costs first, not the +0.5 ADD_MULTIPLIED_BASE armor component. Respect the existing trade API's two input slots. Details: `docs/balance/V041_GOBLIN_TUNED_TRADE_ECONOMY.md`.
8. Apotheosis affix armor random trim is **cosmetic**, preserves existing trims and must not affect loot value/roll/chest chance: `docs/balance/V041_APOTHEOSIS_RANDOM_AFFIX_TRIMS_DESIGN.md`.

## Container identity (authoring contract)
| Class | Purpose | Contents / design | Restriction |
|---|---|---|---|
| **Scrap** | Environmental storytelling, low stakes | Loose materials, recoverable crafting leftovers, small food/material rewards | Never high-tier exclusive/quest-gating item |
| **Supply** | Sustain an ongoing expedition | Food, arrows, potions, torches, ropes/utility where native IDs exist, modest repair materials | May remain valuable at high tier without competing with boss trophies |
| **Equipment** | A meaningful choice for one slot | Armor, weapons, spell equipment and supported affix rolling with tier ceiling | **Never** guarantee overpowering named boss-grade components from ordinary spawner-farmable loot |
| **Treasure** | High-value exploration result | Smaller rare accessories/components, non-exclusive relic chances, valuable enchanting/gear ingredients | Higher tier improves quality, not arbitrary quantity 10× |
| **Grand Treasure** | Large set-piece, final locked room, special quest | Thematic unique reward plus a curated gear/material selection; structure identity preserved | Distinguish *one-time* progression-specific reward from renewable loot |

### Mapping algorithm: **structure × container**
1. Get effective structure ID, group/pool and actual chest location. Determine named locked/boss chest vs ordinary crate; **NBT/template evidence required**.
2. Map each chest source to a class using original context; do not globally label all `minecraft:chests/simple_dungeon` containers T5 because one T5 structure invokes it.
3. Apply one AO per-tier **generic** reward pool while preserving native thematic entries (or leave original alone if compatibility requires).
4. Grant mandatory quest rewards via a validated once-per-player milestone route, **not** by setting super-rare chest contents that gate everyone.
5. Apply affix rarity/gem ceiling **after** resolving the player's unlocked progression level and native item NBT/data components. Do not double-roll with Apotheosis and other global loot modifiers.
6. Record repeatability: structure chest per-player once / replenishable spawner drops / repeatable boss trophy / account-limited prestige reward.

## Provisional rarity-access matrix (not percentages)
| Enemy/structure tier | Generic chest baseline | Boss-specific gem/high-grade access | Other gear story |
|---|---|---|---|
| **T0–T2** | Mostly **native unchanged** | No Artifact/Heirloom/Esoteric; normal low-tier gems retain native progression | T2 benchmark: enchanted diamond plus 2 grade-A supports, but gear not necessarily given directly |
| **T3** | Modest increase in good supply/equipment, thematic treasure | No high-tier gem grade | Early useful affix item or unique exploration reward; no mastery free pass |
| **T4** | Distinct well-guarded treasure/vaults; no single chest should replace several hours of gear progression | Standard gem progression up to Perfect if source/reward route supports it | Better enchanting, socketing ingredients, strategic resistance gear; Mine Cells early loot unchanged |
| **T5** | More consequential Equipment/Treasure + bosses' own native reward | Perfect-grade rewards; **Ancient not generally random yet** | Favors complete build and first notable affix/special utility items |
| **T6** | Major dangerous dungeon cap and dedicated boss trophy | **Boss-only Artifact**, strong T6 milestone enables future Ancient-access; don't scatter Artifact in ordinary chests | Dead King or comparable T6 unlock route **provisional** |
| **T7** | Grand Treasure/unique boss rewards; ordinary crates stay mostly sustain | **Artifact and Heirloom** from named boss or major first-clear; Ancient standard through Pinnacle where verified | Intended long-endgame mastery, avoid spawner drops producing these grades |
| **T8** | Limited elite unique rewards, difficult repeatable rewards | **Esoteric** from named Tier 8 boss or other deliberately authored late-game systems | T8 uniques cannot be devalued by generic enchanted mobs |
| **T9** | Signature trophies, scarce cosmetic/exclusive crafting options | Heirloom–Esoteric builds expected; **no automatic higher invented tier** | The final quest's Heirloom held-item upgrade is a controlled milestone, not a new chest drop |

**Distinguish** a gem grade from an equipment affix rarity: a high rarity affix item need not have a high grade socketed gem, and vice versa.

## First implementation candidate probabilities (all **placeholder**)
To avoid fake precision, start with *chest-class composition by structure*, **not** claiming item rarity odds measured from mod sources. For a sampled dungeon's meaningful chest inventory **class distribution**, provisional defaults:
| Structure T | Scrap | Supply | Equipment | Treasure | Grand Treasure | Notes |
|---|---:|---:|---:|---:|---:|---|
| 0–2 | preserve native | preserve native | preserve native | preserve native | preserve native | Don't force policy onto early-world loot |
| 3 | 20% | 45% | 20% | 15% | 0% | This is a **design target for chest archetypes**, not a native loot-roll probability |
| 4 | 10% | 35% | 30% | 20% | 5% | Restrict Grand to specifically authored set-pieces; split can vary by structure |
| 5 | 5% | 30% | 30% | 25% | 10% | Large mixed dungeons should retain supplies mid-route |
| 6 | 0% | 25% | 30% | 30% | 15% | Do not grant Grand each time a farmable spawner respawns |
| 7–9 | special/manual | special/manual | special/manual | special/manual | special/manual | Boss-tier loot authored per encounter, not this ordinary-dungeon distribution |

**Interpretation:** these are % shares of *designed chest archetypes in a sample dungeon*, not independent item drop probabilities; never blindly turn this table into per-roll `weight` values. A structure with one singular treasure room receives a hand-selected class, not percentages.

## Player gear readiness rubric (qualitative until measured)
| Tier | Expected viable setup | Clear warning signals | Build diversity |
|---|---|---|---|
| 0–1 | Vanilla survival basics: armor, shield or dodge, food, travel | Night mobs kill new player very quickly | Melee/ranged default both valid |
| 2 | **Enchanted diamond** and **≥2 grade-A combat-support items** (existing AO design anchor) | Two ordinary enemies overwhelm player without warning | No compulsory unique Origin or spellbook |
| 3 | Developed enchants, one clear fighting style, decent healing/range | Unavoidable AoE or frequent gear break | Melee/ranged/spell routes should work |
| 4 | Sustain/resistance prep, multiple usable utilities, first substantial affixes or niche relic | Boss drops in one hit despite defensive prep | Viable solo Mine Cells / early dimension encounters |
| 5 | Coherent offensive + defensive synergies, non-trivial accessories, better targeting/positioning | Requires perfect rare drop or one cursed ring | Multiple independent loot routes |
| 6 | Endgame-ready with enchant/affix and specialist response tools, likely good gem kit | Arbitrary DPS/HP check with no alternative | T6 boss reward unlocks further gear |
| 7 | Pinnacle-aware Ancient access and Artifact/Heirloom path, viable control/avoidance | Generic T4 loot invalidates all upgrades | Strong but readable combat |
| 8 | Heirloom / Esoteric targeted build, advanced fight-specific counters | Forced single invincible item/Origin | High specialization but nonmandatory |
| 9 | Mastered Heirloom–Esoteric builds, telegraph literacy, pressure resilience | Boss-only works for scripted 5+ player group | Soloable ideally; rare team-oriented prestige variant acceptable |

No raw HP, weapon DPS or spell coefficient targets can be responsibly locked without actual equipment-stat survey and boss combat probes. Log each candidate's **damage taken per telegraphed hit, %HP swing, kill time, potion usage and performance** before publishing numbers.

## Four critical economy controls
**Apotheosis:** audit exact `apotheosis:rarity`, affix components, sockets and global loot modifier order; keep *world rarity*, *gem grade* and *container class* independent. Do not accidentally give a Tier 8 gem through generic Tier 2 chest loot.

**Goblin Traders:** actual NeoForge implementation allows tuned chainmail for **1–3 iron plus 6–14 emeralds**; earlier proposed **4–8 diamonds + 16–32 emeralds** is a **trial economy placeholder**, pending measured material flow. Netherite currently trades at **2 Nether Stars + 1 Dragon Head**; do not harden costs without Wither farmability analysis. Don't overwrite trade output components.

**Relics/Artifacts/Curios/Spell gear:** draw from validated native mods' item families; check how powerful support items bypass raw armor/HP assumptions. No mandatory Origin, curse, one spell school or exact RNG item.

**Mine Cells/Trial Chambers:** preserve baseline Mine Cells early rewards. Separately author improved **Tier 4 Trial Chamber waves/vault rewards** only after actual normal/ominous/vault source data inspection; do not assume Dungeon Difficulty rewrites trial configuration.

## Acceptance checks before gameplay
- All rollable items resolve to installed IDs; native thematic loot preserved on sampled WDA, IDAS, Mine Cells, Cataclysm and Twilight Forest set pieces.
- No infinite early reward: kill-spawner mob drop, respawned boss, logout/reload, Lootr per-player reopen, regenerated structure.
- No progression lock from an untradeable rarity or random boss drop; accessible alternative path.
- Validate first-clear guarantee and party credit with two client accounts; compare 1-player vs 5–7-player reward supply.
- Measure actual component stats to understand armor multipliers, spells, healing, invulnerability and crit loops.
- Check corrupt/special Gem Case insertion/reload behavior after Remnant 2.7.0 and Apotheotic port updates.

**Deliverable stage:** specification and trial composition only. Do not represent these as installed JSON or in-game-tested values.
