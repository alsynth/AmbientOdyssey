# Stellaria dependency and provenance record

Checked 17 October 2026. A downloaded Stellaria jar was not available to hash or inspect in this environment. This file separates the published release from the newer source tree.

## Stellaria release vs source

| Input | Verified value | Status |
|---|---|---|
| Minecraft target | 1.21.1 | Published page and source metadata |
| Official published file | 1.0.0; Modrinth version ID GdByPVEt; coordinate maven.modrinth:zX7Jf0It:GdByPVEt | Official Modrinth page |
| Published loader/environment | Fabric; client and server | Published page |
| Published declared dependencies | Fabric API 0.116.12+1.21.1; MidnightLib 1.9.3+1.21.1-fabric; Veil 4.2.0; GeckoLib 4.9.1 | Modrinth version index; actual downloaded jar metadata not inspected |
| Published jar URL/hash | Not captured | Do not treat a source hash as the released jar hash |
| Source repository | https://github.com/Lekeko/Stellaria | Official source |
| Source ref and commit | master; 5b9ce3705e057a3d3b68bf7726aa10215b88d28b | Checked-out source |
| Source archive SHA-256 | 13361a9734bb21ff61a37ca9beb5ab9ed464fcdc82239d9c81afa5bc07698e18 | SHA-256 of git archive at the commit above |
| Source mod version | 2.0.0 | gradle.properties |
| Source Java requirement | 21 | build.gradle compile release and source compatibility |
| Source Fabric Loader | 0.19.3 | gradle.properties |
| Source Fabric API | 0.116.12+1.21.1 | gradle.properties |
| Source Veil | Fabric Veil 4.5.0 | build.gradle dependency plus gradle.properties |
| Source GeckoLib | Fabric 4.9.1 | build.gradle dependency plus gradle.properties |
| Source MidnightLib | 1.9.3+1.21.1-fabric | build.gradle dependency plus gradle.properties |
| Source build wrapper | Gradle 9.5.0 | gradle-wrapper.properties; distribution unavailable here |

The release and source are not interchangeable. The source 2.0.0 dependency declaration is newer than the published 1.0.0 listing. No unreleased source jar was built.

## NeoForge Connector candidates

These are candidates surfaced from the official version listings, not a tested lock:

| Component | Candidate for 1.21.1 | Evidence | Status |
|---|---|---|---|
| NeoForge | 21.1.252 | AO target | Target only; no runtime |
| Sinytra Connector | 2.0.0-beta.17+1.21.1; Modrinth version ID IITF0PRC | Official version page | Candidate, not installed |
| Forgified Fabric API | 0.116.15+2.3.4+1.21.1; Modrinth version ID K4hHKnnI | Official version page | Candidate, not installed |
| Launchpad | Version not resolved | Connector guidance says assess only if required by the chosen Connector/mod combination | Unverified |
| Native NeoForge Veil | Exact version and API match not resolved | Stellaria declares Fabric Veil APIs, including client renderer and Quasar APIs | Unverified |
| Native NeoForge GeckoLib | Exact version and cross-loader API match not resolved | Stellaria uses GeckoLib types in entity and renderer code | Unverified |
| Native NeoForge MidnightLib | Exact version and cross-loader API match not resolved | Published dependency is Fabric-specific | Unverified |

Do not install a Fabric Veil jar and a NeoForge Veil jar together. Do not assume the Fabric API wrappers provide Veil or GeckoLib classes. The required APIs must resolve to one compatible implementation on both sides, with no duplicate mod IDs.

## AO rendering baseline inspected

The current AO performance-preparation document identifies the comparison baseline as Embeddium 1.0.15, NeoOculus 1.8.7, and Complementary Reimagined r5.9.3 (CurseForge project/file 627557:8884654). Euphoria Patcher was not installed in that audited baseline; 1.10.5 was a proposed separate trial. AO's later profile must be rechecked before a runtime run. No Stellaria shader combination was tested.
