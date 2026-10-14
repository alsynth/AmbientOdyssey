"""PR56 read-only DD candidate coverage and source-evidence safety audit.

Reads three checked-in research snapshots and writes a fail-closed per-zone
status table; it does NOT simulate Minecraft, assert source-NBT absence means
no mobs, or authorize any DD deployment.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=ROOT/"experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json"
BAL=ROOT/"docs/balance"
TIER= BAL/"DD_FULL_FIRST_PASS_TIER_MAP_20261014.csv"
NBT = BAL/"DD_NATIVE_NBT_EVIDENCE_20261014.csv"
APPROVED = BAL/"DD_OWNER_PROTECTED_26_SPAWNER_STRUCTURES_20261014.csv"
SOURCE_MATCHER=BAL/"DD_POSTMAP_FIVE_SITE_ENTITY_MATCHER_20261014.csv"
NEW_PINNED_NBT=BAL/"DD_PINNED_NATIVE_TEMPLATE_SPAWNER_AUDIT_20261014.json"

def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as h:
        return list(csv.DictReader(h))

def read_id_map(path):
    rows=read_csv(path)
    d={}
    for row in rows:
        key=row["structure_id"]
        if key in d:raise AssertionError("Duplicate structure_id: "+key)
        d[key]=row
    return d

def audit():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    tier=read_id_map(TIER)
    source=read_id_map(NBT)
    owner=read_id_map(APPROVED)
    matched_evidence=read_csv(SOURCE_MATCHER)
    pinned_native=json.loads(NEW_PINNED_NBT.read_text(encoding="utf-8"))
    current_native_by_id={x["structure_id"]:x for x in pinned_native["sites"]}
    difficulties={x["name"]:x for x in cfg["difficulty_types"]}
    assert len(difficulties)==len(cfg["difficulty_types"])==7
    assert set(difficulties)=={f"ao_tier_{n}" for n in range(7)}
    for n in (0,1):
        assert difficulties[f"ao_tier_{n}"]["entities"]==[], "No T0/T1 DD attributes!"
    regexps=[]
    multipliers={}
    for n in range(2,7):
        candidate=difficulties[f"ao_tier_{n}"]
        assert len(candidate["entities"])==1
        entry=candidate["entities"][0]
        matcher=entry["entity_matches"]
        assert matcher["attitude"]=="HOSTILE"
        expression=matcher["type"]
        assert expression.startswith("~"),"Expect explicit DD regular expression"
        regexps.append(expression)
        assert not any(float(x)!=0 for x in entry["spawners"].values()),"Spawner scaling should remain disabled"
        multipliers[n]={x["attribute"]:{"operation":x["operation"],"value":x["value"]}
                        for x in entry["attributes"]}
    assert len(set(regexps))==1,"DD Tier2–6 must use same entity eligibility matcher"
    regex=re.compile(regexps[0][1:])
    mobs=regexps[0].split("(?:",1)[1].split(")",1)[0].split("|")
    assert len(mobs)==17 and all(regex.fullmatch("minecraft:"+v) for v in mobs)

    # Source-matcher data describes only 8 explicitly seen entity/source pairs,
    # often for structures NOT in the original 53 DD candidate zones.
    source_sites={}
    for record in matched_evidence:
        source_sites.setdefault(record["site"],[]).append(record)
        inferred="YES" if regex.fullmatch(record["entity_id"]) else "NO"
        assert inferred==record["regex_match"],"Source matcher differs from DD candidate"
        assert record["native_placement_tested"]=="NO"
        assert record["attitude_checked"]=="NO"

    zones=[]
    seen=set()
    for dimension in cfg["dimensions"]:
        dim=dimension["world_matches"]["dimension"]
        for zone in dimension["zones"]:
            structure=zone["zone_matches"]["structure"]
            pair=(dim,structure)
            if pair in seen:raise AssertionError("Duplicate DD zone: "+str(pair))
            seen.add(pair)
            tier_in_cfg=int(zone["difficulty"]["name"].removeprefix("ao_tier_"))
            mapped=tier.get(structure)
            if mapped is None:raise AssertionError("DD zone missing from tier catalogue: "+structure)
            expected=int(mapped["proposed_tier"])
            if expected!=tier_in_cfg:
                raise AssertionError(f"DD zone mismatch {structure}: {tier_in_cfg}!={expected}")
            if structure in owner:
                if expected!=0 or tier_in_cfg!=0:
                    raise AssertionError("Owner-approved Tier0 spawner structure has DD buffs: "+structure)
            evidence=source.get(structure)
            if evidence is None:
                association="NOT_IN_HISTORIC_NATIVE_NBT_LEDGER"
                count_normal=count_trial=0
                source_entities=[]
            else:
                association=evidence["nbt_assoc_status"]
                count_normal=int(evidence["static_mob_spawner_blocks"])
                count_trial=int(evidence["static_trial_spawner_blocks"])
                source_entities=[v.strip() for v in re.split(r"[;,| ]+",evidence["sample_entity_ids"]) if v.strip()]
            positive=(count_normal>0 or count_trial>0)
            nbt_coverage="POSITIVE_SOURCE_TEMPLATE_INDICATOR" if positive else (
                "NO_LINKED_TEMPLATE_EVIDENCE__NOT_PROOF_EMPTY")
            source_pairs=source_sites.get(structure,[])
            fresh=current_native_by_id.get(structure)
            zones.append({
                "dimension":dim,"structure_id":structure,
                "candidate_DD_tier":tier_in_cfg,"catalogue_tier":expected,
                "source_profile_status":mapped["PR50_installation_status"],
                "source_NBT_association":association,
                "source_spawner_count":count_normal,
                "source_trial_spawner_count":count_trial,
                "source_mob_id_examples":source_entities,
                "linked_NBT_coverage":nbt_coverage,
                "new_pinned_JAR_templates_inspected":fresh["native_templates_inspected"] if fresh else 0,
                "new_pinned_JAR_source_spawner_occurrences":fresh["native_source_spawner_block_occurrences"] if fresh else 0,
                "new_pinned_JAR_source_graph_complete":fresh["source_graph_complete"] if fresh else False,
                "new_pinned_JAR_source_entity_ids":fresh["source_entity_type_ids"] if fresh else [],
                "new_pinned_JAR_DD_type_matches":fresh["source_DD_entity_matcher_matches"] if fresh else [],
                "new_pinned_JAR_DD_type_misses":fresh["source_DD_entity_matcher_misses"] if fresh else [],
                "new_pinned_JAR_scan_error":fresh["unresolved_native_graph_errors"] if fresh else ["NOT_PART_OF_THIS_TARGETED_JAR_SCAN"],
                "matcher_source_pairs":len(source_pairs),
                "DD_regex_example_matches":[v for v in source_entities if regex.fullmatch(v)],
                "DD_regex_example_misses":[v for v in source_entities if not regex.fullmatch(v)],
                "runtime_entity_behavior_verified":False,
                "runtime_spawner_behavior_verified":False,
                "native_structure_placement_verified":False,
                "live_DD_deployment_authorized":False,
                "next_action":("No DD attributes by policy" if expected<2 else
                               "Inspect pinned native templates and accessible spawner/entity sources; test vanilla/mobded mob matcher, trial mechanics, elite double stacking before any rollout"),
            })
    if len(zones)!=53:raise AssertionError(f"Expected 53 candidate zones; got {len(zones)}")
    high=[z for z in zones if 2<=z["candidate_DD_tier"]<=6]
    if len(high)!=28:raise AssertionError(f"Expected 28 Tier2–6 zones; got {len(high)}")
    return {
        "scope":"CANDIDATE_DD_V3_RESEARCH_ONLY_NOT_GAMEPLAY_DEPLOYED",
        "profile":"experiments/structure-difficulty-v3/candidate/config/dungeon_difficulty/difficulty_v2.json",
        "total_candidate_zones":len(zones),
        "attribute_scaled_T2_T6_zones":len(high),
        "unbuffed_T0_T1_zones":len(zones)-len(high),
        "exact_catalogue_tier_mismatches":0,
        "owner_T0_protected_structures_in_scaled_zones":sum(1 for z in high if z["structure_id"] in owner),
        "candidate_vanilla_hostile_entity_types":sorted(mobs),
        "candidate_entity_type_count":len(mobs),
        "candidate_type_matcher":regexps[0],
        "spawner_mutations_in_candidate_attributes":False,
        "source_ledger_explicit_spawner_indicators_in_scaled_zones":sum(z["linked_NBT_coverage"]=="POSITIVE_SOURCE_TEMPLATE_INDICATOR" for z in high),
        "scaled_zones_without_positive_linked_NBT_indicators":sum(z["linked_NBT_coverage"]!="POSITIVE_SOURCE_TEMPLATE_INDICATOR" for z in high),
        "new_pinned_JAR_source_positive_scaled_zones":sum(z["new_pinned_JAR_source_spawner_occurrences"]>0 for z in high),
        "new_pinned_JAR_source_positive_indicators_total":sum(z["new_pinned_JAR_source_spawner_occurrences"] for z in high),
        "scaled_zones_without_NEW_positive_pinned_JAR_NBT_evidence":sum(z["new_pinned_JAR_source_spawner_occurrences"]==0 for z in high),
        "source_snapshot_note":"Old linked NBT indicator count is 0/28 but NEW targeted native JAR evidence is positive for 6/28; absence of evidence on other zones or partial graphs is not proof of no mobs.",
        "source_matcher_examples_total":len(matched_evidence),
        "source_matcher_examples_matched":sum(x["regex_match"]=="YES" for x in matched_evidence),
        "source_matcher_examples_unmatched":sum(x["regex_match"]=="NO" for x in matched_evidence),
        "source_matcher_explicit_sites_inside_scaled_candidate":sorted(
            set(source_sites)&{z["structure_id"] for z in high}),
        "DD_scaling_values_by_tier":multipliers,
        "zones":zones,"live_DD_eligible":False,
        "valid_static_inventory_not_natural_generation":True
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    obj=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("Zones:",obj["total_candidate_zones"],"T2–T6:",obj["attribute_scaled_T2_T6_zones"])
    print("Exact tier mismatches:",obj["exact_catalogue_tier_mismatches"])
    print("Historical linked spawner positive in T2–T6:",obj["source_ledger_explicit_spawner_indicators_in_scaled_zones"])
    print("NO POSITIVE SOURCE NBT IS NOT PROOF OF NO MOBS")
    print("NEW targeted pinned JAR positive DD zones:",obj["new_pinned_JAR_source_positive_scaled_zones"],"/",obj["attribute_scaled_T2_T6_zones"])
    print("Vanilla eligible mob types:",obj["candidate_entity_type_count"])
    print("Out-of-candidate example matches:",obj["source_matcher_examples_matched"],"of",obj["source_matcher_examples_total"])
    print("Report:",args.out)

if __name__=="__main__":
    main()
