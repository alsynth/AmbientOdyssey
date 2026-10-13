# Ambient Odyssey — v0.5 RPG / Boss / Loot / Campaign design package
**13 October 2026** · Branch: `research/rpg-boss-loot-campaign-design-20261013` · **Research/design-only** (no playable build, no new mod, no Questlog JSON deployed)

## Read first / source hierarchy
1. `AGENTS.md`, `docs/status/AGENT_WORKFLOW.md`, `docs/status/CURRENT_STATE.md` and the **current** consolidated r19+ release source, rather than stale `main`.
2. `docs/balance/README_STRUCTURE_MAPPING_V3_2026-10-13.md` and `AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv` (v3.1 user mapping corrections; branch inherited from mapping research).
3. This package. It adds proposals and Work-mode implementation slices **without modifying gameplay**.
4. `docs/questing/QUEST_CAMPAIGN_ARCHITECTURE.md` and the current actual quest index (older introduction is dated and does not describe the latest deployed 52 quests).

## Package files
| Path | Purpose | Status |
|---|---|---|
| [Boss tiers/gates](V050_BOSS_ROSTER_AND_GATES_PROVISIONAL.md) | T0–T9 roster and named T5–T6 options | Preserves known decisions; new routes provisional |
| [Boss CSV](V050_BOSS_ROSTER_PROVISIONAL.csv) | **38** structured boss/family/placeholder records | No invented entity IDs; boss/structure distinction |
| [Loot and gear](V050_LOOT_GEAR_ECONOMY_PROVISIONAL.md) | Five chest classes, gem/rank unlocks, tentative chest archetype allocation, player gear readiness | Design only; no live drop chances |
| [Quest campaign](../questing/V050_QUEST_CAMPAIGN_BLUEPRINT_PROVISIONAL.md) | Nine main Questlog chapters + optional T9 epilogue | Preserve live Questlog/FTB source |
| [Quest beat CSV](../questing/V050_QUEST_BEATS_PROVISIONAL.csv) | **101** authoring beats (97 main, 4 epilogue) | Candidate triggers and fallback text, not engine quest IDs |
| [Multiplayer & replayability](V050_ENCOUNTER_MULTIPLAYER_REPLAYABILITY_PROVISIONAL.md) | Solo-first encounters, performance-safe 5–7-person scaling hypotheses, anti-dupe/retries | Formula prototypes **not** applied |
| [Owner decision register](V050_OWNER_DECISION_REGISTER.csv) | **22** issues with provisional defaults and explicit approvals | Owner can review later; don't interrupt technical progress |
| [Implementation handoff](V050_IMPLEMENTATION_HANDOFF.md) | Ordered small experimental implementation slices and test gates | Intended for Work mode |

## Binding user decisions kept
- Latest structure map **427 entries**, **386 named candidate IDs**, **41 archived/reference rows** (not all verified active).
- WDA Aviary T6 End; Bastion T5; Nether Fortress T4; Keep Kayra T6; Twilight Forest Hydra Lair T4; Sky Arena and Ice Arena T3; Maledictus T7 **at Frosted Prison**, not old fictional Cursed Graveyard.
- Geburah Arena **unassigned**, third T9 End superboss **unselected**.
- Tier 9 **Tyros and Scylla**, Tier 8 **Bosses' Rise 5 encounters / Umbrakar / Last of Deepslate**, Tier 7 notable Cataclysm bosses, Remnant Ossukage/Kotsukage, Qliphoth Chesed/Malkuth and Ice and Fire Hydra.
- **Scylla belongs at Acropolis (`cataclysm:acropolis`)**; **Leviathan** at **Sunken City (`cataclysm:sunken_city`)**. This corrects an erroneous earlier provisional place mapping. Confirm against installed version and Integrated Cataclysm precedence.
- **Remnant Bosses 2.7.0** update intended, GitHub issue #43; not asserted already installed.
- Loot: Scrap / Supply / Equipment / Treasure / Grand Treasure; T0–2 mostly unchanged; early Mine Cells loot unchanged; Tier 6 boss Artifact, strong Tier 6 unlock Pinnacle + Ancient, Tier 7 Artifact/Heirloom, Tier 8 Esoteric; Tier 9 Heirloom–Esoteric power level.
- Final mastery quest must **upgrade held item to Heirloom**, not an exploitable new /give item, if safe engine capability is established.
- Main questline compact and accessible, optional modded realm campaigns, FTB is educational field manual. **No Origins gameplay, backend, races, or Origins-based classes/quests**; no mandatory cursed ring, guild, museum, world-first leaderboard, scheduled events, MCA Reborn or Big Globe; no unnecessary new ocean-loot redesign.
- Roughly 90% tier content completion is sufficient rather than every optional boss.

## Removed gameplay system — binding decision
- **Origins is excluded entirely** from Ambient Odyssey. No Origins selection screen, Origins/NeoOrigins/Pehkui-for-Origins addons, race powers, Origin questline or Origins-dependent balance. Keep classless, gear/spell/build-based specialization where supported by other already-installed mods. See `V050_ORIGINS_EXCLUSION_20261013.md`.

## Provisional owner decisions (not final)
1. T5 accessible main route using BOMD Lich or Void Blossom.
2. Strong Tier 6 Pinnacle primary Dead King **plus a second verified comparable boss**.
3. Trial class distribution and mixed gear/drop rarity rules.
4. Nearby-party size scaling formula and rewards/first-clear accounting.
5. Geburah potential Tier 7 pending owner review; **actual canonical catalogue still null**.
6. Third T9 End boss remains *open* rather than automatically chosen.
7. Latest Ignis/Leviathan tier plan indicates T7; older notes considered T8 — document discrepancy, no stealth 'fix'.

## Why no executable content here
Work mode is already working on structure edits, Dungeon Difficulty and mod-specific mechanics. Writing unverified quest JSON, boss config or Paxi files on a separate branch would create merge conflicts and risk broken gameplay. This package gives Work a **fully structured design source and a first executable implementation queue**, while preserving the playable rollback.

**Next action for Work mode:** read [implementation handoff](V050_IMPLEMENTATION_HANDOFF.md), reconcile v0484+ exact mod JARs and active quests, then build an isolated T5–T6 milestone + one T3/T5 loot prototype without claiming runtime success.

**Validation state:** documents/CSV authored; no Minecraft runtime, ZIP build, shader benchmark or package regression claimed.
