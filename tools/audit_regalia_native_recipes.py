"""Authenticate a small reviewed Regalia extension against installed native resources.

Recipe evidence is source verification, not runtime item-registry verification.
Only explicitly listed catalogue items are considered; unknown candidates stay held.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RECIPES = {
    'dagger_of_hunger': 'data/eternal_starlight/recipe/dagger_of_hunger.json',
    'chain_of_souls': 'data/eternal_starlight/recipe/chain_of_souls.json',
    'soulit_spectator': 'data/eternal_starlight/recipe/shapeless/soulit_spectator.json',
    'etheric_eye': 'data/eternal_starlight/recipe/etheric_eye.json',
}


def is_native_crafting_output(recipe, item):
    return (recipe.get('type') in {'minecraft:crafting_shaped', 'minecraft:crafting_shapeless'}
            and recipe.get('result', {}).get('id') == item
            and not recipe.get('neoforge:conditions') and not recipe.get('conditions'))


def audit(jar):
    rows = []
    with zipfile.ZipFile(jar) as z:
        lang = json.loads(z.read('assets/eternal_starlight/lang/en_us.json'))
        boss_tables = {n: json.loads(z.read(n)) for n in z.namelist()
                       if n.startswith('data/eternal_starlight/loot_table/bosses/') and n.endswith('.json')}
        for name, resource in RECIPES.items():
            item = 'eternal_starlight:' + name
            raw = z.read(resource)
            if not is_native_crafting_output(json.loads(raw), item):
                raise ValueError('Not an unconditional native crafting output: ' + item)
            if 'item.eternal_starlight.' + name not in lang:
                raise ValueError('Missing native item language key: ' + item)
            direct = [n for n, obj in boss_tables.items() if item in json.dumps(obj)]
            if direct:
                raise ValueError('Boss loot candidate needs separate acquisition review: ' + item)
            rows.append({'item': item, 'native_recipe': resource,
                         'recipe_sha256': hashlib.sha256(raw).hexdigest(),
                         'direct_native_boss_tables': direct,
                         'status': 'SOURCE_VERIFIED_CRAFTABLE; RUNTIME_REGISTRY_PENDING'})
    return {'jar': jar.name, 'jar_sha256': hashlib.sha256(jar.read_bytes()).hexdigest(),
            'scope': 'Four reviewed C0/C1 catalogue entries; no blanket item-family approval',
            'runtime_verified': False, 'items': rows}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('jar', type=Path)
    a = p.parse_args()
    result = audit(a.jar)
    out = ROOT / 'docs/handoffs/loot-update-20261015/regalia-native-extension.json'
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Authenticated', len(result['items']), 'native crafting outputs; runtime registry pending')
