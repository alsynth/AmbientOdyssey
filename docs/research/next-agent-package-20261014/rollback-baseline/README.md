# Boss config rollback baseline (14 October 2026)

Byte-exact copies of the 39 boss-related files of the owner's live instance `config/` folder (Ambient Odyssey - Full Experimental Pack through PR54), taken before any boss balance value was changed. Hashes: `SHA256SUMS.txt`.

**To undo any later change:** copy the file from here back over the same path under the instance's `config/` folder (keep the folder structure), restart the game, then check the hash (`sha256sum -c SHA256SUMS.txt` from the instance folder). Server-type files (`irons_spellbooks-server.toml`, `block_factorys_bosses-server.toml`, `cataclysm_spellbooks-server.toml`) may also exist in a world's `serverconfig` folder: restore that copy too if the world was created after a change.

Covers: Cataclysm, Cataclysm Spellbooks, Iron's Spellbooks, Bosses of Mass Destruction, F.D. Bosses, Bosses'Rise (block_factorys_bosses), Brutal Bosses, Eternal Starlight, Ice and Fire, Stronger Fire Boss, Remnant Bosses (config/remnant/**), Dungeon Difficulty, Apotheosis / Apothic Attributes / Apothic Spawners.
Not covered: Aquamirae and Archaion (no config file exists in the live instance), datapacks (Paxi), and any file outside `config/`.
