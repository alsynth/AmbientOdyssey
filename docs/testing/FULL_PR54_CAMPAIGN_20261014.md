# Full PR54 + deferred-feature experimental import

Owner requested full combined experiments through PR54, expanded scope to deferred designs, and requested ZIP upload before further combined tests. The first ZIP is uploaded to an unpublished GitHub draft release.

Branch: `experimental/full-pack-through-pr54-20261014`, based on PR54 `03586c13477cdaa988660e25b5ad3962d1a5cfce`.

Base: exact PR50 `dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f`.
ZIP: `Ambient-Odyssey-FULL-PR54-CAMPAIGN-EXPERIMENTAL.zip`, 154480313 bytes, SHA256 `420527903f636c4b0b2f51afbfa94b975fb4bab2a46acb2ecc1df5133c1f0211`.
Draft release: https://github.com/alsynth/AmbientOdyssey/releases/tag/untagged-5833379202de8add5efd

Prototypes: PR51 loot overlay, PR53 weights, PR54 r19 Ancient alias correction; ao-campaign stun/flash suppression, provisional 10% Monstrosity Nether player-kill Rage Glove gate, per-player boss milestones, T6 Pinnacle access, first-clear native r19 gems and guarded held-item rarity upgrade. Campaign adds 101 entries / 7 chapters while preserving 52 existing quests / 13 chapters and 32 manual pages. 83 new entries are reading acknowledgements, 17 actual item/location/advancement objectives, one reserved End encounter. Not 101 verified gameplay tasks.

Packaging: 338 unchanged CF references, 10 custom JARs / expected 341 physical mods. Use `tools/compile_ao_v050_campaign.py`, compile addons, then `tools/package_ao_full_pr54.py` with exact PR50 base, native-CI starter JAR, Sigil 0.1.1 JAR and campaign JAR. Final ZIP/JARs stay outside Git.

Pre-upload evidence: base SHA and ZIP CRC/member readback; campaign compilation; corrected Sigil native tests pass after fixing missing template setup; existing 52-quest and 32-manual source checks pass. Combined startup, loot order, gameplay, UI, multiplayer and persistence NOT TESTED at upload.

Open implementation: third End boss / Geburah undecided; T6 alternate equivalence unproven; contribution-based party credit, five-class structure chest remapping, optional realm campaigns, measured boss attacks/scaling and Simply Swords damage proposals unfinished. Broad deferred-design request is partially implemented, not complete. Do not mark production ready.

## R2 after first native rehearsal

The first uploaded ZIP loaded and joined a disposable world, parsed 153 native quests, and shut down with exit 0. The synthetic probe failed on the incorrect `cataclysm:leviathan` ID. It did not complete the remaining checks. Native chapter loading reports 21 including Questlog's generated/default chapter, versus 20 configured chapter files.

Source-verified correction: `cataclysm:the_leviathan`. Added native Remnant 2.7.0 `remnant_bosses:ossukage`, `kotsukage` and `umbrakar` milestone routes; campaign addon bumped to 0.1.1. R2 is a separate ZIP, uploaded before its tests with explicit owner approval for corrected uploads to the same unpublished release.

R2: 154480384 bytes; SHA256 `8cfb456033f4b79d27862750a15f0a109379088cd0ca4f5a0d7ba511e1930b3a`. Runtime status pending.
