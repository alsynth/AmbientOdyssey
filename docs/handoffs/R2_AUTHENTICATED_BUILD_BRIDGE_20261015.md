# Ambient Odyssey — R2 authenticated asset bridge (practical next build route)
Date: 2026-10-15. This is a **build preparation recipe**, not R3 gameplay verification or deployment.

## What is available now
- Source: PR #63, `experimental/master-integration-20261015`; existing `tools/package_master_integration.py`, `tools/validate_master_integration.py`, and `tools/build_r2.py`.
- Authenticated draft release: ID **413478281**, tag `experimental-master-integration-r2-20261015`, main asset ID **642899990**. Its R2 import ZIP is **154,492,540 bytes**, SHA256 **db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617**.
- R2 import has **337 CurseForge refs**, **10 bundled custom addon JARs**. It is NOT an offline collection of 330 official mod JARs, and it does not need to be to import through CurseForge. Importing into CurseForge fetches those references.
- R2 verification: clean source compilation and archive/static checks recorded. **No R2 Minecraft runtime / two-player Lootr / natural FTF arena acceptance.**

## ONE COMMAND after GitHub sign-in
On the owner's **Windows PC** with Python 3.10+ and GitHub CLI installed:

```powershell
gh auth login
git clone https://github.com/alsynth/AmbientOdyssey.git
cd AmbientOdyssey
git fetch origin experimental/master-integration-20261015
git checkout experimental/master-integration-20261015
python tools/prepare_r2_local_inputs.py --out-dir build/r2-inputs
```

The script authenticates through GitHub CLI to download the exact private asset, then enforces SHA256, expected archive size, ZIP CRC, 337 distinct CF references, SkyArena removal, NeoForge 21.1.252, and 10 nested custom JAR checks. Generates `build/r2-inputs/R2-INPUTS-VERIFIED.json`. **Do not commit the downloaded 154.5 MB binary into Git.** No auth token or private data is written to the report.

If GitHub's release-asset API responds with metadata instead of binary in a particular CLI version, or if `gh` is missing, use a **logged-in browser** to download the R2 ZIP into `C:\AO-Inputs\` and run:

```powershell
python tools/prepare_r2_local_inputs.py --local "C:\AO-Inputs\Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip" --out-dir build/r2-inputs
```

The script still enforces the exact same hash and archive checks. For private GitHub auth, **do not supply Claude with a GitHub token**; supply only the R2 ZIP, its verified inventory, and relevant source/code patches.

## Exact usage for a future R3 build
1. Freeze the **R2 ZIP as immutable binary input**. Keep source revision used to build R2 (documented in `docs/handoffs/r2-package-20261015/README.md`) separate from newer experimental PR63 HEAD. Don't claim latest code is inside R2 until rebuilt.
2. Claude/Work mode implements only verified owner-approved missing integrations on a new draft branch; record exact source HEAD, changed resource paths, hashes and distinct compiled addon classes. No need to redownload 330 official CurseForge JARs into the builder.
3. If changing `ao-campaign`, `ao-starter-chest` or `ao-augmenting-sigils`, compile Java against actual NeoForge/Apotheosis dependencies (Java 21), **replace** prior addon JAR in new import rather than stacking two versions. Can't mark source edits as compiled just because the old R2 JAR exists.
4. The existing R2 `tools/package_master_integration.py` is **PR50-base hash-gated**, NOT an R2-to-R3 delta packager. Either produce a reviewed R2-based delta builder that verifies original R2 sha and all paths, or build from exact PR50 base using existing packager. Do NOT casually feed R2 to `tools/build_r2.py --base`: its PR50 hash gate correctly rejects it.
5. Keep 337 CF pins, 10 custom JARs unless explicitly approved otherwise, all unrelated ZIP members byte-preserved, native loot additive-only, and no resurrected SkyArena; package R3 under a **different filename** and new draft release. Include rollback ZIP and changed member SHA256 receipt. Static passes do not imply gameplay passes.
6. Only then import R3 to a NEW CurseForge profile on owner's PC, test base world and multiplayer/dedicated server, and freeze generation-sensitive content before Chunky.

## R3 source design gaps (do not fill by guessing)
- Broad Regalia target remains incomplete (R2 generated only 9 item IDs); preserve all Enigmatic and Pasterdream accessory native-only exclusions, and the separate **Simply Swords unique-weapon** pool (owner's later correction supersedes early all-swords request).
- T3+ 5% native **best-pool** Grand Treasure modifier has 14 source-derived candidates; verify actual 'best pool' mapping and no replacement/recursive or Lootr reopens. T2 Scrap/Treasure increase still lacks numeric approvals and source-by-source mapping.
- Some boss identities/config routes remain unresolved; Cornelia T6 category with T7 combat treatment unimplemented in native config. R2 status/README documents this and T9 loot deferred.
- R2 70/30 Brutal Bosses x4 HP/x3 damage and 23 verified-scope DD Overworld zones remain correct, pending in-game confirmation.
- The previously approved boss rarity rates: T6 Ancient20%/Artifact2%, T7 Ancient25%/Artifact8%/Heirloom5%, T8 Ancient30%/Artifact15%/Heirloom8%/Esoteric5%. Extra high rarity affixed items are not gems; native Apotheosis gems and apex crafting unchanged.

## Cross-references
- `docs/handoffs/r2-package-20261015/README.md`
- `docs/handoffs/CLAUDE_COMPLETE_IMPORT_ZIP_HANDOFF_20261015.md`
- `docs/handoffs/R2_INTAKE_VERIFICATION_20261015.md`
- `docs/handoffs/LOOT_ADDITIVE_ONLY_VERIFICATION_GATE_20261015.md`

**No release downloaded, R3 archive assembled or runtime test conducted by authoring this handoff.** The downloader is not validated against the private binary until run by the authenticated owner; manual download is a supported fallback.
