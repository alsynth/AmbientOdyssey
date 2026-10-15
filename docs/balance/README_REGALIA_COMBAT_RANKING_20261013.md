# Ambient Odyssey — Regalia combat-power ranking v0.1
**13 October 2026 · Design/research only · No gameplay or loot values changed**

## Current source files
- `REGALIA_ITEM_CATALOGUE_EXPANSION_2026-10-13.csv` — **497** item-level candidates from 14 source-mod families. Preserves all prior columns, adds 8 scoring/evidence fields.
- `REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv` — same **497** candidates ordered by provisional **combat** impact first, **not utility power**.
- `REGALIA_JEWELRY_PATTERN_POWER_AUDIT_20261013.csv` — 15 Iron's Jewelry **pattern resources**, not 15 unique item registry entries.
- This document — evidence, rules, and the near-term audit order.

## User policy (binding design intention)
**High utility is welcome early.** Night Vision, mobility, teleportation, grapples, scouting, convenience and even creative flight can be exciting early loot. Don't automatically block those behind Tier 7 because they are useful.

Focus gating on **offensive damage multipliers, unbounded cooldown/cost bypass, defense, automated dodges, lifesteal and death prevention**, especially where Regalia stacks with Apotheosis affixes/gems, spell scaling, additional Curios slots or another Regalia item.

**Ordinary equipment is fine in chests.** Gear becomes exceptional via enchanting, Apotheosis reforging, gems, upgrades and unique effects. Keep normal weapons/armor relatively unrestricted; regulate unusual abilities and *upgrading materials* if they actually cause skips.

**Strong utility is not intrinsically unfair;** a harmless Night Vision charm can be available T1 regardless of Utility 5. Utility-based challenge bypass (creative flight/teleport into locked boss rooms) should be *tested as a structural mechanic*, not automatically cause a global late-game loot ban.

## Ranking scale and caveats
| Score | Offense | Defense | Utility |
|---|---|---|---|
| 0 | No direct listed offense | No direct listed defense | No direct utility documented |
| 1–2 | Small/conditional impact | Minor/conditional protection | Convenience or situational aid |
| 3 | Meaningful combat advantage | Meaningful survivability | Significant traversal/economy help |
| 4 | Large damage, summons, scaling | Major mitigation/dodge/healing | Major exploration or freedom |
| 5 | Potential extreme/unbounded combat | Death prevention, repeated immunity | Extraordinary utility such as flight or remote scouting |

**`?` means insufficient mechanic evidence, NOT a score of zero.** Scores are **editorial estimates** of possible impact under the described conditions, not actual measured boss fight effectiveness. Item rarity names (Divine/Legendary), registered names, source class names or tooltips alone **do not prove** the exact mechanics of the installed jar.

**Combat gate bands:** `C0` no listed combat, `C1` minor, `C2` meaningful, `C3` major, `C4` potentially extreme, `C?` unknown. **C3/T5+ and C4/T7+** language is only a **review hypothesis**, not a final item minimum tier or change to any chest. Actual access remains as native unless separately implemented.

First pass **497 records**:
- **7 C4** candidate extreme combat
- **25 C3** major combat candidates
- **11 C2** meaningful
- **12 C1** minor
- **21 C0** no known combat impact
- **421 C?** unscored because direct item mechanics/loaded-version semantics have not been read or are inconclusive.

That is **76 entries with preliminary scores** and **421 awaiting deeper investigation**. The unscored 421 are not automatically safe or weak, and shouldn't be arbitrarily assigned Tiers from source family/rarity.

## First seven combat-priority cases
| Item | Source | Why first | Initial rule |
|---|---|---|---|
| **Qym Head** | Pasterdream | Official English tooltip states spell casting ignores cooldowns | **Review access**, slot and cross-mod spell semantics. Don't claim bypass applies to Iron's or Ars before source test |
| **Cecilia's Blessing** | Pasterdream | Grants 5s invulnerability, rapid health regen and Blink cooldown reset when HP falls below 15% | Review cooldown/exploit with repeated procs |
| **Turnback Cloak** | Pasterdream | Active effect dodges 6 hits over 90s, cooldown/energy expenditure described | Review invulnerability stacking and boss projectile interaction |
| **Cursium Chestplate** | Cataclysm | Self-revival at 5 HP + 5s immunity followed by 6 min debuff in source English description | Compare total effective survivability; don't ignore native lockout |
| **Abyssal Tiara (full set)** | Aquamirae | Source full-set death handler cancels most lethal damage, fully heals, applies Crystallization 300s | Verify source 7.2.7 against installed 7.2.10, including crystallization lockout |
| **Tempest Trident** | Aquamirae | Source `modifyOutgoingDamage` multiplies by `1 + Constant(20)` underwater; *could be a huge multiplier* | **P0 verify semantics in installed 7.2.10**; do not hard-code 21× as live fact |
| **The Infinitum** | Enigmatic Legacy Plus | AO config records unusual special damage + lifesteal values | Investigate formulas/curse path and stacking; don't infer stats directly from TOML numbers |

**Priority is not a nerf order.** If acquisition is hard and the ability is appropriate for the encounter tier, keeping it strong is desirable. A conditional full-set revive or cloak with a 300s cooldown can be more balanced than its short description suggests.

