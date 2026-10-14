# AO Loot Economy — first targeted balance wave (13 October 2026)

Status: Experimental draft, not merged or runtime-tested. Base: PR #50 branch `experimental/pr45-runtime-rpg-acceptance-20261013`. This branch does not modify Work's live structure or Claude's boss branch.

## User-approved policies

- Preserve normal native loot distributions of Simply Swords, Relics, Artifacts, Enigmatic Legacy, and vanilla Lootr individualized chest rolls. Audit *new additions* for unexpected cheap loot injections instead of broadly nerfing existing tables.
- Preserve Apotheosis default affix-generation approach; audit/tune **World Tier unlocks and generation chances** later, not wholesale distribution replacements.
- Goblin-Tuned chainmail helmet/chest/legs/boots: change offer cost to **32 diamonds plus 4 Iron's Spells Cinder Essence** per piece, *only after verifying the item registry ID and matching actual pinned Goblin Traders trade JSON*. Retain full original item data components, modifier, durability and max one trade. No rarity/spawn nerf. Original documented price 1–3 iron + 6–14 emeralds per piece.
- Basic Flight Ring: replace central diamond with one **Nether Star**. Implemented in this draft's source recipe file.
- Advanced Flight Ring: recipe proposal is `ENE / DAD / IRI` where E=Eye of Ender, N=Cinder Essence, D=Netherite Ingot, A=Basic Flight Ring, I=Arcane Ingot, R=Ars Nouveau Air Essence. This shorthand uses center row `DAD`; bottom row `IRI`, *not* the user's old echo-shard recipe. Verify `irons_spellbooks`/Ars resource names from installed JARs. Keep unmodified until verified; the old Nether Star and Echo Shard are removed by the proposed upgrade. Validate all three ingredient IDs and exact loaded recipe priority.
- Rage Glove: remove access from *ordinary early acquisition* once all installed loot sources verified; reserve as rare RNG reward of an existing **Tier 7 Nether boss** after Claude identifies final candidate. No boss or loot change yet.
- Infinitium and Cursed Ring unchanged.
- Simply Swords unique weapons: user interested in +1–2 attack damage if underperforming; benchmark and determine repairability and affix interaction before change.

## Next audit (independent of structures/bosses)
1. **New additions acquisition table**: for each newly added mod since v0.4.8, list powerful materials/items, all crafting/loot/trading sources, initial expected player stage, exploit risk. Do not rewrite old sources absent a concrete bypass.
2. **Cheap high-impact recipes**: flight/teleport accessories; rings; advanced spell components; craftable boss-equivalent weapons and armor. Verify exact registered item IDs, recipe overrides and pack load order. Test viable alternatives, not just paper ingredient rarity.
3. **Apotheosis World Tier configuration**: enumerate tiers, unlock predicates, affix-rarity weights and other mods' overlapping loot injection; propose targeted probability edits after data collection. Ordinary mobs should not grant high-rarity affixed equipment per user decision.
4. **Regalia exceptions**: prioritize Rage Glove, Qym Head spell interactions; leave Infinitium and Cursed Ring. Find actual installed acquisition paths, not just wiki claims.
5. **Data-safe implementation**: only touched trade entries in exact native JSON; no inadvertent stripping of Goblin-Tuned data components. No broad edits to Nether/End shared tables. Preserve Lootr individual rolls.
6. **Test protocol**: structural JSON validity, recipe ingredient registry existence, frozen manifest, data-pack priority, fresh world/dedicated server, unchanged baseline behavior, no quest/boss/structure regressions.

## Decisions awaiting verification
- Exact item IDs and original trade entries for Cinder Essence, Arcane Ingot and Air Essence; no speculative identifiers committed.
- Tier 7 Nether boss for Rage Glove, pending boss work.
- Whether changing Simply Swords unique attack values is necessary based on actual combat tests.

The only game-affecting change committed so far is Basic Flight Ring: diamond → Nether Star.
