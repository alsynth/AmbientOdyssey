# Test 6 — user exploration findings & first full gameplay log

**Observed:** 9 October 2026 (user session ~21:49–22:44 local). **Source build:** Test 6 candidate on `structure/test6`, after user manually replaced broken Structory: Towers v1.0.17 with `Structory_Towers_1.21.x_v1.0.14.jar`. **Evidence:** user's `latest(20261009-204744).log` (17,857 lines; not copied to Git because it contains launcher account/session metadata). **Status:** successful local world exploration; balance/performance issues remain and no dedicated-server test completed.

## User's direct observations (not automatic validation)

**Positive/working:**
- Prairie is populated and lively; Farmers and Create structures are seen adequately.
- Maple and Sakura forests do contain structures, although dense trees naturally limit viable placement.
- Mushroom Village **observed on Mushroom Island** (positive eligibility observation, not proof it *never* spawns elsewhere).
- No WDA Small Blimp or Coliseum observed in the test (positive but not definitive exclusion proof).
- Explorify **Black Spiral generated in the Nether and seemed fine**.
- Game reached Overworld, Nether and End without a fatal runtime crash following the manual Structory downgrade.

**Balance and worldgen changes requested:**
1. **Too much Prairie** despite good structure density. Rebalance biome selection/distribution in **Test 7** (not Test 6); keep its ecological identity.
2. **Too many lighthouses**. Identify source/structure ID, config and placement owner; modestly reduce frequency while preserving coastal landmarks. Log also reports missing lighthouse jigsaw pool `kaisyn:village/beach_lighthouse/villager_lighthouse_master` 5 times; inspect likely unrelated/related structure before patching.
3. **Too many Eternal Starlight portals**. Lower their natural generation probability substantially, but keep at least one accessible progression path and preserve biome availability.
4. **Bridges remain scarce** (one seen despite YUNG's Bridges plus another bridge provider) even with more rivers/streams; **Streams Reflowing** appears to create poor geometry for bridges. Distinguish a native Minecraft river/structure compatibility issue from tag/placement eligibility and stream connectivity; audit two sources and their placed-feature/structure-set routes, don't merely multiply frequency.
5. **Block Factory's Bosses dragon tower** both overlaps other structures and is too common for its boss-dungeon importance. Reassess rare boss landmark tier, stronger separation/exclusion/collision mitigation and biome selector; inspect actual effective placement before changing data.
6. **WDA Heavenly ships in End** appear exceptionally far/rare (none sighted). Verify End-only native set and locate behavior; do not automatically buff based on one survey, but compare actual terrain/biome eligibility.
7. Nether and especially **End portal/dimension transfer take too long**. Benchmark uncached entry vs repeat visits; profile dimension worldgen and portal transition without judging only a first-generation cost.
8. Average **client FPS below 100** without shader or DH; intermittent chunk-generation freezes. Requires profiling independent rendering (GPU-heavy) vs integrated-server new-chunk stalls.
9. **Incendium weapon textures absent**. Recommend bundling official **Sparkles: Stardust Labs Resourcepack** after MC 1.21.1/resource pack test: https://modrinth.com/resourcepack/sparkles ; official README https://github.com/Stardust-Labs-MC/Sparkles-Resourcepack/blob/main/README.md . Some custom entity/shield/Elytra models may additionally require compatible rendering support.
10. End obsidian structure dropped **“Cryo Duct”** (user phrasing) with missing texture. Log **confirms** missing model texture `astrological:block/crying_duct_tip` for `astrological:crying_duct#inventory`; inspect Astrological structure loot/palette and item asset, do not claim the observed structure's provider without registry ID.
11. **Iron's Gems 'n Jewelry is absent** from installed mod list; source project 1101111 official 1.21.1 NeoForge release exists: https://www.curseforge.com/minecraft/mc-mods/irons-jewelry . User requests evaluation/addition.
12. User requested a new **Nether Bastion overhaul**; candidate Better Bastions (https://www.curseforge.com/minecraft/mc-mods/better-bastions) states NeoForge 1.21.1 compatibility and bastion-tag/Incendium support; do not install until comparison with Incendium, YUNG's Nether Fortresses and existing boss/structure stack.
13. User requests **a mob that automatically repairs creeper holes**. A 1.21.5-only Jungle Robot datapack has this behavior (https://www.planetminecraft.com/data-pack/jungle-robot-6648930/) but is NOT confirmed on NeoForge 1.21.1; possible 1.21.1 NeoForge mechanic alternative Better Protection Explosions https://modrinth.com/mod/better-protection-explosions which restores terrain but **does not add a repair mob**. Park mob concept for compatibility check/design, do not substitute silently.
14. **Approved next-wave candidates:** Better Inventory and Backpacks (CF 1618019, v1.3.2 NeoForge 1.21.1 file 9099710, https://www.curseforge.com/minecraft/mc-mods/better-inventory-and-backpacks/files/9099710) and Shadow Drop (CF 1490601, NeoForge 1.21.1 file to pin after metadata check; https://www.curseforge.com/minecraft/mc-mods/shadow-drop). User explicitly requested both. Must check UI overlays (PasterDream GUI, Sophisticated Backpacks, Curios and Enigmatic Legacy+, cosmetics and performance) before adding to shared release.

## Actual log leads (not performance causality proofs)

- **29** integrated-server `Can't keep up!` warnings; individual stalls include **18,822 ms / 376 ticks behind**.
- FreeTerraForged on normal shutdown: **27,550 chunks generated**; **100.14 ms thread-time/chunk**; **9.06 real chunks/second**; **5.0% parallel efficiency** over **3,040,402 ms wall time**. This is a measured exploration benchmark, not a diagnosis of a single bad mod.
- `kaisyn:village/beach_lighthouse/villager_lighthouse_master` **5** times as “Empty or non-existent pool”.
- `astrological:crying_duct#inventory` reports missing `astrological:block/crying_duct_tip` texture in the resource reload (twice).
- Multiple invalid item references, including `byg:snowdrops` and `supplementaries:quark/hanging_sign_blossom`, indicating legacy/incompatible structure or loot data. Identify the source before editing/removing them.
- `iceandfire:portal_data` reported unknown/non-serializable attachment multiple times; assess whether it affects teleporting/world persistence.
- Other warnings: Embeddium modified by NeOculus (reported as tainted, common compatibility caveat); item model/texture warnings across other mods; modded mixin conflicts and missing optional reference maps. Do NOT interpret every warning as an actual fatal or assume it causes low FPS.
- No `FATAL` appears in this session; world shut down cleanly.

## Shareable 0.3.6 client test candidate produced independently

A **playtest-only** CurseForge import ZIP was generated from the original statically checked Test 6 candidate, modifying the **single Structory Towers file pin** (8396885 → 7078283), manifest display name/version, descriptive in-ZIP metadata and a playtest README. It retains 246 CurseForge projects and the exact worldgen/config files from the tested Test 6 candidate.

- Filename: `Ambient-Odyssey-v0.3.6-Structure-Test6-Candidate-FIXED.zip`
- Size: **69,731,644 bytes**.
- SHA-256: `ca8b695145e58a5d5775e0e0a8555871f2fa318a25ee68ba45d426dcc640d8df`
- ZIP CRC, root manifest and all 246 entries passed; unchanged structure/config override bytes were checked against previously validated Test 6.
- **IMPORTANT:** This archive was generated outside the repository builder, so not yet a reproducible `git checkout && python build_release_030.py` output. It is NOT uploaded to GitHub/private Release or universally accessible via chat sandbox URL. Anyone distributing it must upload the ZIP separately (e.g. Discord/Drive). **The authoritative GitHub source lock still needs a permanent 1.0.14 repin and release metadata/build validation**. Do not pretend GitHub currently generates the corrected ZIP.
- Further live testing/metadata QA is required; all newly requested mods above are backlog items **not part of v0.3.6 candidate**.

## Next work order

P0: Permanent Structory repin in editable source, update validators and binary-audit claims, reproducible corrected test ZIP; fix malformed lighthouse pool and meaningful registry reference errors. P1: Profile slow Nether/End transitions and actual FPS/chunk generation; resolve dragon tower overlap, over-common portals and lighthouses, and assess bridge+Streams Reflowing compatibility. P2: Adjust Prairie share (Test 7), balance Heavenly End structures after density evidence, add Sparkles resource pack, test Better Inventory/Shadow Drop/UI interactions, evaluate Iron's Jewelry, bastions and hole-repair companion/mod. Keep stable `main` rollback unchanged.

Report changes using verified commit IDs, original source file IDs, archive hashes and runtime observations. Avoid adding unvetted mods to the actively tested 0.3.6 preview without a new test build/version.
