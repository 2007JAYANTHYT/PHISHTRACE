from pathlib import Path
from ..config import SAMPLES_DIR
from ..services.email_parser import parse_email_bytes
from ..services.header_auth import analyze_header_hops
from ..services.url_analysis import analyze_all_urls
from ..services.threat_engine import evaluate_threat
from ..services.gemma_provider import gemma_service, build_deterministic_gemma_fallback
from ..services.evidence_service import evidence_vault
from ..models.schemas import EmailDetail
from .database import db

SAMPLE_EMAILS = [
    {
        "filename": "sample_1_legit_corporate.eml",
        "raw": b"""From: "Elena Rostova" <elena.rostova@enterprise-acme.org>
To: "Alex Devlin" <alex.devlin@enterprise-acme.org>
Subject: Quarterly Board Governance Meeting -- Agenda & Materials
Date: Thu, 08 Oct 2026 14:15:00 +0000
Message-ID: <legit-board-20261008-01@enterprise-acme.org>
Return-Path: <elena.rostova@enterprise-acme.org>
Authentication-Results: mx.enterprise-acme.org; dkim=pass (signature verified); spf=pass smtp.mailfrom=elena.rostova@enterprise-acme.org; dmarc=pass
Received-SPF: pass (google.com: domain of elena.rostova@enterprise-acme.org designates 209.85.220.41 as permitted sender)
Received: from mail-pj1-f41.google.com (mail-pj1-f41.google.com [209.85.220.41])
    by mx.enterprise-acme.org (Postfix) with ESMTPS id 4W0fK32PzSz1
    for <alex.devlin@enterprise-acme.org>; Thu, 08 Oct 2026 14:15:02 +0000
Content-Type: text/plain; charset="utf-8"

Hi Alex,

Please find the finalized agenda for tomorrow's quarterly executive review meeting. 
All committee members have confirmed attendance.

Agenda topics:
1. Q3 Fiscal Performance & Engineering Milestones
2. Infrastructure Security Audits
3. Open-source Tooling Allocations for FY2027

See you in Boardroom 3 at 10:00 AM.

Best regards,
Elena Rostova
Chief Governance Officer
Enterprise Acme Group
"""
    },
    {
        "filename": "sample_2_scholarship_fee_phish.eml",
        "raw": b"""From: "Global STEM Foundation" <awards@stem-scholarship-grants.xyz>
To: "Scholarship Applicant" <student.fellow@university-mail.edu>
Subject: Congratulations: Your $12,500 Global STEM Fellowship (Action Required)
Date: Wed, 07 Oct 2026 09:30:00 +0000
Message-ID: <grant-award-xyz-2026@stem-scholarship-grants.xyz>
Reply-To: "Disbursement Office" <processing@offshore-grant-escrow.top>
Authentication-Results: mx.university-mail.edu; spf=neutral; dkim=none; dmarc=none
Received: from server1.hostinger.com (server1.hostinger.com [103.253.144.10])
    by mx.university-mail.edu with ESMTP id 8H3xL9211z; Wed, 07 Oct 2026 09:30:05 +0000
Content-Type: text/html; charset="utf-8"

<!DOCTYPE html>
<html>
<body>
<h2>OFFICIAL NOTICE OF SELECTION: GLOBAL STEM ENDOWMENT</h2>
<p>Dear Candidate,</p>
<p>We are delighted to inform you that your application for the 2026 Global STEM Excellence Grant has been approved in the amount of <strong>$12,500.00 USD</strong>.</p>
<p>To finalize disbursement into your institutional account, you must confirm your credentials and remit a nominal <strong>processing fee deposit of $85</strong> within 48 hours.</p>
<p><a href="http://stem-scholarship-grants.xyz/claim-award">Click here to submit your processing fee deposit</a></p>
<p>Failure to complete verification will result in grant forfeiture.</p>
<br>
<p>STEM Endowment Selection Board</p>
</body>
</html>
"""
    },
    {
        "filename": "sample_3_urgent_bec_wire_transfer.eml",
        "raw": b"""From: "Marcus Vance (CEO)" <ceo.office.vance@gmail.com>
To: "Sarah Jenkins (Finance Director)" <sarah.jenkins@enterprise-acme.org>
Subject: URGENT & CONFIDENTIAL: Acquisition Wire Transfer Instructions
Date: Thu, 08 Oct 2026 16:45:00 +0000
Message-ID: <urgent-bec-wire-991204@gmail.com>
Reply-To: "Marcus Vance Private" <mance-privatereply@secure-offshore-mail.net>
Authentication-Results: mx.enterprise-acme.org; dkim=pass; spf=pass; dmarc=none
Received: from mail-io1-xd88.google.com ([209.85.216.170])
    by mx.enterprise-acme.org with ESMTPS id 3L9P019Z; Thu, 08 Oct 2026 16:45:04 +0000
Content-Type: text/plain; charset="utf-8"

Sarah,

I am currently tied up in an offsite executive board meeting regarding a highly confidential acquisition. 

Due to a banking audit with Vendor Apex, their standard account has been placed on temporary hold. We need to execute an immediate payment change of banking details to avoid contract cancellation.

Please arrange an urgent wire transfer of $84,200.00 right now to our partner's updated escrow routing number:
Bank: Horizon International Trust
Routing Number: 021000021
Account Number: 99482104882
Beneficiary: Apex Consulting Global Ltd

Treat this matter with absolute confidentiality. Do not call my cell phone as I cannot step out of the boardroom. Confirm via reply once the wire transfer confirmation is generated.

Marcus Vance
Chief Executive Officer
Enterprise Acme Group
"""
    },
    {
        "filename": "sample_4_o365_credential_harvest.eml",
        "raw": b"""From: "Microsoft Office365 Security" <no-reply@security-alerts-office365.top>
To: "User Identity" <target.employee@enterprise-acme.org>
Subject: CRITICAL ALERT: Your Microsoft 365 Account Will Be Terminated in 24 Hours
Date: Wed, 07 Oct 2026 18:20:00 +0000
Message-ID: <msft-alert-terminate-8831@office365-top.com>
Authentication-Results: mx.enterprise-acme.org; dkim=fail; spf=softfail; dmarc=fail
Received: from vps-relays.changway.nl ([45.154.255.89])
    by mx.enterprise-acme.org with ESMTP id 5Q9911X; Wed, 07 Oct 2026 18:20:03 +0000
Content-Type: text/html; charset="utf-8"

<!DOCTYPE html>
<html>
<body>
<div style="background:#0078d4;color:white;padding:12px;"><h3>Microsoft 365 Security Protection</h3></div>
<p>Your institutional cloud mailbox session has expired due to failed multi-factor 2FA validation.</p>
<p><strong>Immediate action required:</strong> Failure to verify your password and authenticate identity will result in permanent account termination and loss of email archives within 24 hours.</p>
<p>Please re-authenticate your corporate credentials below:</p>
<p><a href="http://185.220.101.5/office365-login.html">https://login.microsoftonline.com/common/oauth2/v2.0/authorize</a></p>
<p>IT Security Administration -- Enterprise Services</p>
</body>
</html>
"""
    },
    {
        "filename": "sample_5_malicious_macro_payload.eml",
        "raw": b"""From: "Corporate Payroll Department" <payroll@internal-updates.online>
To: "All Employees" <staff.distribution@enterprise-acme.org>
Subject: Revised Q3 Staff Salary and Commission Roster
Date: Tue, 06 Oct 2026 11:10:00 +0000
Message-ID: <payroll-roster-20261006@internal-updates.online>
Authentication-Results: mx.enterprise-acme.org; dkim=none; spf=fail; dmarc=none
Received: from offshore-mta.seychelles.net ([91.240.118.42])
    by mx.enterprise-acme.org with ESMTP id 7K1122ZZ; Tue, 06 Oct 2026 11:10:04 +0000
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="====BOUNDARY_PHISH_PAYROLL===="

--====BOUNDARY_PHISH_PAYROLL====
Content-Type: text/plain; charset="utf-8"

Team,

Attached is the revised Q3 compensation adjustment file.
Please open the attached workbook, enable content macros to decrypt your personalized staff tier, and verify your account routing details by Friday.

Regards,
Human Resources & Payroll
--====BOUNDARY_PHISH_PAYROLL====
Content-Type: application/vnd.ms-excel.sheet.macroEnabled.12; name="Q3_Updated_Corporate_Payroll.xlsm"
Content-Disposition: attachment; filename="Q3_Updated_Corporate_Payroll.xlsm"
Content-Transfer-Encoding: base64

UEsDBBQAAAAIAAAAAAAAAAAAAAAAAAAAAAARAAAAeGwvd29ya2Jvb2sueG1szcxNCsIwEEDhvVCP
YGbSNGtBXEiKiIsupGkkM2hmSEq8vVDq0s27fPje0zZkWwS6S6nUkq0N5Kk91sYpYy9M9T0z
--====BOUNDARY_PHISH_PAYROLL====--
"""
    },
    {
        "filename": "sample_6_anonymized_mta_relay.eml",
        "raw": b"""From: "Vendor Logistics Dispatch" <dispatch@global-logistics-corp.com>
To: "Warehouse Operations" <inventory@enterprise-acme.org>
Subject: Notice of Delivery Route Rescheduling #TRK-88190
Date: Mon, 05 Oct 2026 08:00:00 +0000
Message-ID: <trk-88190-dispatch@global-logistics.com>
Authentication-Results: mx.enterprise-acme.org; dkim=none; spf=neutral; dmarc=none
Received: from relay2.mta-tor.de ([185.220.101.5])
    by mx.enterprise-acme.org with ESMTP id 9X0044; Mon, 05 Oct 2026 08:00:02 +0000
Content-Type: text/plain; charset="utf-8"

Notice: Your pending freight delivery #TRK-88190 has been rescheduled due to regional customs inspection. 
Track transit progress at our public carrier dispatch center.
"""
    }
]

