from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from ...models.schemas import GmailStatus
from ...services.gmail_service import gmail_service

router = APIRouter()

@router.get("/integrations/gmail/status", response_model=GmailStatus)
def get_gmail_status():
    return gmail_service.get_status()

@router.get("/integrations/gmail/connect")
def initiate_gmail_connect():
    try:
        url = gmail_service.get_auth_url()
        return {"authorization_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/integrations/gmail/callback")
def handle_gmail_callback(code: Optional[str] = Query(None), error: Optional[str] = Query(None)):
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth authorization error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code.")

    success = gmail_service.exchange_code(code)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to exchange authorization code for tokens.")

    return {"status": "authenticated", "message": f"Successfully connected to Gmail: {gmail_service.user_email}"}

@router.post("/integrations/gmail/sync")
def sync_gmail_emails():
    status = gmail_service.get_status()
    if not status.connected:
        raise HTTPException(status_code=400, detail="Gmail is not connected. Configure credentials in backend/.env or use .eml upload.")
    
    fetched = gmail_service.fetch_recent_emails(max_results=10)
    return {"status": "synced", "count": len(fetched)}
