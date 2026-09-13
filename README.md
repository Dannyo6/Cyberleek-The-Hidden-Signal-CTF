# Round 02: What the Image Remembered // The Hidden Signal
**Campaign Arc:** *CYBERLEEK: The Internet Never Forgets*  
**Domain & Techniques:** Steganography + Applied Cryptography (Bit-Plane Extraction, Stream Keystream XOR, Balanced Feistel Block Cipher in CBC Mode, Polybius Substitution, Columnar Transposition)  
**Timeline & Incident:** August 2026 GTA VI Unreleased Developer Asset Leak  
**Difficulty Level:** Medium–Hard (Sequential 4-Stage Forensic Investigation Chain)  
**Target Solve Time:** 35–45 minutes (Requires custom Python automation; single-click GUI tools fail by design)  
**Authoritative Final Flag:** `CYBERLEEK{H1dd3n_4@S}`  
**Transition Quote:** *"You found the signal. Now find the system that carried it."*  
**Tagline:** *"The original disappeared. The pixels didn't."*

---

## Executive Summary & Challenge Overview

```
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗     ███████╗███████╗██╗  ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔════╝██╔════╝██║ ██╔╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     █████╗  █████╗  █████╔╝ 
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║     ██╔══╝  ██╔══╝  ██╔═██╗ 
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████╗███████╗███████╗██║  ██╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                    EVIDENCE 02 // THE HIDDEN SIGNAL
```

Round 02 immerses participants in a high-stakes forensic investigation following the catastrophic **August 2026 developer asset leak** of *Grand Theft Auto VI*, orchestrated by the underground collective **$CYBERLEEK**. Unlike conventional security breaches involving raw database dumps, $CYBERLEEK exfiltrated early Vice City developer debug wireframes containing an active, multi-layer telemetry exfiltration signal.

The challenge is structured as a **strictly decoupled, four-stage cryptographic and steganographic investigation chain**. Participants cannot skip levels or brute-force intermediate states: every level uncovers specific intermediate keys, mathematical seeds, or extraction coordinates required to unlock and decode the subsequent forensic evidence artifact, culminating in the recovery of the authoritative CTF token:

$$\text{Canonical Flag: } \mathbf{CYBERLEEK\{H1dd3n\_4@S\}}$$

---

## Narrative Briefing: The $CYBERLEEK Incident

In mid-August 2026, an unreleased developer debug render from the *Project Americas* build pipeline (GTA VI Vice City Sector 04 Wireframe) surfaced across decentralized bulletin boards and peer-to-peer relay caches. The asset leak was claimed by threat actor **$CYBERLEEK**.

```
[03:18:22] <vance_lead> Internal debug metrics: GPU draw calls 4,821, VRAM load 14.8GB...
[03:19:45] <j_marston_net> Did you update the developer network telemetry authentication?
[03:20:12] <vance_lead> Yes. The stream validator requires two security parameters:
                        1. Key Token (LEEK_STREAM_KEY_*)
                        2. LCG Seed (0x*)
[03:21:30] <vance_lead> Obfuscated using our classic two-stage cipher:
                        Step 1: 6x6 Polybius matrix (A-Z with I/J combined, 0-9, and '_').
                        Step 2: Columnar transposition using target city codename 'VICE'.
```

Initial triage by incident response teams revealed:
1. **Developer Discord/IRC Logs (`dev_leak_chat.txt`):** Internal build engineers discussed obfuscating stream validation credentials using classical composition ciphers to prevent plaintext leakage across monitored internal bridges.
2. **Network Memory Cache Dumps (`traffic_intercept.hex`):** A packet capture dump taken from an internal memory cache sync relay (`NET-CAP-8080`) containing telemetry encrypted with a Linear Congruential Generator keystream.
3. **Developer Wireframe Render (`cyberleek_screen.png`):** A $1280 \times 720$ 32-bit RGBA developer HUD debug screenshot concealing low-order bit-plane telemetry across non-standard pixel strides and offsets.
4. **Encrypted Manifest Package (`recovery_manifest.enc`):** An encrypted 32-byte binary blob protected by a custom 16-round balanced Feistel block cipher in CBC mode containing the final developer case resolution token.

---

## Architectural Decoupling & Scaffolding Tree

Round 02 adheres to an **airtight administrative and participant architectural separation**. Participant distribution bundles contain zero organizer scripts, zero solutions, and zero plaintext flags.

