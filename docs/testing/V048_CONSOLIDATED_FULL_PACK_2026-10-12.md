# v0.4.8 full-pack gem/Whaleborne log test

The owner supplied Apotheotic port `0.4.8-prototype` for a full-pack diagnostic
run while Claude continues its unfinished implementation. Do not substitute the
older four-dependency gem-only kit or call this a completed port.

## Exact composition

- Exact v045.1 armor/Q fixed full import as base, SHA-256
  `fa775ce9ebc3dec4b6c70e50d5c3bf0dab0117c28bb80c3e6bf7b2cdbe0a8364`.
- All **330 original CurseForge pins**, assets/configs/quests preserved.
- **Whaleborne 1.2.5**, Minecraft 1.21.1 native NeoForge, CF **1272075:8914201**;
  331 total project references. Official CurseForge and Modrinth binaries matched
  byte-for-byte. Native metadata requires only MC/NeoForge; the three library/UI
  integrations are optional. Native spawn modifier selects `#minecraft:is_deep_ocean`,
  weight 1, one Hullback. No spawn tuning or extra libraries added.
- User's exact `ao-apotheotic-port-prototype-0.4.8-prototype.jar`, SHA-256
  `ddec6b79655bc5ff45979e88ef62df7c440646e6d48d6804e3e1476faba32f52`.
- Available latest local Wet Sand development artifact, SHA-256
  `fc7e84d341339f5ad88d9485ab6316b86edacfc9c1e9caccef2c562d0f3a5b49`.
- AO Affix Trims **0.1.1**, Questlog bridge **0.1.5**, worldgen safety **0.1.4**,
  Streams/Mine Cells bridge **0.1.0** inherited from the exact full base.
- Prototype dependencies match its supplied kit exactly: Apotheosis 8.9.0,
  Placebo 9.9.2, Apothic Attributes 2.11.0, Patchouli 93. Recommended RAM 10 GiB.
- Owner's checklist/optional QA datapack are in `overrides/AO_TEST_NOTES`.
  Cheap QA recipes are NOT automatically activated; no test-probe JAR ships.

## Checks and actual run

Archive CRC, unique/safe paths, exact binary hashes, required dependency pins,
331 unique project IDs, and byte-identical preservation of every unrelated base
member passed. Installed full-roster test snapshot had no duplicate top-level
NeoForge mod IDs. Third-party binaries are manifest references, not committed JARs.

**Native production client startup + world join + clean save PASS**, exit code 0,
against all 330 runtime JARs plus one isolated test-only probe. Used a disposable
flat world and offline identity, with actual full-roster configs/overrides, Java 21
and NeoForge 21.1.252. Live CurseForge profiles, source kit and saves were untouched.
No new multiplayer or natural ocean/dungeon gameplay certification is implied.

Native registry results: **9 rarities, 233 affixes, 58 gems** loaded. Two port
definitions were rejected, matching the owner's request for missing-ID diagnosis:

| Gem | Exact loader error |
| --- | --- |
| `ao_apotheotic_port:modded/depths` | `Failed to get element apothic_enchanting:earths_boon` |
| `ao_apotheotic_port:aether/aether` | `Unknown registry key ... minecraft:attribute: neoforge:elytra_flight` |

The supplied prototype is preserved unchanged for Claude's investigation. The
parse failures did not prevent world join. Other historical full-pack warnings
remain in the local complete log; they were not silently fixed in this build.

## Owner's settled scope

- Malkuth complete arena and Mine Cells portal/progression are user-verified.
- Dungeon Crawl spawner verification is for the next actual dungeon test/log.
- Keybind work follows gem/armor work. Other fixes follow this consolidated test.
- Four unwanted recipe routes remain disabled; do not delete their false-condition
  overrides, which would restore the native recipes. No loot/balance/quest overhaul.
- Claude owns ongoing gem-port work. This task packages and diagnoses that binary.

## Reproduce

`tools/package_v048_consolidated_test.py` requires explicit paths to the hash-pinned
full base, exact user prototype, Wet Sand and official Whaleborne binaries, original
kit folder and output ZIP. It fails closed on a changed dependency/input. Optional
`--log-report` embeds the plain diagnostic findings under AO_TEST_NOTES.

Output: `Ambient-Odyssey-v0.4.8-FULL-GEM-WHALEBORNE-TEST.zip`, with root
`manifest.json`. Its adjacent `.inputs.json` records final hash and size. Import as
a NEW CurseForge profile and use a throwaway world; send that profile's latest.log
after the test. Natural prototype gem drops are still intentionally disabled.
