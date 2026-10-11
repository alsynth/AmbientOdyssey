#!/usr/bin/env python3
"""Validate AO's merged Luki + Dungeons & Taverns key model overrides.

The upstream mod JARs remain installed via CurseForge; this Paxi resource repair
contains *only* JSON model routing and does not redistribute either mod's ARR art.
"""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile
R=Path(__file__).resolve().parent.parent
DIR="release_030/overrides/config/paxi/resourcepacks/ao_lukis_dnt_key_compat/assets/minecraft/models/item/"
NORMAL={711:"shrine_key",712:"creeper_key",713:"citadel_key",715:"monument_key",717:"donjon_key",718:"outstation_key",719:"nether_key",721:"end_castle_key",722:"toxic_key",6161:"mansion_key",6767:"stronghold_key"}
OMINOUS={711:"ominous_shrine_key",712:"ominous_toxic_key",714:"citadel_boss_key",716:"monument_boss_key",720:"end_ship_key",723:"toxic_boss_key",6162:"ravager_key",6768:"dragon_key"}
def check(read):
    for filename,expected in [("trial_key.json",NORMAL),("ominous_trial_key.json",OMINOUS)]:
        d=json.loads(read(filename))
        assert d["parent"]=="minecraft:item/generated"
        assert d["textures"]["layer0"]=="minecraft:item/"+filename[:-5]
        assert "display" in d and len(d["display"])==4
        entries=d["overrides"]
        ids=[e["predicate"]["custom_model_data"] for e in entries]
        assert ids==sorted(expected), (filename,ids)
        assert len(ids)==len(expected) and len(ids)==len(set(ids))
        found={e["predicate"]["custom_model_data"]:e["model"] for e in entries}
        assert found=={k:"minecraft:item/keys/"+v for k,v in expected.items()},(filename,found)
    print("PASS: 19 total custom-key model routes, preserving all 4 Luki keys and 15 Dungeons & Taverns keys")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",type=Path)
    ap.add_argument("--control",action="store_true",help="Check the resulting 328-project working Mine Cells profile")
    a=ap.parse_args()
    check(lambda n:(R/(DIR+n)).read_text(encoding="utf-8"))
    if a.archive:
        with ZipFile(a.archive) as z:
            assert z.testzip() is None
            check(lambda n:z.read("overrides/"+DIR.removeprefix("release_030/overrides/")+n).decode("utf-8"))
            m=json.loads(z.read("manifest.json"))
            refs={x["projectID"]:x["fileID"] for x in m["files"]}
            assert refs[1385782]==7227735, "Luki's Woodland Mansions version changed"
            assert refs[853794]==5768823, "Dungeons & Taverns version changed"
            if a.control:
                assert len(refs)==328,len(refs)
                assert all(x not in refs for x in (832882,1430156,1581408))
            print(f"PASS CurseForge import: {len(refs)} refs, exact author mod versions, Paxi model merge present")
    print("STATIC ONLY: still requires client-side visuals check with Mansion/Ravager and DnT keys")
if __name__=="__main__":
    main()
