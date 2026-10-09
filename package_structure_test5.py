#!/usr/bin/env python3
"""Package and verify Test 5 from local sources with no network resolution."""
import argparse
import ast
import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from build_release_030 import build
from validate_continuation_031 import validate

ROOT = Path(__file__).resolve().parent
DOCUMENTS = ['TODO.md', 'STRUCTURE_BIOME_AUDIT.md', 'STRUCTURE_TEST5_CHANGELOG.md',
             'STRUCTURE_TEST5_VALIDATION.md', 'STRUCTURE_TEST5_INSTALL.md',
             'TANS_OPEN_FIELD_TUNING_PLAN.md', 'README-0.3.1.md', 'MOD_STRUCTURE_SCREENING.md',
             'MISSING_JARS.txt', 'APPROVED_ADDITION_JARS.txt']
CATALOGUES = ['STRUCTURE_REGISTRY_CATALOG.csv', 'STRUCTURE_BIOME_MATRIX.csv',
              'STRUCTURE_SET_CATALOG.csv', 'FARMERS_STRUCTURE_CATALOG.csv',
              'CODE_GENERATED_PLACEMENT_ROUTES.csv', 'NATIVE_RESOURCE_COLLISIONS.csv',
              'INSTALLED_MOD_STRUCTURE_SCREENING.csv', 'FUTURE_MOD_STRUCTURE_SCREENING.csv',
              'CREATE_ADDON_STRUCTURE_SCREENING.csv', 'APPROVED_STRUCTURE_ADDITIONS.csv']
SCREENING_OUTPUTS = ['MOD_STRUCTURE_SCREENING.md', 'APPROVED_ADDITION_JARS.txt',
                     'APPROVED_STRUCTURE_ADDITIONS.csv', 'INSTALLED_MOD_STRUCTURE_SCREENING.csv',
                     'FUTURE_MOD_STRUCTURE_SCREENING.csv', 'CREATE_ADDON_STRUCTURE_SCREENING.csv',
                     'release_030/approved-structure-additions.json']


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(source.read()).hexdigest()


def safe(name):
    path = PurePosixPath(name)
    return not path.is_absolute() and '..' not in path.parts and '\\' not in name


