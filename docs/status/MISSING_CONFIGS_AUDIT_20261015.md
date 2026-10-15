# Missing-configs audit (15 October 2026)

**Result:** no config needs porting into source. The configs in the pushed profile copy (`7177883`, folder `Ambient Odyssey v0.4.9.1 … TEST (1)/`) are either older AO source versions that R4 replaced, Sky Arena files (removed by owner decision), or local launcher files. One file, the DD config, is a 53-zone pilot with End and Nether zones. It contradicts decision 5.5 (Overworld-only, 30 zones), so it must **not** be ported.

**Status:** static, read-only. Compared each file's git blob with source at `fix/source-r4-parity` (`3bd6f1b`; source = R4 bytes, 0 real differences) and searched all history for the same blob.

| Profile file | vs source | Where this exact version came from | Action |
|---|---|---|---|
| `config/block_factorys_bosses-server.toml` | differs | older AO source (`956d696`) | none, R4 newer |
| `config/brutalbosses.json` | differs | older AO source (`956d696`) | none, R4 newer |
| `config/cataclysm-common.toml` | differs | older AO source (`956d696`) | none |
| `config/irons_spellbooks-server.toml` | differs | older AO source (`956d696`) | none |
| `config/lootr-common.toml` | differs | older AO source (`956d696`) | none |
| `config/bosses_of_mass_destruction.json5` | differs | rollback baseline (`138259f`) | none |
| `config/iceandfire/iaf-common.json` | differs | rollback baseline (`138259f`) | none |
| `config/remnant/bosses/{kotsukage,ossukage,umbrakar}.json` | differ | rollback baseline (`138259f`) | none |
| `config/paxi/datapacks/ao_flight_balance/…/advanced_ring.json` | differs | older AO source (`ca244ef`) | none |
| `config/paxi/datapacks/ao_flight_balance/…/basic_ring.json` | differs | older AO source (`d535013`) | none |
| `config/dungeon_difficulty/difficulty_v2.json` | differs | **not in any source commit**: 53 zones (46 Overworld, 2 End, 5 Nether) vs R4's 30 Overworld-only | **don't port**; contradicts 5.5 |
| `config/sky_arena.json`, `config/skyarena-common.toml`, `config/cristellib/skyarena/*` (2) | missing | Sky Arena, removed (issue 58) | none |
| `AO_TEST_NOTES/FULL_IMPORT_INPUTS.json` | missing at this path | import note; R4 ships its own corrected copy | none |
| `minecraftinstance.json`, `.curseclient` | missing | CurseForge launcher files | none; don't track |

## The other direction (R4 configs absent from your local profile)
The local profile is pre-R4, so it lacks every R4 change: 30-zone DD, Brutal 70/30/×4/×3, 51 native boss fields, and Solo Quests `teamSyncEnabled=false`. The fix is checklist D1: import R4 as a **new** profile. Don't copy files into the old one.
