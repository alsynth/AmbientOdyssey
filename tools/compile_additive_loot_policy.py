"""Compile only authenticated owner bands; no unknown catalogue item is auto-approved."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOC=ROOT/'docs/handoffs/loot-update-20261015'
def compile_policy():
 rows=list(csv.DictReader((ROOT/'docs/balance/REGALIA_COMBAT_PRIORITY_RANKING_20261013.csv').open(encoding='utf-8-sig')))
 # Reviewed low/moderate utility Artifacts plus two explicitly approved Aquamirae C4 exceptions.
 regalia=sorted({r['item_registry_candidate'] for r in rows if r['combat_risk_band'][:2] in {'C0','C1','C2'} and r['item_registry_candidate'].startswith('artifacts:')}|{'aquamirae:abyssal_tiara','aquamirae:tempest_trident'})
 bosses={}
 for r in json.loads((ROOT/'docs/handoffs/integration-20261015/boss-reconciliation.json').read_text()):
  if r['entity_id'].startswith(('iceandfire:fire_dragon','iceandfire:ice_dragon','iceandfire:lightning_dragon','eternal_starlight:')):continue
  bosses[r['entity_id']]=r['current_category_tier']
 bosses.update({'bosses_of_mass_destruction:lich':5,'bosses_of_mass_destruction:void_blossom':5,'bosses_of_mass_destruction:gauntlet':5,'twilightforest:hydra':4})
 unique=json.loads((DOC/'simplyswords-native-uniques.json').read_text())['values']
 data={'bosses':bosses,'regalia':regalia,'unique_weapons':sorted(set(unique)),
   'rare_affix_rates':{'6':{'ancient':.20,'artifact':.02},'7':{'ancient':.25,'artifact':.08,'heirloom':.05},'8':{'ancient':.30,'artifact':.15,'heirloom':.08,'esoteric':.05}},
   'grand_treasure':json.loads((DOC/'grand-treasure-candidates.json').read_text()),
   'native_gems':'UNCHANGED; no AO gem rewards or World Tier unlock overrides',
   'regalia_unreviewed':'Held, including unresolved Annihilator and native-exclusive boss trophy candidates',
   'ownership':'One additive set per player-credited kill; pickup targeted to credited killer; no per-party multiplication'}
 p=ROOT/'addons/ao-campaign/src/main/resources/ao_loot_policy.json';p.write_text(json.dumps(data,indent=2)+'\n')
 (DOC/'effective-loot-policy.json').write_text(json.dumps(data,indent=2)+'\n')
 print('Policy:',len(bosses),'boss entity IDs,',len(regalia),'Regalia,',len(unique),'unique weapons,',len(data['grand_treasure']),'Grand contexts')
if __name__=='__main__':compile_policy()
