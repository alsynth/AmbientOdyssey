"""Tests for R4-based (not R2-based) Grand Treasure review-only delta."""
import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r5grand',ROOT/'tools/preview_r5_grand_from_r4.py')
tool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

class R4GrandFiveDiff(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=tool.BASE.read_bytes()
        cls.base=json.loads(cls.raw)
        cls.draft=json.loads(tool.PROPOSALS.read_text(encoding='utf-8'))

    def test_exact_r4_source_blob_is_pinned(self):
        git_blob=hashlib.sha1(b'blob '+str(len(self.raw)).encode()+b'\x00'+self.raw).hexdigest()
        self.assertEqual(self.draft['source_policy_git_blob_sha1'],git_blob)

    def test_five_proposed_indices_only(self):
        out,receipt=tool.transform(self.base,self.draft)
        self.assertEqual(len(out['grand_treasure']),14)
        self.assertEqual(len(receipt),5)
        self.assertTrue(all(not r['gameplay_accepted'] for r in receipt))
        a={tool.key(r):r for r in self.base['grand_treasure']}
        b={tool.key(r):r for r in out['grand_treasure']}
        self.assertEqual(set(a),set(b))
        changed={k for k in a if a[k]!=b[k]}
        self.assertEqual(changed,{tool.key(r) for r in self.draft['changes']})
        for k in changed:
            self.assertEqual({p for p in a[k] if a[k][p]!=b[k][p]},{'pool_index'})
        for name in self.base:
            if name!='grand_treasure':self.assertEqual(out[name],self.base[name])
        self.assertEqual(self.base['regalia'],out['regalia'])
        self.assertEqual(self.base['unique_weapons'],out['unique_weapons'])
        self.assertEqual(self.base['rare_affix_rates'],out['rare_affix_rates'])

    def test_keep_kayra_treasure_own_pool(self):
        out,_=tool.transform(self.base,self.draft)
        by={r['table'].split('/')[-1]:r for r in out['grand_treasure']}
        self.assertEqual(by['keep_kayra_library_treasure']['pool_index'],1)
        self.assertEqual(by['keep_kayra_treasure']['pool_index'],1)
        self.assertEqual(by['keep_kayra_garden_normal']['pool_index'],1)
        self.assertEqual(by['keep_kayra_library_normal']['pool_index'],2)

    def test_other_three_thematic_sources(self):
        out,_=tool.transform(self.base,self.draft)
        by={r['table'].split('/')[-1]:r for r in out['grand_treasure']}
        self.assertEqual(by['murky_chest_reward']['pool_index'],2)
        self.assertEqual(by['hidden_trough_treasure']['pool_index'],1)
        self.assertEqual(by['generic_magic_treasure']['pool_index'],1)

    def test_owner_probability_change_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['chance']=.15
        with self.assertRaisesRegex(ValueError,'preserved R4 field chance'):tool.transform(self.base,bad)

    def test_unreviewed_source_hash_change_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['source_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'source_sha256'):tool.transform(self.base,bad)

    def test_stale_r4_source_index_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['original_pool_index']+=1
        with self.assertRaisesRegex(ValueError,'stale/rebased'):tool.transform(self.base,bad)

    def test_noop_proposal_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['proposed_pool_index']=bad['changes'][0]['original_pool_index']
        with self.assertRaisesRegex(ValueError,'no-op'):tool.transform(self.base,bad)

    def test_unapproved_added_context_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['table']='minecraft:chests/unapproved'
        with self.assertRaisesRegex(ValueError,'unauthorized chest'):tool.transform(self.base,bad)

    def test_wrong_original_roster_rejected(self):
        bad=copy.deepcopy(self.base);bad['regalia']=[]
        with self.assertRaisesRegex(ValueError,'Unexpected R4 addon policy roster'):tool.transform(bad,self.draft)

    def test_autoapproved_status_rejected(self):
        bad=copy.deepcopy(self.draft);bad['changes'][0]['approval']='APPROVED_GAMEPLAY'
        with self.assertRaisesRegex(ValueError,'Cannot auto-promote'):tool.transform(self.base,bad)

    def test_release_sha_must_be_r4(self):
        bad=copy.deepcopy(self.draft);bad['source_release_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'pinned published R4'):tool.transform(self.base,bad)

if __name__=='__main__':unittest.main()