```
Round-2-CTF/
├── .gitignore                                  # Git ignore rules protecting build artifacts
├── README.md                                   # Comprehensive production CTF manual & architecture
├── round2.md                                   # Challenge specification & operational guidelines
│
├── admin/                                      # ORGANIZER OPERATIONS (INTERNAL ONLY)
│   ├── PRODUCTION_SUBMISSION_RULES.md          # Platform rate limiting, scoring & disqualification rules
│   ├── build_bundles.py                        # Automated packaging script with zero-leak audit
│   ├── evidence_bundle.zip                     # Pre-packaged, validated participant distribution zip
│   ├── test_round2_chain.py                    # 12-test automated end-to-end verification test suite
│   │
│   ├── level1/                                 # Level 2.1 Admin Suite (Polybius + Transposition)
│   │   ├── main.md                             # Organizer reference walkthrough & verification solver
│   │   ├── src/
│   │   │   └── generate_level1.py              # Level 2.1 deterministic artifact generator
│   │   └── uploads/
│   │       └── dev_leak_chat.txt               # Verification copy of Level 2.1 evidence
│   │
│   ├── level2/                                 # Level 2.2 Admin Suite (32-bit LCG Stream XOR)
│   │   ├── main.md                             # Organizer reference walkthrough & verification solver
│   │   ├── src/
│   │   │   └── generate_level2.py              # Level 2.2 deterministic artifact generator
│   │   └── uploads/
│   │       └── traffic_intercept.hex           # Verification copy of Level 2.2 evidence
│   │
│   ├── level3/                                 # Level 2.3 Admin Suite (Blue/Alpha LSB Stego)
│   │   ├── main.md                             # Organizer reference walkthrough & verification solver
│   │   ├── src/
│   │   │   └── generate_level3.py              # Level 2.3 wireframe generator & stego embedder
│   │   └── uploads/
│   │       └── cyberleek_screen.png            # Verification copy of Level 2.3 carrier image
│   │
│   └── level4/                                 # Level 2.4 Admin Suite (16-Round Feistel CBC)
│       ├── main.md                             # Organizer reference walkthrough & verification solver
│       ├── src/
│       │   └── generate_level4.py              # Level 2.4 Feistel CBC cipher engine & manifest generator
│       └── uploads/
│           ├── recovery_manifest.enc           # Verification copy of Level 2.4 encrypted manifest
│           └── stage4_validation.json          # Cryptographic validation metadata & hashes
│
└── user/                                       # PARTICIPANT DISTRIBUTION BUNDLE (PUBLIC)
    ├── ROUND2_PARTICIPANT_PREREQUISITES.md     # Participant environment checklist & competition rules
    │
    ├── level1/                                 # Level 2.1 Participant Release
    │   ├── challenge.md                        # Level 2.1 briefing & investigation objective
    │   └── files/
    │       └── dev_leak_chat.txt               # Level 2.1 evidence file
    │
    ├── level2/                                 # Level 2.2 Participant Release
    │   ├── challenge.md                        # Level 2.2 briefing & investigation objective
    │   └── files/
    │       └── traffic_intercept.hex           # Level 2.2 evidence file
    │
    ├── level3/                                 # Level 2.3 Participant Release
    │   ├── challenge.md                        # Level 2.3 briefing & investigation objective
    │   └── files/
    │       └── cyberleek_screen.png            # Level 2.3 carrier evidence file (1280x720 RGBA)
    │
    └── level4/                                 # Level 2.4 Participant Release
        ├── challenge.md                        # Level 2.4 briefing & investigation objective
        └── files/
            └── recovery_manifest.enc           # Level 2.4 encrypted manifest file
```

### Component Responsibility Matrix

| Path | Audience | Security Policy | Primary Function |
| :--- | :--- | :--- | :--- |
| `admin/levelX/src/` | Organizers | Restricted | Houses deterministic Python generators for all challenge assets. |
| `admin/levelX/main.md` | Organizers | Restricted | Contains comprehensive mathematical explanations and complete solver scripts. |
| `admin/test_round2_chain.py` | Organizers | Restricted | Automated test harness validating all 12 test assertions against `user/`. |
| `admin/build_bundles.py` | Organizers | Restricted | Builds `evidence_bundle.zip` and performs automated AST/string leak checks. |
| `user/levelX/challenge.md` | Participants | Public | Level narrative context, evidence file pointers, and investigation goals. |
| `user/levelX/files/` | Participants | Public | Raw cryptographic and steganographic challenge artifacts. |

---

## Technical Pipeline Matrix

The investigation proceeds through four strictly coupled cryptographic transitions:

