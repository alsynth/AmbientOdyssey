# Ambient Odyssey 0.4.1 — combined Streams × Mine Cells + styled Questlog

Base: `experimental/v0.4.1-questlog-native-tab-style-20261011` (commit `77a5feea`).
Streams compat imported **unchanged** from `experimental/v041-streams-minecells-code-audit-20261011`, latest source commit `b4c2f196`.
Branch: `experimental/v041-streams-minecells-questlog-combined-20261011`.

This experimental variant combines the previously user-confirmed Streams compatibility Mixin addon with the source-compiled Better Inventory Questlog Q-tab (v0.1.1). Build release contains 329 CurseForge manifest refs. It re-adds only Streams Reflowing 2.14.4 (1581408/9060294) on top of the user-confirmed Mine Cells 328-ref control. Noisiumed and Structure Essentials remain excluded.

The native-styled Questlog addon remains **client only**. The Streams / Mine Cells addon is a **both-sides** mixin; include it on the dedicated server along with Streams Reflowing and Mine Cells. Their code is source-built, not fetched as a JAR from unknown provider sites or published as a new third-party CurseForge mod.

Build workflow: `.github/workflows/v041-streams-minecells-questlog-combined.yml`.
Source archive validator: `tools/package_v041_streams_questlog_combo.py`.

**What was verified:** The user confirmed Streams+Mine Cells addon works in singleplayer in an earlier test (Prison→Promenade, Overworld rivers, and after restart); the styled Questlog addon compiled and earlier 328-ref pack was statically tested. This new specific combined distribution is **not runtime tested**, and dedicated-server multiplayer remains untested. Noisiumed/Structure Essentials are not restored. Preserve both the working 328-ref and prior tested singleplayer instances separately.

**Acceptance:** Fresh world Prison, safe entrance, connected floors, reachable Promenade, Overworld streams working; E inventory native Q tab and ! badge, correct journal navigation, key texture appearances; restart; later dedicated server for multiple players. Nothing in automated ZIP checks substitutes for in-game testing.
