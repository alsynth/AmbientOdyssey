# Ambient Odyssey 0.3.1 Structure Test 5 sources

Run `python3 build_release_030.py` with Python 3.10 or newer. This builds `build/Ambient-Odyssey-v0.3.1-structure-test5.zip` from the included locked baseline and local overrides, without network resolution or installed mod JARs. The inherited script name and `release_030` directory are retained; `release_030/release-lock.json` selects Test 5. Mod project/file pins match Test 4.

Run `python3 validate_structure_test5.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5.zip` to repeat the scoped static gates using the included offline JAR snapshot and cached Test 4 reference. Use `--report PATH` for a JSON result. Optionally add `--test4 PATH` to compare directly with the original Test 4 export. Rebuilding twice should produce identical bytes; ZIP entries are sorted and use fixed metadata.

Edit the following source inputs before rebuilding:

| Input | Compiled content |
|---|---|
| `release_030/structure-density.json` | Placement configs, native-set membership overrides, six AO grids, three Heavenly clones, structure disable and exclusion tags |
| `release_030/structure-compatibility.json` | Provider biome-tag additions/replacements, sky selectors, native structure snapshots and Artifacts slot restorations |
| `compile_compatibility_031.py` and `release_030/biome-roster.json` | Shared climate/landform classifications and curated biome roster |
| `release_030/structure-repairs.json` | Four asset-backed template pools and Simply More recipe syntax repair |
| `release_030/biome-pools.json` | Existing Biolith replacement pools; unchanged in Test 5 |
| `release_030/overrides/` | Retained native configs and other assets |

The builder runs all four compilers automatically. Compiler-owned compatibility, density and repair data directories are regenerated from inputs, including removal of obsolete files. Do not edit their generated JSON alone.

`audit_jars_031.py`, `inspect_class_031.py` and `nbt_audit_031.py` support new JAR/resource, class and template audits. `python3 write_structure_audit.py` regenerates the report and three CSV catalogues from the included evidence. Raw third-party JARs are not redistributed in this source archive; the snapshot records resource provenance and JAR hashes.

Read `STRUCTURE_TEST5_CHANGELOG.md`, `STRUCTURE_BIOME_AUDIT.md`, `STRUCTURE_TEST5_VALIDATION.md` and `TODO.md` for the implemented changes and exact limits. The actual audit covers 177 complete JARs; 60 names from the supplied runtime remain unavailable after failed archive transfers. Static checks do not certify those JARs, a Minecraft registry load, real-world density or performance. No gameplay pass is claimed.

`STRUCTURE_TEST5_INSTALL.md` describes the import and later acceptance steps. `TANS_OPEN_FIELD_TUNING_PLAN.md` is staged only; Test 5 keeps the existing tree, terrain, climate and wildlife settings. Earlier numbered test documents are historical references.
