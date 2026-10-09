# Ambient Odyssey — Current Project State

**Updated:** 9 October 2026. **Canonical repository:** `alsynth/AmbientOdyssey`. **Minecraft:** 1.21.1. **Loader:** NeoForge 21.1.252.

**For every new agent/chat:** Read root [AGENTS.md](../../AGENTS.md), this status document, [runtime acceptance](../testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md), and the handoff files. GitHub is the source of truth; chat history and downloaded importer kits are not required to understand the build.

## Branch and release status

| Branch | Role | Status |
|---|---|---|
| `main` | **Test 5 Audit1** rollback and stable source | Do not merge Test 6 without runtime acceptance |
| `structure/test6` | **Test 6 implementation** and evidence | **SOURCE COMMITTED**, scoped static checks passed, gameplay/runtime **NOT TESTED** |
| Test 7 | Future terrain/biome wave | Only a queue/planning document; **do not start yet** |

**Test 6 implementation push verified:** `ba8551200f803a37dd8450c1a80da13ebc913967` and subsequent documentation commits on `structure/test6`. All three original Claude patches are versioned in `docs/patches/` and their editable source changes, generated worldgen assets, manifest, tests and evidence are in this branch. **No Test 6 gameplay release has been approved.**

## What is actually implemented

- **WDA:** modest Overworld major frequency 0.80 with separate End-only native owner kept at 27/38; Bathhouse unchanged 112/48 frequency 0.5; Mushroom Village single rare owner 40/20 frequency 0.5, `minecraft:mushroom_fields` only. No Small Blimp/Coliseum natural spawning.
- **Eight approved structure addons in CurseForge manifest/source:** YUNG's Extras, YUNG's Bridges, Structory: Towers v1.0.17, Archaion, Explorify, Additional Structures, Create: Structures Arise, Create: Easy Structures; **AAA Particles** added to satisfy Archaion. Exact pins: `release_030/release-lock.json` and `release_030/approved-structure-additions.json`.
- **Worldgen selectors:** addon eligibility expanded into curated biomes; existing Audit1 Farmers Structures tuning (20 sets) kept without multiplying again; existing compatibility fixes preserved.
- **Explicit 9 Oct user decisions:** Keep Explorify Black Spiral **enabled provisionally** pending real Nether checks; use Structory: Towers **v1.0.17 CF 783522:8396885** with a version compatibility exception. These decisions supersede old handoff rows; loader compatibility is still unverified.

## Verified evidence — static only

- Windows import candidate recorded in `docs/status/TEST6_CANDIDATE_IMPORT.json`.
- `246` CurseForge manifest projects; `1,081` extracted ZIP members matched approved reference.
- Two identical local builds, ZIP SHA-256 `1383d71ec7178490ddf5b056c29c34fc14cd9ce0d48a972294ca799cf71ccec8`.
- `247` continuation checks and `35` focused Test 6 checks passed; reports: `docs/status/TEST6_ADDONS_CONTINUATION_VALIDATION.json`, `docs/status/TEST6_ADDONS_FOCUSED_VALIDATION.json`.
- Original 73,500,294-byte Tan's Huge Trees custom ZIP is tracked in ordinary Git (not LFS).
- **Not tested:** actual CurseForge download/install of every new pinned file, Minecraft client or dedicated-server startup, worldgen registry acceptance, natural structures, FTF terrain fit, Nether Black Spiral overlap, Structory cross-version behavior, or generation performance.

## Build / next action

From a checkout of `structure/test6` (not `main`), with Python 3.10+:

```powershell
py build_release_030.py
py validate_continuation_031.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test6-continuation.json
py validate_structure_test6.py --archive build/Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip --report build/test6-focused.json
```

The ZIP retains the historical Test 5 filename even though contents are the Test 6 candidate. Import it into a *new disposable CurseForge test profile*. **Run the [Test 6 runtime acceptance checklist](../testing/STRUCTURE_TEST6_RUNTIME_ACCEPTANCE.md) next.** Do not start the permanent server map.

Do not edit generated Paxi datapacks alone; change editable `release_030/` inputs/scripts, rebuild and validate. Never copy unmodified third-party mod JARs into Git or claim a static audit proves runtime compatibility.

## Outstanding work / known risks

1. **Runtime compatibility:** Structory v1.0.17 bypasses ordinary version-label screening; verify MC 1.21.1/NeoForge at load. Archaion + AAA Particles and Create addons need real loader checks. No original third-party JARs are stored in Git.
2. **Worldgen acceptance:** new addon structures, biome parity, Black Spiral Nether intersections, Farmers spawn rates, overlap/clipping, bridges and large landmarks in FTF/Biolith/streams.
3. **Performance:** fresh-chunk costs and eventual dedicated 5–7-player server stability.
4. **Validator portability:** `audit_jars_031.overlay_tags` splits an absolute path on the first `/data/` and can wrongly fail when the checkout is under `/mnt/data/`. Until fixed, validate from a path without that substring; do not misdiagnose the fake missing tag.
5. **Distribution:** final Test 6 release assets, root manifest, hashes, changelog and reviewed PR to `main` only after runtime acceptance.

## Work required from the next agent

Confirm checked-out branch and Git SHA; reproduce the build and scoped validators before edits; study `docs/handoff/01_TEST6_IMPLEMENTATION_BRIEF.md`, `02_POST_HANDOFF_DECISIONS.md`, `TODO.md`, and `docs/audits/`. Carry out the runtime checklist, record outcomes with seed/logs/coordinates, commit only evidenced source fixes with regenerations and update this file. Do not reopen decisions already approved on 9 October or prematurely apply Test 7 biomes.

**Evidence language:** `Implemented` = in Git commit. `Static verified` = checks run. `Runtime verified` = actual Minecraft run with evidence. `Blocked` = actual dependency/test barrier. Be precise.
