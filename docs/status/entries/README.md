# Implementation progress entries

One receipt per completed batch or branch, named `YYYY-MM-DD-<slug>.md`. Each file states the branch, what changed, and its test level (source, static, engine, multiplayer) separately.

Add a new file instead of appending to [IMPLEMENTATION_PROGRESS.md](../IMPLEMENTATION_PROGRESS.md), so parallel branches merge without conflicts. Don't rewrite old receipts; mark superseded ones with a line at the top.

Read the files in date order; the newest file wins where they disagree.
