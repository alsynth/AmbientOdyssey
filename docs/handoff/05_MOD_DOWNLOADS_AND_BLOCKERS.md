# Test 6 pinned structure addons — CurseForge file pages and runtime checks

**Updated after verified Test 6 source import, 9 Oct 2026:** These files are **now pinned in `release_030/release-lock.json` and exported into the candidate CurseForge manifest** on `structure/test6`. They are NOT original JAR files inside Git, and have **not** passed client/server runtime acceptance. File pages are for download/compatibility checks, not further manifest editing.

| Mod | CurseForge project:file | Selected file page | Status |
|---|---:|---|---|
| YUNG's Extras | `1015146:5812546` | https://www.curseforge.com/minecraft/mc-mods/yungs-extras-neoforge/files/5812546 | Not bundled / binary unverified |
| YUNG's Bridges | `1015149:5812553` | https://www.curseforge.com/minecraft/mc-mods/yungs-bridges-neoforge/files/5812553 | Not bundled / binary unverified |
| Structory: Towers | `783522:8396885` | https://www.curseforge.com/minecraft/mc-mods/structory-towers/files/8396885 | **v1.0.17 user-approved**; requires actual NeoForge 1.21.1 load test / file compatibility exception |
| Archaion | `1620396:8983496` | https://www.curseforge.com/minecraft/mc-mods/archaion/files/8983496 | Inspect AAA Particles dependency |
| Explorify | `698309:8082824` | https://www.curseforge.com/minecraft/mc-mods/explorify/files/8082824 | **Black Spiral enabled with user approval**; fresh-Nether compatibility pending |
| Additional Structures | `297680:6584803` | https://www.curseforge.com/minecraft/mc-mods/additional-structures/files/6584803 | Not bundled / binary unverified |
| Create: Structures Arise | `1010066:8837992` | https://www.curseforge.com/minecraft/mc-mods/create-structures-arise/files/8837992 | Not bundled / binary unverified |
| Create: Easy Structures | `949158:6344382` | https://www.curseforge.com/minecraft/mc-mods/create-easy-structures/files/6344382 | Not bundled / binary unverified |

**AAA Particles:** Pinned as `979809:9101011` (v2.3.3) in the Test 6 manifest to support Archaion. Verify actual loader compatibility and resource behavior in game; do not replace this pin with a random 'latest' build.

**Historical IDs (not current):** Structory Towers `5800614`, `7078283`; Explorify `5482463`. The current user-approved pins supersede these. The static addon binary audit report is under `docs/audits/TEST6_ADDON_AUDIT.md`.

**Other missing files:** `03_Reference/MISSING_JARS.txt` lists 41 installed-profile JARs absent from full binary audit. That list is not permission to remove installed mods. Original mods need not be copied into this handoff; the recipient can acquire official files if a deeper audit is required.

**Next step:** [runtime acceptance checklist](../testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md). Full client/server import and natural generation remain unverified. Static audit hashes are documented, but original third-party JARs are not bundled.
