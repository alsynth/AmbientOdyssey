#!/usr/bin/env python3
"""Read-only audit of installed NeoForge/Fabric mod metadata for Ambient Odyssey.

Does not install mods, remove client-only mods, start Minecraft, or claim runtime
compatibility. Python 3.11+ standard library only.

  python tools/audit_installed_jars_v04.py --profile "/path/to/instance"
  python tools/audit_installed_jars_v04.py --profile "/path/to/instance" --server "/path/to/server"
  python tools/audit_installed_jars_v04.py --profile "/path/to/instance" --report report.json

Reports JAR base filenames and declared mod IDs, never complete local paths,
log lines, usernames or addresses. Source metadata may omit bundled Jar-in-Jar
libraries, transformed Fabric dependencies, or dev-only mods; interpret gaps
as follow-up warnings rather than proofs of missing runtime dependencies.
"""
import argparse
import json
import sys
import tomllib
import zipfile
from collections import defaultdict
from pathlib import Path

MAX_METADATA = 1024 * 1024
BUILTIN = {"minecraft", "neoforge", "forge", "java", "fabricloader"}
# The Connector bridge can satisfy Fabric module IDs indirectly. Do not fake
# their presence: label these as bridge inspection requirements.
FABRIC_BRIDGE = {"fabric", "fabric-api", "fabric-api-base"}
REQUIRED_SERVER = {"questlog", "minecells"}
SOURCES = (
    ("META-INF/neoforge.mods.toml", "neoforge"),
    ("META-INF/mods.toml", "forge"),
    ("fabric.mod.json", "fabric"),
)

def get_dir(path):
    p = Path(path).expanduser()
    if (p / "mods").is_dir():
        return p / "mods"
    if (p / ".minecraft" / "mods").is_dir():
        return p / ".minecraft" / "mods"
    return p if p.is_dir() and p.name == "mods" else p / "mods"

def _metadata(jar):
    with zipfile.ZipFile(jar) as z:
        names = set(z.namelist())
        for filename, kind in SOURCES:
            if filename not in names:
                continue
            if z.getinfo(filename).file_size > MAX_METADATA:
                raise ValueError("oversized mod metadata")
            raw = z.read(filename)
            data = json.loads(raw) if kind == "fabric" else tomllib.loads(raw.decode("utf-8-sig"))
            if kind == "fabric":
                ident = data.get("id")
                if not isinstance(ident, str) or not ident:
                    raise ValueError("Fabric mod ID missing")
                provided = [x for x in data.get("provides", []) if isinstance(x, str)]
                depends = data.get("depends") if isinstance(data.get("depends"), dict) else {}
                dependencies = [{"id": str(k), "side": "BOTH", "kind": "fabric-required"}
                                for k in depends]
                return {"format": kind, "ids": [ident, *provided], "requires": dependencies}
            mods = data.get("mods", [])
            if not isinstance(mods, list):
                raise ValueError("invalid mods table")
            ids = [m["modId"] for m in mods if isinstance(m, dict) and
                   isinstance(m.get("modId"), str) and m["modId"].strip()]
            if not ids:
                raise ValueError("NeoForge mod IDs missing")
            dependencies = []
            deps = data.get("dependencies", {})
            if isinstance(deps, dict):
                for owner, values in deps.items():
                    if owner not in ids or not isinstance(values, list):
                        continue
                    for item in values:
                        if not isinstance(item, dict):
                            continue
                        required = (item.get("type", "").lower() == "required" or
                                    item.get("mandatory") is True)
                        if required and isinstance(item.get("modId"), str):
                            dependencies.append({"id": item["modId"],
                                "side": str(item.get("side", "BOTH")).upper(),
                                "kind": "native-required", "owner": owner})
            return {"format": kind, "ids": ids, "requires": dependencies}
    return {"format": "unknown", "ids": [], "requires": []}

