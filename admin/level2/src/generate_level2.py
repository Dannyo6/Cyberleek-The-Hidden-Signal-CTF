#!/usr/bin/env python3
"""
Generator for Level 2: Intercepted Network Traffic
Domain: Cryptography (Medium)
Theme: CYBERLEEK — August 2026 GTA VI Developer Asset Leak

Generates:
  - admin/level2/uploads/traffic_intercept.hex
  - user/level2/files/traffic_intercept.hex
Cipher: Stream XOR cipher using 32-bit LCG keystream
Seeded with: 0x7A3F combined with LEEK_STREAM_KEY_8080

Decoded output reveals Level 3 stego extraction parameters:
  - 2-bit LSB interleaved across Blue and Alpha channels
  - Stride = 7 pixels
  - Offset = 0x1A4 (420 decimal)
"""

import hashlib
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LEVEL_DIR = SCRIPT_DIR.parent
ADMIN_DIR = LEVEL_DIR.parent
ROUND2_DIR = ADMIN_DIR.parent

UPLOADS_DIR = LEVEL_DIR / "uploads"
USER_FILES_DIR = ROUND2_DIR / "user" / "level2" / "files"
OUTPUT_FILENAME = "traffic_intercept.hex"

SEED_HEX = "0x7A3F"
KEY_TOKEN = "LEEK_STREAM_KEY_8080"

# LCG Constants (Numerical Recipes / 32-bit standard)
LCG_A = 1664525
LCG_C = 1013904223
LCG_M = 2**32

PLAINTEXT = """[CYBERLEEK NETWORK TELEMETRY INTERCEPT // AUG 2026]
SOURCE: 10.240.16.88:8080 (DEV_RELAY) -> 192.168.1.42:9000
BUILD_TAG: GTA6_DEV_ALPHA_BUILD_20260815_VCS
TRAFFIC_TYPE: DEVELOPER MEMORY CACHE SYNC PACKET DUMP
STATUS: CRITICAL ASSET STREAM COMPROMISED

STEGANOGRAPHY EXTRACTION PARAMETERS FOR CARRIER IMAGE:
- TARGET IMAGE: cyberleek_screen.png
- ENCODING: 2-bit LSB interleaved across Blue and Alpha channels
  (Blue bits [1:0] store lower 2 bits, Alpha bits [1:0] store upper 2 bits of each nibble)
- PIXEL OFFSET: 0x1A4 (420)
- PIXEL STRIDE: 7 pixels
- PAYLOAD FORMAT: Big-endian 32-bit length header followed by payload containing:
  1. IV: IV_CYBERLEEK_2026
  2. STAGE4_BLOB: Feistel block cipher encrypted recovery payload
"""


def init_lcg(seed_hex: str, key_token: str) -> int:
    """Combines seed and key token into initial LCG state using polynomial rolling hash."""
    state = int(seed_hex, 16)
    for b in key_token.encode("utf-8"):
        state = (state * 31 + b) & 0xFFFFFFFF
    return state


def lcg_keystream(initial_state: int, length: int) -> bytes:
    """Generates keystream bytes from LCG state."""
    state = initial_state
    stream = bytearray()
    for _ in range(length):
        state = (LCG_A * state + LCG_C) & 0xFFFFFFFF
        stream.append((state >> 16) & 0xFF)
    return bytes(stream)


def xor_crypt(data: bytes, keystream: bytes) -> bytes:
    """Applies symmetric XOR between data and keystream."""
    return bytes(d ^ k for d, k in zip(data, keystream))


def generate_challenge():
    """Generates traffic_intercept.hex for both uploads/ and user/level2/files/."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    plaintext_bytes = PLAINTEXT.encode("utf-8")
    initial_state = init_lcg(SEED_HEX, KEY_TOKEN)
    keystream = lcg_keystream(initial_state, len(plaintext_bytes))
    ciphertext = xor_crypt(plaintext_bytes, keystream)

    # Wrap formatted hex lines (16 hex bytes per line)
    hex_bytes_list = [f"{b:02X}" for b in ciphertext]
    lines = []
    for i in range(0, len(hex_bytes_list), 16):
        lines.append(" ".join(hex_bytes_list[i:i + 16]))
    formatted_hex = "\n".join(lines)

    header_content = f"""================================================================================
CYBERLEEK INCIDENT ARCHIVE // EVIDENCE 02: THE HIDDEN SIGNAL
CASE REF: CYBERLEEK-2026-GTA6  |  CAPTURE ID: NET-CAP-8080
SUBJECT: Intercepted Developer Stream Telemetry (Hex Dump)
================================================================================

EVIDENCE DESCRIPTION:
Raw packet stream intercepted from internal developer memory cache sync traffic
shortly after unauthorized external data transmission alerts triggered.

ANNOTATION (SECURITY FORENSICS):
The telemetry payload is encrypted using a synchronous stream XOR cipher.
Keystream is driven by a 32-bit Linear Congruential Generator (LCG):
  Recurrence: X_{{n+1}} = (1664525 * X_n + 1013904223) mod 2^32
  Byte Output: (X_{{n+1}} >> 16) & 0xFF
The generator was seeded using the credentials recovered from the developer chat:
  Base Seed: Seed parameter from Level 1
  Key Mix: Key Token from Level 1 mixed into state via polynomial hash:
           state = (state * 31 + byte) mod 2^32 for each byte in Key Token.

--------------------------------------------------------------------------------
ENCRYPTED TELEMETRY STREAM (HEX):
--------------------------------------------------------------------------------
{formatted_hex}
--------------------------------------------------------------------------------

STATUS: ENCRYPTED // PENDING STREAM DECRYPTION
================================================================================
"""

    targets = [UPLOADS_DIR / OUTPUT_FILENAME, USER_FILES_DIR / OUTPUT_FILENAME]
    sha256_hash = ""
    for target in targets:
        with open(target, "w", encoding="utf-8") as f:
            f.write(header_content)
        file_size = target.stat().st_size
        sha256_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        rel_path = target.relative_to(ROUND2_DIR)
        print(f"[+] Successfully generated Level 2 artifact:")
        print(f"    Path:   {rel_path}")
        print(f"    Size:   {file_size} bytes")
        print(f"    SHA256: {sha256_hash}")

    return sha256_hash


if __name__ == "__main__":
    generate_challenge()
