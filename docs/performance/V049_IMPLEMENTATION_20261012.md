# v049 client implementation - work in progress

Base: r19 full pack SHA10fe2562..., on performance/v049-client-overhaul-20261012. Added exact CF Euphoria915902:8884680 and EntityCulling448233:9100286; downloaded bytes match Modrinth SHA512 and CurseForge CDN. Removed disabled EquipmentCompare502561, LegendaryTooltips532127, exclusive Prism638111. Iceberg retained due AllTheLeaks integration references. Outer/nested bytecode audit found no remaining Prism references; removed mod dependencies were checked against native/Fabric declarations.

Streams client-only particle options now use bubbles1, debrisfalse, density0.5, cap250 and radius64. No terrain/planning/audio edits. EntityCulling safeMode=true, tickCulling=false; baseline whitelist defaults remain. Euphoria original patcher locally generates AO Performance/Balanced/Quality copies, using actual generated shader LOW/MEDIUM/HIGH options. Balanced selected by default, native shader menu permits weaker/stronger presets. No modified shader binaries redistributed. Original matching Complementary CF pin preserved.

Builder tools/package_v049_client_test.py asserts exact r19 base and manifest delta, 328 pins, preserved other bundled JARs and every unrelated config/quest/worldgen/loot byte. Source release-lock projection is330 (historical source divergence), consolidated import328. Existing Q/E and tooltip scroll features must be retested after removal.

Validation currently pending: full shader-on native UI/scene and frametime tests. First isolated full-roster shader-OFF startup test is running. No FPS gain or broad gameplay certification claimed. Do not promote until the test log is appended here.