```mermaid
flowchart TD
    subgraph L1 ["Level 2.1: Leaked Developer Chat"]
        A1["dev_leak_chat.txt"] --> B1["Revert Columnar Transposition (Key: 'VICE')"]
        B1 --> C1["6x6 Polybius Grid Coordinate Lookup"]
        C1 --> D1["Recovered Plaintext: KEY_LEEK_STREAM_KEY_8080_SEED_0X7A3F"]
    end

    subgraph L2 ["Level 2.2: Intercepted Stream Telemetry"]
        D1 --> E2["Key Token: LEEK_STREAM_KEY_8080<br>Seed: 0x7A3F"]
        E2 --> F2["Polynomial Rolling Hash State Init<br>state = (state * 31 + byte) mod 2^32"]
        F2 --> G2["32-bit LCG Keystream Engine<br>X_{n+1} = (1664525 * X_n + 1013904223) mod 2^32"]
        A2["traffic_intercept.hex"] --> H2["Stream Keystream XOR Decryption"]
        G2 --> H2
        H2 --> I2["Decoded Stego Parameters:<br>• Carrier: cyberleek_screen.png<br>• Interleaving: Blue & Alpha 2-bit LSB<br>• Stride: 7 pixels, Offset: 0x1A4 (420)"]
    end

    subgraph L3 ["Level 2.3: Developer Screen Wireframe"]
        I2 --> J3["Pillow RGBA Bit-Plane Extractor"]
        A3["cyberleek_screen.png"] --> J3
        J3 --> K3["Low Nibble: Blue[1:0] | (Alpha[1:0] << 2)<br>High Nibble: Blue[1:0] | (Alpha[1:0] << 2)"]
        K3 --> L3["Recovered Payload:<br>• IV Token: IV_CYBERLEEK_2026<br>• Ciphertext: STAGE4_BLOB (32 bytes)"]
    end

    subgraph L4 ["Level 2.4: Core Asset Recovery"]
        E2 --> M4["Key Token: LEEK_STREAM_KEY_8080"]
        L3 --> N4["IV Token: IV_CYBERLEEK_2026"]
        L3 --> O4["Encrypted STAGE4_BLOB / recovery_manifest.enc"]
        M4 & N4 --> P4["SHA-256 Subkey Derivation (16 Rounds)<br>K_r = SHA256(Key || IV || r)[:8]"]
        N4 --> Q4["CBC IV Derivation<br>IV_BLOCK = SHA256(IV)[:16]"]
        P4 & Q4 & O4 --> R4["16-Round Balanced Feistel Decryption (CBC Mode)"]
        R4 --> S4["PKCS7 Unpadding"]
        S4 --> T4["FINAL AUTHORITATIVE CTF FLAG:<br>CYBERLEEK{H1dd3n_4@S}"]
    end
```

### Comprehensive Level Specification Matrix

| Stage | Artifact File | Category | Difficulty | Mathematical & Algorithmic Core | Recovered Yields |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2.1** | `dev_leak_chat.txt` (2,355 B) | Classical Cryptography | Easy / Med | 1. Revert Columnar Transposition (Key `VICE`, len 4, order $C \rightarrow 1, E \rightarrow 2, I \rightarrow 3, V \rightarrow 0$)<br>2. Invert 6x6 Polybius coordinate square (25 letters, digits 0–9, `_`) | **Key Token:** `LEEK_STREAM_KEY_8080`<br>**Seed:** `0x7A3F` |
| **2.2** | `traffic_intercept.hex` (3,731 B) | Stream Ciphers | Medium | 1. Polynomial key mixing: $\text{state} = (\text{state} \cdot 31 + b) \pmod{2^{32}}$<br>2. 32-bit LCG recurrence: $X_{n+1} = (1664525 \cdot X_n + 1013904223) \pmod{2^{32}}$<br>3. High-entropy keystream extraction: $(X_{n+1} \gg 16) \ \& \ \text{0xFF}$<br>4. Symmetric XOR stream decryption | **Stego Parameters:**<br>- Target: `cyberleek_screen.png`<br>- Interleaving: Blue & Alpha 2-bit LSB<br>- Offset: `0x1A4` (420)<br>- Stride: 7 pixels |
| **2.3** | `cyberleek_screen.png` (59,888 B) | Bit-Plane Steganography | Hard | 1. $1280 \times 720$ RGBA array traversal starting at byte offset $420$, step $7$<br>2. 2-pixel dual-channel byte reconstruction:<br>   - Pixel 0: $(B_0 \ \& \ 3) \mid ((A_0 \ \& \ 3) \ll 2)$<br>   - Pixel 1: $(B_1 \ \& \ 3) \mid ((A_1 \ \& \ 3) \ll 2)$<br>3. Read 4-byte big-endian length prefix $L$, extract $L$ bytes | **IV String:** `IV_CYBERLEEK_2026`<br>**Ciphertext:** `STAGE4_BLOB`<br>(32-byte hex string matching `recovery_manifest.enc`) |
| **2.4** | `recovery_manifest.enc` (32 B) | Modern Cryptography | Hard | 1. 16-round balanced Feistel cipher in CBC mode ($16$-byte blocks, $8$-byte halves)<br>2. Subkey derivation: $K_r = \text{SHA-256}(\text{Key} \parallel \text{IV} \parallel r\text{.to\_bytes(2, 'big')})[:8]$<br>3. Feistel round: $F(R, K_r) = \text{SHA-256}(R \parallel K_r)[:8]$<br>4. CBC IV block: $\text{SHA-256}(\text{IV})[:16]$<br>5. PKCS7 unpadding | **Final CTF Flag:**<br>`CYBERLEEK{H1dd3n_4@S}` |

---

## Participant Walkthrough & Solving Guide

### Environment Setup & Prerequisites

Participants require a standard Python 3.10+ security forensics environment. Install the necessary packages via `pip`:

```bash
pip install Pillow pycryptodome numpy
```

Verify your Python environment:
```bash
python -c "import PIL, Crypto, numpy; print('[+] Environment verification successful!')"
```

