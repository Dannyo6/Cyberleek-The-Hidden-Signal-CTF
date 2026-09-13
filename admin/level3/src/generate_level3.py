#!/usr/bin/env python3
"""
Generator for Level 3: Developer Screen Steganography
Domain: Steganography (Hard)
Theme: CYBERLEEK — August 2026 GTA VI Developer Asset Leak

Generates:
  - admin/level3/uploads/cyberleek_screen.png
  - user/level3/files/cyberleek_screen.png
Visual: Authentic GTA VI Vice City style debug wireframe / developer screen (1280x720 RGBA)
Embedding:
  - 2-bit LSB interleaved across Blue and Alpha channels
  - Stride = 7 pixels
  - Offset = 0x1A4 (420 decimal)
Payload:
  - 32-bit big-endian length prefix
  - Structured text payload recovering:
      IV: IV_CYBERLEEK_2026
      BLOB: <hex-encoded STAGE4_BLOB>
"""

import hashlib
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = Path(__file__).resolve().parent
LEVEL_DIR = SCRIPT_DIR.parent
ADMIN_DIR = LEVEL_DIR.parent
ROUND2_DIR = ADMIN_DIR.parent

UPLOADS_DIR = LEVEL_DIR / "uploads"
USER_FILES_DIR = ROUND2_DIR / "user" / "level3" / "files"
OUTPUT_FILENAME = "cyberleek_screen.png"

# Steganography parameters specified by Level 2
OFFSET = 0x1A4  # 420
STRIDE = 7

# Import generate_level4 from admin/level4/src
LEVEL4_SRC = ADMIN_DIR / "level4" / "src"
if str(LEVEL4_SRC) not in sys.path:
    sys.path.insert(0, str(LEVEL4_SRC))

import generate_level4

IV_VECTOR = "IV_CYBERLEEK_2026"
KEY_TOKEN = "LEEK_STREAM_KEY_8080"
TARGET_FLAG = "CYBERLEEK{H1dd3n_4@S}"

WIDTH, HEIGHT = 1280, 720


