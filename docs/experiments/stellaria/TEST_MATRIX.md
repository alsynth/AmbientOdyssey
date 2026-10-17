# Stellaria test matrix

**Runtime state: NOT TESTED.** Static source audit ran; no game process launched.

| Gate | Setup / action | Status | Evidence or blocker |
|---|---|---|---|
| Source metadata | Inspect official release page and source master; hash source archive | Static pass | DEPENDENCIES.md; source commit 5b9ce37; source archive SHA-256 recorded |
| Source sidedness | Run tools/audit_stellaria_server_paths.py against the checked Stellaria tree | Static findings | Three direct client-only calls reachable from server paths; one common boss class needs review |
| Build | Run Stellaria Gradle build | Blocked | No Java 21 or installed Gradle; wrapper download of Gradle 9.5.0 fails with Network is unreachable |
| Minimal NeoForge/Connector game boot | 1.21.1 / 21.1.252, Connector, compatible FFAPI, Stellaria dependencies | Not tested | No dependencies or launcher runtime available |
| Dedicated server boot | Minimal headless server, then AO full server | Not tested | Actual ./gradlew runServer attempt stopped at wrapper download before server configuration |
| Client baseline | Stellaria + required APIs, no Embeddium/NeoOculus/shaderpack | Not tested | No graphical runtime |
| Embeddium | Add current AO Embeddium 1.0.15 | Not tested | No graphical runtime |
| NeoOculus without active shader | Add AO NeoOculus 1.8.7, leave shaderpack off | Not tested | No graphical runtime |
| Complementary Reimagined | AO pinned r5.9.3; check sky, clouds, black-hole, lasers, particles, HUD and transitions | Not tested | No graphical runtime |
| Euphoria | Add 1.10.5 only as a separate condition | Not tested | Not part of audited AO baseline; no graphical runtime |
| Solas alternative | Only if the current AO profile supports it; test independently | Not tested | No live profile available |
| Low render distance | 6, 10, 16 chunks and AO's 12/6 default comparison; entity distance documented | Not tested | No live client/server |
| Boss encounter | Portal, entry, glide/dodge, waves, Zregos, segmented body, exit/death/save/restart | Not tested | Dedicated server and connected client unavailable |
| Two-player interaction | Staggered/simultaneous entry, targeting, persistence, logout/rejoin, inventory | Not tested | No multiplayer runtime |
| Shader toggles/restarts | Toggle shaders, change dimensions repeatedly, restart while enabled | Not tested | No graphical runtime |
| Performance | Avg FPS/1% lows, frame times, CPU/GPU, memory, MSPT at 6/10/16 chunks | Not tested | No GPU/game process |
| AO coexistence | Current R4 profile, compare with same profile without Stellaria | Not tested | No AO instance/profile mounted |

## Attempted command

Command: ./gradlew runServer in the Stellaria source checkout.

Result: exit code 1 before Gradle starts. The wrapper attempted to download Gradle 9.5.0 from services.gradle.org and failed with java.net.SocketException: Network is unreachable. This is an environment/setup block, not a Stellaria compile or dedicated-server result.

Environment recorded: OpenJDK 17.0.20, git 2.51.1, no system Gradle. The source requires Java 21. No client screenshots, server logs, shader visuals, or performance samples were produced.

## Static audit output

tools/audit_stellaria_server_paths.py reported:
- glide_calls_client_animation_from_server_payload: present
- server_tick_calls_veil_client_easing: present
- boss_entity_has_client_render_calls: present
- common_boss_class_references_client_api: present

These are source findings, not a runtime crash diagnosis. See BUGS_AND_PATCHES.md.

## Retry on 17 October 2026, 14:02 Europe/Amsterdam

- Rechecked installed runtimes: only OpenJDK 17.0.20 is present; no system Gradle or Java 21 installation was found.
- Re-ran ./gradlew runServer; it again exited 1 before Gradle configuration with java.net.SocketException: Network is unreachable while fetching Gradle 9.5.0.
- Followed the distribution redirect with curl; the release download timed out. No server process started.
- Result is unchanged: build, NeoForge launch, server/client join, shader and gameplay gates remain NOT TESTED.
