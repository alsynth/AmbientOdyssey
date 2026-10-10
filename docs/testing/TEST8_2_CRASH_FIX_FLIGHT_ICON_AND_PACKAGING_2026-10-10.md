# Ambient Odyssey — Test 8.2 startup crash fix, official APIs, Flight Rings, artwork and private import (10 Oct 2026)

## Actual latest.log: fatal error before main menu

User attached `latest(20261010-011309).log` from Test8.1. At log line 654, ~03:12:11 local time, Java ModLauncher fails before client start:

```text
java.lang.module.ResolutionException:
Modules com.twelvemonkeys.common.image and mpf export package
com.twelvemonkeys.image to module irons_jewelry
```

This is a **Java module package collision between My Picture Frame (`mpf`, loaded `mypictureframe-neoforge-1.21.1-1.5.0.jar`) and the TwelveMonkeys image library**. Iron's Jewelry is the resolution target, not necessarily the problematic mod. The log ends before Minecraft main menu and contains no worldgen runtime evidence. **Action:** remove My Picture Frame from the manifest, do NOT downgrade Jewelry 2.0.2 or Iron's Lib. User can verify by disabling MPF on a duplicated instance. Repo `release_030/release-lock.json` now excludes CF project `1582023`. This is a reasoned isolation fix, not a runtime-proven fix until user tests Test8.2.

The same log establishes that user locally installed HAPI, Atlas API, Better Bastions and NeoReefRedux, but the previous Test8.1 zip lacked their proper distribution. We fixed the API manifest pins in Test8.2:
- Hybrid API `883374:9063597` = `hapi-neoforge-1.21.1-1.1.3.jar` (CF hosted; All Rights Reserved, manifest only)
- Atlas API `1145462:6880789` = `atlas_api-1.21.1-1.2.0.jar` (CF hosted; All Rights Reserved, manifest only)
- Flight Rings `401229:7782196` = `FlightRings-neoforge-2.0.0.jar` (MIT; manifest only)
- MidnightLib `488090:7318664` = `midnightlib-neoforge-1.9.2+1.21.1.jar` (Flight Rings linked development requirement; manifest only)

**Total 265 unique CurseForge references:** 262 previous −1 My Picture Frame +4 pinned additions; shaders (Solas/Complementary), 10GiB RAM, IceAndFire cave fixes, Rustic rarity and all Test8.1 configs kept.

## Paxi Flight Rings recipes (no KubeJS needed)

The mod author source `tired9494/Flight-Rings` branch `1.21.1-architectury` defines `flight_rings:basic_ring`, `flight_rings:advanced_ring` and data recipe IDs `basic_ring` and `advanced_ring`. Paxi pack `release_030/overrides/config/paxi/datapacks/ao_flight_balance` contains exact replacement recipe IDs and `pack_format:48`.

- Basic `ABA / CPC / MDM`: A Amethyst Shard, B Blaze Rod, C Gold Ingot, P Ender Pearl, M Phantom Membrane, D Diamond. Requires Nether blaze/Ender Pearl and phantom membrane; **not a free early-game creative ring**. Mod's default basic ring consumes hunger when used (effect depends on mod config; do not claim confirmed in this pack).
- Advanced `ENE / DAD / ESE`: E Eye of Ender, N Nether Star, D Netherite Ingot, A Basic Ring, S Echo Shard. Intended pre-End late-midgame/late-game boss reward. Default advanced ring uses XP penalty (test).
- Paxi recipe priority and JEI/crafting actual overrides must be tested. Also test 5-player server `allow-flight` permission, flight logout/reconnect and ring wear/consumption.

## Artwork: user's ORIGINAL file

User uploaded a **1254×1254** title image `Ambient Odyssey_ Forest Path to the Mountain.png` (RGBA). It is copied byte-exact inside the private test ZIP at `overrides/Ambient-Odyssey-Icon.png` (SHA256 `88a3646aae57a61b30fe5ee76ce6326b0c0ac2017ccaa0715a71d0d42b6342e5`). A separate 512×512 project-ready preview `Ambient-Odyssey-Project-Icon-512.png` was generated locally (SHA256 `1cf005922e9e857da68c53ab3938a56de3bbadee875c725eb197e07036fed75a`), but binary originals are **not yet checked into GitHub source**. CurseForge profile avatar is app metadata not reliably restored on import; set local profile icon manually from exported png, and upload project avatar separately in CurseForge project settings. No invented manifest icon field.