def _get_font(size: int):
    candidates = [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_developer_screen() -> Image.Image:
    """Generates an authentic GTA VI Vice City developer debug screen."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(14, 10, 26, 255))
    draw = ImageDraw.Draw(img)

    # Perspective Grid lines (Synthwave / Vice City style)
    horizon_y = 420
    y = horizon_y
    step = 4
    while y < HEIGHT:
        alpha = int(100 + 155 * ((y - horizon_y) / (HEIGHT - horizon_y)))
        draw.line([(0, y), (WIDTH, y)], fill=(0, 210, 255, alpha), width=1)
        step += 3
        y += step

    cx = WIDTH // 2
    for x in range(-WIDTH, 2 * WIDTH, 64):
        draw.line([(cx, horizon_y), (x, HEIGHT)], fill=(200, 0, 220, 110), width=1)

    # Neon wireframe geometric buildings
    buildings = [
        (80, 240, 180, 420),
        (200, 180, 320, 420),
        (340, 280, 420, 420),
        (860, 220, 960, 420),
        (980, 160, 1120, 420),
        (1140, 260, 1220, 420),
    ]
    for x1, y1, x2, y2 in buildings:
        draw.rectangle([x1, y1, x2, y2], outline=(0, 240, 255, 180), width=2)
        for sub_y in range(y1 + 30, y2, 30):
            draw.line([(x1, sub_y), (x2, sub_y)], fill=(0, 180, 220, 90), width=1)
        for sub_x in range(x1 + 30, x2, 30):
            draw.line([(sub_x, y1), (sub_x, y2)], fill=(0, 180, 220, 90), width=1)

    # 3D Debug Coordinate Axes Wireframe at Center
    axes_center = (cx, 280)
    draw.line([axes_center, (cx, axes_center[1] - 80)], fill=(0, 255, 100, 230), width=3)
    draw.line([axes_center, (cx + 90, axes_center[1] + 35)], fill=(255, 50, 50, 230), width=3)
    draw.line([axes_center, (cx - 75, axes_center[1] + 45)], fill=(50, 120, 255, 230), width=3)

    draw.text((cx - 5, axes_center[1] - 100), "+Y", fill=(0, 255, 100, 230), font=_get_font(12))
    draw.text((cx + 100, axes_center[1] + 35), "+X", fill=(255, 50, 50, 230), font=_get_font(12))
    draw.text((cx - 95, axes_center[1] + 45), "+Z", fill=(50, 120, 255, 230), font=_get_font(12))

    # Debug Wireframe bounding box around center object
    draw.rectangle([cx - 100, 200, cx + 100, 360], outline=(255, 0, 128, 180), width=1)

    # HUD Developer Telemetry Text
    font_large = _get_font(20)
    font_mono = _get_font(13)

    draw.text((25, 20), "PROJECT AMERICAS // GTA VI INTERNAL DEV BUILD 2026.08.15", fill=(255, 255, 255, 240), font=font_large)
    draw.text((25, 48), "BRANCH: dev/vice_city_sector04_wireframe | TARGET: PS5_PRO / XSX / PC", fill=(0, 240, 255, 200), font=font_mono)
    draw.text((25, 68), "RENDERER: VULKAN-NEXT // COLOR: RGBA8_UNORM // SHADING: WIREFRAME_OVERLAY", fill=(180, 180, 200, 180), font=font_mono)

    draw.text((WIDTH - 350, 20), "TELEMETRY: LIVE STREAMING", fill=(0, 255, 150, 240), font=font_large)
    draw.text((WIDTH - 350, 48), "FRAME_RATE: 119.82 FPS (0.41ms)", fill=(0, 240, 255, 200), font=font_mono)
    draw.text((WIDTH - 350, 68), "VRAM_ALLOC: 14.82 GB / 24.00 GB", fill=(180, 180, 200, 180), font=font_mono)
    draw.text((WIDTH - 350, 88), "STREAM_ID: VCS-ALPHA-RELAY-8080", fill=(255, 0, 128, 200), font=font_mono)

    draw.text((25, HEIGHT - 55), "DEV CAM: POS[-1042.4, 28.1, 485.3] ROT[0.0, -11.2, 45.0] FOV: 75.0", fill=(200, 200, 220, 200), font=font_mono)
    draw.text((25, HEIGHT - 35), "WATERMARK: $CYBERLEEK LEAK FORENSICS // EVIDENCE ITEM 02 // RESTRICTED", fill=(255, 0, 128, 220), font=font_mono)

    draw.text((WIDTH - 320, HEIGHT - 35), "CONFIDENTIAL // DO NOT DISTRIBUTE", fill=(255, 80, 80, 200), font=font_mono)

    return img


def embed_stego_payload(base_img: Image.Image, payload: bytes) -> Image.Image:
    """
    Embeds payload across Blue and Alpha channels using 2-bit LSB interleaving.
    Offset = 0x1A4 (420), Stride = 7 pixels.
    """
    img = base_img.copy()
    pixels = img.load()
    width, height = img.size
    total_pixels = width * height

    data_to_embed = len(payload).to_bytes(4, "big") + payload
    num_bytes = len(data_to_embed)
    required_pixels = num_bytes * 2

    last_pixel_idx = OFFSET + (required_pixels - 1) * STRIDE
    if last_pixel_idx >= total_pixels:
        raise ValueError(f"Payload too large: requires {last_pixel_idx} pixels, capacity is {total_pixels}")

    pixel_cursor = 0
    for byte_val in data_to_embed:
        low_nibble = byte_val & 0x0F
        high_nibble = (byte_val >> 4) & 0x0F

        idx0 = OFFSET + pixel_cursor * STRIDE
        x0, y0 = idx0 % width, idx0 // width
        r0, g0, b0, a0 = pixels[x0, y0]
        b0 = (b0 & 0xFC) | (low_nibble & 0x03)
        a0 = (a0 & 0xFC) | ((low_nibble >> 2) & 0x03)
        pixels[x0, y0] = (r0, g0, b0, a0)
        pixel_cursor += 1

        idx1 = OFFSET + pixel_cursor * STRIDE
        x1, y1 = idx1 % width, idx1 // width
        r1, g1, b1, a1 = pixels[x1, y1]
        b1 = (b1 & 0xFC) | (high_nibble & 0x03)
        a1 = (a1 & 0xFC) | ((high_nibble >> 2) & 0x03)
        pixels[x1, y1] = (r1, g1, b1, a1)
        pixel_cursor += 1

    return img


def extract_stego_payload(img: Image.Image) -> bytes:
    """Extracts the embedded byte payload."""
    pixels = img.load()
    width, height = img.size

    def read_byte_at_pixel_pair(p_pair_idx: int) -> int:
        idx0 = OFFSET + (p_pair_idx * 2) * STRIDE
        idx1 = OFFSET + (p_pair_idx * 2 + 1) * STRIDE
        x0, y0 = idx0 % width, idx0 // width
        x1, y1 = idx1 % width, idx1 // width
        _, _, b0, a0 = pixels[x0, y0]
        _, _, b1, a1 = pixels[x1, y1]
        low_nibble = (b0 & 0x03) | ((a0 & 0x03) << 2)
        high_nibble = (b1 & 0x03) | ((a1 & 0x03) << 2)
        return low_nibble | (high_nibble << 4)

    length_bytes = bytearray()
    for i in range(4):
        length_bytes.append(read_byte_at_pixel_pair(i))
    payload_len = int.from_bytes(length_bytes, "big")

    payload = bytearray()
    for i in range(payload_len):
        payload.append(read_byte_at_pixel_pair(4 + i))

    return bytes(payload)


def generate_challenge():
    """Generates cyberleek_screen.png for both uploads/ and user/level3/files/."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    USER_FILES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Obtain Stage 4 Blob from generate_level4
    stage4_blob = generate_level4.encrypt_stage4(KEY_TOKEN, IV_VECTOR, TARGET_FLAG)
    stage4_blob_hex = stage4_blob.hex().upper()

    # 2. Construct structured payload
    payload_text = f"""[CYBERLEEK_STAGE4_PAYLOAD]
IV: {IV_VECTOR}
BLOB: {stage4_blob_hex}
"""
    payload_bytes = payload_text.encode("utf-8")

    # 3. Create base developer screen image
    base_img = create_developer_screen()

    # 4. Embed payload into Blue/Alpha 2-bit LSB planes
    stego_img = embed_stego_payload(base_img, payload_bytes)

    # 5. Save to both destinations
    targets = [UPLOADS_DIR / OUTPUT_FILENAME, USER_FILES_DIR / OUTPUT_FILENAME]
    sha256_hash = ""
    for target in targets:
        stego_img.save(target, format="PNG", optimize=False)
        file_size = target.stat().st_size
        sha256_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        rel_path = target.relative_to(ROUND2_DIR)
        print(f"[+] Successfully generated Level 3 artifact:")
        print(f"    Path:   {rel_path}")
        print(f"    Size:   {file_size} bytes")
        print(f"    SHA256: {sha256_hash}")

    # 6. Self-test extraction
    extracted_bytes = extract_stego_payload(stego_img)
    assert extracted_bytes == payload_bytes, "Self-test extraction failed!"
    assert IV_VECTOR.encode("utf-8") in extracted_bytes, "IV missing from extracted payload!"
    assert stage4_blob_hex.encode("utf-8") in extracted_bytes, "Blob missing from extracted payload!"

    return sha256_hash


if __name__ == "__main__":
    generate_challenge()
