"""Bounded source-NBT streaming tests for a huge Keep Kayra-style template.

The synthetic fixture puts blocks BEFORE palette to exercise the two-pass
reader; the second check verifies bounded decompression fails closed.
"""
import gzip
import io
import json
import struct
import unittest
import zipfile
from tools.pr56_stream_nbt import extract_selected
from tools.audit_pr56_native_template_spawners import extract_template

def string(s):
    b=s.encode("utf-8")
    return struct.pack(">H",len(b))+b

def tag(t,name,blob):
    return bytes([t])+string(name)+blob

def comp(*fields):
    return b"".join(fields)+b"\0"

def str_tag(name,value):
    return tag(8,name,string(value))

def int_tag(name,value):
    return tag(3,name,struct.pack(">i",value))

def compound_tag(name,*fields):
    return tag(10,name,comp(*fields))

def list_tag(name,kind,members):
    return tag(9,name,struct.pack(">Bi",kind,len(members))+b"".join(members))

def fixture():
    pool=str_tag("pool","dungeons_arise:keep_kayra/pieces")
    spawner_nbt=compound_tag("nbt",compound_tag("SpawnData",
        compound_tag("entity",str_tag("id","minecraft:skeleton"),
                     list_tag("Items",10,[comp(str_tag("id","minecraft:diamond_sword"))]))))
    palette=[
        comp(str_tag("Name","minecraft:spawner")),
        comp(str_tag("Name","minecraft:stone")),
        comp(str_tag("Name","minecraft:jigsaw")),
    ]
    blocks=[
        comp(int_tag("state",1),list_tag("pos",3,[struct.pack(">i",n) for n in (0,0,0)])),
        comp(int_tag("state",0),spawner_nbt),
        comp(int_tag("state",2),compound_tag("nbt",pool)),
    ]
    # Blocks before palette forces the first pass to scan past blocks
    # without storing them; the second pass retains only flagged states.
    root=bytes([10])+string("")+comp(
        list_tag("blocks",10,blocks),
        list_tag("palette",10,palette),
        list_tag("entities",10,[]))
    return gzip.compress(root)

class KeepKayraStreamRegression(unittest.TestCase):
    def test_two_pass_gzip_block_before_palette_and_filter_equipment(self):
        zip_mem=io.BytesIO()
        with zipfile.ZipFile(zip_mem,"w",zipfile.ZIP_STORED) as z:
            z.writestr("data/test/structure/huge.nbt",fixture())
        zip_mem.seek(0)
        with zipfile.ZipFile(zip_mem) as z:
            compact,metadata=extract_selected(z,"data/test/structure/huge.nbt")
        self.assertEqual(metadata["streaming_mode"],"TWO_PASS_LIMITED_NBT")
        self.assertEqual(metadata["palette_states"],3)
        self.assertEqual(metadata["interesting_block_records"],2)
        parsed=extract_template(compact)
        self.assertEqual(parsed["normal_spawners"],1)
        self.assertEqual(parsed["trial_spawners"],0)
        self.assertEqual(parsed["normal_spawn_entity_ids"],["minecraft:skeleton"])
        self.assertNotIn("minecraft:diamond_sword",parsed["normal_spawn_entity_ids"])
        self.assertEqual(parsed["jigsaw_child_pools"],["dungeons_arise:keep_kayra/pieces"])

    def test_uncompressed_byte_budget_and_reject_unknown_compression(self):
        zdata=io.BytesIO()
        with zipfile.ZipFile(zdata,"w") as z:
            z.writestr("source.nbt",fixture())
            z.writestr("invalid.nbt",b"not valid")
        zdata.seek(0)
        with zipfile.ZipFile(zdata) as z:
            with self.assertRaisesRegex(ValueError,"STREAM_LIMIT_EXCEEDED"):
                extract_selected(z,"source.nbt",max_bytes=25)
            with self.assertRaisesRegex(ValueError,"UNSUPPORTED_NBT_STREAM_COMPRESSION"):
                extract_selected(z,"invalid.nbt")

    def test_no_palettes_refuses_empty_mob_conclusion(self):
        body=bytes([10])+string("")+comp(list_tag("blocks",10,[]))
        zdata=io.BytesIO()
        with zipfile.ZipFile(zdata,"w") as z:z.writestr("no_palette.nbt",gzip.compress(body))
        zdata.seek(0)
        with zipfile.ZipFile(zdata) as z:
            with self.assertRaisesRegex(ValueError,"MISSING_NBT_PALETTE"):
                extract_selected(z,"no_palette.nbt")

if __name__=="__main__":
    unittest.main()
