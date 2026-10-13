# Ambient Odyssey — Quest campaign narrative and milestone blueprint (v0.5 provisional)
**13 Oct 2026 · DESIGNED only; no Questlog JSON, FTB pages, quest triggers, rewards or new art deployed.**

## Existing implementation and source-of-truth
- Existing live development **v0484 r19** already has **52 Questlog quests / 13 chapters and 32 FTB Manual pages** (read `AGENTS.md` and latest tested import before editing). Earlier `QUEST_CAMPAIGN_ARCHITECTURE.md` contains a **planning v0.1** banner claiming no production quests; that particular banner is obsolete.
- Preserve stable IDs, current chapter assets, user GUI decisions, per-player persistence, previously tested Q/E integration, FTB manuals and the original WDA questline. Do **not** overwrite actual quest files from this design branch.
- **Questlog = story/adventure/milestones/rewards**; **FTB Quests = educational/reference manual**. No duplicated completion rewards.
- Existing nine main storyline chapters and many **opt-in** mod campaigns; do not force every dimension, cursed ring, boss, biome, wildlife kill or rare structure. **Do not write Origins selection, power, species, background or class-layer quests: Origins is excluded from AO.**.
- Resist RNG hostage progression: main chapter permits alternative equivalent T5–6 boss routes; rare structures are optional field notes. The server is intended for **5–7**, but most encounters must remain reasonably soloable.
- No rejected meta-systems: no exploration museum, Lost Expedition Stories, Party Expedition Planner, world-first leaderboards, mandatory guilds or scheduled world events.

## Progression language
**Haven → Frontier → Ascent → Summit → Pinnacle** represents world/gear unlock stages, **not** a hard law forbidding visiting interesting locations. Separately define encounter tier T0–T9.

| Main chapter | AO tier | Provisional planned quest total | Narrative turning point | Required state |
|---|---:|---:|---|---|
| 1. **The First Pages** | T0 | 12 | You learn how to read the world and survive | Inventory/map/JEI/Questlog competence |
| 2. **The Open Road** | T1 | 11 | Expedition preparedness and non-grindy discoveries | Location + mobility |
| 3. **Trial by Steel** | T2 | 12 | First significant fight; enchanted diamond and combat supports | Equivalent curated T2 completion |
| 4. **The Wider World** | T3 | 12 | First deliberate specialization; an arena or memorable dungeon | Choice of combat style |
| 5. **The Threshold** | T4 | 10 | Nether, stronghold and midgame trials become feasible | One qualifying T4 milestone |
| 6. **Old Powers** | T5 | 12 | Large dungeons, new realms and significant named threats | One qualifying T5 boss/encounter from alternatives |
| 7. **The Legendary Hunt** | T6 | 11 | Fight for Pinnacle access and Artifact rewards | Stronger T6 boss milestone with one equivalent alternate |
| 8. **The Breaking Point** | T7 | 9 | Defeat an extreme but fair boss and master high-grade gear | Pinnacle plus elective T7 achievement |
| 9. **Beyond the Known** | T8 | 8 | Mastery gauntlets and epilogue preparation | Optional T8 accomplishment |
| **The Final Horizon (epilogue)** | T9 | 4 | Tyros / Scylla / future End super-encounter | **Optional**, needs verified registry and deliberate rewards |

**Target: 97 main story beats**, plus 4 optional T9 epilogue beats. Totals are editorial targets, not evidence of actual published objectives. `V050_QUEST_BEATS_PROVISIONAL.csv` contains detailed authoring anchors and **does not** replace the existing v0.4 Questlog content.

## Chapter authoring and reward rules
**Chapter 1 — First Pages:** tutorial for map, JEI, per-player Lootr and Curios/backpack; one safe small reward. Never send a new player on a deadly first-night trek to see a menu. If read-open triggers don't exist, provide a safe confirm/read objective using Questlog-supported behavior.

**Chapter 2 — Open Road:** find one of several distinct landmark types, prepare a trail kit, first field-note collectible (only if valid ID), discover Waystone/map. Unique structures should be a *choice*, not a mandatory rare spawn.

**Chapter 3 — Trial by Steel:** prepare enchanted diamond and ≥2 grade-A combat supports; finish one verified Tier 2 dungeon or alternate encounter. Don't have server blindly check armor enchant NBT until predicate support is proven; use a recorded milestone/advancement or explicitly manual confirmation for unmeasurable gear state.

**Chapter 4 — Wider World:** player experiments with melee, bows, Iron's spells, Ars, or other owned system. T3 **Sky Arena or Ice Arena** is a valid optional site milestone, not automatically an entity-kill objective. Reward a modest upgrade/trophy token rather than one mandatory spell item.

**Chapter 5 — Threshold:** one T4 challenge (Trial Chamber, a Mine Cells milestone, or equivalent curated location), Nether access and Tier 4 survival challenge. **Mine Cells early loot unchanged.** End Remastered requires **12 of 16 eyes** if effective AO config confirms; do not require all 16.

**Chapter 6 — Old Powers:** optional trials with WDA, large IDAS, Nether Bastion T5 (fortress T4) and one of the **provisional BOMD T5** fights. A Tier 5 mainline route must not depend on one inaccessible/rare structure or an addon with unsolved source ID.

