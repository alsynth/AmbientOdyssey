#!/usr/bin/env python3
"""Fetch or inspect the pinned private AO R2 CurseForge import on an AUTHENTICATED PC.

Downloads via an installed GitHub CLI ('gh auth login') without copying any token
into this script, source control, logs, or third-party agent prompts.

Usage:
  python tools/prepare_r2_local_inputs.py --out-dir build/r2-inputs
  python tools/prepare_r2_local_inputs.py --local "C:\AO-Inputs\Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip" --out-dir build/r2-inputs

This is an INPUT PREPARATION / validation tool, not an R3 packager or gameplay test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = "alsynth/AmbientOdyssey"
RELEASE_ID = 413478281
ASSET_ID = 642899990
FILENAME = "Ambient-Odyssey-MASTER-INTEGRATION-R2-PRIVATE-20261015.zip"
EXPECTED_SHA256 = "db8269ff8c31650240f50b04b53bf9e1acdfca2e9b510e3495186b05978dd617"
EXPECTED_SIZE = 154_492_540
EXPECTED_CF_REFERENCES = 337
EXPECTED_CUSTOM_JARS = 10


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for data in iter(lambda: src.read(2 * 1024 * 1024), b""):
            digest.update(data)
    return digest.hexdigest()


def obtain_asset(dest: Path, local: Path | None) -> str:
    if dest.exists():
        if sha256(dest) == EXPECTED_SHA256:
            return "already-present-pinned-asset"
        raise ValueError(f"{dest} already exists but has the WRONG SHA256; not overwriting it")

    if local is not None:
        if not local.is_file():
            raise FileNotFoundError(local)
        if sha256(local) != EXPECTED_SHA256:
            raise ValueError("Supplied local R2 ZIP does not match the approved R2 SHA256")
        shutil.copy2(local, dest)
        return "copied-local-pinned-asset"

    if shutil.which("gh") is None:
        raise RuntimeError("Install GitHub CLI, run 'gh auth login', or use --local with the R2 release ZIP")

    # gh CLI uses your own authenticated login. The API endpoint redirects to
    # the release asset; stdout must be captured as BYTES, never via PowerShell >.
    # A GitHub API JSON error, empty file or HTML will fail the exact SHA check.
    with tempfile.NamedTemporaryFile(dir=dest.parent, prefix=".r2-download-", delete=False) as raw:
        temp_path = Path(raw.name)
        cmd = [
            "gh", "api", "--hostname", "github.com",
            "-H", "Accept: application/octet-stream",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            f"repos/{REPO}/releases/assets/{ASSET_ID}",
        ]
        proc = subprocess.run(cmd, stdout=raw, stderr=subprocess.PIPE, check=False)

    try:
        if proc.returncode:
            raise RuntimeError(
                "GitHub asset download failed. Check 'gh auth status' and your "
                "repository permissions. " + proc.stderr.decode("utf-8", errors="replace")[:500]
            )
        if sha256(temp_path) != EXPECTED_SHA256:
            raise ValueError(
                "GitHub CLI did not return the exact pinned R2 bytes. "
                "Download the R2 ZIP in your signed-in browser and use --local. "
                "Never disable or change the hash gate to make an unrelated file pass."
            )
        temp_path.replace(dest)
        return "authenticated-github-api-asset"
    finally:
        if temp_path.exists():
            temp_path.unlink()


def inspect_r2(archive: Path) -> dict:
    if archive.stat().st_size != EXPECTED_SIZE:
        raise ValueError(f"R2 size mismatch: got {archive.stat().st_size}, expected {EXPECTED_SIZE}")
    actual = sha256(archive)
    if actual != EXPECTED_SHA256:
        raise ValueError(f"R2 SHA256 mismatch: {actual}")

    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError("R2 ZIP CRC validation failed")
        members = z.namelist()
        if len(members) != len(set(members)):
            raise ValueError("R2 ZIP has duplicate archive paths")
        manifest = json.loads(z.read("manifest.json"))
        if manifest.get("minecraft", {}).get("version") != "1.21.1":
            raise ValueError("Unexpected Minecraft version")
        if not any(v.get("id") == "neoforge-21.1.252" for v in manifest.get("minecraft", {}).get("modLoaders", [])):
            raise ValueError("Unexpected NeoForge version")
        refs = manifest.get("files", [])
        if len(refs) != EXPECTED_CF_REFERENCES or len({f["projectID"] for f in refs}) != len(refs):
            raise ValueError("R2 CurseForge reference inventory mismatch")
        if any(f["projectID"] == 1141465 for f in refs):
            raise ValueError("Removed Demi's Sky Arena returned to manifest")

        jar_paths = sorted(
            n for n in members if n.startswith("overrides/mods/") and n.lower().endswith(".jar")
        )
        if len(jar_paths) != EXPECTED_CUSTOM_JARS:
            raise ValueError(f"Expected 10 bundled JARs; got {len(jar_paths)}")
        jars = []
        for name in jar_paths:
            binary = z.read(name)
            import io
            with zipfile.ZipFile(io.BytesIO(binary)) as nested:
                if nested.testzip() is not None:
                    raise ValueError(f"Corrupt embedded JAR: {name}")
            jars.append({
                "path": name,
                "sha256": hashlib.sha256(binary).hexdigest(),
                "bytes": len(binary),
            })
        return {
            "status": "STATIC_ARCHIVE_VERIFIED_ONLY",
            "source_release_id": RELEASE_ID,
            "source_asset_id": ASSET_ID,
            "source_release_url": f"https://github.com/{REPO}/releases/tag/untagged-28508fbadd878b4afd7d",
            "zip_name": FILENAME,
            "zip_size_bytes": archive.stat().st_size,
            "zip_sha256": actual,
            "curseforge_references": len(refs),
            "official_mod_references_expected": 330,
            "custom_jar_count": len(jars),
            "custom_jars": jars,
            "minecraft_runtime_tested": False,
            "r3_built": False,
            "note": "Keep R2 immutable; newer R3 compilation must replace changed addon JARs, not add duplicates.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("build/r2-inputs"))
    parser.add_argument("--local", type=Path, help="Already-downloaded exact R2 ZIP (offline validation)")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    dest = args.out_dir / FILENAME
    provenance = obtain_asset(dest, args.local)
    receipt = inspect_r2(dest)
    receipt["obtained_via"] = provenance
    receipt["local_archive_path"] = str(dest.resolve())
    report_path = args.out_dir / "R2-INPUTS-VERIFIED.json"
    report_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "archive": str(dest),
        "sha256": receipt["zip_sha256"],
        "curseforge_references": receipt["curseforge_references"],
        "embedded_jars": receipt["custom_jar_count"],
        "inventory": str(report_path),
        "minecraft_runtime_tested": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"INPUT PREPARATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
