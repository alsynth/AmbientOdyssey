"""Read-only D&T 1.21.1 native JAR / AO firewatch collection-tag audit.

Usage: python tools/audit_pr56_dnt_firewatch_source.py --jar pinned.jar --out audit.json
Fails closed unless SHA1 equals the precise PR50 import pin. NEVER modifies the jar
or any active Paxi files. Emits compact extracted data only, not binary assets.
"""
import argparse
import hashlib
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

EXPECTED_SHA1 = "249a5bdd0e8622b8a11f88758e6f5fd5fda036a3"
EXPECTED_MOD = "dungeons-and-taverns-v4.4.4 [NeoForge].jar"
PREFIX = "data/nova_structures/"
COLLECTIONS = ("birch_forests", "cherry_forests", "savannas")
TOWERS = ("birch", "cherry", "dark_oak", "forest", "jungle", "mangrove", "savanna", "swamp", "taiga")
ROSTER_PATH = "docs/audits/CURRENT_BIOME_ROSTER.json"
BIOLITH_PATH = "docs/audits/CURRENT_BIOLITH_PLACEMENT.json"
BRIDGE = "experiments/structure-biome-compatibility/firewatch-tag-bridge-draft"
PAXI = "release_030/overrides/config/paxi/datapacks"


def text_json(zf, name):
    try:
        with zf.open(name) as stream:
            return json.load(stream)
    except KeyError:
        return None


def selector_ids(obj):
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        return [v if isinstance(v, str) else v.get("id", "") for v in obj if isinstance(v, (str, dict))]
    return []


def sha1_file(path):
    dig = hashlib.sha1()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            dig.update(block)
    return dig.hexdigest()


