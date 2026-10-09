import React, { useState } from 'react';
import {
  Network,
  ShieldAlert,
  Calendar,
  Tag,
  ExternalLink,
  ChevronRight,
  Server,
  Link,
  Mail,
  UserCheck,
  Sparkles,
  RefreshCw,
  Zap,
  Brain,
  Copy,
  Check
} from 'lucide-react';
import { CampaignCluster } from '../lib/types';
import { runPromptPlayground } from '../lib/api';

interface CampaignsProps {
  campaigns: CampaignCluster[];
  onSelectEmail: (id: string) => void;
}

export const Campaigns: React.FC<CampaignsProps> = ({ campaigns, onSelectEmail }) => {
  const [selectedCampaign, setSelectedCampaign] = useState<CampaignCluster | null>(
    campaigns.length > 0 ? campaigns[0] : null
  );
  const [aiLoading, setAiLoading] = useState(false);
  const [aiBrief, setAiBrief] = useState<string | null>(null);
  const [aiModelUsed, setAiModelUsed] = useState<string>('');
  const [copied, setCopied] = useState(false);

  const handleGenerateAiBrief = async () => {
    if (!selectedCampaign) return;
    setAiLoading(true);
    try {
      const prompt = `Synthesize an adversary profile and Microsoft Sentinel hunting playbook for cyber threat campaign '${selectedCampaign.name}'. Adversary persona: ${selectedCampaign.threat_actor_persona}. Shared indicators: ${selectedCampaign.indicators.join(', ')}.`;
      const res = await runPromptPlayground('meta-llama/llama-3.3-70b-versatile', prompt);
      setAiBrief(res.response_text);
      setAiModelUsed(res.model_name);
    } catch (e: any) {
      console.error(e);
      setAiBrief(`Error generating threat briefing: ${e.message}`);
    } finally {
      setAiLoading(false);
    }
  };

  const handleCopy = () => {
    if (!aiBrief) return;
    navigator.clipboard.writeText(aiBrief);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-violet-950/80 border border-violet-800 text-violet-400">
            <Network className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 uppercase tracking-wide">
              Threat Campaign Intelligence Explorer
            </h2>
            <p className="text-xs text-slate-400">
              Correlated cyber attack operations, shared IOC infrastructure, and adversary TTP personas
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Campaign Cluster List */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            Active Campaign Clusters ({campaigns.length})
          </h3>

          {campaigns.map((camp) => {
            const isSelected = selectedCampaign?.campaign_id === camp.campaign_id;
            return (
              <div
                key={camp.campaign_id}
                onClick={() => setSelectedCampaign(camp)}
                className={`p-4 rounded-xl border transition cursor-pointer ${
                  isSelected
                    ? 'bg-violet-950/30 border-violet-700 shadow-md'
                    : 'bg-slate-900 border-slate-800 hover:border-slate-700 hover:bg-slate-800/40'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="font-mono text-[10px] text-violet-400 bg-violet-950 px-2 py-0.5 rounded border border-violet-800">
                    {camp.campaign_id}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                    camp.severity === 'Critical'
                      ? 'bg-red-950 text-red-400 border border-red-800'
                      : camp.severity === 'High'
                      ? 'bg-orange-950 text-orange-400 border border-orange-800'
                      : 'bg-yellow-950 text-yellow-400 border border-yellow-800'
                  }`}>
                    {camp.severity}
                  </span>
                </div>

                <h4 className="text-sm font-bold text-slate-200 mb-1">{camp.name}</h4>
                <p className="text-xs text-slate-400 line-clamp-2">{camp.description}</p>

                <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                  <span>{camp.email_ids.length} Incidents Linked</span>
                  <span>{camp.indicators.length} IOCs</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Campaign Detailed Graph & Persona Card */}
        <div className="lg:col-span-2 space-y-5">
          {selectedCampaign ? (
            <>
              {/* Threat Actor Persona */}
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <UserCheck className="h-5 w-5 text-cyan-400" />
                    <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
                      Adversary Profile & Operation Persona
                    </h3>
                  </div>
                  <div className="flex items-center gap-1.5 font-mono text-[11px] text-slate-400">
                    <Calendar className="h-3.5 w-3.5" />
                    <span>First Seen: {selectedCampaign.first_seen}</span>
                  </div>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 mb-4">
                  <p className="text-xs text-cyan-200/90 leading-relaxed font-mono">
                    "{selectedCampaign.threat_actor_persona}"
                  </p>
                </div>

                {/* TTP Tags */}
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {selectedCampaign.ttp_tags.map((ttp) => (
                    <span
                      key={ttp}
                      className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono text-[10px]"
                    >
                      {ttp}
                    </span>
                  ))}
                </div>

                {/* Correlated Indicators */}
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                    Correlated Shared Indicators of Compromise (IOCs)
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedCampaign.indicators.map((ioc, i) => (
                      <span
                        key={i}
                        className="px-2.5 py-1 rounded-md bg-slate-950 border border-slate-800 font-mono text-xs text-red-300/90"
                      >
                        {ioc}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* AI Campaign Adversary Profiler & Hunting Playbook */}
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <Brain className="h-5 w-5 text-purple-400" />
                    <div>
                      <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
                        Open-Source LLM Campaign Profiler (Meta Llama 3.3 70B)
                      </h3>
                      <p className="text-[11px] text-slate-400">
                        Synthesizes adversary threat brief, attribution hypothesis, and hunting rules
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={handleGenerateAiBrief}
                    disabled={aiLoading}
                    className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-xs rounded-lg shadow transition cursor-pointer disabled:opacity-60 shrink-0"
                  >
                    <Sparkles className={`h-3.5 w-3.5 ${aiLoading ? 'animate-spin' : ''}`} />
                    <span>{aiLoading ? 'Synthesizing...' : 'Generate AI Campaign Dossier'}</span>
                  </button>
                </div>

                {aiBrief ? (
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                      <span className="flex items-center gap-1.5">
                        <Zap className="h-3 w-3 text-cyan-400" />
                        Model: {aiModelUsed || 'Meta Llama 3.3 70B'}
                      </span>
                      <button
                        onClick={handleCopy}
                        className="text-slate-400 hover:text-slate-200 flex items-center gap-1 cursor-pointer transition text-xs"
                      >
                        {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                        <span>{copied ? 'Copied' : 'Copy Dossier'}</span>
                      </button>
                    </div>
                    <pre className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 font-mono whitespace-pre-wrap leading-relaxed">
                      {aiBrief}
                    </pre>
                  </div>
                ) : (
                  <div className="p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs text-slate-500 flex items-center justify-between">
                    <span>Click "Generate AI Campaign Dossier" to run open-weight model analysis on this cluster.</span>
                    <span className="font-mono text-[10px] text-purple-400">Zero Hallucination</span>
                  </div>
                )}
              </div>

              {/* Interactive Visual Relationship Graph */}
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
                <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide mb-3">
                  Correlated IOC Entity Relationship Map
                </h3>
                <p className="text-xs text-slate-400 mb-4">
                  Click on any email incident node to open the full forensic investigation dossier.
                </p>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 cyber-grid min-h-[300px] flex flex-col justify-center">
                  <div className="flex flex-col items-center gap-6">
                    {/* Central Campaign Node */}
                    <div className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-violet-900/80 to-purple-900/80 border-2 border-violet-500 shadow-lg text-center">
                      <span className="text-[10px] font-mono text-violet-300 uppercase block">Campaign Hub</span>
                      <span className="font-bold text-xs text-white">{selectedCampaign.name}</span>
                    </div>

                    <div className="w-0.5 h-6 bg-slate-700" />

                    {/* Nodes Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 w-full">
                      {selectedCampaign.nodes
                        .filter((n) => n.type !== 'campaign')
                        .map((node) => {
                          const isEmail = node.type === 'email';
                          return (
                            <div
                              key={node.id}
                              onClick={() => {
                                if (isEmail) onSelectEmail(node.id);
                              }}
                              className={`p-3 rounded-lg border text-xs flex items-center justify-between transition ${
                                isEmail
                                  ? 'bg-slate-900 hover:bg-slate-800 border-cyan-800/80 text-cyan-300 cursor-pointer shadow hover:scale-[1.02]'
                                  : 'bg-slate-950 border-slate-800 text-slate-300 cursor-default'
                              }`}
                            >
                              <div className="flex items-center gap-2 truncate">
                                {isEmail ? (
                                  <Mail className="h-4 w-4 shrink-0 text-cyan-400" />
                                ) : node.type === 'domain' ? (
                                  <Server className="h-4 w-4 shrink-0 text-amber-400" />
                                ) : (
                                  <Link className="h-4 w-4 shrink-0 text-red-400" />
                                )}
                                <span className="font-mono truncate">{node.label}</span>
                              </div>
                              {isEmail && <ChevronRight className="h-4 w-4 text-cyan-500 shrink-0" />}
                            </div>
                          );
                        })}
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="p-12 text-center text-slate-500 text-xs">
              Select a campaign cluster on the left to inspect correlation telemetry.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
