# Git history audit (Task F, 15 October 2026)

**Result:** one commit puts third-party binaries in history. `7177883` "whole pack push" (15 Oct, on `main` and pushed) added **331 third-party mod JARs (1.50 GiB)** plus 7 third-party resource and shader pack ZIPs, all under `Ambient Odyssey v0.4.9.1 - Structure Difficulty + Celestisynth TEST (1)/`. No other commit on any branch adds a JAR. None of the 10 AO custom JARs has ever been committed. No credentials found; `minecraftinstance.json` holds only local install paths (Windows user name) and public CurseForge author data.

**Status:** read-only audit of every local and remote-tracking ref. Nothing rewritten.

## Numbers (all refs)
- 4,465 blobs. Largest types: JAR 331 / 1,503.6 MiB, ZIP 12 / 79.4 MiB, CSV 213 / 50.3 MiB, JSON 1,278 / 22.1 MiB.
- Local `.git`: 80 MiB pack + 1.37 GiB loose objects (the JARs).
- Refs containing `7177883`: `main`, `origin/main`, `hygiene/untrack-jars` (local + remote). PR64 and all the other feature or experimental branches don't contain it.

## Binaries in history

| What | Where | Commit | Rule |
|---|---|---|---|
| 331 mod JARs (1.50 GiB) | profile copy `.../mods/` | `7177883` | **Breaks** "no unmodified third-party mod JARs in git" |
| 5 resource packs, 2 shader packs (~7 MiB) | profile copy `resourcepacks/`, `shaderpacks/` | `7177883` | Third-party redistribution; still tracked on `hygiene/untrack-jars` |
| Tan's Huge Trees `#main.zip` (70.1 MiB) | `release_030/overrides/config/tanshugetrees/custom_packs/` | initial `79bed7e` | Deliberate, documented in `.gitattributes` |
| `Ambient-Odyssey-v0.2.10.zip` (1.6 MiB, 12 files, no JARs) | repo root | `79bed7e` | Old CurseForge export, OK |
| 2 test datapack ZIPs | `docs/research/next-agent-package-20261014/tools/` | `138259f` | AO-made, OK |

## What `hygiene/untrack-jars` (PR #65) does and doesn't do
- Does: removes the 331 JARs from the index going forward, and ignores `*.jar` except the 10 AO customs.
- Doesn't: remove them from history. Every clone still downloads 1.5 GiB. The profile's configs, `minecraftinstance.json` and the 7 pack ZIPs stay tracked.

## Options (your decision)
1. **Keep history** and merge PR #65. No force-push; the repo stays about 1.5 GiB.
2. **Rewrite `main`:** drop the profile folder's `mods/` (and optionally the pack ZIPs) from `7177883` with `git filter-repo`, then force-push `main` and `hygiene/untrack-jars`. Only those two branches change; PR64 and the others are unaffected. GitHub may keep the old objects until support purges them, and every existing clone must re-clone or hard-reset.
3. **Option 2 + move the profile copy out:** also remove the whole `... TEST (1)/` folder from tracking. First check that nothing in its 17 configs is needed elsewhere.

**Owner decision (15 Oct):** no force-push, no history filtering against `main`, nothing destructive. Options 2 and 3 are **not pursued**; this audit is read-only information. The earlier recommendation of option 2 is withdrawn (nothing was ever rewritten).
