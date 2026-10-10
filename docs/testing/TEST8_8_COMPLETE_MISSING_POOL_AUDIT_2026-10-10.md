# Ambient Odyssey — Test8.8 missing jigsaw pool source audit and exact repair

**10 October 2026 | experimental branch:** `worldgen/test8.8-complete-pool-repair`, based on Test8.6/8.7 source, Minecraft 1.21.1 / NeoForge 21.1.252. **No further in-game test requested by user.** This is an evidence-based binary/datapack repair, not a claim that all game-runtime defects have disappeared.

## Why the Test8.6 log warned
The user's actual 7,958-line `latest(20261010-042806).log` had **214 Lithostitched `Couldn't find template pool reference`** warnings:
- **212** refs to invalid/empty path **`minecraft:`** at repeated structure-connector coordinates (111 unique including the angler refs; many repeated because chunks get processed again).
- **2** refs to nonexistent **`minecraft:angler_additions_3_pool`** at (87, 72, −1297). In pinned `FarmersStructures-1.0.6-1.21.1_neoforge.jar`, these originate from `cook_houses/cook_additions_3_2.nbt`, not an angler structure. Its native valid cook additions pool is `farmers_structures:cook_additions_3_pool`; Test8.6 already defined **`minecraft:cook_additions_3_pool`** alias with all nine native original elements. Test8.8 adds a second exact alias for mistyped `minecraft:angler_additions_3_pool` pointing to those same nine existing room choices, maintaining their processors, weights and names.

## Where blank minecraft colon refs originate
**Audit A**: [complete indexed source inventory](https://github.com/alsynth/AmbientOdyssey/actions/runs/38024711770) checked the **205** JARs in the existing resource index. 72 were candidate structure JARs; **66** had exact CurseForge metadata and downloaded binaries matching the audited installed SHA256. Native compressed NBTs were decoded and jigsaw blocks checked. Found:
- **264** malformed blank outgoing terminal connectors in `adventuredungeons-neoforge-1.21-1.3.1.jar` (Bygone Dungeon, Cold Lair, Ruins, Trial Rooms, etc.).
- **6** in `irons_spellbooks-1.21.1-3.16.3.jar`.
- **1** in `block_factorys_bosses-2.1.2-neo-1.21.1.jar`.
- **0** in 63 other mapped jars, subject to metadata/index coverage.

Every one of these **271** has **`pool=minecraft:`** and **`target=minecraft:`**, but its incoming matching connector **`name` is valid**. These are **malformed terminal endpoints** (unused outgoing branches) rather than evidence of missing room templates. `final_state` correctly restores the intended block (air, cobblestone, etc.).

**Audit B**: [previously-unmapped native JAR coverage](https://github.com/alsynth/AmbientOdyssey/actions/runs/38025157215) downloaded Additional Structures, Create Structures Arise, Create Easy Structures, Archaion and Explorify exact file versions. All five except Create Easy had no other empty refs. Create Easy had **2** more malformed `pool=minecraft:` in `schiene_freight_end.nbt` and `weg_freight_end.nbt`; **their targets are real `create_easy_structures:schiene` and `create_easy_structures:weg` values**, so preserve those valid targets. `Structory Towers 26.2 v1.0.17` was the sixth unindexed candidate but is excluded from the actual pack because of its invalid-mod-file crash. Totals now **273** across **four** installed mods.

**Audit C**: [new-addon completeness scan](https://github.com/alsynth/AmbientOdyssey/actions/runs/38025365856) probed 51 later-pinned addon JAR entries, successfully opened 46 and parsed 1,115 native structure NBTS. Found only those same **two** Create Easy malformed endpoints, nothing additional. The five unreadable mod downloads were BWG, NeOculus, AAA Particles, Borderless Window and Iron's Jewelry; these are not known new jigsaw structure providers, but they are a recorded audit coverage limitation, not falsely counted as clean.

## Exact source-locked correction implemented

**Test8.8** uses `compile_terminal_jigsaws_087.py` only in the private pack builder:
- Download four exact CurseForge versions and enforce their **original installed SHA256** from Audit A / Audit B.
- Decode each affected NBT; only replace invalid outgoing `pool=minecraft:` with vanilla **`pool=minecraft:empty`**.
- When `target=minecraft:` also invalid (271 cases), normalize to **`target=minecraft:empty`**. When target already valid (two Create Easy freight ends), **leave target exactly untouched**.
- **Never edit** any incoming connector `name`, block palette, position, block/entity data, loot, structure shape, processors, original other connector links or dimensions.
- All generated NBTs undergo semantic re-parse/roundtrip and an original-equality check with only their approved outgoing connector fields reverted. Every native JAR and exact count must match, otherwise **fail the build** rather than silently use guessed or updated assets.
- Include 273 Paxi datapack NBT overrides in the PRIVATE import, alongside **one exact Farmer's angler JSON alias** and the earlier Test8.6 repairs. Paxi `ao_worldgen_final_fixes` priority was already confirmed loaded in actual Test8.6 client runtime. Do not replace `minecraft:empty` with an invented structure.
- Preserve the existing Better Bastions / Luki Woodland Mansions two CurseForge project IDs and pinned private NeoReefRedux Modrinth jar; the rest of worldgen and performance settings are unchanged.

**Important future public publishing constraint:** Generated replacement NBT data derives from third-party JARs. This tested PRIVATE ZIP is not assumed to be redistributable publicly until each mod's assets/license and CurseForge's moderation policy are reviewed. The builder scripts distribute metadata/source derivation logic, not the downloaded JARs.

## Independent checks and predictions

Automated [Test8.8 build and reproducibility run](https://github.com/alsynth/AmbientOdyssey/actions/runs/38025321141) is the record of exact checks:
1. Existing **28** Test8.4 terrain/biome/dragon source assertions unchanged.
2. Existing **31** Test8.6 Archaion/Farmer/Create generator assertions, including new angler alias.
3. Native binary SHA256 + **273** exact malformed terminal connectors matched against author JARs, and every altered NBT was re-parsed with content preservation assertions.
4. Real ZIP CRC/manifest/NeoReef checksum/267 CurseForge refs and **273** datapack NBT overrides.
5. Independent parse of all **273** archived NBTS, verify each offending pool resolved to `minecraft:empty`, preserve Create Easy valid targets, and angler alias remains native nine-element equivalent.
6. Bit-identical second build: the ZIP's entire bytes and SHA256 must match across two independent builders using the same source pin/config.
All checks have to be successful before declaring static work complete; the CI record—not this page's existence—is the source of the pass/fail result.

**Prediction:** The entire class of previously observed `minecraft:` **terminal connector warnings** should be eliminated when the loaded datapack takes precedence in newly generated chunks; all observed `minecraft:angler_additions_3_pool` warnings should also be eliminated by the verified alias. The source-level cause is fixed with **high confidence**, but a clean future Minecraft log is the only definitive runtime verification of loader priority in every structure and previously generated chunks. Do not claim a zero-warning game run or automatic repair of existing world chunks. Unrelated `Dungeon Crawl` spawner block-entity warnings, Repurposed city required pieces, render/loot/POI warnings and server generation stalls are **not part of this correction**.

**No user intervention or additional exploratory tests are required for this source-audit task.** Keep the previous successful Test8.6 profile as rollback and treat the new ZIP as a *private source-verified candidate*, not frozen worldgen.
