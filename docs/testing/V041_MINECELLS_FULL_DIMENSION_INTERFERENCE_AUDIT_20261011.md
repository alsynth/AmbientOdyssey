# Ambient Odyssey v0.4.1 — Mine Cells dimension protection audit
Date: 11 October 2026
Branch: `experimental/v0.4.1-minecells-dimension-guards-20261011`
Status: **static-preflight candidate, NOT runtime validated**.

## New decisive control
The user tested **the same Mine Cells + Sinytra Connector stack in a minimal NeoForge modpack** and the dungeon worked flawlessly. So stand-alone Mine Cells and the bridge are confirmed functional in that configuration. The failure in Ambient Odyssey is caused by some element of the full modpack integration or its data/state, but the exact conflict remains unproven.

## Primary concrete exposure: Tan's Huge Trees
- In the exact AO log `latest(20261010-222142).log`, `wover-generator` enumerated the Mine Cells Prison `FlatLevelSource` with feature provider `tanshugetrees(1)`. At about 00:20:04 the THT mod scans **five Mine Cells Prison regions**, which should not be needed in a closed dungeon.
- Tan's open source for the active 1.21.1 NeoForge line, `TannyJungMC/TansHugeTrees`, registers `data/tanshugetrees/neoforge/biome_modifier/world_gen_before_plants.json` with `"biomes": {"type": "neoforge:any"}` and adds `tanshugetrees:world_gen_before_plants` in `underground_decoration`.
- That feature runs `TreeLocation.start` and `TreePlacer.start`; source shows region scans and worldgen state independent of whether a tree actually gets placed. It is positively confirmed to **execute in the dungeon**, not proven to cause Mine Cells structure failure.
- This pack overrides precisely the **same registry path**, preserving the native THT feature and generation step, but swapping its biome holder set to `{"type":"neoforge:not","value":[<all five Mine Cells biomes>]}`. NeoForge 1.21.1's NotHolderSet supports that exact codec. Thus THT stays in *all other biomes*, including AO's overworld, Nether and non-Mine Cells dimensions.
- Code: https://github.com/TannyJungMC/TansHugeTrees/blob/1.21.1/src/main/resources/data/tanshugetrees/neoforge/biome_modifier/world_gen_before_plants.json
- API: https://aldak.netlify.app/javadoc/1.21.1-21.1.x/net/neoforged/neoforge/registries/holdersets/notholderset

## Additional dimension-level protections
- Streams Reflowing was logging watershed preparation inside `minecells:prison` (even when it found zero streams/lakes). Its official 2.14.x `#streamsreflowing:no_streams` tag is included for all five Mine Cells biomes, preventing generation of waterways within the dungeon. **This does not suppress all of Streams' precomputation or global mixins**, and a previous 5-biome no_streams-only isolation test *still produced no dungeon*. We cannot claim it resolves the issue.
- Use separate, non-compiler-owned `ao_minecells_dimension_guards` datapack in Paxi. The AO compatibility compiler recursively clears its **own** `ao_compatibility/data` tree; the new guard files survive rebuilding. The archive validator checks the exact Paxi paths.
- `#ambient_odyssey:minecells_protected` lists five canonical Mine Cells biome IDs as a reusable scope reference. Merely creating this tag does not apply a magical blanket exclusion to other mods.

## Audit of other full-pack suspects and dimension impacts
| Participant | Observation / code behavior | Decision |
|---|---|---|
| Mine Cells 2.0.3 + Sinytra + FFAPI + CCA + owo | Minimal NeoForge control works; AO transport works; AO dungeon broken | **Keep exact pins.** Protect custom native structure_set salts and placement codecs |
| Tan's Huge Trees 1.8.0 beta | Provably injects a heavy worldgen placed feature into **every** biome and scans Mine Cells | **Fix direct biome modifier**, all five Mine Cells biomes |
| Streams Reflowing 2.14.4 | Region precomputation logs in Prison; no river/lake networks in sampled plates | Add official `no_streams` tag, **do not assert complete hook bypass**; keep overworld rivers |
| Structure Essentials 5.0 | Log reports native duplicated Mine Cells salts; AO config has `minimumStructureDistance.enabled=false`, `autoBiomeCompat.enableBiomeCompat=false`, `spacingSeparationModifier=1.0`; search optimizations remain global | Cannot reliably exclude a dimension with this version's configuration; keep for now rather than pretending the settings block mixins. No salt rewrites |
| Noisiumed 3.0.6 NeoForge | Optimizes terrain/noise generation. Mine Cells Prison uses `FlatLevelSource`, not `NoiseBasedChunkGenerator` | No documented dimension blacklist; **not** an established cause; keep the native jar rather than changing many other dimensions |
| FreeTerraForged / ReTerraForged preset | Overworld terrain; user's Prison is a native `FlatLevelSource` | No Mine Cells injection evidenced; leave terrain baseline |
| WoVer surface/biomes | Log enumerates all dimensions but reports added surface-rule merge for **minecraft:the_end**, not Prison | Leave End system intact |
| TerraBlender | Log reports initialization in Aether, Overworld and Nether only | No evidence it changes Prison |
| Biolith | Explicitly says it **ignores minecells:prison** because the dimension type is unknown | Already excluded |
| Apotheosis | Six feature entries appear in some other Mine Cells dimensions, **not Prison** (Prison feature namespaces were `tanshugetrees(1)` and `none(9)`) | Monitor other Mine Cells stages; avoid unsupported global removals |
| Lithostitched / Integrated Patches | Installed, can change structures/features, but AO's own compatibility datapack has no `minecells:*` structure set/templat e rewrite; `integratedpatches` log concerns `generic_structure` | No blanket dimension exclusion inferred from configs. Review only if protected profile still fails |
| Other structure-heavy mods (Trek, WDA, DnT, CTOV etc.) | Their structure biome selectors do not itself imply they operate inside Mine Cells; AO structure curation does not reference Mine Cells | Preserve structure content and do not disable globally |
| ModernFix/Lithium/Sodium related optimizations | Warning: failed cache key for concentric structure placement; unrelated mixin conflict for chunk tickets | Not enough evidence of Mine Cells grid corruption. Avoid speculative toggles |

## Why this is the maximal **grounded config-only** exclusion, not a proof
A datapack biome filter affects biome features/streams. It cannot protect a **dimension** against arbitrary mixins in Structure Essentials, Noisiumed, ModernFix, other global structure placement optimizers or the Minecraft chunk executor. These need *mod-specific code or removal* when no dimension blacklist is exposed. Writing fictitious config keys would silently do nothing.

The Mine Cells Prison structure is custom `minecells:better_random_spread` with `minecells_spacing=1`, `minecells_separation=0`. Its upstream Prison grid builds `addFloor(random, cursor, 3)` and a `PROMENADE` exit. Do not change its native structure-set salt, structure ids, Jigsaw pools, surface, or doorway coordinates.
Source: https://github.com/mim1q/MineCells/tree/minecells-2.0.0%2B1.21.1/src/main/java/com/github/mim1q/minecells/structure/grid

## Runtime acceptance
Import as a new instance (not layered onto a prior profile), use a **fresh** disposable world / ungenerated Mine Cells dungeon region, and check entry not suffocating, three-level progression, connected traversable floors, and the exit doorway to Promenade. If it fails, the next escalation is inspect full loaded mod binaries / mixin lists to implement a specifically scoped source fix; do **not** keep guessing which mods to delete. The **runtime success remains unconfirmed** even when CI passes.
