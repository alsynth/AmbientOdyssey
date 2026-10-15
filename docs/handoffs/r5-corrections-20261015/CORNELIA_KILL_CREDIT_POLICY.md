# Cornelia Pinnacle credit: who counts as the killer

**Owner rule (15 Oct):** progression credit goes only to the player credited with the kill. No proximity or party credit. Loot-drop ownership is a separate question and isn't changed here.

**Status:** Approved: the rule above. Implemented: the gate on `feature/pinnacle-cornelia` already uses vanilla kill credit, and no change was made now. Statically verified: yes (bytecode of Minecraft 1.21.1 `LivingEntity` and Aquamirae 7.2.10 `CaptainCorneliaBoss`). In-game tested: no. Multiplayer tested: no.

## How the criterion awards credit (verified from bytecode)
The Pinnacle criterion is `minecraft:player_killed_entity` with only `entity: aquamirae:captain_cornelia` and **no `killing_blow` condition**.

1. When Cornelia dies, `LivingEntity.die` calls `getKillCredit()`, then `awardKillScore()` on that entity. For a `ServerPlayer` this fires `player_killed_entity`.
2. `getKillCredit()` returns `lastHurtByPlayer`, otherwise `lastHurtByMob`, otherwise nothing.
3. `hurt()` sets `lastHurtByPlayer` when the damage source's **causing entity** (`DamageSource.getEntity()`) is a Player, or is a **tamed Wolf** (the owner is used). Each time it's set, a **100-tick (5 s) timer** starts. `baseTick` clears it when the timer runs out.
4. So credit goes to **the last player who damaged her within the 5 s before death**, not necessarily whoever landed the final blow.

## Cornelia's own damage filter (Aquamirae)
`CaptainCorneliaBoss.hurt` returns `false` (no damage, so no credit update) for:
- direct arrows (`AbstractArrow`);
- these damage types: fall, cactus, drown, lightning, explosion, trident.

Everything else goes to normal `Monster.hurt`.

## Attribution by case

| Case | Who gets credit | Basis |
|---|---|---|
| Melee, spells or mod projectiles whose damage source names the player | that player, if they hit last within 5 s | vanilla rule 3–4 |
| Bow or crossbow arrows, thrown tridents | nobody from that hit (she ignores it) | Cornelia filter |
| Explosions (TNT, creepers, explosive spells using the explosion type) | nobody from that hit | Cornelia filter |
| Tamed wolf | the wolf's owner | vanilla, wolves only |
| Other pets or tamed mobs (non-Wolf) | **nobody**, unless the mod sets the owner as the damage source's entity | vanilla checks only `Wolf`; needs a per-mod test |
| Mod summons (e.g. Iron's Spellbooks summons) | depends on the summon's damage source; **unverified** | needs an engine test |
| Environmental death (lava, fire, void, `/kill`) shortly after a player hit | the last player who hit her, **if within 5 s** | `lastHurtByPlayer` still set |
| Environmental death more than 5 s after the last player hit | nobody | timer cleared |
| Two players fighting together | only the player who hit most recently | rule 4 |

## Proposed deterministic policy (no eligibility change)
1. **Keep vanilla kill credit as the single source of truth.** Credit = `getKillCredit()` at death = the last player to damage Cornelia within 100 ticks, including via a tamed wolf.
2. **No AO code** adds credit for proximity, party, assists or damage share. This matches the owner rule.
3. Pets and summons count **only** if the mod puts the owning player in the damage source (vanilla behaviour). AO doesn't add extra owner lookups, so results stay mod-defined and repeatable.
4. Environmental kills count only through the 5 s vanilla window. AO doesn't extend it.
5. **Document it for players** in the quest or tooltip text: "Pinnacle credit goes to the player who last damaged Captain Cornelia (within 5 seconds of her death). Arrows and explosions don't damage her."

## Tests needed
- Two players: player A hits last vs player B hits last.
- Wolf kill.
- One Iron's summon kill.
- Lava death 3 s and 8 s after the last hit.
- Check that loot drops still follow the mod's own rules.
