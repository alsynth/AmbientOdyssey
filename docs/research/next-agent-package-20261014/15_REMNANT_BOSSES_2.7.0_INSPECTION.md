# Remnant Bosses 2.7.0: direct jar inspection (14 October 2026)

Source: `remnant_bosses-neoforge-1_21_1-2_7_0.jar` uploaded by the owner (mod id `remnant_bosses`, version 2.7.0, Apache-2.0, author NAIZO, 280 files). This is the installed version, so it replaces the 2.6.1 scan.

## Findings (read from the jar and the live config)
- **No worldgen data at all:** no structures, structure sets, template pools or dimensions. The data folder holds only tags, loot tables, recipes and two NeoForge biome modifiers (rat spawns). **Ossukage, Kotsukage, Umbrakar and Hollow Sovereign cannot have arenas that generate with the world.**
- **Summoning is a ritual:** craftable `ancient_altar` (3 chiseled deepslate + diamond + 2 emerald + 1 chiseled deepslate) and `ancient_pedestal` blocks; classes `SovereignRitual`, `RitualInfo`, `BossHunts` (a boss journal). Each boss has an activation item and four pedestal offerings in `config/remnant/bosses/<boss>_summon.json`.
- **Natural spawns exist only for minions** (rats via biome modifier, wraiths via config), not bosses.
- **Config is native and complete** (JAUML library, installed: `jauml-neoforge-1.21.1-2.3.1`). Every stat and ability damage is a key.

## Live values in AO (`config/remnant/`)
| Boss | Entity | Health | Attack | Armor | Ritual (activation item; four pedestal blocks) |
|---|---|---|---|---|---|
| Ossukage | `remnants:ossukage` | 800 (phase 1), phase 2 at 50% | 7, then 9 | 6, then 8 | nether_star; skeleton_skull x4 |
| Kotsukage | `remnants:kotsukage` | 700, phase 2 at 45% | 12, then 16 | 8 | wither_skeleton_skull; bone_block, soul_sand, soul_soil, nether_wart_block |
| Umbrakar | `remnants:umbrakar` | 750, phase 2 at 40% | 14, then 18 | 10 | echo_shard; amethyst_block, crying_obsidian, end_stone, sculk |
| Hollow Sovereign (not in the tier plan) | `remnants:hollow_sovereign` | 950, phase 2 at 45% | 16 | 8 | heart_of_the_sea; bone_block x2, skeleton_skull x2 |
Ability damages are separate keys (for example Umbrakar bite 16, slam 18, tail 15, orb 8, roar 8; Kotsukage swipe 14, stomp 16, poison 10, trap 10; Hollow Sovereign slam 20, beam 24, eruption 18).

## Consequences
- Not worldgen-dependent: no arena to verify, nothing to freeze for these bosses.
- **World-sourced ritual materials:** Umbrakar needs echo shards and sculk (Ancient City / Deep Dark, Overworld) and end stone (the End); Kotsukage needs a wither skeleton skull and Nether blocks; Ossukage needs a Nether Star. The Overworld pregeneration must contain an Ancient City.
- Health is below the 1024 cap for all four.

## Side observation
The 14 Oct game log shows one `AccessDeniedException` (Windows file lock on a temporary file) while JAUML saved `config/remnant/spawning/...` at startup. It happened once and the existing config loaded; it is a local filesystem event, not a pack defect.

## Not this mod
The second upload, `eternal_starlight_delight-neoforge-1_4_0.jar`, is **Eternal Starlight's Delight** (a Farmer's Delight addon, MIT). The boss mod is `eternalstarlight-0.9.1+1.21.1+neoforge.jar`, still needed.
