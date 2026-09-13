#!/usr/bin/env python3
"""
Admin Build & Packaging Utility for CYBERLEEK: Evidence 02 - The Hidden Signal
Automates artifact regeneration and bundles round2/user/ into evidence_bundle.zip.
Enforces strict zero-leakage security audit ensuring zero admin files are packaged.
"""

import hashlib
import os
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROUND2_DIR = SCRIPT_DIR.parent
USER_DIR = ROUND2_DIR / "user"
ADMIN_DIR = ROUND2_DIR / "admin"

# Add generator paths to sys.path
for lvl in ("level1", "level2", "level3", "level4"):
    p = str(ADMIN_DIR / lvl / "src")
    if p not in sys.path:
        sys.path.insert(0, p)

import generate_level1
import generate_level2
import generate_level4
import generate_level3


def build_all():
    print("=" * 70)
    print("CYBERLEEK EVIDENCE 02 // ADMIN REPRODUCIBLE BUILD & PACKAGING PIPELINE")
    print("=" * 70)

    # 1. Regenerate all challenge assets in sequence
    print("\n[*] Step 1: Running Level 1 Generator (generate_level1.py)...")
    generate_level1.generate_challenge()

    print("\n[*] Step 2: Running Level 2 Generator (generate_level2.py)...")
    generate_level2.generate_challenge()

    print("\n[*] Step 3: Running Level 4 Generator (generate_level4.py)...")
    generate_level4.generate_challenge()

    print("\n[*] Step 4: Running Level 3 Generator (generate_level3.py)...")
    generate_level3.generate_challenge()

    # 2. Package evidence_bundle.zip from round2/user/
    print("\n[*] Step 5: Packaging participant distribution bundle from user/...")
    bundle_path = ADMIN_DIR / "evidence_bundle.zip"

    packaged_count = 0
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(USER_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(USER_DIR).as_posix()
                zf.write(file_path, arcname=arcname)
                packaged_count += 1
                print(f"    [+] Packaged: {arcname} ({file_path.stat().st_size} bytes)")

    print(f"[+] Total files packaged: {packaged_count}")

    # 3. Strict zero-leak security audit of the bundle
    print("\n[*] Step 6: Performing strict zero-leak audit of evidence_bundle.zip...")
    forbidden_terms = ["solution", "generate", "test", "upload", "admin", "main.md", "validation"]
    with zipfile.ZipFile(bundle_path, "r") as zf:
        names = zf.namelist()
        for name in names:
            lower = name.lower()
            for term in forbidden_terms:
                if term in lower:
                    raise RuntimeError(f"SECURITY LEAK: Found forbidden term '{term}' in bundle entry: {name}")
            data = zf.read(name)
            if b"CYBERLEEK{H1dd3n_4@S}" in data:
                raise RuntimeError(f"PLAINTEXT FLAG LEAK DETECTED in bundle entry: {name}")

    bundle_size = bundle_path.stat().st_size
    bundle_hash = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
    print("\n[+] Bundle Built & Audited Successfully!")
    print(f"    Bundle Path:   {bundle_path.relative_to(ROUND2_DIR)}")
    print(f"    Bundle Size:   {bundle_size} bytes")
    print(f"    Bundle SHA256: {bundle_hash}")
    print("=" * 70)
    return bundle_hash


if __name__ == "__main__":
    build_all()