---

### Step 1: Solving Level 2.1 — Leaked Developer Chat

#### 1. Forensic Analysis
Examine `user/level1/files/dev_leak_chat.txt`. The chat dialogue reveals that build engineers obfuscated an asset validation token using a two-stage classical cipher:
1. A **6x6 Polybius matrix** mapping the characters `A–Z` (with `I` and `J` combined), `0–9`, and an underscore `_` located at row 6, column 6.
2. A **Columnar Transposition** cipher using the target city codename `VICE`.

The encrypted payload block contains 72 digits arranged in groups of 4:
```text
3515 3165 4236 4141 1546 5241 1515 5452 4633 4636 1546 5446 3636 3315 2515 3333 4515 5452
```

#### 2. Mathematical Inversion
1. **Transposition Inversion:**
   - Transposition keyword: `VICE` (Length $K = 4$).
   - Total characters: $N = 72$ digits $\implies R = 72 / 4 = 18$ rows.
   - Alphabetical sort order of `VICE`:
     - Index 0 (`V`): 4th in alphabet (Rank 3)
     - Index 1 (`I`): 2nd in alphabet (Rank 1)
     - Index 2 (`C`): 1st in alphabet (Rank 0)
     - Index 3 (`E`): 3rd in alphabet (Rank 2)
   - Reading order of ciphertext columns: Column 2 (`C`), Column 3 (`E`), Column 1 (`I`), Column 0 (`V`).
   - Slicing the 72 digits into 4 chunks of 18 digits allows reassembling the 18 rows.

2. **Polybius Coordinate Substitution:**
   - Group the 72 reassembled digits into 36 coordinate pairs $(r, c)$ where $r, c \in [1, 6]$.
   - Look up coordinates in the 6x6 Polybius grid:
     $$\begin{pmatrix}
     \text{A} & \text{B} & \text{C} & \text{D} & \text{E} & \text{F} \\
     \text{G} & \text{H} & \text{I/J} & \text{K} & \text{L} & \text{M} \\
     \text{N} & \text{O} & \text{P} & \text{Q} & \text{R} & \text{S} \\
     \text{T} & \text{U} & \text{V} & \text{W} & \text{X} & \text{Y} \\
     \text{Z} & \text{0} & \text{1} & \text{2} & \text{3} & \text{4} \\
     \text{5} & \text{6} & \text{7} & \text{8} & \text{9} & \text{\_}
     \end{pmatrix}$$
   - Coordinate pair `(2, 4)` maps to row 2, col 4: `K`.
   - The decoded plaintext resolves to:
     ```text
     KEY_LEEK_STREAM_KEY_8080_SEED_0X7A3F
     ```

#### 3. Python Solver (`solve_level1.py`)
```python
#!/usr/bin/env python3
import re
from pathlib import Path

chat_path = Path("user/level1/files/dev_leak_chat.txt")
with open(chat_path, "r", encoding="utf-8") as f:
    chat_text = f.read()

match = re.search(r"ENCRYPTED BUILD VALIDATION PAYLOAD:\s*\n-+\s*\n(.*?)\n-+", chat_text, re.DOTALL)
if not match:
    raise ValueError("Payload block not found in chat log")

ciphertext = match.group(1).replace(" ", "").replace("\n", "").strip()

key = "VICE"
num_cols = len(key)
num_rows = len(ciphertext) // num_cols
key_order = sorted(range(len(key)), key=lambda i: key[i])

cols = {}
pos = 0
for col_idx in key_order:
    cols[col_idx] = ciphertext[pos : pos + num_rows]
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

plaintext = "".join(decoded_chars)
print(f"[+] Decrypted Level 1 Payload: {plaintext}")
# Recovered yields:
# Key Token: LEEK_STREAM_KEY_8080
# Seed:      0x7A3F
```

---

### Step 2: Solving Level 2.2 — Intercepted Stream Telemetry

#### 1. Forensic Analysis
`user/level2/files/traffic_intercept.hex` contains raw hex-encoded packets from a developer relay session. The header specifies that the stream is encrypted with a **Linear Congruential Generator (LCG) keystream XOR cipher**:
- Recurrence: $X_{n+1} = (1664525 \cdot X_n + 1013904223) \pmod{2^{32}}$
- Keystream byte extraction: $\text{byte} = (X_{n+1} \gg 16) \ \& \ \text{0xFF}$
- Seed Initialization: The base state starts with `0x7A3F`. Each byte of `LEEK_STREAM_KEY_8080` is mixed using a polynomial rolling hash:
  $$\text{state}_{i+1} = (\text{state}_i \cdot 31 + \text{byte}) \pmod{2^{32}}$$

#### 2. Mathematical Inversion
1. Parse the hex dump into binary ciphertext bytes.
2. Initialize 32-bit state: $X_0 = 31295$ (`0x7A3F`).
3. Iterate over the UTF-8 bytes of `"LEEK_STREAM_KEY_8080"` and apply the polynomial hash.
4. Advance the LCG for each byte of ciphertext, extracting the high 8 bits of the upper 16-bit entropy.
5. Compute plaintext byte $P_i = C_i \oplus K_i$.

