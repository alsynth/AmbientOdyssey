# Ambient Odyssey — Regalia exceptions requiring owner decision (15 October 2026)

**Research/curation only — not implemented.** Source: 497-entry `REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv` on branch `research/regalia-combat-ranking-20261013`; 7 high-risk C4, 25 C3, 11 C2, 12 C1, 21 C0, 421 C? unscored. All C-ranks are preliminary editorial assessments and native versions/registries not uniformly verified.

## Current owner strategy
- Broad eligible Regalia available through T2–T5; target roughly 90% *of verified suitable reward items* by T5, not an invented classification for the 421 unknowns.
- Bosses T2–T9 provide one guaranteed Regalia in addition to one genuine affixed equipment item and native rewards. Keep native acquisition and use small additive reward tables.
- Hold only truly dangerous offensive, immortality and resource/cooldown bypass gear for late tiers. Utility/flight alone is not grounds for late gating.
- Enigmatic Legacy Plus craftable candidates should be **heavily downweighted in the new boss reward roll** after proving recipe availability from effective JAR recipes; 90% reduction is only an unapproved example, not a final owner decision.
- Don't conflate noncraftable with guaranteed rare boss drops; respect native boss-exclusive trophies and progression conditions.

## 32 source-flagged higher-combat-risk entries — decision queue
These are **not automatically banned or late-tier**. Decide case-by-case between (a) ordinary broad T2–T5 pool, (b) T6–T7, (c) T8–T9, (d) exclude from generic guarantee / preserve native-only, and (e) test first. Because user previously favored natural acquisition for most Regalia, the default for ambiguous mechanics is test first, not late-gate by fiat.

| Band | Item | Mod | Candidate ID | Why flagged (catalogue evidence) | Status |
|---|---|---|---|---|---|
| C4 | Turnback Cloak | NeoPasterDream | pasterdream:turnback_cloak | Source tooltip: automatically dodges 6 hits on activation within 90 s, 300 s cooldown | **HOLD FOR REVIEW** |
| C4 | Cecilia's Blessing | NeoPasterDream | pasterdream:ceciliacare_charm | Source tooltip: 5 s invulnerability, health recovery and Blink cooldown reset below 15% HP | **HOLD FOR REVIEW** |
| C4 | Abyssal Tiara | Aquamirae | aquamirae:abyssal_tiara | Requires full Abyssal armor with Tiara: blocks most deaths, fully heals player, imposes Crystallization for 300 seconds; exact 7.2.10 semantics to test | **HOLD FOR REVIEW** |
| C4 | Cursium Chestplate | L_Ender's Cataclysm | cataclysm:cursium_chestplate | Revive at 5 HP, invulnerable 5 s, then 6-minute self-lockout | **HOLD FOR REVIEW** |
| C4 | The Infinitum | Enigmatic Legacy Plus | enigmaticlegacyplus:the_infinitum | Config: large special damage + lifesteal settings; numerical semantics unverified | **HOLD FOR REVIEW** |
| C4 | Tempest Trident | Aquamirae | aquamirae:tempest_trident | Source implementation multiplies outgoing damage by (1 + 20) if attacker is underwater; verify installed 7.2.10 and actual conditions | **HOLD FOR REVIEW** |
| C4 | Qym Head | NeoPasterDream | pasterdream:qym_head | Pasterdream tooltip says casting ignores cooldowns; potential unrestricted spell rotation | **HOLD FOR REVIEW** |
| C3 | The Testament of Contempt | Enigmatic Legacy Plus | enigmaticlegacyplus:eldritch_amulet | Config: damage and lifesteal plus keepInventory; verify defensive math | **HOLD FOR REVIEW** |
| C3 | Evasion Cloak | NeoPasterDream | pasterdream:evasion_cloak | Source tooltip: widens dodge window to 0.6 s for 90 s | **HOLD FOR REVIEW** |
| C3 | Majestic Elytra | Enigmatic Legacy Plus | enigmaticlegacyplus:majestic_elytra | Flight + resistance from installed config; check bypass/stacking | **HOLD FOR REVIEW** |
| C3 | The Arrogance of Chaos | Enigmatic Legacy Plus | enigmaticlegacyplus:chaos_elytra | Config: large special-damage resistance and flight; early exploration flight acceptable, defense must be checked | **HOLD FOR REVIEW** |
| C3 | Revival Leaves | Enigmatic Legacy Plus | enigmaticlegacyplus:revival_leaf | Config heal/regen/cooldown; survival trigger semantics unverified | **HOLD FOR REVIEW** |
| C3 | Non-Euclidean Cube | Enigmatic Legacy Plus | enigmaticlegacyplus:the_cube | Config damage-limit and auto-trigger; mechanism/unconditionality unverified | **HOLD FOR REVIEW** |
| C3 | Ring of Quenching | Enigmatic Legacy Plus | enigmaticlegacyplus:infernal_ring | Config high special-damage resistance modifier | **HOLD FOR REVIEW** |
| C3 | Heart of the Golem | Enigmatic Legacy Plus | enigmaticlegacyplus:golem_heart | Config armor/toughness/resistance bonuses; verify effective cap and slot | **HOLD FOR REVIEW** |
| C3 | Emblem of Bloodstained Valor | Enigmatic Legacy Plus | enigmaticlegacyplus:berserk_emblem | Config damage/speed/resistance effects; units need source math | **HOLD FOR REVIEW** |
| C3 | Crystal Greatsword | Eternal Starlight | MISSING | Stacking Crystal Infection damage and blocking | **HOLD FOR REVIEW** |
| C3 | Moonring Greatsword | Eternal Starlight | MISSING | Lunar Thorn burst and blocking | **HOLD FOR REVIEW** |
| C3 | Counter Ring | NeoPasterDream | pasterdream:counter_ring | Source tooltip: +3 attack and +50% combat-skill damage briefly after successful dodge | **HOLD FOR REVIEW** |
| C3 | The Twist | Enigmatic Legacy Plus | enigmaticlegacyplus:the_twist | Config unusually high special damage boost/knockback; units to verify | **HOLD FOR REVIEW** |
| C3 | Ghost Face Head | NeoPasterDream | pasterdream:ghost_face_head | Source tooltip: Soul Howl casts cost zero dream energy/sanity, 10% spirit summon | **HOLD FOR REVIEW** |
| C3 | Terra Charm | NeoPasterDream | pasterdream:terra_charm | Source tooltip: -60% Blade of Terra cooldown, +30% aura scaling, reduced energy cost | **HOLD FOR REVIEW** |
| C3 | Caelestis | Simply Swords | simplyswords:caelestis | Official unique weapon, summoning ability; detailed coefficients to verify | **HOLD FOR REVIEW** |
| C3 | Mjolnir | Simply Swords | simplyswords:mjolnir | Official unique weapon: conductive stacks, mobile thunderstorm and thunderclap when fully awakened | **HOLD FOR REVIEW** |
| C3 | Charm of Hell Blade | Enigmatic Legacy Plus | enigmaticlegacyplus:hell_blade_charm | Config high attack/debuff values; units/mechanic unverified | **HOLD FOR REVIEW** |
| C3 | Lost Engine | Enigmatic Legacy Plus | enigmaticlegacyplus:lost_engine | Config critical multiplier and vulnerability cost; must test crit stacking | **HOLD FOR REVIEW** |
| C3 | Coldsnap | Eternal Starlight | MISSING | On-hit freezing and Brittle effect from Eternal Starlight official wiki | **HOLD FOR REVIEW** |
| C3 | Moonring Bow | Eternal Starlight | MISSING | Fully charged arrow produces Lunar Thorns | **HOLD FOR REVIEW** |
| C3 | Rage of Stars | Eternal Starlight | MISSING | 9-meteor AoE on attacks | **HOLD FOR REVIEW** |
| C3 | Starfall Longbow | Eternal Starlight | MISSING | Arrow impacts spawn 9 meteors | **HOLD FOR REVIEW** |
| C3 | Wilted Crossbow | Eternal Starlight | MISSING | Bolts apply Wither/Slowness aura and petals during flight | **HOLD FOR REVIEW** |
| C3 | The Annihilator | L_Ender's Cataclysm | cataclysm:the_annihilator | High critical damage and charged AoE | **HOLD FOR REVIEW** |

