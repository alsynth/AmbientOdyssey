"""Meaningful fail-closed reconciliation and delivered-config safety tests."""
import copy,csv,json,re,unittest
from pathlib import Path
from tools.structure_difficulty_v3 import ROOT,BUDGETS,config_for,reconcile,read_resource_json,nbt_string_links,reachable

def resource(data, digest='one'):
    return {'provider':'fixture.jar','sha256':digest,'path':'fixture','data':data}

class ReconciliationTests(unittest.TestCase):
    def fixture(self):
        row={'id':'1','name':'Fixture','registry_id':'test:dungeon','dim':'Overworld','tier':'4','tier_source':'V2 approved provisional'}
        res={('worldgen/structure','test:dungeon'):[resource({'biomes':'minecraft:plains','start_pool':'test:start'})],('worldgen/structure_set','test:set'):[resource({'structures':[{'structure':'test:dungeon'}]})],('worldgen/template_pool','test:start'):[resource({'fallback':'minecraft:empty','elements':[{'element':{'location':'test:room'}}]})]}
        self.templates={'test:room':[{'provider':'fixture.jar','path':'data/test/structure/room.nbt','sha256':'one','pool_reference_leads':[]}]}
        self.nbt_rows=[{'jar':'fixture.jar','structure_nbt':'data/test/structure/room.nbt','mob_spawners':'1','trial_spawners':'0','vaults':'0','equipped_mob_or_spawner_indicators':'0','spawner_entity_ids':'minecraft:zombie'}]
        return row,res

    def test_collisions_and_unknown_biomes_never_qualify(self):
        row,res=self.fixture()
        self.assertEqual(reconcile([row],res,self.templates,self.nbt_rows)[0]['implementation'],'attribute_pilot')
        res[('worldgen/structure','test:dungeon')].append(resource({'biomes':'minecraft:the_end'},'two'))
        self.assertEqual(reconcile([row],res,{},[])[0]['implementation'],'hold')
        _,res=self.fixture();res[('worldgen/structure','test:dungeon')][0]['data']['biomes']=['minecraft:plains','unknown:biome']
        self.assertIn('dimension_unresolved',reconcile([row],res,{},[])[0]['hold_reasons'])

    def test_new_proposals_and_boss_tiers_stay_held(self):
        row,res=self.fixture();row['tier_source']='New v3 proposal'
        self.assertEqual(reconcile([row],res,{},[])[0]['implementation'],'hold')
        row['tier_source']='Explicit user decision';row['tier']='7'
        self.assertEqual(reconcile([row],res,{},[])[0]['implementation'],'hold')

    def test_replacements_and_conflicting_tiers_stay_held(self):
        row,res=self.fixture()
        self.assertEqual(reconcile([row],res,{},[],{'test:dungeon':'disabled'})[0]['installed_status'],'inactive_native_replacement')
        other=copy.deepcopy(row);other.update(id='2',tier='5')
        self.assertTrue(all(r['implementation']=='hold' for r in reconcile([row,other],res,{},[])))

    def test_comment_parser_preserves_urls_and_quoted_slashes(self):
        self.assertEqual(read_resource_json(b'{/* hi */ "url":"https://host/path", // ok\n "value":2}'),{'url':'https://host/path','value':2})

    def test_unknown_catalogue_dimension_can_use_explicit_native_evidence(self):
        row,res=self.fixture();row['dim']='Unknown'
        r=reconcile([row],res,self.templates,self.nbt_rows)[0]
        self.assertEqual(r['implementation'],'attribute_pilot')
        self.assertEqual(r['implementation_dimension'],'minecraft:overworld')
        self.assertEqual(r['dim'],'Unknown')

    def test_no_encounter_evidence_never_emits_an_attribute_rule(self):
        row,res=self.fixture()
        r=reconcile([row],res,self.templates,[])[0]
        self.assertEqual(r['implementation'],'hold')
        self.assertIn('compatible_ordinary_encounter_unproven',r['hold_reasons'])

    def test_serialized_pool_links_and_cycles_are_finite(self):
        value=b'test:child';raw=b'\x08\x00\x04pool'+len(value).to_bytes(2,'big')+value
        self.assertEqual(nbt_string_links(raw,'pool'),['test:child'])
        row,res=self.fixture();res[('worldgen/structure','test:dungeon')][0]['data']['start_pool']='test:start'
        res[('worldgen/template_pool','test:start')]=[resource({'fallback':'minecraft:empty','elements':[{'element':{'location':'test:entrance'}}]})]
        res[('worldgen/template_pool','test:child')]=[resource({'fallback':'test:start','elements':[{'element':{'location':'test:room'}}]})]
        templates={'test:entrance':[{'sha256':'one','pool_reference_leads':['test:child']}],'test:room':[{'sha256':'two','pool_reference_leads':['test:start']}]}
        pools,nbts,unknown=reachable(res,templates,'test:dungeon')
        self.assertEqual(nbts,['test:entrance','test:room']);self.assertFalse(unknown)

class DeliveredConfigTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/'docs/balance/v3-evidence/RECONCILED_CATALOGUE.csv').open(encoding='utf-8') as f:
            self.rows=list(csv.DictReader(f))
        self.config=json.loads((ROOT/'experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json').read_text())

    def test_all_zones_are_unique_approved_and_supported(self):
        expected={(r['implementation_dimension'],r['registry_id'],int(r['tier'])) for r in self.rows if r['implementation']!='hold'}
        actual=[]
        for d in self.config['dimensions']:
            self.assertNotIn('difficulty',d);self.assertEqual(d['entities'],[])
            for z in d['zones']:
                self.assertIsNone(z['zone_matches']['biome']);self.assertEqual(z['difficulty']['level'],1)
                actual.append((d['world_matches']['dimension'],z['zone_matches']['structure'],int(z['difficulty']['name'].removeprefix('ao_tier_'))))
        self.assertEqual(set(actual),expected);self.assertEqual(len(actual),len(expected))
        self.assertFalse(any(x[1] in {'minecraft:monument','minecraft:fortress','fdbosses:geburah_arena','cataclysm:frosted_prison'} for x in actual))

    def test_no_boss_namespace_loot_party_population_or_xp_scaling(self):
        c=self.config
        self.assertFalse(c['per_player_difficulty']['enabled']);self.assertFalse(c['player_effects']['enabled'])
        self.assertEqual(c['loot_scaling']['armor'],[]);self.assertEqual(c['loot_scaling']['weapons'],[])
        self.assertFalse(c['loot_scaling']['smithing_upgrade']['enabled'])
        for t in c['difficulty_types']:
            tier=int(t['name'].removeprefix('ao_tier_'))
            self.assertFalse(t['allow_loot_scaling'])
            if tier<2:self.assertEqual(t['entities'],[]);continue
            e=t['entities'][0];p=re.compile(e['entity_matches']['type'][1:])
            for boss in ['minecraft:wither','minecraft:ender_dragon','cataclysm:maledictus','remnant_bosses:ossukage','irons_spellbooks:dead_king','minecraft:evoker','minecraft:creeper']:
                self.assertFalse(p.fullmatch(boss))
            self.assertTrue(p.fullmatch('minecraft:zombie'))
            self.assertTrue(all(v==0 for v in e['spawners'].values()));self.assertEqual(e['experience_multiplier'],0)
            self.assertEqual(tuple(a['value'] for a in e['attributes']),BUDGETS[tier])
            self.assertTrue(all(a['offset']==0 and a['randomness']==0 for a in e['attributes']))

    def test_input_rows_and_uncertainty_preserved(self):
        self.assertEqual(len(self.rows),427)
        self.assertTrue(all(r['runtime_generation']=='NOT_TESTED' for r in self.rows))
        self.assertTrue(all(r['implementation']=='hold' for r in self.rows if 'New v3 proposal' in r['tier_source']))

if __name__=='__main__':unittest.main()
