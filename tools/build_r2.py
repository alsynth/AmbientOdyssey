"""R2 one-shot build on a machine WITH Java 21, Gradle 9.2.1, network to NeoForge/Shadowsoffire Maven and the exact PR50 ZIP.
Usage: python tools/build_r2.py --base Ambient-Odyssey-v0491-Structure-Celestisynth-FULL-IMPORT.zip --out build/Ambient-Odyssey-MASTER-INTEGRATION-R2-ALL-DECIDED-PRIVATE-20261015.zip
Steps: regenerate policy/campaign -> clean-build 3 addons -> unit tests -> package (hash-gated) -> validate."""
import argparse,hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PR50='dd72daac0fef6c42f758728abc9b003d680b791ccfe174975ec4424cf1ad3d9f'
def run(*c,cwd=ROOT):print('+',*c);subprocess.run(c,cwd=cwd,check=True)
ap=argparse.ArgumentParser();ap.add_argument('--base',required=True);ap.add_argument('--out',required=True);ap.add_argument('--gradle',default='gradle')
a=ap.parse_args()
if hashlib.sha256(Path(a.base).read_bytes()).hexdigest()!=PR50:sys.exit('Base ZIP is not the exact PR50 import; refusing.')
run(sys.executable,'tools/compile_additive_loot_policy.py');run(sys.executable,'tools/compile_ao_v050_campaign.py')
for addon in ('ao-starter-chest','ao-augmenting-sigils','ao-campaign'):
    d=ROOT/'addons'/addon
    for old in (d/'build/libs').glob('*.jar'):old.unlink()   # never let a stale JAR satisfy a filename check
    run(a.gradle,'clean','build','--no-daemon',cwd=d)
run(sys.executable,'-m','unittest','discover','tests')
sys.path.insert(0,str(ROOT/'tools'))
import package_master_integration as pm
pm.build(a.base,a.out)
run(sys.executable,'tools/validate_master_integration.py',a.out,'--report',a.out+'.static.json')