def scan(mods):
    result = {"jar_count": 0, "metadata_read": 0, "unknown_metadata": [],
              "invalid_jars": [], "duplicate_mod_ids": [], "unresolved_dependencies": [],
              "ids": [], "filenames": [], "formats": {}}
    if not mods.is_dir():
        result["invalid_jars"].append("Mods directory does not exist")
        return result
    ids_to_files = defaultdict(set)
    entries = []
    for jar in sorted(mods.iterdir(), key=lambda p: p.name.lower()):
        if not jar.is_file() or jar.suffix.lower() != ".jar":
            continue
        result["jar_count"] += 1
        result["filenames"].append(jar.name)
        try:
            metadata = _metadata(jar)
        except (OSError, ValueError, UnicodeError, KeyError, TypeError,
                json.JSONDecodeError, tomllib.TOMLDecodeError, zipfile.BadZipFile):
            result["invalid_jars"].append(jar.name + ": JAR/metadata unreadable")
            continue
        kind = metadata["format"]
        result["formats"][kind] = result["formats"].get(kind, 0) + 1
        if kind == "unknown":
            result["unknown_metadata"].append(jar.name)
            continue
        result["metadata_read"] += 1
        for ident in metadata["ids"]:
            ids_to_files[ident].add(jar.name)
        entries.append((jar.name, metadata))
    for ident, filenames in sorted(ids_to_files.items()):
        if len(filenames) > 1:
            result["duplicate_mod_ids"].append({"mod_id": ident, "jars": sorted(filenames)})
    known = set(ids_to_files) | BUILTIN
    for jar_name, metadata in entries:
        for dep in metadata["requires"]:
            ident = dep["id"]
            if ident in known:
                continue
            result["unresolved_dependencies"].append({
                "declared_by": jar_name, "mod_id": ident,
                "side": dep["side"], "kind": dep["kind"],
                "bridge_candidate": ident in FABRIC_BRIDGE or ident.startswith("fabric-"),
            })
    result["ids"] = sorted(ids_to_files)
    return result

def evaluate(client, server=None):
    issues = []
    warnings = []
    if client["invalid_jars"]:
        warnings.append("Some client mod JARs or metadata could not be inspected")
    if client["duplicate_mod_ids"]:
        issues.append("Two or more client JAR files expose the same top-level mod ID")
    if client["unknown_metadata"]:
        warnings.append("Some client JARs contain no recognized top-level mod metadata")
    if client["unresolved_dependencies"]:
        warnings.append("Declared client dependencies not found at top level; embedded/bridge handling must be checked")
    if not client["ids"]:
        issues.append("No client mod IDs could be read")
    facts = {"client": client}
    if server is not None:
        facts["server"] = server
        if server["invalid_jars"] or server["unknown_metadata"]:
            warnings.append("Server-side metadata coverage is incomplete")
        if server["duplicate_mod_ids"]:
            issues.append("Two or more server JAR files expose the same top-level mod ID")
        server_ids = set(server["ids"])
        missing = sorted(REQUIRED_SERVER - server_ids)
        if missing:
            issues.append("Required gameplay mod IDs absent from the server scan: " + ", ".join(missing))
        if server["unresolved_dependencies"]:
            warnings.append("Some dedicated-server required dependencies are unresolved at top level")
        facts["comparison"] = {
            "client_only_mod_ids": sorted(set(client["ids"]) - server_ids),
            "server_only_mod_ids": sorted(server_ids - set(client["ids"])),
            "required_server_mod_ids_missing": missing,
        }
        warnings.append("Client-only mod IDs are comparison data, NOT authoritative sidedness classification")
    warnings.append("No bytecode/mixin execution, jar-in-jar dependency resolution, client rendering or server launch was tested")
    return {"status": "BLOCKED" if issues else "STATIC_REVIEW",
            "runtime_tested": False, "issues": issues, "warnings": warnings, **facts}

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profile", type=Path, required=True, help="Installed client profile or mods folder")
    p.add_argument("--server", type=Path, help="Optional dedicated server directory or mods folder")
    p.add_argument("--report", type=Path, help="Optional new JSON report, never overwrite existing file")
    args = p.parse_args(argv)
    client = scan(get_dir(args.profile))
    server = scan(get_dir(args.server)) if args.server else None
    result = evaluate(client, server)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(payload, end="")
    if args.report:
        if args.report.exists():
            p.error("Refusing to overwrite report")
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(payload, encoding="utf-8")
    return 2 if result["status"] == "BLOCKED" else 0

if __name__ == "__main__":
    sys.exit(main())
