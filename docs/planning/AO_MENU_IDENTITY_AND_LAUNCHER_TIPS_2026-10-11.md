# Ambient Odyssey — title-screen identity and launcher tips

**Requested:** 11 October 2026. **State:** planned only, NOT implemented in the v0.4.3 downloadable test ZIP. Maintain all existing content and preserve rollback branches.

## Next menu/UX patch priorities

1. **Remove BetterEnd's unsolicited main-menu pop-up/window.** Identify the actual owner of the popup (BetterEnd, BCLib/WorldWeaver, another companion mod or notification) in the installed runtime before altering it. Suppress via a supported client config, resource/UI override or narrow integration where possible; do NOT remove BetterEnd/end worldgen as a shortcut. Verify the popup stays gone after restarting and does not hide essential errors.
2. **Replace Minecraft/Aquamirae menu branding with Ambient Odyssey.** Investigate Aquamirae's `themed_main_menu` config and whether it changes panorama, splash/logo or both. Also inspect existing `release_030/overrides/config/cumulus_menus-client.toml` (currently active menu `cumulus_menus:minecraft`) and whether Cumulus Menus can override the title without adding another UI mod. If needed, compare simple NeoForge 1.21.1 logo-only tools (e.g. Simple Menu/UltraEasyMenu) against compatibility and menu injection conflicts. Prefer a lightweight, Minecraft-textured **AMBIENT ODYSSEY** title graphic, no Aquamirae/Minecraft double logo and no intrusive popups. Keep menu buttons operational and resource-pack/shader compatibility intact.
3. **Later phase: full AO-specific menu design.** Original hand-crafted Minecraft-adjacent identity, curated background/panorama, restrained buttons, sensible version text; avoid synthetic-looking glossy UI and unnecessary renderer conflicts. Prototype separately, test common GUI scales and performance, and avoid changing working gameplay mods merely for cosmetics.

## Acceptance

- Title screen opens without the reported BetterEnd pop-up.
- Main logo reads **AMBIENT ODYSSEY**, without the Aquamirae branding (and without duplicated Minecraft logo).
- Singleplayer, Multiplayer, Mods, Options, Quit, accessibility and mod-config entry points remain usable; correct mouse hitboxes at common GUI scales.
- No meaningful increase in startup errors or renderer/menu compatibility warnings.
- Build and label a new test artifact, leaving v0.4.3 and rollback state intact.

## Tips & Tricks later insertion

Add a clear beginner-friendly note about **closing CurseForge after launch**, checking whether it remains in the system tray, and **closing the CurseForge Dashboard** when not needed. Distinguish CurseForge background processes from the Minecraft game and avoid promising exact RAM savings. A planning draft is appended to `docs/questing/FTB_TIPS_AND_TRICKS_V0_3.md`; it is not yet an authored/shipped FTB in-game page.
