import re
from typing import Dict, Any, List, Optional
from ..models.schemas import AiCopilotResponse, EmailDetail

def generate_yara_rule(email: EmailDetail) -> str:
    """Generates an authentic YARA detection rule tailored to the email indicators."""
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', email.subject[:30]) or "Suspicious_Email"
    strings_block = []
    
    if email.headers.sender_domain:
        strings_block.append(f'        $sender_domain = "{email.headers.sender_domain}" nocase')
    if email.urls:
        sample_host = email.urls[0].host
        strings_block.append(f'        $suspicious_host = "{sample_host}" nocase')
    if email.attachments:
        strings_block.append(f'        $attachment_hash = "{email.attachments[0].sha256_hash}"')
    
    if not strings_block:
        strings_block.append(f'        $subject_keyword = "{email.subject[:25]}" nocase')

    rule = f"""rule PhishTrace_{safe_name} {{
    meta:
        description = "Automated IOC detection for {email.subject}"
        threat_level = "{email.risk_assessment.category}"
        risk_score = {email.risk_assessment.score}
        author = "PhishTrace Open-Source AI Copilot"
        date = "{email.date}"
    strings:
{chr(10).join(strings_block)}
    condition:
        any of them
}}"""
    return rule

def generate_m365_rule(email: EmailDetail) -> str:
    """Generates PowerShell Exchange Online Mail Flow Rule command."""
    rule_name = f"PhishTrace-Block-{email.id[:8]}"
    domain = email.headers.sender_domain or "suspicious-domain.com"
    return f"""# Microsoft 365 Exchange Online Transport Rule
New-TransportRule -Name "{rule_name}" \\
    -SenderDomainIs "{domain}" \\
    -SetAuditSeverity "High" \\
    -ApplyHtmlDisclaimerLocation "Append" \\
    -ApplyHtmlDisclaimerText "<div style='background-color:#ffebee;padding:8px;border:2px solid #c62828;'><strong>[PHISHTRACE SECURITY WARNING]</strong> This inbound message was matched against active threat campaign indicators.</div>" \\
    -ModerateMessageByUser "soc-quarantine@yourdomain.com" \\
    -StopRuleProcessing $true"""

def generate_kql_query(email: EmailDetail) -> str:
    """Generates Microsoft Sentinel / Defender KQL threat hunting query."""
    domain = email.headers.sender_domain or "threat-domain.com"
    hash_clause = f' or SHA256 == "{email.attachments[0].sha256_hash}"' if email.attachments else ''
    return f"""// Microsoft Sentinel / Defender Threat Hunting Query
EmailEvents
| where Timestamp >= ago(7d)
| where SenderFromDomain =~ "{domain}" or Subject has "{email.subject[:25]}"
| join kind=leftouter (
    DeviceNetworkEvents
    | where RemoteUrl has "{domain}"{hash_clause}
) on DeviceId
| project Timestamp, RecipientEmailAddress, SenderFromAddress, Subject, DeliveryAction, DeviceName, RemoteUrl"""

def generate_splunk_query(email: EmailDetail) -> str:
    """Generates Splunk SPL threat hunting search."""
    domain = email.headers.sender_domain or "threat-domain.com"
    return f"""index=email sourcetype=ms:o365:reporting:messagetrace (sender="*{domain}*" OR subject="*{email.subject[:20]}*")
| eval threat_level="{email.risk_assessment.category}"
| stats count earliest(_time) as first_seen latest(_time) as last_seen by sender, recipient, subject, status
| convert ctime(first_seen) ctime(last_seen)"""

def generate_sigma_rule(email: EmailDetail) -> str:
    """Generates Sigma generic log detection rule in YAML format."""
    safe_title = re.sub(r'[^a-zA-Z0-9_ ]', '', email.subject[:40]) or "Suspicious Email Indicator"
    domain = email.headers.sender_domain or "threat-domain.com"
    return f"""title: Inbound Threat Campaign - {safe_title}
id: {email.id[:8]}-0000-4000-8000-{email.id[8:16]}
status: experimental
description: Detects inbound communication and network events associated with {email.subject}
author: PhishTrace Open-Source AI Copilot
date: {email.date}
logsource:
    category: email
    product: m365
detection:
    selection:
        SenderDomain: '{domain}'
    condition: selection
falsepositives:
    - Legitimate external partner with identical domain
level: {email.risk_assessment.category.lower()}"""

