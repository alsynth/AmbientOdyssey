# Test build and rollback (DRAFT)

## State of the experimental build
**There is no balance build yet**: no boss value has been changed, so the changed-files list is empty. What exists is research and tooling on the branch `research/v05-boss-dungeon-loot-capability-20261013` (delivered as `boss-dungeon-loot-research.patch`): boss measurement datapacks, the arena check, parsers, tests and documents. It touches no game configuration.

## Rollback baseline (exists now)
`rollback-baseline/` holds **byte-exact copies of the 39 boss-related config files** with SHA-256 hashes, taken before any change. To undo a later change, copy the file back over the same path under `config/`, restart, and verify with `sha256sum -c SHA256SUMS.txt`. Server-type files may also live in a world's `serverconfig` folder: restore that copy too.

## How a change will be made and undone
1. Each change is an edit to one baseline file or a new datapack, listed in the ledger's `changed_values` and `implementation_method` columns and in a changelog with before and after hashes.
2. Experimental builds are separate branches and patches (`git am` to apply, `git revert` or deleting the branch to undo); nothing is merged into the main modpack automatically.
3. A new world is needed to test changes to SERVER-type files or to anything applied at generation (see the Brutal Bosses findings, section 13).

## Planned change surface (files that balance work would touch)
| Mod | File | What it controls |
|---|---|---|
| Cataclysm bosses | `config/cataclysm-common.toml` (`mobs.<boss>`) | health and attack multipliers, ability damages |
| Iron's (Tyros, Dead King) | `config/irons_spellbooks-server.toml` | additional health, attack damage, spell power |
| Bosses of Mass Destruction (Obsidilith) | `config/bosses_of_mass_destruction.json5` | health, armor, attack |
| F.D. Bosses (Chesed, Malkuth) | `config/fdbosses/bosses.json` | ability damages, hit counts, difficulty multipliers |
| Bosses'Rise | `config/block_factorys_bosses-server.toml` | health, armor, damage per boss |
| Remnant Bosses | `config/remnant/bosses/*.json` | every stat, ability damage and ritual |
| Eternal Starlight | `config/eternal_starlight.json` | health, armor, damage scale, respawn |
| Ice and Fire | `config/iceandfire/iaf-common.json` | dragon and hydra health and damage (shared by species) |
| Brutal Bosses | `config/brutalbosses.json` | spawn chance, spacing, global multipliers |
| Any boss | a datapack or the later damage-scaling addon | what the config cannot reach |
Aquamirae (Cornelia) and Archaion (Last of Deepslate) have **no config file** in the live instance: their stats can only change by attribute or code.

## Validation that exists
- `python -m unittest discover -s tests` (the suite has 2 unrelated failures and 2 unrelated errors from before this work; the boss tools' tests pass).
- Static: arena inventory, config snapshot hashes, ledger rebuild (`python tools/aob_build_handoff.py`).
- In game (owner): `AOA-arena-locate-datapack.zip` for arenas, `AOT-edit-test-datapack.zip` for boss stats and damage; guides included.

## What 'implemented' will mean
**Implemented and statically validated** (config parses, hash and diff recorded); **runtime-tested** only after an in-game measurement with the AOT datapack; a boss whose config parses or whose game starts is **not** runtime-tested.
