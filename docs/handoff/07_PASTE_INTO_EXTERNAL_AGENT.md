You are the implementation agent for the Ambient Odyssey Minecraft 1.21.1 NeoForge 21.1.252 modpack.

Extract the supplied external-agent handoff ZIP. Read `00_Instructions/START_HERE.md`, `01_TEST6_IMPLEMENTATION_BRIEF.md`, `02_POST_HANDOFF_DECISIONS.md`, `03_TEST7_BIOME_QUEUE.md`, `04_BUILD_AND_VERIFY.md`, then `03_Reference/TODO.md` and audit reports.

IMPORTANT: `01_Current_Audit1/Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip` is the latest editable *statically verified* source. The two original Test 5 ZIPs under `02_Original_Test5_Baseline` are untouched rollback. Reproduce the audit1 source/build BEFORE editing and preserve all its completed repairs. Do not start from Test4 or apply a second Farmers density multiplier.

Your immediate job is **Structure Test 6**. Integrate exactly eight approved structure mods once their original binaries, loader compatibility and dependencies are verified; preserve restrictions, especially Explorify's Nether Black Spiral. Raise Overworld WDA major frequency modestly to 0.80 without changing the End; keep Bathhouse unchanged; check ordinary WDA buildings; ensure WDA Mushroom Village is rare and exclusive to Mushroom Fields in a dedicated owner set; validate Farmers' actual settings and modded-biome structure eligibility. Avoid duplicate grids and synthetic jigsaw pools. Do not implement Test 7's biome additions yet: they are only documented for the next phase.

Return deterministic, validated source and CurseForge import ZIPs, changelog, machine-readable validation and SHA-256s. Distinguish implemented, statically checked, in-game checked, not tested and blocked. If blockers prevent a complete Test 6, make the largest valid intermediate delivery possible without pretending the blocked parts passed or silently omitting mods.