def seed_database_and_samples():
    """Seeds the demo dataset into files and memory."""
    db.clear()

    for item in SAMPLE_EMAILS:
        filename = item["filename"]
        raw_bytes = item["raw"]

        # Write .eml file to samples/ directory
        sample_path = SAMPLES_DIR / filename
        try:
            with open(sample_path, "wb") as f:
                f.write(raw_bytes)
        except Exception:
            pass

        # Parse email
        parsed = parse_email_bytes(raw_bytes)

        # Forensic headers
        headers = analyze_header_hops(
            received_headers=parsed.received_headers,
            sender_from=parsed.sender_from,
            sender_display_name=parsed.sender_display_name,
            sender_domain=parsed.sender_domain,
            reply_to=parsed.reply_to,
            return_path=parsed.return_path,
            recipient_to=parsed.recipient_to,
            subject=parsed.subject,
            date=parsed.date,
            message_id=parsed.message_id,
            auth_results_raw=parsed.auth_results_raw,
            received_spf_raw=parsed.received_spf_raw,
            dkim_raw=parsed.dkim_signature_raw,
            arc_raw=parsed.arc_results_raw
        )

        # URLs analysis
        url_indicators = analyze_all_urls(parsed.urls, parsed.body_html)

        # Threat evaluation
        assessment, mitre_tactics = evaluate_threat(
            subject=parsed.subject,
            body_text=parsed.body_text,
            headers=headers,
            urls=url_indicators,
            attachments=parsed.attachments
        )

        # Gemma Open-Source AI Threat Analysis (deterministic grounding for samples)
        gemma_analysis = build_deterministic_gemma_fallback(
            subject=parsed.subject,
            body_text=parsed.body_text,
            headers=headers,
            assessment=assessment,
            urls=url_indicators,
            attachments=parsed.attachments
        )

        email_id = parsed.original_digest[:16]

        email_detail = EmailDetail(
            id=email_id,
            subject=parsed.subject,
            sender_from=parsed.sender_from,
            sender_display_name=parsed.sender_display_name,
            sender_domain=parsed.sender_domain,
            reply_to=parsed.reply_to,
            recipient_to=parsed.recipient_to,
            date=parsed.date,
            original_digest=parsed.original_digest,
            body_text_sanitized=parsed.body_text,
            body_html_sanitized=parsed.sanitized_body_preview,
            headers=headers,
            urls=url_indicators,
            attachments=parsed.attachments,
            risk_assessment=assessment,
            gemma_analysis=gemma_analysis,
            mitre_tactics=mitre_tactics,
            source_type="demo",
            created_at=parsed.date
        )

        db.save_email(email_detail)
        evidence_vault.record_investigation(email_detail)

    print(f"Successfully seeded {len(SAMPLE_EMAILS)} threat intelligence emails.")
