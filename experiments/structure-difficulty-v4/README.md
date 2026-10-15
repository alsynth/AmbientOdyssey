# Dungeon Difficulty v4 stronger pilot (14 Oct 2026)

EXPERIMENTAL / NOT LIVE / NOT RUNTIME-TESTED. Based on PR45 v3 candidate (experimental/structure-difficulty-v3-20261013); does not replace installed config or modify rollback.

| Tier | Health base bonus | Attack base bonus | Armor addition |
|---|---:|---:|---:|
| T2 | +100% | +40% | +3 |
| T3 | +150% | +60% | +5 |
| T4 | +200% | +80% | +8 |
| T5 | +250% | +100% | +11 |
| T6 | +300% | +200% | +15 |

Retains 27 Tier2-6 combat zone rules with unchanged structure matches, dimension matches, level=1, vanilla-hostile matcher and disabled spawner/experience/loot multipliers. Removes 26 mappings: old Tier0-1 no-op zones and Mechanical Nest's previously unapproved blanket Tier5 scaling. Mechanical Nest remains boss-focused pending identification of actual boss. Dungeon Crawl stays whole-dungeon Tier3. Keep protected Tier0 sites unchanged; do not add blanket rules for boss entities, Quark or Alex's Mobs incidental entities, slime/creeper mounted Keep Kayra encounter.

**IMPORTANT:** Extra health/attack may double-stack with Apotheosis affix mobs, Brutal Bosses, and native Foundry named buffed mobs. Verify effective stats in test world; cap/exclude if necessary before deployment. Attack attribute does not necessarily govern ranged, magical, explosive or custom damage. DD may buff spawned mobs but is not a generic rewrite of spawner block NBT or worldgen placement. No runtime validation here.

Remaining acceptance: JSON parse with installed DD 3.9.2, exact rule matching, startup, T2/T3/T5/T6 ordinary mobs, Foundry native named mobs, an Apotheosis/Brutal elite, performance, rollback and multiplayer. Test candidate only.

## Owner rationale and tip recommendation

Design intent: prevent Apotheosis progression from trivializing later dungeons, and make high-tier Brutal Bosses potentially demanding group encounters. These are untested additive-to-base DD attribute modifiers, not promised final HP or damage values. Keep elite-stack and boss health cap tests open; do not silently nerf the approved table without gameplay evidence.

**Proposed tips-and-tricks loading screen / questbook copy:** "Tier 4+ dungeons are dangerous. We recommend exploring them with at least two players—especially when a Brutal Boss is present."

The wording is a gameplay recommendation, not a hard multiplayer requirement. Tips are documented here only; actual in-game tip resource integration is still pending.

## Mechanical Nest owner update

Owner assigns the **Mechanical Nest main boss** to the **same boss difficulty tier as Cataclysm's The Harbinger**. Keep boss tier distinct from the structure's older provisional Tier5 label. The current 38-row PR44 boss roster does not explicitly enumerate Harbinger; resolve the exact number against the owner's final tier assignments before implementing its numeric boss scaling. **Do not reinstate the blanket Mechanical Nest DD mob zone**; tune its actual boss through the dedicated boss-balance pass after verifying the entity/source. Ordinary Mechanical Nest minions remain excluded from individual tuning.

## Owner decision: broaden DD coverage (15 Oct 2026)

**Replace the 27-zone pilot as the eventual coverage target:** all installed, enabled and verified tiered **Tier 2+ structures** should receive a corresponding DD zone, including Tier 7–9 structure sites when their separate **structure tier** is known. Tier0–1 excluded. This is a *coverage goal*, NOT permission to classify the 756+ unresolved historical native IDs without checking current installed registry, dimension, final owner-approved tiers, effective resource/structure ownership and non-structure content. Reconcile from the PR56 tier/structure inventory and verify the physical full pack. Preserve 26 owner-protected Tier0 and Dungeon Crawl whole-dungeon Tier3. Remove stale blanket exclusions only when explicitly superseded; Mechanical Nest remains an exception as boss-centric rather than normal mobs. Bosses still need actual entity-ID matcher coverage; being inside a zone does NOT automatically scale a modded boss.

**Added to experimental config now:** `cataclysm:acropolis` (Scylla, End), `cataclysm:frosted_prison` (Maledictus, Overworld), `cataclysm:sunken_city` (Leviathan, Overworld) as provisional DD tier6 *structure* zones. This T6 structure classification is a temporary candidate, **not an owner-approved boss tier**, and the vanilla-only hostile regex means the bosses themselves will NOT be buffed by these rules until exact entity matching is separately verified/expanded. Do not apply an extra native boss buff assuming DD already affects them. Scylla remains boss T9, and Maledictus/Leviathan boss tier should follow the owner's latest roster decision, independent of this temporary zone selection.

**Owner boss-overlap scope:** Dead King is the only named boss from the earlier 27 DD-covered structures presently counted as an intended DD-overlap case (pending actual spawning/identity and modded entity matching). Keep Kayra and Foundry don't count as independent named boss encounters for this crosswalk. Brutal Bosses interactions are accepted conceptually; verify effective stacking rather than exclude them reflexively. All other named bosses should receive tier-based native buffs where their actual entity is not already scaled by DD. Cataclysm three arena bosses require explicit matcher verification; no blanket same HP buff twice.

**Outstanding DD expansion action:** generate an auditable source-derived `structure ID / dimension / structure tier / installed / zone present / reason withheld` crosswalk from PR56 before automated mass zone injection. Expansion not completed by this commit: only 3 explicit zones added (total 30).

## Expansion audit update (15 Oct 2026)

Source: PR56 1,240-row first-pass catalogue. **497 installed/registered Tier2+ candidates**, of which 30 were present when the expansion CSV was generated; 324 additional legacy-provisional, 128 heuristic tier reviews, 14 sites above the currently defined six-tier DD types, and 1 owner-approved Dungeon Crawl exception. Full crosswalk: `DD_TIER2PLUS_INSTALLED_EXPANSION_QUEUE.csv`. Not every catalogue row is runtime-proven, and this queue excludes filename-absent providers / AO generated source requiring separate effective-resource confirmation.

**Dungeon Crawl** is now added in the config as whole-dungeon T3 Overworld zone (`dungeoncrawl:dungeon`), so **31 total draft zones**. Confirm final registry and exact dimension during runtime tests. The CSV reflects the state immediately prior to this addition and therefore marks Dungeon Crawl as pending; don't count it as still missing.

**IMPORTANT correction:** the three added Cataclysm arena zone types are **provisional T6** due to no DD types above T6, while PR56's structure-tier catalogue assigns Acropolis T7, Frosted Prison T7, Sunken City T9. These are *structure* tiers in the first-pass catalogue (often provisional), distinct from boss tiers. Do NOT present them as finalized T6 balancing. Do not assume Cataclysm boss entities are affected by DD's current 17 vanilla-hostile matcher; dedicated modded entity-ID matching remains necessary. Tier 7–9 handling must be designed and reviewed before applying tier-specific DD scaling there.

Next: audit candidate structures' effective dimension+registered IDs, approve or reconcile tier labels, generate new zone sets in batches, validate DD parser and gameplay. Keep active pack and rollback unmodified.
