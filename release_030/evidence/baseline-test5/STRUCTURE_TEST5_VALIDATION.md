# Ambient Odyssey — Structure Test 5 static validation

8 October 2026 · Minecraft 1.21.1 · NeoForge 21.1.252.

**PASS for the scoped static gates and archive/source rebuild checks.** The validation is scoped to the available inputs and does not claim a Minecraft registry load or gameplay test. Actual checks can be rerun with `validate_structure_test5.py`; JAR coverage and unresolved references remain explicit in the audit report and TODO.

## Acceptance scope

- Actual resources from 177 complete, individually CRC-verified JARs; SHA-256/provenance snapshot included.
- 908 inspected native structure definitions, 584 native sets, 3,488 template pools and 1,094 biome-tag definitions.
- Three explicitly declared native-template Overworld clones; six independent AO placement sets.
- Generated JSON, biome/structure references, placement bounds/weights/salts, ownership, disabled structures, dimension separation, pool evidence and slot/recipe repairs.
- Exact correspondence between compiled source overrides and the import export; preservation of 601 unrelated Test 4 config/assets; unchanged 237 locked mod project/file pairs.
- ZIP CRC, safe unique paths, root CurseForge manifest, game/loader/version pins, source archive rebuild and deterministic output.

## Final results

| Check | Result |
|---|---|
| Scoped source and export validation | 76/76 gates pass |
| Compiler-generated JSON | 263 strict JSON files parse; compiler-owned packs use format 48 |
| Python source syntax | All included scripts parse |
| Added modded biome IDs | Present in actual inspected registry JSON resources |
| Added set references | Inspected native structure IDs or three declared native-template AO clones |
| Nested added tags, placement bounds, weights and salts | Pass |
| Small Blimp/Coliseum | No membership in any inspected effective set; native toggles false and generation safeguard tag present |
| Bathhouse and new ordinary/sky groups | One placement owner each; obsolete AO grids absent |
| Sky Villages | Land + all four explicit river/Streams biome IDs; no ocean selectors |
| Heavenly dimension split | AO clones exclude End/Nether; original WDA trio uses End-only selector |
| Pool repairs | Four nonempty pools; every native template has connector provenance, 33 templates total |
| Artifacts and Simply More | Native slot memberships restored; valid recipe override compiled |
| Unrelated Test 4 config/assets | 601 retained assets match Test 4 SHA-256/direct bytes |
| Mod pins and game/loader | 237 project/file pairs match Test 4; Minecraft 1.21.1 / NeoForge 21.1.252 |
| Import archive | CRC pass; 915 unique safe file paths; root manifest; no bundled mod JARs |
| Source archive | CRC pass; unique safe paths; required inputs/scripts and locked baseline included |
| Compiled source/export correspondence | Every source override and current supporting document matches the import ZIP |
| Clean source-archive rebuild | Byte-for-byte identical import ZIP, with all 76 gates passing again |
| Audit report/catalogue regeneration | Byte-for-byte identical report and three CSVs using cached offline evidence |

Detailed gate results are in `release_030/evidence/static-validation-structure-test5.json`. `release-validation-summary.json` records final archive sizes, member counts, hashes and clean-rebuild outcomes. `SHA256SUMS.txt` covers the final deliverables. These two files accompany the delivery and are included in the supporting-files ZIP; archive hashes are not embedded in the source/import archives they describe.

## Reproduce

Extract the source archive into a clean directory. Python 3.10+ and its standard library are sufficient; no external Python packages or network resolution are required.

```bash
python3 build_release_030.py
python3 validate_structure_test5.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5.zip --report validation.json
python3 write_structure_audit.py
```

`python3 package_structure_test5.py --output-dir PATH` builds the import/source/support ZIPs, checks the source ZIP by a clean extraction and rebuild, reruns all gates, verifies report regeneration, and writes standalone documents, summary and checksums. It excludes build output and Python caches from the source archive.

The included cached Test 4 manifest, asset hashes and biome-tag graph allow offline comparison. To compare directly against the original ZIP, add `--test4 PATH` to the validator and `--test4-overrides PATH` to the report writer. The build scripts regenerate compiler-owned data, removing obsolete Test 3/4 grids. ZIP entries are sorted with fixed timestamps/modes. SHA-256 values for final deliverables are supplied externally in `SHA256SUMS.txt` to avoid embedding an archive's own hash in itself.

## Limits and outstanding work

Full `mods1.zip`/`mods3.zip` transfers repeatedly failed HTTP 403. Only complete CRC-verified JAR members from the available prefixes were recovered. **60 mod-folder JAR names from the supplied runtime remain unavailable.** The two additional supplied JARs not listed in that log are accounted for separately. The exact inventory is in `release_030/evidence/jar-audit-coverage-test5.json`.

Consequently, a complete installed-profile audit is not certified. Missing coverage includes CTOV, Cristel Lib 3.1.7, WDA Seven Seas, Traveloptics, Cataclysm Spellbooks and several other surface/End/dimension providers. Supplied Cristel config values and native resource overrides are validated as data; the missing library's actual processing is not certified. Default Minecraft tag resources were not in the uploaded mod JARs, so the matrix preserves unresolved base-game/optional tags rather than treating them as known empty.

IDAS Dread Citadel 5/12 and Ancient Mines entrance 2 do not have matching assets in the inspected JAR; no arbitrary repair is certified. CTOV's logged pool warnings await its actual assets. Blank `minecraft:`/Cook references and other missing-item recipe issues remain separately tracked. Four shipped-asset repairs are included; their static connector provenance does not prove full in-game assembly.

Runtime registry decoding, third-party library behavior, worldgen success, actual rarity, terrain acceptance, clipping, overlaps and performance remain later acceptance work. Nominal weighted-candidate accounting does not measure successful structure density. Streams' terrain-cache timing requires separate lifecycle/profiling evidence. No in-game test was required or performed before finishing the static deliverables.
