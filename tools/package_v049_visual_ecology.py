"""Build a reversible config kit; optionally apply only to the exact PR41 import."""
import argparse, hashlib, json, sys
from pathlib import Path
from zipfile import ZipFile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_v048_ui_fix import archive
ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "4dac3f2f2991fb4b92638b97b80d7c0aa4dbf90631aa721c25707937944de6d0"
FILES = ("particular-common.toml", "alexsmobs.toml")
def build(output, base=None):
    backup = ROOT / "docs/performance/v049-followup"
    if base:
        assert hashlib.sha256(base.read_bytes()).hexdigest() == BASE_SHA, "Requires exact PR41 import"
        with ZipFile(base) as z:
            assert z.testzip() is None
            original = {n:z.read(n) for n in z.namelist()}
        files = dict(original)
        pins = json.loads(files["manifest.json"])["files"]
        assert len(pins) == 328
        for name in FILES:
            path = "overrides/config/" + name
            assert original[path] == (backup/name).read_bytes(), "Unexpected config base: " + name
            files[path] = (ROOT/"release_030"/path).read_bytes()
            files["overrides/AO_TEST_NOTES/v049-rollback/"+name] = original[path]
        m=json.loads(files["manifest.json"])
        m["version"]="0.4.9-visual-ecology-test"
        m["name"]="Ambient Odyssey v0.4.9 - Visual Ecology TEST"
        files["manifest.json"]=(json.dumps(m,indent=2)+"\n").encode()
        allowed={"manifest.json"} | {"overrides/config/"+n for n in FILES}
        assert all(files[n] == b for n,b in original.items() if n not in allowed)
        assert json.loads(files["manifest.json"])["files"] == pins
    else:
        files={}
        for name in FILES:
            files["candidate/config/"+name]=(ROOT/"release_030/overrides/config"/name).read_bytes()
            files["rollback/config/"+name]=(backup/name).read_bytes()
    files["README.md"]=(ROOT/"docs/performance/V049_VISUAL_ECOLOGY_20261013.md").read_bytes()
    sha=archive(output, files)
    report={"sha256":sha,"kind":"experimental import" if base else "config kit (not a CurseForge import)","native_tested":False}
    output.with_suffix(".inputs.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--base",type=Path)
    a=p.parse_args();build(a.output,a.base)
