# Part 2 report (CC_MESSAGE_0_5_5, items 2.1–2.7), 16 Oct 2026

**Result:**
- All Part 2 items are done in source.
- 0.5.5 data-only is built and statically verified.
- The two code items are built and pass their dev-server game tests. They are **not** in 0.5.5.
- Nothing was pushed or uploaded, and I did not log in to CurseForge.
- Nothing has been tested in game.

**Next action (owner):**
- Import the 0.5.5 ZIP and play the checklist.
- Answer the open questions below.

Status words:
- **Approved:** the owner approved it.
- **Implemented:** in source and committed locally.
- **Statically verified:** checked by scripts and tests.
- **In-game tested:** played in a real client. None is in-game tested.
- **Blocked:** cannot continue.

## Frozen submitted JARs
- The 8 uploaded JARs were not modified, rebuilt or replaced.
- Each one is recorded as "submitted" in `docs/status/CF_UPLOAD_TRACKER.md`:

| # | Project | SHA-256 (submitted) |
|---|---|---|
| 01 | Augmenting Sigils | `e3808be107aae556a9e31e872e30e7c520d125a6c794baaf7e360efef26f25fc` |
| 02 | Campaign (0.3.2-experimental) | `6ca143ba394140586c4fb1bd849c54093571442ea8efa9f558b11b3ca1e30a35` |
| 03 | Affix Trims | `96200046a389198b39b4ccd2ff0c9b9c319f55376cfcbefabb0e113f93a28cc7` |
| 04 | Starter Chest | `977def2c4fad272281e0b3b1131ce45ccd8a4f6058ed9441995a0c3ff0382aff` |
| 05 | Streams compat | `465a08063229e8b8e44e0262e7291308da1aece8236f6f3a6e20c67ed858f818` |
| 06 | Questlog bridge | `21b03582d6769d9617dfdd7b31e144950bf9eadf6f1037a8f711bcbcaf347839` |
| 07 | Enigmatic bridge | `7b588fe05e94ebfdba8c6d91bf568bd0e9a65af5fe504ebed9beac5e4c57f394` |
| 08 | Worldgen Safety | `474c1796a23d5f6eceee786ebdbda267293bcd95c0e151613ead1ff0dc59e971` |

- **Held, not submitted:** the Apotheotic port and Wet Sand. Their release conditions are in the tracker.
- **After-approval pin plan:** written down in the tracker, not done.