**Chapter 7 — Legendary Hunt:** build a T6-capable loadout and defeat a **stronger Tier 6** boss. **Iron's Dead King** is a provisional primary, with a comparable verified alternate that Work mode must identify. Unlock Pinnacle/Ancient world access as a **tracked player milestone** only after encounter verification; one boss fight can yield the first **Artifact**-class special reward subject to tested item support.

**Chapter 8 — Breaking Point:** choose from T7 boss paths (e.g., Maledictus at `cataclysm:frosted_prison`, Ignis, Leviathan, Ossukage/Kotsukage, Chesed/Malkuth). Guild/group not required. Optional curse mode stays opt-in. First-clear rewards offer a Heirloom pathway without making every optional boss mandatory.

**Chapter 9 — Beyond the Known:** T8 mastery through selected Bosses' Rise fights, Umbrakar or Last of Deepslate, subject to updated JARs. Don't assume Bosses' Rise is Block Factory's Bosses. Esoteric boss rewards and side objectives. The owner selected Tier 9 Tyros/Scylla **after** older research; preserve newer setting.

**Epilogue — Final Horizon:** Tyros/Scylla T9 challenge + a reserved End boss slot (undecided). The **final mastery quest must upgrade an already held item to Heirloom** using a validated transfer/upgrade implementation; do not fake an item mutation with `/give` duplication. First investigate port item and gem semantics, consumption, component preservation and anti-dupe transaction.

## Optional chapter plan (source-tied, not yet authored)
- **Twilight Path:** complete Twilight Forest normal progression; Naga → Lich → Labyrinth → Hydra Lair **structure T4** and later castles, as actual JAR supports. Do not conflate Ice and Fire Hydra.
- **Kingdoms of the Sky:** Aether and Deep Aether as elective branches; portal, treasure, bosses; no mandatory Aether completion for every player.
- **Starlit Frontier:** Eternal Starlight travel → Cursed Garden, Golem Forge, Stranghoul Den (structure IDs historical; verify); boss/forge skill path.
- **Dreamseeker’s Notes:** NeoPasterDream 0.9.6 dreams, Garden Decryption and Shadow; distinguish puzzles, trade/field observation from boss fights; don't invent later-version realms.
- **Hunter of Legends:** Cataclysm, BOMD, Remnant 2.7.0, F.D. Bosses, Bosses’ Rise, Archaion and Mowzie's source-specific boss dossiers. Native mechanics, distinctive arena names, unique trophy; not five duplicate fetch quests.
- **Frozen Seas / Dragon Hunter:** Aquamirae and Ice and Fire stories (native thematic loot unchanged); no new independent “ocean loot overhaul” system.
- **Cave Expeditions / Arcane Academy / Spellwright:** Alex's Caves, Ars Nouveau, Iron's Spells; guide discovery then meaningful build experimentation, not craft 500 items.
- **Eyes of the End:** collect any sufficient set of End Remastered eyes (effective rule currently intended 12/16). End access isn't blocked by a single rare special boss.
- **Explorer Atlas & archaeology:** selective meaningful discoveries, maybe one excavation trial if sufficiently rewarding. No museum, no exhaustive structure-tracker always-on polling.
- **Relic Scholar / Seven Curses:** normal route always available; cursed ring opt-in and never a required campaign flag.
- **Bumblezone:** Bee Queen **trading NPC**, **not a kill boss**.
- **Skill/build experimentation:** teach optional weapon styles, relic synergies and spell schools already supported by installed mods; no Origins, races, Origin-based classes, selection screen, Origin abilities or mandatory guild.

## Implementation contract for Work mode
1. Reconcile all existing actual 52 Questlog quest IDs / 13 chapters and 32 FTB pages before creating anything. `V050_QUEST_BEATS_PROVISIONAL.csv` names are **human-readable authoring identifiers**, not known engine IDs.
2. Every quest must have explicit `candidate_trigger`, `exact registry requirement`, `fallback`, `reward category`, `validation status`. Never fabricate a boss or recipe ID.
3. Prefer `item_obtain`, `visit_structure`, `visit_dimension`, `entity_kill`, verified advancement, or Questlog-native information step only when capability actually exists.
4. Visiting a structure must be registry-targeted; many variants share one ID. Boss kill may be attributed to only one player: verify nearby contribution/party credit separately.
5. Give meaningful first-clear rewards through a supported once-per-player Questlog path; no duplicate FTB payouts; preserve Lootr and player-specific saves through restart.
6. Avoid expensive always-on polling of hundreds of location quests; only 1–3 active visit tasks per player under default progression.
7. Add narrative flavor and custom descriptive text; new art/icon assets only in an explicitly requested creative asset task, not a substitute for data-backed quests.
8. QA with new player, returning player, one and two accounts, save/restart, dedicated server, mod absent/missing-ID simulations.
9. Keep original quests and WDA rewards intact; no changes to mainline account progress without migration.

**Status:** owner authorized **provisional planning without questions**. Only explicitly user-approved placements are binding; no game code or quest JSON has been changed here.
