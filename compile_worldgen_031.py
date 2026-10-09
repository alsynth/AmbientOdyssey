#!/usr/bin/env python3
"""Compile editable AO pools into Biolith 3.0.14's real datapack format."""
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / 'release_030'
DATA = RELEASE / 'overrides/config/paxi/datapacks/ao_biome_replacement/data/ambient_odyssey'

def compile_pools():
    config = json.loads((RELEASE / 'biome-pools.json').read_text())
    roster = json.loads((RELEASE / 'biome-roster.json').read_text())
    curated = {f'{ns}:{name}' for ns, names in roster.items() for name in names}
    rules = {'additions': [], 'removals': [], 'replacements': [], 'sub_biomes': []}
    all_targets = []
    for pool in config['pools']:
        vanilla = Fraction(str(pool['vanilla_percent'])) / 100
        assert 0 <= vanilla < 1, pool['name']
        weights = {biome: Fraction(str(weight)) for biome, weight in pool['biomes'].items()}
        assert weights and all(w > 0 for w in weights.values()), pool['name']
        assert set(weights).issubset(curated), pool['name']
        total = sum(weights.values())
        fractions = {biome: weight / total for biome, weight in weights.items()}
        # Biolith retains 1-max(proportions) vanilla, then normalizes all requests.
        # Solve that rule for the requested vanilla fraction and relative weights.
        denominator = max(fractions.values()) + vanilla / (1 - vanilla)
        rates = {biome: fraction / denominator for biome, fraction in fractions.items()}
        retained = 1 - max(rates.values())
        assert retained / (sum(rates.values()) + retained) == vanilla
        for target in pool['targets']:
            assert target.startswith('minecraft:') and target not in all_targets, target
            all_targets.append(target)
            for biome, rate in rates.items():
                rules['replacements'].append({
                    'dimension': config['dimension'], 'target': target,
                    'biome': biome, 'proportion': round(float(rate), 12)
                })
    for guard in config.get('climate_guards', []):
        assert guard['biome'] in curated
        for target in guard['targets']:
            assert target in curated
            rules['sub_biomes'].append({
                'dimension': config['dimension'], 'target': target, 'biome': guard['biome'],
                'criterion': {'type': 'biolith:all_of', 'criteria': [
                    {'type': 'biolith:original', 'biome': '#ambient_odyssey:replaced_surface_biomes'},
                    {'type': 'biolith:value', 'parameter': 'temperature', **guard['temperature']}
                ]}
            })
    placement = DATA / 'biolith/biome_placement.json'
    placement.parent.mkdir(parents=True, exist_ok=True)
    placement.write_text(json.dumps(rules, indent=2) + '\n', newline='\n')
    tag = DATA / 'tags/worldgen/biome/replaced_surface_biomes.json'
    tag.parent.mkdir(parents=True, exist_ok=True)
    tag.write_text(json.dumps({'replace': False, 'values': all_targets}, indent=2) + '\n', newline='\n')
    print(f'{len(all_targets)} vanilla targets, {len(rules["replacements"])} pool rules, '
          f'{len(rules["sub_biomes"])} climate guards')
    return rules

if __name__ == '__main__':
    compile_pools()
