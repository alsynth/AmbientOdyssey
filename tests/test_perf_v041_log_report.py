"""Offline, synthetic-only regression tests for AO 0.4.1 log metrics."""
import unittest
from tools.perf_v041_log_report import decimal,p95,summarize

def line(time,level,body):
    return f"[11Oct2026 {time}] [Server thread/{level}] [net.minecraft.server.MinecraftServer/]: {body}"

class TestPerformanceLogReport(unittest.TestCase):
    def test_server_lag_counts_are_not_mislabelled_mspt(self):
        sample="\n".join([
            line("03:31:00.000","WARN","Can't keep up! Is the server overloaded? Running 2150ms or 43 ticks behind"),
            line("03:32:00.000","WARN","Can't keep up! Is the server overloaded? Running 27486ms or 549 ticks behind"),
            line("03:33:00.000","INFO","All saved"),
        ])
        r=summarize(sample)
        self.assertEqual(r["lag_warning_events"]["count"],2)
        self.assertEqual(r["lag_warning_events"]["worst_ms"],27486)
        self.assertEqual(r["lag_warning_events"]["median_warning_ms"],14818)
        self.assertEqual(r["lag_warning_events"]["p95_warning_ms_nearest_rank"],27486)
        self.assertEqual(r["session_elapsed_seconds"],120)
        self.assertIn("NOT observed tick MSPT",r["limitations"][0])

    def test_locale_ftf_counters(self):
        s="".join([
          " FreeTerraForged Native World Gen Performance Report\n",
          " Total Chunks Generated   : 1840\n",
          " Total Thread Time Spent  : 222823 ms\n",
          " Thread Time Per Chunk    : 121,10 ms\n",
          " Real Chunks Per Second   : 5,13\n",
          " Parallel Efficiency      : 6,9%\n",
          " Wall Clock Time          : 358900 ms\n"
        ])
        r=summarize(s)["ftf_shutdown_tracker"]
        self.assertEqual(r["chunks_generated"],1840)
        self.assertEqual(r["parallel_efficiency_percent"],6.9)
        self.assertAlmostEqual(r["real_chunks_per_second"],5.13)
        self.assertAlmostEqual(r["thread_ms_per_chunk"],121.10)

    def test_absent_metrics_remain_null_not_zero(self):
        r=summarize("unrelated")
        self.assertEqual(r["lag_warning_events"]["count"],0)
        self.assertIsNone(r["lag_warning_events"]["worst_ms"])
        self.assertEqual(r["ftf_shutdown_tracker"],{})

    def test_no_raw_identity_from_source_lines(self):
        r=summarize("[11Oct2026 02:00:00.000] C:\\Users\\Somebody\\AppData\\foo 192.168.1.2 ")
        s=str(r)
        self.assertNotIn("Somebody",s)
        self.assertNotIn("192.168",s)

if __name__=="__main__":
    unittest.main()
