#!/usr/bin/env python3
"""Inventory the uploaded Minecraft JAR resources; no network or game launch.

Only root data/ resources are treated as default-active. Built-in optional packs
are inventoried separately rather than silently merged into the registry.
"""
import argparse
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path


def load_json(data):
    """Mojang's lenient JSON accepts comments and trailing commas in mod data."""
    text = data.decode('utf-8-sig') if isinstance(data, bytes) else data
    text = re.sub(r'("(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\n]*)',
                  lambda m: m[0] if m[0].startswith('"') else '', text, flags=re.S)
    return json.loads(re.sub(r',\s*([}\]])', r'\1', text))


def resource_id(path, category):
    m = re.fullmatch(r'data/([^/]+)/' + re.escape(category) + r'/(.+)\.json', path)
    return f'{m[1]}:{m[2]}' if m else None


CATEGORIES = ['worldgen/structure', 'worldgen/structure_set', 'worldgen/template_pool',
              'worldgen/biome', 'tags/worldgen/biome', 'tags/worldgen/structure',
              'tags/worldgen/structure_set', 'tags/item', 'recipe']


def inventory(directory):
    resources = {k: defaultdict(list) for k in CATEGORIES}
    jars, optional, errors = [], [], []
    for path in sorted(Path(directory).glob('*.jar')):
        raw = path.read_bytes()
        jar = {'file': path.name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
               'counts': defaultdict(int)}
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None, path
            for name in sorted(archive.namelist()):
                if not name.endswith('.json'):
                    continue
                for category in CATEGORIES:
                    identifier = resource_id(name, category)
                    if identifier:
                        try:
                            obj = load_json(archive.read(name))
                        except (ValueError, UnicodeError) as exc:
                            errors.append({'jar': path.name, 'path': name, 'error': str(exc)})
                            break
                        resources[category][identifier].append({'jar': path.name, 'path': name, 'data': obj})
                        jar['counts'][category] += 1
                        break
                else:
                    if '/data/' in name and any('/' + c + '/' in name for c in CATEGORIES[:7]):
                        optional.append({'jar': path.name, 'path': name})
        jar['counts'] = dict(jar['counts'])
        jars.append(jar)
    return {'jars': jars, 'resources': {k: dict(v) for k, v in resources.items()},
            'optional_resources': optional, 'parse_errors': errors}


def merge_tags(entries):
    values = []
    for entry in entries:
        data = entry.get('data', entry)
        if data.get('replace', False):
            values = []
        values += data.get('values', [])
    return values


def resolve_tag(identifier, tags, stack=()):
    """Return leaves and unknown nested tags; invalidity is checked separately."""
    if identifier in stack:
        return set(), {'cycle:' + identifier}
    if identifier not in tags:
        return set(), {identifier}
    leaves, missing = set(), set()
    for entry in tags[identifier]:
        data = entry.get('data', entry)
        if data.get('replace', False):
            leaves, missing = set(), set()
        for field in ('values', 'remove'):
            selected = set()
            for value in data.get(field, []):
                identifier2 = value.get('id') if isinstance(value, dict) else value
                if identifier2.startswith('#') and ':' not in identifier2:
                    identifier2 = '#minecraft:' + identifier2[1:]
                elif not identifier2.startswith('#') and ':' not in identifier2:
                    identifier2 = 'minecraft:' + identifier2
                if identifier2.startswith('#'):
                    more, unknown = resolve_tag(identifier2[1:], tags, stack + (identifier,))
                    selected |= more
                    # Optional missing collections do not invalidate a tag;
                    # retain them as evidence of incomplete native coverage.
                    if field == 'values':
                        missing |= unknown
                else:
                    selected.add(identifier2)
            if field == 'values':
                leaves |= selected
            else:
                leaves -= selected
    return leaves, missing


def overlay_tags(native, overrides):
    tags = {k: list(v) for k, v in native.items()}
    for path in sorted(Path(overrides).glob('config/paxi/datapacks/*/data/*/tags/worldgen/biome/**/*.json')):
        rel = path.as_posix().split('/data/', 1)[1]
        ns, name = rel.split('/tags/worldgen/biome/', 1)
        tags.setdefault(ns + ':' + name[:-5], []).append({'data': load_json(path.read_bytes()), 'path': str(path)})
    return tags


def selector_tag_references(selector):
    if isinstance(selector, str):
        return {selector[1:]} if selector.startswith('#') else set()
    if isinstance(selector, list):
        return set().union(*(selector_tag_references(s) for s in selector))
    if isinstance(selector, dict):
        return selector_tag_references(selector.get('values', [])) | selector_tag_references(selector.get('value', []))
    return set()


def resolve_selector(selector, tags, universe):
    """Evaluate NeoForge and/or/not holder sets against an explicit biome universe."""
    if isinstance(selector, str):
        if ':' not in selector:
            selector = '#minecraft:' + selector[1:] if selector.startswith('#') else 'minecraft:' + selector
        return resolve_tag(selector[1:], tags) if selector.startswith('#') else ({selector}, set())
    if isinstance(selector, list):
        leaves, missing = set(), set()
        for child in selector:
            more, unknown = resolve_selector(child, tags, universe)
            leaves |= more
            missing |= unknown
        return leaves, missing
    if isinstance(selector, dict):
        kind = selector['type']
        if kind == 'neoforge:not':
            leaves, missing = resolve_selector(selector['value'], tags, universe)
            return set(universe) - leaves, missing
        if kind in {'neoforge:and', 'neoforge:or'}:
            leaves = set(universe) if kind.endswith(':and') else set()
            missing = set()
            for child in selector['values']:
                more, unknown = resolve_selector(child, tags, universe)
                leaves = leaves & more if kind.endswith(':and') else leaves | more
                missing |= unknown
            return leaves, missing
        return set(), {'unhandled_holder_set:' + kind}
    return set(), {'unhandled_holder_set'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jars', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = inventory(args.jars)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'jars': len(result['jars']), 'counts': {k: len(v) for k, v in result['resources'].items()},
                      'parse_errors': len(result['parse_errors']), 'optional_resources': len(result['optional_resources'])}))


if __name__ == '__main__':
    main()
