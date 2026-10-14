# Owner content exclusions — 14 Oct 2026

**Requested, not yet implemented.** Keep separate from PR56 Dungeon Difficulty catalogue and apply on the next gameplay-config/release integration branch.

| Content | Owner requirement | Target | Required verification | Acceptance |
|---|---|---|---|---|
| Twin Fangs | Remove from generated loot | Relic item loot entries, mod loot injection, chest tables | Confirm exact item ID, owning mod, actual effective loot sources and whether datapack/config supports remove | Item never rolls in ordinary structure/chest/drop loot, including LOOTR and global injection; acquisition outside loot unchanged unless owner specifies |
| Gravitium Striders | Remove from generated loot | Relic item loot entries, mod loot injection, chest tables | Confirm exact item ID, owning mod, actual effective loot sources and whether datapack/config supports remove | Same loot exclusion as above; no broad relic disable |
| Gnat (Opposing Force) | Disable mob spawning | Opposing Force 1.21.1 NeoForge spawning mechanism | Confirm exact entity ID, active version, spawn rules and whether config/datapack/features or scripted spawn path applies | No naturally generated or mod/worldgen-spawned Gnats; ensure other Opposing Force mobs remain enabled |

Web reference at capture: official Opposing Force changelog for 1.21.1 beta4 (Oct 1 2026) specifically added Gnat; the mod documentation notes different mob spawn paths (natural, worldgen, special). **A biome spawn-weight edit alone may not block every mechanism**. Verify actual installed release; do not guess entity ID from display name.

Safety: do not delete the entire relic mod, disable other items/mobs, mutate existing loot pools by blanket rules, or mark complete without in-game test. Investigate compatibility with the team's planned loot rebalance and server pregen. No gameplay config touched in this note.

PR56 mapping progress at time of note: **635/1130 = 56.19%** current-profile provisional tier labels, 495 unranked; 635/1240 = 51.21% all known. Structure tiers with low-looking spawner evidence remain owner-unranked.