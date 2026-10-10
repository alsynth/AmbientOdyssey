#!/usr/bin/env python3
"""Reproducible standalone test-session kit ZIP, no mods or game sources."""
import argparse
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "tools/collect_v04_session.py",
    "tools/audit_installed_jars_v04.py",
    "tools/diagnose_v04_instance.py",
    "docs/testing/V04H_TEST_SESSION_FIELD_SHEET.md",
    "docs/testing/V04H_INSTALLED_JAR_AND_SERVER_PREFLIGHT.md",
    "V04_TESTING_CHECKLIST.md",
    "V04_QUESTLOG_COMPAT.md",
    "TEST_SESSION_KIT_README.txt",
    "RUN_PREFLIGHT_WINDOWS.cmd",
)

def build(output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name in sorted(FILES):
            src = ROOT / name
            if not src.is_file():
                raise FileNotFoundError(src)
            info = zipfile.ZipInfo(name, (2026, 10, 10, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, src.read_bytes())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == set(FILES)
        assert not any(n.startswith("mods/") or n.endswith(".jar") for n in z.namelist())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"{output.name}: {output.stat().st_size} bytes, {len(FILES)} files, SHA256 {digest}")
    return digest

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    build(a.output)
