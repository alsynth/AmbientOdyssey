# Upload kits report (Part 1 checkpoint, 16 October 2026)

**Result:** 9 of the 10 AO JARs are ready to upload as their own CurseForge projects; 1 is held. Every JAR was rebuilt from source with a real Gradle build. Nothing was uploaded, pushed or sent to anyone. **Not tested in game.**

- **Kits:** `release_kits\curseforge_upload\` inside the `release/curseforge-kits` worktree (`%USERPROFILE%\aowt\cf-kits\`), git-ignored. One folder per JAR with the JAR and `UPLOAD_INFO.md`. Index: `release_kits\curseforge_upload\INDEX.md`.
- **Source:** branch `release/curseforge-kits` (local), commits `8ba1277` (exact sources imported) and `6c21542` (metadata, licences, assets). The kit JARs are built from `6c21542`.

| Item | Status |
|---|---|
| 1.1 Inventory | Statically verified |
| 1.2 Per-jar kits + INDEX | Implemented |
| 1.3 Metadata (authors, displayURL, licence) via rebuild | Implemented, statically verified |
| 1.4 Apotheotic port (source found, textures replaced, wording) | Implemented, statically verified. Permission evidence: owner to attach |
| 1.5 Wet Sand rework, option (a) | Implemented, statically verified (18/18 GameTests). Client look not tested |
| 1.6 Gradle build + pinned wrapper | Implemented, verified (all 10 projects build) |

## 1.1 Inventory
| JAR | Source in repo | Mod id | Licence | Depends on | Environment |
|---|---|---|---|---|---|
| ao-campaign 0.3.2 | `addons/ao-campaign` | ao_campaign | MIT | Apotheosis (req); Relics, Simply More (opt); AO port rarities (soft) | both |
| ao-affix-trims 0.1.1 | `addons/ao-affix-trims` | ao_affix_trims | MIT | Apotheosis | both |
| ao-apotheotic-port 0.4.8 | `ports/apotheotic-additions/neoforge` (**imported 16 Oct** from the unpushed Codex commit `2fe7296`; the repo only had 0.0.1) | ao_apotheotic_port | MIT + AFL-3.0 | Apotheosis | both |
| ao-augmenting-sigils 0.1.1 | `addons/ao-augmenting-sigils` | ao_augmenting_sigils | MIT | Apotheosis; AO port rarities (soft) | both |
| ao-enigmatic-betterinventory 0.1.0 | `addons/ao-enigmatic-betterinventory` | aoenigmaticbridge | MIT | Better Inventory, Enigmatic Legacy+ (Curios) | client |
| ao-questlog-betterinventory 0.1.6 | `addons/ao-questlog-betterinventory` | aoquestlogbridge | MIT | Better Inventory, Questlog | client |
| ao-starter-chest 0.2.0 | `addons/ao-starter-chest` | ao_starter_chest | MIT | Apotheosis; Enigmatic Legacy+ (opt) | both |
| ao-wet-sand 0.0.1 | `ports/wet-sand-neoforge` (imported from `experimental/v046`) | ao_wet_sand | GPL-3.0-only | none | both |
| ao-worldgen-safety 0.1.4 | `addons/ao-worldgen-safety` | ao_worldgen_safety | MIT | Dungeon Crawl (declared); **Tan's Huge Trees (needed, not declared)** | both |
| streams-minecells-compat 0.1.0 | `compat/streams-minecells` | ao_streams_minecells | MIT | Streams Reflowing 2.14.4; Mine Cells (opt) | both |
| T.O. Magic Registry Fix 1.0.0 | **not found** (only built JAR copies in 20 test folders; no `.java` anywhere searched: the Codex folders, the worktrees, the repo and all its branches) | ambient_odyssey_to_magic_fix | MIT | T.O Magic 'n Extras | both. Already CF 1729925 / 9079300, not re-uploaded |

**Source check:** before any change, all 10 sources were built unchanged and compared with R4's shipped JARs. **All classes are byte-identical** (5, 4, 37, 4, 2, 3, 2, 7, 6, 3), and text resources are equal apart from line endings. So the repo source is exactly what R4 shipped.

## What changed in each JAR, and final SHA-256
| JAR | Changes vs R4 | Kit SHA-256 |
|---|---|---|
| ao-campaign-0.3.2-experimental | mods.toml metadata; + LICENSE | `6ca143ba39414058…` |
| ao-affix-trims-0.1.1-experimental | same | `96200046a389198b…` |
| ao-augmenting-sigils-0.1.1-experimental | same | `e3808be107aae556…` |
| ao-enigmatic-betterinventory-0.1.0 | same | `7b588fe05e94ebfd…` |
| ao-questlog-betterinventory-0.1.6 | same | `21b03582d6769d96…` |
| ao-starter-chest-0.2.0-experimental | same | `977def2c4fad2722…` |
| ao-worldgen-safety-0.1.4-experimental (held) | same | `c986292f7bba4c07…` |
| ambientodyssey-streams-minecells-compat-0.1.0-experimental | same | `465a08063229e8b8…` |
| ao-apotheotic-port-prototype-0.4.8-prototype | mods.toml (+ credits); NOTICE; + LICENSE (MIT); **4 gem textures replaced** | `229daf3028fe28b4…` |
| ao-wet-sand-prototype-0.0.1-source-prototype | mods.toml (+ description, credits); NOTICE; **19 textures + provenance file removed**; 18 block models rewritten; + `tinted_cube_all` model; + `WetSandClient` class; smoke test updated | `f45b41793920c13b…` |

Full hashes are in each `UPLOAD_INFO.md`. Metadata on every project: `authors="alsynth (Ambient Odyssey)"`, `displayURL` and `issueTrackerURL` pointing at the GitHub repo, licence unchanged. **No version and no registry id was changed.**

## 1.4 Apotheotic port
- **Source:** found. The full 0.4.8 source was in the earlier Codex workspace, at an unpushed commit (`2fe7296`). It is imported unchanged with `git archive`, and **37/37 classes rebuild byte-identical** to R4. Not held for source.
- **Textures:**
  - Pixel check against all 150 Apotheosis textures: **3 pixel-identical**:
    - `ars_mana.png` = Apotheosis `items/gems/3.png`
    - `purity.png` = `gems/16.png`
    - `undergarden.png` = `gems/10.png`
  - One more recolour: `decay.png` ≈ `gems/16.png`, shape and shading correlation 0.997.
  - **All 4 replaced** with original art from `ports/apotheotic-additions/tools/make_original_gem_textures.py`. It is pure geometry and reads no image, so the result is deterministic (MIT). Recorded in `docs/ASSET_SOURCES.md`.
  - **`decay.png` was not on your list of 3.** I replaced it because you said recolours are not enough. Revert by removing it from the generator if you disagree.
  - After replacement, no texture matches Apotheosis. The best correlations are about 0.7, which is the normal level between unrelated gem shapes.
- **Wording:**
  - The kit description, mods.toml `credits` and NOTICE say "Unofficial port based on Apotheotic Additions; used with the original author's permission".
  - They also link https://github.com/Bryce792/ApotheoticAdditions and credit Bryce792 / MCreator, with the AFL-3.0 notice for the ported data and the MIT notice for AO's code.
- **Permission evidence:** INDEX.md says "owner to attach (who, when, where)". Nothing is invented.
- **Dependants:** Augmenting Sigils (higher sigil costs for the four port rarities) and Campaign (rare affix rolls use port rarities). Both run without it, so they are soft dependencies; they are uploaded after it.

## 1.5 Wet Sand
- **Option (a) implemented.** The models reference the vanilla `minecraft:block/sand`, `red_sand` and `suspicious_sand_0..3` sprites through a new AO model, `ao_wet_sand:block/tinted_cube_all`. A new client-only `WetSandClient` darkens each stage: moist `D6D6DC`, wet `B0B0BA`, soaked `8E8E9A`.
- The 19 GPL textures are not in the kit and not in the source any more. Registry ids are unchanged.
- **Licence stays GPL-3.0-only:** the module was a port of a GPL mod. Relicensing is your call.
- **Tested:** the headless GameTest server passes **18/18**. **Not tested:** client rendering (how the tint looks).

## 1.6 Gradle
- First real build of `addons/ao-campaign`: success (done earlier on `build/gradle-wrapper`, SHA-256 `0f77fdb9…`).
- The pinned wrapper (Gradle 9.2.1, distribution hash pinned) is now on `release/curseforge-kits` with the `.gitignore` exception (`!**/gradle/wrapper/gradle-wrapper.jar`).
- All 10 projects build with it (`addons/ao-campaign/gradlew -p <project> jar`).

## Upload order
1. AO Apotheotic Additions Port (Unofficial)
2. Ambient Odyssey Augmenting Sigils
3. Ambient Odyssey Campaign
4. Affix Trims
5. Starter Chest
6. Wet Sand
7. Streams Mine Cells Compat
8. Questlog Inventory Bridge
9. Enigmatic Inventory Bridge

Not uploaded: Worldgen Safety (held). No AO JAR hard-requires another, so steps 4–9 can go in any order.

## Held
- **ao-worldgen-safety:**
  - Its mixin config is `required: true` and targets a Tan's Huge Trees class, but `mods.toml` declares only Dungeon Crawl. Without Tan's Huge Trees the game would fail to load.
  - **Fix (your choice):** declare `tanshugetrees` as a required dependency, or make that mixin optional. Either is a change beyond the approved metadata.

## What the owner must provide
- **Every project:** a square logo, at least 400 × 400, not a solid colour and not copyrighted, with its provenance recorded.
- **Apotheotic port:** permission evidence (who, when, where).
- **Before upload:** push `release/curseforge-kits`, so each project's source link shows the exact source. The unchanged code is already public on `experimental/master-integration-r3-reconciled-20261015` (except the two ports).
- **After upload:** send me each projectID/fileID.

## Could cause rejection, and I could not check
- **Name/slug availability:** not checked (no login).
- **The port:**
  - It ships 3 always-false overrides of Apotheosis affix files and item models under the `apotheosis` namespace. They are new content, not copies, but a reviewer may question them.
  - "Unofficial port" projects need the permission evidence to satisfy moderation.
- **The Streams compat:** mixes into Streams Reflowing (ARR). No code is copied, but it is pinned to one version.
- **Prototype/experimental names:** "prototype" and "experimental" stay in the file names (versions unchanged); reviewers may ask about them.
- **Wet Sand:** tint and look untested in a client. The GPL licence needs the source link to resolve (push first).
- **Logos:** none supplied yet.
- **Description length/format rules:** CurseForge wants a real description, which is given. The rendering of the pasted Markdown was not checked.

**Public-readiness:**
- These kits copy no third-party file except what is credited and licensed: AFL-3.0 data and textures in the port, used with permission.
- Wet Sand now ships no third-party textures, and every kit JAR has authors, displayURL and a licence.
- They are public-safe once you attach the port permission evidence and the logos, and the held JAR is fixed.
