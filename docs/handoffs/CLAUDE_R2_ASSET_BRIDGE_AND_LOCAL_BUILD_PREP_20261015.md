# AO — Claude R2 asset bridge and final-import prep (15 October 2026)
Status: actionable file-transfer and validation handoff, not a deployment or claim that later changes are already packaged.

## Confirmed via authenticated GitHub release metadata
**R2 exists**, newer than R1; available in repository's private draft release:
- Release ID: **413478281**; API `https://api.github.com/repos/alsynth/AmbientOdyssey/releases/413478281`
- Browser page: `https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-28508fbadd878b4afd7d` (draft requires owner access).
- Main asset: `Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip`
- GitHub-reported size: **154,492,540 bytes**
- Recorded SHA256 in branch docs: **db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617** (verify against downloaded bytes).
- Asset ID **642899990**; release also contains rollback ZIP, output ZIP report JSON, R2 README, dependency and static verification JSON.
- Companion source branch `experimental/master-integration-20261015`; read `docs/handoffs/r2-package-20261015/README.md`, `docs/handoffs/R2_INTAKE_VERIFICATION_20261015.md`, `docs/handoffs/R2_BUILD_STATUS_20261015.md`, and `docs/handoffs/CLAUDE_COMPLETE_IMPORT_ZIP_HANDOFF_20261015.md`.
- R2 receipt says 337 CurseForge references (330 official mods + 7 resource/shader references), 10 embedded compiled custom addon JARs, expected 340 total mod JARs after CurseForge downloads. The import ZIP need NOT include the 330 official mods.

## What Claude actually needs from owner (minimal)
1. **Download the R2 main ZIP** while signed into GitHub from the private release. Verify the exact expected SHA256 locally. Do not use the earlier R1 or the R2 rollback ZIP as the build base.
2. Supply Claude **the R2 main ZIP**, either as a direct attachment or via a private authenticated transfer that Claude can read. Supply `R2-README-TESTS-AND-ROLLBACK.md` and `Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip.report.json` if useful. Avoid sharing any GitHub token with Claude.
3. For the source changes, Claude can clone/receive the accessible source branch; if its environment cannot push to GitHub, deliver a **git format-patch series or unified diff plus changed source archive** to the owner, who applies/pushes it from an authenticated computer or sends it to an agent with GitHub connector write access. Preserve source commit SHAs.
4. The ten compiled custom JARs are already embedded at `overrides/mods/*.jar` in the R2 import ZIP. If a future rebuild is needed, retain source/compiled identity and Gradle dependencies; do not rebuild identical addons gratuitously. No need to obtain ~330 CurseForge downloads in Claude's sandbox merely to assemble a standard CurseForge import ZIP.
5. If Claude's environment cannot fetch **NeoForge/Apotheosis Maven dependencies**, compile the addon changes on the owner's PC (with Java 21, Gradle cache/build tool) and supply just the newly compiled JAR(s), or use GitHub Actions with an authenticated workflow run. A source-only patch is not a complete updated import if its new addon code remains uncompiled.
6. **Do not assume any currently installed client version equals R2.** Owner imports/test as NEW disposable CurseForge profile and keeps stable profile untouched.

## Owner-local download / validation — Windows
Open the authenticated draft release and download the R2 main ZIP into a new folder, e.g. `C:\AO-Inputs\`.

PowerShell SHA check:
```powershell
Get-FileHash -Algorithm SHA256 'C:\AO-Inputs\Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip'
```
Expected hash exactly `db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617`. A different hash is a HARD STOP: do not disable integrity checks and do not silently accept an older ZIP.

To inspect *without installing mods*:
```python
import json,zipfile,hashlib
p=r'C:\AO-Inputs\Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip'
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))
    manifest=json.loads(z.read('manifest.json'))
    refs=manifest['files']
    jars=[x for x in names if x.startswith('overrides/mods/') and x.endswith('.jar')]
    print('CF references:',len(refs),'Custom JARs:',len(jars))
    assert len(refs)==337 and len(jars)==10
    for jar in jars: print(jar,hashlib.sha256(z.read(jar)).hexdigest())
```

The R2 ZIP is import-ready **as an experimental test candidate**, not a fully approved production profile. Remaining blockers include: only 9 curated Regalia reward IDs vs broad owner intent, 14 heuristically mapped Grand Treasure contexts, no owner-approved T2 Scrap/Treasure exact rates, missing some named boss mappings and Cornelia damage/HP native implementation route, unproven multiplayer/Lootr and natural-FTF boss encounter behavior. Earlier R1 runtime results cannot validate R2.

## Practical final-import workflow
A. Use **the authenticated R2 ZIP as the last complete, hash-verified base** plus the latest source from the R2 integration branch. Audit the full contents and manifest before making updates. Compare against `docs/handoffs/CLAUDE_COMPLETE_IMPORT_ZIP_HANDOFF_20261015.md`; avoid older PR50 manifest assumptions (338 pins before SkyArena removal) and don't reintroduce SkyArena.
B. Apply *only* verified compatible approved new source/code/config changes, compile addon changes where necessary, ensure 337 manifest refs unless explicitly approved mod roster changes, replace older addon JAR paths instead of adding duplicates, and preserve all untouched native ZIP member content and hashes.
C. Generate a **new R3 experimental ZIP**, separate from R2, full SHA256/member manifest, deterministic change report, tests, rollback. Do not edit the existing R2 draft-release assets.
D. If no GitHub push/release auth is available, supply the R3 ZIP and code patch to owner; upload/push from the authenticated owner computer. If no binary release upload works, an on-PC packager script and source patch is acceptable as a **handoff**, but NOT equivalent to having finished the ZIP.
E. CurseForge client imports manifest references itself. Validate in a separate fresh profile, two-player Lootr, native chest contents, boss kills, addons, worldgen, restart and server side before any permanent Chunky pregeneration.

**No assets were downloaded or R3 built by this documentation update.** File and release existence were checked from authenticated GitHub release metadata; R2 SHA comes from the committed R2 package README, not an independent download hash verification.
