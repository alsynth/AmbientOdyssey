"""Regression gate: no shipped datapack may lock an advancement behind minecraft:impossible
unless code grants it on purpose.

R4 shipped ao_campaign_gates, which replaced the native apotheosis:progression/pinnacle criteria
with minecraft:impossible after campaign code stopped granting it, leaving Pinnacle unobtainable
except via operator /advancement grant. Latest owner decision (15 Oct 2026): Pinnacle = native five
epic gear criteria + a Captain Cornelia kill; ao_campaign_gates now carries exactly that override
(tests/test_pinnacle_cornelia_gate.py). No other native progression file may be overridden.
"""
import json, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_SRC = ROOT / 'addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/AOCampaign.java'
# Every datapack root that a build copies into an import.
SOURCE_ROOTS = [ROOT / 'release_030/overrides', ROOT / 'release_030/experimental_overlays', ROOT / 'addons']
GATE_FILES = ['config/paxi/datapacks/ao_campaign_gates/pack.mcmeta',
              'config/paxi/datapacks/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json']
APPROVED_OVERRIDE = ('release_030/experimental_overlays/v050/overrides/'
                     'config/paxi/datapacks/ao_campaign_gates/data/apotheosis/advancement/progression/pinnacle.json')


def advancement_files():
    for root in SOURCE_ROOTS:
        for p in root.rglob('*.json'):
            parts = p.as_posix().split('/')
            if 'advancement' in parts and '/build/' not in p.as_posix():
                yield p


def advancement_id(path):
    parts = path.as_posix().split('/')
    i = len(parts) - 1 - parts[::-1].index('data')
    j = parts.index('advancement', i)
    return parts[i + 1] + ':' + '/'.join(parts[j + 1:])[:-len('.json')]


def code_granted_ids():
    text = CAMPAIGN_SRC.read_text(encoding='utf-8')
    ids = set(re.findall(r'grant\(player,\s*"([a-z0-9_]+:[a-z0-9_/]+)"\)', text))
    # grant(player, "ao_campaign:milestones/tier_" + tier) covers every tier milestone.
    if re.search(r'grant\(player,\s*"ao_campaign:milestones/tier_"\s*\+\s*tier\)', text):
        ids |= {'ao_campaign:milestones/tier_%d' % t for t in range(2, 10)}
    return ids


def impossible_criteria(data):
    return [k for k, v in data.get('criteria', {}).items() if v.get('trigger') == 'minecraft:impossible']


class NoImpossibleTierGates(unittest.TestCase):
    def test_only_the_approved_pinnacle_override_exists(self):
        overrides = [p.relative_to(ROOT).as_posix() for p in advancement_files()
                     if advancement_id(p).startswith('apotheosis:progression/')]
        self.assertEqual(overrides, [APPROVED_OVERRIDE], 'Only the owner-approved Pinnacle override may exist')

    def test_impossible_only_where_code_grants(self):
        granted = code_granted_ids()
        unreachable = []
        for p in advancement_files():
            data = json.loads(p.read_text(encoding='utf-8'))
            if impossible_criteria(data) and advancement_id(p) not in granted:
                unreachable.append((advancement_id(p), p.relative_to(ROOT).as_posix()))
        self.assertEqual(unreachable, [], 'minecraft:impossible without a code grant is unobtainable')

    def test_campaign_milestones_remain_code_granted(self):
        granted = code_granted_ids()
        for name in ['tier_5', 'tier_6', 'tier_7', 'tier_8', 'tier_9', 'tyros', 'scylla', 'obsidilith']:
            self.assertIn('ao_campaign:milestones/' + name, granted)

    def test_campaign_does_not_grant_world_tiers(self):
        text = CAMPAIGN_SRC.read_text(encoding='utf-8')
        # A leftover unused import of WorldTier is harmless; any use of it is not.
        self.assertNotRegex(text, r'WorldTier\.')
        self.assertNotIn('getUnlockAdvancement', text)
        self.assertNotIn('progression/pinnacle', text)

    def test_gate_pack_ships_and_is_not_stripped(self):
        for rel in GATE_FILES:
            self.assertTrue((ROOT / 'release_030/experimental_overlays/v050/overrides' / rel).is_file(), rel)
        removed = json.loads((ROOT / 'docs/handoffs/integration-20261015/removed-source-paths.json').read_text())
        for rel in GATE_FILES:
            self.assertNotIn(rel, removed)  # the packager would otherwise pop the new override


if __name__ == '__main__':
    unittest.main()
