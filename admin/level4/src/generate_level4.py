#!/usr/bin/env python3
"""
Generator and Synthesis Engine for Level 4: The Core Leaked Developer Asset
Domain: Cryptography (Hard)
Theme: CYBERLEEK — August 2026 GTA VI Developer Asset Leak

Generates:
  - admin/level4/uploads/recovery_manifest.enc
  - admin/level4/uploads/stage4_validation.json
  - user/level4/files/recovery_manifest.enc
Mechanics: 16-Round Feistel-style block cipher in CBC mode
Keys:
  - Level 1 Primary Key: "LEEK_STREAM_KEY_8080"
  - Level 3 IV Token:    "IV_CYBERLEEK_2026"
Decryption Yields:
  Official Registry Flag: CYBERLEEK{H1dd3n_4@S}
"""

import hashlib
import json
from pathlib import Path

TARGET_FLAG = "CYBERLEEK{H1dd3n_4@S}"
KEY_TOKEN = "LEEK_STREAM_KEY_8080"
IV_STRING = "IV_CYBERLEEK_2026"
NUM_ROUNDS = 16
BLOCK_SIZE = 16

SCRIPT_DIR = Path(__file__).resolve().parent
LEVEL_DIR = SCRIPT_DIR.parent
ADMIN_DIR = LEVEL_DIR.parent
ROUND2_DIR = ADMIN_DIR.parent

UPLOADS_DIR = LEVEL_DIR / "uploads"
USER_FILES_DIR = ROUND2_DIR / "user" / "level4" / "files"
OUTPUT_FILENAME = "recovery_manifest.enc"


def get_round_keys(key_token: str, iv_str: str, num_rounds: int = NUM_ROUNDS) -> list:
    """Derives 8-byte subkeys for each Feistel round using SHA-256."""
    keys = []
    for r in range(num_rounds):
        h = hashlib.sha256(key_token.encode("utf-8") + iv_str.encode("utf-8") + r.to_bytes(2, "big")).digest()
        keys.append(h[:8])
    return keys


def feistel_f(r_block: bytes, k_r: bytes) -> bytes:
    """Non-linear round function mapping 8-byte half-block and subkey to 8-byte output."""
    return hashlib.sha256(r_block + k_r).digest()[:8]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def feistel_block(block: bytes, round_keys: list) -> bytes:
    """Executes the balanced Feistel network across half-blocks."""
    L, R = block[:8], block[8:]
    for k in round_keys:
        L, R = R, xor_bytes(L, feistel_f(R, k))
    return R + L


def feistel_encrypt_block(block: bytes, round_keys: list) -> bytes:
    return feistel_block(block, round_keys)


def feistel_decrypt_block(block: bytes, round_keys: list) -> bytes:
    """Decryption in a Feistel network is identical to encryption with reversed subkeys."""
    return feistel_block(block, list(reversed(round_keys)))


def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes) -> bytes:
    if not data:
        raise ValueError("Invalid empty payload")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE or data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS7 padding")
    return data[:-pad_len]


def feistel_cbc_encrypt(plaintext: bytes, key: str, iv: str) -> bytes:
    """Encrypts byte stream using 16-round Feistel cipher in CBC mode."""
    round_keys = get_round_keys(key, iv)
    iv_block = hashlib.sha256(iv.encode("utf-8")).digest()[:BLOCK_SIZE]
    padded = pkcs7_pad(plaintext)
    ciphertext = bytearray()
    prev = iv_block
    for i in range(0, len(padded), BLOCK_SIZE):
        block = padded[i : i + BLOCK_SIZE]
        xored = xor_bytes(block, prev)
        enc = feistel_encrypt_block(xored, round_keys)
        ciphertext.extend(enc)
        prev = enc
    return bytes(ciphertext)


def feistel_cbc_decrypt(ciphertext: bytes, key: str, iv: str) -> bytes:
    """Decrypts byte stream using 16-round Feistel cipher in CBC mode."""
    round_keys = get_round_keys(key, iv)
    iv_block = hashlib.sha256(iv.encode("utf-8")).digest()[:BLOCK_SIZE]
    plaintext = bytearray()
    prev = iv_block
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i : i + BLOCK_SIZE]
        dec = feistel_decrypt_block(block, round_keys)
        plaintext.extend(xor_bytes(dec, prev))
        prev = block
    return pkcs7_unpad(bytes(plaintext))


def encrypt_stage4(key_token: str, iv_str: str, plaintext: str) -> bytes:
    """Public interface to encrypt plaintext into STAGE4_BLOB."""
    return feistel_cbc_encrypt(plaintext.encode("utf-8"), key_token, iv_str)


def decrypt_stage4(key_token: str, iv_str: str, blob: bytes) -> str:
    """Public interface to decrypt STAGE4_BLOB into plaintext string."""
    decrypted_bytes = feistel_cbc_decrypt(blob, key_token, iv_str)
    return decrypted_bytes.decode("utf-8")


def generate_challenge():
    """Generates recovery_manifest.enc for uploads/ and user/level4/files/."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    blob = encrypt_stage4(KEY_TOKEN, IV_STRING, TARGET_FLAG)

    targets = [UPLOADS_DIR / OUTPUT_FILENAME, USER_FILES_DIR / OUTPUT_FILENAME]
    sha256_hash = ""
    for target in targets:
        with open(target, "wb") as f:
            f.write(blob)
        file_size = target.stat().st_size
        sha256_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        rel_path = target.relative_to(ROUND2_DIR)
        print(f"[+] Successfully generated Level 4 artifact:")
        print(f"    Path:   {rel_path}")
        print(f"    Size:   {file_size} bytes")
        print(f"    SHA256: {sha256_hash}")

    # Save validation metadata in uploads/
    validation_meta = {
        "challenge": "CYBERLEEK Level 4 Feistel Recovery",
        "key_token": KEY_TOKEN,
        "iv_token": IV_STRING,
        "blob_hex": blob.hex().upper(),
        "blob_sha256": hashlib.sha256(blob).hexdigest(),
        "flag_sha256": hashlib.sha256(TARGET_FLAG.encode("utf-8")).hexdigest(),
        "expected_flag": TARGET_FLAG
    }
    meta_path = UPLOADS_DIR / "stage4_validation.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(validation_meta, f, indent=2)

    # Self-test decryption
    recovered_flag = decrypt_stage4(KEY_TOKEN, IV_STRING, blob)
    assert recovered_flag == TARGET_FLAG, f"Decryption test failed: {recovered_flag}"

    return blob


if __name__ == "__main__":
    generate_challenge()