## Data-quality and source audit queue
- **421 C?**: no sufficient combat ranking. NOT confirmed safe, not automatically high-tier. Review especially every candidate included into the new guaranteed pool, with actual JAR, registered item ID and native acquisition evidence.
- Several C3 Eternal Starlight entries have a **blank candidate registry ID**, meaning none can be used in executable weighted pools without registry verification.
- Enigmatic Legacy Plus has **123 catalogue entries**, many explicitly marked unknown acquisition/crafting. Inspect installed recipe JSON, native loot modifiers and upgrades; add explicit `craftable:true/false/uncertain` and concrete recipe resource evidence to an audit before weight changes.
- Verify name variants, duplicates and actual item types; catalogue includes normal weapons/equipment and patterns that may not make sense as individual Regalia rewards. Preserve owner goal without claiming all 497 valid.
- Prior owner tested Abyssal Tiara and The Infinitum and did not request broad nerfs; test as necessary but don't automatically blacklist or overwrite native routes. Qym Head cross-mod spell behavior remains an explicit owner test.

## Proposed next owner review order
1. 7 C4 candidates first (Qym Head, Tempest Trident, death-prevention and near-immortality items).
2. 25 C3 candidates, in small batches, with source-verification flags.
3. After source audit, show **only genuinely uncertain** entries to owner; allocate remainder to broad low-tier pool, with targeted exclusions.

No complete Enigmatic recipe extraction or runtime item tests have occurred in this writing session; explicit craftability claims remain unverified.

## Binding owner decisions — first C4 batch (15 October 2026)

These overrides apply **only to the new guaranteed boss Regalia bonus pool**; existing native crafting, loot and acquisition stay unchanged. Do not implement in executable loot tables until integration approval. Earlier catalogue C4 flags are risk-review labels, **not** minimum allowed tiers.

| Item | Approved new boss bonus reward eligibility |
|---|---|
| Qym Head | **Native only** |
| Tempest Trident | **T2–T5** |
| Cecilia's Blessing | **T2–T5** |
| Turnback Cloak | **T2–T5** |
| Abyssal Tiara | **T2–T5** |
| Cursium Chestplate | **Native only** |
| The Infinitum | **T6–T7** |

Native only means excluded from the additive generic boss Regalia roll, not removed from its native drops/crafting. T2–T5 means eligible in the broad early pool even where original power assessment flagged C4. T6–T7 for The Infinitum is a new boss reward band, with native acquisition intact.
