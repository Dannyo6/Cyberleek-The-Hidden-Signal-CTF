# Level 2.1 — Leaked Developer Communications

> **"The original disappeared. The pixels didn't."**

## Case Brief
In August 2026, internal communications and unreleased developer builds for GTA VI were intercepted following a security breach linked to $CYBERLEEK. Digital forensics teams recovered a Discord/IRC build review log (`dev_leak_chat.txt`) from an internal development channel. The developers discuss asset packaging, internal debug metrics, and reference obfuscated stream validation credentials.

## Objective
Analyze the intercepted chat log, reverse the classical cryptographic obfuscation applied to the verification payload, and extract two critical stream parameters:
1. **Key Token** (`LEEK_STREAM_KEY_*`)
2. **Seed** (`0x*`)

## Downloadable Artifact
Download the artifact from the `files/` directory:
- `dev_leak_chat.txt`

## What To Recover
Recover the Key Token string and Seed value. These intermediate credentials are required to decrypt the subsequent network telemetry stream in Level 2.2.

## Operational Directives
- The chat log includes operational dialogue from the developers regarding the cipher structure.
- Examine both stages of the transformation: the Polybius substitution coordinates and the columnar transposition.
- All analysis should be conducted locally on your workstation. No external network connections or live services are required.

---

## Tiered Hints

### Hint 1 — Light
Read the conversation between `vance_lead` and `j_marston_net` carefully. The developers state that the message underwent a two-step cipher: a 6x6 Polybius matrix followed by a Columnar Transposition keyed by their target city codename (`VICE`).

### Hint 2 — Medium
To invert the encryption, you must reverse the operations in reverse order:
1. **Reverse Columnar Transposition first:** The keyword is `VICE` (length 4). The alphabetical order of the letters is `C` (index 2), `E` (index 3), `I` (index 1), `V` (index 0). Divide the total ciphertext digits (72 digits) by the key length (4) to get 18 rows. Reconstruct the 4 columns and read them row-by-row.
2. **Reverse Polybius substitution second:** Group the resulting digits into 2-digit coordinate pairs `(row, col)`.

### Hint 3 — Strong
Construct the 6x6 Polybius grid as described in the chat:
- 25 letters (A–Z with I and J merged into a single cell)
- 10 digits (0–9)
- Underscore `_` in cell (6, 6)

```python
grid = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'K', 'L', 'M'],
    ['N', 'O', 'P', 'Q', 'R', 'S'],
    ['T', 'U', 'V', 'W', 'X', 'Y'],
    ['Z', '0', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_'],
]
```
For each digit pair `(r, c)` where `r, c ∈ [1, 6]`, lookup `grid[r-1][c-1]`. The resulting text will reveal both the Key Token and the hexadecimal Seed value.
