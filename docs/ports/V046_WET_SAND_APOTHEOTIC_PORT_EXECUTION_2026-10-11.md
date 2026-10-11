# AO v0.4.6 — Wet Sand & Apotheotic Additions port execution

**Date:** 11 October 2026. **Branch:** `experimental/v046-wetsand-apotheotic-ports-20261011`.

## Source provenance / requirements

- Wet Sand official original source: [HearthianDev/wet-sand](https://github.com/HearthianDev/wet-sand). GPL-3.0 source license according to repository. Published mod is Fabric; its current main branch targets a newer Minecraft version (at audit: 1.21.11), and its legacy branch targets 1.20.1. Neither is a drop-in 1.21.1 NeoForge JAR. Upstream warns that its default world-generation variant conflicts with worldgen replacement mods, which is especially relevant to AO's FreeTerraForged/Biolith/terrain configuration. Sinytra Connector is installed in AO, but without a matching Fabric 1.21.1 binary it cannot fix a Minecraft version mismatch.
- Apotheotic Additions original source: [Bryce792/ApotheoticAdditions](https://github.com/Bryce792/ApotheoticAdditions). `mods.toml` version 2.2.2, license declaration Academic Free License 3.0, Forge MC 1.20.1 and Apotheosis 7.4.3+. Current AO uses NeoForge MC 1.21.1 and Apotheosis 8.9.0. Preserve upstream credit and investigate asset source/licensing before distributing any derived content.

## Work actually committed

### Wet Sand native milestone 1

- A **distinct, original, isolated NeoForge source prototype** lives under `ports/wet-sand-neoforge`; NOT installed in any current CurseForge import.
- Contains six mod-local registered block and item types for moist/wet/soaked normal and red sand, with server-only random-tick moisture progression toward water and dry regression. This proves registry and basic block API viability, subject to CI and a future runtime test. It does **not** port the original textures, vanilla dry sand conversion, gravity/collision-specific behavior, sugar cane moisture support, suspicious-sand treasure preservation, water-bottle mechanics or natural shoreline/worldgen placement.
- **Next:** finish compile tests and blockstate/model assets, then add protected, cost-bounded conversion of nearby existing vanilla sand without a heavy worldgen scan. Keep no mass terrain rewrite for FTF. Decide whether replacing upstream block IDs is necessary for save migration; do not declare save compatibility.
- **Implementation policy:** keep upstream assets/code out of this MIT-licensed original prototype. If the project later forks/translates upstream GPL-3.0 code or art, change applicable license handling, credit and redistribution compliance accordingly. Do not ship a derivative as closed-source.

### Apotheotic Additions source migration milestone 1

- `ports/apotheotic-additions/port_schema_probe.py` loads the upstream extracted `data/apotheotic_additions` affix files **read-only** and creates an explicit, fail-closed migration report. No old affix JSON is written into active Paxi data or the live pack.
- Legacy `apotheosis:attribute` fields include old `types`, uppercase operation `ADDITION`, and per-rarity `min/steps/step` rolls. Apotheosis 1.21 source uses `categories`, `definition`, lowercase operations, and `min/max` rolls. The port needs custom rarity registry codecs before Artifact/Heirloom/Esoteric entries become valid; labels alone do not add those rarities.
- First CI source audit (before client runtime) classified **264** upstream JSON affix definitions: **118** old attribute-affix candidates blocked on schema/rarity semantics; **146** other affix types needing separate converters. This is a *development inventory*, not successfully migrated features.
- **Next:** inspect 1.21.1 Apotheosis 8.9 exact rarity registration extension points and component codecs. Prototype 1 Artifact and 1 Heirloom rarity plus a minimal compatible affix set with actual loot testing; preserve Esoteric as unobtainable. Then migrate gems, bosses, tables and cross-mod assets in compatibility-filtered batches. No broken old JAR or data should be included by editing version constraints only.

## Testing and release policy

`.github/workflows/v046-two-mod-port-preflight.yml` independently checks the Wet Sand NeoForge source compilation and downloads/examines exact upstream Apotheotic Additions data in a throwaway CI workspace; its artifacts are a **prototype JAR** and a **migration report**, **not a playable combined v0.4.6 modpack**. Do not change v0.4.5 test ZIP or older rollbacks. No in-game support is claimed until both projects pass native client startup, data reload, FTF worldgen and two-player dedicated-server tests.
