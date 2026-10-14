# Dungeon Difficulty v4 stronger pilot (14 Oct 2026)

EXPERIMENTAL / NOT LIVE / NOT RUNTIME-TESTED. Based on PR45 v3 candidate (experimental/structure-difficulty-v3-20261013); does not replace installed config or modify rollback.

| Tier | Health base bonus | Attack base bonus | Armor addition |
|---|---:|---:|---:|
| T2 | +100% | +40% | +3 |
| T3 | +150% | +60% | +5 |
| T4 | +200% | +80% | +8 |
| T5 | +250% | +100% | +11 |
| T6 | +300% | +200% | +15 |

Retains 27 Tier2-6 combat zone rules with unchanged structure matches, dimension matches, level=1, vanilla-hostile matcher and disabled spawner/experience/loot multipliers. Removes 26 mappings: old Tier0-1 no-op zones and Mechanical Nest's previously unapproved blanket Tier5 scaling. Mechanical Nest remains boss-focused pending identification of actual boss. Dungeon Crawl stays whole-dungeon Tier3. Keep protected Tier0 sites unchanged; do not add blanket rules for boss entities, Quark or Alex's Mobs incidental entities, slime/creeper mounted Keep Kayra encounter.

**IMPORTANT:** Extra health/attack may double-stack with Apotheosis affix mobs, Brutal Bosses, and native Foundry named buffed mobs. Verify effective stats in test world; cap/exclude if necessary before deployment. Attack attribute does not necessarily govern ranged, magical, explosive or custom damage. DD may buff spawned mobs but is not a generic rewrite of spawner block NBT or worldgen placement. No runtime validation here.

Remaining acceptance: JSON parse with installed DD 3.9.2, exact rule matching, startup, T2/T3/T5/T6 ordinary mobs, Foundry native named mobs, an Apotheosis/Brutal elite, performance, rollback and multiplayer. Test candidate only.

## Owner rationale and tip recommendation

Design intent: prevent Apotheosis progression from trivializing later dungeons, and make high-tier Brutal Bosses potentially demanding group encounters. These are untested additive-to-base DD attribute modifiers, not promised final HP or damage values. Keep elite-stack and boss health cap tests open; do not silently nerf the approved table without gameplay evidence.

**Proposed tips-and-tricks loading screen / questbook copy:** "Tier 4+ dungeons are dangerous. We recommend exploring them with at least two players—especially when a Brutal Boss is present."

The wording is a gameplay recommendation, not a hard multiplayer requirement. Tips are documented here only; actual in-game tip resource integration is still pending.
