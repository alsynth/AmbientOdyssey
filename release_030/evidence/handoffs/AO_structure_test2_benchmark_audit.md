# Ambient Odyssey — structure-test2 benchmark audit

- Locate operations recorded: 164
- Distinct structures: 22
- Median locate time: 3,122 ms
- Mean locate time: 8,552 ms
- Maximum locate time: 141,631 ms
- Locate calls > 10 seconds: 36
- ModernFix watchdog incidents: 9

## Slowest structure searches

| Structure | Searches | Median ms | Worst ms |
|---|---:|---:|---:|
| `dungeons_arise:kisegi_sanctuary` | 8 | 5,434 | 141,631 |
| `dungeons_arise:infested_temple` | 9 | 10,060 | 107,522 |
| `dungeons_arise:coliseum` | 8 | 9,930 | 55,427 |
| `idas:ruined_fort` | 8 | 8,193 | 43,127 |
| `idas:pillager_fortress` | 8 | 10,601 | 40,998 |
| `dungeons_arise:heavenly_challenger` | 8 | 7,678 | 32,766 |
| `towns_and_towers:village_forest` | 8 | 19,348 | 29,939 |
| `graveyard:medium_graveyard` | 8 | 2,970 | 20,942 |
| `idas:ars_nouveau/archmages_tower` | 8 | 6,522 | 15,946 |
| `integrated_villages:tavern_village` | 8 | 3,858 | 15,669 |
| `cataclysm:frosted_prison` | 8 | 5,473 | 14,318 |
| `dungeons_arise:keep_kayra` | 9 | 2,195 | 12,060 |
| `idas:haunted_manor` | 8 | 3,728 | 8,766 |
| `skyarena:ice_arena` | 8 | 3,140 | 6,983 |
| `philipsruins:ancient_towers` | 8 | 750 | 6,429 |
| `graveyard:large_graveyard` | 8 | 2,166 | 6,192 |
| `pasterdream:shadow_world_door` | 1 | 2,772 | 2,772 |
| `block_factorys_bosses:sandworm_nest` | 8 | 67 | 2,595 |
| `bosses_of_mass_destruction:lich_tower` | 8 | 1,576 | 2,571 |
| `cataclysm:acropolis` | 8 | 1,204 | 2,158 |
| `illagerwarship:warship` | 8 | 320 | 2,089 |
| `pasterdream:dream_church_10` | 1 | 2,037 | 2,037 |

## Interpretation

- Locate timings measure command search latency, not direct structure generation cost.
- The nine benchmark origins are widely separated; already generated chunks around some locations cannot be assumed to make all searches faster.
- Watchdog reports and long searches show that this remains an expensive benchmark workload; do not infer ordinary server tick performance from these timings alone.
- Compare against an earlier benchmark only after extracting matching structure IDs and matching origin coordinates.
