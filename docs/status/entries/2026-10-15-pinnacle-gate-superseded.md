> **Superseded** by [2026-10-15-pinnacle-cornelia.md](2026-10-15-pinnacle-cornelia.md): the owner chose epic gear + Captain Cornelia instead of deleting the gate.

## Pinnacle gate fix (15 October 2026, branch fix/pinnacle-gate)

- **Finding (static, from R4 bytes):** R4's `ao_campaign_gates` Paxi pack replaced native `apotheosis:progression/pinnacle` with `minecraft:impossible`; no code grants it (grant removed in `01c2c58`), so Pinnacle is unobtainable except by operator command. Proof: [PINNACLE_GATE_PROOF.md](../../handoffs/pinnacle-gate-20261015/PINNACLE_GATE_PROOF.md).
- **Source:** gate pack deleted from the v050 overlay and listed in `removed-source-paths.json`. **Static test:** `tests/test_no_impossible_tier_gates.py` 5/5 PASS. **Engine / multiplayer:** not tested. **Packaged:** no (R4 still contains the gate).
