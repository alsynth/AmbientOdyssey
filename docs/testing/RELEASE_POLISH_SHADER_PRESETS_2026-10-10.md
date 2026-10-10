# Ambient Odyssey v0.3.7 Dev3 — release polish and two shader options

**Status 10 Oct 2026:** Source committed on `structure/test6`. User successfully ran **Dev2**, not yet Dev3. `main` remains older stable rollback; don't call Dev3 a release until clean import/client/server tests and worldgen decisions complete.

## User-verified Dev2

- Removing Dimensional Doors removed Creative Mode / inventory crashing in their test; no regression reported.
- Better Inventory/Shadow Drop/Borderless Window/Iron's Jewelry loaded in user's profile.
- NeOculus shader pack menu now opens properly (the Default Options background blur workaround worked).
- **User had to replace Iron's Jewelry 2.0.0 with 2.0.2**, avoiding a downgrade of Iron's Lib which would break other installed Iron mods. We now pin **CurseForge 1101111:8365016**; official file https://www.curseforge.com/minecraft/mc-mods/irons-jewelry/files/8365016 . Do not downgrade `irons_lib`; the unrelated Iron's Spells and other Iron mods need their installed version.

## Two shader options (official-project references, NOT loose binaries)

**Solas Shader V2.3**, CurseForge **678384:5743914**, https://www.curseforge.com/minecraft/shaders/solas-shader/files/5743914 , explicitly tagged Minecraft 1.21.1 and Iris. License All Rights Reserved — do not redistribute loose ZIPs outside official CurseForge project references.

**Complementary Reimagined r5.9.3**, CurseForge **627557:8884654**, https://www.curseforge.com/minecraft/shaders/complementary-reimagined/files/8884654 , supports Minecraft 1.21.1 and Iris per file metadata. Its license permits inclusion via CurseForge project references; do not include a copied stock shaderpack in `overrides/shaderpacks`.

The source build adds these two as `contentType:"shaders"` in the lock; the exported CurseForge manifest uses project/file ID entries. Shaders remain **disabled by default** and optional to activate in game. The CurseForge app is documented to recognize **Add More Content → Shaders** and install them separately from mods. Actual handling of shader project IDs inside this exact manifest (correct `shaderpacks/` location) needs **a fresh CurseForge app import verification**; don't claim it worked just because ZIP static checks passed. Benchmark worldgen and FPS without shaders first.

## Recommended RAM

The release lock sets `recommended_ram_mb=10240` and `build_release_030.py` now sets the manifest `minecraft.recommendedRam` field to **10,240 MiB (10 GiB)**. This is a suggestion, not forced Xmx; CurseForge individual profile memory settings and free physical RAM take precedence. Avoid 10 GiB allocation on systems with insufficient available memory.

## Narrator / accessibility defaults

On fresh installs only, Default Options now contains:
```text
narrator:0
narratorHotKey:false
onboardAccessibility:false
menuBackgroundBlurriness:0
```
The previous profile shipped `narrator:0` but still triggered the *first-launch accessibility onboarding voice*, which is independent. `onboardAccessibility:false` suppresses that startup flow. Correct case for `narratorHotKey`. Default Options preserves each existing player's own `options.txt`; to fix a previously created profile, open **Options → Accessibility → Narrator: Off** (or edit the local `options.txt` after closing game and set `onboardAccessibility:false`, `narrator:0`). Don't force-change an existing user's accessibility preference via a modpack update.

## Missing modpack profile icon

The previous manually created CurseForge ZIP has *no image/icon asset* in archive and `manifest.json` does not contain an icon specification. CurseForge **profile custom icons** are local app metadata and are not reliably preserved by sharing a generic import ZIP; the published **CurseForge project logo** is a separate image on the project page (the project submission rules require a square >=400×400 logo). The original Ambient Odyssey icon asset isn't checked into this source branch or the available archive. **Action needed:** retrieve the original approved Ambient Odyssey icon PNG from the user's asset history or have the user upload it; store a documented original asset in the repo/project's permitted image asset workflow, then set the CurseForge **project logo** and, if necessary, local custom profile icon in the app. Do not invent a `manifest.json.icon` key or falsely claim that adding `overrides/icon.png` will set the CurseForge launcher artwork.

## Quest progression / multiplayer acceptance (not installed yet)

The request is **player-independent quest completion inside shared FTB Teams**, without losing FTB Chunks cooperation. Current `default_reward_team:false` does **not** accomplish this and vanilla FTB Quests shares completion by team.

Candidate: **Solo Quests 1.1.2**, CurseForge **1644371:8614631** (NeoForge 1.21.1), https://www.curseforge.com/minecraft/mc-mods/solo-quests/files/8614631 . It tracks player progress individually; `teamSyncEnabled=false` disables voluntary syncing (serverconfig). **Upstream explicitly states it only functions on dedicated servers and NOT integrated/LAN worlds.** Test a separate dedicated-server copy with FTB Quests 2101.1.36 and 2 players. Backup `world/ftbquests` before attempting migration. Don't add to the shared release without multiplayer testing. Alternative NoreQuests/NoreTeams rewrites team management; not an ordinary checkbox.

## Release checklist

- [x] Correct Iron's Jewelry 2.0.2 CurseForge ID in repo source
- [x] Recommend 10 GiB in lock and source builder manifest
- [x] Default Options narrator onboarding and shader blur settings
- [x] Add two official shader project/file references to manifest source
- [ ] Fresh CurseForge import verifies 2 shader projects go to **Shaderpacks**, not `mods`, and can be selected independently; test with NeOculus 1.8.7
- [ ] Fresh client launch verifies the 2.0.2 jewelry version without changing `irons_lib`
- [ ] Default Options first-run narrator voice does not trigger on a completely fresh profile
- [ ] Restore original profile/project artwork; separately verify square project logo
- [ ] Add **individual quest progress** to final questbook acceptance, test dedicated server separately
- [ ] Source builder and all validators rerun against `0.3.7-prefreeze-dev3` clean checkout (manual test ZIP does not replace this requirement)
- [ ] Ocean expansion selection/test and worldgen freeze signoff remain open.
