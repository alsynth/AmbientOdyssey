#!/usr/bin/env python3
"""Unit test focused on AO log aggregation without leaking user paths."""
import unittest
from tools.audit_v041_runtime_log import analyze

class RuntimeLogAudit(unittest.TestCase):
    def test_read_only_classification(self):
        s='''[time] [Worker/ERROR]: Tried to load invalid item: 'Item must not be minecraft:air'
[time] [Server thread/WARN]: Can't keep up! Is the server overloaded? Running 27486ms or 549 ticks behind
[time] [Worker/WARN]: A mod is trying to add an entity from offthread, this should be avoided. Printing trace:
 at TRANSFORMER/hominid@1.3.4/HominidClientEvents.onEntityJoinWorld
[time] [INFO]: Found mod file "ao-questlog-betterinventory-0.1.2.jar"
[time] [INFO]: Tried unknown magic C:/Users/very_private_name/
'''
        x=analyze(s)
        self.assertEqual(x["server_stalls_ms"]["worst"],27486)
        self.assertEqual(x["typed_events"]["invalid_air_item"],1)
        self.assertEqual(x["typed_events"]["offthread_entity_creation"],1)
        self.assertFalse(x["profile"]["streams_reflowing_file_present"])
        self.assertIn("HominidClientEvents.onEntityJoinWorld",x["offthread_stack_owners"])
        self.assertNotIn("very_private_name",repr(x))
if __name__=="__main__":unittest.main()
