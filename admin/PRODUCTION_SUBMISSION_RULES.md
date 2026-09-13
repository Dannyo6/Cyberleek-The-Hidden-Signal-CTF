# Production Flag Submission & Central CTF Platform Security Rules

> [!IMPORTANT]
> **Central CTF Platform Enforcement Only:** The flag validation, rate limiting (30-second cooldown), wrong-attempt tracking (10 attempts max), scoring, authentication, and team disqualification rules documented below are enforced **authoritatively by the CENTRAL CTF PLATFORM backend**, NOT by the Round 2 challenge files.
>
> Round 02 itself is **strictly static-file based** (offline local participant analysis). Participants solve challenges locally using cryptographic and steganographic tools to advance through intermediate keys (Levels 2.1–2.3) and submit the final token (`CYBERLEEK{H1dd3n_4@S}`) to the central CTF platform. No simulation code, frontend layer, or client-side storage exists within the Round 2 challenge package.

---

## 1. Backend Authoritative State Requirements

The backend database must maintain authenticated per-team state with the following fields:

- `team_id` (UUID / string): Authenticated team identity from session token / API key.
- `score` (integer): Authoritative cumulative points earned by the team.
- `solved_challenges` (array / relation of challenge IDs): Challenge IDs correctly solved by the team.
- `wrong_flag_count` (integer): Cumulative count of incorrect flag submission attempts across the competition (0 - 10).
- `next_submit_at` (timestamp / epoch ms): Server timestamp indicating when the team is next permitted to submit a flag (enforces the 30-second rate limiting cooldown).
- `is_disqualified` (boolean): Flag indicating if the team has reached the maximum allowed wrong flag attempts (10 incorrect submissions).
- `disqualified_at` (timestamp, nullable): Server timestamp when the team was disqualified.

---

## 2. Server-Side Submission Handling Workflow

Upon receiving a flag submission request (`POST /api/v1/submit-flag` with payload `{ challenge_id, flag }`):

1. **Authentication & Team Identity Verification:**
   - Verify JWT or session cookie to identify the team. Reject unauthenticated requests with `401 Unauthorized`.

2. **Disqualification Check:**
   - If `team.is_disqualified == true` or `team.wrong_flag_count >= 10`:
     - Reject request immediately with status `403 Forbidden` (`TEAM DISQUALIFIED — Maximum incorrect flag submissions reached.`).

3. **Sequential Challenge Unlock Rules:**
   - Verify that the requested `challenge_id` is unlocked for this team:
     - `2.1` is unlocked by default.
     - `2.2` requires `2.1` in `team.solved_challenges`.
     - `2.3` requires `2.2` in `team.solved_challenges`.
     - `2.4` requires `2.3` in `team.solved_challenges`.
   - If attempting to submit to a locked challenge, reject with `400 Bad Request` (`CHALLENGE LOCKED — Preceding evidence not yet recovered.`).

4. **Rate Limit / 30-Second Cooldown Check:**
   - If `server_time < team.next_submit_at`:
     - Calculate remaining seconds: `Math.ceil((team.next_submit_at - server_time) / 1000)`.
     - Reject immediately with status `429 Too Many Requests` (`SUBMISSION BLOCKED — Submission cooldown active.`).
     - **Do NOT increment `wrong_flag_count`**, do NOT change score, and do NOT extend cooldown.

5. **Set Immediate Submission Cooldown:**
   - Update `team.next_submit_at = server_time + 30 seconds` immediately for the team (regardless of whether the flag is correct or incorrect).

6. **Flag Processing & Validation:**
   - Trim leading and trailing whitespace from the submitted flag string.
   - Perform strict, case-sensitive comparison against the canonical flag hash or secure backend flag secret.
   - Do NOT lowercase the submitted string.

7. **Duplicate Submission Protection & Correct Flag Handling:**
   - If the submitted flag matches:
     - Do **NOT** increment `wrong_flag_count`.
     - If `challenge_id` is already in `team.solved_challenges`:
       - Do **NOT** award duplicate points.
       - Return `200 OK` with `{ success: true, message: "FLAG ACCEPTED (Already solved)" }`.
     - If `challenge_id` is NOT in `team.solved_challenges`:
       - Append `challenge_id` to `team.solved_challenges`.
       - Increment `team.score` by the challenge value (100 for 2.1, 150 for 2.2, 200 for 2.3, 250 for 2.4).
       - Log audit event.
       - Return `200 OK` with `{ success: true, message: "FLAG ACCEPTED — Evidence recovered." }`.

8. **Incorrect Flag Handling & Disqualification Enforcement:**
   - If the submitted flag does NOT match:
     - Increment `team.wrong_flag_count` by 1.
     - If `team.wrong_flag_count >= 10`:
       - Set `team.is_disqualified = true` and `team.disqualified_at = server_time`.
       - Return status `403 Forbidden` with `{ success: false, message: "TEAM DISQUALIFIED — Maximum incorrect flag submissions reached." }`.
     - Else:
       - Return status `400 Bad Request` with `{ success: false, message: "FLAG REJECTED — Continue investigating." }`.

---

## 3. Server Architecture & Attack Surface Minimization

Round 02 is intentionally engineered to have an extremely small and robust server attack surface:

- **Static Read-Only File Distribution:** Challenge assets are hosted via read-only static file storage or CDN.
- **No Remote Shells / No SSH:** No SSH accounts or bastion hosts are provisioned for participants.
- **No Participant Uploads:** The backend does not accept file uploads, multipart form data, or user binaries.
- **No Command Execution:** The backend does not spawn child processes or execute shell commands on behalf of participants.
- **No Vulnerable Shared Services:** No vulnerable microservices or target containers are exposed to competitor traffic.
- **No Dynamic Challenge Generation:** Challenge files are statically pre-generated and cryptographically verified by SHA-256 hashes.
