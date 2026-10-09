# PhishTrace Architecture & Technical Contract

**Platform:** PhishTrace — AI Email Threat Detection, Geolocation & Forensic Intelligence Platform  
**Event:** Hacktoberfest Hack Day Bengaluru 2026 | Team Dark  

---

## 1. System Architecture Overview

PhishTrace is structured as a typed modular monolith designed for sub-second email forensic triage, RFC-standard parsing, cryptographic evidence hashing, and explainable Open-Source AI reasoning.

```
+-----------------------------------------------------------------------------------+
|                            PhishTrace SOC Frontend                                |
|  React 19 + TypeScript + Vite + Tailwind CSS + Lucide Icons + Leaflet Hop Mapping  |
+-----------------------------------------+-----------------------------------------+
                                          | JSON over REST (Vite Reverse Proxy)
                                          v
+-----------------------------------------------------------------------------------+
|                            PhishTrace FastAPI Backend                             |
|                                                                                   |
|  [RFC 5322 MIME Parser]               [Threat Scoring Engine]                     |
|  * email & policy.default             * Multi-vector non-linear weights (0-100)    |
|  * SHA-256 raw evidence digest        * MITRE ATT&CK Tactic Mapping               |
|                                                                                   |
|  [Header & Relay Hop Forensics]       [Open-Source AI Threat Layer]               |
|  * Chronological Received hop chain   * Gemma 4 / Gemma 2 Open Weights (HuggingFace/Groq)|
|  * Strict RFC1918 Private IP exclusion* Built-in Zero-Latency Deterministic NLP    |
|  * Candidate origin attribution       * Interactive SOC Co-Pilot (YARA / M365)    |
|                                                                                   |
|  [Evidence Vault & Integrity]         [Threat Campaign Correlator]                |
|  * SHA-256 verification of manifests  * Shared IOC Entity Graph                   |
|  * Exportable PDF dossiers (fpdf2)    * Adversary Persona Profiling               |
|  * Append-only SOC audit log          * Automated Threat Clustering               |
+-----------------------------------------------------------------------------------+
```

---

## 2. Forensic Guarantees & Contracts

1. **Deterministic Grounding:**  
   LLM opinions never dictate or overwrite quantitative risk scores. The threat engine calculates an explainable baseline score from 0–100 across orthogonal security vectors:
   - Authentication alignment (SPF, DKIM, DMARC, ARC)
   - Impersonation signals (Executive display name vs freemail sender, From vs Reply-To diversion)
   - Malicious URLs (Naked IP-literals, brand typosquatting, anchor display mismatches, abusive TLDs)
   - Weaponized attachments (.exe, .xlsm macros, double extensions, suspicious SHA-256 hashes)
   - Psychological intent triggers (BEC financial requests, urgent wire transfers, account termination lures)

2. **RFC1918 Private IP Isolation:**  
   All internal, loopback, link-local, and reserved IP subnets (e.g. `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`) are strictly isolated and never transmitted to external geolocation services.

3. **Cryptographic Proof of Chain of Custody:**  
   The platform computes the SHA-256 hex digest of raw message bytes immediately upon ingestion. Stored investigation manifests are signed with a canonical export digest, enabling one-click audit verification that detects even a single altered byte.

4. **Open-Source AI Adaptability:**  
   Supports Gemma 4 and Gemma 2 open weights with live API routing via Groq or Hugging Face serverless, backed by a built-in deterministic open-source cybersecurity NLP engine that requires zero external keys for 100% offline demonstration.
