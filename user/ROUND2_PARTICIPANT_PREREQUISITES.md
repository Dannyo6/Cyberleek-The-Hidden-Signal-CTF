# Round 02: Participant Environment & Tooling Prerequisites
**Participant Guidelines & Environment Preparation**

> [!NOTE]
> **Participant Tooling Guide:** This guide details the recommended software packages, libraries, and tools to analyze the forensic evidence files locally.

---

## 1. Operational Architecture & Competition Guidelines

Round 02 (**EVIDENCE 02: WHAT THE IMAGE REMEMBERED — The Hidden Signal**) is engineered strictly as a **Static-File Forensic Investigation**:

- **Local Problem Solving:** All challenges in Round 02 are solved offline on your local machine using the downloaded challenge evidence files.
- **No Remote Shell / No SSH:** No SSH credentials, target servers, or remote shells are required.
- **No Attacker / Target Infrastructure:** No vulnerable network instances, virtual machines, or target services are provisioned for this round.
- **No File Uploads:** Participants do not upload files, exploit payloads, or binaries to the CTF server.
- **Zero Server Code Execution:** No participant code executes on the CTF server infrastructure.
- **Minimal Server Surface:** The central CTF platform only serves static read-only evidence files and accepts the final flag string submission (`CYBERLEEK{...}`).

---

## 2. Recommended Operating Environment

- **Operating System:** Kali Linux, Ubuntu 22.04/24.04 LTS, Debian, macOS, or WSL2 (Windows Subsystem for Linux).
- **Network Access:** Standard HTTPS access to the central CTF web portal to download initial evidence files and submit the final flag.

---

## 3. Recommended Participant Tooling Checklist

Participants are strongly advised to pre-install and verify the following standard security and forensics tools before the competition begins:

| Tool | Purpose / Category | Typical Command / Usage |
| :--- | :--- | :--- |
| **Python 3** | Scripting, mathematical analysis, frequency analysis, custom decoding scripts | `python3 -V` / `python3 script.py` |
| **Pillow (PIL)** | Python imaging library for pixel-level bit-plane, color channel, and multi-channel LSB analysis | `pip install Pillow` |
| **cryptography** | Python library for cryptographic primitives and cipher decryption | `pip install cryptography` |
| **CyberChef** | Multi-purpose encoding/decoding, hex transforms, data recipes | Web app / Local standalone offline build |
| **xxd / hexdump** | Hexadecimal dump extraction, raw binary inspection, and hex reverse reconstruction | `xxd -r -p input.hex output.bin` |

---

## 4. Verification of Challenge Artifacts

During the competition, participants should verify downloaded artifacts against the official SHA-256 checksums:

```bash
# Initially distributed player files:
sha256sum dev_leak_chat.txt
sha256sum traffic_intercept.hex
sha256sum cyberleek_screen.png
```

---

## 5. Competition Submission Policy

1. **Final Flag Format:** The final competition flag follows the format `CYBERLEEK{...}`.
2. **Intermediate Keys:** Levels 2.1–2.3 yield intermediate credentials used locally to advance through the investigation chain.
3. **Case Sensitivity:** Submissions are strictly case-sensitive.
4. **Submission Cooldown:** A mandatory **30-second cooldown** is enforced by the central CTF platform after every submission attempt.
5. **Disqualification Limit:** A maximum of **10 incorrect attempts** is permitted cumulatively across the team before disqualification on the central platform.
