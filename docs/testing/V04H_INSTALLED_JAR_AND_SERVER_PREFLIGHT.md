# Ambient Odyssey v0.4h — installed JAR and dedicated-server preflight

**Status:** preparation tooling committed; no production server build, multiplayer gameplay, or runtime compatibility claimed.

The existing **331-reference Questlog + Mine Cells CurseForge ZIP** validates manifest pins and bundled assets, but CurseForge downloads the actual mod JARs during import. The original v0.4 dependency audit had **23 metadata gaps**, mostly HTTP 403 access restrictions, and those must not be misrepresented as absent dependencies. The new script performs a read-only pass on JAR metadata already present in a local installed profile.

## After importing to a disposable profile

From a checkout of this branch, run:

\`\`\`bash
python tools/diagnose_v04_instance.py --profile "/path/to/CurseForge/Instances/Ambient Odyssey"
python tools/audit_installed_jars_v04.py --profile "/path/to/CurseForge/Instances/Ambient Odyssey" --report jar-audit-client.json
\`\`\`

On Windows use \`py -3\` if \`python\` is unavailable. No Internet connection is needed. The audit reads \`META-INF/neoforge.mods.toml\`, legacy \`META-INF/mods.toml\`, or \`fabric.mod.json\` without extracting or modifying the JAR. It reports top-level duplicate IDs, unreadable metadata and unresolved declared dependencies. It does **not** infer exact server sidedness from mod titles, guess mixin compatibility or verify transitive Jar-in-Jar libraries.

Once there is a **separately constructed, disposable dedicated-server installation**, compare it with the client:

\`\`\`bash
python tools/audit_installed_jars_v04.py --profile "/path/to/client" --server "/path/to/server" --report jar-audit-server.json
\`\`\`

The report highlights required gameplay IDs (\`questlog\`, \`minecells\`) missing from the scanned server and shows mod-ID differences. A client-only mod ID in the comparison means *only* that it is absent on the server; it is not proof the mod belongs exclusively on the client. Do **not** copy every client JAR to a server or remove flagged dependencies without checking the exact mod's loader metadata, support documentation and a real dedicated server launch.

Reports intentionally omit complete local paths, raw log lines, IP addresses and player names; they still include mod filenames, which are useful for support. Review before sharing.

## Decision gates

- **ZIP/source verified:** 331 official CF project references, exact Mine Cells/Questlog pins, 273 NBT patches, deterministic builds. Earlier 331-ref GitHub Actions evidence is preserved.
- **Installed profile metadata:** only verifiable after CurseForge downloads the 331 file references. Warnings on mods with bundled dependencies may be benign; duplicate top-level mod IDs require human inspection.
- **Dedicated server:** Java 21, explicit server-safe mod roster, datapacks/configs, two players, startup/restart/rejoin, Mine Cells and Dimensional Dungeons portals.
- **Inventory GUI:** Questlog screen-anchored journal button at trial X/Y=38/38; actual clickable placement and FTB/Curios/JEI overlap must be inspected from screenshots before accepting.

Do not adopt an untested world as the permanent server map; back up the known-good 330-ref and 331-ref artifacts and working player saves.

## Verified launch-readiness artifact (10 Oct 2026)

- Source commit: `72e71fa1e76b9e5500148fae2e7964e330d1b6a3`; GitHub Actions [run 38077302870](https://github.com/alsynth/AmbientOdyssey/actions/runs/38077302870) completed successfully.
- Private developer ZIP: **70,847,239 bytes**, SHA-256 `94cccade0b6e0624442b673cde12dac6ff1deeef3e9c48bc182be806da97a06e`.
- CurseForge reference-only ZIP: **70,774,689 bytes**, SHA-256 `e2686946ef6d3b76db833663280b54138570b32d5e70483d20ffa611916755d9`.
- Exact private rebuild was byte-for-byte identical; all synthetic audit tests, source/worldgen validators, package and manifest checks passed. The outer GitHub artifact ZIP contains both imports and the preflight tools. Never import the wrapper ZIP directly.
- The complete modded Minecraft runtime, dedicated-server joins and in-game GUI/Questlog interactions remain untested.
