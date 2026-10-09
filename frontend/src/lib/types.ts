export interface GeoInfo {
  ip: string;
  country?: string;
  country_code?: string;
  city?: string;
  region?: string;
  latitude?: number;
  longitude?: number;
  org?: string;
  asn?: string;
  is_private: boolean;
  source: string;
}

export interface HopInfo {
  hop_number: number;
  from_host?: string;
  by_host?: string;
  ip?: string;
  is_private: boolean;
  timestamp?: string;
  geo?: GeoInfo;
  confidence: number;
  uncertainty_reason?: string;
}

export interface HeaderForensics {
  message_id?: string;
  sender_from: string;
  sender_display_name?: string;
  sender_domain?: string;
  reply_to?: string;
  return_path?: string;
  recipient_to: string;
  subject: string;
  date: string;
  received_hops: HopInfo[];
  spf_observed?: string;
  dkim_observed?: string;
  dmarc_observed?: string;
  arc_observed?: string;
  auth_results_raw?: string;
  origin_candidate_ip?: string;
  origin_geo?: GeoInfo;
  origin_confidence: number;
  origin_caveat?: string;
}

export interface UrlIndicator {
  url: string;
  host: string;
  is_ip_literal: boolean;
  is_lookalike: boolean;
  suspicious_tld: boolean;
  anchor_mismatch: boolean;
  risk_score: number;
  risk_reasons: string[];
}

export interface AttachmentInfo {
  filename: string;
  content_type: string;
  size_bytes: number;
  sha256_hash: string;
  is_executable: boolean;
  is_double_extension: boolean;
  risk_reasons: string[];
}

export interface ThreatSignal {
  category: string;
  rule_id: string;
  description: string;
  severity: string;
  weight: number;
  evidence_quote?: string;
}

export interface RiskAssessment {
  score: number;
  category: 'Low' | 'Guarded' | 'High' | 'Critical';
  confidence: number;
  uncertainty_explanation: string;
  signals: ThreatSignal[];
  recommended_next_step: string;
}

export interface GemmaAnalysis {
  suspected_threat: string;
  summary: string;
  evidence_references: string[];
  recommended_actions: string[];
  uncertainties: string[];
  provider_mode: string;
  model_name: string;
}

export interface MitreTactic {
  tactic_id: string;
  technique: string;
  name: string;
  confidence: string;
  evidence: string;
}

export interface EmailSummary {
  id: string;
  subject: string;
  sender_from: string;
  sender_display_name?: string;
  date: string;
  risk_score: number;
  risk_category: 'Low' | 'Guarded' | 'High' | 'Critical';
  source_type: 'demo' | 'uploaded' | 'gmail_live';
  analyzed_at: string;
}

export interface EmailDetail {
  id: string;
  subject: string;
  sender_from: string;
  sender_display_name?: string;
  sender_domain?: string;
  reply_to?: string;
  recipient_to: string;
  date: string;
  original_digest: string;
  body_text_sanitized: string;
  body_html_sanitized?: string;
  headers: HeaderForensics;
  urls: UrlIndicator[];
  attachments: AttachmentInfo[];
  risk_assessment: RiskAssessment;
  gemma_analysis: GemmaAnalysis;
  mitre_tactics: MitreTactic[];
  source_type: string;
  created_at: string;
}

export interface InvestigationRecord {
  investigation_id: string;
  message_id: string;
  subject: string;
  sender: string;
  risk_score: number;
  risk_category: string;
  original_digest: string;
  export_digest: string;
  created_at: string;
  status: string;
}

export interface VerificationResult {
  investigation_id: string;
  computed_digest: string;
  stored_digest: string;
  matches: boolean;
  verified_at: string;
  details: string;
}

export interface CampaignNode {
  id: string;
  label: string;
  type: string;
  risk_level?: string;
}

export interface CampaignLink {
  source: string;
  target: string;
  relationship: string;
}

export interface CampaignCluster {
  campaign_id: string;
  name: string;
  threat_actor_persona: string;
  description: string;
  severity: string;
  indicators: string[];
  email_ids: string[];
  first_seen: string;
  last_seen: string;
  ttp_tags: string[];
  nodes: CampaignNode[];
  links: CampaignLink[];
}

export interface DashboardSummary {
  total_emails: number;
  critical_threats: number;
  high_threats: number;
  guarded_threats: number;
  low_threats: number;
  emails_requiring_review: number;
  active_campaigns: number;
  recent_investigations: InvestigationRecord[];
  risk_distribution: { name: string; count: number; color: string }[];
  gmail_status: {
    configured: boolean;
    connected: boolean;
    user_email?: string;
    last_sync?: string;
    scope: string;
    message: string;
  };
  ai_status: {
    available: boolean;
    provider: string;
    model: string;
    mode: string;
    latency_ms?: number;
    message: string;
  };
}

export interface LlmModelInfo {
  id: string;
  name: string;
  family: string;
  provider: string;
  context_window: string;
  open_source: boolean;
  description: string;
  badge: string;
}

export interface LlmEvaluation {
  model_id: string;
  model_name: string;
  threat_verdict: string;
  risk_score: number;
  confidence: number;
  reasoning: string;
  key_quote: string;
  latency_ms: number;
}

export interface LlmComparisonResult {
  message_id: string;
  consensus_verdict: string;
  consensus_score: number;
  agreement_percentage: number;
  evaluations: LlmEvaluation[];
}

export interface PromptPlaygroundResponse {
  model_id: string;
  model_name: string;
  response_text: string;
  latency_ms: number;
}

export interface AiCopilotResponse {
  answer: string;
  model_used: string;
  suggested_actions: string[];
  yara_rule?: string;
  m365_rule?: string;
  kql_query?: string;
  splunk_query?: string;
  sigma_rule?: string;
}
