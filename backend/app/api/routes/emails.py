from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timezone
from ...db.database import db
from ...models.schemas import EmailSummary, EmailDetail, HeaderForensics
from ...services.email_parser import parse_email_bytes
from ...services.header_auth import analyze_header_hops
from ...services.url_analysis import analyze_all_urls
from ...services.threat_engine import evaluate_threat
from ...services.gemma_provider import gemma_service
from ...services.evidence_service import evidence_vault

router = APIRouter()

@router.get("/emails", response_model=List[EmailSummary])
def list_emails(
    category: Optional[str] = Query(None, description="Filter by risk category (Low, Guarded, High, Critical)"),
    search: Optional[str] = Query(None, description="Search subject or sender"),
    source: Optional[str] = Query(None, description="Filter by source_type (demo, uploaded, gmail_live)")
):
    emails = db.list_emails()
    if category:
        emails = [e for e in emails if e.risk_category.lower() == category.lower()]
    if source:
        emails = [e for e in emails if e.source_type.lower() == source.lower()]
    if search:
        s_lower = search.lower()
        emails = [e for e in emails if s_lower in e.subject.lower() or s_lower in e.sender_from.lower()]
    return emails

@router.get("/emails/{message_id}", response_model=EmailDetail)
def get_email_detail(message_id: str):
    email = db.get_email(message_id)
    if not email:
        raise HTTPException(status_code=404, detail=f"Email with ID '{message_id}' not found.")
    return email

@router.get("/emails/{message_id}/forensics", response_model=HeaderForensics)
def get_email_forensics(message_id: str):
    email = db.get_email(message_id)
    if not email:
        raise HTTPException(status_code=404, detail=f"Email with ID '{message_id}' not found.")
    return email.headers

@router.post("/emails/upload", response_model=EmailDetail)
async def upload_eml_file(file: UploadFile = File(...)):
    """Uploads and analyzes an RFC .eml email file."""
    if not file.filename.lower().endswith(('.eml', '.msg', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an RFC .eml email file.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Empty email file uploaded.")

    try:
        parsed = parse_email_bytes(raw_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

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
        date=parsed.date or datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"),
        message_id=parsed.message_id,
        auth_results_raw=parsed.auth_results_raw,
        received_spf_raw=parsed.received_spf_raw,
        dkim_raw=parsed.dkim_signature_raw,
        arc_raw=parsed.arc_results_raw
    )

    # URLs
    urls = analyze_all_urls(parsed.urls, parsed.body_html)

    # Threat engine evaluation
    assessment, mitre_tactics = evaluate_threat(
        subject=parsed.subject,
        body_text=parsed.body_text,
        headers=headers,
        urls=urls,
        attachments=parsed.attachments
    )

    # Gemma 4 Open-Source AI Threat Analysis
    gemma_analysis = gemma_service.analyze(
        subject=parsed.subject,
        body_text=parsed.body_text,
        headers=headers,
        assessment=assessment,
        urls=urls,
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
        date=parsed.date or datetime.now(timezone.utc).isoformat(),
        original_digest=parsed.original_digest,
        body_text_sanitized=parsed.body_text,
        body_html_sanitized=parsed.sanitized_body_preview,
        headers=headers,
        urls=urls,
        attachments=parsed.attachments,
        risk_assessment=assessment,
        gemma_analysis=gemma_analysis,
        mitre_tactics=mitre_tactics,
        source_type="uploaded",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    db.save_email(email_detail)
    evidence_vault.record_investigation(email_detail)

    return email_detail

@router.post("/emails/{message_id}/analyze", response_model=EmailDetail)
def reanalyze_email(message_id: str):
    email = db.get_email(message_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    assessment, mitre = evaluate_threat(
        subject=email.subject,
        body_text=email.body_text_sanitized,
        headers=email.headers,
        urls=email.urls,
        attachments=email.attachments
    )
    gemma = gemma_service.analyze(
        subject=email.subject,
        body_text=email.body_text_sanitized,
        headers=email.headers,
        assessment=assessment,
        urls=email.urls,
        attachments=email.attachments
    )
    email.risk_assessment = assessment
    email.mitre_tactics = mitre
    email.gemma_analysis = gemma

    db.save_email(email)
    evidence_vault.record_investigation(email)
    return email
