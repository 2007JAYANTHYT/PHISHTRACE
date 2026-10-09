# PhishTrace — AI Email Threat Detection, Geolocation & Forensic Intelligence Platform

> **Hacktoberfest Hack Day Bengaluru 2026 | Team Dark**  
> *An Open-Source Cyber Threat Intelligence, RFC-Standard Forensics, and Open-Weights AI Operations Center.*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](backend/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?logo=fastapi&logoColor=white)](backend/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg?logo=react&logoColor=black)](frontend/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?logo=typescript&logoColor=white)](frontend/)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA_NIM-Open_Weights_Cloud-76B900.svg?logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![Open Source AI](https://img.shields.io/badge/Open_Source_AI-5_Model_Consensus_Ensemble-8B5CF6.svg)](https://ai.google.dev/gemma)

---

## Executive Summary

**PhishTrace** is a full-stack, demo-ready cybersecurity operations platform that ingests, parses, traces, and analyzes suspicious email messages using deterministic forensic heuristics corroborated by **5 Open-Source and Open-Weight AI Architectures** (Google Gemma 2, Meta Llama 3.2 on NVIDIA NIM, Mistral 7B, Alibaba Qwen 2.5, and PhishTrace Cyber Forensics Engine).

Designed for incident responders, SOC analysts, and security researchers, PhishTrace delivers explainable risk scores (0–100), hop-by-hop relay attribution on an interactive world map, cryptographic SHA-256 evidence chain-of-custody verification, automated YARA/KQL/Splunk/Sigma/M365 defensive rule synthesis, multi-model consensus evaluation, an interactive prompt sandbox, and threat campaign correlation.

---

## 5 Open-Source & Open-Weight LLM Architecture

PhishTrace natively supports and runs top open-weight models without mandatory paid API keys or bulky local weight downloads:

| Model | Architecture | Role & Specialty | Context Window | Mode |
| :--- | :--- | :--- | :--- | :--- |
| **Meta Llama 3.2 11B** (`meta/llama-3.2-11b-vision-instruct`) | Llama 3.2 Open Weights | High-throughput reasoning accelerated on NVIDIA NIM | 128K Tokens | NVIDIA NIM Active Cloud |
| **Google Gemma 2 9B** (`google/gemma-2-9b-it`) | Gemma Open Weights | Grounded intent extraction, structured JSON threat summary | 8K Tokens | Open Weights / Cloud / Local Fallback |
| **Mistral 7B Instruct v0.3** (`mistralai/Mistral-7B-Instruct-v0.3`) | Sliding Window Attention | Ultra-fast token parsing, payload hazard classification | 32K Tokens | Open Weights / Cloud / Local Fallback |
| **Alibaba Qwen 2.5 7B** (`qwen/qwen-2.5-7b-instruct`) | Dense Code Specialist | YARA syntax rules, Sentinel KQL hunting, regex extraction | 32K Tokens | Open Weights / Cloud / Local Fallback |
| **PhishTrace Cyber Engine** (`phishtrace/cyber-forensics-nlp`) | Deterministic Rule Engine | Sub-millisecond RFC header forensic parsing & scoring | Unlimited | Built-in Zero-Latency Engine |

---

## Key Capabilities

### 1. Explainable Threat Detection & Risk Scoring
- Multi-vector non-linear threat scoring (0–100) across 4 standard categories:
  - **Low (0–24)** | **Guarded (25–49)** | **High (50–74)** | **Critical (75–100)**
- Grounded in deterministic security rules:
  - Executive VIP display name impersonation sent via consumer freemail
  - Deceptive `Reply-To` vs `From` diversion
  - Raw IP-literal URL hosts and typosquatted lookalike domains (`xn--`, `.top`, `.xyz`)
  - Misleading anchor text display (`<a href="evil.com">bank.com</a>`)
  - Weaponized macro attachments (`.xlsm`, double extensions, payload hashes)
  - Business Email Compromise (BEC) urgency, routing change, and wire transfer pretexts

### 2. Multi-Model LLM Consensus (5 Models)
- Evaluates email threats in parallel across 5 distinct open-weight models.
- **Agreement Percentage Gauge:** Measures inter-model agreement (e.g. 100% Agreement) to eliminate single-model hallucinations and subjective bias.
- **Model Cards Grid & Consensus Matrix:** Side-by-side comparison of threat verdict, risk score, confidence %, analytical reasoning, grounded evidence anchor quotes, and inference latency.

### 3. Interactive SOC AI Co-Pilot Assistant
- Conversational SOC incident assistant running live in the browser.
- One-click automated synthesis of:
  - **RFC 5322 Compliant YARA Detection Rules**
  - **Microsoft Sentinel / Defender KQL Threat Hunting Queries**
  - **Splunk SPL Incident Correlation Searches**
  - **Sigma Generic Detection Rules (YAML)**
  - **Microsoft 365 Exchange Online Transport (Mail Flow) Rules** (PowerShell)
  - **Executive CISO Incident Advisories**

### 4. SOC LLM Prompt Studio & Experimentation Sandbox
- Located in the **Settings** view.
- Allows analysts to test custom queries against any open-source model.
- Includes pre-built prompt presets:
  - 🎯 *Extract Attack IOCs & C2 Signatures*
  - 🛡️ *Synthesize Microsoft Sentinel KQL Hunting Rule*
  - 📜 *Draft Executive CISO Cyber Advisory*
  - 🧠 *Deceptive Pretext & Psychological Trigger Analysis*
  - 🔍 *Generate High-Fidelity YARA Rules*
- Email context anchoring to test real-world scenarios.

### 5. Header & Authentication Forensics with Hop-by-Hop Origin Tracing
- Full RFC 5322 MIME extraction of `Received:` relay hops in reverse chronological order.
- Clear distinction between **observed inbound gateway headers** and **cryptographically verified author signatures**.
- **RFC1918 Private IP Isolation:** Internal enterprise subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`) are strictly isolated and never transmitted to public geolocation services.
- Earliest candidate public IP identified with explicit attribution confidence and legal/forensic caveats regarding forged headers and VPN relays.
- Interactive Leaflet world map with hop trajectory and timeline fallback.

### 6. Threat Campaign Intelligence & Adversary Profiling
- Entity correlation linking related incidents into threat clusters:
  - **Apex BEC & Executive Wire Fraud Syndicate**
  - **ShadowGate Credential Harvesting Network**
  - **False Academic Grant & Advance-Fee Syndicate**
- Interactive visual graph connecting Campaign Hubs, Incident Nodes, Malicious Domains, Destination URLs, and Relay IPs.
- **AI Campaign Adversary Profiler:** Generates threat actor dossiers and hunting playbooks powered by open-weight LLMs.

### 7. Forensic Evidence Vault & SHA-256 Integrity
- Every analysis generates an immutable investigation record with the original raw file SHA-256 digest and canonical manifest export hash.
- **Verify Hash Action:** Real-time cryptographic recalculation that detects any tampering or modification down to a single byte.
- **Downloadable PDF Investigation Dossier:** Clean, formatted incident reports generated on-the-fly via `fpdf2`.
- **Append-Only SOC Audit Log:** Chronological ledger of all capture and verification events.

### 8. Gmail Read-Only OAuth Integration
- Official Google OAuth 2.0 flow isolated to the minimum read-only scope:
  `https://www.googleapis.com/auth/gmail.readonly`
- Never asks for permission to send, delete, quarantine, or modify user mail.
- Truthful connection reporting: When unconfigured, the app runs completely offline with `.eml` upload and synthetic seed data.

---

## Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Launch Backend
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*Backend initializes SQLite database and seeds 6 realistic threat intelligence emails automatically.*

### 2. Launch Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend opens at `http://localhost:5173` with full API proxy to backend.*

---

## Verification & Testing

Backend test suite verifying RFC parsing, size limits, threat engine scoring, evidence hashing, RFC1918 isolation, and LLM endpoints:
```bash
cd backend
python -m pytest tests -v
```
*11/11 tests pass in ~0.50s.*

Frontend production build verification:
```bash
cd frontend
npm run build
```
*Vite compiles client bundle with 0 errors in ~300ms.*

---

## Synthetic Dataset Samples

Located in `samples/`:
- `sample_1_legit_corporate.eml` — Legitimate Board Meeting Agenda (Low Risk, SPF/DKIM pass)
- `sample_2_scholarship_fee_phish.eml` — Advance-Fee Fellowship Scam (Guarded Risk)
- `sample_3_urgent_bec_wire_transfer.eml` — CEO Impersonation Wire Fraud (Critical Risk, BEC)
- `sample_4_o365_credential_harvest.eml` — Office 365 Credential Harvesting (Critical Risk, IP-literal URL)
- `sample_5_malicious_macro_payload.eml` — Weaponized Payroll Macro Payload (Critical Risk, .xlsm attachment)
- `sample_6_anonymized_mta_relay.eml` — Ambiguous Freight Notice via Tor Exit Relay (Guarded Risk)

---

## Technical Limitations & Disclaimers

- **Prototype Forensic Dossier:** Hashes prove file integrity; this software does not constitute a legally certified digital forensics laboratory certificate.
- **Header Attribution Caveat:** Initial Received headers can be forged by sophisticated adversaries routing through compromised open relays; candidate origin IPs represent network boundaries, not definitive physical perpetrators.
- **Gmail OAuth Flow:** Requires standard Google Cloud Console Client ID/Secret for live mailbox sync; fully functional offline demo and .eml upload are active when credentials are empty.

---

## License

This project is open-source under the [Apache 2.0 License](LICENSE).  
Copyright (c) 2026 Team Dark | Hacktoberfest Hack Day Bengaluru 2026.
