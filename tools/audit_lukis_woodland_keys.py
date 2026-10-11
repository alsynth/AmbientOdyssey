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

    dt_url="https://cdn.modrinth.com/data/tpehi7ww/versions/BYUUUeZA/dungeons-and-taverns-v4.4.4.jar"
    dt_raw=urlopen(Request(dt_url,headers={"User-Agent":"AmbientOdyssey-Audit/1.0"}),timeout=90).read()
    print("DNT bytes",len(dt_raw),"sha256",sha256(dt_raw).hexdigest())
    with zipfile.ZipFile(io.BytesIO(dt_raw)) as dt:
        dt_names=dt.namelist()
        print("DNT archive entries",len(dt_names), "CRC",dt.testzip())
        for p in dt_names:
            if p in ("assets/minecraft/models/item/trial_key.json","assets/minecraft/models/item/ominous_trial_key.json") or (p.startswith("assets/minecraft/models/item/") and ("key" in p or "trial" in p)):
                print("DNT MODEL",p)
                if p.endswith(".json"):
                    print("DNT CONTENT",dt.read(p).decode("utf-8")[:14000])
        print("DNT KEY paths",[p for p in dt_names if "key" in p.lower() and p.startswith("assets/")][:120])

if __name__=="__main__":
    main()
