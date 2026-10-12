# Developer/agent workflow — current

**This is the operational checklist for the next work session.** Earlier accumulated handoffs are archived at [AGENT_WORKFLOW_full_2026-10-10](../archive/history/AGENT_WORKFLOW_full_2026-10-10.md).

1. **Orient:** Read [current state](CURRENT_STATE.md), [repository map](../maintainers/REPO_MAP.md), and [TODO](../../TODO.md). Avoid treating archived Test6 handoff docs as the latest constraints.
2. **Pick a base branch intentionally:** Content source `experimental/v0.4h-q1-ftb-field-manual-20261010` (331 refs, 50 Questlog quests, 32 FTB pages). Organization branch `maintenance/repo-organization-20261010` contains **documentation/CI organization only**; no gameplay/content modifications. Never overwrite `main`, `structure/test6`, stable releases or historical build candidates.
3. **Patch source:** `release_030/` is the pack source; `build_release_030.py` compiles changes. Preserve baseline `Ambient-Odyssey-v0.2.10.zip` and original Tan's Huge Trees source ZIP byte-exact. Keep 331 project IDs/file IDs stable unless changes are explicitly approved.
4. **Quests:** 50 Q1 JSON files under `release_030/overrides/config/questlog/quests/`, 13 chapter JSONs; Q1 index `docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json`. 32 FTB informational pages under `release_030/overrides/config/ftbquests/quests/chapters/` plus language. Ensure rewards are not duplicated across Questlog and FTB. In-game editor: `/ql edit_mode` (operator permission ≥2).
5. **Static checks:** `python tools/validate_v04_quest_campaign.py`; `python tools/validate_v04_ftb_manual.py`; `python tools/validate_v04_questlog.py`; `python tools/validate_v04_fg.py`; inherited `validate_content_040*.py` and `validate_worldgen_*.py`. Exact archive checks: `tools/validate_v04_release.py` and `tools/preflight_v04.py` on an actually generated archive. Use existing GitHub workflow if local binaries missing.
6. **Runtime gates:** Fresh CurseForge import and read-only installed-mod metadata scan; true client startup; Questlog/FTB tabs, GUI scales, character-specific quests/rewards, Mine Cells, structure distribution, dedicated server, two-person persistence/restarts, later 5–7-player FPS/TPS. **None** of these are certified by CI static pass.
7. **Commit:** Isolated branch + clear changelog/status + exact hashes/artifact ID from new run. Put finished ZIPs in Actions artifacts or GitHub releases, not source repo.

**Do not:** move root builders, imports, archives or version-locked inputs merely to make a tree look prettier; falsely mark a boss/structure objective verified; silently enable historically retired workflows. See [archive policy](../maintainers/ARCHIVE_POLICY.md).

## Armor/Questlog fix verification

For branch `fix/affix-trims-questlog-placement-20261012`, run the eight native trim tests and Questlog placement QA described in [the fix guide](../testing/ARMOR_TRIMS_QUESTLOG_FIX_2026-10-12.md). Keep gameplay stats and exact third-party pins unchanged. Prefer short, simple reports.

## Current consolidated test

Use the hash-pinned `tools/package_v048_consolidated_test.py` procedure for the full v048 diagnostic pack. Preserve the supplied prototype byte-for-byte; Claude owns its ongoing port work. Whaleborne is CF 1272075:8914201. Collect the real world-loaded log, not just menu startup; forward the two missing-ID findings to the owner. No automatic transmission to another chat.

## Current v0483 candidate

Use `tools/package_v0483_ring_test.py` on the exact r8 full import. Never reintroduce Subtle Effects (1023913) or its exclusive patch (1657433). Shared Fzzy Config stays. Ring compatibility source is `addons/ao-enigmatic-betterinventory`; isolated native QA in `tools/ring-probe` is never shipped. See [v0483 validation](../testing/V0483_RING_INVENTORY_2026-10-12.md).

The latest annotated UI request moves E to the lower-left tool area and Q above right armor. Build with `--questlog-jar addons/ao-questlog-betterinventory/build/libs/ao-questlog-betterinventory-0.1.6.jar`. Native QA must deliver actual MouseHandler movement/press/release for both buttons.

## Current r19 diagnostic candidate

Use `tools/package_v0484_r19_test.py` with the exact v0483 base and r19 SHA `5baeb932...`. The current owner report already passed all 30 tests; stale r8-run instructions in pasted handoffs do not apply. Keep prototype bytes and owner balance decisions intact. Follow [r19 validation and remaining gates](../testing/V0484_R19_FULL_PACK_2026-10-12.md).

## Performance phase authorized

Use r19 commit92575df / exact v0484 import as baseline. Follow [v049 preparation](../performance/V049_OVERHAUL_PREP_20261012.md); profile representative survival worlds, keep cold/warm and CPU/GPU evidence separate, preserve rollback. Actual candidate renderer metadata blocks blind migration. Performance work can proceed while outstanding gameplay acceptance continues.
