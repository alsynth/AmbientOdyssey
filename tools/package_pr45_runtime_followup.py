"""Package limited runtime evidence and test sources; never includes production mods or saves."""
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def package(output: Path):
    evidence = ROOT / 'docs/balance/pr45-acceptance-evidence'
    status = json.loads((evidence / 'ACCEPTANCE_RESULTS.json').read_text(encoding='utf-8'))
    if status['acceptance_complete']: raise RuntimeError('This package does not certify full acceptance')
    paths = list(evidence.glob('*')) + [ROOT / 'docs/balance/PR45_RUNTIME_ACCEPTANCE_FOLLOWUP_20261013.md']
    paths += [ROOT / 'tools' / n for n in ('prepare_pr45_runtime_snapshot.py', 'prepare_pr45_frozen_rehearsal.py', 'reconcile_pr45_followup_mods.py', 'summarize_pr45_acceptance.py', 'package_pr45_runtime_followup.py', 'run_full_pack_log_probe.py')]
    probe = ROOT / 'tools/pr45-runtime-probe'
    paths += [probe / 'build.gradle', probe / 'settings.gradle'] + [p for p in (probe / 'src').rglob('*') if p.is_file()]
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths):
            if not path.is_file(): continue
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip(): raise RuntimeError('ZIP CRC failure')
        if any(n.endswith('.jar') or '/saves/' in n or 'manifest.json' in n for n in archive.namelist()): raise RuntimeError('Deployment files found in evidence-only kit')
    for source, name in [(ROOT / 'docs/balance/PR45_RUNTIME_ACCEPTANCE_FOLLOWUP_20261013.md', 'PR45-Runtime-Acceptance-Report.md'), (evidence / 'ACCEPTANCE_RESULTS.json', 'PR45-Runtime-Acceptance-Results.json'), (evidence / 'FOLLOWUP_MOD_RECONCILIATION.json', 'Followup-Mod-Reconciliation.json')]: shutil.copy2(source, output.parent / name)
    result = {'sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'crc': 'PASS', 'production_mods_included': False, 'saves_included': False, 'acceptance_complete': False}
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--output', type=Path, required=True)
    package(p.parse_args().output)
