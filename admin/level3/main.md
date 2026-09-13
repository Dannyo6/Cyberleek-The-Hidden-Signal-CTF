# Admin Reference — Level 2.3: Developer Screen Steganography

## 1. Challenge Overview & Metadata
- **Level ID:** 2.3
- **Domain:** Steganography (Hard)
- **Storyline:** Leaked early-build Vice City developer screenshot with debug overlays.
- **Player Artifact:** `user/level3/files/cyberleek_screen.png`
- **Admin Upload:** `admin/level3/uploads/cyberleek_screen.png`
- **Generator Script:** `admin/level3/src/generate_level3.py`
- **Prerequisites:** Steganography extraction parameters from Level 2.2.

## 2. Steganographic Architecture
- **Carrier Specifications:**
  - Dimensions: $1280 \times 720$ pixels
  - Color Format: 32-bit RGBA (lossless PNG)
  - Visual Theme: Vice City neon wireframe debug screen with developer telemetry overlays.
- **Embedding Algorithm:**
  - Offset: Pixel index `0x1A4` (420 decimal)
  - Stride: `7` pixels
  - Bit planes: 2-bit LSB interleaved across Blue and Alpha channels
  - Bit-packing: Each byte spans 2 pixels:
    - **Pixel 0 (Low Nibble):** Blue bits [1:0] $\leftarrow b[1:0]$; Alpha bits [1:0] $\leftarrow b[3:2]$
    - **Pixel 1 (High Nibble):** Blue bits [1:0] $\leftarrow b[5:4]$; Alpha bits [1:0] $\leftarrow b[7:6]$
  - Header: 4-byte big-endian payload length prefix.
- **Extracted Yields:**
  - **IV Token:** `IV_CYBERLEEK_2026`
  - **Encrypted Ciphertext Block:** `STAGE4_BLOB` (32 bytes, identical to `recovery_manifest.enc`)

## 3. Step-by-Step Mathematical Walkthrough
1. Load `cyberleek_screen.png` using Pillow and access pixel data.
2. Read 4 bytes at pixel indices $\text{offset} + (2 \cdot i) \cdot \text{stride}$ and $\text{offset} + (2 \cdot i + 1) \cdot \text{stride}$ for $i \in [0, 3]$ to obtain length $L$.
3. Extract subsequent $L$ bytes and decode to UTF-8 text.
4. Parse `IV: IV_CYBERLEEK_2026` and `BLOB: <HEX_STRING>`.

## 4. Complete Python Solver Script
```python
#!/usr/bin/env python3
"""
Admin Verification Solver — Level 2.3
"""
import re
from pathlib import Path
from PIL import Image

img_path = Path(__file__).resolve().parent.parent.parent / "user" / "level3" / "files" / "cyberleek_screen.png"
if not img_path.exists():
    img_path = Path("user/level3/files/cyberleek_screen.png")

img = Image.open(img_path).convert("RGBA")
pixels = img.load()
width, height = img.size

OFFSET = 0x1A4
STRIDE = 7

def read_byte_at(pair_idx: int) -> int:
    idx0 = OFFSET + (pair_idx * 2) * STRIDE
    idx1 = OFFSET + (pair_idx * 2 + 1) * STRIDE
    x0, y0 = idx0 % width, idx0 // width
    x1, y1 = idx1 % width, idx1 // width
    _, _, b0, a0 = pixels[x0, y0]
    _, _, b1, a1 = pixels[x1, y1]
    low_nibble = (b0 & 0x03) | ((a0 & 0x03) << 2)
    high_nibble = (b1 & 0x03) | ((a1 & 0x03) << 2)
    return low_nibble | (high_nibble << 4)

length_bytes = bytes([read_byte_at(i) for i in range(4)])
payload_len = int.from_bytes(length_bytes, "big")

payload_raw = bytes([read_byte_at(4 + i) for i in range(payload_len)])
payload_str = payload_raw.decode("utf-8")
print(f"[+] Extracted Stego Payload:\n{payload_str}")

iv_match = re.search(r"IV:\s*(\S+)", payload_str)
blob_match = re.search(r"BLOB:\s*([0-9a-fA-F]+)", payload_str)
assert iv_match and blob_match

iv_str = iv_match.group(1)
blob_hex = blob_match.group(1)
stage4_blob = bytes.fromhex(blob_hex)

assert iv_str == "IV_CYBERLEEK_2026"
assert len(stage4_blob) == 32
print(f"[+] Successfully verified Level 2.3 extraction!")
```

## 5. Security & Validation Checklist
- [x] Generator builds artifact cleanly via `generate_level3.py`.
- [x] Automated single-click tools (`zsteg`, `steghide`, `binwalk`) fail due to non-unit stride and multi-channel interleaving.
- [x] Zero plaintext flags leaked in image file data.
