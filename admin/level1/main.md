# Admin Reference — Level 2.1: Leaked Developer Communications

## 1. Challenge Overview & Metadata
- **Level ID:** 2.1
- **Domain:** Cryptography (Easy / Medium)
- **Storyline:** Leaked GTA VI internal Discord/IRC build review logs leaking debug metrics and obfuscated validation tokens.
- **Player Artifact:** `user/level1/files/dev_leak_chat.txt`
- **Admin Upload:** `admin/level1/uploads/dev_leak_chat.txt`
- **Generator Script:** `admin/level1/src/generate_level1.py`

## 2. Cryptographic Architecture
- **Cipher Mechanics:** Two-stage classical composition:
  1. **6x6 Polybius Matrix Substitution:**
     - 25 letters (A–Z with I/J combined)
     - 10 digits (0–9)
     - 1 symbol: underscore `_` at position (6, 6)
  2. **Columnar Transposition:**
     - Keyword: `VICE` (length 4)
     - Column order determined by alphabetical sort of letters: `C` (2), `E` (3), `I` (1), `V` (0)
- **Target Plaintext:** `KEY_LEEK_STREAM_KEY_8080_SEED_0X7A3F` (36 characters $\rightarrow$ 72 digits)
- **Intermediate Recovered Yields:**
  - **Key Token:** `LEEK_STREAM_KEY_8080`
  - **Seed:** `0x7A3F`

## 3. Step-by-Step Mathematical Walkthrough
1. Extract 72 ciphertext digits from `dev_leak_chat.txt`.
2. Compute row count: $72 / 4 = 18$ rows.
3. Slice ciphertext into 4 column blocks of 18 digits each according to key sort order (`C`, `E`, `I`, `V`).
4. Assemble row-by-row into a 72-digit coordinate stream.
5. Group digits into pairs $(r, c)$ where $r, c \in [1, 6]$.
6. Map pairs via 6x6 Polybius grid:
   ```text
   Row 1: A B C D E F
   Row 2: G H I K L M
   Row 3: N O P Q R S
   Row 4: T U V W X Y
   Row 5: Z 0 1 2 3 4
   Row 6: 5 6 7 8 9 _
   ```
7. Recover plaintext: `KEY_LEEK_STREAM_KEY_8080_SEED_0X7A3F`.

## 4. Complete Python Solver Script
```python
#!/usr/bin/env python3
"""
Admin Verification Solver — Level 2.1
"""
import re
from pathlib import Path

chat_path = Path(__file__).resolve().parent.parent.parent / "user" / "level1" / "files" / "dev_leak_chat.txt"
if not chat_path.exists():
    chat_path = Path("user/level1/files/dev_leak_chat.txt")

with open(chat_path, "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r"ENCRYPTED BUILD VALIDATION PAYLOAD:\s*\n-+\s*\n(.*?)\n-+", text, re.DOTALL)
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

assert "LEEK_STREAM_KEY_8080" in plaintext
assert "0X7A3F" in plaintext.upper()
```

## 5. Security & Validation Checklist
- [x] Generator builds artifact cleanly via `generate_level1.py`.
- [x] Sibling directory `uploads/` receives verification artifact.
- [x] Zero plaintext secrets or flags leaked in metadata or chat dialogue.
- [x] Single-click automated tools fail; custom transposition reversal required.
