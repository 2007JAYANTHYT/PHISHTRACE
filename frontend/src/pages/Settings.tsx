import React, { useState, useEffect } from 'react';
import {
  Settings as SettingsIcon,
  Cpu,
  Mail,
  ShieldCheck,
  Key,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  ExternalLink,
  Save,
  Database,
  Terminal,
  Play,
  Copy,
  Check,
  Sparkles,
  Zap,
  Layers,
  Brain,
  Quote
} from 'lucide-react';
import {
  fetchAiStatus,
  updateAiConfig,
  fetchGmailStatus,
  fetchLlmModels,
  runPromptPlayground,
  fetchEmails
} from '../lib/api';
import { LlmModelInfo, EmailSummary, PromptPlaygroundResponse } from '../lib/types';

export const Settings: React.FC = () => {
  const [aiStatus, setAiStatus] = useState<any>(null);
  const [gmailStatus, setGmailStatus] = useState<any>(null);
  const [groqKey, setGroqKey] = useState('');
  const [nvidiaKey, setNvidiaKey] = useState('');
  const [modelName, setModelName] = useState('meta/llama-3.2-11b-vision-instruct');
  const [savingAi, setSavingAi] = useState(false);
  const [aiSaveMsg, setAiSaveMsg] = useState<string | null>(null);

  // Models catalog & Prompt Studio state
  const [models, setModels] = useState<LlmModelInfo[]>([]);
  const [emails, setEmails] = useState<EmailSummary[]>([]);
  const [selectedPlaygroundModel, setSelectedPlaygroundModel] = useState<string>('google/gemma-2-9b-it');
  const [selectedEmailId, setSelectedEmailId] = useState<string>('');
  const [customPrompt, setCustomPrompt] = useState<string>(
    'Extract all suspicious indicators of compromise (IOCs) and assess attacker motivation.'
  );
  const [runningPlayground, setRunningPlayground] = useState<boolean>(false);
  const [playgroundResult, setPlaygroundResult] = useState<PromptPlaygroundResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const loadStatus = async () => {
    try {
      const ai = await fetchAiStatus();
      setAiStatus(ai);
      if (ai?.model) {
        setModelName(ai.model);
      }
      const gmail = await fetchGmailStatus();
      setGmailStatus(gmail);
      const modelList = await fetchLlmModels();
      setModels(modelList);
      if (modelList.length > 0 && !selectedPlaygroundModel) {
        setSelectedPlaygroundModel(modelList[0].id);
      }
      const emailList = await fetchEmails();
      setEmails(emailList);
      if (emailList.length > 0 && !selectedEmailId) {
        setSelectedEmailId(emailList[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleSaveAi = async () => {
    setSavingAi(true);
    setAiSaveMsg(null);
    try {
      await updateAiConfig({
        groq_api_key: groqKey || undefined,
        nvidia_api_key: nvidiaKey || undefined,
        model_name: modelName || undefined,
      });
      setAiSaveMsg('Open-Source AI configuration updated successfully.');
      await loadStatus();
    } catch (e: any) {
      setAiSaveMsg(`Error: ${e.message}`);
    } finally {
      setSavingAi(false);
    }
  };

  const handleActivateModel = async (id: string) => {
    setModelName(id);
    setSelectedPlaygroundModel(id);
    try {
      await updateAiConfig({ model_name: id });
      setAiSaveMsg(`Activated model: ${id}`);
      await loadStatus();
    } catch (e: any) {
      setAiSaveMsg(`Error activating model: ${e.message}`);
    }
  };

  const handleRunPlayground = async () => {
    if (!customPrompt.trim()) return;
    setRunningPlayground(true);
    try {
      const res = await runPromptPlayground(
        selectedPlaygroundModel,
        customPrompt,
        selectedEmailId || undefined
      );
      setPlaygroundResult(res);
    } catch (e: any) {
      console.error('Playground failed', e);
      setPlaygroundResult({
        model_id: selectedPlaygroundModel,
        model_name: selectedPlaygroundModel,
        response_text: `Error executing query: ${e.message}`,
        latency_ms: 0,
      });
    } finally {
      setRunningPlayground(false);
    }
  };

  const handleCopyResult = () => {
    if (!playgroundResult) return;
    navigator.clipboard.writeText(playgroundResult.response_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const promptPresets = [
    {
      label: '🎯 Extract Attack IOCs',
      prompt: 'Extract all indicators of compromise (IOCs), spoofed domains, and payload hashes from this message.'
    },
    {
      label: '🛡️ Synthesize Sentinel KQL Rule',
      prompt: 'Synthesize a high-fidelity Microsoft Sentinel KQL query to hunt for this threat pattern across tenant mailboxes.'
    },
    {
      label: '📜 Draft CISO Advisory',
      prompt: 'Draft an executive CISO cyber advisory detailing the threat vector, affected departments, and containment status.'
    },
    {
      label: '🧠 Deceptive Pretext Analysis',
      prompt: 'Analyze the psychological social engineering triggers, urgency drivers, and cognitive vulnerabilities exploited in this email.'
    },
    {
      label: '🔍 YARA Signature Generation',
      prompt: 'Generate an RFC 5322 compliant YARA rule to block similar spearphishing waves at the perimeter gateway.'
    }
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-950/80 border border-cyan-800 text-cyan-400">
            <SettingsIcon className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 uppercase tracking-wide">
              Settings & Intelligence Integrations
            </h2>
            <p className="text-xs text-slate-400">
              Configure Open-Source AI architectures, LLM prompt studio, Google read-only mail scopes, and forensic privacy guarantees
            </p>
          </div>
        </div>
      </div>

      {/* 1. Open-Source LLM Architecture Showcase (5 Models) */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
              Supported Open-Source & Open-Weight LLM Models ({models.length || 5})
            </h3>
          </div>
          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950 text-cyan-300 border border-cyan-800">
            Ensemble Ready
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed">
          PhishTrace natively supports and runs top open-source/open-weight models without mandatory paid API keys or bulky local weight downloads. Select any model below to activate as the primary single-model evaluator:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-1">
          {models.map((m) => {
            const isActive = (aiStatus?.model === m.id) || (modelName === m.id);
            return (
              <div
                key={m.id}
                className={`p-4 rounded-xl border transition flex flex-col justify-between ${
                  isActive
                    ? 'bg-cyan-950/20 border-cyan-500 shadow-md ring-1 ring-cyan-500/30'
                    : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-xs font-bold text-slate-100">{m.name}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-900 border border-slate-700 text-cyan-400 font-semibold">
                      {m.badge}
                    </span>
                  </div>
                  <div className="text-[11px] font-mono text-slate-400 mb-2">{m.provider}</div>
                  <p className="text-xs text-slate-300 leading-relaxed mb-3">{m.description}</p>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500 font-mono">Window: {m.context_window}</span>
                  <button
                    onClick={() => handleActivateModel(m.id)}
                    className={`px-2.5 py-1 rounded text-xs font-semibold transition cursor-pointer ${
                      isActive
                        ? 'bg-cyan-500 text-slate-950'
                        : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                    }`}
                  >
                    {isActive ? 'Active Engine' : 'Activate'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 2. Interactive SOC LLM Prompt Studio & Experimentation Sandbox */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Terminal className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
              SOC LLM Prompt Studio & Experimentation Sandbox
            </h3>
          </div>
          <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-purple-950 text-purple-300 border border-purple-800">
            Interactive Testing
          </span>
        </div>

        <p className="text-xs text-slate-400 leading-relaxed">
          Test cybersecurity prompts against any supported open-source LLM. You can bind queries to an uploaded email context to extract IOCs, write detection rules, or summarize attack vectors in real-time.
        </p>

        {/* Model and Context Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Target Open-Source Model</label>
            <select
              value={selectedPlaygroundModel}
              onChange={(e) => setSelectedPlaygroundModel(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono"
            >
              {models.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name} ({m.family})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Email Context Anchor (Optional)</label>
            <select
              value={selectedEmailId}
              onChange={(e) => setSelectedEmailId(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono"
            >
              <option value="">None (Generic Cybersecurity Prompt)</option>
              {emails.map((em) => (
                <option key={em.id} value={em.id}>
                  {em.subject} ({em.risk_category} - {em.risk_score}/100)
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Quick Presets */}
        <div>
          <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            Quick Cybersecurity Prompt Presets
          </label>
          <div className="flex flex-wrap gap-2">
            {promptPresets.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => setCustomPrompt(preset.prompt)}
                className="px-2.5 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 text-[11px] transition cursor-pointer font-medium"
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        {/* Prompt Input */}
        <div>
          <label className="block text-slate-300 font-medium mb-1 text-xs">Prompt Instruction</label>
          <textarea
            rows={3}
            value={customPrompt}
            onChange={(e) => setCustomPrompt(e.target.value)}
            placeholder="Ask the LLM to inspect, decode, or generate threat artifacts..."
            className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono text-xs leading-relaxed"
          />
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-between">
          <button
            onClick={handleRunPlayground}
            disabled={runningPlayground || !customPrompt.trim()}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-bold text-xs rounded-lg shadow transition cursor-pointer disabled:opacity-50"
          >
            {runningPlayground ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4 fill-slate-950" />
            )}
            <span>{runningPlayground ? 'Inferring with Model...' : 'Execute Open-Source LLM Prompt'}</span>
          </button>
          <span className="text-[11px] text-slate-500 font-mono">
            Zero Local Weights Download Required
          </span>
        </div>

        {/* Output Area */}
        {playgroundResult && (
          <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-200">{playgroundResult.model_name}</span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center gap-1">
                  <Zap className="h-2.5 w-2.5" />
                  {playgroundResult.latency_ms}ms
                </span>
              </div>
              <button
                onClick={handleCopyResult}
                className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1 cursor-pointer transition"
              >
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>

            <pre className="text-xs font-mono text-slate-300 bg-slate-900/60 p-3.5 rounded-lg overflow-x-auto whitespace-pre-wrap leading-relaxed border border-slate-800/80">
              {playgroundResult.response_text}
            </pre>
          </div>
        )}
      </div>

      {/* 3. Provider Keys & Configuration */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Cpu className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
              Cloud Inference Provider Credentials (Optional)
            </h3>
          </div>
          {aiStatus && (
            <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-950 text-cyan-300 border border-cyan-800">
              {aiStatus.mode}
            </span>
          )}
        </div>

        {aiStatus && (
          <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Active Provider:</span>
              <span className="font-mono text-cyan-400 font-semibold">{aiStatus.provider}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Active Model Identifier:</span>
              <span className="font-mono text-slate-200">{aiStatus.model}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Inference Mode:</span>
              <span className="text-emerald-400 font-medium">Zero-Latency Deterministic Pipeline</span>
            </div>
            <p className="pt-1 text-[11px] text-slate-400 border-t border-slate-800/80">
              {aiStatus.message}
            </p>
          </div>
        )}

        <div className="space-y-3 pt-2 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">
              Groq API Key (Optional — Free Ultra-Fast Open-Source Gemma 2-9B)
            </label>
            <input
              type="password"
              value={groqKey}
              onChange={(e) => setGroqKey(e.target.value)}
              placeholder="gsk_..."
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">
              NVIDIA NIM API Key (Active Cloud Accelerator — nvapi-...)
            </label>
            <input
              type="password"
              value={nvidiaKey}
              onChange={(e) => setNvidiaKey(e.target.value)}
              placeholder="nvapi-..."
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">
              Custom Model Identifier
            </label>
            <input
              type="text"
              value={modelName}
              onChange={(e) => setModelName(e.target.value)}
              placeholder="google/gemma-2-9b-it"
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg text-slate-200 outline-none font-mono"
            />
          </div>

          {aiSaveMsg && (
            <div className="p-2.5 rounded bg-slate-950 border border-slate-800 text-xs text-cyan-300">
              {aiSaveMsg}
            </div>
          )}

          <button
            onClick={handleSaveAi}
            disabled={savingAi}
            className="flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-bold text-xs rounded-lg shadow transition cursor-pointer"
          >
            <Save className="h-4 w-4" />
            <span>{savingAi ? 'Saving...' : 'Apply Open-Source AI Settings'}</span>
          </button>
        </div>
      </div>

      {/* 4. Gmail Integration Settings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Mail className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
              Gmail Ingestion (Read-Only OAuth Scope)
            </h3>
          </div>
          {gmailStatus && (
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
              gmailStatus.connected
                ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}>
              {gmailStatus.connected ? 'Connected' : 'Offline Demo Mode'}
            </span>
          )}
        </div>

        {gmailStatus && (
          <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">OAuth Scope:</span>
              <code className="text-cyan-400 font-mono text-[11px]">{gmailStatus.scope}</code>
            </div>
            <p className="pt-1 text-[11px] text-slate-400">
              {gmailStatus.message}
            </p>
          </div>
        )}

        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-xs text-slate-400">
          <p className="leading-relaxed">
            <span className="font-semibold text-slate-300">Privacy Safeguard: </span>
            PhishTrace only requests the minimum read-only scope (<code className="text-cyan-400">gmail.readonly</code>). 
            It never requests permission to modify, send, quarantine, or delete messages in your mailbox. 
            When credentials are empty, the entire app functions offline using RFC <code className="text-cyan-400">.eml</code> uploads.
          </p>
        </div>
      </div>

      {/* 5. Security & Forensics Architecture Guarantees */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-3 text-xs">
        <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
          <ShieldCheck className="h-5 w-5 text-emerald-400" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
            Platform Privacy & Compliance Contract
          </h3>
        </div>

        <ul className="space-y-2 text-slate-300">
          <li className="flex items-start gap-2">
            <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>RFC1918 Private IP Isolation:</strong> Loopback and internal subnet addresses (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are strictly excluded from public geolocation lookups.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Zero Weapon Execution Sandbox:</strong> Email attachments, scripts, and embedded objects are never executed; HTML preview is actively sanitized against malicious triggers.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>SHA-256 Evidence Chain:</strong> Original raw message digests are computed before transformations to support immutable forensic audits.</span>
          </li>
        </ul>
      </div>
    </div>
  );
};