## Per item
| Item | Status | Evidence |
|---|---|---|
| Tracker | Implemented | `docs/status/CF_UPLOAD_TRACKER.md`, commit `c3741e3` (`release/0.5.5-data`) |
| 2.1 Sift / Item Displayed | Implemented (TODO entries "requested, unverified") | `TODO.md`, commit `41c367c` |
| 2.2 Scrap/Treasure bundle + hook | Approved (bundle), Implemented, Statically verified (17 Python tests, 5/5 dev-server game tests). Not packaged. Not in-game tested | see below |
| 2.3 Grand per-row switch + preview | Approved (experimental only), Implemented, Statically verified (53 Python tests, 3/3 dev-server game tests). Shipped policy unchanged. Not packaged | see below |
| 2.4 BI rebase | Implemented, Statically verified (regenerated, byte-identical, 0 dirty files) | `feature/better-inventory-loot-exclusion-rebased` @ `5d312be` |
| 2.5 0.5.5 build | Implemented, Statically verified (validator 0 errors, 156 quests; audit private FAIL 0). Not in-game tested | see below |
| 2.5b Ocean check | Owner running; no result yet | `docs/handoffs/release-050-20261016/CORNELIA_OCEAN_CHECK.md` |
| 2.6 Audit J/K/L/M + Ancient City alternatives | Implemented (report + audit tool); alternatives are a proposal only | `docs/status/CURSEFORGE_READINESS.md` (Part 2 section), `tools/curseforge_upload_audit.py` (commit `cb33bf9`, 4 tests) |
| 2.7 Ledger | Implemented | `docs/status/CC_MESSAGE_LEDGER.md` (Part 2 rows, #28) |

### 2.2 Scrap/Treasure (`feature/scrap-treasure-runtime`, commits `4181be9`, `81afc0b`)
**Policy:**
- Now 660 rows (was 492). No existing row changed.
- Rows per tier: T2 457, T3 105, T4 74, T5 2, T6 22.
- Row sources: category scheme 78, boss structure 19, IDAS T3 28, inferred 448.

**What the bundle applied:**
- The 52 tables with no keyword got T2, flagged inferred.
- Boss-structure mods got their campaign boss tier as a chance only, never guaranteed: 17 rows at T6, 2 at T5.
- IDAS got 28 rows at T3. Two IDAS tables were skipped because they have no clear pool.
- beekeepers_house stays T2.
- T1 settlements get no bonus.

**Keyword matcher (long/short):**
- Long keywords match inside a word.
- Short keywords and keywords not on either list match whole words only.
- 11 groups changed category under the new matcher. For example, a campsite moved T3→T2 because of "camp", and CTOV mesa_fortified moved T3→T1 because of "fort". The list is in `SCRAP_TREASURE_EVIDENCE.json`.

**Policy files:**
- The shipped policy stays `enabled=false`.
- The TEST policy (`ao_scrap_treasure_policy.test.json`) has `enabled=true` and `max_guaranteed_increase 0.5`.

**Runtime hook:**
- `ScrapTreasure.java` adds a NeoForge loot modifier, `ao_campaign:scrap_treasure`.
- It reads `config/ao_campaign/scrap_treasure_policy.json`, or the built-in policy if that file is missing.
- It checks the table's hash before drawing from a single pool.
- It respects the blocked list and has a debug log.
- It stacks with the vanilla table and with other mods' modifiers.

**Dev JAR:** `ao-campaign-0.3.4-dev.scraptreasure.jar`, SHA-256 `dfeeedb4c24945ec20ac892d6636599c2c079798bc9ae04de5014bdde82e5caf`.

### 2.3 Grand (`feature/grand-per-row-switch`, commit `ea27fa4`)
**Code:**
- Each row now has an `enabled` switch. Rows with enabled=false or approved=false are skipped.
- A debug log line `AO_GRAND_ROW_FIRED` is written for each row that fires.
- An optional override file is read from `config/ao_campaign/grand_treasure_experimental.json`.

**Vault code path confirmed:** `VaultBlockEntity.resolveItemsToEject` → `LootTable.getRandomItems` → NeoForge loot modifiers. So vaults are Grand sources.

**Experimental preview policy** (`ao_loot_policy.GRAND_EXPERIMENTAL_PREVIEW.json`):
- 38 usable rows: the 14 R4 rows plus 24 approved for experimental builds.
- `dungeoncrawl:chests/treasure` is linked to `dungeoncrawl:dungeon` and approved.
- `infested_temple_top_treasure` is held because no pool passes the rule.

**Pools re-picked:**
- infested_temple_vault 3→2
- Kisegi normal 0→2
- Kisegi ominous 0→3
- mining_complex 2→1
- Seven Seas ships: corvette 0→1, junk 0→1, yacht 0→2, galleon 0→1, frigate 0→1

**Shipped policy:** unchanged vs `132e368`.

**Dev JAR:** `ao-campaign-0.3.4-dev.grandswitch.jar`, SHA-256 `9fcde0030657533ab3827e8e47f111c8d3b9a4a2cc7562995e43829a2a980959`.

### 2.5 0.5.5 data-only (`release/0.5.5-data`, commit `41c367c`)
**Manifest:** name "Ambient Odyssey", version "0.5.5".

**Changes:** 57 added, 2 changed, 15 removed.
- Removed:
  - screenshot_viewer-client.toml
  - resourceful-config-web.json
  - AO_TEST_NOTES (8 files)
  - 4 `*.toml.bak`
  - the empty bountiful/errors.log
- The Tan's cache is kept.
- The Better Inventory part now comes from the rebased branch (`5d312be`).

**Safeguards kept:**
- R4 receipt hashes
- path allowlist
- removal-only exact-path allowlist (new test)
- manifest name/version only

**Output files:**

| File | Size | SHA-256 |
|---|---|---|
| `aowt/_builds/0.5.5/Ambient-Odyssey-0.5.5-PRIVATE-20261016.zip` | 154,578,651 B | `9c3d91efee261105efc90d03d99094857e22e27afb7bda5fd98dee8f06c35656` |
| `…-Rollback.zip` | | `f00955b51fd3c40207c7c68cf0a2e37d1dca371f842c0b152b13d803f25e8648` |

- The 0.5.0 ZIP is unchanged.
- The diff and checklist are in `docs/handoffs/release-055-20261016/`.

**Checks:**
- Master validator: STATIC VERIFIED, 0 errors.
- Packager tests: 11 OK.
- Upload audit:
  - private mode: FAIL 0.
  - public mode: FAIL 3 (author, JARs in overrides, 2 Fabric pins).

**Version note:** any later build with the code items needs a new pack version (e.g. 0.5.6) and new Campaign JAR versions. This is also in the ledger.

## Public-readiness
- **Public-readiness:** 0.5.5 is fine for private import only. A public listing is still blocked by:
  - the empty author;
  - 10 AO JARs in overrides (pin the 8 after approval);
  - 2 Fabric pins;
  - the shaderpack copies;
  - the app-export requirement;
  - the G licence items.
- The full list is in `PUBLIC_READINESS_DEBT.md` and `CURSEFORGE_READINESS.md` (M). All of it is deferred until after the loot and boss work.

## Open questions
1. **Scrap matcher:** should keywords that are on neither list stay whole-word only?
2. **Scrap matcher:** accept the 11 groups that changed category?
3. **Boss tiers:** most boss-structure tiers fell back to the mod's lowest tier because no boss id was found in the templates. Accept those tiers?
4. **Grand:** the Victory frigate pool is a tie between two pools. I picked the lower index, pool 1 (emerald). OK?
5. **Ancient City:** for the 4 templates, (a) a code hook or (b) leave them empty?
6. **Better Inventory:** it was rebased onto `feature/dungeon-loot-scrap-treasure`, as asked, not onto the new runtime branch. Re-base later?
7. **History:** older unpushed commits `c9e0d1a` (user path) and `9894b34` (e-mail) will block a push. What should happen to them?
8. **Ocean check:** waiting for your result.
