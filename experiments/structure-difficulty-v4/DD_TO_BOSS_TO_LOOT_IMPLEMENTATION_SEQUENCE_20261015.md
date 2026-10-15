# Ambient Odyssey — DD consolidation to boss balancing to loot overhaul
Date: 2026-10-15. Planning and source audit, **not deployed**.

## Current scope and sequencing
1. Consolidate selected Tier2+ **Overworld** structure IDs and owner-assigned *structure tiers*. See `DD_CONSOLIDATED_OWNER_TIER_PLAN_20261015.csv`. Preserve owner exceptions.
2. Resolve verified dimensions and registry IDs in batches, then build DD config for those sites; do not turn provisional data into runtime claims.
3. Fix current experimental zone/type mismatches: existing Foundry config T5 vs owner T6, Cataclysm Acropolis T6 draft vs owner structure T9 but End site (defer), and unverified Frosted Prison/Sunken City placeholder T6. A nominal zone does not scale modded bosses unless their entity IDs match.
4. After DD placement and matcher validation, implement **boss-native HP/damage tier baseline** for bosses not already receiving verified DD boss buffs. The owner has NOT yet approved numeric boss multipliers. Keep high-end addon engineering separate.
5. Then tune **Lootr/structure chest loot tables AND individual boss drops**, classing container contents as Scrap, Supply, Equipment, Treasure, Grand Treasure and preserving thematic uniques; Lootr does not itself determine sensible drop rates.

## Boss baseline assignment / overlap gate
- **Dead King**: owner-designated only existing named-dungeon boss potentially overlapping a current DD site (Iron's catacombs). Current DD 17-vanilla-hostile regex does NOT confirm scaling Iron's modded boss. Verify registry entity and encounter/zone.
- **Scylla / Maledictus / Leviathan**: owner permits their arena structures to receive DD scaling. No modded-boss entity matcher is deployed. Scylla Acropolis = structure T9 owner correction, End/other-dimension hold under present Overworld-only expansion. Frosted Prison and Sunken City structure tiers require separate reconciliation before any boss-attribute counting.
- **Brutal Bosses**: global HP x4 / damage x3 / eligible chest chance 70 / minimum distance 30 remains PR59 draft. Owner accepts dangerous interactions with DD; validate actual attributes and multiplicative stacking rather than implicitly exempting.
- **Mechanical Nest**: structure Tier5 retained in the catalogue, **boss-focused**; do not activate blanket DD mob scaling. Owner requests boss parity with Harbinger; exact native entity and final numeric boss-tier reference need verification.
- **Foundry**: owner changed structure T5 -> T6; native named spawner entities carry customized health, so DD may double-stack vanilla entity matches; test.
- Other named bosses: apply boss-specific/native tier buffs only after mapping mod config, entity ID, damage mechanics and confirmed DD overlap. For modded spell, projectile and special damage, generic attack attribute is not guaranteed to alter actual output.

## Frozen decisions
- T2 HP +100%, attack +40%, armor +3; T3 +150%, +60%, +5; T4 +200%, +80%, +8; T5 +250%, +100%, +11; T6 +300%, +200%, +15.
- Settlements and buildings T1; caves/underground T2; temples/ruins T2; towers/forts/camps T3 **as category defaults**, with explicit owner decisions taking precedence.
- Non-Overworld and Pasterdream candidates held for later. Dungeon Crawl whole dungeon Tier3. Tier0-1 excluded. 26 protected Tier0 spawner structures remain protected.
- Category G Ice & Fire mausoleum Tier4; Category B Abandoned Temple T4, Foundry T6, Kisegi Sanctuary T4, Corsair Corvette T4; Category A owner choices retained in ledgers.
- High-tier boss and structure tiers are separate; DD v4 currently defines only T0-T6 types. No implicit mapping T7-T9 -> T6 is approved.
- The 497-row source catalogue contains provisional and dimension-unknown structures. The consolidated tier map is a **review worklist**, not a declaration that all are verified or live.

## Acceptance
Validate structure registry + dimensions in actual full pack; add only effective structure IDs; ensure DD matching can affect spawner-generated ordinary mobs and planned named bosses; benchmark elite stacking on regular T2/T4/T6, Foundry, Dead King, and Brutal Bosses. Confirm startup/dedicated server, no unwanted biome-wide effects, performance and reversible rollback. No draft is merged or runtime tested in this research pass.
