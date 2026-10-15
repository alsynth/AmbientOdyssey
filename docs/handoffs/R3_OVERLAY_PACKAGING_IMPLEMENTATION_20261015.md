# Ambient Odyssey — R2→R3 local packaging pipeline
**15 Oct 2026 | experimental source / static tests only | R2 untouched**

## What this prepares
A **real executable local packager**, not just a roadmap. The verified R2 full import is already available as a **private draft release**, ID 413478281, asset 642899990, with 337 CF pins and 10 custom addon JARs. The full official CurseForge mod JAR collection is not needed inside the new import ZIP.

Added to PR #63 source branch:
- `tools/prepare_r2_local_inputs.py` — retrieve and SHA256-check the private R2 archive with the owner's GitHub login, or validate a browser-downloaded copy.
- `tools/draft_r3_change_plan.py` — generate an audit-ready changeset from a folder of compiled/new `overrides/**` files. Each generated reason is blank and must be filled after review.
- `tools/package_r3_from_r2.py` — assemble a NEW R3 full import ZIP directly from pinned R2, keeping untouched member bytes identical; produce separate rollback ZIP and change receipt.
- `tests/test_package_r3_from_r2.py` — synthetic safety/regression cases.
- `.github/workflows/ao-r3-overlay-preflight.yml` — CI syntax and synthetic test gate (CI results not independently confirmed in this note).

## Exact local workflow
On an authorized PC with Python 3.11+ and GitHub CLI authenticated, checkout `experimental/master-integration-20261015`.

**1. Retrieve R2** (or use `--local <downloaded-R2.zip>`):
```powershell
python tools/prepare_r2_local_inputs.py --out-dir build/r2-inputs
```
Verified input `build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip`: expected SHA256 `db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617`.

**2. Compile the changed addons** using correct Java 21/NeoForge/Apotheosis dependencies and place **only new/changed** files beneath `build/r3-overlay/overrides/...`. The overlay mirrors the eventual import ZIP internal paths, e.g. `build/r3-overlay/overrides/mods/ao-campaign-0.4.0-experimental.jar`. A renamed addon **must** have its old R2 JAR explicitly removed, otherwise duplicate mod IDs are rejected.

**3. Draft a changeset, including explicit old addon removal if renaming**:
```powershell
python tools/draft_r3_change_plan.py --base "build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip" --overlay build/r3-overlay --remove "overrides/mods/ao-campaign-0.3.0-experimental.jar" --out build/r3-plan.json
```
Omit `--remove` if the updated JAR is replacing the old filename directly. The generator does not infer removals. Inspect every proposed change, enter a meaningful top-level `reason` and a meaningful individual `reason` for **each** change. No auto-approval of unknown loot or mods.

Example `r3-plan.json` shape (SHA placeholders are illustrative; use generated real SHA values):
```json
{
  "format": "ao-r2-to-r3-1",
  "reason": "Owner-approved R3 experimental changes; validated each path",
  "changes": [
    {
      "action": "replace",
      "path": "overrides/config/some-owner-approved-file.json",
      "old_sha256": "<verified prior SHA256>",
      "new_sha256": "<sha256 of overlay bytes>",
      "reason": "Exact approved configuration change"
    }
  ]
}
```

**4. Build R3** after review:
```powershell
python tools/package_r3_from_r2.py --base "build/r2-inputs/Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip" --overlay build/r3-overlay --plan build/r3-plan.json --output build/Ambient-Odyssey-MASTER-INTEGRATION-R3-PRIVATE.zip
```
Output:
- `build/Ambient-Odyssey-MASTER-INTEGRATION-R3-PRIVATE.zip` — new full CurseForge import.
- `...-Rollback.zip` — changed original R2 member bytes + removal receipt; **not an import**.
- `...zip.report.json` — before/after hashes, R3 ZIP hash, addon fingerprints and static-only status.

## Enforced safety rules
- Exact R2 SHA check. Never feed R2 into the historical `tools/build_r2.py --base`, which is pinned to PR50.
- Existing ZIP, rollback ZIP, and report files are never overwritten.
- Explicit per-file old and new SHA and reason: additions cannot shadow an existing member; replacements/removals must match expected old hash; path traversal forbidden.
- Original CurseForge manifest's 337 file references and 10 bundled custom addon count must remain unchanged unless a separately reviewed packager upgrade is made.
- Duplicate bundled NeoForge/Fabric mod IDs rejected. Changed/new JARs have their native-loot table overrides checked; unknown foreign/native loot namespace table injection rejected. Existing R2 JAR bytes preserved.
- New `data/minecraft`, `data/apotheosis`, other **foreign-native** loot table replacements and native Apotheosis modifier edits are blocked by default. `global_loot_modifiers.json` must explicitly have `replace:false` with no duplicate entries.
- These checks **do NOT prove** all addon Java behavior is additive. Existing native loot must still be proven preserved by source diff, effective datapack order, integrated tests and actual two-player Lootr chest openings.

## Actual verification / restrictions
The packager's locally staged Python prototype passed **10 synthetic tests**: valid additive ZIP/rollback, wrong base hash, old/new member hash failures, duplicate addon IDs, foreign-namespace addon loot replacement, forbidden native loot path, `replace:true` global modifier, unsafe paths, and output collision. GitHub CI run status is not claimed here.

**NOT DONE:** downloading private R2 bytes to the local test container, executing the packager on the actual 154.5MB import, assembling R3 using compiled changed addons, integrated Minecraft test, two-player Lootr test, worldgen/arena validation, or server acceptance.

**Implementation dependencies:** R2 includes 14 heuristic Grand Treasure sources and only nine curated Regalia bonus IDs; the owner-approved wider Regalia effort and native source verification are separate work and must not be claimed solved by repackaging. T2 Scrap/Treasure amounts remain unapproved. Work Mode/Claude can prepare updated sources and compiled JARs without direct CurseForge mod downloads.
