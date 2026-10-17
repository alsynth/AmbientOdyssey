# Stellaria blockers and patch findings

## Confirmed by source inspection

Source commit: 5b9ce3705e057a3d3b68bf7726aa10215b88d28b. Findings below are static. The upstream issue #1 report names a NoClassDefFoundError for net.minecraft.client.Minecraft (mapped class_310) on dimension entry during custom movement. This source ref was checked for the reported path; no runtime reproduction was possible.

### 1. Artha movement reaches a client animation helper on the server

ModMessagesServer registers an ArthaMovementC2S receiver and calls StellarGlide.glidePLayer on the server (ModMessagesServer.java around line 91). StellarGlide imports HandleAnimICANTTAKEITANYMORE and writes its xImpulse/zImpulse static fields from the movement call (StellarGlide.java around lines 53-59). That helper imports net.minecraft.client.Minecraft and advances renderer animation state. This closely matches the upstream issue report and is the strongest source-level explanation for the class_310 failure.

Minimal compatibility direction: keep all movement physics and validation on the server, but remove the direct server reference to the client animation helper. Send only the small movement/animation state needed to the client, or derive the pose from client movement. Then compile and reproduce the official issue path before treating it fixed.

### 2. Server dimension tick calls a Veil client-only easing API

Stellaria registers ArthaDimensionHandler.tick from START_SERVER_TICK. That method computes the skybox transition and calls foundry.veil.api.client.util.Easing.EASE_OUT_CUBIC. The eased value is then sent to clients. Replace this with a small common math function or calculate presentation-only easing on the client, then test server startup and Artha entry.

### 3. Zregos server path calls Veil renderer particle APIs

Zregos.serverTick reaches handleThoseFuckingParticlesThatIHate when the laser state is active. Its spawnParticle method calls VeilRenderSystem.renderer().getParticleManager(), which is a client renderer service. Server-side attacks should emit a Fabric/NeoForge particle event or send a client S2C effect packet; keep Quasar/VFX creation in a client-only receiver. Validate the behavior with a real server and at least two clients.

### 4. Einfarbig common entity mixes server gameplay and client render state

Einfarbig is a common entity class importing Minecraft and Veil client render/light APIs. Its main tick branches on level().isClientSide, so clientTick is guarded, but class loading and fields still require a dedicated-server run. Separate those fields and light lifecycle calls into a client renderer or client-only attachment. Audit all entity and block-entity common classes for the same pattern; the four checks in the helper are only the first pass.

### 5. Dependency/API ambiguity

The official Modrinth entry is a Fabric 1.21.1 release and lists Fabric-side libraries. Source master now requires Fabric Veil 4.5.0, but the official published jar inspected on the page is still 1.0.0 with Veil 4.2.0. A native NeoForge Veil build cannot be assumed to satisfy the Fabric source API, and two Veil jars must not be loaded together. First create clean release and source-built instances, record the actual jar metadata, then isolate whether the failure comes from Connector, Veil, GeckoLib, or Stellaria.

## Changes made

No Stellaria game code was changed because the required build toolchain and runtime are not available. The AO branch adds a reproducible static audit helper plus this source diagnosis and test matrix. No compatibility fix is claimed.

## Next implementation sequence

1. Use Java 21, obtain Gradle 9.5.0 and build the exact source commit; record the built jar SHA-256.
2. Assemble Fabric control and minimal NeoForge Connector instances with exact release 1.0.0 dependencies and one Veil implementation.
3. Capture dedicated-server startup, connect one client, reproduce dimension entry/glide, then try the four isolated sidedness fixes above.
4. Keep server gameplay authority unchanged; move only rendering and animation code to client events/network callbacks.
5. After server entry and fight work, run the shader matrix from TEST_MATRIX.md against AO's exact current renderer profile.
6. Only then consider the boss for pack integration. This branch does not decide its tier or rewards.
