# Source vs R4 config parity — 15 October 2026

**Result:** No real content difference remains. The 30 content-differing files (plus 2 that differ only in line endings) are 15 build-generated Mine Cells recipes, now synced into source, and 17 files that mods rewrite at load, now documented and ignored. A rebuild with R4's own packager matches R4 in content. The only byte differences left are 109 CRLF-vs-LF line endings from the R4 build machine's checkout.

Status: **SOURCE IMPLEMENTED + STATIC TEST PASS** (parity tool and unit tests). The rebuild is a local parity check only; it is not a release.

## Inputs
- R4 ZIP SHA256 `31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d`.
- PR50 base ZIP (the packager's `--base`) SHA256 `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f` = R4 receipt `base_sha256`.
- The installed JARs match R4's 337 pins. Mine Cells `minecells-2.0.3.jar` SHA256 `194b2318…2481` = the generator's pin.

## Key fact
For all 32 files, **R4 bytes == PR50 base bytes**. `tools/package_master_integration.py` takes them from the base ZIP, not from `release_030/overrides`. So the source copies were stale, while the package was right.

## Classification
| Class | Count | Files | Action |
|---|---:|---|---|
| Build-generated | 15 | `config/paxi/datapacks/ao_v041_runtime_fixes/data/minecells/recipe/compat/{create,farmersdelight}/…` | Synced into source. These are `tools/generate_v042_minecells_recipes.py` output: run against the pinned JAR, it yields bytes identical to R4 for all 15. The source held `neoforge:false` stubs (generator added in `5439f09`, output never committed; the generator's own `--check` mode expects it committed). |
| Rewritten by a mod at load | 17 | see `release_030/MOD_REWRITTEN_CONFIGS.json` | Documented and ignored by the parity check. Each one differs only in formatting, key order or line endings, or by added default keys / installed-mod entries; no source value changes. |
| Real change | 0 | — | — |

**Moog's (`config/moogs_structures.json`):** `MoogsStructureLib-neoforge-1.21.1-3.4.2.jar` → `com/finndog/moogs_structures/config/MslConfig.class` contains `loadAndSync`, `writeFile`, `GsonBuilder.setPrettyPrinting`, `toJson`, `newBufferedWriter`. It reads the file and writes it back with Gson. Parsed source and R4 are identical; only key order and `1` → `1.0` changed.

**Shader preset (`shaderpacks/AO Balanced.txt`):** the 10 keys absent in R4 all hold the shader's default (`SHADOW_QUALITY=2`, `SSAO_QUALI_DEFINE=2`, …), checked against the bundled shader `#define`s. Iris omits defaults on save, and Euphoria Patcher adds 2 header keys, so the effective settings are identical.

## Results (`tools/check_source_r4_parity.py`)
| Comparison | Equal | Line endings only | Documented mod-rewritten | Real |
|---|---:|---:|---:|---:|
| `release_030/overrides` vs R4 (shared paths) | 1,215 | 2 | 15 | **0** |
| Rebuild (packager + PR50 base + R4's 3 addon JARs) vs R4 | 5,290 | 109 | 0 | **0** |

The 109 line-ending-only members are 108 Questlog files and `AO_TEST_NOTES/NATIVE_BALANCE_LEDGER.json`. R4 has CRLF; source is LF, enforced by `.gitattributes` `*.json text eol=lf`. R4 was built from a Windows checkout that converted them. Rebuild SHA256 `5cff6947…b72a`, identical before and after the sync, because the packager reads these 32 files from the base ZIP.

Limits:
- The rebuild used R4's released starter/Sigils/campaign JARs, copied into `addons/*/build/libs` and left uncommitted (git-ignored). There's no Gradle here, so they could not be recompiled.
- Not engine- or multiplayer-tested: config bytes only.

## Rollback
`git revert <this commit>` restores the 15 stub files and removes the manifest, tool, test and this doc. R4 and the PR50 base are untouched.

## Remaining
- Decide whether future builds should normalize Questlog JSON line endings. Functionally irrelevant; it only matters for byte-identical rebuilds.
- `generate_v042_minecells_recipes.py --check` downloads the JAR from the CurseForge CDN. It wasn't run here; the equivalent offline comparison against the pinned installed JAR passed 15/15.
