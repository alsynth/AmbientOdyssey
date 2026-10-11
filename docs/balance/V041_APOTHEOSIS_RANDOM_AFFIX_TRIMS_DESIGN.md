# Ambient Odyssey — Automatic Random Armor Trims on Apotheosis Affix Loot

**11 October 2026** · **Status:** source-confirmed feasible; **research/design only**. No pack/manifest/config/gameplay change, and no compiled addon or runtime test asserted.

## User intent

If equipment found in dungeon/structure chests, dropped by mobs, or yielded by similar loot systems has an **Apotheosis affix rarity**, then **always provide a randomly selected armor trim** if the item is trimmable armor. Decorative behavior only: **do not change loot counts, rarity roll, affix values, base armor stats, enchantments, gem sockets, or item chances**. Preserve any existing intentional armor trim. Do not trim weapons, tools, trinkets, Goblin-Tuned gear *unless it also genuinely carries Apotheosis affix rarity*, or untrimmable armor.

## Source confirmation

- [Apotheosis `Apoth.Components`](https://github.com/Shadows-of-Fire/Apotheosis/blob/1.21/src/main/java/dev/shadowsoffire/apotheosis/Apoth.java): distinct custom `apotheosis:rarity` and `apotheosis:affixes` **data components**. These are not vanilla `minecraft:rarity`. A visual icon / color is insufficient for detecting gear.
- [LootController.createLootItem](https://github.com/Shadows-of-Fire/Apotheosis/blob/1.21/src/main/java/dev/shadowsoffire/apotheosis/loot/LootController.java) creates affix items in-place, setting both the affixes and rarity. This is called from chest loot generation, loot conversions and other sources.
- [Affix loot injection](https://github.com/Shadows-of-Fire/Apotheosis/blob/1.21/src/main/java/dev/shadowsoffire/apotheosis/loot/modifiers/AffixLootModifier.java): generates extra affix item and marks `FROM_CHEST`.
- [Affix conversion](https://github.com/Shadows-of-Fire/Apotheosis/blob/1.21/src/main/java/dev/shadowsoffire/apotheosis/loot/modifiers/AffixConvertLootModifier.java): upgrades an *existing* loot-stack in-place into affix-rarity equipment.
- [Actual Apotheosis global loot modifier list](https://github.com/Shadows-of-Fire/Apotheosis/blob/1.21/src/generated/resources/data/neoforge/loot_modifiers/global_loot_modifiers.json): affix conversion, affix item injection, gems and hooks, ordered. New AO trim modifier must run **after these**, not before.
- [NeoForge 1.21.1 global loot modifier docs](https://docs.neoforged.net/docs/1.21.1/resources/server/loottables/glm/): GLMs are a supported global loot-list post-processing mechanism.
- [NeoForge 1.21.1 vanilla armor trim data component](https://lexxie.dev/neoforge/1.21.1/net/minecraft/core/component/DataComponents.html): `DataComponents.TRIM` contains `ArmorTrim`. Trim pattern/material are registry entries `Registries.TRIM_PATTERN` / `Registries.TRIM_MATERIAL` accessed through server-level registry lookup.

**Pinned AO base:** `Apotheosis-1.21.1-8.9.0.jar`. Public branch `1.21` represents active source and may have later changes; inspect pinned JAR bytecode/components in CI before compiling against it.

## Implementation options

**Preferred optional NeoForge integration addon**, no major loot-table overwrites:

1. Register `ao_affix_trims:random_affix_armor_trim` as a global loot modifier with empty loot conditions or safe chest/entity restrictions. Operate on **existing generated stacks**. Do not add extra loot.
2. For each stack: verify actual custom Apotheosis `rarity` component *and* an affix-bearing `affixes` component (or official `AffixHelper`), `minecraft:trimmable_armor` tag/valid trim equipment category, `DataComponents.TRIM == null`, `!stack.isEmpty()`. Do **not** assume rarity is the vanilla `DataComponents.RARITY`.
3. Select registered vanilla trim material and registered pattern using the **loot context's RNG**; optionally limit to vanilla namespaces, or configure explicit whitelist to exclude custom pattern/material resources lacking textures. Create `new ArmorTrim(materialHolder,patternHolder)`, `stack.set(DataComponents.TRIM, trim)`. The trim does not alter a normal item attribute component or loot roll.
4. **Ordering must be measured:** Apotheosis's `affix_conversion` and `affix_loot_injection` are themselves global loot modifiers. A separate AO GLM that executes earlier would miss new converted/generated stacks. Preserve all other GLMs, set `replace:false`, and test exact execution order. If ordering cannot be guaranteed, hook the **post-generation** point in Apotheosis's pinned `LootController.createLootItem`, or use narrow targeted callback. Do not claim 100% coverage solely from adding GLM JSON.
5. Mob equipment drops: test loot-table drops and mob-worn affix equipment separately. The latter may be transferred via equipment drop handling rather than the entity's loot-table output; if missed, add a narrow `LivingDropsEvent` fallback, but ensure it never trims normal gear or player-thrown items.
6. Lootr individualized chests normally roll loot tables; verify **each player's loot** is trimmed once, trim persists after save/reopen, and successive players can receive different random designs. Check custom WDA/DnT/Moog structure chest tables and static NBT (hard-coded existing items can bypass loot rolls).
7. Existing trimmed armor stays intact. New instances eligible only; never rewrite inventories, player storage, or all world ItemEntities during each tick.

### Visual design choices

- **Recommended for a first test: 100% chance, uniformly randomized among available *vanilla* trim patterns and material colors.** No gameplay stat, value or rarity change. Players still need templates and minerals to **choose** a desired trim intentionally.
- Later option: weight materials and patterns by loot type, world tier or environment for coherence, without gating player enchant/affix strength. E.g. Nether loot leans toward rib/snout/redstone/gold; icy tombs favor quartz/iron; dungeon bosses can select rare visual schemes, but no need for stage one.
- Keep **no trim applied** for helmets/armor not in the appropriate tag or whose renderer cannot show a trim. Avoid layering invalid trim textures onto animated/geckolib/unique armor. `Armor Trim Item Fix` should be tested for visual compatibility; it is not itself an auto-trimming mechanic.

## Implementation gates & tests before enabling by default

| Test | Expected |
|---|---|
| Vanilla unmodified diamond chestplate | No auto trim |
| Rare/epic/mythic Apotheosis affix-rarity diamond armor from chest | Exactly one trim, cosmetic only |
| Apotheosis affix-rarity chestplate from mob loot table | Exactly one trim |
| Apotheosis equipment as guaranteed dungeon rare loot / converted ordinary loot | Exactly one trim after conversion; must check GLM order |
| Apotheosis mob-worn armor dropped on death | Exactly one trim, or mark unsupported pending narrow drop-event fallback |
| Already trimmed affix armor | Original exact pattern/material retained |
| Affix-rarity sword/axe/shield/relic/gem | No trim |
| Goblin-Tuned non-Apotheosis chainmail/netherite | No trim; keep distinct economy |
| Customized/modded non-trimmable armor | No component added |
| Lootr multiplayer chest with 2 players | Independent loot remains independent; no desync/stack duplication |
| Affix rarity display, affix list, attributes, enchantments, gems, durability | **Byte-for-byte equal for those components** to source stack |
| Plain mob farm over time | No extra loot-roll RNG effect beyond trim rolls; no severe server cost |
| Blacklisted rare style/pattern without renderer | No invisible/broken material textures |

## Adjacent loot-system investigation

- **Lootr**: sourced loot per user, expected to use loot tables; runtime verify.
- **When Dungeons Arise / Dungeons and Taverns / Integrated Dungeons and Structures / Moog / Trek**: distinguish loot-table chests from prefilled NBT containers. The old `STRUCTURE_REGISTRY_CATALOG.csv` cannot prove loot path.
- **Apotheosis boss equipment**: generated via affix generator as possible, rather than all mob drops from loot tables; confirm pinned version.
- **Dimensional Dungeons and Mine Cells**: may use custom reward-generation APIs; GLM may miss direct `ItemStack` reward creation. Do **not** touch their working worldgen/Connector fix merely for cosmetic loot.
- **Goblin-Tuned**: is *different* attribute-based gear, retains its own economics and should not receive automatic trim unless independently approved.
- **External random armor loot datapacks**: replacing base items is not equivalent; no reason to add LootJS/KubeJS dependencies for this small item-component enhancement.

**Decision:** Put AO automatic Apotheosis loot armor trimming on the feature-ready research queue. A small optional NeoForge addon is more controlled than modifying hundreds of structure loot tables. Build/test separately; preserve user-verified combined ZIP and the current Balance Lab.
