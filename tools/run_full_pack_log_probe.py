"""Launch a disposable full-roster log probe with production NeoForge libraries.

Uses an offline identity and never reads accounts/tokens. Runtime must be under
this repository's build directory. The caller supplies a copied mod/config
snapshot and the test-only tools/log-probe JAR. Neither the probe nor this runtime
belongs in a released pack. Stop/terminate only the spawned test process.
"""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import zipfile


def allowed(rules):
    if not rules:
        return True
    result = False
    for rule in rules:
        os_rule = rule.get('os', {})
        if os_rule.get('name', 'windows') != 'windows':
            continue
        if os_rule.get('arch') and not re.fullmatch(os_rule['arch'], 'amd64'):
            continue
        if os_rule.get('version') and not re.search(os_rule['version'], '10.0'):
            continue
        if any(rule.get('features', {}).values()):
            continue
        result = rule['action'] == 'allow'
    return result


def launch(install, runtime, jar, java, heap, timeout, width=960, height=540):
    project = Path(__file__).resolve().parents[1]
    runtime = runtime.resolve()
    runtime.relative_to((project / 'build').resolve())
    assert not (runtime / 'minecraftinstance.json').exists(), 'Live CurseForge profiles are not test targets'
    assert (runtime / 'mods').is_dir(), 'Prepare a disposable mod snapshot first'
    version = 'neoforge-21.1.252'
    base = json.loads((install / 'versions/1.21.1/1.21.1.json').read_text())
    neo = json.loads((install / f'versions/{version}/{version}.json').read_text())
    assert neo['id'] == version and neo['inheritsFrom'] == '1.21.1', 'Wrong production loader metadata'
    libraries = {}
    for lib in base['libraries'] + neo['libraries']:
        if not allowed(lib.get('rules')):
            continue
        key = lib['name'].split(':')
        identity = ':'.join(key[:2] + key[3:])
        artifact = lib.get('downloads', {}).get('artifact')
        if artifact:
            libraries[identity] = install / 'libraries' / artifact['path']
    paths = list(libraries.values()) + [install / f'versions/{version}/{version}.jar']
    missing = [str(p) for p in paths if not p.is_file()]
    assert not missing, f'Production launcher library files missing: {missing}'
    natives = runtime / 'production-natives'
    natives.mkdir(exist_ok=True)
    for path in paths:
        if 'natives-windows' in path.name:
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    if name.endswith('.dll'):
                        (natives / PurePosixPath(name).name).write_bytes(archive.read(name))
    values = {'version_name': version, 'library_directory': (install / 'libraries').as_posix(),
              'classpath_separator': ';', 'natives_directory': natives.as_posix(),
              'launcher_name': 'AO-Isolated-Test', 'launcher_version': '1',
              'classpath': ';'.join(p.as_posix() for p in paths), 'auth_player_name': 'AO-Test',
              'auth_uuid': '00000000000000000000000000000001', 'auth_access_token': '0',
              'clientid': '0', 'auth_xuid': '0', 'user_type': 'legacy', 'version_type': 'release',
              'game_directory': runtime.as_posix(), 'assets_root': (install / 'assets').as_posix(),
              'assets_index_name': '17'}
    def arguments(rows):
        result = []
        for row in rows:
            if isinstance(row, dict):
                if not allowed(row.get('rules')):
                    continue
                row = row['value']
            for item in row if isinstance(row, list) else [row]:
                for key, value in values.items():
                    item = item.replace('${' + key + '}', value)
                assert '${' not in item, f'Unresolved launcher placeholder: {item}'
                result.append(item)
        return result
    args = [f'-Xmx{heap}', '-Dao.fullpack.logProbe=true', f'-Dao.fullpack.logProbeTimeoutSeconds={timeout}']
    args += arguments(base['arguments']['jvm'] + neo['arguments']['jvm'])
    args += [neo['mainClass']] + arguments(base['arguments']['game'] + neo['arguments']['game'])
    args += ['--width', str(width), '--height', str(height)]
    argfile = runtime / 'production-launch.args'
    argfile.write_text('\n'.join(json.dumps(s, ensure_ascii=False) for s in args), encoding='utf-8')
    shutil.copy2(jar, runtime / 'mods' / jar.name)
    with (runtime / 'production-launch.log').open('w', encoding='utf-8') as log:
        process = subprocess.Popen([java, '@' + str(argfile)], cwd=runtime, stdout=log, stderr=subprocess.STDOUT)
        (runtime / 'production-client.pid').write_text(str(process.pid))
        try:
            code = process.wait(timeout=timeout + 60)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=15)
            raise RuntimeError('Production client timed out; only the spawned test process was terminated')
    output = (runtime / 'production-launch.log').read_text(encoding='utf-8', errors='replace')
    passed = code == 0 and 'AO_FULL_PACK_WORLD_JOIN_PASS' in output and 'AO_FULL_PACK_PROBE_FAIL' not in output
    return {'launcher': 'production', 'library_files': len(paths), 'exit_code': code,
            'startup_and_world_join': 'PASS' if passed else 'FAIL', 'in_world_gameplay_verified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', type=Path, required=True)
    parser.add_argument('--game-dir', type=Path, required=True)
    parser.add_argument('--mod-jar', type=Path, required=True)
    parser.add_argument('--java', default=shutil.which('java'))
    parser.add_argument('--heap', default='6G')
    parser.add_argument('--timeout', type=int, default=240)
    parser.add_argument('--width', type=int, default=960)
    parser.add_argument('--height', type=int, default=540)
    options = parser.parse_args()
    result = launch(options.install.resolve(), options.game_dir, options.mod_jar.resolve(), options.java, options.heap, options.timeout, options.width, options.height)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['startup_and_world_join'] == 'PASS' else 1)
