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

## Regalia access and Enigmatic Legacy craftability — owner update (15 Oct 2026)

**Supersedes narrow C0–C1 early boss reward bands.** The boss guaranteed Regalia pool should be **much broader**, with roughly **90% of eligible Regalia items accessible at/before boss Tier 5** (i.e. below Tier 6). Only the genuinely exceptional, progression-breaking *combat* cases should be reserved for T6+; high utility alone does not require high gating. The 90% is a design target **after** verification/curation, NOT an assertion that 447 of the 497 catalogue rows already have verified IDs, effects, or suitability. The catalogue has 497 candidates, of which 421 have unknown combat classification; some are ordinary gear rather than discrete Regalia. Do not transform an unscored entry into a safe low-tier drop without checking.

**Enigmatic Legacy / Enigmatic Legacy Plus:** audit all included Regalia item recipes in the exact installed version, including crafting transformations and any conditional recipe/cursed access, using actual recipe JSON/registered recipe data. **Heavily reduce weight in the NEW guaranteed boss Regalia roll for items that players can craft**, rather than changing their native crafting or blindly modifying unrelated native loot. A starting design candidate is a 90% weight reduction (0.1x relative to otherwise comparable noncraftables) for confirmed craftable entries, subject to review; owner said 'heavily decrease' and has NOT approved an exact multiplier. If any of those items already drop from native pools, report native frequencies separately before changing those distributions. If uniquely powerful but craftable, still consider exceptional combat gating; craftability alone must not force unsafe early availability.

The catalogue on `research/regalia-combat-ranking-20261013` lists **123 entries labelled Enigmatic Legacy Plus**; their acquisition-evidence fields often explicitly say 'Unknown — inspect installed recipes...' and are **not proof of craftability**. Confirm each item with the current installed JAR; group color variants/upgrade chain members carefully. Preserve the owner's prior decision that Regalia native acquisition is generally unchanged, except targeted, reviewed craftable-item boss-reward weighting.

Suggested lightweight implementation: one weighted and tier-tagged Regalia reward provider, with source-specific rarity weight multipliers and a short exceptional-combat blocklist; no hundreds of overwritten mod chest tables, and no guaranteed native boss-exclusive trophies copied into unrelated low-tier bosses. Preserve boss-specific signature drops and ability to farm duplicates. Confirm actual item IDs, enchant or curio requirements, and compatibility with NeoForge 1.21.1 prior to packaging.

## Superseding Enigmatic exclusion and C3 review result (15 Oct 2026)

All **Enigmatic Legacy and Enigmatic Legacy Plus** items are **native-only**: exclude them categorically from AO's *additional guaranteed boss Regalia reward* at all tiers, **regardless of whether they are craftable**, and preserve native recipes, loot, crafting and acquisition exactly. This **supersedes the earlier plan to inspect craftability in order to heavily downweight craftable Enigmatic items** for the new Regalia reward: do not downweight or edit native Enigmatic drops. A previously proposed T6–T7 bonus-pool placement for The Infinitum is canceled. Do not conflate the independently approved starter Bonus Chest Spellstone onboarding feature with the guaranteed boss-Regalia roll.

Non-Enigmatic items approved in the first C3 batch: Evasion Cloak, Counter Ring, Ghost Face Head all T2–T5 as provisional new boss-Regalia pool entries; native acquisition unchanged. See `docs/handoffs/REGALIA_OWNER_REVIEW_QUEUE_20261015.md` for full C4/C3 decisions. No executable loot tables edited.

## Additional owner loot direction — newest overrides (15 Oct 2026)
- Exclude **Pasterdream/NeoPasterDream accessories** from the guaranteed supplemental boss Regalia roll; they stay native-only. Overrides prior provisional early inclusion of Cecilia's Blessing, Turnback Cloak, Counter Ring, Ghost Face Head and Evasion Cloak. Keep native acquisition untouched.
- Do not spend effort on restrictive per-item Eternal Starlight classification; owner says those items are not a major concern. Preserve native sources, use verified entries in broad rewards where eligible.
- Every eligible boss additionally gets **one random Simply Swords sword from the entire installed sword pool**, separately from (1) its guaranteed Apotheosis-affixed item and (2) its guaranteed Regalia reward; independent of preserved native loot. Include all sword variants and uniques with registered item IDs; no arbitrary exclusion based solely on strength. Verify what the installed mod actually classifies as swords. Roll semantics/weights remain implementation details pending verification; uniform random across registered swords is the initial assumption, not an approved numerical distribution.
- Do not let the broad Simply Swords pool accidentally re-add excluded Pasterdream or Enigmatic items to Regalia; maintain three distinct reward mechanisms. No executable modifications in this document.