## Uploaded 3rd-party mods are bundled for PRIVATE testing only

The **exact user-provided JAR bytes** are stored as:
- `overrides/mods/betterbastions-1.0.0+neoforge-1.21.1.jar` SHA256 `847ca595f5bf7a88ec1b5893ce66dd48a96fb5c9babd96b45bb6e0b5975910fc`. Officially hosted on CurseForge project 1713723; exact CF file ID not yet established. For public upload **must replace embedded JAR with proper CurseForge manifest ref**, as CF rejects hosted JARs included under overrides.
- `overrides/mods/neoreefredux-1.0.jar` SHA256 `a590ada50e328760ab147f98596f482d13d48c0c87b50ff85270a21776144dfb`, Modrinth official release https://modrinth.com/mod/neoreefredux/version/1.0 , source https://github.com/andriyko69/NeoReefRedux, GPL-3.0-or-later; source author and original Reef Redux author credited. Under `overrides/ambient_odyssey/licenses/NeoReefRedux-GPL-3.0.txt` (license copy) plus source/credit readme. For public upload, **confirm the mod is on CurseForge approved non-CurseForge list or submit approval request**; open GPL license alone is insufficient for moderation.
- Do NOT try to embed HAPI, Atlas, Flight Rings or any other CF-hosted mods in overrides: must be manifest references.

**Official CurseForge policies:** https://support.curseforge.com/support/solutions/articles/9000197908-exporting-a-modpack-for-curseforge-project-submission and https://support.curseforge.com/support/solutions/articles/9000197279-moderation-policies . Moderation also requires the app-generated export and prohibits manual manifests.

## Actual private test archive

`/mnt/data/Ambient-Odyssey-v0.3.8-Test8.2-CrashFix-Flight-Icon-AllMods-PRIVATE.zip`

- **71,030,063 bytes**; SHA-256 `6c5f0c7dc3d406140e3e38c1889c54274da4d4550bc139a244064540df15ed8a`
- **1,077 ZIP members**, **265 manifest project IDs**, unmodified 1.21.1 + NeoForge 21.1.252, recommended 10,240 MiB RAM.
- Built independently from previously checked Test8.1 ZIP and verified: root `manifest.json`, exact file IDs, removal of MPF, no duplicate ZIP names/project IDs, two user-uploaded JAR SHA256 matches, icon SHA256, 3 Paxi recipe/pack files parse as JSON, ZIP CRC pass, every old non-manifest member byte-identical to Test8.1.
- This local ZIP **has NOT been generated by the authoritative GitHub `build_release_030.py` nor imported/launched in Minecraft**. Source lock and recipes match, but vendor JAR bytes/logo remain outside GitHub source and need manual assets or documented build inputs to reproduce private preview.
- Any claims of fixed crash, recipe replacement, full worldgen freeze, Quest progress, FPS, deep ocean compatibility, shader selection or public CurseForge submission remain PENDING runtime verification.

## New first-run test order

1. **Import Test8.2 as completely separate profile**. Confirm all 265 CurseForge mods/shader project refs resolve, and EXACTLY one copy of user-supplied Better Bastions and NeoReefRedux is under mods after import; no duplicated manual copies. Do not import into previous Test8.1 instance.
2. Try **main menu launch first**; if crash persists attach latest.log and actual crash report. Make sure no MPF JAR is present. Distinguish original TwelveMonkeys collision from any new errors.
3. Test newly pinned HAPI and Atlas API, Hybrid Aquatic and Iron's Jewelry 2.0.2 interactions; no Iron's Lib downgrade.
4. JEI `flight_rings:basic_ring` and `flight_rings:advanced_ring`, verify exactly new recipes, craftable, flight penalties and no server fly kick.
5. On fresh seed, follow full [Test8.1 one-pass worldgen checklist](TEST8_COMBINED_WORLDGEN_ONE_PASS_CHECKLIST.md) including dragons, coastline, structures, Deep Oceans, Nether bastions.
6. Two-player dedicated Solo Quests check; basic quest task earned by player A must remain incomplete for same FTB Teams party member B; serverconfig `teamSyncEnabled=false`.
7. **Keep public project v0.3.6 separate** until app export passes. Restore profile art manually from `Ambient-Odyssey-Icon.png`.

