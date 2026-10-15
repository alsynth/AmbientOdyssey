# Ambient Odyssey — Grand Treasure and Tier 2+ incremental loot design
**15 October 2026 | DESIGN / SOURCE VERIFICATION QUEUE | Not deployed or runtime-tested**

## Non-negotiable owner decisions
- Retain original native mod structure/boss loot tables, unique drops, existing Apotheosis chest-affix odds, native gem drops and apex-tier gem crafting. Add **small, narrowly scoped bonus pools**, not hundreds of table replacements.
- Increase **Scrap and Treasure rewards starting T2**. This supersedes the older "T0–T2 entirely unchanged" note, but **early Mine Cells rewards stay native**.
- **Grand Treasure begins T3, with an independent 5% bonus chance PER ELIGIBLE DUNGEON CHEST**, not 5% per structure and not a 5% share of chest archetypes. Preserve Lootr per-player rolls. For N eligible independent chests, P(at least one bonus) = 1 - 0.95^N. Exact per-player server loot context must be tested, not assumed.
- A rolled Grand Treasure **adds** to the existing chest without removing native items. No automatic high-grade Artifact/Heirloom/Esoteric injection from ordinary T3 chests.
- Boss rewards (independent of dungeon chest design): guaranteed genuine affix item + curated Regalia excluding all Enigmatic items and Pasterdream accessories + random **all-Simply-Swords-swords** reward, in addition to native loot. Approved rare affixed-item bonus chances T6 Ancient20% Artifact2%, T7 Ancient25% Artifact8% Heirloom5%, T8 Ancient30% Artifact15% Heirloom8% Esoteric5%. T9 deferred. Separate loot work must not silently conflate these with gem drops.

## Lightweight chest implementation concept — PRELIMINARY
Attach **one supplemental bonus roll** to individually verified eligible structure chest loot contexts (source-specific loot tables / scoped loot modification where possible); do not globally alter shared vanilla chest tables or overwrite named dungeon loot. Evaluate load order and whether any mod currently adds global treasure modifiers. Avoid double-granting a Grand Treasure roll where two loot table paths reach the same inventory. Use original Lootr instancing semantics, and test multiple players' unopened loot independent rolls.

### Compact Grand Treasure reward families (no new source IDs asserted)
| Family | Suggested T3–4 examples | Suggested T5–6 examples | Boundaries |
|---|---|---|---|
| Crafting/upgrade resource bundle | diamonds, emeralds, lapis, gold, enchanting inputs in modest bundles | somewhat larger bundles, selected nether materials if available | avoid gold/diamond inflation and unique progression unlock ingredients |
| Enchanting / progression components | enchanted books via existing valid native loot pools; ordinary enchanting supplies | comparable existing enchanting materials and enhancement components | do not force high rare affixes, ignore unsupported native registered IDs |
| Exploration utilities | basic travel/consumable utilities if in installed vanilla/native tables | stronger situational travel/consumable utilities if source IDs verified | no native-exclusive boss trophies or gated Regalia |
| Curated native themed reward | one valuable item already present in that structure's own normal loot, with slightly better odds | a corresponding source-specific valuable native item | preserve thematic identity; don't move End-specific reward to Overworld without approval |

**Selection is a design proposal, not owner-approved percentages or exact items.** Initially prefer native structures' existing high-value entries, reweight through targeted additive logic, and only use broadly available vanilla items as a fallback. Define a small per-tier family table (e.g. T3–4 and T5–6) rather than 497 structure-specific mega-tables. The 5% event should be *meaningful*; avoid rewards that are weaker than ordinary chest contents.

### Tier 2+ Scrap and Treasure enhancement — PRELIMINARY
- Scrap: small increases to native recoverable metals, arrows/string/leather, redstone/lapis and other non-gating supplies where that context makes sense. No guaranteed rare gear or boss crafting token.
- Treasure: small increases to existing valuable native loot entries and appropriate enhancement/crafting materials; buff selected existing treasure sources rather than adding generic diamond blocks to every chest.
- T2: restrained enhancement; T3–4: more recognizable Treasure reward chances; T5–6: better quality but not guaranteed rarity/gear skip.
- Do **not** increase the number of chest block entities or rewrite world generation to achieve this; target loot contents only.

## Required audit before executable implementation
1. Inventory real installed/current full-pack JARs, Paxi datapacks, Lootr conversion config and all relevant loot modifiers; map structure IDs, chest templates, loot table resource paths and source mod owners.
2. Sample a cross-section: T2 cave, T3 dungeon, T4 temple/Trial Chamber, T5 fortress, T6 Foundry and owner-approved larger dungeon; identify whether each chest is native/ordinary shared, Lootr, fixed NBT, or a unique reward chest.
3. Produce a 20–30 row **candidate chest-source mapping** with structure, dimension, chest table ID, native content, eligibility, source proof, whether bonus is independently per-player, collision risk and rollback path. No guessed structure IDs or hidden global injections.
4. Implement **only** after source maps are verified; prefer targeted additive NeoForge loot modifier if correct for this version, or a narrowly scoped datapack path preserving entire base table with audit/test. Never claim a recipe or reward ID exists until verified in installed resources.
5. Smoke test (disposable world + non-operator two-player): 100+ eligible chest rolls across tiers, Grand Treasure roll incidence ~5% per eligible roll in expectation (sample noise normal); native loot preserved; no duplicate modifier, repeat/open and relog cannot farm the bonus; Lootr genuinely individualized.
6. Acceptance: no early high-grade affix drops; no change to native Apotheosis chest affix odds, Mine Cells early loot, gem crafting/drops, dimension rewards or unselected Regalia acquisition. Record final source hashes, exact patch diff and rollback.

## Explicit design questions requiring owner choice after native loot samples
- What counts as an eligible chest: all dungeon loot-table chests, or only genuinely meaningful dungeon reward chests? Default: all verified dungeon loot-table chests, excluding decor barrels, village loot and fixed guaranteed trophy chests.
- Should Grand Treasure be a bonus **bundle** or exactly one special item? Proposed default: one compact themed bundle (1 focal reward + a few minor materials) to justify the rare proc.
- Should higher tiers retain 5% or scale upward? Owner explicitly approved **5% from T3**, but has not said to raise it later. Default keep 5% at all T3+ until changed.
- Are T7+ structure chest additions even in scope? DD currently only T2–T6 Overworld; leave T7+ individual boss arenas separate.
