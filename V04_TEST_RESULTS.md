# v0.4 experimental — verification and known issues

## What actually ran

Java 21.0.12.1, Minecraft 1.21.1, NeoForge 21.1.252 and only Mine Cells 2.0.3 + Connector beta.17 + FFAPI 2.3.5 + inherited NeoForge owo-lib ran on a loopback-only disposable dedicated server. The controlled first run reached `Done`, force-loaded chunks in all five Mine Cells dimensions, saved and stopped with exit 0. A second run loaded the saved world, saved and stopped with exit 0. No player joined; no client rendering, portal progression, boss fights or multiplayer gameplay was exercised.

Evidence: `docs/testing/v04-evidence/minecells-server-launch-1.txt`, `minecells-server-launch-2.txt`, `minecells-binary-audit.json`. Mojang session-key lookup was restricted and logged an HTTP error in this offline test; it did not prevent startup. This is not a test of online authentication.

## Static checks

- Active `structure/test6` built before edits: 265 references; SHA256 `2263aaf52223c86459312ee88f5c4d45d7e55520873f53760a5daf17e969646b`. Its historical continuation validator failed on post-Test5 configuration drift. This was reported before integration, not hidden as a pass.
- Merged 313-reference expansion built successfully before Mine Cells changes. All newer content and worldgen gate scripts passed before integration.
- v0.4 uses the same source-backed content/worldgen gates with an explicit candidate label/count, including the formerly b1-only validator's explicit later Galosphere removal. No unrelated native invariant is relaxed.
- Package validator checks exact bridge/library pins, 4 negative bridge regressions, no original Fabric API, ZIP CRC, unique/safe paths, root manifest, strict JSON, all 273 repaired NBT templates and exact private NeoReef hashes. Final results/hashes are recorded separately in `docs/testing/v04-evidence/release-validation.json` and the delivered checksums file.

## Dependency audit coverage

All 221 baseline and 104 current-addition file identities were resolved from exact CurseForge project/file metadata. At audit time, 282 of 305 selected native binary records could be inspected; 23 records remain unavailable or fail the strict Python TOML parser. This count excludes the separately inspected 3 Mine Cells/bridge files and 2 new library files. Details and hashes: `docs/testing/v04-evidence/dependency-audit.json`.

Native descriptors revealed required Iceberg and JamLib absent from the actual source manifest; both are now pinned. Illager Invasion's Extensible Enums dependency is bundled, so no redundant project was added. The four-mod Mine Cells runtime verifies its bundled Gimm1q/Fabric Loader dependency path. Missing audited mod IDs that correspond to unavailable selected binaries remain audit gaps, not proof the source manifest lacks them. Full-pack version and conflict closure cannot be certified until those exact files are inspected/installed and the complete pack launches.

## Remaining known issues

1. **Full AO v0.4 client and dedicated server untested.** Renderer/mixin interactions with the newly added FFAPI/Connector stack remain a release risk; automatic minimal-server success is insufficient.
2. **Worldgen is not frozen.** Natural distribution, terrain fit, bridge/Streams geometry, POI mismatches and ocean/Nether/End quality require the grouped acceptance run.
3. **Loot/content:** Iron's Jewelry developer loot table, legacy item IDs in native structures, optional Bumblezone trades, Patchouli/BetterEnd book, atlas/model/texture and GeckoLib animation warnings still need exact owner-backed repairs. Do not replace IDs globally or fabricate rewards.
4. **Gameplay:** Mine Cells portals, progression, respawn, bosses and multiplayer synchronization remain untested. Bonus Chest Lootr instancing remains unverified; no starter-loot redesign is shipped.
5. **Ambience/performance:** canopy audio behavior and Streams fast-terrain fallback remain unresolved. New distance defaults are configured but no measured full-pack speedup exists. Dedicated 5–7-player cold-generation performance remains untested.
6. **Expansion backlog:** quest/archaeology campaigns, comprehensive keybind overhaul, Origins/class integration, MCA Reborn, Big Globe and renderer/LOD experiments remain deferred. Research-only and ambiguous candidates were not silently installed.
7. **Distribution:** private developer ZIP contains NeoReefRedux; reference-only export omits it. CurseForge import installation/sidedness and public publication approval remain untested. Existing released branches and `main` are preserved.

Use `V04_TESTING_CHECKLIST.md` for one substantial test session. This is an experimental test candidate, not a fully accepted stable release.
