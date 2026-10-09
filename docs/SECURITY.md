# PhishTrace Security & Privacy Policy

## Security Model

PhishTrace is built on defensive, local-first security principles.

### 1. Attachment and Script Sandboxing
- Email attachments are analyzed strictly statically: filenames, extension risks, file size thresholds, and SHA-256 cryptographic digests.
- Attachments, macros, scripts, and embedded executables are **never executed**.
- HTML email bodies undergo regex sanitization stripping `<script>`, `<iframe>`, `<object>`, `<embed>`, inline event handlers (`onload`, `onclick`), and `javascript:` URLs before display in the SOC preview.

### 2. Privacy & Network Boundary Isolation
- **Private Subnets:** Internal network infrastructure (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `::1`) is never leaked to external geolocation APIs.
- **Gmail OAuth Scopes:** Only the minimum read-only scope (`https://www.googleapis.com/auth/gmail.readonly`) is used. PhishTrace never asks for write, send, delete, or modify permissions.

### 3. Open-Source AI Prompt Defense
- Analyzed email content is treated as untrusted data.
- System prompts isolate email bodies from control instructions to neutralize indirect prompt injection attacks attempting to alter threat classifications.

### 4. Cryptographic Evidence Integrity
- Hashes are calculated over exact immutable bytes using Python's `hashlib.sha256`.
- Manifest verification detects any tampering in stored database records.
