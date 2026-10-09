from fastapi import APIRouter, HTTPException
from typing import List
from ...db.database import db
from ...models.schemas import CampaignCluster
from ...services.campaign_service import campaign_service

router = APIRouter()

@router.get("/campaigns", response_model=List[CampaignCluster])
def get_campaigns():
    emails = db.get_all_email_details()
    return campaign_service.correlate_campaigns(emails)

@router.get("/campaigns/{campaign_id}", response_model=CampaignCluster)
def get_campaign_detail(campaign_id: str):
    emails = db.get_all_email_details()
    campaigns = campaign_service.correlate_campaigns(emails)
    for c in campaigns:
        if c.campaign_id == campaign_id:
            return c
    raise HTTPException(status_code=404, detail="Campaign not found")
