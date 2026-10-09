import React, { useState } from 'react';
import {
  Sparkles,
  Send,
  Copy,
  Check,
  Shield,
  FileCode,
  Terminal,
  Bot,
  User,
  Loader2
} from 'lucide-react';
import { invokeAiCopilot } from '../../lib/api';
import { AiCopilotResponse } from '../../lib/types';

interface AiCopilotWidgetProps {
  messageId: string;
  emailSubject: string;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  modelUsed?: string;
  yaraRule?: string;
  m365Rule?: string;
  kqlQuery?: string;
  splunkQuery?: string;
  sigmaRule?: string;
  suggestedActions?: string[];
}

export const AiCopilotWidget: React.FC<AiCopilotWidgetProps> = ({
  messageId,
  emailSubject,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'ai',
      text: `Hello Analyst. I have ingested the forensic metadata, observed headers, and threat signals for "${emailSubject}". How can I assist your incident response?`,
      modelUsed: 'PhishTrace Open-Source Gemma Security Co-Pilot',
      suggestedActions: [
        'Generate YARA rule',
        'Generate KQL hunting query',
        'Generate Splunk SPL query',
        'Generate Sigma rule',
        'Generate M365 Mail Flow rule',
        'Draft CISO incident advisory'
      ]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleSend = async (promptToSend?: string) => {
    const text = promptToSend || input;
    if (!text.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: text.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!promptToSend) setInput('');
    setLoading(true);

    try {
      const res: AiCopilotResponse = await invokeAiCopilot(messageId, text.trim());
      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: res.answer,
        modelUsed: res.model_used,
        yaraRule: res.yara_rule || undefined,
        m365Rule: res.m365_rule || undefined,
        kqlQuery: res.kql_query || undefined,
        splunkQuery: res.splunk_query || undefined,
        sigmaRule: res.sigma_rule || undefined,
        suggestedActions: res.suggested_actions,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `ai-err-${Date.now()}`,
          sender: 'ai',
          text: `Error contacting Open-Source AI Copilot: ${err.message}`,
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-[560px]">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-gradient-to-tr from-cyan-500/20 to-violet-500/20 border border-cyan-500/30 text-cyan-400">
            <Sparkles className="h-4 w-4 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              SOC AI Forensic Co-Pilot
              <span className="text-[10px] font-mono font-medium px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                Gemma Open Weights
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Context-grounded reasoning, rule generation & response drafting</p>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-3 space-y-3 pr-1 text-xs">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className="flex items-center gap-1.5 mb-1 px-1">
              {m.sender === 'user' ? (
                <>
                  <span className="text-[10px] font-mono text-slate-400">SOC Analyst</span>
                  <User className="h-3 w-3 text-cyan-400" />
                </>
              ) : (
                <>
                  <Bot className="h-3 w-3 text-violet-400" />
                  <span className="text-[10px] font-mono text-slate-400">
                    {m.modelUsed || 'PhishTrace AI'}
                  </span>
                </>
              )}
            </div>

            <div
              className={`max-w-[92%] rounded-lg p-3 leading-relaxed whitespace-pre-wrap ${
                m.sender === 'user'
                  ? 'bg-cyan-950/70 text-cyan-100 border border-cyan-800'
                  : 'bg-slate-950/80 text-slate-200 border border-slate-800'
              }`}
            >
              {m.text}

              {/* YARA Rule code block */}
              {m.yaraRule && (
                <div className="mt-3 rounded-md bg-slate-900 border border-slate-700 p-2.5">
                  <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800 text-[10px] text-cyan-400 font-mono">
                    <span className="flex items-center gap-1">
                      <FileCode className="h-3.5 w-3.5" /> YARA Detection Signature
                    </span>
                    <button
                      onClick={() => copyToClipboard(m.yaraRule!, `yara-${m.id}`)}
                      className="flex items-center gap-1 text-slate-400 hover:text-cyan-300 transition"
                    >
                      {copiedId === `yara-${m.id}` ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="font-mono text-[11px] text-emerald-300 overflow-x-auto p-1">
                    {m.yaraRule}
                  </pre>
                </div>
              )}

              {/* Microsoft Sentinel KQL block */}
              {m.kqlQuery && (
                <div className="mt-3 rounded-md bg-slate-900 border border-slate-700 p-2.5">
                  <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800 text-[10px] text-violet-400 font-mono">
                    <span className="flex items-center gap-1">
                      <Terminal className="h-3.5 w-3.5" /> Microsoft Sentinel / Defender KQL Query
                    </span>
                    <button
                      onClick={() => copyToClipboard(m.kqlQuery!, `kql-${m.id}`)}
                      className="flex items-center gap-1 text-slate-400 hover:text-violet-300 transition"
                    >
                      {copiedId === `kql-${m.id}` ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="font-mono text-[11px] text-violet-300 overflow-x-auto p-1">
                    {m.kqlQuery}
                  </pre>
                </div>
              )}

              {/* Splunk SPL block */}
              {m.splunkQuery && (
                <div className="mt-3 rounded-md bg-slate-900 border border-slate-700 p-2.5">
                  <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800 text-[10px] text-amber-400 font-mono">
                    <span className="flex items-center gap-1">
                      <Terminal className="h-3.5 w-3.5" /> Splunk SPL Hunting Query
                    </span>
                    <button
                      onClick={() => copyToClipboard(m.splunkQuery!, `splunk-${m.id}`)}
                      className="flex items-center gap-1 text-slate-400 hover:text-amber-300 transition"
                    >
                      {copiedId === `splunk-${m.id}` ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="font-mono text-[11px] text-amber-300 overflow-x-auto p-1">
                    {m.splunkQuery}
                  </pre>
                </div>
              )}

              {/* Sigma Rule block */}
              {m.sigmaRule && (
                <div className="mt-3 rounded-md bg-slate-900 border border-slate-700 p-2.5">
                  <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800 text-[10px] text-cyan-400 font-mono">
                    <span className="flex items-center gap-1">
                      <FileCode className="h-3.5 w-3.5" /> Sigma Generic Detection Rule (YAML)
                    </span>
                    <button
                      onClick={() => copyToClipboard(m.sigmaRule!, `sigma-${m.id}`)}
                      className="flex items-center gap-1 text-slate-400 hover:text-cyan-300 transition"
                    >
                      {copiedId === `sigma-${m.id}` ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="font-mono text-[11px] text-cyan-300 overflow-x-auto p-1">
                    {m.sigmaRule}
                  </pre>
                </div>
              )}

              {/* M365 PowerShell rule block */}
              {m.m365Rule && (
                <div className="mt-3 rounded-md bg-slate-900 border border-slate-700 p-2.5">
                  <div className="flex items-center justify-between mb-1.5 pb-1 border-b border-slate-800 text-[10px] text-sky-400 font-mono">
                    <span className="flex items-center gap-1">
                      <Terminal className="h-3.5 w-3.5" /> Exchange Online Transport Rule
                    </span>
                    <button
                      onClick={() => copyToClipboard(m.m365Rule!, `m365-${m.id}`)}
                      className="flex items-center gap-1 text-slate-400 hover:text-sky-300 transition"
                    >
                      {copiedId === `m365-${m.id}` ? (
                        <>
                          <Check className="h-3 w-3 text-emerald-400" /> Copied
                        </>
                      ) : (
                        <>
                          <Copy className="h-3 w-3" /> Copy
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="font-mono text-[11px] text-sky-300 overflow-x-auto p-1">
                    {m.m365Rule}
                  </pre>
                </div>
              )}
            </div>

            {/* Suggested action chips */}
            {m.suggestedActions && m.suggestedActions.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-2">
                {m.suggestedActions.map((action, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(action)}
                    className="px-2 py-0.5 rounded-full bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-[10px] transition cursor-pointer"
                  >
                    + {action}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 p-2 text-cyan-400 text-xs font-mono">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span>Gemma Open-Source Co-Pilot reasoning...</span>
          </div>
        )}
      </div>

      {/* Input bar */}
      <div className="pt-2 border-t border-slate-800 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask AI Co-Pilot (e.g. Generate YARA, explain hops, draft CISO advisory)..."
          className="flex-1 bg-slate-950 border border-slate-800 focus:border-cyan-500 rounded-lg px-3 py-2 text-xs text-slate-200 outline-none"
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          className="p-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-semibold rounded-lg disabled:opacity-40 transition cursor-pointer"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};
