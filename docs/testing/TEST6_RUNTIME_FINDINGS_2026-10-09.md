# Structure Test 6 — first live runtime log and blocking failure

**Date:** 2026-10-09. **Evidence:** User-supplied first CurseForge client launch log `latest(20261009-194515).log` (full log supplied in conversation; NOT committed because it contains local account/location and launcher details). The selected Test 6 source candidate is `structure/test6`. This result is **RUNTIME TESTED: FAIL AT CLIENT PRE-LOAD**. It is not fresh-world/gameplay acceptance.

## Runtime environment

- Minecraft `1.21.1`; NeoForge `21.1.252`; Eclipse Adoptium Java `21.0.9`; Windows 11.
- User imported the released Test 6 **candidate** whose historical profile/internal version is still `0.3.1-structure-test5-audit1`.
- Relevant new files reached the mod discovery stage: AAA Particles 2.3.3, Archaion 1.4.4, YUNG's Bridges/Extras, Create: Structures Arise, Create: Easy Structures, Additional Structures, Explorify 1.6.5, plus others. **Discovery is not proof they all initialize correctly.**
- Log begins at 21:43:58, critical failure at **21:44:19**. Did **not** reach a menu or a world.

## Fatal problem — CONFIRMED

```text
[21:44:19] [Render thread/FATAL] Error during pre-loading phase:
File mods\Structory_Towers_26.2_v1.0.17.jar is not a valid mod file
net.neoforged.neoforgespi.locating.InvalidModFileException:
Missing ModLoader in file (Structory_Towers_26.2_v1.0.17.jar)
```

This was **user-approved v1.0.17** in the manifest, but the approval was conditional on a successful NeoForge 1.21.1 load. The static manifest/version override `783522:8396885` cannot make an invalid native mod descriptor load. Upstream issue describes **exact same file and exception** on NeoForge 1.21.1: https://github.com/Stardust-Labs-MC/Structory-Towers/issues/8 .

**Next diagnostic test (not yet done):** on a *disposable CurseForge Test 6 profile only*, replace v1.0.17 with **Structory: Towers 1.0.14, CurseForge project:file `783522:7078283`**, https://www.curseforge.com/minecraft/mc-mods/structory-towers/files/7078283 . CurseForge lists this file as compatible with MC 1.21.1 and NeoForge. Do not retain **both** versions. If loader succeeds, test actually entering a fresh world. If it fails, capture the new `latest.log`, exact filename and failure; do not assume fallback success until observed.

**Before permanent source/CurseForge release changes:** once the fallback is proven, change the authoritative `release_030/release-lock.json`, the `release_030/approved-structure-additions.json`, screening catalogue, pinned-version validators and any derived metadata, rerun both static suites and clean builds. Clearly record a new test-candidate hash. **Do not merely swap the local JAR and call the exported ZIP fixed.**

## Other log output — NOT YET ROOT CAUSED

- Following the invalid-mod error, the client emitted `Cowardly refusing to send event ... to a broken mod state`, then a Quark/Zeta rendering initialization exception (`Where is minecraft???`). This is plausibly **downstream of the already broken mod-loading state**; only diagnose Quark independently if it recurs once the invalid Structory JAR is removed/replaced.
- One Paxi duplicate-pack source warning and many `missing refmap`/`optional Mixin target not found` lines are present; none in this log supersedes the explicit NeoForge pre-load FATAL.
- No proof yet of worldgen, addon biome registration, actual structures, performance or Nether compatibility.

## Status and required follow-up

- [x] Identified startup blocker from actual user log.
- [x] Confirmed upstream report of same v1.0.17 loader failure.
- [ ] Test v1.0.14 alone in disposable test profile; record resulting log.
- [ ] If successful, repin, regenerate derived audits/validators, rebuild and re-validate stable Test 6 candidate.
- [ ] Reach main menu/fresh world, then proceed with `docs/testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md`.
- [ ] Test actual natural worldgen, dimensions, biome parity, overlaps and performance.

Keep `main` Test 5 baseline unchanged; don't start Test 7 worldgen work before this gate passes.