#### 3. Python Solver (`solve_level2.py`)
```python
#!/usr/bin/env python3
import re
from pathlib import Path

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

# Polynomial state mixing
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
print("[+] Decrypted Stream Telemetry:\n")
print(plaintext)
```

**Recovered Plaintext Stream Telemetry:**
```text
[CYBERLEEK NETWORK TELEMETRY INTERCEPT // AUG 2026]
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
```

---

### Step 3: Solving Level 2.3 — Developer Screen Steganography

#### 1. Forensic Analysis
Standard steganography tools (`zsteg`, `steghide`, `binwalk`, `strings`) fail because:
1. **Non-Zero Offset:** Embedding begins at pixel offset $420$ (`0x1A4`).
2. **Non-Unit Stride:** Pixels are sampled every $7\text{th}$ pixel.
3. **Multi-Channel Interleaving:** Every byte is partitioned across two pixels and two color channels:
   - **Pixel 0 (Low Nibble):** Blue bits [1:0] store bits [1:0]; Alpha bits [1:0] store bits [3:2].
   - **Pixel 1 (High Nibble):** Blue bits [1:0] store bits [5:4]; Alpha bits [1:0] store bits [7:6].
4. **Length Prefix:** A 4-byte big-endian integer defines the length of the hidden payload.

#### 2. Reconstruction Logic
$$\text{Pixel 0 Low Nibble: } N_L = (B_0 \ \& \ 3) \mid ((A_0 \ \& \ 3) \ll 2)$$
$$\text{Pixel 1 High Nibble: } N_H = (B_1 \ \& \ 3) \mid ((A_1 \ \& \ 3) \ll 2)$$
$$\text{Byte Value: } \text{Byte} = N_L \mid (N_H \ll 4)$$

#### 3. Python Solver (`solve_level3.py`)
```python
#!/usr/bin/env python3
import re
from pathlib import Path
from PIL import Image

img_path = Path("user/level3/files/cyberleek_screen.png")
img = Image.open(img_path).convert("RGBA")
pixels = img.load()
width, height = img.size

OFFSET = 0x1A4  # 420
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

# 1. Read 4-byte big-endian payload length
length_bytes = bytes([read_byte_at(i) for i in range(4)])
payload_len = int.from_bytes(length_bytes, "big")
print(f"[+] Extracted Payload Length: {payload_len} bytes")

# 2. Extract payload string
payload_raw = bytes([read_byte_at(4 + i) for i in range(payload_len)])
payload_str = payload_raw.decode("utf-8")
print(f"[+] Extracted Payload:\n{payload_str}")

# 3. Parse IV and STAGE4_BLOB
iv_match = re.search(r"IV:\s*(\S+)", payload_str)
blob_match = re.search(r"BLOB:\s*([0-9a-fA-F]+)", payload_str)
assert iv_match and blob_match

iv_str = iv_match.group(1)
stage4_blob = bytes.fromhex(blob_match.group(1))

print(f"[+] Successfully Recovered IV:   {iv_str}")
print(f"[+] Successfully Recovered Blob: {stage4_blob.hex().upper()} ({len(stage4_blob)} bytes)")
```

**Recovered Stego Payload:**
```text
[CYBERLEEK_STAGE4_PAYLOAD]
IV: IV_CYBERLEEK_2026
BLOB: A107048F523A14C3DBF34516BA6BB087805C9967AAA05A165B9DC0FF83209AAB
```

---

### Step 4: Solving Level 2.4 — Core Asset Recovery Manifest

#### 1. Forensic Analysis
`user/level4/files/recovery_manifest.enc` (or the 32-byte `STAGE4_BLOB` extracted from Level 2.3) is protected by a 16-round balanced Feistel block cipher operating in Cipher Block Chaining (CBC) mode:
- **Block Size:** 16 bytes (split into 8-byte halves $L$ and $R$).
- **Subkey Derivation:** For rounds $r \in [0, 15]$:
  $$K_r = \text{SHA-256}(\text{"LEEK\_STREAM\_KEY\_8080"} \parallel \text{"IV\_CYBERLEEK\_2026"} \parallel r\text{.to\_bytes(2, 'big')})[:8]$$
- **Round Function:**
  $$F(R, K_r) = \text{SHA-256}(R \parallel K_r)[:8]$$
- **Feistel Network:**
  - Forward: $L_{i+1} = R_i$, $R_{i+1} = L_i \oplus F(R_i, K_i)$
  - Reverse (Decryption): Identical network evaluated with round keys in reverse sequence: $K_{15}, K_{14}, \dots, K_0$.
- **CBC Initialization Vector:**
  $$\text{IV\_BLOCK} = \text{SHA-256}(\text{"IV\_CYBERLEEK\_2026"})[:16]$$
- **Padding:** Standard PKCS7 padding.

