#!/usr/bin/env python3
"""Produce exact-JAR, minimally patched 1.21.1 terminal jigsaw NBT overrides.

Only changes intentionally dangling outgoing connector fields `pool` and
`target` from `minecraft:` to `minecraft:empty`. Keeps all structure
geometry, processors, connector names and remaining block/entity tags.
Source JARs are SHA256-locked to Test8.6's actual installed-binary audit.
Generated NBT overrides are private-pack material, not checked-in mod assets.
"""
import copy
import gzip
import hashlib
import io
from pathlib import Path, PurePosixPath
import urllib.parse
import urllib.request
import zipfile

try:
    import nbtlib
except ImportError as err:
    raise SystemExit("Test8.7 native NBT compiler needs `pip install nbtlib==2.0.4`") from err

ROOT = Path(__file__).resolve().parent
PREFIX = "overrides/config/paxi/datapacks/ao_worldgen_final_fixes/"
EXPECTED = (
    {
        "filename": "adventuredungeons-neoforge-1.21-1.3.1.jar",
        "fileid": 5808396,
        "sha256": "a5ae9687c37ab5a383d1b3a5a6f46a0b8bdeb3aca643745323c3b78c6ca6c347",
        "count": 264,
        "namespace": "adventuredungeons"
    },
    {
        "filename": "block_factorys_bosses-2.1.2-neo-1.21.1.jar",
        "fileid": 8123167,
        "sha256": "9e230bd509e7aeb3af4c08125db0340734c0179d83483649a16e45c0ea085e8c",
        "count": 1,
        "namespace": "block_factorys_bosses"
    },
    {
        "filename": "irons_spellbooks-1.21.1-3.16.3.jar",
        "fileid": 8680204,
        "sha256": "13d644474ddba4f8478b4ce68294687fd509c994b3f344a224142b102dbe6f73",
        "count": 6,
        "namespace": "irons_spellbooks"
    }
)
CACHE = ROOT / "build" / "cache" / "native-jigsaw-087"

def native_jar(entry):
    cache = CACHE / entry["filename"]
    if cache.exists():
        content=cache.read_bytes()
        if hashlib.sha256(content).hexdigest()==entry["sha256"]:
            return content
        cache.unlink()
    fileid=entry["fileid"]
    url=(f"https://mediafilez.forgecdn.net/files/{fileid//1000}/{fileid%1000:03d}/"
         +urllib.parse.quote(entry["filename"]))
    request=urllib.request.Request(url,headers={"User-Agent":"AmbientOdyssey-SourceLockedWorldgenRepair/1.0"})
    with urllib.request.urlopen(request,timeout=90) as f:
        content=f.read(65_000_000)
    actual=hashlib.sha256(content).hexdigest()
    if actual!=entry["sha256"]:
        raise ValueError(f"Native JAR mismatch for {entry['filename']}: expected SHA {entry['sha256']}, actual {actual}")
    CACHE.mkdir(parents=True,exist_ok=True)
    cache.write_bytes(content)
    return content

def fix_jigsaws(entries=None):
    """Return exactly 271 pack override path -> GZIP NBT bytes and count report."""
    outputs={}
    counts={}
    for entry in (entries or EXPECTED):
        fixed=0
        native=native_jar(entry)
        with zipfile.ZipFile(io.BytesIO(native)) as jar:
            assert jar.testzip() is None
            for filename in jar.namelist():
                if not (filename.startswith("data/") and "/structure/" in filename and filename.endswith(".nbt")):
                    continue
                raw=jar.read(filename)
                try:
                    original=gzip.decompress(raw)
                except OSError:
                    continue
                if b"minecraft:" not in original or b"jigsaw" not in original or b"pool" not in original:
                    continue
                # NBT 10-byte length prefix filters most native valid jigsaws.
                if b"\x00\x0aminecraft:" not in original:
                    continue
                document=nbtlib.File.parse(io.BytesIO(original))
                original_document=copy.deepcopy(document)
                palette=document["palette"]
                changed=[]
                for block in document["blocks"]:
                    state=palette[int(block["state"])]
                    if str(state["Name"])!="minecraft:jigsaw":
                        continue
                    tile=block.get("nbt",{})
                    pool=str(tile.get("pool",""))
                    if pool!="minecraft:":
                        continue
                    # Every scanned bad connector is an intentional *terminal*
                    # in the original: both outgoing pool and target are empty.
                    if str(tile.get("target",""))!="minecraft:":
                        raise ValueError("Nonterminal invalid jigsaw unexpectedly found: "+filename)
                    name=str(tile.get("name",""))
                    if name in ("","minecraft:"):
                        raise ValueError("Connector has invalid attach name: "+filename)
                    tile["pool"]=nbtlib.String("minecraft:empty")
                    tile["target"]=nbtlib.String("minecraft:empty")
                    changed.append(tuple(int(v) for v in block["pos"]))
                    fixed+=1
                if not changed:
                    continue
                assert len(changed)==1, "Unexpected many affected blocks in "+filename
                # Semantic guarantee: no geometry, blocks, names, loot or entities changed.
                original_document["blocks"]=copy.deepcopy(document["blocks"])
                for block in original_document["blocks"]:
                    state=palette[int(block["state"])]
                    if str(state["Name"])=="minecraft:jigsaw" and tuple(int(v) for v in block["pos"]) in changed:
                        tile=block["nbt"]
                        tile["pool"]=nbtlib.String("minecraft:")
                        tile["target"]=nbtlib.String("minecraft:")
                assert original_document==nbtlib.File.parse(io.BytesIO(original)), "Unexpected original decode corruption"
                with io.BytesIO() as stream:
                    document.write(stream)
                    encoded=gzip.compress(stream.getvalue(),compresslevel=9,mtime=0)
                reround=nbtlib.File.parse(io.BytesIO(gzip.decompress(encoded)))
                assert reround==document, "NBT roundtrip changed content: "+filename
                path=PREFIX+filename
                assert PurePosixPath(path).parts[0]=="overrides"
                assert path not in outputs
                outputs[path]=encoded
        counts[entry["filename"]]=fixed
        if fixed!=entry["count"]:
            raise AssertionError(f"Native malformed connector count for {entry['filename']}: expected {entry['count']}, found {fixed}")
    assert len(outputs)==271, "Unexpected number of packed NBT overrides"
    print("Verified exact native malformed terminal-pool NBT overrides:",counts)
    return outputs,counts

if __name__=="__main__":
    files,report=fix_jigsaws()
    print("Generated",len(files),"NBT templates and verified semantic roundtrips. No files written into source tree.")
