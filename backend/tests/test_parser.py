import pytest
from app.services.email_parser import parse_email_bytes, compute_sha256

def test_legitimate_eml_parsing():
    raw = b"""From: "Test User" <test@example.com>
To: target@company.com
Subject: Test Hello
Date: Wed, 07 Oct 2026 10:00:00 +0000
Message-ID: <msg123@example.com>

This is a test email message.
"""
    data = parse_email_bytes(raw)
    assert data.subject == "Test Hello"
    assert "test@example.com" in data.sender_from and "Test User" in data.sender_from
    assert data.sender_domain == "example.com"
    assert data.original_digest == compute_sha256(raw)
    assert "test email message" in data.body_text

def test_safe_error_on_oversized():
    huge_payload = b"X" * (16 * 1024 * 1024) # 16MB > 15MB limit
    with pytest.raises(ValueError) as exc:
        parse_email_bytes(huge_payload)
    assert "exceeds" in str(exc.value)

def test_attachment_hash_extraction():
    raw = b"""From: sender@domain.com
To: user@domain.com
Subject: Attachment Test
Content-Type: multipart/mixed; boundary="BOUNDARY"

--BOUNDARY
Content-Type: text/plain

See attached.
--BOUNDARY
Content-Type: application/octet-stream; name="payload.bin"
Content-Disposition: attachment; filename="payload.bin"
Content-Transfer-Encoding: base64

SGVsbG8gV29ybGQ=
--BOUNDARY--"""
    data = parse_email_bytes(raw)
    assert len(data.attachments) == 1
    assert data.attachments[0]["filename"] == "payload.bin"
    assert len(data.attachments[0]["sha256_hash"]) == 64
