# Ambient Odyssey — Structure Test 5 audit1 sources

This continuation repairs the audited existing stack and stages the eight master-approved structure additions for binary review. Minecraft is 1.21.1, NeoForge 21.1.252; the 237 locked project/file pairs are unchanged. Gameplay acceptance and 0.4.0 promotion remain pending.

Python 3.10+ and its standard library are sufficient; the verified build uses Python 3.12.14. No network resolution or installed JARs are required to rebuild the included baseline and overrides.

```bash
python3 build_release_030.py
python3 validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report validation.json
python3 write_structure_audit.py
python3 write_mod_screening_031.py
python3 package_structure_test5.py --output-dir ../delivery
```

The package command performs a clean source-ZIP extraction/rebuild, repeats the export gates, verifies deterministic report/catalogue regeneration, and writes import/source/support ZIPs, standalone reports, detailed summary and SHA256SUMS. Build output and caches are excluded from the source ZIP. Original Test 5 rollback hashes are in `release_030/evidence/baseline-reproduction.json`.

| Editable input | Generated content |
|---|---|
| `release_030/structure-density.json` | Placement configs, native-set members, six AO grids, three Heavenly clones, disable/exclusion tags and 20 Farmers placements |
| `release_030/structure-compatibility.json` | 145 provider/sky/optional tag patches, direct CTOV/Rustic selectors and slot repairs |
| `release_030/structure-repairs.json` | Eight asset-backed pools, recipes, entity tags, loot-modifier alias, native NBT migration and 33 client models |
| `release_030/native-template-inputs/` | Exact native Waystones template used by the migration; hash/provenance recorded |
| `release_030/approved-structure-additions.json` | Eight staged metadata pins; disabled, binary/dependency audit pending; does not modify the manifest |
| `release_030/biome-roster.json` / `biome-pools.json` | Preserved 40 OW + 2 Nether roster and existing Biolith settings |
| `release_030/release-lock.json` / `overrides/` | Locked manifest decisions and retained native configs/assets |

The four compilers clear their owned generated directories before rebuilding. Change the authoring inputs, not just generated data. Paxi datapacks use format 48; the new client repair resource pack uses format 34. Existing terrain, Streams, Tan, TRMT, options, keybinds and quests are preserved.

The expanded evidence represents 196 complete-binary resource audits, with 26 binaries directly available for this continuation's class/resource screen. Forty-one existing-profile JARs remain unavailable. `MISSING_JARS.txt` gives exact filenames; `APPROVED_ADDITION_JARS.txt` lists the separate eight additions. Those eight are not installed and Explorify's Black Spiral remains blocked on its exact native audit.

`audit_continuation_031.py --jars PATH` refreshes the continuation evidence from complete supplied binaries; `audit_jars_031.py`, `inspect_class_031.py` and `nbt_audit_031.py` support resource, class and template inspection. Evidence regeneration is offline after a binary refresh. Third-party JARs are not redistributed.

Read TODO, the changelog, audit, screening, validation and installation documents for the exact implementation and limits. The baseline evidence preserves original documents with original counts; current root documents describe audit1. The Tan open-field plan is staged and unapplied.
