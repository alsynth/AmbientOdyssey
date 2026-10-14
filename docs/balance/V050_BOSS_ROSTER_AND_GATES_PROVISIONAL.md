# Ambient Odyssey — Boss roster, tiers, and progression gates (provisional v0.5)
**13 October 2026 · DESIGN ONLY · no mods/config/quests changed**

## Sources and authority
Read `docs/balance/README_STRUCTURE_MAPPING_V3_2026-10-13.md`, `docs/balance/AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv`, `docs/questing/QUEST_CAMPAIGN_ARCHITECTURE.md`, and the v0.4.1 boss-editability audit. Do not treat a **structure tier** as a boss tier: a hostile ruin can be T4 while its boss is higher, and vice versa. All newly suggested encounters below are placeholders until source/JAR verification and user approval. Preserve explicit decisions. Before implementation compare against the **v0484 r19 consolidated** JAR roster, not `main` or historical scanner rows.

## Decision ledger (do not silently change)
| Boss / encounter | Intended boss tier | Decision status | Notes |
|---|---:|---|---|
| Sky Arena structure, Ice Arena structure | 3 | User confirmed | Structure tiers; boss identity separately audit |
| Twilight Forest Hydra Lair | 4 | User confirmed | **Not** Ice and Fire Hydra |
| Maledictus — `cataclysm:frosted_prison` | 7 | User confirmed | Single real site; obsolete “Cursed Graveyard” row is archived |
| Cataclysm Ignited Revenant, Coralssus, Kobolediator | 6 | Prior user tier plan | Mid-to-late minibosses; entity presence/IDs verify |
| Netherite Monstrosity, Ancient Remnant, Ender Guardian, Ender Golem | 7 | Prior user tier plan | Ender Golem classified in earlier tier choice; boss vs miniboss verify |
| Ignis, Leviathan | 7 | **Most recent user tier roster** | An older planning message suggested T8; **newest user grouping T7 takes precedence**; keep this discrepancy in decision log |
| Ice and Fire Hydra | 7 | User tier plan | Different from Twilight Forest Hydra |
| Ossukage, Kotsukage (Remnant Bosses) | 7 | User tier plan | Target Remnant Bosses **2.7.0** before balancing; issue #43 |
| Chesed, Malkuth (F.D. Bosses / Qliphoth) | 7 | User tier plan | Engine has nonstandard damage/phase mechanics; arena IDs available |
| **All five Bosses’ Rise encounters** | 8 | User tier plan | **Do not conflate** this mod with **Block Factory’s Bosses**: Sandworm/Yeti/Dragon/Knight/Kraken have independent configs. Individual Bosses’ Rise entity IDs/name scan pending |
| Umbrakar (Remnant Bosses) | 8 | User tier plan | v2.7.0 mechanics/config re-audit needed |
| Last of Deepslate (Archaion) | 8 | User tier plan, binary check | Confirm installed version and encounter asset before wiring |
| Tyros (Iron's Spells), Scylla (Cataclysm) | 9 | **Latest explicit user tier decision** | Older v0.4.1 docs placed them T8; newer user choice T9 supersedes |
| **Third Tier 9 encounter — The End** | 9 | **Reserved; no boss selected** | Needs a genuinely distinctive final End encounter; no automatic promotion of Obsidilith / Ender Guardian. No invented entity or mod |
| Geburah Arena — `fdbosses:geburah_arena` | — | **Explicitly undecided** | Do not fill from Chesed/Malkuth. Review boss fight source and mechanics first |

These are **boss-tier design entries**; their underlying structure IDs/places still need current-jar/runtime verification. Tier 9 must be exceptional by abilities, phase depth, and counterplay, not just bigger HP.

## Provisional missing midgame route (pending owner decisions; **not user-approved**)
| Tier | Provisional route | Alternatives | Gate philosophy / implementation note |
|---|---|---|---|
| T0–1 | New-player survival and exploration | Safe ruins, settlements, travel | No boss lock |
| T2 | Early dungeon trial + special equipment | Any two source-verified T2 encounters | Assumed enchanted-diamond and two grade-A combat supports by late T2; no hard build lock |
| T3 | Sky Arena / Ice Arena **site challenge** | WDA/IDAS dangerous sites | Do **not** assume an arena's registered structure has a killable boss |
| T4 | Mine Cells midgame gauntlet + optional Twilight Forest path | Wither *only as an optional candidate* pending user/encounter review; Trial Chamber T4 | Mine Cells early-game loot must remain unchanged; no mandatory rare-cell encounter |
| T5 | **BOMD Lich or Void Blossom** as provisional named milestone | BOMD Gauntlet, an equivalent verified Overworld T5 major encounter | User preference: prioritize accessible Overworld boss options; 2 alternative routes if one boss is rare or gated |
| T6 | **Iron's Dead King** provisional 'major T6' Pinnacle-unlock boss | A **separately verified, comparable T6** named boss, not an exotic rare-only dimension | T6 bosses may award **Artifact**-class special rewards; stronger T6 unlocks **Pinnacle and Ancient** access |
| T6 optional | Eternal Starlight bosses, Aquamirae (Mother of Maze/Cornelia), underground dragons, Cataclysm mini-bosses | Other smaller-dimension bosses once scanned | These deepen the tier but should not force one magic school/dimension |
| T7 | Cataclysm high bosses, F.D. Chesed/Malkuth, Remnant Ossukage/Kotsukage, Ice and Fire Hydra | Multiple branches | Artifact and Heirloom reward access; most bosses can be tackled solo |
| T8 | Five Bosses’ Rise bosses, Umbrakar, Last of Deepslate | No newly invented boss | Esoteric-class boss rewards; optional expert/mastery route |
| T9 | Tyros, Scylla, **open End slot** | None without approval | Final superboss tier; balanced for Heirloom–Esoteric builds |

**Important implementation rule:** A Tier 5–6 *boss gate* is a narrative/account-unlock event; merely walking into a Tier 5–6 structure does not imply unlocking advanced world tiers. No single rare, one-off structure is mandatory.

## World Tier / grade unlock outline
Named AO phases: **Haven → Frontier → Ascent → Summit → Pinnacle**. Use progression **milestone states**, separate from difficulty/location tags and from raw inventory checks.
- Haven: newcomer T0–1 content and baseline world.
- Frontier: reach T2–3 competence via curated encounters or alternate milestone paths.
- Ascent: T3–5 serious dungeons, Nether, dungeon challenges.
- Summit: T5–6 major challenges; no forced specialization.
- Pinnacle: unlocked by a **stronger T6 boss milestone** (Dead King is a provisional primary choice) with a feasible second comparable route. The user intends **Ancient-access progression** on Pinnacle.
- T7–9 are **optional post-Pinnacle mastery**; Pinnacle is not an automatic reward for ordinary T4 exploration.
- Existing Questlog chapter count remains nine main chapters across T0–8 plus optional T9 epilogue, not one chapter per arbitrary World Tier.

If a single boss gate creates a hard RNG or high-ping barrier, replace it with an equivalent choice; **do not** auto-complete the campaign. Roughly **90% tier completion** should suffice; outstanding optional boss hunts remain in the journal.

## Boss authoring acceptance criteria
1. **Identity:** exact source version, entity registry, boss spawn/arena trigger, dimension, structure ID and whether Integrated addon overrides native resources.
2. **Editable envelope:** actual native HP/armor/damage stats, attack-specific damage, healing, resistance, phase HP/damage caps, invulnerable windows, despawn/reset/retreat, loot output, mob ownership and summons.
3. **Solo baseline:** one non-abusive, level-appropriate gear set from each of melee/ranged/magic if supported; punishable attacks, no unavoidable instant kill, finite refill.
4. **Multiplayer:** 2 and 5–7 players; scale only nearby participants, cap stacking with native configs / Dungeon Difficulty / Apotheosis / Brutal Bosses. No artificial online-player-global HP boost.
5. **Restart/wipe:** bosses heal/reset or encounters reset sufficiently to stop 'suicide chip' and re-login exploits without deleting player inventories.
6. **Reward:** quest completion credit for nearby participating players, replay rules, unique trophy vs repeatable generic loot, evidence-backed per-player vs global containers.
7. **Performance:** native effects, AI ticks, projectile counts and arena spawner caps under shaders + dedicated server.

### Known unsettled choices (all remain *PROVISIONAL*)
- Exact T5–T6 mandatory boss names/alternate route; balance after encounter version/JAR audit.
- Geburah boss tier; third T9 End boss.
- Cataclysm legacy tier discrepancy noted above.
- Which of five Bosses’ Rise fights merit intentional multiplayer prestige treatment; no team-only lock by default.
- Details of World Tier account flags, multiplayer unlock sharing and save persistence.

**No executable datapacks or JSON quests are created by this document.** Refer to later implementation branches; do not silently mark this research-only branch as game-tested.

