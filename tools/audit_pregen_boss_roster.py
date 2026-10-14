#!/usr/bin/env python3
"""Static pre-generation boss/arena roster gate for Ambient Odyssey.

Combines the exact PR50-import pins inherited by the PR54 test profile with
the PR44 provisional boss roster and the historic v3 structure-ID mapping.

Scope is STRICTLY source-level, never proof a boss or arena naturally generates.
A report containing blockers is a successful audit, NOT a worldgen GO.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"docs/balance/pr45-acceptance-evidence/FULL_IMPORT_INPUTS.json"
BOSSES=ROOT/"docs/balance/V050_BOSS_ROSTER_PROVISIONAL.csv"
STRUCTURES=ROOT/"docs/balance/AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv"

# Strict filename selectors. A filename that merely contains "boss" must NOT
# count as Bosses' Rise or Bosses of Mass Destruction (Block Factory is separate).
NATIVE_PROVIDER_FILENAME_PATTERNS={
 "Mine Cells":[r"^minecells[-_.]"],
 "Twilight Forest":[r"^twilightforest[-_.]"],
 "Bosses of Mass Destruction":[r"bosses_of_mass_destruction",r"bossesofmassdestruction",r"bosses-of-mass-destruction",r"^bomd[-_.]"],
 "Iron's Spells":[r"^irons_spellbooks[-_.]"],
 "Cataclysm":[r"^L_Ender's Cataclysm "],
 "Eternal Starlight":[r"^eternalstarlight[-_.]"],
 "Aquamirae":[r"^aquamirae[-_.]"],
 "Ice and Fire":[r"^iceandfire[-_.]"],
 "Remnant Bosses":[r"^remnant_bosses[-_.]"],
 "F.D. Bosses":[r"^fdbosses[-_.]"],
 "Bosses' Rise":[r"bosses[_. -]?rise",r"bossesrise",r"risingbosses"],
 "Archaion":[r"^archaion[-_.]"],
}
SPECS={
 "REMOVAL_APPROVED_DONT_RETAIN_IN_FINAL_PACK":"SkyArena-1.3.6-1.21.1.jar",
 "REQUIRED_MOD_TIER8":"Bosses' Rise",
 "REVIEW_PROVISIONAL_TIER5":"Bosses of Mass Destruction",
}
BUILTIN_ISSUES={
 "Bosses' Rise":"No matching named JAR in pinned import; investigate whether an alternative filename, external archive, or planned new mod accounts for the approved five T8 boss encounters.",
 "Bosses of Mass Destruction":"No matching named JAR in pinned import; proposed T5 Lich/Void Blossom and optional Gauntlet/Obsidilith are not verified as installed. Approval to omit/change paths is NOT inferred.",
}
EARLY_GATE="NO_GO__PINNED_BOSS_ROSTER_OR_ARENA_VERIFICATION_INCOMPLETE"


def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as fh:
        return list(csv.DictReader(fh))


def roster_provider(name,mod_rows):
    if name=="Unselected":return []
    patterns=NATIVE_PROVIDER_FILENAME_PATTERNS.get(name)
    if not patterns:raise ValueError("Boss source mapping missing: "+name)
    return sorted({row["name"] for row in mod_rows
                   if any(re.search(p,row["name"],re.I) for p in patterns)})


def audit(manifest=MANIFEST,bosses=BOSSES,structures=STRUCTURES):
    m=json.loads(Path(manifest).read_text(encoding="utf-8"))
    physical=[x for x in m["roster"] if x.get("kind")=="mod"]
    if m["cf_download_pins"]!=len(m["roster"]) or m["cf_mod_pins"]!=len(physical):
        raise ValueError("PR50 source manifest count does not agree with roster")
    if len({(r.get("projectID"),r.get("fileID")) for r in m["roster"]}) != len(m["roster"]):
        raise ValueError("Duplicate CurseForge pin in imported roster")
    if any(not r.get("sha1") for r in physical):
        raise ValueError("Unpinned CF mod entry present")
    srows=read_csv(structures)
    historic_ids={x["registry_id"] for x in srows if x.get("registry_id")}
    b_rows=read_csv(bosses)
    if not b_rows:raise ValueError("No boss entries")
    entries=[]
    for row in b_rows:
        provider=row["source_mod"]
        matches=roster_provider(provider,physical)
        site=row["candidate_structure_id"].strip()
        if provider=="Unselected":
            installed="UNSELECTED_NOT_AN_INSTALL_DECISION"
        else:
            installed="MATCHING_PINNED_MOD_FILENAME" if matches else "NO_MATCHING_PINNED_MOD_FILENAME"
        if not site:arena="NO_SPECIFIC_ARENA_ID_IN_DESIGN"
        elif site in historic_ids:arena="HISTORIC_REGISTRY_ID_LISTED__NOT_RUNTIME"
        else:arena="NOT_IN_HISTORIC_STRUCTURE_CATALOGUE__REVIEW_ID"
        entries.append({
           "tier_in_PR44_design":row["tier"],
           "boss":row["encounter"],
           "source_mod":provider,
           "source_mod_pin_status":installed,
           "matching_CF_mod_names":matches,
           "candidate_structure_id":site or None,
           "structure_ID_source_status":arena,
           "owner_decision_status":row["decision_status"],
           "active_dimension_and_spawn_mechanism":"NOT_VERIFIED_BY_THIS_SOURCE_AUDIT",
           "natural_generation_tested":False,
           "boss_spawned_in_world_tested":False,
        })
    groups=Counter((x["source_mod"],x["source_mod_pin_status"]) for x in entries)
    missing=sorted(set(x["source_mod"] for x in entries if x["source_mod_pin_status"]=="NO_MATCHING_PINNED_MOD_FILENAME"))
    sky=sorted(r["name"] for r in physical if "SkyArena" in r["name"])
    remnant=roster_provider("Remnant Bosses",physical)
    if len(remnant)!=1:raise ValueError("Ambiguous Remnant Bosses pin")
    report={
      "report_type":"AO_PREGEN_BOSS_ARENA_ROSTER_EVIDENCE",
      "as_of":"2026-10-14",
      "source_manifest":"PR50 pinned 338-reference import inherited unchanged by experimental full-PR54 builder",
      "manifest_roster_entries":len(m["roster"]),
      "manifest_mod_entries":len(physical),
      "bundled_AO_custom_JAR_count_PR50":m["bundled_custom_mods"],
      "custom_mods_are_separate_from_CF_entries":True,
      "source_scope_only":True,
      "this_does_not_identify_boss_entity_IDs_or_runtime_arena_generation":True,
      "quest_work_deferred_for_this_gate":True,
      "T9_third_End_boss_reserved_not_selected":True,
      "remnant_bosses_2_7_0_pinned":all("2.7.0" in x for x in remnant),
      "PR44_boss_entries":len(entries),
      "unselected_boss_placeholders":sum(x["source_mod"]=="Unselected" for x in entries),
      "provider_groups":[{"mod":k[0],"status":k[1],"boss_rows":n} for k,n in sorted(groups.items())],
      "absent_from_named_pinned_mod_roster":missing,
      "missing_named_provider_issues":{k:BUILTIN_ISSUES.get(k,"Verify pinned provider identity") for k in missing},
      "SkyArena_still_pinned":bool(sky),
      "SkyArena_pinned_file_names":sky,
      "SkyArena_removal_approved_issue":58,
      "brutal_bosses_pregen_values_in_separate_draft_PR":59,
      "bosses":[*entries],
      "hard_stop_decisions":[
        "Resolve five Bosses' Rise T8 encounters: matching source mod not identified in the inherited pinned manifest",
        "Remove or explicitly reconcile Sky Arena/Ice Arena from effective next test import before permanent pregen",
        "Determine whether BOMD T5 boss/arena additions are still required, then pin and validate or explicitly defer",
        "Confirm true boss-ARENA placement and spawn mechanisms in fresh disposable world on exact full candidate before any Chunky 10–20k freeze",
        "Any newly selected third T9 End boss needing NEW terrain/arena/dimension content must be included before pregeneration; otherwise keep that slot explicitly reserved",
        "Integrate the distinct Brutal Bosses 70/30/HP4/damage3 patch before generating production chunks",
        "Preserve integrated Cataclysm and other collided arena providers until actual resource winner is verified",
      ],
      "generation_frozen":False,
      "signoff":EARLY_GATE,
    }
    return report


def markdown(r):
    lines=[
      "# AO permanent-world boss/arena pregeneration gate",
      "",
      "**Source-only NO-GO** until the owner and build pipeline resolve the roster and naturally generated arena checks. This does not certify whether a mod exists in a different local profile.",
      "",
      "## Confirmed pinned import facts",
      "",
      f"- **{r['manifest_roster_entries']}** CurseForge pins, of which **{r['manifest_mod_entries']}** are mods.",
      f"- **{r['PR44_boss_entries']}** boss/encounter design rows, all provisional for runtime generation.",
      f"- Remnant Bosses pinned at 2.7.0: **{r['remnant_bosses_2_7_0_pinned']}**.",
      f"- Sky Arena (approved to remove in issue #58) still pinned: **{r['SkyArena_still_pinned']}**.",
      f"- Provider families absent under identifiable pinned JAR names: **{', '.join(r['absent_from_named_pinned_mod_roster']) or 'none'}**.",
      "",
      "## Blockers and signoff conditions",
      "",
      *[f"- [ ] {item}" for item in r["hard_stop_decisions"]],
      "",
      "## Boss-by-boss native provider + structure-ID evidence",
      "",
      "| Tier | Encounter | Provider | Native roster | Site from PR44 | Historical site evidence |",
      "| --- | --- | --- | --- | --- | --- |",
    ]
    for b in r["bosses"]:
        lines.append("| "+ " | ".join([
            b["tier_in_PR44_design"],b["boss"],b["source_mod"],
            b["source_mod_pin_status"],b["candidate_structure_id"] or "unassigned",
            b["structure_ID_source_status"]])+" |")
    lines += [
      "",
      "**Important:** The 'historical registry ID' status is not proof an arena actually generates in the installed profile.",
      "No boss IDs, biome selectors, summon triggers, worldgen proof, effective Paxi/Integrated resource priority or post-pregen safety have been inferred.",
      "",
      "Boss stats and loot tuning are tracked separately from arena placement; changes to placed spawner-NBT and container table assignments must be settled before permanent pregen.",
      "",
    ]
    return "\n".join(lines)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-json",type=Path)
    p.add_argument("--output-md",type=Path)
    a=p.parse_args()
    r=audit()
    if a.output_json:
        a.output_json.parent.mkdir(parents=True,exist_ok=True)
        a.output_json.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if a.output_md:
        a.output_md.parent.mkdir(parents=True,exist_ok=True)
        a.output_md.write_text(markdown(r),encoding="utf-8")
    print("AO pregen boss/arena:",r["signoff"])
    print("source boss rows:",r["PR44_boss_entries"])
    print("pinned mod providers missing:",r["absent_from_named_pinned_mod_roster"])
    print("Sky Arena still pinned despite removal issue #58:",r["SkyArena_still_pinned"])
    print("Remnant Bosses 2.7.0:",r["remnant_bosses_2_7_0_pinned"])
    print("No live installation/config/spawn/arena modification performed.")


if __name__=="__main__":
    main()
