import re
from typing import List, Tuple, Dict, Any, Optional
from ..models.schemas import (
    RiskAssessment, ThreatSignal, HeaderForensics, 
    UrlIndicator, AttachmentInfo, MitreTactic
)

# Common VIP / Executive Titles used in Business Email Compromise (BEC)
VIP_TITLES = ["ceo", "cfo", "coo", "chief executive", "president", "director", "founder", "chairman", "vice president", "vp", "controller", "treasurer"]

# Critical BEC / Wire Transfer / Payment Phishing Keywords
BEC_PAYMENT_PATTERNS = [
    (r'wire\s+transfer', "Wire transfer request", 25),
    (r'urgent\s+payment', "Urgent payment solicitation", 25),
    (r'change\s+(?:of\s+)?bank(?:ing)?\s+details', "Bank account modification instructions", 35),
    (r'updated\s+invoice', "Updated invoice instructions", 20),
    (r'routing\s+number', "Banking routing/account numbers solicitation", 20),
    (r'swift\s+(?:code|transfer)', "SWIFT transaction request", 20),
    (r'confidential\s+acquisition', "Confidential M&A / executive secrecy pretext", 25),
    (r'gift\s+card', "Urgent gift card purchase request", 30),
]

# Credential Harvesting / Account Suspension Patterns
CREDENTIAL_HARVESTING_PATTERNS = [
    (r'account\s+(?:suspended|locked|terminated|disabled)', "Account suspension threat", 25),
    (r'password\s+expires?', "Password expiration lure", 20),
    (r'verify\s+your\s+identity', "Identity verification lure", 20),
    (r'security\s+alert', "Security alert pressure tactic", 15),
    (r'immediate\s+action\s+required', "Coercive urgency trigger", 20),
    (r'sign\s*in\s+to\s+keep\s+access', "Credential sign-in pressure", 25),
    (r'2fa\s+(?:bypass|disabled|verify)', "MFA / 2FA verification deception", 25),
]

# Fee / Scholarship / Job Scam Patterns
FEE_SCAM_PATTERNS = [
    (r'scholarship\s+grant', "Scholarship lure", 15),
    (r'processing\s+fee', "Upfront fee demand", 25),
    (r'registration\s+deposit', "Upfront deposit demand", 25),
    (r'guaranteed\s+acceptance', "Guaranteed acceptance pretext", 20),
]

