#!/usr/bin/env python3
"""Regenerate the structure screening reports from saved, scoped evidence."""
import csv
import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = ROOT / 'release_030'
E = R / 'evidence'

# File metadata verified on the primary CurseForge file pages, 9 October 2026.
# These are staged choices, not entries in the locked installation manifest.
APPROVED = [
    ('YUNG\'s Extras', 'yungs-extras-neoforge', 1015146, 5812546, 'YungsExtras-1.21.1-NeoForge-5.1.1.jar'),
    ('YUNG\'s Bridges', 'yungs-bridges-neoforge', 1015149, 5812553, 'YungsBridges-1.21.1-NeoForge-5.1.1.jar'),
    ('Structory: Towers', 'structory-towers', 783522, 7078283, 'Structory_Towers_1.21.x_v1.0.14.jar'),
    ('Archaion', 'archaion', 1620396, 8983496, 'archaion-1.21.1-1.4.4.jar'),
    ('Explorify', 'explorify', 698309, 8082824, 'Explorify v1.6.5.mod.jar'),
    ('Additional Structures', 'additional-structures', 297680, 6584803, 'AdditionalStructures-1.21-(v.6.3.2-NEO).jar'),
    ('Create: Structures Arise', 'create-structures-arise', 1010066, 8837992, 'Create-Structures-Arise-1.21.1-NeoForge-176.49.49.jar'),
    ('Create: Easy Structures', 'create-easy-structures', 949158, 6344382, 'create_easy_structures-0.2a-neoforge-1.21.1.jar'),
]


