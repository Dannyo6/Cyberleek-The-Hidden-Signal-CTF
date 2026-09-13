#!/usr/bin/env python3
"""
Generator for Level 1: Developer Leak Chat
Domain: Cryptography (Easy / Medium)
Theme: CYBERLEEK — August 2026 GTA VI Developer Asset Leak

Generates:
  - admin/level1/uploads/dev_leak_chat.txt
  - user/level1/files/dev_leak_chat.txt
Cipher: Polybius 6x6 substitution + Columnar Transposition (Key: "VICE")
Decryption yields:
  Key Token: "LEEK_STREAM_KEY_8080"
  Seed:      "0x7A3F"
"""

import hashlib
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LEVEL_DIR = SCRIPT_DIR.parent
ADMIN_DIR = LEVEL_DIR.parent
ROUND2_DIR = ADMIN_DIR.parent

UPLOADS_DIR = LEVEL_DIR / "uploads"
USER_FILES_DIR = ROUND2_DIR / "user" / "level1" / "files"
OUTPUT_FILENAME = "dev_leak_chat.txt"

# Plaintext to hide in the chat logs
SECRET_PLAINTEXT = "KEY_LEEK_STREAM_KEY_8080_SEED_0X7A3F"
TRANSPOSITION_KEY = "VICE"

# 6x6 Polybius Grid:
# 25 letters (A-Z, I/J merged), 10 digits (0-9), 1 underscore ('_')
POLYBIUS_GRID = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'K', 'L', 'M'],
    ['N', 'O', 'P', 'Q', 'R', 'S'],
    ['T', 'U', 'V', 'W', 'X', 'Y'],
    ['Z', '0', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_'],
]

CHAR_TO_COORD = {}
for r_idx, row in enumerate(POLYBIUS_GRID):
    for c_idx, char in enumerate(row):
        coord = f"{r_idx + 1}{c_idx + 1}"
        CHAR_TO_COORD[char] = coord
CHAR_TO_COORD['J'] = CHAR_TO_COORD['I']  # I/J merged


def polybius_encrypt(plaintext: str) -> str:
    """Substitutes each character with its 2-digit (row, col) Polybius coordinate."""
    coords = []
    for c in plaintext.upper():
        if c in CHAR_TO_COORD:
            coords.append(CHAR_TO_COORD[c])
        else:
            raise ValueError(f"Character '{c}' not supported in Polybius grid")
    return "".join(coords)


def columnar_transposition_encrypt(digits: str, key: str) -> str:
    """
    Encrypts digit string using Columnar Transposition.
    Writes rows across len(key) columns, then reads columns in alphabetical order of key.
    """
    num_cols = len(key)
    num_rows = (len(digits) + num_cols - 1) // num_cols
    padded_digits = digits.ljust(num_rows * num_cols, '6')

    grid = []
    for r in range(num_rows):
        row = padded_digits[r * num_cols : (r + 1) * num_cols]
        grid.append(list(row))

    key_order = sorted(range(len(key)), key=lambda i: key[i])

    ciphertext = []
    for col_idx in key_order:
        for r in range(num_rows):
            ciphertext.append(grid[r][col_idx])

    return "".join(ciphertext)


def generate_challenge():
    """Generates dev_leak_chat.txt for both uploads/ and user/level1/files/."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Polybius substitution
    polybius_digits = polybius_encrypt(SECRET_PLAINTEXT)
    assert len(polybius_digits) == 72

    # 2. Columnar transposition with key "VICE"
    ciphertext = columnar_transposition_encrypt(polybius_digits, TRANSPOSITION_KEY)

    # Format ciphertext into groups of 4 for presentation
    formatted_cipher = " ".join(ciphertext[i:i+4] for i in range(0, len(ciphertext), 4))

    chat_content = f"""================================================================================
CYBERLEEK INCIDENT ARCHIVE // EVIDENCE 02: THE HIDDEN SIGNAL
SOURCE: DISCORD-IRC-BRIDGE (10.240.16.4:6697) #americas-build-review
INCIDENT DATE: 2026-08-14 03:22:19 UTC
CLASSIFICATION: LEAKED GTA VI DEV BUILD REVIEW & DEBUG LOGS
================================================================================

[03:18:22] <vance_lead> Internal debug metrics: GPU draw calls 4,821, VRAM load 14.8GB, sub-tick physics stable.
[03:19:02] <vance_lead> CI pipeline finished packing the Vice City sector 4 wireframe debug assets.
[03:19:45] <j_marston_net> Did you update the developer network telemetry authentication?
[03:20:12] <vance_lead> Yes. The stream validator requires two security parameters:
                        1. Key Token (LEEK_STREAM_KEY_*)
                        2. LCG Seed (0x*)
[03:21:00] <j_marston_net> Don't post the credentials in plaintext here. Security team is monitoring logs.
[03:21:30] <vance_lead> Standard protocol applies. I obfuscated the credential block using our 
                        classic two-stage cipher:
                        - Step 1: 6x6 Polybius matrix (A-Z with I/J combined, 0-9, and '_' in position 6,6).
                        - Step 2: Columnar transposition using our target city codename 'VICE'.
[03:22:01] <vance_lead> Decrypt the coordinate stream and look up the grid to recover the token and seed.
[03:22:15] <vance_lead> Here is the raw verification payload from the build server:

--------------------------------------------------------------------------------
ENCRYPTED BUILD VALIDATION PAYLOAD:
--------------------------------------------------------------------------------
{formatted_cipher}
--------------------------------------------------------------------------------

[03:23:10] <j_marston_net> Got it. Plugging the Key Token and Seed into our packet stream interceptor now.
[03:24:00] <vice_asset_bot> BUILD_ALERT: Sector 04 render carrier uploaded to staging storage.

================================================================================
STATUS: EVIDENCE CAPTURED // PENDING CRYPTOGRAPHIC ANALYSIS
================================================================================
"""

    targets = [UPLOADS_DIR / OUTPUT_FILENAME, USER_FILES_DIR / OUTPUT_FILENAME]
    sha256_hash = ""
    for target in targets:
        with open(target, "w", encoding="utf-8") as f:
            f.write(chat_content)
        file_size = target.stat().st_size
        sha256_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        rel_path = target.relative_to(ROUND2_DIR)
        print(f"[+] Successfully generated Level 1 artifact:")
        print(f"    Path:   {rel_path}")
        print(f"    Size:   {file_size} bytes")
        print(f"    SHA256: {sha256_hash}")

    return sha256_hash


if __name__ == "__main__":
    generate_challenge()
