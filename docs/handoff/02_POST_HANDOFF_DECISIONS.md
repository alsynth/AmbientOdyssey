# Decisions recovered after initial Structure Test 6 handoff

**Authoritative specific decisions as of 9 October 2026.** These were not all present in the original user-pasted brief.

| Topic | Status | Specific decision / implication |
|---|---|---|
| Test sequencing | Confirmed | Structure Test 6 **before** terrain/biome Test 7; no combined rewrite. |
| WDA Mushroom Village | **NEW Test 6 requirement** | `dungeons_arise:mushroom_village` should generate **only** in Mushroom Fields, with rare dedicated set; remove from normal placements. Need actual registry/asset checks. |
| WDA Mushroom Village mobs/loot | Future combat balancing | Later make Piglins/Piglin Brutes much stronger and improve loot. Do not sneak into Test 6. |
| WDA majors | Confirmed | Only modest increase from 27/38 to 0.80 Overworld; preserve End frequency. Bathhouse unchanged. |
| Farmers Structures | **Already implemented statically in audit1** | ~2x candidate grids all 20 variants with dimension-aware protection; investigate real spawn acceptance, no second blind multiplier. |
| Eight approved addons | Pending, NOT installed | YUNG's Extras, Bridges; Structory: Towers; Archaion; Explorify; Additional Structures; Create: Structures Arise; Create: Easy Structures. |
| Corrected exact file selections | Superseded 9 October | Structory: Towers **v1.0.17 (CF 783522:8396885)** explicitly approved instead of 7078283; Explorify **8082824** unchanged. Runtime compatibility must still be checked. |
| Archaion | Dependency blocker to investigate | AAA Particles reported missing; check precise supported 1.21.1 NeoForge release/API. |
| Explorify | Superseded 9 October | User explicitly confirmed keeping Nether Black Spiral enabled provisionally, subject to testing actual Nether compatibility. |
| Test 7 warm/tropical biomes | Approved for **later** | BWG Tropical Rainforest; BWG Baobab Savanna; BOP Dryland. These are not yet incorporated in Test 5 audit1's 40+2 roster. |
| Test 7 cold/dry choices | Not decided | Stop further cold/dry selections pending Better Snowy Biomes: Enhanced inspection. Do not infer approval for an uninspected biome. The approval of BOP Dryland was earlier than the later decision to defer **additional** cold/dry tuning. |
| Block Factory's Biomes | Explicitly **rejected** | Do not add its biomes or mod. Distinguish from existing Block Factory's **Bosses** (different mod). |
| Current biome roster | Unchanged in audit1 | 40 curated Overworld + 2 Nether; Test 7 selections are queued, not yet merged. `03_Reference/CURRENT_BIOME_ROSTER.json` contains exact current list. |
| Integrated Stronghold | Retain | MTR stronghold OFF; MTR desert/jungle temple ON; MTR ocean-monument replacement OFF. |
| YUNG mines | Existing state | Test 5 audit1 master TODO retains YUNG's Better Mineshafts; Moog's Mineshafts Reimagined not selected. Do not arbitrarily reverse without live file evidence. |
| Other exclusions | Retain | No FDstructure; no StructureOverlapless; no extra Create structure addons; Big Globe, Luki's Crazy Chambers and Sunken Spires deferred; no Born in Chaos/companion mods. |

## Important changes since the original handoff

1. Test 5 **audit1** now exists and is the best working snapshot. It contains additional statically verified fixes; initial handoff predated them. No natural-generation test was claimed.
2. Expanded audit reports **196** audited resource snapshots (177 prior + 19 new), **26** unique binaries directly inspected in the continuation, **41** existing-profile JARs still unavailable; do not reuse obsolete '177 + 17 of 60' as the current state.
3. Older handoff's request to *perform* CTOV, Dungeons & Taverns, Cataclysm Spellbooks and Farmers repairs has partly been satisfied by audit1; review the new changelog before applying anything.
4. The eight new approved addon JARs were not supplied or installed. They must be downloaded and inspected independently by the recipient.
