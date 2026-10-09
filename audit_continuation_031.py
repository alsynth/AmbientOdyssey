#!/usr/bin/env python3
"""Extend the Test 5 audit from complete JARs, retaining original provenance."""
import argparse
import collections
import gzip
import hashlib
import json
import re
import zipfile
from pathlib import Path
from audit_jars_031 import CATEGORIES, inventory, load_json, resource_id
from inspect_class_031 import inspect

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'release_030/evidence'
EXTRA = ['tags/entity_type', 'loot_table', 'loot_modifiers',
         'worldgen/processor_list', 'worldgen/configured_feature',
         'worldgen/placed_feature', 'neoforge/biome_modifier',
         'lithostitched/worldgen_modifier', 'dimension', 'dimension_type']


def dump(path, value, compressed=False):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)


def audit(jars):
    baseline_path = EVIDENCE / 'baseline-test5/jar-resource-index-test5.json.gz'
    baseline = json.loads(gzip.decompress(baseline_path.read_bytes()))
    local = inventory(jars)
    resources = {category: dict(rows) for category, rows in baseline['resources'].items()}
    known = {row['sha256'] for row in baseline['jars']}
    fresh = [row for row in local['jars'] if row['sha256'] not in known]
    fresh_names = {row['file'] for row in fresh}
    for category, table in local['resources'].items():
        for identifier, rows in table.items():
            selected = [row for row in rows if row['jar'] in fresh_names]
            if selected:
                resources.setdefault(category, {}).setdefault(identifier, []).extend(selected)
    screens = []
    details = {}
    for jar in local['jars']:
        path = Path(jars) / jar['file']
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            extra_counts = collections.Counter()
            errors = []
            class_hits = []
            metadata = {}
            for name in names:
                if name in {'META-INF/neoforge.mods.toml', 'META-INF/mods.toml', 'fabric.mod.json'}:
                    metadata[name] = archive.read(name).decode('utf-8-sig')
                if name.endswith('.json'):
                    for category in EXTRA:
                        identifier = resource_id(name, category)
                        if not identifier:
                            continue
                        try:
                            obj = load_json(archive.read(name))
                        except (ValueError, UnicodeError) as exc:
                            errors.append({'jar': jar['file'], 'path': name, 'error': str(exc)})
                            break
                        extra_counts[category] += 1
                        if jar['file'] in fresh_names:
                            resources.setdefault(category, {}).setdefault(identifier, []).append(
                                {'jar': jar['file'], 'path': name, 'data': obj})
                        break
                if name.endswith('.class') and not name.startswith(('org/', 'com/google/', 'com/llamalad7/')):
                    obj = inspect(archive.read(name))
                    terms = sorted({term for term in obj['constants']
                                    if any(key in term for key in ['StructureSet', 'STRUCTURE_SET',
                                           'registerStructure', 'ConfiguredFeature', 'PlacedFeature',
                                           'TemplatePool', 'WorldgenModifier', 'BiomeModifier',
                                           'StructureTemplate', 'EndDragonFight', 'SpikeFeature'])})
                    if terms:
                        class_hits.append({'class': name, 'references': terms})
            counts = {**jar['counts'], **dict(extra_counts)}
            templates = [n for n in names if re.fullmatch(r'data/[^/]+/structure/.+\.nbt', n)]
            structure_data = any(counts.get(c, 0) for c in ['worldgen/structure', 'worldgen/structure_set'])
            other_worldgen = any(counts.get(c, 0) for c in EXTRA[3:])
            classification = ('STRUCTURE_PROVIDER' if structure_data else
                              'WORLDGEN_DATA_OR_CODE_REVIEW' if other_worldgen or class_hits else
                              'NO_STRUCTURE_ROUTE_DETECTED')
            screens.append({'jar': jar['file'], 'sha256': jar['sha256'], 'crc': 'PASS',
                            'new_to_audit': jar['file'] in fresh_names,
                            'classification': classification, 'counts': counts,
                            'default_structure_templates': len(templates),
                            'code_hits': len(class_hits), 'parse_errors': errors,
                            'negative_scope': 'Root resources and class constant-reference screen; not a formal proof of absence.'})
            details[jar['file']] = {'metadata': metadata, 'class_hits': class_hits,
                                    'default_structure_templates': templates, 'parse_errors': errors,
                                    'all_resource_paths': [n for n in names if n.startswith('data/') and n.endswith('.json')]}
    snapshot = {'jars': baseline['jars'] + fresh, 'resources': resources,
                'optional_resources': baseline['optional_resources'] +
                    [row for row in local['optional_resources'] if row['jar'] in fresh_names],
                'parse_errors': baseline['parse_errors'] +
                    [row for row in local['parse_errors'] if row['jar'] in fresh_names],
                'provenance': {'baseline': '177 complete CRC-verified JARs from original Test 5 audit',
                               'new_complete_jars': len(fresh),
                               'extended_categories_scope': 'New JARs only; original snapshot was limited to its recorded categories.',
                               'current_complete_local_jars': len(local['jars'])}}
    original = json.loads((EVIDENCE / 'baseline-test5/jar-audit-coverage-test5.json').read_text())
    recovered = sorted(set(original['unretrieved_logged_jars']) & fresh_names)
    coverage = {**original,
                'audited_jars': sorted(set(original['audited_jars']) | fresh_names),
                'unretrieved_logged_jars': sorted(set(original['unretrieved_logged_jars']) - fresh_names),
                'newly_recovered_logged_jars': recovered,
                'baseline_audited_count': len(baseline['jars']),
                'expanded_audited_count': len(snapshot['jars']),
                'current_session_complete_jars': len(local['jars']),
                'new_count_explanation': '17 handoff JARs plus previously supplied Curios and Traveloptics = 19 unique newly recovered JARs.',
                'continuation_transfer_note': 'Full mods2.zip transfer now returned HTTP 403. Prior CRC-checked snapshot remains preserved; no new audit of unavailable binary members is claimed.'}
    dump(EVIDENCE / 'jar-resource-index-test5.json.gz', snapshot, True)
    dump(EVIDENCE / 'jar-audit-coverage-test5.json', coverage)
    dump(EVIDENCE / 'new-jar-screen.json', screens)
    dump(EVIDENCE / 'new-jar-details.json.gz', details, True)
    dump(EVIDENCE / 'structure-provider-audit-summary.json', {
        'audited_jars': len(snapshot['jars']), 'new_jars': len(fresh),
        'missing_logged_jars': len(coverage['unretrieved_logged_jars']),
        'resource_counts': {key: len(rows) for key, rows in resources.items()},
        'new_parse_errors': [e for row in screens for e in row['parse_errors']],
        'scope': snapshot['provenance']})
    print(json.dumps({'audited_jars': len(snapshot['jars']), 'new_jars': len(fresh),
                      'remaining_missing': len(coverage['unretrieved_logged_jars']),
                      'resources': {key: len(rows) for key, rows in resources.items()
                                    if key in CATEGORIES[:5]}}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jars', type=Path, required=True)
    audit(parser.parse_args().jars)