#### 2. Python Solver (`solve_level4.py`)
```python
#!/usr/bin/env python3
import hashlib
from pathlib import Path

manifest_path = Path("user/level4/files/recovery_manifest.enc")
ciphertext = manifest_path.read_bytes()

KEY_TOKEN = "LEEK_STREAM_KEY_8080"
IV_STRING = "IV_CYBERLEEK_2026"

# 1. Derive 16 round subkeys
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

# 2. Derive CBC IV Block
iv_block = hashlib.sha256(IV_STRING.encode("utf-8")).digest()[:16]

# 3. Decrypt in CBC Mode using reversed keys
reversed_keys = list(reversed(round_keys))
plaintext = bytearray()
prev = iv_block

for i in range(0, len(ciphertext), 16):
    block = ciphertext[i : i + 16]
    dec = feistel_block(block, reversed_keys)
    plaintext.extend(bytes(x ^ y for x, y in zip(dec, prev)))
    prev = block

# 4. Remove PKCS7 padding
pad_len = plaintext[-1]
flag = plaintext[:-pad_len].decode("utf-8")

print("=" * 60)
print(f"[+] FINAL CTF FLAG RECOVERED: {flag}")
print("=" * 60)
assert flag == "CYBERLEEK{H1dd3n_4@S}"
```

---

### Master End-to-End Solve Script

For rapid automated verification of the entire investigation chain, save and execute `solve_round2_all.py`:

```python
#!/usr/bin/env python3
"""
CYBERLEEK EVIDENCE 02 // MASTER PARTICIPANT END-TO-END SOLVER
Executes the full 4-stage forensic solve chain against user/ files.
Asserts authoritative flag: CYBERLEEK{H1dd3n_4@S}
"""
import hashlib
import re
from pathlib import Path
from PIL import Image

USER_DIR = Path("user")

# --- STAGE 1: Leaked Developer Chat ---
print("[*] Stage 1: Decoding dev_leak_chat.txt...")
chat_text = (USER_DIR / "level1/files/dev_leak_chat.txt").read_text(encoding="utf-8")
cipher_digits = re.search(r"ENCRYPTED BUILD VALIDATION PAYLOAD:\s*\n-+\s*\n(.*?)\n-+", chat_text, re.DOTALL).group(1).replace(" ", "").replace("\n", "").strip()

key = "VICE"
num_cols = len(key)
num_rows = len(cipher_digits) // num_cols
cols = {}
pos = 0
for col_idx in sorted(range(len(key)), key=lambda i: key[i]):
    cols[col_idx] = cipher_digits[pos : pos + num_rows]
    pos += num_rows

digits_str = "".join("".join(cols[c][r] for c in range(num_cols)) for r in range(num_rows))
polybius = [
    ['A', 'B', 'C', 'D', 'E', 'F'], ['G', 'H', 'I', 'K', 'L', 'M'],
    ['N', 'O', 'P', 'Q', 'R', 'S'], ['T', 'U', 'V', 'W', 'X', 'Y'],
    ['Z', '0', '1', '2', '3', '4'], ['5', '6', '7', '8', '9', '_'],
]
l1_plain = "".join(polybius[int(digits_str[i])-1][int(digits_str[i+1])-1] for i in range(0, len(digits_str), 2))
key_token = "LEEK_STREAM_KEY_8080"
seed_hex = "0x7A3F"
assert key_token in l1_plain and "0X7A3F" in l1_plain
print(f"    [+] Level 1 Yields -> Key Token: {key_token}, Seed: {seed_hex}")

# --- STAGE 2: Intercepted Stream Telemetry ---
print("\n[*] Stage 2: Decrypting traffic_intercept.hex...")
hex_content = (USER_DIR / "level2/files/traffic_intercept.hex").read_text(encoding="utf-8")
l2_cipher = bytes.fromhex(re.search(r"ENCRYPTED TELEMETRY STREAM \(HEX\):\s*\n-+\s*\n(.*?)\n-+", hex_content, re.DOTALL).group(1).replace(" ", "").replace("\n", ""))

state = int(seed_hex, 16)
for b in key_token.encode("utf-8"):
    state = (state * 31 + b) & 0xFFFFFFFF
keystream = bytearray()
for _ in range(len(l2_cipher)):
    state = (1664525 * state + 1013904223) & 0xFFFFFFFF
    keystream.append((state >> 16) & 0xFF)

l2_plain = bytes([c ^ k for c, k in zip(l2_cipher, keystream)]).decode("utf-8")
assert "0x1A4" in l2_plain and "7 pixels" in l2_plain
offset = 0x1A4
stride = 7
print(f"    [+] Level 2 Yields -> Offset: {hex(offset)}, Stride: {stride}, Blue/Alpha 2-bit LSB")

# --- STAGE 3: Developer Screen Wireframe ---
print("\n[*] Stage 3: Extracting stego payload from cyberleek_screen.png...")
img = Image.open(USER_DIR / "level3/files/cyberleek_screen.png").convert("RGBA")
pixels = img.load()
w, _ = img.size

def read_byte(pair_idx):
    i0, i1 = offset + (pair_idx * 2) * stride, offset + (pair_idx * 2 + 1) * stride
    _, _, b0, a0 = pixels[i0 % w, i0 // w]
    _, _, b1, a1 = pixels[i1 % w, i1 // w]
    return ((b0 & 3) | ((a0 & 3) << 2)) | (((b1 & 3) | ((a1 & 3) << 2)) << 4)

p_len = int.from_bytes(bytes([read_byte(i) for i in range(4)]), "big")
payload = bytes([read_byte(4 + i) for i in range(p_len)]).decode("utf-8")
recovered_iv = re.search(r"IV:\s*(\S+)", payload).group(1)
recovered_blob = bytes.fromhex(re.search(r"BLOB:\s*([0-9a-fA-F]+)", payload).group(1))
assert recovered_iv == "IV_CYBERLEEK_2026"
print(f"    [+] Level 3 Yields -> IV: {recovered_iv}, STAGE4_BLOB: {len(recovered_blob)} bytes")

# --- STAGE 4: Final Feistel Synthesis ---
print("\n[*] Stage 4: Synthesizing Feistel Block Cipher in CBC mode...")
round_keys = [hashlib.sha256(key_token.encode() + recovered_iv.encode() + r.to_bytes(2, "big")).digest()[:8] for r in range(16)]

def feistel(b, keys):
    L, R = b[:8], b[8:]
    for k in keys:
        L, R = R, bytes(x ^ y for x, y in zip(L, hashlib.sha256(R + k).digest()[:8]))
    return R + L

iv_block = hashlib.sha256(recovered_iv.encode()).digest()[:16]
plain = bytearray()
prev = iv_block
for i in range(0, len(recovered_blob), 16):
    blk = recovered_blob[i : i + 16]
    plain.extend(bytes(x ^ y for x, y in zip(feistel(blk, list(reversed(round_keys))), prev)))
    prev = blk

flag = plain[:-plain[-1]].decode("utf-8")
print("\n" + "=" * 65)
print(f">>> [SUCCESS] FINAL CANONICAL FLAG: {flag} <<<")
print("=" * 65)
assert flag == "CYBERLEEK{H1dd3n_4@S}"
```

