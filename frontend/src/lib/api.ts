import {
  DashboardSummary,
  EmailSummary,
  EmailDetail,
  CampaignCluster,
  InvestigationRecord,
  VerificationResult,
  AiCopilotResponse
} from './types';
const RAW_API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');
const API_BASE = RAW_API_URL ? `${RAW_API_URL}/api` : '/api';

export async function fetchDashboard(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE}/dashboard/summary`);
  if (!res.ok) throw new Error(`Failed to fetch dashboard: ${res.statusText}`);
  return res.json();
}

export async function fetchEmails(category?: string, search?: string): Promise<EmailSummary[]> {
  const params = new URLSearchParams();
  if (category && category !== 'All') params.append('category', category);
  if (search) params.append('search', search);

  const url = `${API_BASE}/emails${params.toString() ? `?${params.toString()}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch emails: ${res.statusText}`);
  return res.json();
}

export async function fetchEmailDetail(id: string): Promise<EmailDetail> {
  const res = await fetch(`${API_BASE}/emails/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch email detail: ${res.statusText}`);
  return res.json();
}

export async function uploadEmlFile(file: File): Promise<EmailDetail> {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/emails/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to upload email');
  }
  return res.json();
}

export async function reanalyzeEmail(id: string): Promise<EmailDetail> {
  const res = await fetch(`${API_BASE}/emails/${id}/analyze`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to reanalyze email: ${res.statusText}`);
  return res.json();
}

export async function fetchCampaigns(): Promise<CampaignCluster[]> {
  const res = await fetch(`${API_BASE}/campaigns`);
  if (!res.ok) throw new Error(`Failed to fetch campaigns: ${res.statusText}`);
  return res.json();
}

export async function fetchEvidenceList(): Promise<InvestigationRecord[]> {
  const res = await fetch(`${API_BASE}/evidence`);
  if (!res.ok) throw new Error(`Failed to fetch evidence records: ${res.statusText}`);
  return res.json();
}

export async function verifyEvidence(investigationId: string): Promise<VerificationResult> {
  const res = await fetch(`${API_BASE}/evidence/${investigationId}/verify`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to verify evidence: ${res.statusText}`);
  return res.json();
}

export async function fetchAiStatus() {
  const res = await fetch(`${API_BASE}/ai/status`);
  if (!res.ok) throw new Error(`Failed to fetch AI status: ${res.statusText}`);
  return res.json();
}

export async function updateAiConfig(config: { groq_api_key?: string; nvidia_api_key?: string; model_name?: string }) {
  const res = await fetch(`${API_BASE}/ai/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });
  if (!res.ok) throw new Error(`Failed to update AI config: ${res.statusText}`);
  return res.json();
}

export async function invokeAiCopilot(messageId: string, prompt: string): Promise<AiCopilotResponse> {
  const res = await fetch(`${API_BASE}/ai/copilot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message_id: messageId, user_prompt: prompt }),
  });
  if (!res.ok) throw new Error(`Failed to invoke AI Copilot: ${res.statusText}`);
  return res.json();
}

export async function fetchLlmModels(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/ai/models`);
  if (!res.ok) throw new Error(`Failed to fetch LLM models: ${res.statusText}`);
  return res.json();
}

export async function compareLlmModels(messageId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/ai/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message_id: messageId }),
  });
  if (!res.ok) throw new Error(`Failed to compare LLM models: ${res.statusText}`);
  return res.json();
}

export async function runPromptPlayground(modelId: string, prompt: string, messageId?: string): Promise<any> {
  const res = await fetch(`${API_BASE}/ai/playground`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model_id: modelId, user_prompt: prompt, message_id: messageId }),
  });
  if (!res.ok) throw new Error(`Failed to run prompt playground: ${res.statusText}`);
  return res.json();
}

export async function fetchGmailStatus() {
  const res = await fetch(`${API_BASE}/integrations/gmail/status`);
  if (!res.ok) throw new Error(`Failed to fetch Gmail status: ${res.statusText}`);
  return res.json();
}