def evaluate_threat(
    subject: str,
    body_text: str,
    headers: HeaderForensics,
    urls: List[UrlIndicator],
    attachments: List[AttachmentInfo]
) -> Tuple[RiskAssessment, List[MitreTactic]]:
    """
    Deterministic, explainable threat engine.
    Calculates weighted risk score (0-100) using orthogonal security dimensions.
    """
    signals: List[ThreatSignal] = []
    mitre_tactics: List[MitreTactic] = []
    content_lower = f"{subject}\n{body_text}".lower()

    # -------------------------------------------------------------
    # 1. Authentication Signals (Observed SPF/DKIM/DMARC)
    # -------------------------------------------------------------
    if headers.dmarc_observed in ("fail", "reject_policy"):
        signals.append(ThreatSignal(
            category="authentication",
            rule_id="AUTH_DMARC_FAIL",
            description="Domain fails DMARC policy validation; high probability of sender domain spoofing",
            severity="critical",
            weight=35,
            evidence_quote=f"DMARC status: {headers.dmarc_observed}"
        ))
        mitre_tactics.append(MitreTactic(
            tactic_id="T1566.002",
            technique="Phishing: Spearphishing Service",
            name="DMARC Policy Rejection",
            confidence="High",
            evidence="DMARC check failed or policy rejected by inbound gateway"
        ))
    elif headers.spf_observed in ("fail", "softfail"):
        signals.append(ThreatSignal(
            category="authentication",
            rule_id="AUTH_SPF_FAIL",
            description=f"Inbound sending IP is unauthorized in domain SPF record ({headers.spf_observed})",
            severity="high",
            weight=20,
            evidence_quote=f"SPF status: {headers.spf_observed}"
        ))

    if headers.dkim_observed == "fail":
        signals.append(ThreatSignal(
            category="authentication",
            rule_id="AUTH_DKIM_FAIL",
            description="DKIM cryptographic body signature failed validation or was altered in transit",
            severity="high",
            weight=25,
            evidence_quote="DKIM status: fail"
        ))

    # -------------------------------------------------------------
    # 2. Impersonation & Sender Deception Signals
    # -------------------------------------------------------------
    display_name = (headers.sender_display_name or "").lower()
    from_addr = headers.sender_from.lower()
    sender_domain = (headers.sender_domain or "").lower()

    # Check VIP / Executive display name spoofing
    vip_match = any(vip in display_name for vip in VIP_TITLES)
    free_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]
    is_freemail = any(sender_domain.endswith(f) for f in free_domains)

    if vip_match and is_freemail:
        signals.append(ThreatSignal(
            category="impersonation",
            rule_id="IMPERSONATION_VIP_FREEMAIL",
            description=f"Executive / Leadership identity claimed in display name ('{headers.sender_display_name}') while transmitting from external freemail provider ('{sender_domain}')",
            severity="critical",
            weight=35,
            evidence_quote=f"From: {headers.sender_from}"
        ))
        mitre_tactics.append(MitreTactic(
            tactic_id="T1566.001",
            technique="Phishing: Spearphishing Link / Pretexting",
            name="Executive Impersonation",
            confidence="High",
            evidence=f"Executive name '{headers.sender_display_name}' sent via consumer freemail"
        ))

    # Check From vs Reply-To Mismatch
    if headers.reply_to:
        reply_lower = headers.reply_to.lower()
        if sender_domain and sender_domain not in reply_lower and ("@" in reply_lower):
            signals.append(ThreatSignal(
                category="impersonation",
                rule_id="REPLY_TO_MISMATCH",
                description="Sender From domain does not match Reply-To address; replies are redirected to a different destination",
                severity="high",
                weight=25,
                evidence_quote=f"From domain: {sender_domain} vs Reply-To: {headers.reply_to}"
            ))

    # -------------------------------------------------------------
    # 3. URL & Link Risk Signals
    # -------------------------------------------------------------
    high_risk_urls = [u for u in urls if u.risk_score >= 40]
    ip_literal_urls = [u for u in urls if u.is_ip_literal]
    lookalike_urls = [u for u in urls if u.is_lookalike]
    anchor_mismatches = [u for u in urls if u.anchor_mismatch]

    if ip_literal_urls:
        signals.append(ThreatSignal(
            category="malicious_url",
            rule_id="URL_IP_LITERAL",
            description=f"Message contains {len(ip_literal_urls)} naked IP-literal hyperlink(s) bypassing domain name infrastructure",
            severity="critical",
            weight=35,
            evidence_quote=f"Sample target: {ip_literal_urls[0].url}"
        ))
        mitre_tactics.append(MitreTactic(
            tactic_id="T1204.001",
            technique="User Execution: Malicious Link",
            name="IP-Literal Redirection",
            confidence="High",
            evidence=f"Raw IP host {ip_literal_urls[0].host} embedded in link"
        ))

    if lookalike_urls:
        signals.append(ThreatSignal(
            category="malicious_url",
            rule_id="URL_LOOKALIKE_BRAND",
            description=f"Detected typosquatted lookalike brand destination ({lookalike_urls[0].host})",
            severity="critical",
            weight=30,
            evidence_quote=f"Lookalike host: {lookalike_urls[0].host}"
        ))

    if anchor_mismatches:
        signals.append(ThreatSignal(
            category="malicious_url",
            rule_id="URL_ANCHOR_MISMATCH",
            description="Deceptive hyperlink display text disguises actual malicious destination URL",
            severity="high",
            weight=25,
            evidence_quote=f"Disguised target: {anchor_mismatches[0].url}"
        ))

    # -------------------------------------------------------------
    # 4. Attachment Risk Signals
    # -------------------------------------------------------------
    exec_attachments = []
    for a in attachments:
        is_exec = getattr(a, 'is_executable', False) if not isinstance(a, dict) else a.get('is_executable', False)
        is_double = getattr(a, 'is_double_extension', False) if not isinstance(a, dict) else a.get('is_double_extension', False)
        if is_exec or is_double:
            exec_attachments.append(a)

    if exec_attachments:
        first_att = exec_attachments[0]
        fname = getattr(first_att, 'filename', '') if not isinstance(first_att, dict) else first_att.get('filename', '')
        sha = getattr(first_att, 'sha256_hash', '') if not isinstance(first_att, dict) else first_att.get('sha256_hash', '')
        signals.append(ThreatSignal(
            category="attachment",
            rule_id="ATTACHMENT_EXECUTABLE",
            description=f"Potentially weaponized payload attachment detected ({fname})",
            severity="critical",
            weight=40,
            evidence_quote=f"File: {fname} (SHA256: {sha[:12]}...)"
        ))
        mitre_tactics.append(MitreTactic(
            tactic_id="T1566.002",
            technique="Phishing: Spearphishing Attachment",
            name="Weaponized Attachment",
            confidence="High",
            evidence=f"Executable or macro attachment: {fname}"
        ))

    # -------------------------------------------------------------
    # 5. Content Intent, BEC & Psychological Urgency Signals
    # -------------------------------------------------------------
    bec_hits = []
    for pattern, label, wt in BEC_PAYMENT_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            bec_hits.append((label, wt, match.group(0)))

    if bec_hits:
        highest_bec = max(bec_hits, key=lambda x: x[1])
        signals.append(ThreatSignal(
            category="content_urgency",
            rule_id="CONTENT_BEC_FINANCIAL",
            description=f"Business Email Compromise (BEC) indicator: {highest_bec[0]}",
            severity="critical" if highest_bec[1] >= 30 else "high",
            weight=highest_bec[1],
            evidence_quote=f"Keyword match: '{highest_bec[2]}'"
        ))
        mitre_tactics.append(MitreTactic(
            tactic_id="T1566",
            technique="Phishing",
            name="Financial Fraud / BEC Solicitation",
            confidence="High",
            evidence=f"Financial manipulation trigger '{highest_bec[2]}'"
        ))

    cred_hits = []
    for pattern, label, wt in CREDENTIAL_HARVESTING_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            cred_hits.append((label, wt, match.group(0)))

    if cred_hits:
        highest_cred = max(cred_hits, key=lambda x: x[1])
        signals.append(ThreatSignal(
            category="content_urgency",
            rule_id="CONTENT_CREDENTIAL_PRESSURE",
            description=f"Psychological coercion and credential harvesting trigger: {highest_cred[0]}",
            severity="high",
            weight=highest_cred[1],
            evidence_quote=f"Trigger phrase: '{highest_cred[2]}'"
        ))

    fee_hits = []
    for pattern, label, wt in FEE_SCAM_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            fee_hits.append((label, wt, match.group(0)))

    if fee_hits and not bec_hits:
        highest_fee = max(fee_hits, key=lambda x: x[1])
        signals.append(ThreatSignal(
            category="content_urgency",
            rule_id="CONTENT_FEE_ADVANCE",
            description=f"Advance fee / scholarship fee solicitation: {highest_fee[0]}",
            severity="medium",
            weight=highest_fee[1],
            evidence_quote=f"Fee phrase: '{highest_fee[2]}'"
        ))

    # -------------------------------------------------------------
    # 6. Origin Relay Anomaly Signals
    # -------------------------------------------------------------
    if headers.origin_geo and headers.origin_geo.country in ["Russia", "Seychelles", "Anonymous"]:
        signals.append(ThreatSignal(
            category="reputation",
            rule_id="GEO_ANOMALOUS_ORIGIN",
            description=f"Earliest external relay hop traces to high-risk or bulletproof hosting territory ({headers.origin_geo.country})",
            severity="medium",
            weight=15,
            evidence_quote=f"Hop IP: {headers.origin_candidate_ip} ({headers.origin_geo.org})"
        ))

    # -------------------------------------------------------------
    # Score Calculation & Non-linear Normalization
    # -------------------------------------------------------------
    # Sum weights with diminishing returns to avoid exceeding 100
    if not signals:
        # Legitimate baseline check: verified auth headers boost trust
        is_clean_auth = (headers.spf_observed == "pass" and headers.dkim_observed == "pass")
        final_score = 4 if is_clean_auth else 12
        category = "Low"
        confidence = 0.95
        uncertainty = "No adverse threat signals detected. Clean SPF/DKIM verification and standard MTA headers."
        recommended = "Standard safe delivery. No investigative intervention required."
    else:
        # Sort weights descending
        weights = sorted([s.weight for s in signals], reverse=True)
        # Primary weight + 60% of second + 40% of third + 20% of rest
        score_accum = 0.0
        for i, w in enumerate(weights):
            if i == 0:
                score_accum += w
            elif i == 1:
                score_accum += w * 0.65
            elif i == 2:
                score_accum += w * 0.45
            else:
                score_accum += w * 0.25

        # Cap between 0 and 100
        final_score = int(min(100, max(0, round(score_accum))))

        # Categorize
        if final_score >= 75:
            category = "Critical"
            recommended = "QUARANTINE IMMEDIATELY. Block sender domain and destination IPs on perimeter gateway; initiate BEC incident response protocol."
            confidence = 0.92
            uncertainty = "High certainty based on corroborating multi-vector signals (authentication failure, coercion intent, or malicious payload)."
        elif final_score >= 50:
            category = "High"
            recommended = "Quarantine message pending SOC analyst review. Add URLs to security proxy blocklist and warn targeted recipient."
            confidence = 0.85
            uncertainty = "Clear indicators of deceptive intent present. Verify authenticity with sender via trusted out-of-band channel."
        elif final_score >= 25:
            category = "Guarded"
            recommended = "Flag banner warning to recipient. Apply heightened scrutiny to any financial instructions or links."
            confidence = 0.78
            uncertainty = "Moderate anomalies detected (e.g., unusual origin relay or softfail SPF). May be legitimate misconfigured newsletter or targeted probe."
        else:
            category = "Low"
            recommended = "Allow delivery with standard corporate email hygiene."
            confidence = 0.90
            uncertainty = "Minor technical deviation detected without malicious payload or deceptive indicators."

    assessment = RiskAssessment(
        score=final_score,
        category=category,
        confidence=confidence,
        uncertainty_explanation=uncertainty,
        signals=signals,
        recommended_next_step=recommended
    )

    return assessment, mitre_tactics
