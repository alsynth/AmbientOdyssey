"""Owner decision 15 Oct 2026: Pinnacle = native five epic gear criteria + a Captain Cornelia kill."""
import hashlib, json, os, struct, sys, unittest, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import compile_pinnacle_cornelia_gate as gen

OVERRIDE = gen.DATA / 'data/apotheosis/advancement/progression/pinnacle.json'
EVIDENCE = ROOT / 'docs/handoffs/pinnacle-gate-20261015/CORNELIA_EVIDENCE.json'
CAMPAIGN = ROOT / 'addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign'
MODS = Path(os.environ.get('AO_MODS_DIR', r'C:/Users/headq/curseforge/minecraft/Instances/Ambient Odyssey v0.4.9.1 - Structure Difficulty + Celestisynth TEST/mods'))
EPIC = ['epic_helm', 'epic_chest', 'epic_legs', 'epic_feet', 'epic_hand']


def class_strings(data):
    count = struct.unpack('>H', data[8:10])[0]; i = 10; k = 1; utf = {}; refs = []
    while k < count:
        t = data[i]
        if t == 1:
            n = struct.unpack('>H', data[i + 1:i + 3])[0]; utf[k] = data[i + 3:i + 3 + n].decode('utf-8'); i += 3 + n
        elif t in (3, 4, 9, 10, 11, 12, 17, 18): i += 5
        elif t in (5, 6): i += 9; k += 1
        elif t in (7, 16, 19, 20): i += 3
        elif t == 8: refs.append(struct.unpack('>H', data[i + 1:i + 3])[0]); i += 3
        elif t == 15: i += 4
        else: raise ValueError(t)
        k += 1
    return [utf[r] for r in refs]


class PinnacleCorneliaGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = OVERRIDE.read_bytes(); cls.data = json.loads(cls.raw)

    def test_everything_except_dragon_criterion_is_native_byte_for_byte(self):
        # Reverse the only substitution; the result must be the exact pinned native file.
        native = self.raw.decode('utf-8').replace(gen.CORNELIA_KILL, gen.NATIVE_DRAGON).replace('"kill_captain_cornelia"', '"kill_ender_dragon"')
        self.assertEqual(hashlib.sha256(native.encode('utf-8')).hexdigest(), gen.NATIVE_SHA256)

    def test_five_epic_criteria_unchanged(self):
        crit = self.data['criteria']
        self.assertEqual(sorted(crit), sorted(EPIC + ['kill_captain_cornelia']))
        slots = {'epic_helm': 'head', 'epic_chest': 'chest', 'epic_legs': 'legs', 'epic_feet': 'feet', 'epic_hand': 'hand'}
        for name, slot in slots.items():
            c = crit[name]
            self.assertEqual(c['trigger'], 'apotheosis:equipped_item')
            self.assertEqual(c['conditions']['slots'], slot)
            self.assertEqual(c['conditions']['items']['predicates']['apotheosis:item_with_rarity']['rarities'],
                             ['apotheosis:epic', 'apotheosis:mythic'])
        self.assertEqual(self.data['requirements'], [[n] for n in EPIC] + [['kill_captain_cornelia']])

    def test_cornelia_criterion_shape(self):
        c = self.data['criteria']['kill_captain_cornelia']
        self.assertEqual(c['trigger'], 'minecraft:player_killed_entity')
        self.assertEqual(c['conditions']['entity'], [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                      'predicate': {'type': 'aquamirae:captain_cornelia'}}])
        self.assertNotIn(b'ender_dragon', self.raw)

    def test_cornelia_resolves_to_registered_entity(self):
        ev = json.loads(EVIDENCE.read_text(encoding='utf-8'))
        self.assertEqual(ev['entity_id'], gen.CORNELIA)
        self.assertTrue(ev['registry_literal_present'])
        self.assertIn('aquamirae:captain_cornelia', (CAMPAIGN / 'AOCampaign.java').read_text(encoding='utf-8'))
        jar = MODS / ev['jar']
        if not jar.is_file(): self.skipTest('Aquamirae JAR not available; recorded evidence checked')
        self.assertEqual(hashlib.sha256(jar.read_bytes()).hexdigest(), ev['jar_sha256'])
        z = zipfile.ZipFile(jar)
        self.assertIn('captain_cornelia', class_strings(z.read(ev['registry_class'])))
        self.assertIn('data/aquamirae/loot_table/entities/captain_cornelia.json', z.namelist())

    def test_no_impossible_anywhere_in_gate_packs(self):
        for root in (gen.DATA, gen.LANG):
            for p in root.rglob('*'):
                if p.is_file(): self.assertNotIn(b'minecraft:impossible', p.read_bytes(), p)

    def test_criterion_has_a_display_name(self):
        lang = json.loads((gen.LANG / 'assets/apotheosis/lang/en_us.json').read_text(encoding='utf-8'))
        self.assertIn('advancements.apotheosis.progression.pinnacle.criteria.kill_captain_cornelia', lang)

    def test_no_code_grants_pinnacle(self):
        for p in CAMPAIGN.glob('*.java'):
            src = p.read_text(encoding='utf-8')
            self.assertNotIn('progression/pinnacle', src, p.name)
            self.assertNotIn('getUnlockAdvancement', src, p.name)
            self.assertNotIn('kill_captain_cornelia', src, p.name)

    def test_generator_output_is_current(self):
        jar = MODS / 'Apotheosis-1.21.1-8.9.0.jar'
        if not jar.is_file(): self.skipTest('Apotheosis JAR not available')
        for p, b in gen.build(gen.native_bytes(jar)).items(): self.assertEqual(gen.lf(p.read_bytes()), b, p)


if __name__ == '__main__':
    unittest.main()
