"""Source-parity and archive safety for the Ambient Odyssey offline Quest Atlas."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.export_quest_atlas import load_atlas

class QuestAtlasSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = load_atlas()
        cls.content = json.loads((ROOT / "site/quest-data.json").read_text(encoding="utf-8"))

    def test_export_is_derived_exactly_from_questlog(self):
        self.assertEqual(self.content, self.atlas)
        self.assertEqual(len(self.content["quests"]), 50)
        self.assertEqual(len(self.content["chapters"]), 13)

    def test_unique_quest_ids_and_known_chapters(self):
        quests = self.atlas["quests"]
        ids = {q["id"] for q in quests}
        self.assertEqual(len(ids), len(quests))
        chapters = {c["id"] for c in self.atlas["chapters"]}
        self.assertEqual({q["chapter"] for q in quests}, chapters)
        self.assertEqual(sum(c["quest_count"] for c in self.atlas["chapters"]), 50)

    def test_quest_prerequisites_reference_real_quests(self):
        ids = {q["id"] for q in self.atlas["quests"]}
        for q in self.atlas["quests"]:
            for prereq in q["prerequisites"]:
                if prereq["type"] == "questlog:quest_complete":
                    self.assertIn(prereq["quest"].removeprefix("questlog:"), ids)

    def test_no_save_data_or_external_scripts(self):
        for q in self.atlas["quests"]:
            self.assertNotIn("player_uuid", q)
            self.assertNotIn("completed", q)
        page = (ROOT / "site/quests.html").read_text(encoding="utf-8")
        self.assertIn('src="quest-data.js"', page)
        self.assertIn('src="assets/quest-atlas.js"', page)
        self.assertNotIn('src="http', page)
        self.assertNotIn("fetch(", (ROOT / "site/assets/quest-atlas.js").read_text(encoding="utf-8"))

    def test_roadmap_preserves_historical_phases(self):
        text = (ROOT / "site/index.html").read_text(encoding="utf-8")
        self.assertIn("Development Roadmap", text)
        self.assertIn("Quest Atlas", text)
        self.assertIn("ambient-odyssey-roadmap-v1", text)
        self.assertIn('href="quests.html"', text)

    def test_generated_js_matches_json(self):
        javascript = (ROOT / "site/quest-data.js").read_text(encoding="utf-8")
        self.assertTrue(javascript.startswith("window.AO_QUEST_DATA = "))
        self.assertTrue(javascript.endswith(";\n"))
        self.assertEqual(json.loads(javascript[len("window.AO_QUEST_DATA = "):-2]), self.content)

if __name__ == "__main__":
    unittest.main()
