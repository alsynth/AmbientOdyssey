"""Package performance preparation only: no mod binaries, live configs or performance claims."""
import argparse,hashlib,json,tomllib
from pathlib import Path
from package_v048_ui_fix import archive
ROOT=Path(__file__).resolve().parents[1]
def package(output):
 prep=ROOT/'docs/performance/v049-prep'
 baseline=json.loads((prep/'BASELINE.json').read_bytes())
 assert baseline['cf_pin_count']==329 and baseline['performance_measured'] is False
 particles=tomllib.loads((prep/'STREAMS_BALANCED_CANDIDATE.toml').read_text(encoding='utf-8'))['particles']
 assert particles['streamBubbles']==1 and particles['maxStreamParticlesPerTick']==250 and particles['streamParticleScanRadius']==64
 members={'READ_FIRST.txt':b'Preparation kit, not a CurseForge import or auto-installer.\nRunbook: OVERHAUL_PLAN.md. Start with three baseline trials and the shader/Streams comparisons.\nCandidate configs are references; apply only to a disposable test profile.\nAll CSV measurements are blank. No performance gain is certified.\nClient 1440p/144Hz, 10GB heap initially; preserve the r19 rollback.\n'}
 members['OVERHAUL_PLAN.md']=(ROOT/'docs/performance/V049_OVERHAUL_PREP_20261012.md').read_bytes()
 for p in sorted(prep.iterdir()):
  if p.is_file():members['references/'+p.name]=p.read_bytes()
 for n in ['perf_v041_log_report.py','perf_v041_trials.py','perf_preflight_v04.py']:
  members['tools/'+n]=(ROOT/'tools'/n).read_bytes()
 members['TOOLS.txt']=b'Python 3 required.\npython tools/perf_v041_trials.py references/BENCHMARKS.csv --out measured-summary.json\npython tools/perf_v041_log_report.py PATH_TO_LATEST_LOG --out log-summary.json\nKeep exact hashes, shader options and matching cold/warm routes for comparisons.\n'
 assert not any(n.endswith(('.jar','.log','.sparkprofile')) for n in members)
 digest=archive(output,members)
 output.with_suffix('.inputs.json').write_text(json.dumps({'output_sha256':digest,'source_files':{n:hashlib.sha256(b).hexdigest() for n,b in members.items()},'preparation_only':True,'measured_gain':False},indent=2)+'\n',encoding='utf-8')
 print(digest)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);package(p.parse_args().output)
