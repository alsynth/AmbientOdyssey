"""Source-only regressions for Ambient Odyssey history audit (no Minecraft)."""
import unittest
from tools.audit_v042_historical_fixes import report

class HistoryRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=report()
        cls.items={i["feature"]:i for i in cls.data["checks"]}

    def test_all_retain_source_gates(self):
        self.assertEqual(self.data["counts"]["gaps"],0,self.items)
        self.assertGreaterEqual(self.data["counts"]["present_source_only"],14)

    def test_regression_risks_not_treated_runtime_verified(self):
        self.assertEqual(self.data["evidence_level"],"SOURCE_ONLY_NOT_RUNTIME")
        for name in ("5–7-player dedicated server and chunkgen profiling",
                     "Questlog Q icon still mispositioned",
                     "Dungeon Crawl spawner block-entity lifecycle",
                     "504 air item messages not fully attributed",
                     "Q2 complex RPG and dimension quests"):
            self.assertEqual(self.items[name]["status"],"unresolved_or_runtime_untested")

    def test_amulet_slot_is_conservative(self):
        self.assertEqual(self.items["Curios amulet slot"]["status"],"present_source_only")
        self.assertEqual(self.items["Curios conservative common config"]["status"],"present_source_only")

    def test_other_selected_user_rules_survive(self):
        for name in ("30% sleep","quiet rain/water defaults","rare mutants",
                     "approved structure rarity","manual task uniqueness",
                     "WDA progression retained","Q1 Questlog count"):
            self.assertEqual(self.items[name]["status"],"present_source_only")

if __name__=="__main__":unittest.main()
