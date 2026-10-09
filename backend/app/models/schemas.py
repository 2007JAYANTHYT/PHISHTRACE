from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GeoInfo(BaseModel):
    ip: str
    country: Optional[str] = "Unknown"
    country_code: Optional[str] = ""
    city: Optional[str] = "Unknown"
    region: Optional[str] = "Unknown"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    org: Optional[str] = "Unknown"
    asn: Optional[str] = "Unknown"
    is_private: bool = False
    source: str = "Local Cache / Public DB"

class HopInfo(BaseModel):
    hop_number: int
    from_host: Optional[str] = "unknown"
    by_host: Optional[str] = "unknown"
    ip: Optional[str] = None
    is_private: bool = False
    timestamp: Optional[str] = None
    geo: Optional[GeoInfo] = None
    confidence: float = Field(0.0, description="Confidence score 0.0 - 1.0")
    uncertainty_reason: Optional[str] = None

class HeaderForensics(BaseModel):
    message_id: Optional[str] = None
    sender_from: str
    sender_display_name: Optional[str] = None
    sender_domain: Optional[str] = None
    reply_to: Optional[str] = None
    return_path: Optional[str] = None
    recipient_to: str
    subject: str
    date: str
    received_hops: List[HopInfo] = []
    
    # Observed headers vs independently verified
    spf_observed: Optional[str] = "none" # pass, fail, softfail, neutral, none
    dkim_observed: Optional[str] = "none"
    dmarc_observed: Optional[str] = "none"
    arc_observed: Optional[str] = "none"
    auth_results_raw: Optional[str] = None
    
    origin_candidate_ip: Optional[str] = None
    origin_geo: Optional[GeoInfo] = None
    origin_confidence: float = 0.0
    origin_caveat: Optional[str] = None

class UrlIndicator(BaseModel):
    url: str
    host: str
    is_ip_literal: bool = False
    is_lookalike: bool = False
    suspicious_tld: bool = False
    anchor_mismatch: bool = False
    risk_score: int = 0
    risk_reasons: List[str] = []

class AttachmentInfo(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    sha256_hash: str
    is_executable: bool = False
    is_double_extension: bool = False
    risk_reasons: List[str] = []

class ThreatSignal(BaseModel):
    category: str # "authentication", "impersonation", "content_urgency", "malicious_url", "attachment", "reputation"
    rule_id: str
    description: str
    severity: str # "low", "medium", "high", "critical"
    weight: int
    evidence_quote: Optional[str] = None

class RiskAssessment(BaseModel):
    score: int = Field(..., ge=0, le=100)
    category: str # "Low", "Guarded", "High", "Critical"
    confidence: float = Field(..., ge=0.0, le=1.0)
    uncertainty_explanation: str
    signals: List[ThreatSignal] = []
    recommended_next_step: str

class GemmaAnalysis(BaseModel):
    model_config = {"protected_namespaces": ()}
    suspected_threat: str
    summary: str
    evidence_references: List[str]
    recommended_actions: List[str]
    uncertainties: List[str]
    provider_mode: str = "Deterministic Open-Source Fallback" # or "Gemma 4 / Hugging Face Open Weights"
    model_name: str = "google/gemma-2-9b-it"

class MitreTactic(BaseModel):
    tactic_id: str
    technique: str
    name: str
    confidence: str
    evidence: str

class LlmModelInfo(BaseModel):
    model_config = {"protected_namespaces": ()}
    id: str
    name: str
    family: str
    provider: str
    context_window: str
    open_source: bool
    description: str
    badge: str

class LlmEvaluation(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: str
    model_name: str
    threat_verdict: str
    risk_score: int
    confidence: float
    reasoning: str
    key_quote: str
    latency_ms: float

class LlmComparisonResult(BaseModel):
    model_config = {"protected_namespaces": ()}
    message_id: str
    consensus_verdict: str
    consensus_score: int
    agreement_percentage: int
    evaluations: List[LlmEvaluation]

class PromptPlaygroundRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: str
    message_id: Optional[str] = None
    user_prompt: str

class PromptPlaygroundResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: str
    model_name: str
    response_text: str
    latency_ms: float

class AiCopilotMessage(BaseModel):
    role: str # "user", "assistant", "system"
    content: str
    timestamp: Optional[str] = None

class AiCopilotRequest(BaseModel):
    message_id: str
    user_prompt: str
    conversation_history: List[Dict[str, str]] = []

class AiCopilotResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    answer: str
    model_used: str
    suggested_actions: List[str] = []
    yara_rule: Optional[str] = None
    m365_rule: Optional[str] = None
    kql_query: Optional[str] = None
    splunk_query: Optional[str] = None
    sigma_rule: Optional[str] = None

class EmailSummary(BaseModel):
    id: str
    subject: str
    sender_from: str
    sender_display_name: Optional[str] = None
    date: str
    risk_score: int
    risk_category: str
    source_type: str = "demo" # "demo", "uploaded", "gmail_live"
    analyzed_at: str

class EmailDetail(BaseModel):
    id: str
    subject: str
    sender_from: str
    sender_display_name: Optional[str] = None
    sender_domain: Optional[str] = None
    reply_to: Optional[str] = None
    recipient_to: str
    date: str
    original_digest: str
    body_text_sanitized: str
    body_html_sanitized: Optional[str] = None
    headers: HeaderForensics
    urls: List[UrlIndicator] = []
    attachments: List[AttachmentInfo] = []
    risk_assessment: RiskAssessment
    gemma_analysis: GemmaAnalysis
    mitre_tactics: List[MitreTactic] = []
    source_type: str = "demo"
    created_at: str

class InvestigationRecord(BaseModel):
    investigation_id: str
    message_id: str
    subject: str
    sender: str
    risk_score: int
    risk_category: str
    original_digest: str
    export_digest: str
    created_at: str
    status: str = "Verified"

class VerificationResult(BaseModel):
    investigation_id: str
    computed_digest: str
    stored_digest: str
    matches: bool
    verified_at: str
    details: str

class CampaignNode(BaseModel):
    id: str
    label: str
    type: str # "email", "domain", "url", "ip", "hash"
    risk_level: Optional[str] = None

class CampaignLink(BaseModel):
    source: str
    target: str
    relationship: str # "sent_from", "contains_url", "shares_attachment", "originates_at"

class CampaignCluster(BaseModel):
    campaign_id: str
    name: str
    threat_actor_persona: str
    description: str
    severity: str
    indicators: List[str]
    email_ids: List[str]
    first_seen: str
    last_seen: str
    ttp_tags: List[str]
    nodes: List[CampaignNode] = []
    links: List[CampaignLink] = []

class DashboardSummary(BaseModel):
    total_emails: int
    critical_threats: int
    high_threats: int
    guarded_threats: int
    low_threats: int
    emails_requiring_review: int
    active_campaigns: int
    recent_investigations: List[InvestigationRecord]
    risk_distribution: List[Dict[str, Any]]
    gmail_status: Dict[str, Any]
    ai_status: Dict[str, Any]

class AiStatus(BaseModel):
    model_config = {"protected_namespaces": ()}
    available: bool
    provider: str
    model: str
    mode: str
    latency_ms: Optional[float] = None
    message: str

class GmailStatus(BaseModel):
    configured: bool
    connected: bool
    user_email: Optional[str] = None
    last_sync: Optional[str] = None
    scope: str
    message: str
