# Ambient Odyssey — owner-approved targeted loot direction (15 Oct 2026)

Status: design decision, NOT deployed. This note supersedes any earlier proposal to comprehensively replace existing mod loot tables or alter Apotheosis generic chest affix odds.

## Preserve rather than rewrite
- Keep existing/native structure and boss loot tables as the primary loot source, including thematic uniques, modded materials, and established drop chances.
- Keep current Apotheosis equipment-affix generation in chests intact; user considers it balanced. No arbitrary 20/40/65% Equipment-chest affix injector.
- Prefer small, additive, source-specific rewards and selective buffs to existing pools; do not create enormous duplicated loot tables. Avoid broad shared-table modifications causing incidental rewards in unrelated dungeons.

## Dungeon chest additions
- **Starting at structure Tier 2**, increase availability/value of **Scrap and Treasure** within existing loot sources. Exact adjustment amounts and native table identities remain to be determined from source inspection.
- **Starting at structure Tier 3**, introduce a **5% Grand Treasure chance** in eligible dungeon chest/treasure contexts. The owner has not specified per-chest vs per-dungeon trigger semantics; determine and confirm scope before implementing probabilities. Grand Treasure should come from a small curated supplemental reward set or existing valuable native pools, not a replacement of everything. Preserve per-player Lootr chest behavior.
- Existing documented chest archetype percentages from earlier v0.5 design are not owner-approved drop probabilities. Supersede any old T3 '0% Grand Treasure' assumption: owner now explicitly wants Grand Treasure possible at T3 at 5%. Do not convert archetype mix percentage directly into loot-roll weights.
- No broad Mine Cells early-loot rewrite.

## Boss additions (every kill, including repeat kills, owner agreed)
- Guarantee **one real randomized Apotheosis affixed equipment item** from every eligible Tier 2–9 boss kill, independent of the native loot rolls; exact rarity progression/pools must respect world-tier rules and current installed rarity system. Do not edit existing chest affix generation.
- Guarantee **one tier-appropriate Regalia item** from every eligible Tier 2–9 boss kill, independent of native rewards and the affix-item guarantee.
- Existing unique drops/materials remain available. Regalia reward pools MUST be curated from the existing Regalia catalogues and source-verified available item IDs; exclude unclassified/progression-breaking items and avoid auto-including all 419 candidates. 'Guaranteed' means one per eligible boss kill; multiplayer ownership/per-player eligibility and repeat-farming safeguards still require design and verification.
- Additional rare Ancient/Artifact/Heirloom/Esoteric rewards remain separate from these two guarantees and subject to previous approved higher-tier scarcity rules. Affix item rarity is not gem grade; don't conflate the two.
- Standard boss tiers and exceptions: Chesed/Malkuth/Geburah boss Tier5 exempt stat buffs; Dead King and Captain Cornelia boss Tier6 category even with Tier7 combat treatment; rare loot uses their *category*, not temporary combat stat multiplier.

## Implementation checklist
1. Audit effective table IDs, NBT fixed container loot, actual installed item registries and Global Loot Modifier order before touching tables.
2. Design a small overlay/injection path using existing pools, compatible with Lootr per-player and installed Apotheosis APIs; don't overwrite native tables.
3. Specify Grand Treasure 5% trigger scope (eligible individual chests or a once-per-dungeon reward) separately to avoid accidental multiplication across many chests.
4. Produce curated Regalia tier pools with an explicit owner review; don't auto-assign unclassified catalogue entries.
5. Test repeat kills, multiplayer, first-clear rewards, two real affix/Regalia guarantees, world-tier access and exploit prevention.
6. Keep exact before/after loot diffs, parse/runtime checks and rollback; do not claim a live change without installing it.

## Final Grand Treasure roll semantics (owner confirmation)

**Starting with Tier 3: independently roll a 5% Grand Treasure bonus chance for each eligible dungeon chest**, not a 5% chance per dungeon. Keep the chest's native loot table and add the reward selectively; do not replace base content. An eligible chest is a verified dungeon loot container, not every barrel, storage prop, ordinary village chest, or generic shared table used outside that dungeon. Use Lootr's per-player chest instancing properly; validate whether the roll is per player's instanced loot or world-wide, and ensure no duplicate injection on reopen. Higher-tier odds remain unspecified until the owner approves them. The prior T3 0%-Grand archetype proposal is superseded by this explicit per-chest 5% chance.
