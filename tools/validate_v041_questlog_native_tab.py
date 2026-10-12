#!/usr/bin/env python3
"""Source and import archive checks for AO native-styled Questlog tab v0.1.5."""
import argparse, pathlib, zipfile, json, io
R=pathlib.Path(__file__).resolve().parent.parent
S=R/"addons/ao-questlog-betterinventory/src/main/java/dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge.java"
JAR="overrides/mods/ao-questlog-betterinventory-0.1.5.jar"
def source():
    s=S.read_text()
    for token in ['extends AbstractButton','betterinventory", "textures/gui/inventory.png"','TAB_U = 220','TAB_SELECTED_V = 21','TAB_WIDTH = 24','TAB_HEIGHT = 20','SETTINGS_X = 280','rightOfSettings = left + SETTINGS_X + SETTINGS_WIDTH + TAB_MARGIN','return new Anchor(rightOfSettings, top)','getGuiLeft()','getGuiTop()','getYSize()','private record Anchor','top - TAB_HEIGHT - TAB_MARGIN','this.setX(buttonX(this.parent))','this.setY(buttonY(this.parent))','Component.literal("Q")','graphics.drawString(minecraft.font, "!"','showsBadge()','mostRecentNotificationQuest']:
        assert token in s,token
    assert "Button.builder(" not in s
    assert "QuestlogScreen(Minecraft.getInstance().screen)" not in s
    print("PASS: Better Inventory source atlas used, native tab alignment and ! badge present.")
def archive(p):
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        assert JAR in z.namelist()
        m=json.loads(z.read("manifest.json"))
        refs={f["projectID"]:f["fileID"] for f in m["files"]}
        assert len(refs)==330
        assert refs[1202066]==8952784 and refs[1618019]==9099710
        # Other mod inclusion choices belong to the exact-baseline package validator.
        data=z.read(JAR)
        with zipfile.ZipFile(io.BytesIO(data)) as j:
            assert j.testzip() is None
            assert "dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge$QuestlogTab.class" in j.namelist()
            assert "dev/ambientodyssey/questlogbridge/QuestlogBetterInventoryBridge.class" in j.namelist()
    print("PASS: 330-ref CurseForge archive embeds compiled AO native tab and pins the tested Questlog/Better Inventory versions.")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=pathlib.Path)
    x=p.parse_args()
    source()
    if x.archive: archive(x.archive)
