# Task B: T2–T6 Scrap/Treasure, Approach A (additive native rolls)

**Status: Blocked.** Approved: intent only. Implemented: no. Statically verified: the spec search below. In-game tested: no. Multiplayer tested: no.

## 1. Previously selected activation rates: none found
I searched every local and remote branch (all `.md`, `.json`, `.toml`, `.java`). No document selects activation rates for Scrap or Treasure. Every source says the amounts are still open:

- `docs/handoffs/LOOT_OVERHAUL_OWNER_DECISIONS_20261015.md:11` (PR64): "Starting at structure Tier 2, increase availability/value of **Scrap and Treasure** within existing loot sources. **Exact adjustment amounts and native table identities remain to be determined from source inspection.**"
- `docs/handoffs/GRAND_TREASURE_AND_T2_LOOT_PILOT_20261015.md` (`88a69c8`, branch `experimental/master-integration-20261015`): "T2: restrained enhancement; T3–4: more recognizable Treasure reward chances; T5–6: better quality but not guaranteed rarity/gear skip." And: "Produce source-grounded per-structure before/after targets; **exact increase remains unapproved until measured.**"
- `docs/handoffs/CLAUDE_CANONICAL_MASTER_HANDOFF_20261015.md:87`: "**NOT IMPLEMENTED**: exact amounts and source tables not yet approved; do not invent global weights or replace loot tables." Line 111: "T2+ Scrap/Treasure additions lack numeric approval, even though the intent is approved."
- `docs/balance/V050_LOOT_GEAR_ECONOMY_PROVISIONAL.md` (13 Oct) has percentages, but they're **chest-archetype shares**, not rates. T3: Scrap 20% / Treasure 15%; T4: 10/20; T5: 5/25; T6: 0/30; T0–2: "preserve native". The doc says: "This is a design target for chest archetypes, **not a native loot-roll probability** … never blindly turn this table into per-roll weight values." Its T0–2 rule was later superseded by "starting T2".

## 2. Comparison with your earlier targets
Your targets: T2 +20/+10, T3–4 +25/+15, T5–6 +30/+20 (Scrap/Treasure).

- **No recorded rates exist to compare with**, so they can't "agree". They don't appear anywhere in the repo.
- They don't match the V050 shares either. Those measure something different (what share of chests is Scrap vs Treasure) and run the other way: Scrap falls and Treasure rises with tier.
- They do follow the direction of the 15 Oct pilot text (restrained at T2, more at higher tiers).

## 3. Missing values (I haven't invented defaults)
1. **Meaning of "+20%".** Either (a) the chance that one extra native roll fires per chest, or (b) +20% more items from the existing pool. Approach A suggests (a), but it isn't written down.
2. **The rates themselves**, per tier and class, as approved numbers.
3. **Which chests are Scrap or Treasure.** All 15,163 rows in `docs/balance/v3-evidence/LOOT_TABLE_INDEX.csv` are `UNCLASSIFIED; requires reachable-template and economy review`. Without a class there's nothing to attach a Scrap or Treasure rate to.
4. **Which pool is "the" Scrap or Treasure pool** inside a multi-pool native table (the same question Grand answered per table).
5. **Tier per table:** Grand has 14 mapped contexts; T2 and the other T2–T6 Scrap/Treasure contexts aren't mapped.

## 4. Proposed mechanism (not implemented)
- Reuse the Grand pattern (`GrandTreasure.java`): a scoped global loot modifier keyed on a verified table ID, then one extra draw (`rolls=1`) from a named native pool, added after native generation. Native tables are untouched.
- A separate policy section (`scrap_treasure`) in `ao_loot_policy.json`. Every rate starts as `null`, and the code skips any context whose rate is `null`. Reverting means setting the rate to `null` or removing the section.
- Hard guards:
  - tier 2–6 only;
  - an explicit per-table allowlist;
  - no table that holds boss-exclusive or unique items (checked against the R4 unique and Regalia lists);
  - no shared generic tables unless the trigger is scoped to a structure (see the `generic_magic_treasure` finding in the Grand evidence);
  - Grand approvals stay a separate section with no shared flags.
- **Validation plan, reported in two separate columns:**
  - static: hashes, allowlist and policy schema;
  - in-game: at least 100 sampled chest generations per tier, before/after item counts, Lootr per-player instancing.

## Next action (yours)
Give the five missing values (1–5). I'll then produce the 20–30 row candidate mapping the pilot doc requires before any code.
