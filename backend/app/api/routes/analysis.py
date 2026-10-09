from fastapi import APIRouter
from ...db.database import db
from ...models.schemas import DashboardSummary
from ...services.campaign_service import campaign_service
from ...services.evidence_service import evidence_vault
from ...services.gmail_service import gmail_service
from ...services.gemma_provider import gemma_service

router = APIRouter()

@router.get("/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary():
    emails = db.get_all_email_details()
    total = len(emails)
    
    crit = sum(1 for e in emails if e.risk_assessment.category == "Critical")
    high = sum(1 for e in emails if e.risk_assessment.category == "High")
    guarded = sum(1 for e in emails if e.risk_assessment.category == "Guarded")
    low = sum(1 for e in emails if e.risk_assessment.category == "Low")

    campaigns = campaign_service.correlate_campaigns(emails)
    investigations = evidence_vault.list_investigations()

    risk_dist = [
        {"name": "Critical (75-100)", "count": crit, "color": "#ef4444"},
        {"name": "High (50-74)", "count": high, "color": "#f97316"},
        {"name": "Guarded (25-49)", "count": guarded, "color": "#eab308"},
        {"name": "Low (0-24)", "count": low, "color": "#22c55e"}
    ]

    return DashboardSummary(
        total_emails=total,
        critical_threats=crit,
        high_threats=high,
        guarded_threats=guarded,
        low_threats=low,
        emails_requiring_review=crit + high,
        active_campaigns=len(campaigns),
        recent_investigations=investigations[:6],
        risk_distribution=risk_dist,
        gmail_status=gmail_service.get_status().dict(),
        ai_status=gemma_service.get_status()
    )
