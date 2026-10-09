# PhishTrace Synthetic Threat Intelligence Samples

This directory contains 6 RFC-compliant `.eml` test messages designed for testing, offline demonstrations, and security evaluation.

## Sample Manifest

1. **`sample_1_legit_corporate.eml`**
   - **Type:** Legitimate Corporate Communication
   - **Scenario:** Quarterly Board of Governance Meeting Agenda.
   - **Attributes:** Valid Google Workspace infrastructure, `spf=pass`, `dkim=pass`, `dmarc=pass`.
   - **Expected Verdict:** **Low (Score: < 20)**

2. **`sample_2_scholarship_fee_phish.eml`**
   - **Type:** Advance-Fee / Scholarship Grant Scam
   - **Scenario:** $12,500 fake academic fellowship demanding $85 registration fee deposit.
   - **Attributes:** External lookalike domain `.xyz`, `spf=neutral`, Hostinger VPS relay hop.
   - **Expected Verdict:** **Guarded / High (Score: 40-60)**

3. **`sample_3_urgent_bec_wire_transfer.eml`**
   - **Type:** Business Email Compromise (BEC) & Executive Impersonation
   - **Scenario:** CEO display name spoofing requesting urgent confidential wire transfer ($84,200).
   - **Attributes:** VIP display name from consumer Gmail, deceptive Reply-To header, routing number solicitation.
   - **Expected Verdict:** **Critical (Score: 80-95)**

4. **`sample_4_o365_credential_harvest.eml`**
   - **Type:** Credential Harvesting & Account Lockout Phishing
   - **Scenario:** Urgent Microsoft 365 2FA session expiration threat.
   - **Attributes:** Naked IP-literal URL destination (`http://185.220.101.5`), deceptive anchor text, `dmarc=fail`.
   - **Expected Verdict:** **Critical (Score: 85-95)**

5. **`sample_5_malicious_macro_payload.eml`**
   - **Type:** Weaponized Attachment Spearphishing
   - **Scenario:** Urgent payroll roster adjustment with weaponized macro payload.
   - **Attributes:** Macro-enabled spreadsheet attachment (`.xlsm`), base64 payload, `spf=fail`, Seychelles offshore MTA.
   - **Expected Verdict:** **Critical (Score: 85-98)**

6. **`sample_6_anonymized_mta_relay.eml`**
   - **Type:** Ambiguous Logistics Notice via Anonymized MTA
   - **Scenario:** Delivery route rescheduling notification.
   - **Attributes:** Traces through German Tor exit relay (`185.220.101.5`), missing client IP, ambiguous SPF.
   - **Expected Verdict:** **Guarded (Score: 25-45)**
