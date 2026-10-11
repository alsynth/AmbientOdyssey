#!/usr/bin/env python3
"""AO structure-encounter NBT census.

Reads an installed CurseForge instance's physical mod JARs (not manifest metadata)
and enumerates NBT structure templates containing vanilla mob spawners, trial
spawners, vaults, and equipment-bearing embedded entities.

Requires: pip install nbtlib==2.0.4
Does NOT edit the JARs or generated structures. This is a content scan, not a
claim that every template is reachable/generated in the pack.
"""
import argparse
import csv
import gzip
import io
import json
import pathlib
import re
import zipfile
from collections import Counter

try:
    import nbtlib
except ImportError as exc:
    raise SystemExit("Install nbtlib 2.0.4: python -m pip install nbtlib==2.0.4") from exc


TEMPLATE_RE = re.compile(r"^data/[^/]+/(?:structures?|structure_template)/.*\.nbt$", re.I)
INTERESTING = {"minecraft:spawner", "minecraft:mob_spawner", "minecraft:trial_spawner", "minecraft:vault"}
EQUIP = {"ArmorItems", "HandItems", "equipment", "Equipment", "ArmorDropChances", "HandDropChances"}


def plain(val):
    """Convert nbtlib tags to plain Python types without requiring private API."""
    if isinstance(val, dict):
        return {str(k): plain(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [plain(v) for v in val]
    try:
        if hasattr(val, "value"):
            return plain(val.value)
    except (TypeError, ValueError):
        pass
    if isinstance(val, (bytes, int, float, str, bool)) or val is None:
        return val
    return str(val)


def load_nbt(data):
    raw = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
    return nbtlib.File.parse(io.BytesIO(raw))


def palette_names(root):
    palette = root.get("palette")
    if palette is None:
        palettes = root.get("palettes", [])
        palette = palettes[0] if palettes else []
    return [str(e.get("Name", "")) for e in palette]


def get_spawn_types(nbt):
    result = set()
    for candidate in [nbt.get("SpawnData", {})]:
        if isinstance(candidate, dict):
            entity = candidate.get("entity", candidate.get("Entity", {}))
            if isinstance(entity, dict) and entity.get("id"):
                result.add(str(entity["id"]))
    for candidate in nbt.get("SpawnPotentials", []):
        if not isinstance(candidate, dict):
            continue
        data = candidate.get("data", candidate.get("Data", candidate))
        if isinstance(data, dict):
            e = data.get("entity", data.get("Entity", data))
            if isinstance(e, dict) and e.get("id"):
                result.add(str(e["id"]))
    return result


def examine(jar_name, structure_path, tree):
    palette = palette_names(tree)
    counts = Counter()
    spawn_entities = set()
    geared = 0
    configurations = set()
    vault_ref = set()
    for block in tree.get("blocks", []):
        try:
            idx = int(block["state"])
        except (TypeError, ValueError, KeyError):
            continue
        name = palette[idx] if 0 <= idx < len(palette) else ""
        if name not in INTERESTING:
            continue
        counts[name] += 1
        nbt = block.get("nbt", {})
        if not isinstance(nbt, dict):
            continue
        if name in ("minecraft:spawner", "minecraft:mob_spawner"):
            spawn_entities.update(get_spawn_types(nbt))
            if any(field in json.dumps(plain(nbt), ensure_ascii=False) for field in EQUIP):
                geared += 1
        elif name == "minecraft:trial_spawner":
            for key in ("normal_config", "ominous_config", "spawn_potentials", "SpawnPotentials"):
                if key in nbt:
                    configurations.add(f"{key}={str(nbt[key])[:140]}")
        elif name == "minecraft:vault":
            for key in ("config", "loot_table", "key_item", "ominous"):
                if key in nbt:
                    vault_ref.add(f"{key}={str(nbt[key])[:140]}")
    for entry in tree.get("entities", []):
        entity = entry.get("nbt", {})
        if isinstance(entity, dict) and any(k in entity for k in EQUIP):
            geared += 1
    return {
        "jar": jar_name,
        "structure_nbt": structure_path,
        "mob_spawners": counts["minecraft:spawner"] + counts["minecraft:mob_spawner"],
        "trial_spawners": counts["minecraft:trial_spawner"],
        "vaults": counts["minecraft:vault"],
        "equipped_mob_or_spawner_indicators": geared,
        "spawner_entity_ids": " | ".join(sorted(spawn_entities)),
        "trial_config_samples": " | ".join(sorted(configurations))[:600],
        "vault_config_samples": " | ".join(sorted(vault_ref))[:600],
        "scan_confidence": "STATIC_TEMPLATE_ONLY; MAY_USE_CODE_SPAWN_OR_ALTERNATE_PALETTES",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mods-dir", type=pathlib.Path, required=True)
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("build/ao-encounter-template-nbt.csv"))
    p.add_argument("--include-empty", action="store_true")
    args = p.parse_args()
    if not args.mods_dir.is_dir():
        p.error(f"no mod directory: {args.mods_dir}")
    jars = sorted(args.mods_dir.glob("*.jar"))
    output = []
    failures = []
    scanned = 0
    for jar in jars:
        try:
            with zipfile.ZipFile(jar) as archive:
                for name in archive.namelist():
                    if not TEMPLATE_RE.match(name):
                        continue
                    try:
                        tree = load_nbt(archive.read(name))
                        result = examine(jar.name, name, tree)
                        scanned += 1
                        if args.include_empty or any(result[k] for k in ("mob_spawners", "trial_spawners", "vaults", "equipped_mob_or_spawner_indicators")):
                            output.append(result)
                    except Exception as err:
                        failures.append({"jar": jar.name, "structure_nbt": name, "error": str(err)[:250]})
        except (zipfile.BadZipFile, OSError) as err:
            failures.append({"jar": jar.name, "error": str(err)[:250]})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["jar", "structure_nbt", "mob_spawners", "trial_spawners", "vaults",
              "equipped_mob_or_spawner_indicators", "spawner_entity_ids",
              "trial_config_samples", "vault_config_samples", "scan_confidence"]
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        writer.writerows(output)
    errors_file = args.out.with_suffix(".errors.json")
    errors_file.write_text(json.dumps(failures, indent=2), encoding="utf-8")
    print(f"Jars seen: {len(jars)}; templates decoded: {scanned}; templates with indicators: {len(output)}; errors: {len(failures)}")
    print(f"Results: {args.out}; errors: {errors_file}")
    print("Note: resources, dimensions, entity-code spawns and structure pool selection NOT fully proven by this NBT scan.")


if __name__ == "__main__":
    main()
