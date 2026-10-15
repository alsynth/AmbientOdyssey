"""Static guards for source/R4 parity (no R4 ZIP needed; tools/check_source_r4_parity.py does the full diff)."""
import json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT / 'release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes/data/minecells/recipe'


class SourceR4Parity(unittest.TestCase):
    def test_mod_rewritten_manifest_is_valid(self):
        data = json.loads((ROOT / 'release_030/MOD_REWRITTEN_CONFIGS.json').read_text(encoding='utf-8'))
        paths = [f['path'] for f in data['files']]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(len(paths), 17)
        for f in data['files']:
            self.assertIn(f['evidence'], {'jar_string', 'inferred'})
            self.assertTrue((ROOT / 'release_030/overrides' / f['path']).is_file(), f['path'])
        # Generated Mine Cells recipes are real content, never "ignore".
        self.assertFalse(any('minecells' in p for p in paths))

    def test_minecells_recipes_are_generated_not_stubs(self):
        files = sorted(RECIPES.glob('**/*.json'))
        self.assertEqual(len(files), 15)
        for p in files:
            data = json.loads(p.read_text(encoding='utf-8'))
            conds = data.get('neoforge:conditions', [])
            self.assertNotIn({'type': 'neoforge:false'}, conds, p.name)
            self.assertTrue(any(c.get('type') == 'neoforge:mod_loaded' for c in conds), p.name)
            self.assertIn('type', data)
            self.assertNotIn(b'\r', p.read_bytes())


if __name__ == '__main__':
    unittest.main()
