import json,re,tomllib,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MasterIntegration(unittest.TestCase):
 def test_exemptions_and_category_combat_separation(self):
  text=(ROOT/'addons/ao-campaign/src/main/java/dev/ambientodyssey/campaign/AOCampaign.java').read_text()
  for boss in ['chesed','malkuth','geburah']:self.assertIn('Map.entry("fdbosses:'+boss+'", 5)',text)
  self.assertIn('Map.entry("irons_spellbooks:dead_king", 6)',text)
  self.assertIn('Map.entry("aquamirae:captain_cornelia", 6)',text)
  ledger=json.loads((ROOT/'docs/handoffs/integration-20261015/native-balance-ledger.json').read_text())
  self.assertFalse(any('fdbosses' in r['path'] for r in ledger))
  self.assertEqual([r['after'] for r in ledger if r['key']=='Dead King.additionalAttackDamage'],[50])
 def test_no_unapproved_rage_gate(self):
  data=json.loads((ROOT/'addons/ao-campaign/src/main/resources/data/neoforge/loot_modifiers/global_loot_modifiers.json').read_text())
  self.assertEqual(data['entries'],[])
 def test_native_cataclysm_only_intended_fields(self):
  current=tomllib.loads((ROOT/'release_030/overrides/config/cataclysm-common.toml').read_text())
  self.assertEqual(current['mobs']['kobolediator']['combat_config']['attack_multiplier'],5)
  self.assertEqual(current['mobs']['ignis']['combat_config']['attack_multiplier'],10)
  self.assertEqual(current['mobs']['netherite_ministrosity']['combat_config']['health_multiplier'],1)
  self.assertEqual(current['mobs']['scylla']['spear_damage'],14)
 def test_dd_budget_and_holds(self):
  d=json.loads((ROOT/'release_030/overrides/config/dungeon_difficulty/difficulty_v2.json').read_text())
  expected={2:[1,.4,3],3:[1.5,.6,5],4:[2,.8,8],5:[2.5,1,11],6:[3,2,15]}
  for t in d['difficulty_types']:
   n=int(t['name'].split('_')[-1])
   if n>=2:self.assertEqual([a['value'] for a in t['entities'][0]['attributes']],expected[n])
  zones=[z for w in d['dimensions'] for z in w['zones']]
  self.assertEqual(len(zones),23)
  self.assertFalse(any(z['zone_matches']['structure'] in {'cataclysm:frosted_prison','cataclysm:sunken_city','dungeons_arise:mechanical_nest'} for z in zones))
if __name__=='__main__':unittest.main()
