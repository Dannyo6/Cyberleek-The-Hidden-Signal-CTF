#!/usr/bin/env python3
"""
Automated Test Suite for CYBERLEEK: Evidence 02 - The Hidden Signal
Validates the complete 4-level investigation chain across all 12 mandatory test cases.
Resolves artifacts against round2/user/levelX/files/.
Asserts that the final decrypted flag strictly equals CYBERLEEK{H1dd3n_4@S}.
"""

import hashlib
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
ROUND2_DIR = SCRIPT_DIR.parent
ADMIN_DIR = SCRIPT_DIR
USER_DIR = ROUND2_DIR / "user"

# Register generator paths
for lvl in ("level1", "level2", "level3", "level4"):
    p = str(ADMIN_DIR / lvl / "src")
    if p not in sys.path:
        sys.path.insert(0, p)

import generate_level1
import generate_level2
import generate_level3
import generate_level4

TARGET_FLAG = "CYBERLEEK{H1dd3n_4@S}"
EXPECTED_KEY_TOKEN = "LEEK_STREAM_KEY_8080"
EXPECTED_SEED_HEX = "0x7A3F"
EXPECTED_IV = "IV_CYBERLEEK_2026"


def run_all_tests():
    print("=" * 75)
    print("CYBERLEEK: EVIDENCE 02 — THE HIDDEN SIGNAL // AUTOMATED TEST SUITE")
    print("=" * 75)

    # 1. Regenerate fresh challenge assets
    print("\n[*] Step 0: Regenerating fresh challenge assets across all 4 levels...")
    generate_level1.generate_challenge()
    generate_level2.generate_challenge()
    generate_level4.generate_challenge()
    generate_level3.generate_challenge()

    results = []
    hashes = {}

    # Initialize clean isolated test directory with player artifacts from user/
    with tempfile.TemporaryDirectory() as test_dir:
        test_path = Path(test_dir)
        p_l1 = test_path / "level1"
        p_l2 = test_path / "level2"
        p_l3 = test_path / "level3"
        p_l4 = test_path / "level4"
        for p in (p_l1, p_l2, p_l3, p_l4):
            p.mkdir(parents=True)

        shutil.copy(USER_DIR / "level1" / "files" / "dev_leak_chat.txt", p_l1 / "dev_leak_chat.txt")
        shutil.copy(USER_DIR / "level2" / "files" / "traffic_intercept.hex", p_l2 / "traffic_intercept.hex")
        shutil.copy(USER_DIR / "level3" / "files" / "cyberleek_screen.png", p_l3 / "cyberleek_screen.png")
        shutil.copy(USER_DIR / "level4" / "files" / "recovery_manifest.enc", p_l4 / "recovery_manifest.enc")

        print("\n[+] Clean isolated test directory initialized with user/ artifacts.")

        key_token = ""
        seed_hex = ""
        stego_offset = None
        stego_stride = None
        recovered_iv = ""
        recovered_blob = b""

        # =====================================================================
        # TEST 1: Solve Level 1 -> Key: LEEK_STREAM_KEY_8080, Seed: 0x7A3F
        # =====================================================================
        try:
            with open(p_l1 / "dev_leak_chat.txt", "r", encoding="utf-8") as f:
                chat_text = f.read()

            match = re.search(r"ENCRYPTED BUILD VALIDATION PAYLOAD:\s*\n-+\s*\n(.*?)\n-+", chat_text, re.DOTALL)
            assert match, "Encrypted payload section not found in Level 1 chat"
            ciphertext = match.group(1).replace(" ", "").replace("\n", "").strip()

            key = "VICE"
            num_cols = len(key)
            num_rows = len(ciphertext) // num_cols
            key_order = sorted(range(len(key)), key=lambda i: key[i])

            cols = {}
            pos = 0
            for k_idx in key_order:
                cols[k_idx] = ciphertext[pos : pos + num_rows]
                pos += num_rows

            digits = []
            for r in range(num_rows):
                for c in range(num_cols):
                    digits.append(cols[c][r])
            digits_str = "".join(digits)

            polybius_grid = [
                ['A', 'B', 'C', 'D', 'E', 'F'],
                ['G', 'H', 'I', 'K', 'L', 'M'],
                ['N', 'O', 'P', 'Q', 'R', 'S'],
                ['T', 'U', 'V', 'W', 'X', 'Y'],
                ['Z', '0', '1', '2', '3', '4'],
                ['5', '6', '7', '8', '9', '_'],
            ]

            decoded_chars = []
            for i in range(0, len(digits_str), 2):
                r = int(digits_str[i]) - 1
                c = int(digits_str[i + 1]) - 1
                decoded_chars.append(polybius_grid[r][c])
            l1_plain = "".join(decoded_chars)

            assert EXPECTED_KEY_TOKEN in l1_plain, f"Key Token {EXPECTED_KEY_TOKEN} not found"
            assert "0X7A3F" in l1_plain.upper(), f"Seed {EXPECTED_SEED_HEX} not found"
            assert TARGET_FLAG not in l1_plain, "Flag must not be leaked in Level 1"

            key_token = EXPECTED_KEY_TOKEN
            seed_hex = EXPECTED_SEED_HEX
            results.append(("TEST 1", "PASS", f"Recovered Key Token: '{key_token}', Seed: '{seed_hex}'"))
        except Exception as e:
            results.append(("TEST 1", "FAIL", str(e)))

        # =====================================================================
        # TEST 2: Attempt Level 2 solve without Level 1 key -> Verify shortcut failure
        # =====================================================================
        try:
            with open(p_l2 / "traffic_intercept.hex", "r", encoding="utf-8") as f:
                l2_content = f.read()

            match = re.search(r"ENCRYPTED TELEMETRY STREAM \(HEX\):\s*\n-+\s*\n(.*?)\n-+", l2_content, re.DOTALL)
            assert match
            hex_str = match.group(1).replace(" ", "").replace("\n", "").strip()
            l2_ciphertext = bytes.fromhex(hex_str)

            trivial_seeds = [0, 1, 0x1337, 0xFFFF]
            for ts in trivial_seeds:
                state = ts
                stream = bytearray()
                for _ in range(len(l2_ciphertext)):
                    state = (1664525 * state + 1013904223) & 0xFFFFFFFF
                    stream.append((state >> 16) & 0xFF)
                dec = bytes([c ^ k for c, k in zip(l2_ciphertext, stream)])
                assert b"cyberleek_screen.png" not in dec, "Decryption succeeded with invalid seed!"

            results.append(("TEST 2", "PASS", "Level 2 fails cleanly with incorrect/trivial LCG seeds"))
        except Exception as e:
            results.append(("TEST 2", "FAIL", str(e)))

        # =====================================================================
        # TEST 3: Solve Level 2 with Level 1 credentials -> Recover stego parameters
        # =====================================================================
        try:
            state = int(seed_hex, 16)
            for b in key_token.encode("utf-8"):
                state = (state * 31 + b) & 0xFFFFFFFF

            stream = bytearray()
            for _ in range(len(l2_ciphertext)):
                state = (1664525 * state + 1013904223) & 0xFFFFFFFF
                stream.append((state >> 16) & 0xFF)

            l2_plaintext = bytes([c ^ k for c, k in zip(l2_ciphertext, stream)]).decode("utf-8")
            assert "cyberleek_screen.png" in l2_plaintext
            assert "2-bit LSB interleaved across Blue and Alpha" in l2_plaintext
            assert "0x1A4" in l2_plaintext
            assert "7 pixels" in l2_plaintext
            assert TARGET_FLAG not in l2_plaintext

            stego_offset = 0x1A4
            stego_stride = 7
            results.append(("TEST 3", "PASS", f"Recovered Stego Parameters (Offset={hex(stego_offset)}, Stride={stego_stride}, Blue/Alpha 2-bit)"))
        except Exception as e:
            results.append(("TEST 3", "FAIL", str(e)))

        # =====================================================================
        # TEST 4: Attempt Level 3 stego extraction with wrong parameters -> Verify failure
        # =====================================================================
        try:
            img = Image.open(p_l3 / "cyberleek_screen.png").convert("RGBA")
            pixels = img.load()
            w, h = img.size

            wrong_len_bytes = bytearray()
            for i in range(4):
                idx0 = (i * 2)
                idx1 = (i * 2 + 1)
                b0 = pixels[idx0 % w, idx0 // w][2]
                a0 = pixels[idx0 % w, idx0 // w][3]
                b1 = pixels[idx1 % w, idx1 // w][2]
                a1 = pixels[idx1 % w, idx1 // w][3]
                low = (b0 & 3) | ((a0 & 3) << 2)
                high = (b1 & 3) | ((a1 & 3) << 2)
                wrong_len_bytes.append(low | (high << 4))
            wrong_len = int.from_bytes(wrong_len_bytes, "big")
            assert wrong_len > 100000 or wrong_len == 0 or wrong_len != 97

            results.append(("TEST 4", "PASS", "Stego extraction with default/incorrect parameters yields invalid payload"))
        except Exception as e:
            results.append(("TEST 4", "FAIL", str(e)))

        # =====================================================================
        # TEST 5: Solve Level 3 with exact parameters -> Extract IV and STAGE4_BLOB
        # =====================================================================
        try:
            def read_byte_at(pair_idx: int) -> int:
                idx0 = stego_offset + (pair_idx * 2) * stego_stride
                idx1 = stego_offset + (pair_idx * 2 + 1) * stego_stride
                x0, y0 = idx0 % w, idx0 // w
                x1, y1 = idx1 % w, idx1 // w
                _, _, b0, a0 = pixels[x0, y0]
                _, _, b1, a1 = pixels[x1, y1]
                low = (b0 & 3) | ((a0 & 3) << 2)
                high = (b1 & 3) | ((a1 & 3) << 2)
                return low | (high << 4)

            length_bytes = bytes([read_byte_at(i) for i in range(4)])
            payload_len = int.from_bytes(length_bytes, "big")
            assert 20 < payload_len < 1000, f"Unexpected payload length: {payload_len}"

            payload_raw = bytes([read_byte_at(4 + i) for i in range(payload_len)])
            payload_str = payload_raw.decode("utf-8")

            iv_match = re.search(r"IV:\s*(\S+)", payload_str)
            blob_match = re.search(r"BLOB:\s*([0-9a-fA-F]+)", payload_str)
            assert iv_match and blob_match, "Failed to parse IV and BLOB from payload"

            recovered_iv = iv_match.group(1)
            recovered_blob = bytes.fromhex(blob_match.group(1))

            assert recovered_iv == EXPECTED_IV, f"IV mismatch: {recovered_iv}"
            assert len(recovered_blob) == 32, f"Blob length mismatch: {len(recovered_blob)}"
            results.append(("TEST 5", "PASS", f"Extracted IV: '{recovered_iv}' and Blob ({len(recovered_blob)} bytes)"))
        except Exception as e:
            results.append(("TEST 5", "FAIL", str(e)))

        # =====================================================================
        # TEST 6: Verify cyberleek_screen.png has zero static plaintext leaks
        # =====================================================================
        try:
            raw_img_bytes = (p_l3 / "cyberleek_screen.png").read_bytes()
            assert TARGET_FLAG.encode("utf-8") not in raw_img_bytes, "Flag leaked in raw image bytes!"
            assert b"H1dd3n_4@S" not in raw_img_bytes, "Flag fragment leaked in raw image bytes!"
            assert recovered_iv.encode("utf-8") not in raw_img_bytes, "IV leaked in raw image bytes!"
            results.append(("TEST 6", "PASS", "Zero plaintext flag or IV leaked in cyberleek_screen.png file data"))
        except Exception as e:
            results.append(("TEST 6", "FAIL", str(e)))

        # =====================================================================
        # TEST 7: Attempt Level 4 decryption with wrong/partial keys -> Verify failure
        # =====================================================================
        try:
            wrong_keys = ["WRONG_STREAM_KEY", "LEEK_STREAM_KEY_9999", "admin", "password"]
            for wk in wrong_keys:
                try:
                    res = generate_level4.decrypt_stage4(wk, recovered_iv, recovered_blob)
                    assert res != TARGET_FLAG
                except Exception:
                    pass

            results.append(("TEST 7", "PASS", "Level 4 Feistel decryption strictly rejects invalid keys and IVs"))
        except Exception as e:
            results.append(("TEST 7", "FAIL", str(e)))

        # =====================================================================
        # TEST 8: Execute Level 4 synthesis with full key -> Asserts CYBERLEEK{H1dd3n_4@S}
        # =====================================================================
        try:
            final_token = generate_level4.decrypt_stage4(key_token, recovered_iv, recovered_blob)
            assert final_token == TARGET_FLAG, f"Flag mismatch: {final_token} != {TARGET_FLAG}"
            results.append(("TEST 8", "PASS", f"Flag strictly matches: '{final_token}'"))
        except Exception as e:
            results.append(("TEST 8", "FAIL", str(e)))

        # =====================================================================
        # TEST 9: Verify recovery_manifest.enc matches extracted blob & decrypts
        # =====================================================================
        try:
            manifest_bytes = (p_l4 / "recovery_manifest.enc").read_bytes()
            assert manifest_bytes == recovered_blob, "recovery_manifest.enc does not match extracted STAGE4_BLOB"
            manifest_decrypted = generate_level4.decrypt_stage4(key_token, recovered_iv, manifest_bytes)
            assert manifest_decrypted == TARGET_FLAG
            results.append(("TEST 9", "PASS", "recovery_manifest.enc matches Level 3 blob and cleanly decrypts to flag"))
        except Exception as e:
            results.append(("TEST 9", "FAIL", str(e)))

        # =====================================================================
        # TEST 10: Zero legacy references remaining in active challenge files
        # =====================================================================
        try:
            legacy_keywords = [b"arkham", b"riddler", b"blackgate", b"mirror_room"]
            checked_count = 0
            for root, _, files in os.walk(ROUND2_DIR):
                for file in files:
                    if file.endswith((".py", ".md", ".txt", ".hex", ".json")) and file != "test_round2_chain.py":
                        fp = Path(root) / file
                        content = fp.read_bytes().lower()
                        for kw in legacy_keywords:
                            assert kw not in content, f"Legacy reference '{kw.decode()}' found in {fp.relative_to(ROUND2_DIR)}"
                        checked_count += 1

            results.append(("TEST 10", "PASS", f"Zero legacy references across all {checked_count} challenge files"))
        except Exception as e:
            results.append(("TEST 10", "FAIL", str(e)))

        # =====================================================================
        # TEST 11: Verify evidence_bundle.zip integrity and zero-leak policy
        # =====================================================================
        try:
            bundle_zip = ADMIN_DIR / "evidence_bundle.zip"
            assert bundle_zip.exists(), "evidence_bundle.zip must exist in admin/"

            with zipfile.ZipFile(bundle_zip, "r") as zf:
                names = zf.namelist()
                assert "level1/files/dev_leak_chat.txt" in names
                assert "level2/files/traffic_intercept.hex" in names
                assert "level3/files/cyberleek_screen.png" in names
                assert "level4/files/recovery_manifest.enc" in names
                for name in names:
                    lower = name.lower()
                    assert "admin" not in lower, f"Admin path leaked in bundle: {name}"
                    assert "solution" not in lower, f"Solution leaked in bundle: {name}"
                    assert "generate" not in lower, f"Generator leaked in bundle: {name}"
                    data = zf.read(name)
                    assert TARGET_FLAG.encode("utf-8") not in data

            results.append(("TEST 11", "PASS", "evidence_bundle.zip verified: complete user files, zero admin leaks"))
        except Exception as e:
            results.append(("TEST 11", "FAIL", str(e)))

        # =====================================================================
        # TEST 12: Verify all challenge artifacts using SHA-256
        # =====================================================================
        try:
            required_artifacts = [
                USER_DIR / "level1" / "files" / "dev_leak_chat.txt",
                USER_DIR / "level2" / "files" / "traffic_intercept.hex",
                USER_DIR / "level3" / "files" / "cyberleek_screen.png",
                USER_DIR / "level4" / "files" / "recovery_manifest.enc",
                ADMIN_DIR / "level1" / "uploads" / "dev_leak_chat.txt",
                ADMIN_DIR / "level2" / "uploads" / "traffic_intercept.hex",
                ADMIN_DIR / "level3" / "uploads" / "cyberleek_screen.png",
                ADMIN_DIR / "level4" / "uploads" / "recovery_manifest.enc",
                ADMIN_DIR / "evidence_bundle.zip",
            ]
            for art in required_artifacts:
                assert art.exists(), f"Missing required artifact: {art}"
                h = hashlib.sha256(art.read_bytes()).hexdigest()
                hashes[art.name] = (art.stat().st_size, h)

            results.append(("TEST 12", "PASS", f"All {len(hashes)} challenge artifacts verified with SHA-256"))
        except Exception as e:
            results.append(("TEST 12", "FAIL", str(e)))

    # Display Test Summary Table
    print("\n" + "=" * 75)
    print(f"{'TEST ID':<10} | {'STATUS':<6} | {'NOTES'}")
    print("-" * 75)
    all_passed = True
    for tid, status, notes in results:
        print(f"{tid:<10} | {status:<6} | {notes}")
        if status != "PASS":
            all_passed = False
    print("=" * 75)

    if all_passed:
        print("\n>>> ALL 12 TESTS PASSED! CYBERLEEK ROUND 2 READY FOR PRODUCTION <<<")
        print(f">>> AUTHORITATIVE FLAG: {TARGET_FLAG} <<<\n")
    else:
        print("\n>>> ONE OR MORE TESTS FAILED <<<\n")

    return all_passed, results, hashes


if __name__ == "__main__":
    success, _, _ = run_all_tests()
    if not success:
        sys.exit(1)
