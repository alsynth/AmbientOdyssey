# Questbook Reconciliation After AO Content Expansion

**10 Oct 2026 · Process draft, not an installed system.**

## Why this exists

AO's final content roster is still expanding. We can write compelling quest copy now while delaying exact objective bindings until items, mobs, recipes, structure placement and boss tiers are stable. A later expansion must not quietly delete progress, duplicate rewards or introduce impossible objectives.

## Authoring sources to preserve

- MOD_QUEST_COVERAGE_MATRIX.csv — classification of mod and integration sources, not exact current game roster.
- QUEST_CONTENT_SEEDS.csv — broad milestone inventory.
- WRITTEN_QUEST_DRAFTS_V0_2.json — detailed original copy, matching existing stable seed IDs.
- FTB_FIELD_MANUAL_DRAFT_PAGES_V0_2.md — learning pages, separate from adventure rewards.
- VERSION_PINNED_CONTENT_LEADS_2026-10-10.md — source-backed mod-specific research.
- Questlog 3.4.1 config quest JSON and FTB SNBT become outputs **only after implementation/testing**.

## Procedure after each content expansion

1. Freeze the **actual** modpack state: CurseForge manifest/project and file IDs, manually bundled JAR hashes, NeoForge, datapacks, KubeJS/Paxi and a successful client log. Historical audit names are not proof of today's installed mods.
2. Compare mod entries: added, removed, upgraded, reverted, port swapped, integration changed and library-only additions. Record an old-versus-new version for every mod.
3. Compare **gameplay registries** separately: dimensions, biomes, reachable structures, bosses/mobs, items, recipes, advancements, loot pools, progress triggers and player-equipment slots. A registry entry can exist but never generate naturally.
4. Reclassify each changed entry: major optional campaign, smaller questline, cameo, Explorer Journal discovery, FTB educational article, integration, or no quest.
5. Match all existing quest objective targets to real worldgen and obtainability. If an item or structure disappears, define an alternative or retire the quest with a migration; never ship the impossible objective.
6. Refresh the boss-tier and gear readiness information, especially Tier 2's enchanted diamond armor and two concurrently equipable A-grade combat supports.
7. Run editorial review: clear newcomer text, optional content remains optional, no mandatory rare RNG dungeon, no forced Origin, no compelled Seven Curses acceptance and no spoilers for unseen bosses.
8. Check generated quest definitions for unique IDs, valid references, cyclic prerequisites, duplicate/infinite rewards, feasible trigger types and notification spam.
9. Test on a copied two-player dedicated server, including quest discovery, boss credit, multiple Origins, logout/reconnect, death and server restart.
10. Publish migration notes and update the AO wiki data only from verified content. Progress/UUIDs/coordinates must never be shared automatically.

## Content change matrix

| Change | Default quest treatment |
|---|---|
| Brand-new major realm | Independent Questlog chapter: arrival, discovery, equipment, named challenges and ending |
| New distinct boss or dungeon | One or several tier-appropriate optional encounter quests, plus discover-vs-clear tracking |
| New biome and scenery providers | Explorer Journal percentage grouping; narrative entry only where there is distinct gameplay |
| One-off structure pack | Curated representative discoveries; don't require all near-identical random variants |
| New magic/ritual system | Introductory Questlog mastery with deep FTB Field Manual explanation |
| Gear, Relics, weapon mods | Learn unique mechanics, experiment with viable loadouts; verify actual Curios slots |
| New Origin and discipline addons | Character guide, identity-specific optional tasks; never gate main quest |
| Create, food, storage, cosmetics | Usually one optional cameo or FTB explanation, not core RPG progression |
| Library, shader or FPS mod | No standalone quest |
| Boss tier / loot / recipe changes | Update objective targets, danger note and reward policy without rewriting existing player history |
| Disabled structures or removed mods | Retire or replace impossible quests before packaging, preserving claimed rewards |

## Data that must remain stable

- **Published Quest ID:** immutable. Never reuse it for a different accomplishment.
- **Chapter ownership:** prefer stable; migrations permitted with testing.
- **Player progress and claimed rewards:** survive updates; no free duplicate payout.
- **Registry target:** may be re-bound only with explicit version tag and testing.
- **Tier label:** updated from actual AO boss/gear calibration.
- **Visible/hidden state:** avoid revealing dozens of new high-tier quests when an update loads.
- **Optional-route flag:** Seven Curses, optional dimensions, magic schools, noncombat professions remain opt-in.

## Performance and discovery tracking

Questlog's 1.21.1 visit-biome and visit-structure objectives poll roughly every 20 ticks while active, per exact source audit. Do not register hundreds of unfinished location objectives for every player without profiling. Prefer the eventual silent Explorer Journal to own the exhaustive registry checklist and selectively inform Questlog of major discoveries, if a bridge is reliable.

Track **biome type seen**, **structure type discovered**, **specific site visited**, **guardian defeated** and optional **site mastery** separately. Percent denominators must count only reachable enabled content, not every registered template or disabled structure set.

## Audit status labels

draft_copy → id_found → achievable → implemented → offline_checked → server_passed → released.

Each status requires evidence. A documentation page, a quest idea, a compiled JSON and a multiplayer-tested reward are **different deliverables**.

## Highest-value reconciliation subjects

NeoPasterDream 0.9.6 versus later realms/puzzles, Enigmatic Legacy Plus 1.1.2 cursed and standard routes, Origin backend, Aquamirae, major dimension portals and boss progressions, End Remastered eye conditions, and AO structure density/eligibility. After every relevant expansion update their exact-version evidence before authoring actual objectives.

## Things intentionally excluded

No required guild systems, world events, museum/trophy cabinet, scripted Lost Expedition story chains, bespoke party expedition planner, or world-first records.

**Current outcome:** only source documents. No production mod/config/gameplay/quest progress change.
