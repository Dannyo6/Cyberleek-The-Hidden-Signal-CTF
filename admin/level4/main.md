# Admin Reference — Level 2.4: Final Asset Recovery

## 1. Challenge Overview & Metadata
- **Level ID:** 2.4
- **Domain:** Modern Cryptography (Hard)
- **Storyline:** Cryptographic recovery of the core leaked developer asset.
- **Player Artifact:** `user/level4/files/recovery_manifest.enc`
- **Admin Upload:** `admin/level4/uploads/recovery_manifest.enc` (and `stage4_validation.json`)
- **Generator Script:** `admin/level4/src/generate_level4.py`
- **Prerequisites:**
  - `LEEK_STREAM_KEY_8080` (from Level 2.1)
  - `IV_CYBERLEEK_2026` (from Level 2.3)
  - `STAGE4_BLOB` (from Level 2.3 or `recovery_manifest.enc`)

## 2. Cryptographic Architecture
- **Cipher Mechanics:** 16-round balanced Feistel block cipher in Cipher Block Chaining (CBC) mode with PKCS7 padding.
- **Block Size:** 16 bytes (split into 8-byte halves $L$ and $R$).
- **Subkey Derivation:**
  $$K_r = \text{SHA-256}(\text{"LEEK\_STREAM\_KEY\_8080"} \parallel \text{"IV\_CYBERLEEK\_2026"} \parallel r\text{.to\_bytes(2, 'big')})[:8]$$
  for each round $r \in [0, 15]$.
- **Round Function:**
  $$F(R, K_r) = \text{SHA-256}(R \parallel K_r)[:8]$$
- **CBC IV Block:**
  $$\text{IV\_BLOCK} = \text{SHA-256}(\text{"IV\_CYBERLEEK\_2026"})[:16]$$
- **Decryption Result:**
  Authoritative competition flag:
  ```text
  CYBERLEEK{H1dd3n_4@S}
  ```

## 3. Step-by-Step Mathematical Walkthrough
1. Load `recovery_manifest.enc` (or `STAGE4_BLOB`).
2. Generate the 16 round subkeys in order.
3. For each 16-byte block in CBC mode:
   - Run Feistel network using subkeys in reverse order ($K_{15} \dots K_0$).
   - XOR with the previous ciphertext block (or IV block).
4. Remove PKCS7 padding.
5. Decode decrypted bytes to reveal the canonical flag `CYBERLEEK{H1dd3n_4@S}`.

## 4. Complete Python Solver Script
```python
#!/usr/bin/env python3
"""
Admin Verification Solver — Level 2.4
"""
import hashlib
from pathlib import Path

manifest_path = Path(__file__).resolve().parent.parent.parent / "user" / "level4" / "files" / "recovery_manifest.enc"
if not manifest_path.exists():
    manifest_path = Path("user/level4/files/recovery_manifest.enc")

ciphertext = manifest_path.read_bytes()

KEY_TOKEN = "LEEK_STREAM_KEY_8080"
IV_STRING = "IV_CYBERLEEK_2026"

round_keys = [
    hashlib.sha256(KEY_TOKEN.encode("utf-8") + IV_STRING.encode("utf-8") + r.to_bytes(2, "big")).digest()[:8]
    for r in range(16)
]

def feistel_block(block: bytes, keys: list) -> bytes:
    L, R = block[:8], block[8:]
    for k in keys:
        F = hashlib.sha256(R + k).digest()[:8]
        L, R = R, bytes(x ^ y for x, y in zip(L, F))
    return R + L

iv_block = hashlib.sha256(IV_STRING.encode("utf-8")).digest()[:16]
plaintext = bytearray()
prev = iv_block

for i in range(0, len(ciphertext), 16):
    block = ciphertext[i : i + 16]
    dec = feistel_block(block, list(reversed(round_keys)))
    plaintext.extend(bytes(x ^ y for x, y in zip(dec, prev)))
    prev = block

pad_len = plaintext[-1]
flag = plaintext[:-pad_len].decode("utf-8")

print(f"[+] Successfully Decrypted Final Level 4 Flag: {flag}")
assert flag == "CYBERLEEK{H1dd3n_4@S}"
```

## 5. Security & Validation Checklist
- [x] Generator builds artifact cleanly via `generate_level4.py`.
- [x] Feistel block cipher operates in pure Python with zero external dependencies.
- [x] Incomplete/partial keys fail padding or yield pseudorandom garbage.
- [x] Flag string `CYBERLEEK{H1dd3n_4@S}` matches platform target.
