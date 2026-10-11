# AO 0.4.2 follow-up — recipes, invalid-air attribution, spawners, Questlog Q

**Source branch:** experimental/v042-recipes-nbt-spawner-ui-repair-20261011.
**Starting point:** the **330-reference** v0.4.2 Many-Fix ZIP, accepted earlier
Trek/Create rarity and three AO-authored addons. Private experimental work:
nothing below is proven by a Minecraft client launch yet.

## Exact 19-recipe native attribution

[Native source CI](https://github.com/alsynth/AmbientOdyssey/actions/runs/38146933860)
retrieved and inspected exact CurseForge project/file pins (SHA256 where source
lock provides it).

- **15/15 Mine Cells 2.0.3 Create/Farmer's Delight definitions present.**
  Source: CurseForge 618790/7033510, SHA256
  194b2318ec65896422f70bfc30983eb062c912c85295945c85599f64524e2481.
  The Fabric JSON has Fabric-only `fabric:load_conditions`,
  `processingTime`, old `item` output keys, 81,000 Fabric droplet fluid
  quantity and original cutting-board tool/result codecs.
  New `tools/generate_v042_minecells_recipes.py` regenerates exactly these 15
  IDs, converting according to the corresponding 1.21.1 Create and Farmer's
  Delight upstream native datapack codecs. Input/output item IDs, relative
  quantities, bonus drops/chances and 1 bucket of fluid remain unchanged.
  Conversion requires original JAR SHA; refuses unknown inputs or 81000!=bucket.
- **1/1 Dimensional Dungeons guidebook source present.** It already has
  `neoforge:mod_loaded` for Patchouli but depends on a custom Patchouli
  recipe serializer and book registration in the exact loaded version. This
  candidate **keeps it disabled** until those runtime registries are verified;
  do not replace it with an invented vanilla book.
- **0/3 Brewin' And Chewin' food recipe IDs present** in pinned 4.5.0 JAR.
  `hamburger_with_cheese`, `pizza_from_dough` and `toast_with_cheese` may be
  provided by another addon or stale recipe layer. The original items/formats
  and actual native owner are unknown; **all three remain disabled**.
- The 15 are **source+schema test candidates**; to claim real crafting, user
  must open JEI and operate Create/farmers cutting with compatible installed mods,
  confirm correct fluid transfer, drops and server save/reload without codec errors.

## Invalid `minecraft:air` item stack warnings

Exact [Dungeon Crawl 1.21 source](https://github.com/xyroc/DungeonCrawl/blob/neoforge/1.21/src/main/java/xiroc/dungeoncrawl/dungeon/monster/RandomMonster.java)
defines a zombie-villager custom offer with `buyB id=minecraft:air, Count=0`,
which is not a valid optional ItemStack in modern serialization. A **single
targeted Mixin** on its static field removes only that zero-count `buyB` when
source field matches. It leaves primary payment, trade sell, price, limits,
other nonair `buyB`, all other mods and all worldgen NBT untouched.
**Do not claim this explains all 504–540 logged errors.** The older index
audited only about 65 of 72 candidate structure sources; numerous native
structure templates have legitimate empties and some have invalid-positive
Count items. Each actual offender needs source matching before patching.

## Dungeon Crawl spawner persistence

The exact pinned [Spawner.java](https://github.com/xyroc/DungeonCrawl/blob/neoforge/1.21/src/main/java/xiroc/dungeoncrawl/dungeon/block/Spawner.java)
sets the spawner block and immediately calls `getBlockEntity(pos)`, which may
return null while `WorldGenRegion` is staging a block entity rather than live.
This causes the native "Failed to fetch a mob spawner" and unconfigured blocks.

Experimental `DungeonCrawlSpawnerPendingNbtMixin`:
1. In the exact native `Spawner.place` call, intercept only the
   `LevelAccessor.getBlockEntity(pos)` call.
2. If live spawner BE exists, leave it completely alone. If only a WorldGenRegion
   pending spawner block exists, pass a temporary SpawnerBlockEntity to
   original Dungeon Crawl logic (keep original random monsters, equipment,
   loot, delays and custom spawn data).
3. On method return serialize it with `saveWithFullMetadata(registryAccess)`,
   preserving id and coordinates, and store it in that generating
   `ChunkAccess.setBlockEntityNbt`. No worker-thread live entity spawning,
   no asynchronous `setBlock`, no blank placeholder.
4. Needs exact native bytecode/mixin compile check and fresh-world persistence
   test for configured monster type both on placement and **after server restart**.
   It is **not runtime proved**. A compilation pass cannot guarantee injection
   is applied at launch; `mixins.required=true` makes failures visible.

## Better Inventory Questlog v0.1.3

[Better Inventory 1.3.2 layout source](https://github.com/falling-colud/better-inventory/blob/main/src/main/java/dev/fallingcloud/betterinventory/BetterInventoryLayout.java)
places backpack tabs at x offsets 52–172, crafting 172–196 and settings
198–218, all relative to inventory GUI left at y=top. The old Q was x=222
on the *same row*, and the player reported unwanted overlap. The newly
authored Q tab is x=198 but **above the settings button at top−22** when
viewport permits, otherwise BELOW the complete inventory, then a side
fallback if neither vertical location fits. The drawn sprite and click hitbox
use the same live position per frame and it logs debug coordinates.
Use a full UI screenshot in GUI scales 2, 3, 4 to verify correct visual/hitbox
and compatibility with screen extensions; do not claim it already looks good.

## One combined test after ZIP build

On a fresh disposable Minecraft world / separate CurseForge instance:
- Boot and verify exact addon versions `ao-worldgen-safety-0.1.2-experimental`,
  `ao-questlog-betterinventory-0.1.3`, the same 330 third-party pins, no
  fatal mixin/serializer errors.
- Check JEI native Mine Cells compatibility recipes and run at least one each:
  Create crushing/cutting/haunting/filling and Farmer's Delight cutting.
- Spawn Dungeon Crawl normal/caged dungeon rooms across several new chunks;
  revisit after exit/restart: does the spawner contain expected mob and
  persist equipment, SpawnPotentials and delay?
- Open inventory at scales 2/3/4: Q tab must be above gear, open and return
  to correct parent; no backpack, gear, crafting or JEI overlap; check Q badge.
- Collect full latest.log. Compare air warning counts and spawner errors with
  previous log; do not infer a global fix from a reduced count.
- Verify earlier Curios amulet slot, quest/manual checkmarks, normal mob spawn,
  Mine Cells/Streams dimensions and Trek/Create balance did not regress.

**Never overwrite stable release or the v0.4.2 many-fix test ZIP.**
