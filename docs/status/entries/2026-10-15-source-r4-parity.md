## Source vs R4 parity (15 October 2026, branch fix/source-r4-parity)

- **Static:** all 32 source/R4 differences classified: 15 build-generated Mine Cells recipes (generator output == R4 bytes; now synced into source), 17 mod-rewritten configs (documented in `release_030/MOD_REWRITTEN_CONFIGS.json`), 0 real changes. Details: [SOURCE_R4_PARITY.md](../../handoffs/source-r4-parity-20261015/SOURCE_R4_PARITY.md).
- **Static test:** `tools/check_source_r4_parity.py` vs R4: source 0 real differences; rebuild with R4's packager and PR50 base 0 real differences (109 line-ending-only). `tests/test_source_r4_parity.py` 2/2 PASS. **Engine / multiplayer:** not applicable / not tested.
