# Structure Test 6 — Minecraft runtime acceptance plan

> **First runtime blocker (9 Oct 2026):** Startup did **not** complete. Structory: Towers v1.0.17 (`8396885`) is rejected by NeoForge 21.1.252: `Missing ModLoader`. See [first runtime findings](TEST6_RUNTIME_FINDINGS_2026-10-09.md). Test older 1.0.14 in a disposable profile and record new log before resuming this acceptance checklist.



**Written:** 9 October 2026. **Source:** `structure/test6` (not `main`). **Minecraft:** 1.21.1 / NeoForge 21.1.252. **Status:** static checks passed; **no Test 6 Minecraft client or server runtime acceptance has yet been recorded**.

## What is ready

The Test 6 candidate is committed to GitHub. It includes the approved eight structure additions (YUNG's Extras, YUNG's Bridges, Structory: Towers, Archaion, Explorify, Additional Structures, Create: Structures Arise and Create: Easy Structures), AAA Particles, the WDA major Overworld/End split, the dedicated Mushroom Fields-only Mushroom Village placement and curated addon selectors. The selected files are pinned in `release_030/release-lock.json`. Actual third-party JARs are **not stored in Git**; CurseForge must resolve them at import.

Completed static evidence: `docs/status/TEST6_CANDIDATE_IMPORT.json`; 247 continuation checks and 35 Test 6 checks; 1,081 extracted ZIP entries checked against the reference; 246 manifest projects. **These checks do not imply successful CurseForge downloads, loader startup, dimension compatibility or terrain-fit behavior.**

## Phase A — create a disposable test instance (fast smoke test)

1. From the GitHub checkout's **`structure/test6`** branch, ensure no uncommitted local work is being overwritten. Run `py build_release_030.py` (Windows) or `python3 build_release_030.py`. It should output `build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip` as a **candidate CurseForge import archive**. Its Test 5 Audit1 filename is historical; content is Test 6.
2. Verify this **exact ZIP** has `manifest.json` at archive root and extractable overrides. Compare SHA-256 and file-count evidence against `docs/status/TEST6_CANDIDATE_IMPORT.json`. The checked-in successful Windows import's reported hash is `1383d71ec7178490ddf5b056c29c34fc14cd9ce0d48a972294ca799cf71ccec8`.
3. In CurseForge, choose Minecraft → **Import Profile**, select this ZIP, and install into a **NEW test profile**. Preserve any earlier test/save profiles. Confirm all mods downloaded; report missing/unsupported files or version rejection rather than silently substituting JARs.
4. Use the pack's Java 21 runtime as appropriate for MC 1.21.1. Start without shaders or Distant Horizons initially. Allocate ~8 GB RAM as a starting point, adapting to available physical memory. Allow extra time for initial terrain/structure generation.
5. Reach the main menu, then create a disposable *fresh* creative test world with commands permitted and a recorded seed. Do **not** use a previously explored Test 5 world for primary worldgen acceptance.
6. Record the date, Git commit SHA, import ZIP hash, actual CurseForge profile's installed mod list if download differs, Java version, memory, and `latest.log`.

**Immediate stop conditions:** launcher refuses a required mod, NeoForge rejects Structory Towers v1.0.17 or AAA Particles, loading hangs indefinitely, registry/datapack errors, crash, required addon missing. Save full `latest.log` plus crash report before editing anything.

## Phase B — worldgen and selector testing (fresh chunks)

Test actual *natural generation* separately from `/locate structure`: locating a structure ID can prove a registration/path works, but does not establish expected density or good terrain fit. Use the registered IDs from the loaded pack / audit; don't guess IDs for mods. Track seed, coordinates, dimension and biome in your notes.

| Target | Required observation / failure to watch |
|---|---|
| **WDA majors** | Overworld majors continue generating in intended eligible biomes; End-only Heavenly/Aviary definitions remain End-only. The Overworld grid is 50/45, frequency 0.80; End native grid remains 50/45 at 27/38. |
| **WDA Mushroom Village** | Only eligible in `minecraft:mushroom_fields`, rare dedicated 40/20, frequency 0.5; verify no non-Mushroom-Fields placement or duplicate owner. |
| **WDA Bathhouse / exclusions** | Bathhouse remains rare (112/48, 0.5); WDA Small Blimp and Coliseum must not naturally appear. |
| **Explorify Black Spiral** | **User-approved enabled**; test Nether generation, bastion-biome eligibility, overlaps with other Nether content and spawn integrity. Disable only if an evidenced issue demands it. |
| **Structory: Towers v1.0.17** | Confirm the CF cross-version pinned file loads on MC 1.21.1 NeoForge; locate naturally generated towers and check blocks, loot and terrain fit. |
| **Archaion + AAA Particles** | Both load and their structures/particle assets work; look for missing dependency or rendering exceptions. |
| **YUNG's Extras + Bridges** | Real structures/placed features register; bridges fit river/canyon geometry, including FTF-generated terrain. |
| **Additional Structures** | Observe structures in curated vanilla and modded biomes; look for frequent tiny structures or major landmark collisions. |
| **Create: Structures Arise + Easy Structures** | Observe worldgen, correct Create blocks and loot, and density of Easy Structures' native independent grids. |
| **Farmers Structures** | Spot-check its *20 already-tuned structure sets* in intended biomes; do not double the frequency again without measurements. |
| **Biome parity** | Compare vanilla versus curated modded biomes; record whether new and old structures disproportionately appear in vanilla despite eligibility tags. |
| **Overlap / terrain** | Check buried, floating, intersecting or clipped structures (especially large WDA, Iron's Spellbooks mountain tower and bridges). |

Recommended minimum workflow: smoke test **one fresh Overworld seed**, Nether and End, then a second seed for density/biome eligibility. Use creative spectator/free movement, commands and `/locate` for targeted checks, plus independent natural sightings; do not treat limited samples as statistically conclusive. For heavy initial-load settings, limit render/simulation distance during the smoke test rather than disabling worldgen mods and claiming acceptance.

## Phase C — performance and server preparation

After startup and placement tests pass, check new-chunk generation stalls, heap use, TPS on the target multiplayer server and log spam. Test multiplayer separately; a single-player success does not establish dedicated-server compatibility. Preserve server errors, profiler/spark results where available, and whether FTF/Biolith/streams and structures behave together. **Do not launch or pre-generate the permanent 5–7-player server world yet.** Keep Test 7 terrain/biome changes separate.

## Evidence to attach to an issue or PR

- Exact branch + SHA; CurseForge import ZIP SHA; MC/NeoForge/Java versions and available RAM.
- `latest.log` and any crash reports, plus install errors (only relevant logs; avoid sharing private tokens/paths).
- Seed, dimension, biome, coordinates, screenshot and structure ID for each observed bad spawn/overlap.
- A short pass/fail table for the sections above; indicate **static-only**, **runtime tested**, **not tested** and **blocked** distinctly.
- Compatibility fixes should go to `structure/test6` with regenerated outputs and regression evidence; keep `main` at stable Audit1 until reviewed acceptance.

## Project order after this test

1. Fix crashes/loader compatibility and confirmed worldgen issues, rerun both validators.
2. Repeat focused runtime acceptance and source/import hash checks.
3. Prepare distinct Test 6 release artifacts, changelog, and reviewed PR to `main`.
4. Only **after** Test 6 acceptance, begin **Test 7** biome/terrain configuration and testing. Balance/questbook work follows later; it is not a substitute for a stable worldgen baseline.
