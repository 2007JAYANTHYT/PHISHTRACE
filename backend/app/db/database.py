from typing import Dict, List, Optional
from ..models.schemas import EmailDetail, EmailSummary

class Database:
    def __init__(self):
        self._emails: Dict[str, EmailDetail] = {}

    def get_email(self, email_id: str) -> Optional[EmailDetail]:
        return self._emails.get(email_id)

    def list_emails(self) -> List[EmailSummary]:
        summaries = []
        for e in self._emails.values():
            summaries.append(EmailSummary(
                id=e.id,
                subject=e.subject,
                sender_from=e.sender_from,
                sender_display_name=e.sender_display_name,
                date=e.date,
                risk_score=e.risk_assessment.score,
                risk_category=e.risk_assessment.category,
                source_type=e.source_type,
                analyzed_at=e.created_at
            ))
        return sorted(summaries, key=lambda s: s.analyzed_at, reverse=True)

    def save_email(self, email: EmailDetail):
        self._emails[email.id] = email

    def get_all_email_details(self) -> List[EmailDetail]:
        return list(self._emails.values())

    def clear(self):
        self._emails.clear()

db = Database()
