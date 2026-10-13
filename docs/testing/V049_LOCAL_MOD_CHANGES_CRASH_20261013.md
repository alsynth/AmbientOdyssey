# Ambient Odyssey — v0.4.9 local additions and crash (13 October 2026)

Source: user-supplied latest(20261013-182534).log for Ambient Odyssey v0.4.9 Client Performance TEST, MC 1.21.1 NeoForge 21.1.252.

## Crash (confirmed)
At 20:24:42, Simply More 1.3.0 Alpha StunEffect.applyEffectTick invokes EntityUtils.putAllItemsOnCooldown, line 40, which tries to cast client-side ClientLevel to server-side ServerLevel. This throws ClassCastException while a MmmMmmMmmMmm TargetDummyEntity is being ticked. Simply More is the direct code defect; target dummy is the triggering entity, not proved defective. Test without stunning dummies, and check upstream for a fixed version or add proper server-side guard.

## Local additions / updates to reconcile
423 distinct "Found mod file" JARs observed. These are present in the player's test instance; new vs updated vs existing is NOT confirmed until compared to actual previous resolved release manifest. Candidates warranting reconciliation with former release, filenames observed:
- aces_spell_utils-1.2.7.3-1.21.1.jar
- ancient_remnants-1.5.2+1.21.1-neoforge.jar
- antiquetradingship-1.4.0-neoforge-1.21.1.jar
- apothiccombat-1.2.1.jar
- aquatic_creepers-neoforge-1.0.0+1.21.jar
- archaion-1.21.1-1.4.4.jar
- astrological-1.21.1-1.7.1.jar
- atmosfera-1.21.1-NeoForge-1.0.2.jar
- benssharks-1.2.6-neoforge-1.21.1.jar
- block_factorys_bosses-2.1.2-neo-1.21.1.jar
- brutalbosses-1.21.1-8.6.jar
- cataclysm_spellbooks-1.1.14-1.21.jar
- cosycritters-0.3.3+1.21.1-neoforge.jar
- cultofazazelneoforge-1.1.4.12.jar
- denseflower-1.0.0.jar
- dungeon_difficulty-neoforge-3.9.2+1.21.1.jar
- endrem_additions-neoforge-1.2.0.jar
- enhancedbossbars-1.0.0.jar
- ftb-solo-quests-1.21.1-neoforge-1.1.2.jar
- ftboceanmobs-21.1.4.jar
- hybrid_aquatic-neoforge-1.21.1-1.7.4.jar
- irons_jewelry-1.21.1-2.0.2.jar
- irons_lib-1.21.1-2.2.0.jar
- jearchaeology-1.21.1-1.2.0.jar
- jupiter-2.3.7-1.21.1-neoforge.jar
- simplymore-forge-1.3.0_alpha.jar (crash involved)

## Explicit rejection
**Mob Plaques is NOT wanted.** MobPlaques-v21.1.1-1.21.1-NeoForge.jar is present in the log. Remove from player-local profile and exclude from future official profiles. Do not interpret presence as approval.

## Separate warnings
- cardinal-components-api-6.1.2.jar was skipped by early NeoForge Fabric detection. Investigate Connector loading before changing it.
- Repeated malformed JSON: Unterminated array at line 11 column 6 path $.values[6]. Identify tag path later.
- Missing models/translation errors were logged, but not demonstrated to cause this crash.

## Next actions
Compare complete 423-JAR local snapshot against actual pre-v0.4.9 manifest and classify all added, changed, removed mods; only then add approved changes to release. Keep Mob Plaques out. No runtime validation, release edits, or actual mod changes made by this note.
