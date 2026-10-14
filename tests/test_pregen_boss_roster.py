"""Source-only pregen roster audit: zero Minecraft-runtime claims."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import audit_pregen_boss_roster as audit


class PregenBossGateRegression(unittest.TestCase):
    def test_pinned_import_and_approved_removal_are_not_silently_marked_done(self):
        report=audit.audit()
        self.assertEqual(report["manifest_roster_entries"],338)
        self.assertEqual(report["manifest_mod_entries"],331)
        self.assertEqual(report["PR44_boss_entries"],38)
        self.assertTrue(report["remnant_bosses_2_7_0_pinned"])
        self.assertTrue(report["SkyArena_still_pinned"])
        self.assertIn("SkyArena-1.3.6-1.21.1.jar",report["SkyArena_pinned_file_names"])
        self.assertFalse(report["generation_frozen"])
        self.assertIn("NO_GO",report["signoff"])

    def test_bosses_rise_and_bomd_are_not_confused_with_block_factory_bosses(self):
        report=audit.audit()
        absent=set(report["absent_from_named_pinned_mod_roster"])
        self.assertIn("Bosses' Rise",absent)
        self.assertIn("Bosses of Mass Destruction",absent)
        rise=[e for e in report["bosses"] if e["source_mod"]=="Bosses' Rise"]
        bomd=[e for e in report["bosses"] if e["source_mod"]=="Bosses of Mass Destruction"]
        self.assertEqual(len(rise),5)
        self.assertEqual(len(bomd),4)
        self.assertTrue(all(e["source_mod_pin_status"]=="NO_MATCHING_PINNED_MOD_FILENAME"
                            for e in rise+bomd))
        self.assertFalse(audit.roster_provider(
            "Bosses' Rise",[{"name":"block_factorys_bosses-2.1.2-neo-1.21.1.jar"}]))
        self.assertFalse(audit.roster_provider(
            "Bosses of Mass Destruction",[{"name":"fdbosses-3.2-1.21.1.jar"}]))

    def test_named_bosses_have_source_only_not_runtime_confidence(self):
        r=audit.audit()
        self.assertTrue(all(not e["natural_generation_tested"] and
                            not e["boss_spawned_in_world_tested"]
                            for e in r["bosses"]))
        self.assertEqual(len([b for b in r["bosses"]
                              if b["tier_in_PR44_design"]=="T9"]),3)
        self.assertEqual(len([b for b in r["bosses"]
                              if b["source_mod"]=="Unselected"]),2)
        self.assertTrue(r["T9_third_End_boss_reserved_not_selected"])
        self.assertTrue(any("integrated" in x.lower() for x in r["hard_stop_decisions"]))
        self.assertIn("NO_GO",audit.markdown(r))

if __name__=="__main__":unittest.main()