## Other important source examples
**Pasterdream attack/specialization:** Terra Charm (-60% Blade of Terra cooldown), Counter Ring (+50% skill damage after dodging), Ghost Face Head (Soul Howl spells waive Dream-melt costs), Evasion Cloak (extended Blink window). These are interesting Regalia because they improve specific builds rather than just generic attributes.

**Pasterdream easy utility:** Bright Butterfly (Night Vision and Darkness immunity), Endeye Charm (Enderman neutrality), Pure Gold Charm (Piglin neutrality), Paper Plane (wind mobility), Wind Knight Flag (headwind reversal) — may safely appear early pending their native loot sources.

**Cataclysm:** source matched 1.21.1/3.33, distinctive armor and weapons, Cursium revive, charged AoE; one of the strongest ongoing original-boss Regalia sources.

**Aquamirae:** its 1.21.1 source branch currently reports **7.2.7**, versus **7.2.10 physically installed**. More than twenty weapon/armor/ability registrations mapped, but don't assume every armor piece is a stand-alone T7 Regalia; set thresholds and aquatic conditional effects matter. **Dagger of Greed** drops emeralds when attacking villagers/illagers with a break chance: examine **economy abuse**, not combat gating.

**More Relics Mass Gauntlet:** extraordinarily high **configured damage cap** must NOT be called measured damage. It is deliberately **unscored** pending actual proc and calculation source.

**Flight Rings:** upstream basic ring uses gold/quartz and offers creative flight with possible hunger/XP/durability penalties. **High-utility early access is allowed by user policy.** Check server interaction (tower bypass, boss room traversal), do not simply make it T8.

## Remaining mod decisions for Regalia
- **Goety:** NOT present in the 332-JAR installed-profile audit of PR #45; **don't add Goety Regalia** to active catalogue. It can be screened if added later.
- **Twilight Forest, Iron's Spellbooks:** user wants no major targeted Regalia sweep from these. Treat normal equipment as Gear/Spells, not Regalia.
- **Ice and Fire:** basic weapons/armor not a current Regalia priority; only unusually special abilities after evidence, otherwise out.
- **Pasterdream** confirmed important and now has **48 new candidates** from native Curios and wing registration; English descriptions for some are strong; rest still need native item class/loot source.
- **Aquamirae** now has **30 new candidates** (special AbilitySet armor, boss weapons and utility); individual conditional powers need source inspection and installed version reconciliation.
- Other prior installed mod families retain earlier provisional entries, without inventing mods outside current pack.

## Next concrete audit order (without gameplay changes)
1. **Resolve C4/C3 and P0 combinations** first, with actual in-JAR effect handlers, stacking and cooldown/source, especially Pasterdream bypass/defense and Aquamirae conditional death prevention/underwater damage.
2. **Verify acquisition** for those ~32 highest-risk cases: chest table, recipe, boss drop, transaction materials, upgrade conditions and rarity. Keep individual unique items strong if difficulty and tradeoff justify it.
3. **Follow source item descriptions for currently unscored Relics, Artifacts, Reliquified and EL+**. Give scores only after obtaining direct mechanics; do not label 421 unknown items T0.
4. **Build utility shortlist** (flight, travel, information, underwater, night vision) with a preferential early/midgame availability policy; review only access glitches/campaign locks.
5. **Audit multi-item immortality and DPS loops** across NeoPasterDream dodge/Cecilia, Cataclysm revive, Aquamirae armor, Relics resurrection, Enigmatic lifesteal, Apotheosis high HP/gem regen, spell cost reduction. Per-player actual sample builds, not hypothetical item names.
6. Only then adjust material costs, boss first-clear reward, gem gates, or source rarity in a separate experimental overlay with rollback and user review. **No automatic item nerfs approved.**

## Source repositories
- [Pasterdream Curio registrations](https://github.com/LOVE-U987/NeoPasterDream1/blob/main/PasterDream/src/main/java/com/pasterdream/pasterdreammod/registry/items/PDItemsCurios.java) and [English effect text](https://github.com/LOVE-U987/NeoPasterDream1/blob/main/PasterDream/src/main/resources/assets/pasterdream/lang/en_us.json)
- [Aquamirae 1.21.1 ability sets](https://github.com/ObscuriaLithium/Aquamirae/blob/1.21.1/common/src/main/java/dev/obscuria/aquamirae/registry/AquamiraeAbilitySets.java); [full-set Tiara death handler](https://github.com/ObscuriaLithium/Aquamirae/blob/1.21.1/common/src/main/java/dev/obscuria/aquamirae/common/ability/armor/AbyssalArmorFullSetWithTiaraAbility.java); [Tempest Trident damage handler](https://github.com/ObscuriaLithium/Aquamirae/blob/1.21.1/common/src/main/java/dev/obscuria/aquamirae/common/ability/weapon/TempestTridentAbility.java)
- [Cataclysm 3.33 source registry](https://github.com/lender544/new1.20.1/blob/1.21/src/main/java/com/github/L_Ender/cataclysm/init/ModItems.java)
- [Flight Rings item registrations](https://github.com/tired9494/flight-rings/blob/1.21.1-architectury/common/src/main/java/tired9494/flight_rings/registry/ModItems.java)

**No claims of Java mod runtime validation, chest probability, item tier approval or actual config mutation. This is a prioritized research pass.**
