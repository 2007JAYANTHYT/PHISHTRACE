import pytest
from app.services.evidence_service import evidence_vault
from app.services.geo_intelligence import geo_service
from app.db.seed import seed_database_and_samples
from app.db.database import db

def test_evidence_verification_and_tampering():
    seed_database_and_samples()
    emails = db.get_all_email_details()
    assert len(emails) > 0

    first_email = emails[0]
    rec = evidence_vault.record_investigation(first_email)
    
    # Check valid verification
    ver_clean = evidence_vault.verify_integrity(rec.investigation_id)
    assert ver_clean.matches is True

    # Simulate tampering with stored record
    stored = evidence_vault.get_investigation(rec.investigation_id)
    stored["risk_score"] = 0 # Tampered
    ver_tampered = evidence_vault.verify_integrity(rec.investigation_id)
    assert ver_tampered.matches is False

def test_private_ip_isolation():
    # RFC 1918 addresses must NEVER be reported as public or sent to public geolocation
    private_ips = ["10.0.0.1", "192.168.1.1", "172.16.5.20", "127.0.0.1"]
    for ip in private_ips:
        assert geo_service.is_routable_public_ip(ip) is False
        geo = geo_service.lookup_ip(ip)
        assert geo.is_private is True
        assert geo.source == "Private Address Space"
