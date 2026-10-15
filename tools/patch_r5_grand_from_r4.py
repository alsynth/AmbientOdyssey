#!/usr/bin/env python3
"""Safely prepare R5 test-addon JAR from EXACT R4 import, Grand JSON only.

Never modifies the original R4 ZIP, its published release, source files,
native loot tables or player worlds. Human source/category review must be
explicit; the output is experimental and requires Minecraft/Lootr tests.

--mode draft: create a DENIED-by-default five-context review form.
--mode patch: hash-gated resource-only addon copy for an R5 test import.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R4_SHA="31b037a710320c840bcede26003f46a7219fb1e14e14674d35efcf4e086e6c6d"
CAMPAIGN_SHA="802461a621d5d20b7aaaa50dacc69035af517a1a73b7bae39fd771234d2a39b7"
CAMPAIGN_PATH="overrides/mods/ao-campaign-0.3.2-experimental.jar"
POLICY_MEMBER="ao_loot_policy.json"
FORMAT="AO_R5_GRAND_FIVE_REVIEW_V1"

def sha(b):return hashlib.sha256(b).hexdigest()
def key(r):return (r["structure"],r["table"])
def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))

def draft(preview,preview_bytes):
    if preview.get("status")!="REVIEW_ONLY_NOT_A_COMPILED_RELEASE":
        raise ValueError("Preview must remain explicitly review-only")
    changes=preview.get("changed_pools",[])
    if len(changes)!=5 or len({r["table"] for r in changes})!=5:
        raise ValueError("Five context changes required")
    return {"format":FORMAT,"status":"DRAFT_NOT_APPROVED",
            "preview_sha256":sha(preview_bytes),
            "decisions":[{
                "table":r["table"],
                "native_source_sha256":r["native_table_sha256"],
                "proposed_pool_index":r["review_only_candidate_pool"],
                "installed_native_source_verified":False,
                "effective_paxi_source_verified":False,
                "native_entry_functions_and_category_reviewed":False,
                "approved_for_experimental_test_only":False,
                "reviewer_rationale":""
            } for r in changes]}

def verify_review(preview,preview_bytes,approved):
    if approved.get("format")!=FORMAT or approved.get("status")!="APPROVED_FOR_EXPERIMENTAL_TEST_ONLY":
        raise ValueError("Approval status missing; draft review must fail closed")
    if approved.get("preview_sha256")!=sha(preview_bytes):
        raise ValueError("Review references another or modified preview file")
    changes=preview["changed_pools"]
    reviews=approved.get("decisions")
    if not isinstance(reviews,list) or len(reviews)!=5 or len({r.get("table") for r in reviews})!=5:
        raise ValueError("Need exactly five separate native source review decisions")
    indexed={r["table"]:r for r in reviews}
    if set(indexed)!={c["table"] for c in changes}:
        raise ValueError("Reviewed table set differs from R4 review-only delta")
    for c in changes:
        r=indexed[c["table"]]
        if r.get("native_source_sha256")!=c["native_table_sha256"] or r.get("proposed_pool_index")!=c["review_only_candidate_pool"]:
            raise ValueError("Approval refers to another source hash or native pool")
        for field in ("installed_native_source_verified","effective_paxi_source_verified",
                      "native_entry_functions_and_category_reviewed",
                      "approved_for_experimental_test_only"):
            if r.get(field) is not True:
                raise ValueError("Unverified native source, Paxi winner or category: "+c["table"]+" / "+field)
        rationale=r.get("reviewer_rationale","")
        if not isinstance(rationale,str) or len(rationale.strip())<24:
            raise ValueError("Manual source/category rationale must be at least 24 chars")
    return True

def extract_r4(path):
    binary=Path(path).read_bytes()
    if sha(binary)!=R4_SHA:raise ValueError("Incorrect original R4 release ZIP SHA256")
    with zipfile.ZipFile(io.BytesIO(binary)) as z:
        names=z.namelist()
        if len(set(names))!=len(names) or z.testzip():
            raise ValueError("R4 import ZIP has duplicate members or bad CRC")
        manifest=json.loads(z.read("manifest.json"))
        if len(manifest["files"])!=337:
            raise ValueError("R4 original CurseForge reference count changed")
        jars=[n for n in names if n.startswith("overrides/mods/") and n.endswith(".jar")]
        if len(jars)!=10 or CAMPAIGN_PATH not in jars:
            raise ValueError("R4 original custom addon roster changed")
        addon=z.read(CAMPAIGN_PATH)
        if sha(addon)!=CAMPAIGN_SHA:
            raise ValueError("R4 original compiled campaign addon hash differs")
        return addon

def jar_entries(binary):
    with zipfile.ZipFile(io.BytesIO(binary)) as z:
        if z.testzip():raise ValueError("Corrupt R4 campaign JAR")
        all_info=[(i,z.read(i)) for i in z.infolist() if not i.is_dir()]
        if len({i.filename for i,b in all_info})!=len(all_info):
            raise ValueError("Duplicate campaign JAR resources")
        return all_info

def build_resource_patch(original,preview,preview_bytes,approval):
    verify_review(preview,preview_bytes,approval)
    infos=jar_entries(original)
    old={info.filename:data for info,data in infos}
    required={POLICY_MEMBER,"META-INF/neoforge.mods.toml",
              "dev/ambientodyssey/campaign/GrandTreasure.class",
              "dev/ambientodyssey/campaign/BossRewards.class"}
    if required-set(old):raise ValueError("R4 JAR missing known campaign entry")
    meta=old["META-INF/neoforge.mods.toml"].decode("utf-8")
    if 'modId="ao_campaign"' not in meta or 'version="0.3.2-experimental"' not in meta:
        raise ValueError("Expected original R4 campaign 0.3.2 identity")
    if any(i.filename.upper().startswith("META-INF/") and
           i.filename.upper().endswith((".SF",".RSA",".DSA",".EC")) for i,_ in infos):
        raise ValueError("Cannot alter a signed JAR's internal JSON")
    base=json.loads(old[POLICY_MEMBER])
    proposed=preview["policy"]
    if set(base)!=set(proposed):
        raise ValueError("Changed campaign policy root keys")
    if any(base[k]!=proposed[k] for k in base if k!="grand_treasure"):
        raise ValueError("Non-Grand boss/Regalia/unique/gem/reward policy changed")
    old_rows=base["grand_treasure"]
    new_rows=proposed["grand_treasure"]
    if len(old_rows)!=14 or len(new_rows)!=14 or [key(v) for v in old_rows]!=[key(v) for v in new_rows]:
        raise ValueError("R4 original 14 Grand chest contexts do not match proposed scope")
    changes=[]
    for before,after in zip(old_rows,new_rows):
        fields={f for f in set(before)|set(after) if before.get(f)!=after.get(f)}
        if fields not in (set(),{"pool_index"}):
            raise ValueError("Illegal field drift beyond original native pool index")
        if before["chance"]!=.05 or after["chance"]!=.05:
            raise ValueError("Owner five-percent bonus rule changed")
        if fields:changes.append((before["table"],before["pool_index"],after["pool_index"]))
    expected={(c["table"],c["old_pool"],c["review_only_candidate_pool"]) for c in preview["changed_pools"]}
    if len(changes)!=5 or set(changes)!=expected:
        raise ValueError("R4 addon policy does not match exactly five source-reviewed pool changes")
    target=(json.dumps(proposed,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,"w") as z:
        for info,data in infos:
            z.writestr(info,target if info.filename==POLICY_MEMBER else data)
    patched=buffer.getvalue()
    compare={i.filename:data for i,data in jar_entries(patched)}
    if set(old)!=set(compare) or compare[POLICY_MEMBER]!=target or any(
        compare[n]!=v for n,v in old.items() if n!=POLICY_MEMBER
    ):
        raise ValueError("Patched addon modified compiled classes or unrelated resources")
    return patched,{
        "status":"R5_GRAND_RESOURCE_ONLY_EXPERIMENTAL_JAR_NOT_RUNTIME_TESTED",
        "basis_release_sha256":R4_SHA,
        "basis_campaign_jar_sha256":CAMPAIGN_SHA,
        "patched_campaign_jar_sha256":sha(patched),
        "r4_old_policy_sha256":sha(old[POLICY_MEMBER]),
        "r5_staged_policy_sha256":sha(target),
        "only_modified_jar_member":POLICY_MEMBER,
        "other_members_byte_identical":len(old)-1,
        "changed_grand_pool_indices":changes,
        "mod_version_still":"0.3.2-experimental (resource-only test variant)",
        "minecraft_runtime_tested":False,
        "lootr_multiplayer_tested":False,
        "original_native_mod_loot_overridden":False,
        "warning":"TEST JAR only; keep R4 immutable and build a SEPARATE full R5 import from this exact replacement."
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode",choices=("draft","patch"),required=True)
    p.add_argument("--preview",type=Path,required=True)
    p.add_argument("--approval",type=Path)
    p.add_argument("--r4",type=Path)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--receipt",type=Path)
    args=p.parse_args()
    if args.out.exists() or args.receipt and args.receipt.exists():
        raise ValueError("Never overwrite another review, addon or receipt")
    if not args.out.resolve().is_relative_to((ROOT/"build").resolve()):
        raise ValueError("All output belongs under the repo build/ directory")
    preview_bytes=args.preview.read_bytes()
    preview=json.loads(preview_bytes)
    if args.mode=="draft":
        if args.r4 or args.approval or args.receipt:raise ValueError("Draft only needs review-only preview and --out")
        result=draft(preview,preview_bytes)
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print("R5 five-pool human review template created (ALL approvals FALSE)")
    else:
        if not args.r4 or not args.approval or not args.receipt:
            raise ValueError("Patch needs exact R4 ZIP, approved review and separate receipt")
        if args.receipt.resolve()==args.out.resolve() or not args.receipt.resolve().is_relative_to((ROOT/"build").resolve()):
            raise ValueError("Receipt must be separate and inside build/")
        if "overrides" in args.receipt.resolve().parts or args.out.name!=Path(CAMPAIGN_PATH).name:
            raise ValueError("Receipt cannot be under overrides; output must retain original campaign JAR filename")
        original=extract_r4(args.r4)
        patched,receipt=build_resource_patch(original,preview,preview_bytes,read_json(args.approval))
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_bytes(patched)
        args.receipt.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        print("New R5 TEST addon prepared from immutable original R4 bytes; not an import ZIP or runtime validation")

if __name__=="__main__":main()
