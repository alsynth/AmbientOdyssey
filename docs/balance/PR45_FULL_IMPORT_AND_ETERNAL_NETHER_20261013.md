# Full experimental import and resumed structure work

Complete private CurseForge import: `Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip`, SHA256 `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f` (154,378,233 bytes). Import as a new profile using CurseForge's Import option. No preceding profile is required; the importer resolves the manifest's official downloads. Minecraft 1.21.1 / NeoForge 21.1.252. This is a client experimental pack, not a dedicated-server package.

## Payload and verification

The root manifest contains 338 exact download references: 331 official mods and seven resource/shader packs. Seven unchanged inherited custom JARs are bundled in `overrides/mods`; expected physical production mod count is 338. The complete v049 export SHA256 `8643e31b8f086dfde6c9729643ac5b77c692edb38ac000e7186a767b996c67a9` supplies all prior compiled content. Every official cached mod/resource matches CurseForge metadata SHA1; all seven bundled JARs match the reconciled profile's SHA256. No saves, account metadata, server lists, logs or test addons are packaged.

Download references reconcile the nine local additions missing from that export (five recent additions plus Reliquified Ars Nouveau, Ars Delight and two Ars/Sophisticated integration mods), update Remnant Bosses to its already-installed 2.7.0 artifact and add Celestisynth 1.3.9. The only changed existing game-config files are DD's 53-rule candidate and the two already-authored particle/wildlife follow-up configs. Four default configs for recent additions are also included. Original difficulty and the two original performance configs are retained as reference rollback files under `AO_TEST_NOTES/rollback`.

The builder verifies ZIP CRC and every written archive member, preserves all other base entries byte-for-byte, preserves 52 quests and all prior manual/worldgen/loot content, and rejects incomplete or mismatched mod mappings. Native Questlog and FTB validators pass: 52 quests, 13 referenced chapters and 32 manual pages. Exact inputs and SHA values are in `pr45-acceptance-evidence/FULL_IMPORT_INPUTS.json`.

The archive was materialized from its overrides plus hash-verified cached official downloads in a disposable directory. Production launcher client startup, fresh flat-world join, save and clean exit pass with code 0. The instrumented check adds one separate test JAR, which does not ship. All 11 synthetic difficulty/exclusion/control checks pass; all 382 queried structure IDs register and all 192 selected resources exist. Celestisynth's queried Traverser, Star Monolith and Rainfall Turret entities register. Parsed DD settings match effective candidate fields after installed Gson null elision. Evidence: `FULL_IMPORT_RUNTIME_RESULTS.json` and `FULL_IMPORT_RUNTIME_MARKERS.txt`.

The CurseForge UI import itself was not driven. Native results cover startup and controlled synthetic rules, not Celestisynth weapon combat, natural dimensions/structures, elite stacking, existing-save migration, dedicated server or multiplayer. The earlier 337-JAR Celestisynth status is historical; this new full-import rehearsal establishes limited native loading. Full acceptance remains incomplete. The inherited Simply More stun/target-dummy crash and requested flashing fix remain separate unfinished work; this package does not claim those repaired.

## Structure work resumed

Eternal Nether's exact installed JAR SHA256 is `9680efb45ec51250da820b8d525ab739fe0210458651ea87f13c3de9b2691a93`. All 30 NBT templates decode without errors; 24 native pools trace without unresolved pool/template references. The audit now follows `minecraft:feature_pool_element` references as well as NBT locations. Features are important encounter sources, not missing templates.

| Structure | Reachable NBT templates | Ordinary spawner evidence | Other native controls | Tier |
| --- | ---: | --- | --- | --- |
| `eternalnether:catacomb` | 19 | One Wither Skeleton spawner | Catacomb weighted mob feature, prisoner/Wither Skeleton feature references | Unassigned hold |
| `eternalnether:citadel` | 5 | None | Warped Enderman feature; native monster spawn override | Unassigned hold |
| `eternalnether:piglin_manor` | 2 | None | Indoor weighted mobs and outdoor mounted mob feature; native spawn override | Unassigned hold |

Native `ModFeatures`, `MobFeature` and `MobPassengerFeature` bytecode confirms that features create/finalize mobs, make them persistent and insert them into the generated level. Piglin Manor's indoor weighted list uses Piglin Hunter weight 1 and vanilla Piglin weight 3. Catacomb's list uses Corpor 1, Wither Skeleton Knight 2, Wraither 3 and vanilla Wither Skeleton 1. Those are native feature-selection weights, not tier decisions or complete encounter population odds. Outdoor Piglin Manor uses a Piglin Hunter/Wither Skeleton Horse combination. No NBT equipment marker alone captures that mechanic.

Observed template loot references include `eternalnether:chests/catacomb/treasure_rib`, `eternalnether:chests/citadel` and Piglin Manor's shared `minecraft:chests/bastion_hoglin_stable`. The shared vanilla table must not be globally retuned as if exclusively owned by the new manor. Full graph and inspected bytecode are committed under `pr45-acceptance-evidence/ETERNAL_NETHER_*`.

Next structure acceptance needs natural Nether placement/assembly and actual spawn/loot measurements, entity stats and equipment/elite interactions before proposing tiers. Keep the three separate holds and all existing approved tiers. No loot wrapper, quest gate or difficulty rule for these three sites is enabled by the import.

## Reproduce

`tools/package_pr45_full_import.py` requires the exact base export, the profile's local CurseForge metadata, the frozen 337-JAR snapshot and the hash-pinned Celestisynth JAR. It only reads that metadata and writes filtered pin/hash records, never the original metadata file. `tools/prepare_pr45_full_import_rehearsal.py` materializes a new directory under repository `build/` from the import and verified cached downloads. Use the existing isolated native launcher helper with the separate client-only probe.

`tools/audit_eternalnether_followup.py` uses the existing streaming NBT reader with nbtlib 2.0.4. It changes no JARs, templates, native feature definitions or tier assignments. Its resource closure establishes source reachability, not actual selection, assembly or gameplay completion.
