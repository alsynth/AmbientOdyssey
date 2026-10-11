"""Regression coverage for conservative v0.4.1 native structure item provenance."""
import unittest
from audit_invalid_structure_items_089 import (
    BAD, CANDIDATES, is_structure_nbt_path, recursive_hits
)


class InvalidStructureItemAuditTests(unittest.TestCase):
    def test_current_log_registry_item_is_not_omitted(self):
        self.assertIn("biomesoplenty:rose_quartz_shard", BAD)
        self.assertEqual(CANDIDATES, {item.encode("utf-8") for item in BAD})

    def test_current_and_legacy_structure_paths(self):
        self.assertTrue(is_structure_nbt_path("data/mansions/structure/mansion/room.nbt"))
        self.assertTrue(is_structure_nbt_path("data/old_mod/structures/house.nbt"))
        self.assertFalse(is_structure_nbt_path("assets/minecraft/structure/model.nbt"))
        self.assertFalse(is_structure_nbt_path("data/mod/worldgen/template_pool/house.json"))
        self.assertFalse(is_structure_nbt_path("data/mod/loot_table/house.nbt"))

    def test_nested_inventory_preserves_source_path(self):
        tree = {
            "blocks": [
                {"nbt": {"Items": [
                    {"Slot": 0, "id": "minecraft:air", "Count": 1},
                    {"Slot": 1, "id": "biomesoplenty:rose_quartz_shard", "count": 1},
                    {"Slot": 2, "id": "minecraft:diamond", "Count": 1},
                ]}},
            ],
            "metadata": {"id": "minecraft:air"},  # not an inventory stack
        }
        hits = list(recursive_hits(tree))
        self.assertEqual(len(hits), 2)
        self.assertEqual({h["item"] for h in hits},
                         {"minecraft:air", "biomesoplenty:rose_quartz_shard"})
        self.assertTrue(all("/blocks/0/nbt/Items/" in h["path"] for h in hits))

    def test_direct_item_stacks_with_count(self):
        hits = list(recursive_hits({"id": "redeco:hammer", "Count": 1}))
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["item"], "redeco:hammer")


if __name__ == "__main__":
    unittest.main()
