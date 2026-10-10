# Ambient Odyssey — Midgame/pre-End flight audit

**Status:** Research shortlist only, **no new flight mod installed** for current worldgen Test8.1. User wants meaningful travel before the End/vanilla Elytra without trivializing early exploration. Test fall-damage handling, Curios, server performance and progression.

## Already installed — try before adding mods

- **Iron's Spells 'n Spellbooks v3.16.3:** **Angel Wings** spell grants temporary spectral *Elytra-like* gliding, not permanent free Creative flight. The mod's in-game guides describe it as “wings made of holy energy, acting as an elytra, for a brief period”; spells such as Ascension can facilitate height. Source: https://github.com/iron431/irons-spells-n-spellbooks/blob/1.21/src/main/resources/assets/irons_spellbooks/lang/en_us.json
- **Ars Nouveau:** Tier-3 **Glide** glyph provides temporary Elytra-style gliding (not unlimited lift) and is mana/progression gated; docs https://ars.guide/1.21.1/docs/spell_theory/glyphs/ . Investigate Launch/Leap as a complementary spell
- **Ice and Fire:** Hippogryph riding (depending on taming/spawn config) is a collectible mount that may already provide appropriate travel progression. Note user's dragon breeding/taming system is late-game and separate
- **Existing exploration mods:** Verify if current pack has craftable temporary elytra or glide artifacts before adding duplicates; prioritize distinctive progression

## Compatible NeoForge 1.21.1 external options

1. **Flight Rings** (CurseForge project **401229**; NeoForge 1.21.1 2.0.0), https://www.curseforge.com/minecraft/mc-mods/flight-rings . **Two rings:** basic creative flight drains hunger heavily (designed for shorter trips); pure ring consumes XP with infinite item durability. **Best bounded midgame travel** if strong costs are tuned further. Check base crafting material; default base ring may still be too accessible
2. **Simple Flight Ring** (MIT, NeoForge 1.21.1), https://modrinth.com/mod/simple-flight-ring . Several tiered limited-duration rings with durability and advanced relic-only rings; offers a clear midgame-endgame gradient; initial wood/stone rings may be too cheap. Compare crafted rings to Iron's existing spellbook balance
3. **Create: Balanced Flight — NeoForge fork** (MC 1.21.1), https://www.curseforge.com/minecraft/mc-mods/create-balanced-flight-fork-neoforge . **Flight Anchor** requires Create kinetic power and enables flight within a radius; **Ascended Flight Ring** expands mobile freedom. **Excellent progression structure** if Create 6.0.10, Curios, GeckoLib dependency requirements match live pack. Need config/radius benchmark and exact file; don't treat as pre-approved
4. **Ring Of Flight** (Minecraft 1.21.1 NeoForge), https://www.curseforge.com/minecraft/mc-mods/ring-of-flight . Curios creative flight item **requires Elytra in final recipe**, so it does NOT solve user's pre-End goal unless an explicit alternative crafting recipe is approved. Deprioritize by default.

## Recommendation and playtest gates

Begin with **existing Iron's Angel Wings, Ars Nouveau Glide and Hippogryph** options, then compare **Flight Rings** (hunger/XP cost) to **Create: Balanced Flight** (stationary midgame flight). Choose one with player effort and resource cost appropriate to **nether/midgame exploration**, not cheap always-on Creative. Avoid disabling structure collision/exploration by making unrestricted flight available immediately. Server flight checks: permissions, anticheat/fly kick, Curios slot, logout/reconnect midair, Nether/lava rescue, falling immunity, mana drain, speed and simultaneous 5–7-player lag. Add questbook explanation if approved.

**Do not insert an unselected flight mod into the current worldgen-freeze candidate**: flight can be added after worldgen freeze because it does not alter terrain or structures.