---

## Organizer & Admin Operations

### 1. Deterministic Challenge Asset Regeneration

Organizers can deterministically regenerate all challenge assets from scratch. Generators write identical copies to `admin/levelX/uploads/` and `user/levelX/files/`:

```bash
# From the repository root:
python admin/level1/src/generate_level1.py
python admin/level2/src/generate_level2.py
python admin/level4/src/generate_level4.py
python admin/level3/src/generate_level3.py
```

> [!NOTE]
> **Generation Order Dependency:** `generate_level4.py` must run before `generate_level3.py` because Level 3 dynamically imports and encrypts `STAGE4_BLOB` into the carrier image `cyberleek_screen.png`.

---

### 2. Zero-Leak Participant Bundle Packaging

To package the player distribution archive `admin/evidence_bundle.zip`, execute `build_bundles.py`:

```bash
cd admin
python build_bundles.py
```

The script automatically executes:
1. Fresh regeneration of all 4 challenge levels in sequence.
2. Zip packaging of `user/` artifacts into `admin/evidence_bundle.zip`.
3. Automated AST and string inspection to enforce zero organizer leaks (scans for `admin`, `main.md`, `generate`, `solution`, `test`, and plaintext flag leaks).

#### Packaging Output:
```text
======================================================================
CYBERLEEK EVIDENCE 02 // ADMIN REPRODUCIBLE BUILD & PACKAGING PIPELINE
======================================================================

[*] Step 1: Running Level 1 Generator (generate_level1.py)...
[+] Successfully generated Level 1 artifact:
    Path:   admin/level1/uploads/dev_leak_chat.txt (2355 bytes)
    Path:   user/level1/files/dev_leak_chat.txt (2355 bytes)

[*] Step 2: Running Level 2 Generator (generate_level2.py)...
[+] Successfully generated Level 2 artifact:
    Path:   admin/level2/uploads/traffic_intercept.hex (3731 bytes)
    Path:   user/level2/files/traffic_intercept.hex (3731 bytes)

[*] Step 3: Running Level 4 Generator (generate_level4.py)...
[+] Successfully generated Level 4 artifact:
    Path:   admin/level4/uploads/recovery_manifest.enc (32 bytes)
    Path:   user/level4/files/recovery_manifest.enc (32 bytes)

[*] Step 4: Running Level 3 Generator (generate_level3.py)...
[+] Successfully generated Level 3 artifact:
    Path:   admin/level3/uploads/cyberleek_screen.png (59888 bytes)
    Path:   user/level3/files/cyberleek_screen.png (59888 bytes)

[*] Step 5: Packaging participant distribution bundle from user/...
    [+] Packaged: ROUND2_PARTICIPANT_PREREQUISITES.md (3470 bytes)
    [+] Packaged: level1/challenge.md (2858 bytes)
    [+] Packaged: level1/files/dev_leak_chat.txt (2355 bytes)
    [+] Packaged: level2/challenge.md (2899 bytes)
    [+] Packaged: level2/files/traffic_intercept.hex (3731 bytes)
    [+] Packaged: level3/challenge.md (3458 bytes)
    [+] Packaged: level3/files/cyberleek_screen.png (59888 bytes)
    [+] Packaged: level4/challenge.md (3751 bytes)
    [+] Packaged: level4/files/recovery_manifest.enc (32 bytes)
[+] Total files packaged: 9

[*] Step 6: Performing strict zero-leak audit of evidence_bundle.zip...

[+] Bundle Built & Audited Successfully!
    Bundle Path:   admin/evidence_bundle.zip
    Bundle Size:   67979 bytes
======================================================================
```

