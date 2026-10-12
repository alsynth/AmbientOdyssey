# Armor trims and Questlog button fix — 12 October 2026

Base: v0.4.5 source `6228a5a`; branch `fix/affix-trims-questlog-placement-20261012`.
Minecraft 1.21.1 / NeoForge 21.1.252 / Apotheosis 8.9.0 / Better Inventory 1.3.2 / Questlog 3.4.1.

## Armor trims — addon 0.1.1-experimental

The old addon only ran as a global loot modifier. It could run before Apotheosis
converted a stack and did not cover native gear/reward generation outside loot tables.
Now inject at the RETURN of the exact four-argument `LootController.createLootItem`
factory, after the native affixes and name are complete. Both native overloads
converge there. Keep the global modifier and add one-time dropped-item/chest-open
fallbacks for late modifiers and older loot. No per-tick scans.

Eligible items must have a bound native Apotheosis rarity, nonempty actual affixes
and the trimmable-armor tag. Choose random vanilla material/pattern; preserve an
existing trim and all other components. Cosmetic randomness does not consume
the native affix/loot generator's RNG.

**Eight native Minecraft GameTests PASS** on the installed dependency versions:
factory coverage of all four armor slots; ordinary armor/weapons/empty stacks;
existing trim plus component preservation; dropped old/late items; native item
serialization; rejection of empty affix markers; old chest-open event; global
loot fallback retaining list order/count. Actual required mixin applied.

Reproduce: `CI=true gradle -p addons/ao-affix-trims build runGameTestServer`.
The task requires a fresh eight-test PASS marker, not just exit code 0.

## Questlog — bridge 0.1.5

Installed Better Inventory JAR SHA-256 and layout constants are recorded in
`ARMOR_QUESTLOG_EVIDENCE_2026-10-12.json`. The old assumed settings x=198 and width=24
were wrong: actual tabs start at 134, crafting=254, gear x=280 and width=20.
Old Q x=224 overlapped the backpack tabs. Correct Q x is **GUI left+302**, y=GUI top.
Rendering, click hitbox and badge use the same anchor. Native floating Q stays disabled.

**Actual isolated native Minecraft client PASS:** real installed Better Inventory,
Questlog and Cloth Config, a disposable flat integrated world, native screen and
three GUI scales. Screenshots were visually inspected. One Q sits immediately
right of Settings; its hitbox opens the actual journal and Escape returns to
the same inventory at each scale. Native gear constants are read by the QA
assertion from the installed mod; this is not a hand-drawn layout mock.

| GUI scale | GUI left/top | Gear x span | Q x/y |
| --- | --- | --- | --- |
| 2 | 264/162 | 544–564 | 566/162 |
| 3 | 104/72 | 384–404 | 406/72 |
| 4 | 24/27 | 304–324 | 326/27 |

Reproduce with these three installed JARs in
`addons/ao-questlog-betterinventory/build/client-qa-runtime/mods`, the checked-in
Questlog client config copied into its `config/`, and
`CI=true gradle -p addons/ao-questlog-betterinventory build runClientQA`.
The task requires a fresh QA PASS marker. Test classes/harnesses are excluded
from both distributed addon JARs.

## Packages and remaining verification

`AO-Armor-Trims-Questlog-Update.zip`: extract and run INSTALL.cmd; select the
actual CurseForge profile (including a newer v046 kit if used). It backs up the
two AO addon JARs and Questlog client config, replaces only those addons and
disables native Q, preserving other config sections, mods and saves.

`Ambient-Odyssey-v0.4.5.1-ARMOR-QUESTLOG-FIX-TEST.zip`: separate full CurseForge
test import derived from exact successful run **38175613274**. All 330 project/file
pins and every unrelated ZIP member are unchanged; only the two AO addons and
manifest identity differ. It does not include later v046 port work.

**Not certified:** full AO rendering with JEI/Curios/all other overlays; custom
modded armor renderers that ignore vanilla trims; narrow-display fallbacks;
two-player dedicated-server gameplay. These limits do not negate the native
factory/drop/chest tests or isolated UI click/screenshot verification.
