# Repository map — current Ambient Odyssey development

Use this guide instead of reconstructing "what's current" from hundreds of filenames.

| Directory / file | Role | Maintenance action |
| --- | --- | --- |
| `README.md` | Single fresh entry point | Update when active candidate changes |
| `AGENTS.md` | Short AI/dev execution constraints | Keep current only; historical notes archived |
| `TODO.md` | Detailed rolling backlog (historical entries included) | Check latest bottom section before planning |
| `release_030/` | **Authoritative Minecraft source tree** for every override/config, datapack, pinned manifest source, FTB/Questlog | Do not rename without migrating build/test scripts |
| `Ambient-Odyssey-v0.2.10.zip` | Historical manifest baseline used by `build_release_030.py` | **Must stay at root** |
| `build_release_030.py` | Current locked 331-reference modpack exporter | Run explicit --private-modrinth vs reference-only modes |
| Root `compile_*.py`, `validate_*.py` | Original Worldgen Test 5/6/8 build chain used by v0.4h | Keep paths stable; many imports are by module name |
| Root `*.csv`, `*.md` historical reports | Legacy audit inputs, source catalogs and exact documents deliberately included in ZIPs | Do not casually move: some are referenced by validators or appended as overrides |
| `tools/`, `tests/` | Current preflight, synthetic auditor and Q1/FTB validators | Put **new** tools here rather than adding more root scripts |
| `docs/status/` | Short current status and active agent checklist | Archive previous verbose status before rewriting |
| `docs/questing/` | 50 Questlog Q1, 32 FTB Manual references, future campaigns and QA | See README and admin guide |
| `docs/testing/` | First-run field sheet, performance/ambience/worldgen acceptance | Treat static checks separately from game runs |
| `docs/audits/` | Research, mod lists, biome/structure catalogs and optional proposals | Historical evidence, not automatic inclusion |
| `docs/handoff/`, `docs/patches/` | Original Structure Test 6 handoff/patches | **Historical**; don't apply blindly |
| `docs/archive/` | Previous full status copies, bootstrap and archive manifest | Retained; nothing silently erased |
| `.github/workflows/` | Six v0.4-era workflows plus the repo-organization validator | Current active sources only |
| `.github/workflows-archive/2026-10-10/` | **30 historical single-use actions** (retained byte-exact) | Restore to workflow root only if knowingly re-running old one-shot testing |

## Current package summary

Minecraft 1.21.1 / NeoForge 21.1.252. 331 exact CurseForge refs, Mine Cells through Fabric Connector, 50 Questlog Q1 entries (13 tabs), 32 FTB Manual pages (3 chapters) plus WDA. [Verified source workflow](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259) with [artifact](https://github.com/alsynth/AmbientOdyssey/actions/runs/38080830259/artifacts/11680318532), actual full client/server gameplay **NOT TESTED**.

## Safe release check

```bash
python tools/validate_v04_quest_campaign.py
python tools/validate_v04_ftb_manual.py
python tools/validate_v04_fg.py
python tools/validate_v04_questlog.py
python build_release_030.py --output build/test-reference-only.zip
python tools/validate_v04_release.py build/test-reference-only.zip
python tools/preflight_v04.py build/test-reference-only.zip --require-minecells
```

The build may take several minutes and requires pinned source data; for the optional private ZIP the builder also fetches one exact SHA512-pinned third-party JAR. Source/ZIP PASS is not a gameplay pass.

## Archiving policy

Archive and rewrite **guides, statuses and one-time CI workflow declarations**, not the working executable build chain, worldgen assets or release inputs. The [machine-readable archive manifest](../archive/ARCHIVE_MANIFEST.json) stores every original file path and blob SHA. Previous full history is accessible in Git regardless of branch state. The branch `maintenance/repo-organization-20261010` is an **optional housekeeping candidate**, not a new release.