---

### 3. Automated Test Suite Verification

Run the full 12-test validation suite to verify cryptographic chain integrity, zero shortcut vulnerabilities, and canonical flag recovery:

```bash
cd admin
python test_round2_chain.py
```

#### Verbatim Test Suite Results:
```text
===========================================================================
CYBERLEEK: EVIDENCE 02 — THE HIDDEN SIGNAL // AUTOMATED TEST SUITE
===========================================================================

[*] Step 0: Regenerating fresh challenge assets across all 4 levels...
[+] Clean isolated test directory initialized with user/ artifacts.

===========================================================================
TEST ID    | STATUS | NOTES
---------------------------------------------------------------------------
TEST 1     | PASS   | Recovered Key Token: 'LEEK_STREAM_KEY_8080', Seed: '0x7A3F'
TEST 2     | PASS   | Level 2 fails cleanly with incorrect/trivial LCG seeds
TEST 3     | PASS   | Recovered Stego Parameters (Offset=0x1a4, Stride=7, Blue/Alpha 2-bit)
TEST 4     | PASS   | Stego extraction with default/incorrect parameters yields invalid payload
TEST 5     | PASS   | Extracted IV: 'IV_CYBERLEEK_2026' and Blob (32 bytes)
TEST 6     | PASS   | Zero plaintext flag or IV leaked in cyberleek_screen.png file data
TEST 7     | PASS   | Level 4 Feistel decryption strictly rejects invalid keys and IVs
TEST 8     | PASS   | Flag strictly matches: 'CYBERLEEK{H1dd3n_4@S}'
TEST 9     | PASS   | recovery_manifest.enc matches Level 3 blob and cleanly decrypts to flag
TEST 10    | PASS   | Zero legacy references across all 21 challenge files
TEST 11    | PASS   | evidence_bundle.zip verified: complete user files, zero admin leaks
TEST 12    | PASS   | All 5 challenge artifacts verified with SHA-256
===========================================================================

>>> ALL 12 TESTS PASSED! CYBERLEEK ROUND 2 READY FOR PRODUCTION <<<
>>> AUTHORITATIVE FLAG: CYBERLEEK{H1dd3n_4@S} <<<
```

---

### 4. Authoritative Submission & Platform Scoring Rules

As specified in `admin/PRODUCTION_SUBMISSION_RULES.md`, all flag validation and submission tracking are enforced **authoritatively by the central CTF platform backend**:

1. **Scoring Breakdown:**
   - **Level 2.1:** 100 Points
   - **Level 2.2:** 150 Points
   - **Level 2.3:** 200 Points
   - **Level 2.4:** 250 Points
   - **Total Cumulative Round Score:** **700 Points**
2. **Submission Cooldown:** A strict **30-second cooldown** is enforced per team after every flag attempt (whether correct or incorrect). Spammed requests during cooldown return HTTP `429 Too Many Requests` without penalty.
3. **Disqualification Policy:** A cumulative ceiling of **10 incorrect submissions** across Round 02 results in permanent team disqualification (`403 Forbidden`).
4. **Server Attack Surface:** Round 02 is **strictly static-file based**. No participant code executes on the CTF server, no SSH instances exist, and no file uploads are permitted.

---

## Authoritative Flag Reference & Cryptographic Checksums

### Canonical Flag
```text
CYBERLEEK{H1dd3n_4@S}
```
- **Flag SHA-256:** `22fbffbe465eb1a473f32aa68c07e0b57e79c2980c6913c2db7639f7ebad1ea6`

### Artifact SHA-256 Hashes
```text
fd1d7144d223ecd6328c5f145593d08066663c10783a5e2e167f2a48f17dbbfd  user/level1/files/dev_leak_chat.txt
833d8368bc594f7eccf6d8d498263159c57b625fe2f46870b0df7a9d456a3d89  user/level2/files/traffic_intercept.hex
9ecd26c3005b8a92a388d434b858e7284acca415b102476a844f83bf359d51dd  user/level3/files/cyberleek_screen.png
a107048f523a14c3dbf34516ba6bb087805c9967aaa05a165b9dc0ff83209aab  user/level4/files/recovery_manifest.enc
```

---

> *"You found the signal. Now find the system that carried it."*
