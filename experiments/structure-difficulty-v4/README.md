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
