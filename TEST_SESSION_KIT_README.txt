Ambient Odyssey v0.4h — standalone TEST SESSION KIT

This kit DOES NOT contain Minecraft or mod JAR files. Get the preserved tested ZIPs
from GitHub Actions 38077302870, artifact 11679672185:
https://github.com/alsynth/AmbientOdyssey/actions/runs/38077302870/artifacts/11679672185

Use Python 3.11+ on Windows:
  py -3 tools/collect_v04_session.py --profile "C:\CurseForge\Instances\Ambient Odyssey" --output "AO-session-1.zip"
Optional: --server "C:\path\to\separate server"

The generated ZIP includes report.json, summary.md and field-sheet.md only.
It NEVER copies raw logs, screenshots, player names or server addresses; some JAR
filenames appear in its metadata summary, so review before sharing. To diagnose a
crash, provide original log/crash report separately after reviewing private contents.
All actual client, GUI, Mine Cells, worldgen and server tests start NOT TESTED.
The script never changes Minecraft files or makes network requests.
