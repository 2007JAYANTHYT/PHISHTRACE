import pytest
from app.services.threat_engine import evaluate_threat
from app.models.schemas import HeaderForensics, UrlIndicator, AttachmentInfo

def test_legitimate_clean_email():
    headers = HeaderForensics(
        sender_from="elena@company.com",
        sender_domain="company.com",
        recipient_to="user@company.com",
        subject="Meeting Agenda",
        date="2026-10-08",
        spf_observed="pass",
        dkim_observed="pass",
        dmarc_observed="pass"
    )
    assessment, mitre = evaluate_threat(
        subject="Meeting Agenda",
        body_text="Here is the agenda for tomorrow morning.",
        headers=headers,
        urls=[],
        attachments=[]
    )
    assert assessment.score < 25
    assert assessment.category == "Low"
    assert assessment.confidence >= 0.85

def test_critical_bec_wire_transfer():
    headers = HeaderForensics(
        sender_from="Marcus Vance (CEO) <ceo.spoof@gmail.com>",
        sender_display_name="Marcus Vance (CEO)",
        sender_domain="gmail.com",
        reply_to="attacker@offshore.net",
        recipient_to="cfo@company.com",
        subject="URGENT: Executive Wire Transfer Instructions",
        date="2026-10-08",
        spf_observed="pass",
        dkim_observed="none",
        dmarc_observed="fail"
    )
    assessment, mitre = evaluate_threat(
        subject="URGENT: Executive Wire Transfer Instructions",
        body_text="Please process an urgent wire transfer with change of banking details immediately.",
        headers=headers,
        urls=[],
        attachments=[]
    )
    assert assessment.score >= 75
    assert assessment.category == "Critical"
    assert any(s.rule_id == "IMPERSONATION_VIP_FREEMAIL" for s in assessment.signals)
    assert any(s.rule_id == "CONTENT_BEC_FINANCIAL" for s in assessment.signals)
    assert 0 <= assessment.score <= 100
