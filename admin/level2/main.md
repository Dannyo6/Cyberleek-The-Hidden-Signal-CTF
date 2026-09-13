# Admin Reference — Level 2.2: Intercepted Developer Stream Telemetry

## 1. Challenge Overview & Metadata
- **Level ID:** 2.2
- **Domain:** Cryptography (Medium)
- **Storyline:** Network packet dump intercepting internal developer memory cache syncs.
- **Player Artifact:** `user/level2/files/traffic_intercept.hex`
- **Admin Upload:** `admin/level2/uploads/traffic_intercept.hex`
- **Generator Script:** `admin/level2/src/generate_level2.py`
- **Prerequisites:** `LEEK_STREAM_KEY_8080` and `0x7A3F` from Level 2.1.

## 2. Cryptographic Architecture
- **Cipher Mechanics:** Synchronous stream XOR cipher driven by a 32-bit Linear Congruential Generator (LCG).
- **LCG Parameters:**
  - Multiplier $a = 1664525$
  - Addend $c = 1013904223$
  - Modulus $m = 2^{32} = 4294967296$
  - Recurrence: $X_{n+1} = (a \cdot X_n + c) \pmod{2^{32}}$
  - Keystream Byte: $(X_{n+1} \gg 16) \ \& \ 0\text{xFF}$
- **State Seeding:**
  - Base State: $X_0 = \text{int}("0\text{x7A3F}", 16) = 31295$
  - Key Mixing: For each byte in `"LEEK_STREAM_KEY_8080"`:
    $$\text{state} = (\text{state} \cdot 31 + \text{byte}) \pmod{2^{32}}$$
- **Decrypted Plaintext Yields:**
  - Carrier: `cyberleek_screen.png`
  - Bitmask plane: 2-bit LSB interleaved across Blue and Alpha channels
  - Stride: Every 7th pixel
  - Offset: Byte offset `0x1A4` (420 decimal)
  - Target payload: `STAGE4_BLOB` and `IV_CYBERLEEK_2026`

## 3. Step-by-Step Mathematical Walkthrough
1. Parse the hexadecimal text from `traffic_intercept.hex` into raw bytes.
2. Initialize LCG state using the polynomial hash of the Level 1 key and seed.
3. Advance LCG for each byte of ciphertext and extract upper 16-bit entropy as keystream byte.
4. XOR ciphertext bytes with keystream bytes.
5. Decode UTF-8 string to reveal steganography parameters for Level 2.3.

## 4. Complete Python Solver Script
```python
#!/usr/bin/env python3
"""
Admin Verification Solver — Level 2.2
"""
import re
from pathlib import Path

hex_path = Path(__file__).resolve().parent.parent.parent / "user" / "level2" / "files" / "traffic_intercept.hex"
if not hex_path.exists():
    hex_path = Path("user/level2/files/traffic_intercept.hex")

with open(hex_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"ENCRYPTED TELEMETRY STREAM \(HEX\):\s*\n-+\s*\n(.*?)\n-+", content, re.DOTALL)
if not match:
    raise ValueError("Hex stream section not found in artifact")

hex_str = match.group(1).replace(" ", "").replace("\n", "").strip()
ciphertext = bytes.fromhex(hex_str)

seed_hex = "0x7A3F"
key_token = "LEEK_STREAM_KEY_8080"

state = int(seed_hex, 16)
for b in key_token.encode("utf-8"):
    state = (state * 31 + b) & 0xFFFFFFFF

A = 1664525
C = 1013904223
M = 2**32

keystream = bytearray()
for _ in range(len(ciphertext)):
    state = (A * state + C) & 0xFFFFFFFF
    keystream.append((state >> 16) & 0xFF)

plaintext = bytes([c ^ k for c, k in zip(ciphertext, keystream)]).decode("utf-8")
print("[+] Decrypted Stream Telemetry:\n", plaintext)

assert "cyberleek_screen.png" in plaintext
assert "0x1A4" in plaintext
assert "7 pixels" in plaintext
```

## 5. Security & Validation Checklist
- [x] Generator builds artifact cleanly via `generate_level2.py`.
- [x] State search space ($2^{32}$) prevents trivial brute force without Level 1 secrets.
- [x] Output accurately informs participant of Level 2.3 extraction parameters.
