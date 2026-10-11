"""Synthetic validation of v0.4.1 performance measurements."""
import unittest
from tools.perf_v041_trials import report

def measurement(scenario="idle",variant="baseline",trial=1,**fields):
    r=dict(status="MEASURED",scenario=scenario,variant=variant,trial=str(trial),
           build_sha256="abc123",seed="seed1",route_id="north-path",
           dimension="minecraft:overworld",terrain_state="existing",
           players="1",shaders="false",render_distance="12",
           simulation_distance="6",ram_mib="10240",
           avg_fps="50",fps_1pct_low="25",avg_mspt="8",p95_mspt="12",
           tps="20",chunks_generated="")
    r.update(fields)
    return r

class TestTrialQuality(unittest.TestCase):
    def test_three_identical_trials_are_eligible(self):
        rows=[measurement(trial=i,avg_fps=str(48+i)) for i in (1,2,3)]
        r=report(rows)
        g=r["groups"][0]
        self.assertTrue(g["eligible_for_comparison"])
        self.assertEqual(g["medians"]["avg_fps"],50)
        self.assertEqual(g["measured_trials"],3)
    def test_two_are_provisional(self):
        r=report([measurement(trial=1),measurement(trial=2)])
        self.assertFalse(r["groups"][0]["eligible_for_comparison"])
    def test_profile_settings_must_match(self):
        rows=[measurement(trial=1),measurement(trial=2),
              measurement(trial=3,simulation_distance="8")]
        g=report(rows)["groups"][0]
        self.assertFalse(g["eligible_for_comparison"])
        self.assertTrue(any("NONCOMPARABLE" in s for s in g["quality_notes"]))
    def test_missing_performance_metric_not_success(self):
        r=report([measurement(avg_fps="",fps_1pct_low="",avg_mspt="",p95_mspt="",tps="",chunks_generated="")])
        self.assertEqual(r["groups"],[])
        self.assertTrue(r["invalid_rows"])
    def test_planned_not_presented_as_measured(self):
        r=report([{"scenario":"new_chunks","variant":"baseline","status":"PLANNED"}])
        self.assertEqual(r["measured_rows"],0)
        self.assertEqual(r["unmeasured_template_rows"],1)

if __name__=="__main__":
    unittest.main()
