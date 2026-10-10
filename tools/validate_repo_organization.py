#!/usr/bin/env python3
"""Static-only repository organization safety test; no game/server interaction.

Requires Git checkout for blob identity checks. Does not mutate repository data.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT/"docs/archive/ARCHIVE_MANIFEST.json"
ACTIVE={
    "v04-experimental.yml",
    "v04h-installed-jar-audit.yml",
    "v04h-q1-ftb-manual.yml",
    "v04h-q1-questbook.yml",
    "v04h-questlog.yml",
    "v04h-test-session-kit.yml",
    "repository-organization.yml",
}
CHECK_MARKDOWN=[
    "README.md", "AGENTS.md", "docs/README.md",
    "docs/maintainers/REPO_MAP.md", "docs/maintainers/ARCHIVE_POLICY.md",
    "docs/status/CURRENT_STATE.md", "docs/status/AGENT_WORKFLOW.md",
    "docs/questing/QUESTLOG_ADMIN_GUIDE.md", "docs/questing/README.md",
    "docs/archive/README.md",
]
def ls_git_blobs():
    result=subprocess.run(
        ["git","ls-files","-s"], cwd=ROOT,
        text=True, capture_output=True, check=True
    )
    found={}
    for line in result.stdout.splitlines():
        head, filename = line.split("\t",1)
        mode,sha,stage=head.split()
        assert stage=="0"
        found[filename]=(mode,sha)
    return found

def validate():
    paths=ls_git_blobs()
    manifest=json.loads(ARCH.read_text(encoding="utf-8"))
    assert len(manifest["archived_workflows"])==30
    assert len(manifest["archived_bootstrap"])==2
    assert len(manifest["archived_docs"])==5
    assert len(paths)>1350
    for collection in ("archived_workflows","archived_bootstrap","archived_docs"):
        for row in manifest[collection]:
            assert row["to"] in paths, row
            assert paths[row["to"]][1]==row["sha"], ("Archive blob changed!",row)
            if collection!="archived_docs":
                assert row["from"] not in paths, ("Legacy root/workflow not moved!",row)
            else:
                assert row["from"] in paths and paths[row["from"]][1]!=row["sha"]
    active={Path(p).name for p in paths if p.startswith(".github/workflows/")}
    assert active==ACTIVE,(active,ACTIVE)
    archive={Path(p).name for p in paths if p.startswith(".github/workflows-archive/2026-10-10/")}
    assert len(archive)==30 and not (active&archive)

    assert "release_030/release-lock.json" in paths
    assert "Ambient-Odyssey-v0.2.10.zip" in paths
    assert "release_030/overrides/config/tanshugetrees/custom_packs/#main.zip" in paths
    assert "build_release_030.py" in paths
    assert "release_030/overrides/config/ftbquests/quests/chapters/when_dungeons_arise.snbt" in paths
    q=[p for p in paths if p.startswith("release_030/overrides/config/questlog/quests/") and p.endswith(".json")]
    q_chapters=[p for p in paths if p.startswith("release_030/overrides/config/questlog/chapters/") and p.endswith(".json")]
    assert len(q)==50 and len(q_chapters)==13
    ftb=[p for p in paths if p.startswith("release_030/overrides/config/ftbquests/quests/chapters/")]
    assert {"field_manual.snbt","tips_and_tricks.snbt","keybind_cheatsheet.snbt","when_dungeons_arise.snbt"}<= {Path(p).name for p in ftb}
    lock=json.loads((ROOT/"release_030/release-lock.json").read_text(encoding="utf-8"))
    assert lock["version"]=="0.4.0-experimental-minecells-fg-questlog-q1"
    assert lock["experimental_minecells"]["expected_manifest_refs"]==331
    broken=[]
    for doc in CHECK_MARKDOWN:
        contents=(ROOT/doc).read_text(encoding="utf-8")
        # Ignore URLs, anchors and inline title markup; check only actual authored relative link paths.
        for target in re.findall(r"\]\(([^)]+)\)",contents):
            target=target.split("#",1)[0]
            if not target or target.startswith(("https://","http://","mailto:")):
                continue
            target=target.split(" ",1)[0]
            if not (ROOT/doc).parent.joinpath(target).exists():
                broken.append([doc,target])
    assert not broken,("Broken new navigation links",broken)
    print(json.dumps({
        "status":"PASS_REPOSITORY_STRUCTURE_STATIC_ONLY",
        "active_workflows":len(active), "archived_workflows":len(archive),
        "old_bootstrap_moved":2,"historical_handoffs_copied":5,
        "questlog_quests":len(q),"questlog_chapters":len(q_chapters),
        "curseforge_refs":331,"broken_new_links":0,
        "content_or_gameplay_tested":False
    },indent=2))
    return True

if __name__=="__main__":
    validate()