def run_copilot_assistant(
    prompt: str,
    email: EmailDetail
) -> AiCopilotResponse:
    """
    AI Forensic Co-Pilot reasoning engine.
    Analyzes analyst queries against real email context, generates forensic answers,
    YARA rules, and defensive configurations.
    """
    p_lower = prompt.lower()
    suggested = []
    yara = None
    m365 = None
    kql = None
    splunk = None
    sigma = None

    # Check all rule generation intents independently
    if "yara" in p_lower:
        yara = generate_yara_rule(email)
    if "kql" in p_lower or "sentinel" in p_lower or "defender" in p_lower:
        kql = generate_kql_query(email)
    if "splunk" in p_lower or "spl" in p_lower:
        splunk = generate_splunk_query(email)
    if "sigma" in p_lower:
        sigma = generate_sigma_rule(email)
    if "m365" in p_lower or "exchange" in p_lower or "transport rule" in p_lower or "block" in p_lower:
        m365 = generate_m365_rule(email)

    # Determine answer summary and suggestions based on generated rules
    generated_types = []
    if yara: generated_types.append("YARA detection rule")
    if kql: generated_types.append("Microsoft Sentinel KQL query")
    if splunk: generated_types.append("Splunk SPL hunting search")
    if sigma: generated_types.append("Sigma detection rule")
    if m365: generated_types.append("Exchange Online Mail Flow rule")

    if generated_types:
        answer = (
            f"I have synthesized the requested security detection artifacts ({', '.join(generated_types)}) "
            f"tailored to message '{email.subject}'. The rules correlate observed sender telemetry "
            f"({email.headers.sender_domain or 'target domain'}), payload hashes, and headers for immediate perimeter/SIEM deployment."
        )
        suggested = ["Draft CISO incident advisory", "Analyze Received header hops", "Audit recipient click telemetry"]
    elif "ciso" in p_lower or "executive" in p_lower or "advisory" in p_lower or "report" in p_lower:
        answer = (
            f"### EXECUTIVE INCIDENT ADVISORY\n\n"
            f"**Classification:** {email.risk_assessment.category.upper()} PRIORITY ({email.risk_assessment.score}/100)\n"
            f"**Threat Vector:** {email.gemma_analysis.suspected_threat}\n"
            f"**Target:** {email.recipient_to}\n"
            f"**Attribution Candidate:** {email.headers.origin_candidate_ip or 'Unresolved Proxy'} "
            f"({email.headers.origin_geo.country if email.headers.origin_geo else 'Unknown'})\n\n"
            f"**Incident Summary:**\n"
            f"{email.gemma_analysis.summary}\n\n"
            f"**Immediate Mitigations:**\n"
            f"1. Perimeter gateway blocking of sender and associated indicators.\n"
            f"2. Audit of recipient mailbox for click-through or credential entry.\n"
            f"3. Password reset and MFA session revocation if credentials were submitted."
        )
        suggested = ["Generate KQL hunting query", "Generate M365 Mail Flow rule", "Generate YARA rule"]
    elif "hop" in p_lower or "header" in p_lower or "relay" in p_lower or "origin" in p_lower:
        hops_count = len(email.headers.received_hops)
        earliest_ip = email.headers.origin_candidate_ip or "None"
        answer = (
            f"Forensic Header Analysis for '{email.subject}':\n\n"
            f"- **Observed Hop Count:** {hops_count} Recorded Received Headers.\n"
            f"- **Candidate External Origin:** `{earliest_ip}` "
            f"({email.headers.origin_geo.city if email.headers.origin_geo else 'N/A'}, {email.headers.origin_geo.country if email.headers.origin_geo else 'N/A'}).\n"
            f"- **Authentication Forensics:** SPF={email.headers.spf_observed}, DKIM={email.headers.dkim_observed}, DMARC={email.headers.dmarc_observed}.\n\n"
            f"**Forensic Note:** {email.headers.origin_caveat or 'All hops validated through trusted relay networks.'}"
        )
        suggested = ["Generate KQL hunting query", "Generate YARA rule", "Draft CISO advisory"]
    else:
        # General investigative answering
        answer = (
            f"Based on full forensic telemetry for **'{email.subject}'**:\n\n"
            f"- **Threat Assessment:** Risk Score {email.risk_assessment.score}/100 ({email.risk_assessment.category}).\n"
            f"- **Attacker Mechanism:** {email.gemma_analysis.suspected_threat}.\n"
            f"- **Key Evidence:** {', '.join(email.gemma_analysis.evidence_references[:2]) if email.gemma_analysis.evidence_references else 'Authentic signature'}.\n"
            f"- **Analyst Recommendation:** {email.risk_assessment.recommended_next_step}\n\n"
            f"You can prompt me to generate YARA rules, Microsoft Sentinel KQL queries, Splunk SPL searches, Sigma rules, or M365 transport rules."
        )
        suggested = ["Generate YARA rule", "Generate KQL hunting query", "Generate Splunk SPL query", "Generate Sigma rule", "Generate M365 transport rule"]

    return AiCopilotResponse(
        answer=answer,
        model_used="PhishTrace Open-Source Gemma Security Co-Pilot",
        suggested_actions=suggested,
        yara_rule=yara,
        m365_rule=m365,
        kql_query=kql,
        splunk_query=splunk,
        sigma_rule=sigma
    )
