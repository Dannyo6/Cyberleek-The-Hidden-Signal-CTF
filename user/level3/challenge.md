# Level 2.3 — The Developer Screen / The Hidden Signal

> **"The original disappeared. The pixels didn't."**

## Case Brief
Digital forensics teams recovered an authentic developer screen capture (`cyberleek_screen.png`) originating from the August 2026 GTA VI leak. The image depicts a Vice City wireframe debug session with developer HUD telemetry and 3D coordinate grids. Forensics confirms that binary validation data has been concealed deep within the pixel bit-planes of this carrier file.

## Objective
Implement a custom Python pixel extraction routine using the parameters recovered from Level 2.2 to extract the hidden payload from `cyberleek_screen.png`.

## Downloadable Artifact
Download the artifact from the `files/` directory:
- `cyberleek_screen.png`

## What To Recover
Extract the structured payload and isolate:
1. **IV Vector String:** (`IV_*` format)
2. **Stage 4 Encrypted Blob:** `STAGE4_BLOB` (binary bytes / hex)

## Operational Directives
- Automated single-click tools like `zsteg` or `steghide` will fail because the embedding uses non-standard offset, stride, and multi-channel 2-bit interleaving.
- Use Python with Pillow (`PIL.Image`) to access raw RGBA pixel tuples.
- The carrier format is RGBA (32-bit color). Both Blue and Alpha channels carry data.

---

## Tiered Hints

### Hint 1 — Light
Open `cyberleek_screen.png` using Python's Pillow library (`PIL.Image.open("cyberleek_screen.png").convert("RGBA")`). Do not rely on automated tools like `zsteg` or `stegsolve`, as they assume sequential (stride=1), 1-bit, or single-channel LSB layouts.

### Hint 2 — Medium
The extraction parameters decoded in Level 2.2 specify:
- **Pixel Offset:** The starting pixel index recovered from the telemetry stream
- **Pixel Stride:** The step size between sampled pixels
- **Channels:** Blue and Alpha (2 bits each per pixel, yielding 4 bits / 1 nibble per pixel)
- **Byte Structure:** Every byte requires 2 pixels:
  - First pixel (index `offset + (2*i) * stride`): lower nibble
    - Blue bits [1:0]: `bits [1:0]`
    - Alpha bits [1:0]: `bits [3:2]`
  - Second pixel (index `offset + (2*i + 1) * stride`): upper nibble
    - Blue bits [1:0]: `bits [5:4]`
    - Alpha bits [1:0]: `bits [7:6]`

### Hint 3 — Strong
Here is a Python function to extract bytes directly from the image using the parameters derived in Level 2.2:

```python
from PIL import Image

img = Image.open("cyberleek_screen.png").convert("RGBA")
pixels = img.load()
width, height = img.size

# Use the offset and stride recovered from Level 2.2:
# offset = int("0x...", 16)
# stride = ...

def read_byte(p_idx):
    idx0 = offset + (p_idx * 2) * stride
    idx1 = offset + (p_idx * 2 + 1) * stride
    x0, y0 = idx0 % width, idx0 // width
    x1, y1 = idx1 % width, idx1 // width
    _, _, b0, a0 = pixels[x0, y0]
    _, _, b1, a1 = pixels[x1, y1]
    low_nibble = (b0 & 0x03) | ((a0 & 0x03) << 2)
    high_nibble = (b1 & 0x03) | ((a1 & 0x03) << 2)
    return low_nibble | (high_nibble << 4)

# First 4 bytes indicate the payload length (big-endian)
length_bytes = bytes([read_byte(i) for i in range(4)])
length = int.from_bytes(length_bytes, "big")

# Read payload
payload = bytes([read_byte(4 + i) for i in range(length)]).decode("utf-8")
print(payload)
```
The decoded payload contains the initialization vector (`IV_*`) and the hex-encoded ciphertext blob for Level 2.4.
