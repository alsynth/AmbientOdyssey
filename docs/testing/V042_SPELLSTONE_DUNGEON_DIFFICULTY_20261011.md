# Ambient Odyssey v0.4.2 — Spellstone + Dungeon Difficulty combined repair

**Branch:** `experimental/v042-spellstone-dungeon-difficulty-combined-20261011`. Private CurseForge import, 330 exactly pinned third-party references. This extends the preceding v0.4.2 recipe/spawner/Questlog build without dropping its 15 original Mine Cells recipe conversions, 4 still-disabled recipes, Dungeon Crawl pending spawner NBT, exact optional air trade guard, Questlog v0.1.3, Hominid/Tan and Streams/Mine Cells bridges, the 32 manual FTB click-to-acknowledge tasks, Curios amulet support, and user-approved TREK/Create rarity.

## Attached log limitation

The newest log available in this chat is `latest(20261011-121133).log` covering 13:51–14:11 in the **earlier v0.4.1 Worldgen Safety and Data Repairs** profile. It predates both user Curios screenshots (14:29, 14:53) and the many-fix build. It has Enigmatic spellstone recipe category warnings but zero actual Dungeon Difficulty mod initialization. **It cannot explain the 2-current-HP mobs or verify today's new fixes.** Obtain the exact v0.4.2 test `latest.log` from the tested CurseForge instance.

## Reconstructed regressions from upstream source

### Spellstone

Enigmatic Legacy Plus 1.1.2 `ELCuriosDataProvider` registers Curios `spellstone` size **0**, and its registered item tag exists at `data/curios/tags/item/spellstone.json`. Previously some players acquire a spellstone slot via item-based unlocks. Our prior amulet compatibility only guaranteed `amulet` capacity >= 1. That does not guarantee a visible `spellstone` slot. The screenshots show the missing bottom-row slot compared with the older version.

This branch adds `data/curios/curios/slots/spellstone.json` through **the authoritative `compile_compatibility_031.py` compiler**, after it clears/rebuilds Paxi data. It requests `size:1`, `operation:SET`, `replace:false`, and the original author icon `enigmaticlegacyplus:slot/empty_spellstone_slot`. The amulet slot stays unchanged and normal Curios items remain owned by their original author tags. Source/file checks cannot guarantee a particular existing save's Curios unlock state; verify one slot in fresh + established disposable saves.

### Dungeon Difficulty

**Root cause 1 — packaged config was in the wrong directory.** Old final build wrote `overrides/config/dungeon_difficulty_v2.json`. Pinned Dungeon Difficulty 1.21.1 source uses `new ConfigManager<>("difficulty_v2",...) .setDirectory("dungeon_difficulty")`; installed modpacks confirm `config/dungeon_difficulty/difficulty_v2.json` is the real path. The old file was ignored, leaving default difficulty rules rather than our intended six-dungeon pilot. Final v0.4.2 packager and ZIP validator now require the correct nested path, reject the old one, preserve six zones and keep complete original settings.

**Root cause 2 — original selector was vanilla-only.** The former `entity_matches.type` matched only `minecraft:(zombie|skeleton|...)`, excluding enemies added by other mods. This branch retains that original vanilla whitelist, and adds selected ordinary monster families from Born in Chaos, Illager Invasion, Rotten Creatures, Creeper Overhaul, and Dungeon Crawl; regex excludes boss-like names. `entity_matches.attitude=HOSTILE` remains mandatory; global bosses and other dangerous content mods (Cataclysm, Iron's Spellbooks bosses, Mine Cells) are still excluded. This is intentionally not global scaling.

**Root cause 3 — once-only zone evaluation too early.** Original 3.9.2 `ServerEntityManagerMixin.onAddEntity` calls `EntityScaling.scale` on insertion. Its `EntityScaling.scale` saves `markEvaluated(dimension)` even when no matching zone exists. If a structure is not yet indexed while a freshly generated chunk spawns a mob, that mob is forever counted as evaluated and cannot receive correct difficulty later. New AO worldgen addon `0.1.3-experimental` subscribes only to server-side main-thread hostile mob join and, after +10 ticks, retries *the original Dungeon Difficulty scaler* iff no difficulty was previously applied, clearing only the no-zone evaluation sentinel. It can retry once more at +40 ticks if the first retry still finds nothing. No direct health or attribute replacement, no unsafe worker calls, no endless per-tick polling, no changed stats for successfully scaled mobs.

**2 HP symptom remains unverified.** Dungeon Difficulty's intended max-health modifiers are positive, and the mod's original scaler preserves **current/max-health fraction** while increasing max health. A mob with 2 *current* HP might be wounded, reflect its innate base HP, or be affected by a different spawn order. This patch deliberately does **not** indiscriminately heal or replace entity attributes. Please provide the new `latest.log`, mob type, max health, current health, and source of spawn to diagnose the 2 HP issue specifically.

## Single combined acceptance circuit

1. Install only the exact generated `Ambient-Odyssey-v0.4.2-SPELLSTONE-DIFFICULTY-COMBINED-TEST.zip` into a **new CurseForge profile**, not the GitHub artifact outer ZIP. Preserve the earlier Many-Fix and Recipes-Spawner-UI ZIPs for rollback; do not migrate active survival-world data.
2. Open Curios in a fresh game. The native spellstone icon must appear in addition to the amulet icon. Equip a legitimate Enigmatic spellstone, close/reopen, save/rejoin, and verify no slot disappears. Also inspect an older *backup copy* of your world if needed.
3. Spawn fresh ordinary vanilla hostile mobs in a newly generated Dungeon Crawl dungeon and WDA Keep Kayra; measure current and MAX health separately, base armor and damage. Check values outside these structures remain unaffected. Repeat with Born in Chaos/Illager Invasion mobs and a new second Dungeon Crawl dungeon. Avoid testing mobs spawned before the new build—Dungeon Difficulty stores a persistent evaluated/scaled flag.
4. Verify Cataclysm/other boss mobs were not incidentally buffed; pre-existing six-dungeon levels 2/3 unchanged. Restart world and generate another structure to test worldgen registration.
5. Run Create and Farmer's Delight integration recipes, inspect Dungeon Crawl spawner settings across save/rejoin, and open Questlog with Q tab at GUI scales 2 and 3. Both previous repairs are intentionally included unchanged.
6. Collect current version `latest.log`. If any new mobs spawn at <=2 current HP, record mob ID via `/data get entity <target> id` and both current/max HP via in-game debug or `/attribute`. If relevant, include a screenshot of health bar *before any combat* and whether spawned from a spawner or naturally.
7. Compare Spark profiles only under similar new-chunk travel patterns; the fixes are **not** presented as a proven performance improvement.

All GitHub build passes are **source / compilation / ZIP preflight** only until the user actually plays this specific import.
