# Level 2.2 — Intercepted Developer Stream Telemetry

> **"The original disappeared. The pixels didn't."**

## Case Brief
Following the initial asset leaks in August 2026, network monitoring taps captured an encrypted packet stream emitted by the GTA VI developer relay server (`10.240.16.88:8080`) during an internal memory cache sync. The intercepted data was captured as raw hexadecimal bytes (`traffic_intercept.hex`).

## Objective
Analyze the intercepted stream dump, implement the synchronous stream XOR decryption algorithm driven by the 32-bit Linear Congruential Generator (LCG), and recover the steganography extraction parameters for the carrier asset.

## Downloadable Artifact
Download the artifact from the `files/` directory:
- `traffic_intercept.hex`

## What To Recover
Recover the steganography parameters needed to analyze the image in Level 2.3:
- Target color channels and bit-depth
- Pixel Offset
- Pixel Stride

## Operational Directives
- The Key Token (`key_token`) and Seed (`seed_hex`) recovered from Level 2.1 are strictly required to initialize the LCG state.
- Decrypting the stream requires a custom Python script or mathematical implementation of the PRNG keystream.
- Perform all processing locally on your forensic environment.

---

## Tiered Hints

### Hint 1 — Light
Convert the hexadecimal text from `traffic_intercept.hex` into raw binary bytes. Review the header annotations in the evidence file—the encryption is a synchronous stream XOR cipher using a 32-bit Linear Congruential Generator (LCG).

### Hint 2 — Medium
The LCG parameters are standard 32-bit values:
$$X_{n+1} = (1664525 \cdot X_n + 1013904223) \pmod{2^{32}}$$
For each step, the keystream byte is extracted from the upper 16 bits of the state:
$$\text{byte} = (X_{n+1} \gg 16) \ \& \ 0\text{xFF}$$
To initialize $X_0$, start with the base seed integer decoded from Level 1 (`int(seed_hex, 16)`), and update the state sequentially for each byte in the Level 1 Key Token (`key_token`) using a polynomial rolling hash:
$$\text{state} = (\text{state} \cdot 31 + \text{byte}) \pmod{2^{32}}$$

### Hint 3 — Strong
Here is the core Python logic for the LCG keystream and XOR decryption:

```python
# Use intermediate credentials recovered from Level 2.1:
# seed_hex = "0x..." 
# key_token = "LEEK_STREAM_KEY_..."

state = int(seed_hex, 16)
for b in key_token.encode("utf-8"):
    state = (state * 31 + b) & 0xFFFFFFFF

keystream = bytearray()
for _ in range(len(ciphertext_bytes)):
    state = (1664525 * state + 1013904223) & 0xFFFFFFFF
    keystream.append((state >> 16) & 0xFF)

plaintext = bytes([c ^ k for c, k in zip(ciphertext_bytes, keystream)])
print(plaintext.decode("utf-8"))
```
The decrypted plaintext will specify the target carrier image and exact steganography extraction parameters (channels, offset, stride).
