#!/usr/bin/env python3
"""Audit authoritative Luki's Woodland Mansions 1.21.1 mod resources.
Uses official upstream Modrinth v1.0+mod; no assets are redistributed.
"""
import io, json, zipfile
from urllib.request import urlopen, Request
from hashlib import sha256
from pathlib import Path
URL="https://cdn.modrinth.com/data/RZN5D3zs/versions/1fEmTmPi/lukis-woodland-mansions-v1.0.jar"
def main():
    raw=urlopen(Request(URL,headers={"User-Agent":"AmbientOdyssey-Audit/1.0"}),timeout=45).read()
    print("ARCHIVE bytes",len(raw),"sha256",sha256(raw).hexdigest())
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        print("Archive count",len(names), "CRC",z.testzip())
        for p in names:
            if p.startswith("assets/") and ("/models/item/" in p or "/items/" in p or "/textures/item/" in p):
                print("ASSET",p)
                if p.endswith(".json") and ("key" in p.lower() or "trial" in p.lower()):
                    print("CONTENT",z.read(p).decode("utf-8")[:2200])
        for p in names:
            if p in ("pack.mcmeta","META-INF/neoforge.mods.toml","META-INF/mods.toml","fabric.mod.json"):
                print("META",p,z.read(p).decode("utf-8")[:1800])
        for p in names:
            if "key" in p.lower() and (p.endswith(".json") or p.endswith(".png")):
                print("KEY",p)
        assets=[p for p in names if p.startswith("assets/")]
        print("Total ASSETS",len(assets))
        assert assets, "No client assets found in original mod jar"
        (Path("build")/"lukis-key-asset-audit.json").parent.mkdir(parents=True,exist_ok=True)
        (Path("build")/"lukis-key-asset-audit.json").write_text(json.dumps({"project":"Luki's Woodland Mansions","version":"v1.0+mod","source":URL,"sha256":sha256(raw).hexdigest(),"assets":assets,"keys":[p for p in names if "key" in p.lower()],"metadata":[p for p in names if p in ("pack.mcmeta","META-INF/neoforge.mods.toml","META-INF/mods.toml","fabric.mod.json")]},indent=2))
if __name__=="__main__":
    main()
