> **Updated status, 9 October 2026:** Structure Test 6 source has now been committed to `structure/test6`. This file's original Audit1 instructions below describe historical preparation, **not the current next step**. For the current build use the commands below and [runtime acceptance checklist](../testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md). There is no need to extract a ChatGPT Library ZIP.

```powershell
# In a clean checkout of the structure/test6 branch (Python 3.10+):
py build_release_030.py
py validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test6-continuation.json
py validate_structure_test6.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test6-focused.json
```

**Scope:** 246 manifest projects; 247 continuation + 35 focused static checks. Build hash evidence: `docs/status/TEST6_CANDIDATE_IMPORT.json`. Output filename is historical; test contents are Test 6. **No actual runtime acceptance yet**.

---

# Baseline reproduction, Test 6 build and validation

Audit1 scripts are stored at the root of its source ZIP. No external agent needs the original chat or ChatGPT Library to use them.

## Windows/Linux/Mac workflow (Python 3.10+)

1. Unzip `01_Current_Audit1/Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip` into a clean folder. Save a second untouched copy for hashes/rollback.
2. `python --version` / `python3 --version`.
3. `python build_release_030.py` — compare resulting archive to bundled `Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip` and audit1 summary SHA-256 BEFORE modifying source. Do not quietly assume the older Test 5 build script and current continuation have identical behavior.
4. `python validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report validation.json` (adjust `--archive` to the script's actual output path if needed).
5. `python write_structure_audit.py` and `python write_mod_screening_031.py` to regenerate catalogues, compare with packed report files.
6. Check SHA-256/CRC/safe unique paths and `manifest.json` at the *exact* import ZIP root. Compare project/loader pins, unmodified resource assets, baseline source differences and original audit1 import hash.
7. Branch the extracted working copy and implement Test 6 changes in source. Add regression gates for all eight additions, WDA major Overworld/End separation, Mushroom Village single rare Mushroom Fields route, Farmers already-tuned variants, Bathhouse and excluded structures.
8. Build again, validate, regenerate reports and clean-rebuild a second time for determinism. Deliver new source + import + changelog + validation + hashes.

## Current audit1 facts (reported by its included static validation)

Original Test 5 was rebuilt byte-for-byte and passed 76 original gates before audit1 was created. Audit1 reported 196 binary snapshots and 41 missing installed files, statically verified source/export consistency, and deterministic ZIP rebuilds. Audit1 **has not passed in-game acceptance**; file-content, native selectors and /locate evidence do not prove natural appearance or terrain fit. Exact scoped validator count is in `03_Reference/release-validation-summary.json`.

## Source-first principles

Preserve native ZIPs unchanged as rollback; never directly patch only the generated import. Keep dimension-specific definitions, unique salts and placement ownership. Do not include third-party mod binaries in the agent's final CurseForge import ZIP. Fetch external mods legitimately by project/file ID into the installation's manifest, verifying all dependencies.

## What NOT to claim

No Test 6 export has been created in this handoff. No new addon binary was downloaded, hashed, dependency-checked, installed or runtime-tested. No new Mushroom Village placement, WDA frequency change or Test 7 biome addition has been implemented by this package preparation step.
