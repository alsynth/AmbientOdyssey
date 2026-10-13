# Ambient Odyssey — Encounter design, multiplayer scaling and replayability (v0.5 provisional)
**13 Oct 2026 · DESIGN, NO RUNTIME IMPLEMENTATION**

## Principles
- Solo-first design for **5–7 regular multiplayer participants**. Core progression is solo-feasible; only rare intentionally marked prestige fights (at most **1–3 encounters per tier**) may favor a team, never block the main campaign.
- Difficulty tiers are **player expectations / localized encounter rules**, not hard geographic travel walls. Dungeon Difficulty area scaling must not silently stack with native bosses, Apotheosis, Brutal Bosses or integrated addon modifiers.
- Avoid health-sponge endgame; emphasize **telegraphs, target switching, distinct enemies, punish windows, positional danger, mixed ranged/melee/spell combat and a reason to use utility**.
- Retain native thematic arenas and unique loot. High tier should improve actual encounter mechanics where technically feasible, not merely raise HP.
- Bosses and hard scripted mechanics may be **excluded from structure-wide entity scaling** until dedicated tested native parameters are known.

## Provisional encounter palette
| Tier | Player experience | Mob/arena composition | Proof required |
|---|---|---|---|
| 0–1 | Relaxed wonder / preparation | Standard ambient threats, light patrols | Avoid hostile mob spawn in supposed peaceful settlement |
| 2 | Recognizable dungeon | 2–3 types with different jobs; gear diversity without oneshot | Natural early gear support and spawner density |
| 3 | Named complex / Sky and Ice Arena sites | Melee plus a ranged/special unit; hazards with clear counterplay | Sky/Ice Arena structure presence, native trigger, minimal grief |
| 4 | Longer challenge | Multiple rooms, staged waves, limited elites, manageable spawner counts; **Trial Chamber** and Mine Cells | Trial spawner normal vs ominous configuration, vault rewards, midgame boss survivability |
| 5 | Major fortress / Bastion | Defensive garrisons, spaced elites, meaningful treasure guard, fallback route | Bastion Tier 5 but Fortress Tier 4 user decision; block-breaking/escape behavior |
| 6 | Campaign capstone dungeon | Purpose-built boss or stronger curated waves + counters; not a random NBT-spawned overtuned zombie | T6 boss native phases/stats/loot, alternative route, no immutable high-tier requirement |
| 7 | Extreme boss | Distinct phase counters, recovery windows and signature drops | Remnant 2.7.0, Cataclysm specials and F.D. hit-count mechanics |
| 8 | Mastery boss | Several mechanics together but telegraphed; positioning, interruption, endurance | Bosses' Rise separate from Block Factory bosses, Umbrakar reset/loot |
| 9 | Superboss | Bespoke multi-stage mastery; counterplay for melee and non-melee | Tyros, Scylla and reserved unselected End boss, performance under players |

## Optional 5–7 player scaling trial (formulas intentionally not live)
Only count **distinct participants actually in the arena**, not every online player. Count players nearby during a short encounter window, then stabilize the count to avoid logout/login HP manipulation.

For an eligible **tested encounter only**, first candidate (not a config instruction):
- Boss health multiplier: `1 + 0.35 × min(max(participants−1,0),4)` (2.4× cap at 5+).
- Direct boss attack damage multiplier: `1 + 0.08 × min(max(participants−1,0),4)` (1.32× cap).
- Support mobs/wave count multiplier: `1 + 0.20 × min(max(participants−1,0),3)` (1.6× cap).
- **Never multiply by all three on top of native player scaling**. Prefer changing just one or two of the knobs based on per-boss telemetry and avoid producing more total projectiles than the server can handle.
- If a boss's real threat comes from hardcoded special attacks, attribute changes may only alter idle attack, not actual damage. Such encounter stays **exempt** until tested.
- If party-size scaling creates worse solo experiences or deaths on logout, disable it and rely on capped mechanics/arena density first.

**Why these values:** a tentative 5-player cap gives roughly 2.4× HP, substantially less than five independent solos; damage remains telegraphed and mostly positional. They are **starting hypotheses**, not game-balanced conclusions.