def run(jar, root):
    digest = sha1_file(jar)
    if digest != EXPECTED_SHA1:
        raise RuntimeError(f"Wrong D&T JAR SHA1: {digest}; expected {EXPECTED_SHA1}. DO NOT ANALYZE")

    roster = json.loads((root / ROSTER_PATH).read_text(encoding="utf-8"))
    curated = {namespace + ":" + x for namespace, group in roster.items() for x in group}
    replacements = json.loads((root / BIOLITH_PATH).read_text(encoding="utf-8"))["replacements"]
    replaced_vanilla = {x["target"] for x in replacements}

    with zipfile.ZipFile(jar) as zf:
        names = set(zf.namelist())
        structure_files = sorted(n for n in names if n.startswith(PREFIX + "worldgen/structure/") and n.endswith(".json"))
        tag_files = sorted(n for n in names if n.startswith(PREFIX + "tags/worldgen/biome/") and n.endswith(".json"))
        structure_sources = {}
        selector_consumers = defaultdict(list)
        for src in structure_files:
            obj = text_json(zf, src)
            if not isinstance(obj, dict):
                continue
            key = "nova_structures:" + src.split("/worldgen/structure/", 1)[1][:-5]
            biomes = selector_ids(obj.get("biomes", []))
            structure_sources[key] = {"path": src, "type": obj.get("type"), "biomes": biomes}
            for biome in biomes:
                selector_consumers[biome].append(key)

        tag_data = {}
        for t in tag_files:
            obj = text_json(zf, t)
            if not isinstance(obj, dict):
                continue
            key = "nova_structures:" + t.split("/tags/worldgen/biome/", 1)[1][:-5]
            tag_data[key] = {"path": t, "replace": obj.get("replace", False),
                             "values": selector_ids(obj.get("values", []))}

        draft = {}
        for tag in COLLECTIONS:
            name = f"data/nova_structures/tags/worldgen/biome/collections/{tag}.json"
            proposed = json.loads((root / BRIDGE / name).read_text(encoding="utf-8"))["values"]
            key = "nova_structures:collections/" + tag
            consumers = sorted(selector_consumers.get("#" + key, []))
            source = tag_data.get(key)
            vals = source["values"] if source else []
            draft[tag] = {
                "native_tag_exists": source is not None,
                "native_file": source["path"] if source else None,
                "native_replace": source["replace"] if source else None,
                "native_values": vals,
                "native_curated_direct_overlap": sorted(curated.intersection(vals)),
                "candidate_additions": proposed,
                "candidate_are_curated": all(v in curated for v in proposed),
                "candidate_already_in_native": sorted(set(proposed).intersection(vals)),
                "direct_structure_consumers": consumers,
                "non_firewatch_consumers": [s for s in consumers if not s.startswith("nova_structures:firewatch_tower_")],
                "nested_other_tag_references": sorted(k for k, row in tag_data.items() if "#" + key in row["values"]),
            }

        towers = {}
        for suffix in TOWERS:
            key = "nova_structures:firewatch_tower_" + suffix
            row = structure_sources.get(key)
            towers[key] = {"registered_native_structure_json": row is not None,
                           "selector": row["biomes"] if row else [],
                           "direct_replaced_vanilla": sorted(replaced_vanilla.intersection(row["biomes"])) if row else []}
        forest_path = PREFIX + "worldgen/structure/firewatch_tower_forest.json"
        forest = text_json(zf, forest_path)
        candidate_originals = {
            suffix: text_json(zf, PREFIX + f"worldgen/structure/firewatch_tower_{suffix}.json")
            for suffix in ("birch", "cherry", "savanna", "forest")
        }
        land_ref = "#nova_structures:collections/land"
        land_direct_consumers = sorted(selector_consumers.get(land_ref, []))
        # A collection tag may be used indirectly by other biome tags, including land.
        for name in COLLECTIONS:
            key = "nova_structures:collections/" + name
            upward = [key]
            visited = set()
            while upward:
                key_now = upward.pop()
                if key_now in visited:
                    continue
                visited.add(key_now)
                for ancestor, row in tag_data.items():
                    if "#" + key_now in row["values"]:
                        upward.append(ancestor)
            draft[name]["transitive_tag_keys"] = sorted(visited)
            draft[name]["transitive_structure_consumers"] = sorted({
                sid for tagkey in visited for sid in selector_consumers.get("#" + tagkey, [])
            })

        paxi_overrides = []
        paxi_root = root / PAXI
        if paxi_root.exists():
            for p in paxi_root.rglob("firewatch_tower_*.json"):
                if "/worldgen/structure/" in p.as_posix():
                    paxi_overrides.append(p.relative_to(root).as_posix())

        report = {
            "source": "OFFICIAL_PR50_CURSEFORGE_PIN_SHA1_MATCH",
            "filename": EXPECTED_MOD, "curseforge_project_id": 853794,
            "curseforge_file_id": 5768823, "sha1": digest,
            "native_structure_json_count": len(structure_files),
            "native_biome_tag_count": len(tag_files),
            "native_firewatch_structures": towers,
            "candidate_tag_analysis": draft,
            "complete_structure_selector_consumers_for_candidate_tags": {
                "#" + key: sorted(vals) for key, vals in selector_consumers.items()
                if key in {"#nova_structures:collections/" + t for t in COLLECTIONS}
            },
            "forest_original_native_structure_json": forest,
            "four_original_native_structure_json": candidate_originals,
            "land_collection_direct_structure_consumers": land_direct_consumers,
            "forest_native_source_file": forest_path,
            "current_researched_repo_paxi_firewatch_overrides": sorted(paxi_overrides),
            "declared_biolith_replacement_targets": sorted(replaced_vanilla),
            "native_worldgen_tested": False,
            "profile_resource_priority_runtime_tested": False,
            "safe_to_deploy": False,
        }
        return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    output = run(args.jar, args.root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("Native JAR SHA1 verified:", output["sha1"])
    print("Original forest definition found:", output["forest_original_native_structure_json"] is not None)
    for tag, row in output["candidate_tag_analysis"].items():
        print(tag, "exists=", row["native_tag_exists"],
              "structures=", len(row["direct_structure_consumers"]),
              "other consumers=", len(row["non_firewatch_consumers"]),
              "native curated=", len(row["native_curated_direct_overlap"]))
        for consumer in row["non_firewatch_consumers"]:
            print("  other consumer:", consumer)
    print("REPORT:", args.out.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
