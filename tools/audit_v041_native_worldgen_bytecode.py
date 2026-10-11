#!/usr/bin/env python3
"""Inspect EXACT installed native 1.21.1 beta bytecode before mixin speculation."""
import hashlib, json, pathlib, re, subprocess, urllib.request, zipfile
DATA={
 "tanshugetrees":("https://mediafilez.forgecdn.net/files/8026/658/TansHugeTrees-1.8.0-NeoForge-1.21.1-BETA.jar",
                  "tannyjung.tanshugetrees_core.game.GameUtils$Mob"),
 "hominid":("https://cdn.modrinth.com/data/4whAQxB5/versions/C6C67bp7/hominid-1.3.4.jar",
            "com.alganaut.hominid.registry.event.HominidClientEvents"),
 "dungeoncrawl":("https://cdn.modrinth.com/data/q0rRg4lH/versions/D7lKpb69/DungeonCrawl-NeoForge-1.21-2.3.17.jar",
            "xiroc.dungeoncrawl.dungeon.block.Spawner")
}
def main():
    out={}
    for name,(url,cls) in DATA.items():
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"AmbientOdyssey-Bytecode-Audit/1.0"})
            with urllib.request.urlopen(req,timeout=70) as f:raw=f.read(90000000)
            path=pathlib.Path("build/native-jars")/(name+".jar");path.parent.mkdir(exist_ok=True,parents=True);path.write_bytes(raw)
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
                assert cls.replace(".","/")+".class" in z.namelist(),cls
            p=subprocess.run(["javap","-classpath",str(path),"-c","-p",cls],capture_output=True,text=True,timeout=40)
            assert p.returncode==0,p.stderr[:300]
            lines=p.stdout.splitlines()
            selected=[]
            for i,line in enumerate(lines):
                if any(needle in line for needle in ("summonWorldGen(","summon(","onEntityJoinWorld(","void place(","addFreshEntity","getBlockEntity","setBlock(")):
                    selected.append({"lineno":i+1,"context":lines[max(0,i-5):min(len(lines),i+26)]})
            out[name]={"url":url,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
                       "class":cls,"method_excerpt":selected[:32]}
            print("AUDIT",name,"BYTES",len(raw),"SHA",out[name]["sha256"],flush=True)
            for item in selected[:18]:print("METHOD",item["lineno"],"\n".join(item["context"])[:2000],flush=True)
        except Exception as e:
            out[name]={"error":type(e).__name__+":"+str(e)[:350]}
            print("AUDIT_ERROR",name,out[name]["error"],flush=True)
    dest=pathlib.Path("build/v041-native-thread-bytecode.json")
    dest.write_text(json.dumps(out,indent=2)+"\n")
    assert "sha256" in out["hominid"] and "sha256" in out["tanshugetrees"]
if __name__=="__main__":main()
