# AO v0.4.1 source-based worldgen patch

## Confirmed Hominid 1.3.4 off-thread conversion
The 11 Oct actual client log contains 2 stack traces, both Hominid FinalizeSpawnEvent->ServerLevel.addFreshEntity, one at 76 and one at 85. Upstream Hominid source https://github.com/Alganaut/Hominid/blob/main/src/main/java/com/alganaut/hominid/registry/event/HominidClientEvents.java confirms two separate 10% Zombie replacements (Juggernaut, Bellman). In async StructureTemplate placement those replacements run off-server-thread and Cupboard warns.

New original AO NeoForge addon `ao-worldgen-safety` intercepts **only Hominid's off-thread Zombie FinalizeSpawnEvent handler** and cancels that specific unsafe handler invocation. It **preserves vanilla template zombies** (no discard), and Hominid's Juggernaut/Bellman replacements for ordinary main-thread spawns remain untouched. Slight gameplay tradeoff: zombie conversion won't occur in asynchronously placed structures, which is preferable to unsafe offthread entity insertion. No change to other Hominid mobs/events, no mixin to worldgen chunk system. Client and dedicated server need this addon. Java compile and static JAR checks are not Minecraft runtime validation.

## Luki Woodland Mansions native pool
The exact official native JAR v1.0+mod SHA256 `61c477cbe76847a204157c92b944438edc610abd91c71aff1ab7e58aca3a1e65` contains the real structure NBT `mansions:mansion/bottom_back_left.nbt`, and `mansion/main.json` selects it, but `worldgen/template_pool/mansion/bottom_back_left.json` is missing even though front-left's NBT outgoing jigsaw explicitly requests it. The client emitted four lithostitched missing-pool warnings when locating a mansion.

The AO separate Paxi datapack restores only **that pool registry entry**, with one single_pool_element pointing to the author's actual NBT, using the author's documented `mansions:mansion_texture` processor and rigid projection. `fallback=minecraft:empty`, no new fabricated geometry or textures. The internal jigsaw **name/target semantics and whether the back piece physically connects are still unverified**; playtest a newly generated mansion. This is not a blanket alias or reward rewrite. Author mod JAR untouched.

## Other open issues
- Tan's Huge Trees 1.8.0 beta warning from `GameUtils$Mob.summonWorldGen`, despite upstream's attempt at scheduling. Need *exact installed JAR bytecode* before code-level redirect; we do not apply an unverified global ServerLevel patch.
- Dungeon Crawl 2.3.17 `Spawner.place`: worldgen `setBlock` then `getBlockEntity` returns null before its block entity exists. `custom_spawners=false` does **not** fix this path. Safe NBT/serialization-lifecycle patch requires exact chunk APIs and validation; left unchanged instead of corrupting spawners.
- 540 `minecraft:air` item errors plus absent `redeco:hammer` and `biomesoplenty:rose_quartz_shard` need *source attribution*. Do not globally replace items with arbitrarily different loot.
- Performance 27.5s integrated server stall under cold generation, to be profiled before terrain/structure settings.
All carried over content, Mine Cells Streams bypass, Luki key resource repair, Questlog v0.1.2 and FTB informational manuals are unchanged unless release verification finds drift.