## Wipe, reset and farm design
| Encounter kind | On wipe / distance | Repeat reward | Exploit guard |
|---|---|---|---|
| Ordinary spawner dungeon | Spawn reset/native logic; normal looted chests remain Lootr-per-player | Basic materials / occasional native mob drops | Limit affix and high-grade gem drops from easily repeatable mob spawners |
| Trial Chamber / vault | Respect actual native reset and normal/ominous mechanics | Native cooldown as supported | No manufactured 'always fresh vault' loophole |
| T5–6 named boss | Heal/reset or despawn/re-summon under documented rules | Normal native unique loot and bounded consumable materials | Record individual first-clear token; no unlimited extra World Tier unlocks |
| T7–8 elite boss | Reset phases and boss health between attempts; preserve fair traversal | Some repeatable crafting mats, **limited** high-grade gem rewards | No AFK spawn-kill, duping or portable arena exploit |
| T9 superboss | Preserve dramatic repeat fight and trophy; no forced rare RNG lock | Cosmetics/rare mats after first reward | Can't produce infinite account-bound permanent upgrades by spamming quest completion |

Optional research candidates **Boss Ultimatum** (wipe reset) and one of **Multiplayer Bosses** / **Multiplayer Boss Attribute Modifier** are *alternatives requiring exact-version compatibility*, **not** installed on this design branch. Don't add overlapping scalers blindly.

## Gear-specific fairness and support checks
- Fight test sets: shield/close-range, bow/mobility, Iron's spells, Ars and optionally specialized relic/Curios; no Origin or cursed-ring dependency.
- Audit whether status effects (withering, magic, fire, elemental, % HP) bypass armor expected from the gear atlas.
- After armor/damage buffs, verify close-range windows are actually accessible; 'can defeat with infinite arrow cheese' is not a satisfying Tier 7 boss.
- Target **at most two simultaneous unavoidable threats**, no unavoidable instant deaths on normal gear and max 1–2 punishing learnable errors per attempt, subject to tier tests. These are design targets, not measured tuning.
- For participants, XP/quest credits/rewards should reflect meaningful contribution and not merely the last hit. If Questlog can't do this directly, use validated owner-authored advancement/event hooks and persist per UUID.

## Repeatable content / endgame options
- **First-clear journal dossiers** for each named boss family; not world-first leaderboards and not all mandatory.
- **Arena rematches** that consume a fair, renewable but not trivial summoning resource if the boss supports it.
- **Crafting material loops** across multiple T6–8 bosses rather than one best-in-slot drop farm, with thematic unique loot preserved.
- **Weekly/daily events are not required**; no scheduled world events. Repeatability must work in an always-running private server.
- **Optional mastery achievements**: no-death or equipment-restriction modes *only if real telemetry supports detection*, no cheats/command pseudo-verification.
- **Cosmetic prestige** (trophies, banners, titles, particles) over unchecked permanent stats after T9.
- Endgame is designed for **players joining late**; no first-server-group-only progression rewards.

## Minimum test matrix
| Check | Solo | 2 players | 5–7 players |
|---|---|---|---|
| New encounter spawn, arena worldgen and exit | Yes | Yes | Yes |
| Effective boss HP, special attack damage, armor caps | Yes | Yes | Yes |
| Native phase behavior, wipe and reentry | Yes | Yes | Yes |
| Quest credit, first-clear reward, Lootr and reboot | Yes | Yes | Yes |
| CPU/MSPT, AI/projectiles, shader-client FPS | Baseline | Sample | Required |
| Repeated kill/drop/dupe attempts | Yes | Yes | Sample |

## Technical pending
- Exact mod/structure/entity registry mapping from current **v0484 r19 / newer** binaries, including disabled/deleted content and integrated addon precedence.
- Gear readiness telemetry before any live damage/HP multipliers.
- Manual boss editability datapack coverage: not every mod tested; binary-level evidence and native config fields are separate from live tests.
- Scarcity and distribution of boss summons; Lootr per-player vs native boss corpse drops.
- Player-count freeze window and anti-cheese scheme.
- Original free exploration and existing portal routing must not regress.

**Nothing in this document is a claim of functional mod config or plugin capability.**
