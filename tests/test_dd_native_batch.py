import unittest
from tools.compile_dd_native_batch import eligibility


class NativeDdBatch(unittest.TestCase):
    def setUp(self):
        self.plan={'structure_id':'test:dungeon','decision':'CHANGE','selected_structure_tier':'4'}
        self.evidence={'registered':True,'normal_preset_biome_overlap':{
            'minecraft:overworld':['minecraft:plains'],'minecraft:the_nether':[],'minecraft:the_end':[]}}

    def test_approved_registered_overworld_candidate(self):
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'NATIVE_REGISTRY_AND_OVERWORLD_BIOME_ELIGIBLE')

    def test_missing_id_or_source_only_name_is_held(self):
        self.assertEqual(eligibility(self.plan,None,set()),'HOLD_ID_NOT_REGISTERED')
        self.evidence['registered']=False
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'HOLD_ID_NOT_REGISTERED')

    def test_other_dimension_or_ambiguous_biomes_are_held(self):
        self.evidence['normal_preset_biome_overlap']['minecraft:the_end']=['minecraft:plains']
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'HOLD_AMBIGUOUS_NORMAL_DIMENSION')
        self.evidence['normal_preset_biome_overlap']['minecraft:overworld']=[]
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'HOLD_NO_NORMAL_OVERWORLD_BIOME_MATCH')

    def test_unapproved_category_default_and_tier_zero_are_not_promoted(self):
        self.plan['decision']='CATEGORY_DEFAULT'
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'HOLD_OWNER_TIER_NOT_APPROVED')
        self.plan.update(decision='KEEP',selected_structure_tier='0')
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'HOLD_OWNER_TIER_NOT_APPROVED')

    def test_protected_site_and_nest_exception(self):
        self.assertEqual(eligibility(self.plan,self.evidence,{'test:dungeon'}),'EXCLUDED_OWNER_EXCEPTION')
        self.plan['structure_id']='dungeons_arise:mechanical_nest'
        self.assertEqual(eligibility(self.plan,self.evidence,set()),'EXCLUDED_OWNER_EXCEPTION')
