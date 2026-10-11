"""Synthetic guards: native Trek/Create rarity must preserve game content."""
import io
import json
from zipfile import ZipFile
import unittest
from tools.generate_v041_trek_create_rarity import render, TREK_OVERWORLD, CREATE_RATIO

def native_zip(entries):
    out=io.BytesIO()
    with ZipFile(out,"w") as z:
        for path,spacing,separation,size in entries:
            structures=[{"structure":"trek:overworld/test_"+str(i),"weight":1} for i in range(size)]
            z.writestr(path,json.dumps({
                "structures":structures,
                "placement":{"type":"minecraft:random_spread","spacing":spacing,
                             "separation":separation,"salt":123456789,
                             "frequency":1,"frequency_reduction_method":"default"}
            }))
    return out.getvalue()

def changed(orig,updated):
    a=orig["placement"];b=updated["placement"]
    assert orig["structures"]==updated["structures"]
    assert {k:v for k,v in a.items() if k!="spacing"}=={k:v for k,v in b.items() if k!="spacing"}

class TestNativeSelectiveRarity(unittest.TestCase):
    def test_trek_only_targeted_overworld_sets(self):
        root="data/trek/worldgen/structure_set/"
        entries=[
            (root+"overworld/common.json",24,12,13),
            (root+"overworld/medium.json",30,12,76),
            (root+"overworld/rare.json",48,24,16),
            (root+"overworld/very_rare.json",96,48,3),
            (root+"nether/common.json",24,12,13),
            (root+"monster_room/lower.json",1,0,4),
        ]
        native=native_zip(entries)
        n,outputs,audit=render("trek-structure-expansion",native)
        self.assertEqual((n,len(outputs),len(audit)),(6,3,3))
        for p,new in outputs.items():
            self.assertIn(p.stem,TREK_OVERWORLD)
            self.assertEqual(json.loads(new)["placement"]["spacing"],TREK_OVERWORLD[p.stem][1])

    def test_create_preserves_farms_and_original_salts(self):
        root="data/create_structures_arise/worldgen/structure_set/"
        native=native_zip([
            (root+"windmill.json",90,10,1),
            (root+"honey_pit.json",130,10,1),
            (root+"chocolate_pit.json",130,10,1),
            (root+"createhouse.json",120,70,1),
        ])
        n,out,report=render("test6-create-structures-arise",native)
        self.assertEqual((n,len(out)),(4,1))
        blob=next(iter(out.values()))
        self.assertEqual(json.loads(blob)["placement"]["spacing"],156)
        self.assertEqual(json.loads(blob)["placement"]["salt"],123456789)
        self.assertEqual(json.loads(blob)["placement"]["separation"],70)

    def test_create_easy_windmill_remains_unchanged(self):
        root="data/create_easy_structures/worldgen/structure_set/"
        n,out,report=render("test6-create-easy-structures",native_zip([
            (root+"windmill.json",60,15,1),
            (root+"factory_1.json",60,25,1),
        ]))
        self.assertEqual((n,len(out)),(2,1))
        self.assertEqual(json.loads(next(iter(out.values())))["placement"]["spacing"],78)

if __name__=="__main__":unittest.main()
