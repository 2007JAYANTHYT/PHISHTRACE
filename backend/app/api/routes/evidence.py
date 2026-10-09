from fastapi import APIRouter, HTTPException, Response
from typing import List, Dict, Any
from ...services.evidence_service import evidence_vault
from ...db.database import db
from ...models.schemas import InvestigationRecord, VerificationResult

router = APIRouter()

@router.get("/evidence", response_model=List[InvestigationRecord])
def list_evidence():
    return evidence_vault.list_investigations()

@router.get("/evidence/audit-log")
def get_audit_trail() -> List[Dict[str, Any]]:
    return evidence_vault.get_audit_logs()

@router.get("/evidence/{investigation_id}")
def get_evidence_record(investigation_id: str):
    rec = evidence_vault.get_investigation(investigation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    return rec

@router.post("/evidence/{investigation_id}/verify", response_model=VerificationResult)
def verify_evidence(investigation_id: str):
    return evidence_vault.verify_integrity(investigation_id)

@router.get("/evidence/{investigation_id}/export")
def export_evidence_json(investigation_id: str):
    rec = evidence_vault.get_investigation(investigation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Investigation record not found")
    return rec

@router.get("/evidence/{investigation_id}/pdf")
def export_evidence_pdf(investigation_id: str):
    rec = evidence_vault.get_investigation(investigation_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Investigation record not found")

    email = db.get_email(rec["message_id"])
    if not email:
        raise HTTPException(status_code=404, detail="Referenced email message not found")

    pdf_bytes = evidence_vault.generate_pdf_report(email, investigation_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={investigation_id}_dossier.pdf"}
    )
