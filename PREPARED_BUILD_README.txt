Ambient Odyssey v0.4h Launch Readiness — EXPERIMENTAL ONLY
Minecraft 1.21.1 / NeoForge 21.1.252 / 331 pinned CurseForge project references.

Import the actual PRIVATE or CF-References ZIP from this workflow artifact into a NEW disposable CurseForge profile.
Do NOT import the GitHub artifact wrapper as a modpack.
Do NOT unzip a CurseForge pack directly into an existing profile.
The PRIVATE ZIP includes the audited NeoReefRedux test JAR, is for personal testing and is not a public CurseForge release.

After installation, run RUN_PREFLIGHT_WINDOWS.cmd on Windows, or use:
  python tools/diagnose_v04_instance.py --profile "/path/to/instance"
  python tools/audit_installed_jars_v04.py --profile "/path/to/instance"

For a separate dedicated server, also use:
  python tools/audit_installed_jars_v04.py --profile "/path/to/client" --server "/path/to/server"

These scripts are READ ONLY. They do not remove mods, fix broken dependencies or execute Minecraft.
Review the 23 historical unavailable/parse-failed JAR metadata records.
Questlog journal button position is provisional: GUI X=38/Y=38 screen-anchored, no quests authored yet.
Full AO client and multiplayer runtimes are NOT VERIFIED.
Existing 330-ref and previous 331-ref builds and all rollback branches are preserved.

See docs/testing/V04H_INSTALLED_JAR_AND_SERVER_PREFLIGHT.md and V04_TESTING_CHECKLIST.md.
