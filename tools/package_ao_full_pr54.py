"""Build a separate, reproducible private full import through draft PR54."""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import zipfile

import package_ao_loot_economy_pilot as loot

ROOT = Path(__file__).resolve().parents[1]
SIGIL_NAME = 'ao-augmenting-sigils-0.1.1-experimental.jar'


def build(base, starter, sigils, output, campaign=None):
    base, starter, sigils, output = map(Path, (base, starter, sigils, output))
    if output.exists() or output.resolve() in {p.resolve() for p in (base, starter, sigils)}:
        raise ValueError('Output must be new and separate from inputs')
    jar = loot.read_zip(sigils)
    for name in ('dev/ambientodyssey/augmentingsigils/SigilCosts.class',
                 'dev/ambientodyssey/augmentingsigils/mixin/AugmentingMenuMixin.class',
                 'dev/ambientodyssey/augmentingsigils/mixin/AugmentingTooltipsMixin.class',
                 'META-INF/neoforge.mods.toml', 'ao_augmenting_sigils.mixins.json'):
        if name not in jar:
            raise ValueError('Missing compiled Sigil addon member: ' + name)
    if 'ao_augmenting_sigils' not in jar['META-INF/neoforge.mods.toml'][1].decode():
        raise ValueError('Unexpected Sigil mod identity')
    for resource in ('ao_augmenting_sigils.mixins.json', 'META-INF/neoforge.mods.toml'):
        if jar[resource][1] != (ROOT / 'addons/ao-augmenting-sigils/src/main/resources' / resource).read_bytes():
            raise ValueError('Sigil artifact resources differ from reviewed source')
    starter_members = loot.read_zip(starter)
    resources = ROOT / 'addons/ao-starter-chest/src/main/resources'
    for source in resources.rglob('*'):
        if source.is_file():
            name = source.relative_to(resources).as_posix()
            # NeoForge generates mod-pack metadata; the validated CI JAR omits this source file.
            if name == 'pack.mcmeta' and name not in starter_members:
                continue
            if name not in starter_members or starter_members[name][1] != source.read_bytes():
                raise ValueError('Starter artifact resource differs from source: ' + name)
    (ROOT / 'build').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ao-pr54-', dir=ROOT / 'build') as temp:
        intermediate = Path(temp) / 'loot.zip'
        with contextlib.redirect_stdout(io.StringIO()):
            loot_report = loot.build(base, starter, intermediate)
        entries = loot.read_zip(intermediate)
    original = loot.read_zip(base)
    payload = {n: data for n, (_, data) in entries.items()}
    rarity_root = ROOT / 'release_030/overrides/config/paxi/datapacks/ao_world_tier_balance'
    rarity_files = sorted(p for p in rarity_root.rglob('*') if p.is_file())
    if {p.relative_to(rarity_root).as_posix() for p in rarity_files} != {
        'pack.mcmeta', *('data/apotheosis/rarities/' + r + '.json' for r in ('uncommon', 'rare', 'epic', 'mythic'))
    }:
        raise ValueError('Unexpected rarity overlay file set')
    for p in rarity_files:
        data = p.read_bytes()
        json.loads(data)
        loot.checked_add(payload, 'overrides/config/paxi/datapacks/ao_world_tier_balance/' + p.relative_to(rarity_root).as_posix(), data)
    loot.checked_add(payload, loot.MOD_ROOT + SIGIL_NAME, sigils.read_bytes())
    if campaign:
        campaign = Path(campaign)
        campaign_members = loot.read_zip(campaign)
        for name in ('dev/ambientodyssey/campaign/AOCampaign.class', 'dev/ambientodyssey/campaign/RageGloveGate.class',
                     'dev/ambientodyssey/campaign/BossGems.class', 'META-INF/neoforge.mods.toml'):
            if name not in campaign_members: raise ValueError('Incomplete campaign JAR: ' + name)
        loot.checked_add(payload, loot.MOD_ROOT + 'ao-campaign-0.1.0-experimental.jar', campaign.read_bytes())
        overlay = ROOT / 'release_030/experimental_overlays/v050/overrides'
        for p in sorted(overlay.rglob('*')):
            if p.is_file():
                loot.checked_add(payload, 'overrides/' + p.relative_to(overlay).as_posix(), p.read_bytes())
    manifest = json.loads(payload['manifest.json'])
    manifest['name'] = 'Ambient Odyssey - Full Experimental Pack through PR54'
    manifest['version'] = '0.5.0-pr54-experimental'
    if campaign:
        manifest['name'] += ' + Campaign and Deferred Features'
        manifest['version'] += '-campaign'
    payload['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    notes = (
        'PRIVATE EXPERIMENTAL FULL IMPORT THROUGH PR54\n'
        'Includes PR50 full Celestisynth/DD/performance base, PR51 starter/loot/recipes,\n'
        'PR53 World Tier rarity weights, and PR54 rarity-priced augmenting Sigils.\n'
        '338 pinned CurseForge references; 9 bundled custom JARs; 340 physical mod JARs after import.\n'
        'Import as a NEW CurseForge profile. New disposable world, Bonus Chest ON.\n'
        'Full acceptance remains pending: two-player Lootr rolls/restart, JEI/Goblin offers,\n'
        'World Tier data priority/Luck, augmenting tooltip/buttons/payment at 63/64 Sigils,\n'
        'Celestisynth combat, natural encounters/elite stacking and dedicated multiplayer.\n'
        'Deferred designs are not implemented: Simply More stun/flashing, Rage Glove boss gate,\n'
        'v0.5 boss-loot-campaign designs and +1-2 Simply Swords unique damage.\n'
        'Do not promote to production until gameplay acceptance is recorded.\n'
    ).encode()
    loot.checked_add(payload, 'overrides/AO_TEST_NOTES/FULL_PR54.txt', notes)
    if campaign:
        payload['overrides/AO_TEST_NOTES/FULL_PR54.txt'] += (
            '\nCAMPAIGN OVERLAY INCLUDED: 101 additional journal entries (83 are reading notes;\n'
            '1 reserved unassigned End encounter), 7 additional chapters, 10 bundled JARs / 341 physical JARs.\n'
            'Native T5/T6/T7/T8/T9 milestones; one first-clear Artifact/Heirloom/Esoteric gem per grade;\n'
            'one guarded /ao_mastery upgrade of the held affixed item after T8 + Tyros + Scylla.\n'
            'Pinnacle unlock: Dead King or provisional Kobolediator alternate, not automatic activation.\n'
            'Rage Glove: only Netherite Monstrosity player-kill Nether loot, provisional 10% RNG.\n'
            'Simply More stun/implicit_stun and dazzled flash application suppressed.\n'
            'Supersedes deferred statements above for those implemented features.\n'
            'Unassigned third End boss, unproven fight equivalence/party credit, loot-class mapping,\n'
            'measured boss tuning/scaling and full multiplayer acceptance remain OPEN.\n').encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    result = loot.read_zip(output)
    if set(result) != set(payload) or any(result[n][1] != data for n, data in payload.items()):
        raise ValueError('Output readback failed')
    if manifest['files'] != json.loads(original['manifest.json'][1])['files']:
        raise ValueError('CurseForge pins changed')
    custom_count = 10 if campaign else 9
    if len([n for n in result if n.startswith(loot.MOD_ROOT) and n.endswith('.jar')]) != custom_count:
        raise ValueError('Unexpected bundled custom JAR count')
    changed = {n: {'before_sha256': loot.sha(original[n][1]) if n in original else None,
                   'after_sha256': loot.sha(data)}
               for n, data in payload.items() if n not in original or original[n][1] != data}
    allowed_original_changes = set(loot_report['changed'])
    if any(n in original and n not in allowed_original_changes for n in changed):
        raise ValueError('Unexpected original payload change')
    report = {'base_sha256': loot.BASE_SHA256, 'output_sha256': loot.sha(output.read_bytes()),
              'starter_sha256': loot.sha(starter.read_bytes()), 'sigil_sha256': loot.sha(sigils.read_bytes()),
              'cf_references': 338, 'bundled_custom_jars': custom_count, 'expected_physical_mod_jars': 331 + custom_count,
              'included_prs': [50, 51, 53, 54], 'crc_and_member_readback': 'PASS',
              'unrelated_base_payload_preserved': True, 'full_pack_runtime_tested': False,
              'changed': changed}
    Path(str(output) + '.report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'changed'}, indent=2))
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--campaign', type=Path)
    for arg in ('base', 'starter', 'sigils', 'output'):
        p.add_argument('--' + arg, type=Path, required=True)
    a = p.parse_args()
    build(a.base, a.starter, a.sigils, a.output, a.campaign)
