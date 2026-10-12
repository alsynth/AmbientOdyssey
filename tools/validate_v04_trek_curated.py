#!/usr/bin/env python3
"""Static checks for the experimental Trek-for-RS mod and DnT curation."""
import argparse
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/"release_030/release-lock.json"
PACK=ROOT/"release_030/overrides/config/paxi/datapacks/ao_dnt_trek_curation"
AUDIT=ROOT/"docs/audits/DNT_TREK_CURATION_NATIVE_AUDIT.json"
BASE="overrides/config/paxi/datapacks/ao_dnt_trek_curation/"
REMOVE={368293,1071336}
TREK=(1418999,8296269)
def validate(archive=None):
    lock=json.loads(LOCK.read_text())
    assert lock["version"]=="0.4.1-experimental-trek-structures"
    assert REMOVE <= set(lock["remove_projects"].values())
    assert lock["additions"]["trek-structure-expansion"]["projectId"]==TREK[0]
    assert lock["additions"]["trek-structure-expansion"]["id"]==TREK[1]
    assert lock["experimental_minecells"]["expected_manifest_refs"]==331
    native=json.loads(AUDIT.read_text())
    disabled=native["disabled"]
    assert len(disabled)==30 and native["catalogue_structure_count"]==96
    assert "remnant_graveyard" in disabled and "ruin_town" in disabled
    assert "remnant_taiga_castle" in native["retained"]
    assert not any(k.startswith(("nether_","end_","piglin_","skeleton_camp_")) for k in disabled)
    assert (PACK/"pack.mcmeta").exists()
    assert (PACK/"data/ambient_odyssey/tags/worldgen/biome/dnt_trek_disabled.json").exists()
    for slug in disabled:
        j=json.loads((PACK/f"data/nova_structures/worldgen/structure/{slug}.json").read_text())
        assert j["biomes"]=="#ambient_odyssey:dnt_trek_disabled"
    assert len(list((PACK/"data/nova_structures/worldgen/structure").glob("*.json")))==30
    assert not (ROOT/"release_030/overrides/config/paxi/datapacks/ao_worldgen_final_fixes/data/repurposed_structures").exists()
    paths=set(lock["remove_override_paths"])
    assert "overrides/config/repurposed_structures-neoforge/modded_loot.toml" in paths
    assert "overrides/config/cristellib/repurposed_structures/structure_toggle_config.json5" in paths
    if archive:
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            names=set(z.namelist())
            m=json.loads(z.read("manifest.json"))
            refs={x["projectID"]:x["fileID"] for x in m["files"]}
            # Accept the exact approved v0483 removal, while retaining historical archive checks.
            expected_refs = 329 if m.get("version") in {"0.4.8.3-ring-inventory-test", "0.4.8.4-r19-full-pack-test"} else 331
            if expected_refs == 329:
                assert {1023913, 1657433}.isdisjoint(refs)
            assert len(refs)==expected_refs and TREK[0] in refs and refs[TREK[0]]==TREK[1]
            assert not (REMOVE & set(refs))
            assert BASE+"pack.mcmeta" in names
            for slug in disabled:
                p=BASE+f"data/nova_structures/worldgen/structure/{slug}.json"
                assert p in names and json.loads(z.read(p))["biomes"]=="#ambient_odyssey:dnt_trek_disabled"
            assert all(not n.startswith("overrides/config/cristellib/repurposed_structures/") for n in names)
            assert all(not n.startswith("overrides/config/paxi/datapacks/ao_compatibility/data/repurposed_structures/") for n in names)
    print(json.dumps({"status":"PASS_STATIC_ONLY","trek_project_file":TREK,
      "removed_projects":sorted(REMOVE),"dnt_disabled":len(disabled),
      "dnt_kept":len(native["retained"]),"preserved_nether_end":True,
      "archive_checked":bool(archive),"full_game_runtime_tested":False},indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path)
    validate(p.parse_args().archive)
