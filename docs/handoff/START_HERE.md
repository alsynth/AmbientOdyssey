# Ambient Odyssey — external-agent package

**Handoff prepared:** 9 October 2026. **Game:** Minecraft 1.21.1. **Loader:** NeoForge 21.1.252. **Current focus:** Structure Test 6, followed separately by biome/terrain Test 7.

## Which version is current?

**Current verified *static* working snapshot:** `01_Current_Audit1/Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip`.
It supersedes the older Test 5 source *for new changes*, but is NOT an in-game-approved release. It includes additional audited-source fixes and reports; it intentionally does not include the eight pending structure mods. Its packaged CurseForge import is included for comparison, not as a fresh-world gameplay pass.

**Untouched rollback / original Test 5:** both pristine archives in `02_Original_Test5_Baseline/`. Do not edit or overwrite them.

**Your executable job:** implement `01_TEST6_IMPLEMENTATION_BRIEF.md` ON TOP OF the audit1 editable source, respecting `02_POST_HANDOFF_DECISIONS.md` and `03_TEST7_BIOME_QUEUE.md`. Do not redo audited, statically completed fixes. Source first; generated Paxi/datapacks and CurseForge export next. Deliver import ZIP + source ZIP + changelog + validation + hashes.

**Fastest path:**
1. Open `01_Current_Audit1/*sources*.zip`; extract to a new working folder. Keep its original bytes untouched.
2. Run `python --version`, `python build_release_030.py`, the continuation validator and clean reproducibility checks. See `04_BUILD_AND_VERIFY.md`.
3. Read `03_Reference/TODO.md`, `STRUCTURE_BIOME_AUDIT.md`, `STRUCTURE_TEST5_CHANGELOG.md`, `SOURCE_CHANGES.csv`, `APPROVED_STRUCTURE_ADDITIONS.csv`, and the CSV audits.
4. Acquire/inspect the eight **unbundled** approved mod JARs, checking exact dependencies and 1.21.1 NeoForge before touching manifest/source. Never silently omit a blocked mod.
5. Implement Test 6 (including the *new* Mushroom Village decision), run static validation, package, report what is and is not runtime tested.
6. Prepare, but DO NOT prematurely apply, the Test 7 biome additions or terrain changes.

## Package arrangement
- `00_Instructions/`: reconciled execution specification; original handoff preserved separately.
- `01_Current_Audit1/`: latest statically validated source, its known compiled import, supporting evidence; JAR-free.
- `02_Original_Test5_Baseline/`: unchanged baseline source/import/support for rollback and source-to-export comparison.
- `03_Reference/`: convenient extracted, editable-readable copies of the current reports, CSVs, native biome roster and compatibility configuration. Authoritative generated reports are also inside the source ZIP.

## Boundaries and honesty
- No third-party original JARs have been bundled. None of the third-party JAR binaries were edited by this handoff.
- The latest static reports claim expanded audit scope, not a successful gameplay test. See `release-validation-summary.json` for exact scoped gate counts.
- Original Test 5 runtime evidence says Minecraft loaded and a Heavenly Challenger locate worked; that is NOT a clean new-world density/performance pass for audit1 or Test 6.
- The handoff author has packaged supplied files and verified archive integrity, **not executed a Minecraft client/server acceptance run**.
- **Blockers:** eight new binaries/dependency closure; 41 unavailable original-profile JARs; some native tag/resource priority and unrepaired IDAS references; Archaion/AAA Particles compatibility; untested natural generation.
