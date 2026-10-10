# Ambient Odyssey v0.4 experimental — Mine Cells

Minecraft 1.21.1 · NeoForge 21.1.252 · 318 CurseForge references · 10 GiB recommended client allocation.

This candidate combines `structure/test6`, `content/0.4.0e-audit-first-wide-expansion` and `experimental/v0.4-minecells-preflight` without changing those branches or `main`.

## Integration

- Mine Cells 2.0.3, Connector 2.0.0-beta.17 and Forgified Fabric API 0.116.15+2.3.5 are exact file-pinned. Existing NeoForge owo-lib 0.12.15.5-beta.1 is retained. Mine Cells remains truthfully labeled Fabric; no original Fabric API is added. The exact 1.21.1 bridge does not declare Launchpad as a dependency.
- Carry forward all 0.4a–e content: Controlling and FTB XMod Compat; settlements/NPCs, Naturalist, Better Archeology and ambience; five resource-pack references; rare Mutant Monsters, Illager Invasion, Chipped, Handcrafted, Dusty Decorations, Night Lights and Apothic Combat; sixteen visual/QoL/discovery/photo additions and their prior dependencies. See the exact lock and earlier wave audits for the complete roster.
- Add missing Iceberg 1.3.0 and JamLib 1.2.2-build.2 dependencies discovered by inspecting exact native descriptors. Preserve inherited Comforts and all other existing pins. Correct Borderless Window's filename casing without changing its project/file ID.

## Repairs and defaults

- Preserve the inherited 273 native terminal-jigsaw repairs, source-backed template pool repairs, curated biomes, Farmers Structures tuning, rare major landmarks, dragon-cave tuning, Flight Ring recipe repairs and independent windmill salt.
- Repair Traveloptics' fire-element entity-tag JSON by inserting the missing comma, without changing membership.
- Bridge Fungi Delight's three legacy `forge:mushrooms/*` references to its existing `c:mushrooms/*` tags.
- Preserve 30% sleeping, fire spread off and mob griefing off. The latter also affects villager crop farming; boss effects may ignore it.
- Preserve quieter Waves/weather/block audio and disabled natural gorilla/fly/cockroach spawning. Rare mutant weights remain 0.01.
- New-profile defaults: render distance 12 and simulation distance 6. Existing player options are preserved by DefaultOptions. No measured AO performance improvement is claimed.

## Verification boundary

Mine Cells' isolated four-mod dedicated server actually ran: fresh world, five dimension force-load commands, save, clean stop, restart and clean stop. Full AO startup, client rendering, player portals/bosses/loot and multiplayer gameplay are **not runtime verified**. Exact checks, audit gaps and remaining issues are in `V04_TEST_RESULTS.md`; grouped acceptance is in `V04_TESTING_CHECKLIST.md`.

The complete developer test ZIP embeds checksum-pinned NeoReefRedux and is marked PRIVATE/experimental. The reference-only export omits that manual JAR. Neither export is a claim of CurseForge publication approval; native template override redistribution also needs publication review. No third-party mod JARs are committed to Git.

## Experimental 0.4f/0.4g reconciliation (330 refs)

A separate candidate branch `experimental/v0.4-minecells-fg-integration-20261010` merges twelve pinned 1.21.1 NeoForge projects into the already committed Mine Cells bridge: **Armor Trim Item Fix, Shulker Box Tooltip, Crafting Tweaks, Chat Heads, Sound Physics Remastered, Polymorph, Brewin' And Chewin', Dimensional Dungeons, Ancient Remnants, TarotCards Remastered, Aquaculture Delight, End Remastered Additions**. The original 318-ref release and source branches are preserved; no previous non-Native-Fabric Mine Cells pins or 273 jigsaw repairs changed. The previous 0.4g branch's unrelated Subtle Effects version bump was intentionally NOT cherry-picked.

New source tests assert all twelve exact project/file IDs, preserve inherited project pins and validate 330 refs, while the existing CI builds both experimental ZIPs. Any GitHub Actions success is evidence of source/packaging integrity, not proof of a working 330-mod client or multiplayer server. See [integration handoff](V04_FG_INTEGRATION.md).

## 0.4h — Questlog GUI compatibility-only candidate (331 refs)

Added the native NeoForge 1.21.1 Questlog 3.4.1 (`1202066:8952784`) on the experimental preflight-hardening branch without touching the earlier successful 330-ref ZIP. Its required Cloth Config 15.0.140 is already pinned in the original baseline (`348521:5729127`). Added source-backed `questlog-client.toml` trial for a screen-anchored button; no chapters, quests, rewards, class progression or FTB Quest replacements. Final button position and coexistence with the customized inventory must be confirmed in-game. See `V04_QUESTLOG_COMPAT.md`.

## v0.4h launch-readiness tooling (no mod changes)

Kept all **331 project/file pins** including Questlog and Mine Cells unchanged. Added a read-only installed-JAR metadata scanner with synthetic tests and separate client/server comparison, plus a local test runbook for the remaining 23 restricted/failed binary metadata records. New GitHub Actions package includes optional diagnostic tools beside the ZIP exports for Windows and command-line use. Passing metadata checks are not proof of complete Minecraft/client/server runtime compatibility.

## Q1 Field Manual trial — separate experimental ZIP (10 October 2026)

Kept the same **331 pinned mod projects** and the prior **50 native Questlog Q1 quests**. Added **29 FTB Quests in-game educational reference pages across 3 chapters** with optional checkmark markers, zero rewards, no dependencies or forced tutorials. Original WDA SNBT chapter is untouched; pre-existing English translation keys preserved while 29 article translations were appended. FTB Q1 source and package static validation passed GitHub Actions `38080599858` (source `e003e791b22aee124e551b47782b2a9332204856`); private ZIP 70,913,963 bytes SHA256 `9db3bbfaaf74a5d216795ac6934cf7c26d744ff228924bfc06630e3f9cfc5d1f`, reference-only ZIP 70,841,413 bytes SHA256 `a7b5d97d29a4673ac4d60de8723b59114945881e0992627f4c5c403faf24e191`. Actual FTB GUI, Questlog click behavior and multiplayer are NOT TESTED.
