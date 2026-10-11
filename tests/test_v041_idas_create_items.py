"""Synthetic structure NBT regression for IDAS 1.21.1 native item correction."""
import gzip
import io
import unittest
import nbtlib
from tools.repair_v041_idas_create_items import OLD, NEW, edit_template


def sample(ids):
    blocks = nbtlib.List[nbtlib.Compound]()
    for item in ids:
        blocks.append(nbtlib.Compound({
            "nbt": nbtlib.Compound({
                "Items": nbtlib.List[nbtlib.Compound]([
                    nbtlib.Compound({"id": nbtlib.String(item),
                                    "Count": nbtlib.Int(2), "Slot": nbtlib.Byte(3)})
                ])
            })
        }))
    doc = nbtlib.File({"blocks": blocks, "metadata": nbtlib.String("unchanged")})
    buffer = io.BytesIO()
    doc.write(buffer)
    return gzip.compress(buffer.getvalue(), mtime=0)


class NativeIdasCreateTests(unittest.TestCase):
    def test_only_exact_old_inventory_items(self):
        original = sample([OLD, "minecraft:diamond", OLD])
        out, paths = edit_template(original, 2)
        parsed = nbtlib.File.parse(io.BytesIO(gzip.decompress(out)))
        ids = [str(b["nbt"]["Items"][0]["id"]) for b in parsed["blocks"]]
        self.assertEqual(ids, [NEW, "minecraft:diamond", NEW])
        self.assertEqual(parsed["metadata"], "unchanged")
        self.assertEqual(len(paths), 2)

    def test_fail_closed_on_unexpected_count(self):
        with self.assertRaises(AssertionError):
            edit_template(sample([OLD]), 2)

    def test_no_mutation_of_unrelated_fields(self):
        data = sample(["minecraft:air", "minecraft:iron_ingot"])
        out, hits = edit_template(data, 0)
        self.assertEqual(hits, [])
        parsed = nbtlib.File.parse(io.BytesIO(gzip.decompress(out)))
        self.assertEqual(str(parsed["blocks"][0]["nbt"]["Items"][0]["id"]), "minecraft:air")


if __name__ == "__main__":
    unittest.main()
