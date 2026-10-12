# v048 tooltip and startup patch

Branch: `fix/v048-tooltip-startup-ui-20261012`, based on the full gem/Whaleborne diagnostic pack.

## Settings

- WorldWeaver 21.0.26 supplies BetterEnd's pre-menu `WelcomeScreen`. Its native `VersionCheckerClient.presentUpdateScreen` adds it while `internal.did_present_welcome_screen` is false. Mark it acknowledged and disable the library's update popup checks. Preserve world presets, repair patches and experimental world-load warnings.
- Legendary Tooltips 1.5.5: blacklist all items from its borders, disable 3D item previews and its scrolling, and reset its experimental size overrides. Its native size overrides still produced clipped text in the full-pack stress test.
- Equipment Compare 1.3.13: temporarily disable comparison tooltips using its supported `blacklist = ["*"]`. Native screenshots showed long text rendering outside resized comparison panels, even with one comparison and explicit Legendary Tooltips bounds. Keep the mod installed and key bindings unchanged; one/strict defaults make a future re-enable conservative.
- SimplyTooltips 0.1.5: use its supported master renderer for both vanilla and modded items. Retain its 160-pixel text/body limits and mouse-wheel scrolling. Disable tabs so affix details are available in the same scrollable view without another key. Its `DrawContextMixin` replaces the gathered tooltip once, and `ScreenScrollMixin` queues mouse-wheel movement while a scrollable tooltip is active.
- There is no standalone Item Borders JAR in the tested roster. Do not remove unrelated Borderless Window.

These are a compatibility configuration patch, not an upstream code diagnosis. The supplied screenshots establish the symptom; visual acceptance must use the real client, not config parsing alone.

## Build and install

`python tools/package_v048_ui_fix.py --base build/Ambient-Odyssey-v0.4.8-FULL-GEM-WHALEBORNE-TEST.zip`

The builder requires the exact base SHA-256 `b0f506a1192d4e2e66a577872e78af68e8383c7df2c03d9d16b578c059cc2ebe`. It preserves all 331 CurseForge pins and all unrelated archive members, including every bundled JAR, quest, recipe guard and worldgen file.

For the existing profile, extract `Ambient-Odyssey-v048-UI-FIX-KIT.zip`, close Minecraft and run `INSTALL.cmd`. Select the profile folder. The installer merges only the named settings, backs up existing files, and rolls back write failures. It does not install or remove mods. Alternatively import `Ambient-Odyssey-v0.4.8.1-FULL-UI-FIX-TEST.zip` as a new profile.

## Apotheotic Additions

Per the user's instruction, record and defer its log results. The installed v048 log at 17:52 reports the same missing `apothic_enchanting:earths_boon` and `neoforge:elytra_flight` IDs already recorded in [the findings](V048_GEM_LOG_FINDINGS_2026-10-12.txt). Claude owns the unfinished gem work; the exact supplied prototype stays byte-identical.

## Verification

- Installer exercised against a disposable copy of generated configs: all targeted settings changed; every unrelated parsed setting preserved.
- TOML/JSON parse and ZIP integrity checks passed. All bundled mods, quest files and recipe files remain byte-exact.
- Native UI probe source: `tools/ui-probe`, excluded from both delivered archives. It creates a disposable flat world, activates the test player tier, generates actual Apotheosis mythic swords, selects a separate held sword, opens the installed Better Inventory screen, and captures plain/comparison tooltips at GUI scales 2/3/4.
- Multiplayer, shader-enabled tooltips and every modded item's custom tooltip remain outside this check.

Native final result: **PASS**, client exit 0 and clean save. Plain and fully visible affixed swords rendered at GUI scales 2/3/4 in the full roster. The 30-line lore stress tooltip stayed in one bounded panel; the native mouse callback changed scroll offset to 69 pixels and moved the first visible lore line from 1 to 5. Patched startup reached TitleScreen with no WorldWeaver welcome/update screen. See [native results](v048-ui-evidence/NATIVE_RESULTS.txt), [plain tooltip](v048-ui-evidence/patched-plain-scale2.png), [affixes](v048-ui-evidence/patched-affixed-scale3.png), [before wheel](v048-ui-evidence/patched-long-before-wheel.png), [after wheel](v048-ui-evidence/patched-long-after-wheel.png), and [build hashes](v048-ui-evidence/BUILD_INPUTS.json).