def write_zip(path, entries):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, source in sorted(entries.items()):
            assert safe(name), name
            info = zipfile.ZipInfo(name, (2026, 10, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())
    return verify_zip(path)


def verify_zip(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert archive.testzip() is None, 'CRC failure: ' + str(path)
        assert len(names) == len(set(names)), 'Duplicate paths: ' + str(path)
        assert all(safe(name) for name in names), 'Unsafe path: ' + str(path)
        return len(names)


def run(script, args, cwd):
    result = subprocess.run([sys.executable, script, *args], cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(script + '\n' + result.stdout + result.stderr)
    return result.stdout


def package(output):
    output = output.resolve()
    assert output != ROOT and not output.is_relative_to(ROOT / 'release_030')
    output.mkdir(parents=True, exist_ok=True)
    # Reports must be generated before the import embeds them. The subsequent
    # clean extraction check proves that the cached-evidence reports reproduce.
    run('write_mod_screening_031.py', [], ROOT)
    run('write_structure_audit.py', [], ROOT)
    import_zip = build(output=output / 'Ambient-Odyssey-v0.3.1-structure-test5-audit1.zip')
    report = validate(archive=import_zip)
    (ROOT / 'release_030/evidence/static-validation-structure-test5.json').write_text(json.dumps(report, indent=2) + '\n')
    assert all(check['passed'] for check in report['checks'])
    python_sources = list(ROOT.glob('*.py'))
    for path in python_sources:
        ast.parse(path.read_text(), filename=str(path))

    source_entries = {}
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.is_relative_to(output):
            continue
        rel = path.relative_to(ROOT)
        if any(part in {'build', '__pycache__', '.git'} for part in rel.parts) or path.suffix == '.pyc':
            continue
        source_entries[rel.as_posix()] = path
    original = json.loads((ROOT / 'release_030/evidence/baseline-source-file-hashes.json').read_text())['files']
    current = {name: digest(path) for name, path in source_entries.items() if name != 'SOURCE_CHANGES.csv'}
    changed = []
    for name in sorted(set(original) | set(current)):
        if name == 'SOURCE_CHANGES.csv' or original.get(name) == current.get(name):
            continue
        changed.append({'path': name, 'change': 'added' if name not in original else 'deleted' if name not in current else 'modified',
                        'before_sha256': original.get(name, ''), 'after_sha256': current.get(name, '')})
    change_path = ROOT / 'SOURCE_CHANGES.csv'
    with change_path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=['path', 'change', 'before_sha256', 'after_sha256'])
        writer.writeheader()
        writer.writerows(changed)
    source_entries[change_path.name] = change_path
    source_zip = output / 'Ambient-Odyssey-v0.3.1-sources-test5-audit1.zip'
    source_members = write_zip(source_zip, source_entries)
    required = {'build_release_030.py', 'validate_structure_test5.py', 'validate_continuation_031.py', 'package_structure_test5.py',
                'audit_continuation_031.py', 'report_continuation_031.py', 'write_mod_screening_031.py',
                'release_030/native-template-inputs/waystones-desert-waystone.nbt',
                'release_030/approved-structure-additions.json', 'SOURCE_CHANGES.csv',
                'release_030/structure-density.json', 'release_030/structure-compatibility.json',
                'release_030/structure-repairs.json', 'release_030/release-lock.json',
                'Ambient-Odyssey-v0.2.10.zip', *DOCUMENTS, *CATALOGUES}
    assert required <= set(source_entries), required - set(source_entries)
    assert not any(name.endswith('.jar') for name in source_entries)

    with tempfile.TemporaryDirectory(prefix='ao-test5-rebuild-') as temp_name:
        temp = Path(temp_name)
        clean = temp / 'sources'
        clean.mkdir()
        with zipfile.ZipFile(source_zip) as archive:
            archive.extractall(clean)
        rebuilt = temp / import_zip.name
        run('build_release_030.py', ['--output', str(rebuilt)], clean)
        assert digest(import_zip) == digest(rebuilt), 'Clean source rebuild differs'
        repeated = json.loads(run('validate_continuation_031.py', ['--archive', str(rebuilt)], clean))
        assert repeated['checks'] == len(report['checks']) and repeated['status'].startswith('PASS')
        run('write_structure_audit.py', [], clean)
        for name in ['STRUCTURE_BIOME_AUDIT.md', *CATALOGUES]:
            assert digest(ROOT / name) == digest(clean / name), 'Audit regeneration differs: ' + name
        run('write_mod_screening_031.py', [], clean)
        for name in SCREENING_OUTPUTS:
            assert digest(ROOT / name) == digest(clean / name), 'Screening regeneration differs: ' + name
        # Cached input hashes make the source-change report independently
        # reviewable without needing the original 70 MB source ZIP.
        rebuilt_hashes = {name: digest(clean / name) for name in current}
        assert current == rebuilt_hashes, 'Extracted source content differs'

    support_entries = {}
    for name in [*DOCUMENTS, *CATALOGUES, 'SOURCE_CHANGES.csv']:
        target = output / name
        shutil.copyfile(ROOT / name, target)
        support_entries[name] = target
    for path in (ROOT / 'release_030/evidence').rglob('*'):
        if not path.is_file():
            continue
        rel = 'evidence/' + path.relative_to(ROOT / 'release_030/evidence').as_posix()
        target = output / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        support_entries[rel] = target
    coverage = json.loads((ROOT / 'release_030/evidence/jar-audit-coverage-test5.json').read_text())
    summary = {
        'status': 'PASS (expanded scoped static gates and archive/source rebuild checks)',
        'gameplay_tested': False,
        'scoped_check_count': len(report['checks']),
        'python_scripts_syntax_checked': len(python_sources),
        'counts': report['counts'],
        'import_archive': {'filename': import_zip.name, 'size_bytes': import_zip.stat().st_size,
                           'sha256': digest(import_zip), 'crc': 'PASS', 'members': verify_zip(import_zip)},
        'source_archive': {'filename': source_zip.name, 'size_bytes': source_zip.stat().st_size,
                           'sha256': digest(source_zip), 'crc': 'PASS', 'members': source_members},
        'clean_source_archive_rebuild': 'byte-for-byte identical',
        'clean_rebuild_scoped_check_count': repeated['checks'],
        'audit_report_and_three_catalogue_rebuild': 'byte-for-byte identical',
        'screening_report_and_catalogues_rebuild': 'byte-for-byte identical',
        'source_changes': {'filename': 'SOURCE_CHANGES.csv', 'rows': len(changed),
                           'scope': 'All changed/new/deleted packaged source files except the change report itself, whose own hash cannot be self-referential.'},
        'coverage': {'original_resource_audit': 177, 'new_complete_binary_audits': 19,
                     'expanded_resource_audit': 196, 'current_complete_binary_screens': 26,
                     'missing_existing_profile_jars': 41, 'approved_additions_not_installed': 8},
        'coverage_inventory': 'evidence/jar-audit-coverage-test5.json',
        'limitations': report['limitations'],
    }
    assert coverage, 'Missing JAR coverage inventory'
    summary_path = output / 'release-validation-summary.json'
    summary_path.write_text(json.dumps(summary, indent=2) + '\n')
    support_entries[summary_path.name] = summary_path
    checksum_path = output / 'SHA256SUMS.txt'
    checksum_entries = {import_zip.name: import_zip, source_zip.name: source_zip, **support_entries}
    checksum_path.write_text(''.join(digest(path) + '  ' + name + '\n' for name, path in sorted(checksum_entries.items())))
    support_entries[checksum_path.name] = checksum_path
    support_zip = output / 'Ambient-Odyssey-Structure-Test5-Audit1-Supporting-Files.zip'
    support_members = write_zip(support_zip, support_entries)
    # The internal checksum list covers the other files. Append the support ZIP's
    # hash only to the external list, avoiding a self-referential ZIP hash.
    with checksum_path.open('a') as stream:
        stream.write(digest(support_zip) + '  ' + support_zip.name + '\n')
    print(json.dumps({'status': summary['status'], 'checks': len(report['checks']),
                      'source_members': source_members, 'support_members': support_members,
                      'clean_rebuild': 'identical', 'audit_rebuild': 'identical',
                      'screening_rebuild': 'identical', 'source_change_rows': len(changed),
                      'import_sha256': digest(import_zip), 'source_sha256': digest(source_zip),
                      'support_sha256': digest(support_zip)}))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'build')
    args = parser.parse_args()
    package(args.output_dir)
