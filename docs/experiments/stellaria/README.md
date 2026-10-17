# Stellaria NeoForge feasibility probe

**Verdict: NOT TESTED at runtime.** Static source review found multiple likely dedicated-server side-boundary failures. No Stellaria code or modpack profile is included in this change.

## Scope and baseline

This experiment is based on the latest consolidated AO development source, PR 64 branch experimental/master-integration-r3-reconciled-20261015 at parent commit 3806fa1d1a7aef6e3a8ecad666e185815963b7c4. It does not change main or the R4 package. Stellaria source was inspected at Lekeko/Stellaria commit 5b9ce3705e057a3d3b68bf7726aa10215b88d28b.

AO targets Minecraft 1.21.1 and NeoForge 21.1.252. Its inspected render baseline is Embeddium 1.0.15, NeoOculus 1.8.7 and Complementary Reimagined r5.9.3. Euphoria Patcher 1.10.5 was a proposed isolated follow-up, not installed in the inspected baseline. This comes from docs/performance/V049_OVERHAUL_PREP_20261012.md; no live game profile was available in this environment.

## What was completed

- Inspected the current AO status, operating workflow, PR 64 and canonical implementation handoff before choosing the parent branch.
- Inspected Stellaria's published Modrinth release and the exact current upstream source commit. The published release is 1.0.0, while source master declares 2.0.0 and changes its Veil dependency to 4.5.0.
- Added and ran tools/audit_stellaria_server_paths.py against the checked source. It reports three direct server-to-client API paths and one common entity needing side-split review.
- Attempted the actual upstream Gradle server task with ./gradlew runServer. Gradle stopped before configuration: the wrapper could not download its Gradle 9.5.0 distribution because network access is unavailable.
- Recorded the exact environment, source hash, candidate stack and untested gates in the linked evidence files.

## Runtime verdict

There is no verified working Connector setup yet. The environment has Java 17.0.20; Stellaria declares Java 21 and its Gradle build targets Java 21. Gradle 9.5.0 is not cached, and the wrapper download fails with a network-unreachable error. The repository also has no Minecraft launcher, dedicated-server installation, graphics device/session, or AO instance available to this task. Therefore no NeoForge boot, dedicated-server join, shader rendering, fight, multiplayer, or performance result is claimed.

Do not interpret the source audit as a proven crash trace. The audit identifies code paths that must be fixed or disproved with a real server run. See BUGS_AND_PATCHES.md.

## Candidate test stack for the next runtime-enabled pass

Use a clean disposable NeoForge 1.21.1 / 21.1.252 profile. Test a current Connector 1.21.1 build with its compatible Forgified Fabric API first, then the official Stellaria 1.0.0 release and its exact listed dependencies. Do not mix its Fabric Veil 4.2.0 with NeoForge Veil. Source master 2.0.0 is a separate build candidate and must not be substituted for the released file without a successful reproducible build and recorded hash. Launchpad requirements and matching NeoForge Veil/GeckoLib/MidnightLib builds remain unverified; see DEPENDENCIES.md.

Run the test stages in TEST_MATRIX.md, starting with baseline rendering, then add AO's Embeddium/NeoOculus and shader stack one item at a time. Test Complementary Reimagined on the measured AO baseline; add Euphoria only as a separate follow-up condition. Do not start a fight until dedicated-server boot and entry are clean.

## Reproduction

1. Check out this experiment branch and read DEPENDENCIES.md and BUGS_AND_PATCHES.md.
2. Obtain a Java 21 runtime and Gradle wrapper distribution, then build a clean 1.0.0 release instance and a separate source 2.0.0 build.
3. Record hashes for every downloaded jar and the complete instance manifest before launching.
4. Run each row in TEST_MATRIX.md on disposable worlds; keep logs and screenshots only for tests that actually ran.
5. Update each status row with the exact result before any pack integration decision.