def write_csv(name, rows):
    assert rows
    with (ROOT / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    snapshot = json.loads(gzip.decompress((E / 'jar-resource-index-test5.json.gz').read_bytes()))
    screens = {row['jar']: row for row in json.loads((E / 'new-jar-screen.json').read_text())}
    coverage = json.loads((E / 'jar-audit-coverage-test5.json').read_text())
    stage = []
    for name, slug, project, file, filename in APPROVED:
        stage.append({'name': name, 'slug': slug, 'projectID': project, 'fileID': file,
                      'filename': filename, 'game_version': '1.21.1', 'loader': 'NeoForge',
                      'primary_file_url': f'https://www.curseforge.com/minecraft/mc-mods/{slug}/files/{file}',
                      'metadata_verified_date': '2026-10-09', 'sha256': None,
                      'enabled': False, 'binary_audited': False, 'dependencies_verified': False,
                      'status': 'BLOCKED_JAR_AUDIT',
                      'special_requirement': ('Identify and disable the exact Nether Black Spiral placement route before installation.' if slug == 'explorify' else 'Audit definitions, pools, features, code placement and dependencies before installation.')})
    authoring = R / 'approved-structure-additions.json'
    if authoring.exists():
        # The JSON is the editable authoring source. Report regeneration must
        # preserve deliberate pin edits rather than silently restoring defaults.
        payload = json.loads(authoring.read_text())
        stage = payload['mods']
        assert len(stage) == 8 and payload['manifest_mutation'] is False
    else:
        authoring.write_text(json.dumps({
            'schema': 1, 'scope': 'Approved staged additions; not installed by Test 5 audit1.',
            'manifest_mutation': False, 'mods': stage}, indent=2) + '\n')
    write_csv('APPROVED_STRUCTURE_ADDITIONS.csv', stage)
    (ROOT / 'APPROVED_ADDITION_JARS.txt').write_text(
        'Eight approved additions: exact proposed binaries to provide for the next audit.\n'
        'Separate from the 41 missing existing-profile JARs in MISSING_JARS.txt.\n'
        'File metadata is verified; checksums, dependency closure and native content await actual JARs.\n\n'
        + '\n'.join(row['filename'] for row in stage) + '\n')

    installed = []
    for row in snapshot['jars']:
        filename = row['file']
        fresh = screens.get(filename)
        counts = row['counts']
        structure_count = counts.get('worldgen/structure', 0)
        related = sum(counts.get(k, 0) for k in ['worldgen/structure_set', 'worldgen/template_pool',
                        'worldgen/configured_feature', 'worldgen/placed_feature', 'lithostitched/worldgen_modifier'])
        decision = fresh['classification'] if fresh else (
            'STRUCTURE_PROVIDER' if structure_count else 'PLACEMENT_OR_TEMPLATE_DATA_REVIEW' if related
            else 'NO_STRUCTURE_DEFINITION_IN_RECORDED_CATEGORIES')
        installed.append({'jar': filename, 'sha256': row['sha256'], 'bytes': row['bytes'],
                          'structure_definitions': structure_count,
                          'structure_sets': counts.get('worldgen/structure_set', 0),
                          'template_pools': counts.get('worldgen/template_pool', 0),
                          'biome_tags': counts.get('tags/worldgen/biome', 0),
                          'screening_decision': decision,
                          'current_binary_class_screen': bool(fresh),
                          'newly_recovered': filename in coverage['newly_recovered_logged_jars'],
                          'evidence_scope': ('Current complete binary: CRC, SHA, resource inventory and class-reference screen' if fresh
                                             else 'Preserved original complete-binary CRC/SHA/resource snapshot; no new class inspection'),
                          'negative_scope': 'No absence certification; code, features, builtin packs and dependencies require review.'})
    write_csv('INSTALLED_MOD_STRUCTURE_SCREENING.csv', installed)

    registry = (E / 'CANDIDATE_REGISTRY_2026-10-06.md').read_text()
    candidates = []
    for match in re.finditer(r'^(\d+)\. \*\*(.+?)\*\* — (.+)$', registry, re.M):
        ordinal, name, description = match.groups()
        lower = (name + ' ' + description).lower()
        relevant = any(word in lower for word in ['structure', 'worldgen', 'terrain', 'biome', 'dimension',
                     'dungeon', 'village', 'temple', 'tower', 'ship', 'boss', 'cave', 'ruin', 'trial', 'road', 'river', 'ocean'])
        status = 'Unselected research backlog; current master TODO takes precedence.'
        if name.startswith('Archaion'):
            status = 'Approved; exact binary/dependencies still pending.'
        elif name == 'StructureOverlapless':
            status = 'Do not install with current Integrated API arrangement; superseded by master TODO.'
        elif 'Big Globe' in name:
            status = 'Separate deferred experiment.'
        elif 'Sunken Spires' in name:
            status = 'Deferred ocean expansion.'
        elif name == 'Streams Reflowing':
            status = 'Already retained in current terrain stack.'
        elif name == 'Integrated Patches':
            status = 'Already retained by the locked current build.'
        candidates.append({'registry_number': int(ordinal), 'candidate': name,
                           'recorded_assessment_and_description': description,
                           'screening_decision': 'AUDIT_WORLDGEN_OR_PLACEMENT_ROUTES' if relevant else 'NO_STRUCTURE_CLAIM_IN_RECORDED_DESCRIPTION',
                           'evidence_scope': 'Description triage only; no binary audit or current-version compatibility certification.',
                           'master_decision': status,
                           'required_before_install': 'Exact 1.21.1 NeoForge binary, dependency closure, resources/builtin packs/features/code route screen.'})
    assert len(candidates) == 166 and {x['registry_number'] for x in candidates} == set(range(1, 167))
    write_csv('FUTURE_MOD_STRUCTURE_SCREENING.csv', candidates)

    # Public positives help find further providers without turning discovery
    # into authorization to add them. Unknown negatives stay unknown.
    stage_by_slug = {row['slug']: row for row in stage}
    create = [
        {'candidate': 'Create: Rustic Structures', 'structure_evidence': 'Actual binary: 4 structures, 4 sets, 4 pools; curated selector repairs included.',
         'decision': 'Retained; audited and repaired', 'primary_url': 'https://www.curseforge.com/minecraft/mc-mods/create-rustic-structures'},
        {'candidate': 'Create: Structures Arise', 'structure_evidence': 'Approved structure addon; pinned file metadata supports 1.21.1 NeoForge. Native content pending.',
         'decision': 'Approved; blocked on binary audit', 'primary_url': stage_by_slug['create-structures-arise']['primary_file_url']},
        {'candidate': 'Create: Easy Structures', 'structure_evidence': 'Approved structure addon; pinned file metadata supports 1.21.1 NeoForge. Native content pending.',
         'decision': 'Approved; blocked on binary audit', 'primary_url': stage_by_slug['create-easy-structures']['primary_file_url']},
        {'candidate': 'Create: Structures Overhaul', 'structure_evidence': 'Official project describes biome-themed natural, locatable structures and optional BOP integration.',
         'decision': 'Unselected; metadata/version and binary audit required', 'primary_url': 'https://www.curseforge.com/minecraft/mc-mods/create-structures-overhaul'},
        {'candidate': 'Create: Let The Adventure Begin', 'structure_evidence': 'Official project describes Create-themed structures; 1.21.1 release metadata was located.',
         'decision': 'Unselected; binary and dependency audit required', 'primary_url': 'https://www.curseforge.com/minecraft/mc-mods/create-let-the-adventure-begin'},
        {'candidate': 'Create: structures', 'structure_evidence': 'Official project describes railway stations and requires several Create addons; latest file title/game-tag mismatch needs resolution.',
         'decision': 'Unselected; do not select a file from its filename alone', 'primary_url': 'https://www.curseforge.com/minecraft/mc-mods/create-structures'},
        {'candidate': 'Create: The Factory Must Grow / The Factory Must Work', 'structure_evidence': 'Oil-deposit/worldgen feature routes warrant inspection; this does not establish natural building generation.',
         'decision': 'Unselected; exact project/version and feature/code audit required', 'primary_url': 'https://www.curseforge.com/minecraft/mc-mods/create-the-factory-must-grow'},
        {'candidate': 'Create: Diesel Generators / New Age and other technical addons', 'structure_evidence': 'No binary absence proof available; machinery descriptions alone do not certify absence of features or structures.',
         'decision': 'Unselected; screen exact binaries before any future installation', 'primary_url': ''},
    ]
    write_csv('CREATE_ADDON_STRUCTURE_SCREENING.csv', create)
    new_table = '\n'.join(f"| `{row['jar']}` | {row['classification']} | {row['counts'].get('worldgen/structure', 0)} | {row['counts'].get('worldgen/structure_set', 0)} |" for row in screens.values() if row['new_to_audit'])
    approved_table = '\n'.join(f"| {row['name']} | {row['projectID']} / {row['fileID']} | `{row['filename']}` |" for row in stage)
    create_table = '\n'.join(f"| {row['candidate']} | {row['structure_evidence']} | {row['decision']} |" for row in create)
    text = f'''# Ambient Odyssey — Structure-provider screening, Test 5 audit1

Updated 9 October 2026. The current master TODO authorizes eight additions; they remain staged because their exact binaries are unavailable. This export repairs the audited existing stack. It does not install unselected Create addons or promote the project to 0.4.0.

## Evidence and coverage

- 196 complete binaries are represented by CRC/SHA/resource evidence: the preserved 177-JAR baseline plus 19 newly recovered binaries.
- 26 unique complete binaries were available for direct inspection this continuation: those 19 plus 7 re-supplied baseline JARs. Their class-reference screen is recorded in `evidence/new-jar-screen.json` and `evidence/new-jar-details.json.gz`.
- 41 exact logged JAR filenames remain unavailable. `MISSING_JARS.txt` is the manual-upload list; these are separate from the eight new additions.
- The old large-archive transfer record is historical. The current full `mods2.zip` transfer returned HTTP 403; old resource evidence is retained without claiming a new binary inspection.
- `INSTALLED_MOD_STRUCTURE_SCREENING.csv` has one row per audited JAR with SHA, resource counts and evidence scope. Zero structure JSON is not proof of zero worldgen.

## Newly recovered existing-profile binaries

| JAR | Screen | Structures | Sets |
|---|---|---:|---:|
{new_table}

CTOV has 78 native structure definitions and zero native structure-set JSON files. Its inspected Java/config route adds 63 enabled village entries and 11 outpost entries to vanilla placement sets through Lithostitched. The 74 routes are in `CODE_GENERATED_PLACEMENT_ROUTES.csv`; actual runtime application remains untested.

YUNG's Better End Island changes End generation through EndDragonFight/spike/gateway/platform code rather than standalone structure JSON. Waystones has feature, pool and Lithostitched village integration routes. Both must remain in worldgen screening even when the standalone structure-definition count is zero. Cristel Lib and YUNG's API are frameworks; framework class references alone do not make them independent landmark providers.

## Eight approved additions — metadata selected, installation pending

| Mod | CurseForge project / file | Exact proposed JAR |
|---|---|---|
{approved_table}

Primary file URLs and verification date are in `APPROVED_STRUCTURE_ADDITIONS.csv` and editable `release_030/approved-structure-additions.json`. All eight have `enabled=false`, `binary_audited=false`, `dependencies_verified=false` and no invented SHA-256. They are absent from the locked candidate manifest. `APPROVED_ADDITION_JARS.txt` provides the separate upload list.

For each binary, inspect native definitions, placement sets, pools/NBT, tags, features, biome modifiers, builtin packs and registration/mixin code; verify dependencies against the exact installed pins. Select native placement owners before adjusting candidate density. Explorify must remain out of the export until the exact Nether Black Spiral ID and disabling mechanism are verified; no guessed ID or ineffective empty-tag patch is included.

## Other Create addons

| Candidate | Evidence | Current decision |
|---|---|---|
{create_table}

`CREATE_ADDON_STRUCTURE_SCREENING.csv` includes primary project links. Public project/file descriptions establish a screening priority, not a completed binary audit or permission to install. Structures, worldgen features such as oil deposits, and manually/instance-created content must be recorded separately.

## Future pack candidates

`FUTURE_MOD_STRUCTURE_SCREENING.csv` preserves all 166 numbered candidates from the 6 October registry, with a first-pass description screen. Potential worldgen, village, dungeon, dimension, boss or terrain routes are flagged for binary review. Other descriptions receive “no structure claim in recorded description”, never a certified “adds no structures”. The current master TODO supersedes the registry's old install preferences, particularly StructureOverlapless and competing terrain stacks. The registry is an audit backlog, not an installation list.

## Remaining work

Prioritize the unavailable Create, dimension and worldgen libraries/providers, including Create, CreateOPlenty, Undergarden, Deep Aether, Deeper and Darker, Bumblezone, Twilight Forest, Dimensional Doors, TRMT, Citadel/Zeta/Corgilib/WorldWeaver/Wunderlib and the Cook-related assets. Library status alone does not prove a JAR is irrelevant; dependencies can carry assets or code routes.

The current catalogues cover recorded native definitions and code-derived CTOV routes. They retain unresolved base-game/optional tags and 70 native structure/set/pool resource collisions. Actual runtime resource priority, Cristel/Paxi priority, successful natural generation and fresh-world density remain acceptance tasks. They are not prerequisites for delivering this static repair candidate.
'''
    (ROOT / 'MOD_STRUCTURE_SCREENING.md').write_text(text)
    print(json.dumps({'audited_jars': len(installed), 'current_complete_binary_screens': len(screens),
                      'new_binaries': len(coverage['newly_recovered_logged_jars']),
                      'missing_existing_jars': len(coverage['unretrieved_logged_jars']),
                      'approved_staged': len(stage), 'future_description_rows': len(candidates),
                      'create_screen_rows': len(create)}))


if __name__ == '__main__':
    main()
