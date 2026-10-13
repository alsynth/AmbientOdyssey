"""Summarize observed native exports without promoting limited rehearsals to full acceptance."""
import argparse, hashlib, json, math, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/balance/pr45-acceptance-evidence'

def read(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def equivalent(expected, actual):
    if isinstance(expected, dict):
        if not isinstance(actual, dict): return False
        # The installed Gson omits null-valued object fields when exporting/saving.
        expected = {k: v for k, v in expected.items() if v is not None}
        actual = {k: v for k, v in actual.items() if v is not None}
        return expected.keys() == actual.keys() and all(equivalent(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list): return isinstance(actual, list) and len(expected) == len(actual) and all(equivalent(a, b) for a, b in zip(expected, actual))
    if type(expected) in (int, float) and type(actual) in (int, float): return math.isclose(expected, actual, abs_tol=1e-6, rel_tol=1e-6)
    return expected == actual

def summarize(candidate: Path, rollback: Path, candidate_exit: int, rollback_exit: int):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    results = {'acceptance_complete': False, 'elite_stacking_tested': False, 'natural_encounters_tested': False,
               'dedicated_server_tested': False, 'multiplayer_tested': False, 'loot_overrides_installed': False,
               'quest_prototypes_installed': False, 'celestisynth_runtime_tested': False,
               'gate': 'HOLD: elite cap/exclusion, natural encounter, dedicated-server and multiplayer acceptance remain pending',
               'original_332_runtime': {'status': 'CLIENT_RUNTIME_PASS_FRESH_FLAT_WORLD', 'exit_code_observed': 0, 'structures_queried': 379, 'resource_checks': 153},
               'runs': {}}
    for label, directory, exit_code in [('337_candidate', candidate, candidate_exit), ('337_rollback', rollback, rollback_exit)]:
        native = read(directory / 'PR45_RUNTIME_REGISTRIES.json')
        original = ROOT / 'experiments/structure-difficulty-v3' / ('candidate' if label.endswith('candidate') else 'rollback') / 'config/dungeon_difficulty/difficulty_v2.json'
        log = (directory / 'production-launch.log').read_text(encoding='utf-8', errors='replace')
        markers = [line for line in log.splitlines() if any(k in line for k in ('AO_FULL_PACK_TITLE_PASS', 'AO_FULL_PACK_WORLD_JOIN_PASS', 'AO_PR45_RUNTIME_REGISTRY_EXPORT_PASS', 'AO_FULL_PACK_PROBE_FAIL'))]
        config_matches = equivalent(read(original), native['loaded_dd_config'])
        launch_pass = exit_code == 0 and 'AO_FULL_PACK_WORLD_JOIN_PASS' in log and 'AO_FULL_PACK_PROBE_FAIL' not in log
        row = {'status': 'CLIENT_RUNTIME_PASS_LIMITED_REHEARSAL' if launch_pass and config_matches else 'CLIENT_RUNTIME_FAIL',
               'exit_code_observed': exit_code, 'config_matches_original_json_with_float_tolerance_and_gson_null_elision': config_matches,
               'prepared_overlay_sha256': digest(original),
               'post_runtime_overlay_sha256': digest(directory / 'config/dungeon_difficulty/difficulty_v2.json'),
               'probe_sha256': digest(directory / 'mods/ao-fullpack-log-probe-1.0-test-only.jar'),
               'production_physical_jars': len(read(directory / 'PR45_SNAPSHOT.json')['jar_hashes']),
               'instrumentation_jars': 1, 'structure_ids_queried': len(native['structure_registry_membership']),
               'structure_ids_missing': [k for k, v in native['structure_registry_membership'].items() if not v],
               'effective_resource_checks': len(native['effective_resource_winners']),
               'resource_checks_missing': [r for r in native['effective_resource_winners'] if not r['present']]}
        if label.endswith('candidate'):
            rule = read(directory / 'PR45_ORDINARY_RULE_TESTS.json')
            row['synthetic_rules_all_pass'] = rule['all_pass']; row['synthetic_case_count'] = len(rule['cases'])
            if not rule['all_pass']: row['status'] = 'CLIENT_RUNTIME_FAIL_SYNTHETIC_RULE'
            shutil.copy2(directory / 'PR45_ORDINARY_RULE_TESTS.json', EVIDENCE / '337_ORDINARY_RULE_TESTS.json')
        for source, target in [('PR45_RUNTIME_REGISTRIES.json', label + '_RUNTIME_REGISTRIES.json'), ('PR45_SNAPSHOT.json', label + '_SNAPSHOT.json')]: shutil.copy2(directory / source, EVIDENCE / target)
        (EVIDENCE / (label + '_RUNTIME_MARKERS.txt')).write_text('\n'.join(markers) + '\n', encoding='utf-8')
        results['runs'][label] = row
    for name in ('PR45_CHECK_INPUT.json', 'NEW_STRUCTURE_HOLDS.json'):
        if (candidate / name).exists(): shutil.copy2(candidate / name, EVIDENCE / ('RUNTIME_CHECK_INPUT.json' if name == 'PR45_CHECK_INPUT.json' else name))
    (EVIDENCE / 'ACCEPTANCE_RESULTS.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate', type=Path, required=True); p.add_argument('--rollback', type=Path, required=True)
    p.add_argument('--candidate-exit-code', type=int, required=True); p.add_argument('--rollback-exit-code', type=int, required=True)
    a = p.parse_args(); summarize(a.candidate, a.rollback, a.candidate_exit_code, a.rollback_exit_code)
