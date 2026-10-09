# Ambient Odyssey — Structure Test 5 audit1 installation

Import `Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip` into a separate CurseForge profile. Its root manifest selects Minecraft 1.21.1, NeoForge 21.1.252 and the same 237 locked project/file pairs. The launcher downloads pinned mod JARs; this ZIP contains the manifest and overrides. The original Test 5 remains the rollback candidate.

The eight approved structure additions are staged, not installed. `APPROVED_ADDITION_JARS.txt` is their binary request list. `MISSING_JARS.txt` separately lists the 41 unavailable existing-profile audit inputs. Audit1's static build is complete without an in-game prerequisite; it has not been gameplay-accepted.

For later acceptance, create a fresh world using the comparison seed/settings. Choose Default world type and **Ambient Odyssey 0.3.1** in FreeTerraForged Customize. The preserved preset has continent scale 6500 and river count 15. Already generated chunks keep previous structures.

Check the enabled datapacks/log for `ao_compatibility`, `ao_structure_density`, `ao_structure_repairs` and `ao_biome_replacement`, and the client resource-pack stack for `ao_resource_repairs`. The repair resource pack comes from `config/paxi/resourcepacks/ao_resource_repairs`; it must load for the Traveloptics model overrides. Datapacks use format 48 and the client pack format 34. Restart after worldgen input changes.

Cristel creates its own runtime pack from native modfile data. Native toggle/config membership is now synchronized with AO extraction. Verify live pack priority and AO-only exclusion retention using launch/resource evidence; static catalogues do not assert that Paxi automatically wins all native collisions.

Later observations:

1. Record exact candidate ZIP hash, seed, preset, coordinates and underlying biome IDs; compare ordinary generation separately from locate searches.
2. Check ordinary IDAS/WDA sites, villages and Dungeon Crawl in Prairie, Flower Fields, Sakura and appropriate cool/forest donors. Confirm no natural Small Blimp/Coliseum and a retained, rarer Bathhouse.
3. Check Sky Villages above land and rivers: `minecraft:river`, `minecraft:frozen_river`, `regions_unexplored:muddy_river`, `streamsreflowing:stream`. A visible channel can use a land biome. Ocean biomes remain excluded by the retained village selector.
4. Check the three `ambient_odyssey:heavenly_challenger_overworld`, `ambient_odyssey:heavenly_conqueror_overworld`, `ambient_odyssey:heavenly_rider_overworld` definitions and the original End branches.
5. Inspect the original Foundry/Mechanical Nest/Cabin pool repairs, CTOV mountain outpost and Christmas sand waystone connectors, and the D&T mansion basement. Forced placement verifies assembly; it does not prove natural spawn frequency.
6. Sample appropriate Farmers variants in Overworld/coast/underground/Nether/Aether/Undergarden/Bumblezone without relocating optional absent-dimension variants. Record successes per sampled region rather than treating grid ratios as measured spawn counts.
7. Check Traveloptics rendered models/tags, Cataclysm Spellbooks recipe/loot loading and restored Artifacts/Enigmatic slots. Developer-test models and unrelated animation warnings remain pending.
8. Inspect clipping, overlap and resource winners, particularly vanilla village sets/taiga starts. Record exact structure/template IDs for remaining IDAS/Cook errors.

The original untouched Test 5 import SHA-256 is `abe813ca2765e83a6b5c8c75c9d159e7612ccaf6755143c6e646f322374c45e0`; source SHA-256 is `547223d454a3923b5711099f43a0aa92766d2d997042b379a2efaf9177fef43b`. Archive rollback preserves the old profile/settings. Current archive hashes, integrity and rebuild results are in the external validation summary/checksum file.

Terrain, trees, wildlife, Tan, Streams, TRMT, biome weights, options, controls and quests are preserved. The Tan open-field plan remains separate and unapplied. Follow the current master TODO for later content, runtime and release gates.
