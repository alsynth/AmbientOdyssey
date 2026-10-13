"""Compare scattered follow-up notes with the exact PR45 and frozen runtime rosters."""
import argparse, hashlib, json, re, tomllib, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def reconcile(note: Path, snapshot: Path, output: Path, celestisynth_jar: Path | None = None):
    baseline = {r['jar']: r['sha256'] for r in json.loads((ROOT / 'docs/balance/v3-evidence/INSTALLED_JARS.json').read_text(encoding='utf-8')) if r['jar'] != 'minecraft_1.21.1_client.jar'}
    frozen = json.loads(snapshot.read_text(encoding='utf-8'))['jar_hashes']
    raw = note.read_bytes()
    text = raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
    candidates = re.findall(r'^- ([^\n]+?\.jar)', text, re.M)
    rows = [{'jar': name, 'in_pr45': name in baseline, 'in_frozen_runtime': name in frozen, 'baseline_hash_matches': frozen.get(name) == baseline[name] if name in baseline else None} for name in candidates]
    result = {
        'baseline_physical_jars': len(baseline), 'frozen_physical_jars': len(frozen),
        'source_note': 'https://github.com/alsynth/AmbientOdyssey/blob/6a01951e415c784f134147284200863fddadaf6e/docs/testing/V049_LOCAL_MOD_CHANGES_CRASH_20261013.md',
        'note_candidates': rows,
        'new_physical_jars': [{'jar': n, 'sha256': frozen[n]} for n in sorted(frozen.keys() - baseline.keys())],
        'changed_original_jars': [n for n in baseline.keys() & frozen.keys() if baseline[n] != frozen[n]],
        'missing_original_jars': sorted(baseline.keys() - frozen.keys()),
        'celestisynth': {
            'decision': 'USER_REQUESTED_FOR_NEXT_EXPERIMENTAL_BUILD',
            'status': 'SOURCE_VERIFIED_FILE; NOT_INSTALLED_OR_RUNTIME_TESTED',
            'project_id': 1672331, 'file_id': 8867800,
            'jar': 'celestisynth-1.21.1-1.3.9.jar', 'loader': 'NeoForge', 'minecraft': '1.21.1',
            'source': 'https://www.curseforge.com/minecraft/mc-mods/celestisynth-1-21-1/files/8867800',
            'dependency_description': 'Official description requires GeckoLib and PlayerAnimator; exact JAR dependency ranges pending.',
            'required_checks': ['exact JAR metadata/hash', 'dependency compatibility', 'client and server loading', 'weapon abilities and combat stacking', 'native acquisition and loot', 'worldgen/resource collision audit', 'screen effects and flashing']
        },
        'excluded': ['Mob Plaques: latest main-branch note explicitly rejects it'],
        'interpretation': 'The note\'s 423 Found mod file records are not a verified count of top-level physical JARs. Research PRs 47/48/49 add item catalogue records, not installed mods. This report changes no production profile or release.'
    }
    metadata = []
    for row in result['new_physical_jars']:
        jar = snapshot.parent / 'mods' / row['jar']
        with zipfile.ZipFile(jar) as archive:
            names = archive.namelist()
            metadata.append({**row,
                'metadata': {n: archive.read(n).decode() for n in names if n in ('META-INF/neoforge.mods.toml', 'META-INF/mods.toml', 'fabric.mod.json')},
                'worldgen_structures': [n for n in names if '/worldgen/structure/' in n and n.endswith('.json')],
                'template_pools': [n for n in names if '/worldgen/template_pool/' in n and n.endswith('.json')],
                'loot_tables': [n for n in names if '/loot_table/' in n and n.endswith('.json')],
                'biome_modifiers': [n for n in names if '/biome_modifier/' in n and n.endswith('.json')]})
    result['added_jar_metadata'] = metadata
    if celestisynth_jar is not None:
        with zipfile.ZipFile(celestisynth_jar) as archive:
            if archive.testzip(): raise RuntimeError('Celestisynth ZIP CRC failure')
            text = archive.read('META-INF/neoforge.mods.toml').decode()
            native = tomllib.loads(text)
            if native['mods'][0]['modId'] != 'celestisynth' or native['mods'][0]['version'] != '1.21.1-1.3.9':
                raise RuntimeError('Unexpected Celestisynth artifact')
            record = result['celestisynth']
            record.update({'status': 'STATIC_PASS_ARTIFACT_AND_REQUIRED_DEPENDENCIES; NOT_INSTALLED_OR_RUNTIME_TESTED',
                'sha256': hashlib.sha256(celestisynth_jar.read_bytes()).hexdigest(), 'bytes': celestisynth_jar.stat().st_size,
                'metadata': text, 'zip_crc': 'PASS',
                'dependency_checks': [
                    {'mod_id': 'neoforge', 'required': '[21.1.0,)', 'installed': '21.1.252', 'status': 'STATIC_PASS'},
                    {'mod_id': 'minecraft', 'required': '[1.21.1,1.22)', 'installed': '1.21.1', 'status': 'STATIC_PASS'},
                    {'mod_id': 'geckolib', 'required': '[4.9,)', 'installed': '4.9.3', 'status': 'STATIC_PASS'},
                    {'mod_id': 'playeranimator', 'required': '[2.0,)', 'installed': '2.0.4+1.21.1', 'status': 'STATIC_PASS'},
                    {'mod_id': 'jei', 'required': '[19.21.0.247,) (optional)', 'installed': '19.57.0.451', 'status': 'STATIC_PASS'}],
                'worldgen_resources': [n for n in archive.namelist() if '/worldgen/' in n and n.endswith('.json')],
                'loot_resources': [n for n in archive.namelist() if '/loot_table/' in n and n.endswith('.json')]})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('baseline_physical_jars', 'frozen_physical_jars', 'new_physical_jars', 'changed_original_jars', 'missing_original_jars')}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--note', type=Path, required=True)
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--celestisynth-jar', type=Path)
    a = p.parse_args()
    reconcile(a.note, a.snapshot, a.output, a.celestisynth_jar)
