# Dungeon Difficulty v4 stronger pilot (14 Oct 2026)

EXPERIMENTAL / NOT LIVE / NOT RUNTIME-TESTED. Based on PR45 v3 candidate (experimental/structure-difficulty-v3-20261013); does not replace installed config or modify rollback.

| Tier | Health base bonus | Attack base bonus | Armor addition |
|---|---:|---:|---:|
| T2 | +20% | +10% | +1 |
| T3 | +40% | +15% | +2 |
| T4 | +70% | +25% | +3 |
| T5 | +100% | +35% | +4 |
| T6 | +150% | +50% | +6 |

Retains 27 Tier2-6 combat zone rules with unchanged structure matches, dimension matches, level=1, vanilla-hostile matcher and disabled spawner/experience/loot multipliers. Removes 26 mappings: old Tier0-1 no-op zones and Mechanical Nest's previously unapproved blanket Tier5 scaling. Mechanical Nest remains boss-focused pending identification of actual boss. Dungeon Crawl stays whole-dungeon Tier3. Keep protected Tier0 sites unchanged; do not add blanket rules for boss entities, Quark or Alex's Mobs incidental entities, slime/creeper mounted Keep Kayra encounter.

**IMPORTANT:** Extra health/attack may double-stack with Apotheosis affix mobs, Brutal Bosses, and native Foundry named buffed mobs. Verify effective stats in test world; cap/exclude if necessary before deployment. Attack attribute does not necessarily govern ranged, magical, explosive or custom damage. DD may buff spawned mobs but is not a generic rewrite of spawner block NBT or worldgen placement. No runtime validation here.

Remaining acceptance: JSON parse with installed DD 3.9.2, exact rule matching, startup, T2/T3/T5/T6 ordinary mobs, Foundry native named mobs, an Apotheosis/Brutal elite, performance, rollback and multiplayer. Test candidate only.
