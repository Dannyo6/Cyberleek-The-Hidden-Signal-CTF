# Level 2.4 — Final Asset Recovery

> **"The original disappeared. The pixels didn't."**

## Case Brief
All cryptographic fragments recovered from the August 2026 CYBERLEEK GTA VI leak have now converged:
- **Level 2.1:** Key Token (`key_token` string)
- **Level 2.3:** Vector Identifier (`iv_token` string)
- **Level 2.3 / 2.4:** Encrypted Asset Manifest (`recovery_manifest.enc`)

The developer build system protects the core recovery manifest using a 16-round Feistel-style block cipher in Cipher Block Chaining (CBC) mode.

## Objective
Unmask the encrypted binary payload in `recovery_manifest.enc` by implementing the Feistel CBC decryption network with the recovered Key Token and IV, and recover the authoritative Round 2 CTF flag: `CYBERLEEK{...}`.

## Downloadable Artifact
Download the artifact from the `files/` directory:
- `recovery_manifest.enc` (matches the binary payload `STAGE4_BLOB` extracted from `cyberleek_screen.png`)

## What To Submit
The complete, authoritative CTF flag string:
`CYBERLEEK{...}`

## Operational Directives
- Cipher architecture: 16-round balanced Feistel network with 16-byte blocks (8-byte left and right half-blocks) in CBC mode.
- Subkey generation: For each round $r \in [0, 15]$, subkey $K_r$ is derived via `SHA-256(Key_Token + IV_String + r.to_bytes(2, 'big'))[:8]`.
- Round function: $F(R, K_r) = \text{SHA-256}(R + K_r)[:8]$.
- CBC IV block: `SHA-256(IV_String)[:16]`.
- Plaintext utilizes standard PKCS7 padding.
- Submit the recovered flag directly to the central CTF platform.

---

## Tiered Hints

### Hint 1 — Light
The artifact `recovery_manifest.enc` contains raw binary ciphertext (32 bytes). Its content matches the `STAGE4_BLOB` extracted from `cyberleek_screen.png`. To decrypt it, you need:
1. Key Token recovered from Level 2.1
2. IV Token recovered from Level 2.3

### Hint 2 — Medium
The cipher is a balanced Feistel network with 16-byte blocks (split into two 8-byte halves: $L$ and $R$):
- **Round keys:** 16 subkeys of 8 bytes each:
  $$K_r = \text{SHA-256}(\text{key} \parallel \text{iv} \parallel r\text{.to\_bytes(2, 'big')})[:8]$$
- **Round function:** $F(R, K_r) = \text{SHA-256}(R \parallel K_r)[:8]$
- In a Feistel network, decryption uses the exact same round function as encryption, but with the subkeys applied in reverse order ($K_{15} \dots K_0$).
- In CBC mode, XOR the output of each decrypted block with the previous ciphertext block (or the 16-byte IV block `SHA-256(iv)[:16]` for the first block).

### Hint 3 — Strong
Here is the complete Feistel CBC decryption algorithm in Python:

```python
import hashlib
from pathlib import Path

# Use the tokens recovered from Level 2.1 and Level 2.3:
# key = "LEEK_STREAM_KEY_..."
# iv = "IV_CYBERLEEK_..."

ciphertext = Path("recovery_manifest.enc").read_bytes()

# 1. Derive 16 subkeys
round_keys = [
    hashlib.sha256(key.encode() + iv.encode() + r.to_bytes(2, "big")).digest()[:8]
    for r in range(16)
]

def feistel_block(block: bytes, keys: list) -> bytes:
    L, R = block[:8], block[8:]
    for k in keys:
        F = hashlib.sha256(R + k).digest()[:8]
        L, R = R, bytes(x ^ y for x, y in zip(L, F))
    return R + L

# 2. CBC Decryption
iv_block = hashlib.sha256(iv.encode()).digest()[:16]
plaintext = bytearray()
prev = iv_block

for i in range(0, len(ciphertext), 16):
    block = ciphertext[i : i + 16]
    dec = feistel_block(block, list(reversed(round_keys)))
    plaintext.extend(bytes(x ^ y for x, y in zip(dec, prev)))
    prev = block

# 3. PKCS7 unpad
pad_len = plaintext[-1]
flag = plaintext[:-pad_len].decode("utf-8")
print("FLAG:", flag)
```
The recovered flag will match `CYBERLEEK{...}`.
