# Repository cleanup and archive policy

We retained all previous content in original Git history and relocated selected historical files using their exact existing Git blobs. No cleanup is automatically merged into `main`, into the verified Q1 content branch, or into a rollback branch.

- The **six v0.4 candidate-specific** GitHub workflows were kept active; **30** older worldgen, content research and one-shot workflow YAMLs were moved byte-identically to `.github/workflows-archive/2026-10-10/`. They are not registered GitHub Actions while archived. Restore one to `.github/workflows/` only if intentional and after reviewing its obsolete branch trigger/version lock.
- The two original GitHub bootstrap/upload helper files were moved to `docs/archive/bootstrap/`; they were aimed at creating an empty repo and no longer represent current instructions.
- Older full root README, AGENTS, Current State, Agent Workflow, questing README were **copied to** `docs/archive/history/`, and their original paths replaced with current, concise navigation guides.
- Version-locked `release_030/` files, mod configurations, large ZIP baselines, root import-dependent Python, catalogs and rollback branches were **not moved**.
- Old documentation in `docs/handoff/` and `docs/patches/` remains browseable, clearly historical.

To restore any archived workflow, copy its content back to the original `from` path listed in [ARCHIVE_MANIFEST.json](../archive/ARCHIVE_MANIFEST.json) and review triggers. The `sha` value provides exact original Git blob identity; ensure no new runtime requirements have superseded it.

A read-only CI workflow verifies archive counts and links, then builds the same reference-only ZIP from both source commits to prove the cleanup did not alter packaged bytes. Compare against **pre-cleanup HEAD ca8c91d5090dde5e9e789ebfda474e64f2c01e3c**, not the previous packaged artifact (that artifact predates unrelated documentation updates).

