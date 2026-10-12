# v0.4.8.3 ring inventory compatibility and Subtle Effects removal

Base: latest active GitHub branch `content/v0482-r8-full-pack-20261012`, commit `b106dd9350981df8b78c6d1d8c934b6e4c91bfec`, verified by fetching all remote heads on 12 October. New branch `fix/v0483-ring-inventory-no-subtle-effects-20261012`.

## Changes

Optional client-only `ao-enigmatic-betterinventory` 0.1.0 adds a native-style 24x20 E tab above Settings. Uses Better Inventory 1.3.2's installed tab atlas, selected row on hover/focus, tooltip and narration; leaves Questlog, Curios, backpacks and native inventory buttons intact. Placement checks bounds and visible widgets, then safe fallback positions. No source mod JAR is modified.

Exact installed Enigmatic Legacy+ 1.1.2 bytecode was inspected: `ClientSetupHandler.onInventoryGuiInit` adds its buttons only to vanilla inventory, creative inventory and `ICuriosScreen`; Better Inventory matches none. `EnderChestInventoryButton.getInstance` handles carried stack and sends `EnderRingKeyPacket`, whose server handler opens the player's original Ender Chest. This native action is reused.

Native `isTheCursedOne` also accepts persisted `SevenCursesBearing`; this integration intentionally requires actual `EnigmaticHandler.hasCurio(player, EnigmaticItems.CURSED_RING)` plus `CursedRing.enableEnderRing`, as requested. Holding the item or historical curse state alone does not qualify. No extra button for the separate Ring of Ender; its original support elsewhere remains. State is rechecked on rendering and click; lookup incompatibility disables the integration and logs once.

Removed CF Subtle Effects `1023913:7768631` and exclusive SubtleEndRem compatibility `1657433:8673508` from the active full import. The source release lock removes/bans both IDs, and its validator now enforces absence. No Subtle Effects configuration existed in the shipped base. No separate active client/server mod-list file exists. Historical candidate builders and evidence remain historical. Fzzy Config stays: SimplySwords, SimplyMore, SimplyTooltips and TarotCards require it. End Remastered remains.

## Validation

- Addon and isolated test probe compile with Java 21 / NeoForge 21.1.252; Gradle build PASS.
- Exact-base ZIP CRC, unique manifest pins, removal, bridge metadata/hash and byte-preservation assertions PASS: **329 CF pins**, all remaining pins and original files unchanged. No QA probe bundled. See [input hashes](V0483_RING_BUILD_INPUTS_2026-10-12.json).
- Static quest campaign (52 quests, 13 chapters), FTB Manual (32 pages, 3 chapters), source Questlog/f-g and archive Trek/DnT checks PASS. Source legacy roster remains 331 after this removal; it differs from the consolidated 329-pin import in previously documented historical roster entries. The delta builder is authoritative for this experiment; no unrelated roster migration.
- Actual production full-roster Minecraft client: fresh flat integrated world, initial hidden state, actual server Curios ring equip/client sync, layout/bounds/no visible widget overlaps at GUI scales 2/3/4, native mouse click, original packet/server Ender Chest opening, and server unequip/client button disappearance **PASS**. Clean save/exit code 0. Test runs only in `build/ring-full-pack-probe`; live profiles untouched.
- Screenshots inspected for native-style appearance. Evidence: [native markers](v0483-ring-evidence/NATIVE_RESULTS.txt), [scale 2](v0483-ring-evidence/ring-scale-2.png), [scale 3](v0483-ring-evidence/ring-scale-3.png), [scale 4](v0483-ring-evidence/ring-scale-4.png). Hover sprite implementation uses the same native atlas as Q; interactive hover, focus and disabled-access config still require manual verification.
- Existing unrelated r8 Cornelia recipe and inherited resource/loot diagnostics remain recorded; supplied Apotheotic JAR unchanged. This is not a comprehensive gameplay certification.

## Build / manual checks

```
python tools/package_v0483_ring_test.py --base build/Ambient-Odyssey-v0.4.8.2-R8-FULL-PACK-TEST.zip --jar addons/ao-enigmatic-betterinventory/build/libs/ao-enigmatic-betterinventory-0.1.0.jar --output build/Ambient-Odyssey-v0.4.8.3-RING-INVENTORY-TEST.zip
```

Import as a **new CurseForge profile**, use a throwaway world. Check E tab normal/hover/focus, equipped vs held/unequipped ring, ring-access config disabled, carried items/click, save/reload and multiplayer. Confirm Q, Settings, Curios/backpack integrations still work. Retest the previously crashing mob interaction without Subtle Effects. Broader game tests and dedicated server are not verified. Checklist is shipped in `AO_TEST_NOTES/RING_INVENTORY_CHECKLIST.txt`.
