import React from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  CheckCircle,
  Network,
  Cpu,
  Mail,
  ArrowRight,
  TrendingUp,
  FileSearch,
  ExternalLink,
  ShieldCheck
} from 'lucide-react';
import { DashboardSummary, InvestigationRecord } from '../lib/types';

interface DashboardProps {
  summary: DashboardSummary | null;
  onNavigateToEmail: (messageId: string) => void;
  onNavigateTab: (tab: string) => void;
  onQuickUpload: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  summary,
  onNavigateToEmail,
  onNavigateTab,
  onQuickUpload,
}) => {
  if (!summary) {
    return (
      <div className="py-20 text-center text-slate-400">
        <div className="animate-spin h-8 w-8 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-xs font-mono">Loading Security Operations Center Telemetry...</p>
      </div>
    );
  }

  const getRiskColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'critical':
        return 'text-red-400 bg-red-950/60 border-red-800';
      case 'high':
        return 'text-orange-400 bg-orange-950/60 border-orange-800';
      case 'guarded':
        return 'text-yellow-400 bg-yellow-950/60 border-yellow-800';
      default:
        return 'text-emerald-400 bg-emerald-950/60 border-emerald-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner / Mission Header */}
      <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 p-6 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-mono uppercase tracking-wider">
                Threat Intelligence Live
              </span>
              <span className="text-xs text-slate-400 font-mono">Hacktoberfest Bengaluru 2026</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">
              PhishTrace Security Operations Center
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              AI-driven email forensics, hop-by-hop origin tracing, explainable threat scoring, and cryptographic evidence verification.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onQuickUpload}
              className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-bold text-xs rounded-lg shadow-lg shadow-cyan-600/20 transition cursor-pointer"
            >
              Analyze Email (.EML)
            </button>
            <button
              onClick={() => onNavigateTab('campaigns')}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs rounded-lg border border-slate-700 transition cursor-pointer"
            >
              Campaign Graph
            </button>
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Evaluated</span>
            <FileSearch className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-slate-100">{summary.total_emails}</div>
          <p className="text-[11px] text-slate-500 mt-1">Processed RFC messages</p>
        </div>

        <div className="bg-slate-900/90 border border-red-900/60 rounded-xl p-4 shadow relative overflow-hidden">
          <div className="flex items-center justify-between text-red-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Critical Threats</span>
            <ShieldAlert className="h-4 w-4 text-red-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-red-400">{summary.critical_threats}</div>
          <p className="text-[11px] text-red-300/70 mt-1">Immediate quarantine required</p>
        </div>

        <div className="bg-slate-900/90 border border-orange-900/60 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between text-orange-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">High Risk</span>
            <AlertTriangle className="h-4 w-4 text-orange-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-orange-400">{summary.high_threats}</div>
          <p className="text-[11px] text-orange-300/70 mt-1">Under analyst scrutiny</p>
        </div>

        <div className="bg-slate-900/90 border border-violet-900/60 rounded-xl p-4 shadow">
          <div className="flex items-center justify-between text-violet-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Threat Campaigns</span>
            <Network className="h-4 w-4 text-violet-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-violet-400">{summary.active_campaigns}</div>
          <p className="text-[11px] text-violet-300/70 mt-1">Correlated attacker networks</p>
        </div>
      </div>

      {/* Real-Time Integration & AI Status Banners */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Open-Source AI status */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex items-start gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-950 border border-cyan-800 text-cyan-400 shrink-0">
            <Cpu className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">5-Model Open-Source LLM Ensemble</h4>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-800">
                Active & Grounded
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium mt-0.5">Google Gemma 2 • Meta Llama 3.3 • Mistral 7B • Qwen 2.5 • Cyber Engine</p>
            <div className="flex items-center justify-between mt-1 pt-1 border-t border-slate-800">
              <span className="text-[11px] text-cyan-400 font-mono">Consensus Agreement Engine</span>
              <button
                onClick={() => onNavigateTab('settings')}
                className="text-[11px] text-cyan-400 hover:text-cyan-300 font-semibold cursor-pointer"
              >
                Launch Prompt Studio →
              </button>
            </div>
          </div>
        </div>

        {/* Gmail status */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex items-start gap-3">
          <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-400 shrink-0">
            <Mail className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">Gmail Read-Only Ingestion</h4>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                summary.gmail_status.connected
                  ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                  : 'bg-slate-800 text-slate-400 border-slate-700'
              }`}>
                {summary.gmail_status.connected ? 'OAuth Connected' : 'Seed & .EML Mode'}
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium mt-0.5">
              {summary.gmail_status.connected ? summary.gmail_status.user_email : 'Offline Demo Mode Active'}
            </p>
            <p className="text-[11px] text-slate-400 mt-1 font-mono">{summary.gmail_status.message}</p>
          </div>
        </div>
      </div>

      {/* Threat Distribution Bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">
          Threat Classification Distribution
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {summary.risk_distribution.map((d) => (
            <div key={d.name} className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80">
              <div className="flex items-center justify-between mb-1 text-xs">
                <span className="font-medium text-slate-300">{d.name}</span>
                <span className="font-mono font-bold" style={{ color: d.color }}>{d.count}</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    backgroundColor: d.color,
                    width: `${summary.total_emails > 0 ? (d.count / summary.total_emails) * 100 : 0}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Forensic Investigations Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wide">
              Recent Forensic Investigations
            </h3>
            <p className="text-xs text-slate-400">Cryptographically hashed evidence records and threat ratings</p>
          </div>
          <button
            onClick={() => onNavigateTab('inbox')}
            className="flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 font-medium transition cursor-pointer"
          >
            <span>View All Inbox</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-mono text-[11px]">
                <th className="py-2.5 px-3">Investigation ID</th>
                <th className="py-2.5 px-3">Subject</th>
                <th className="py-2.5 px-3">Sender</th>
                <th className="py-2.5 px-3">Risk Verdict</th>
                <th className="py-2.5 px-3">SHA-256 Digest</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {summary.recent_investigations.map((inv) => (
                <tr key={inv.investigation_id} className="hover:bg-slate-800/40 transition">
                  <td className="py-2.5 px-3 font-mono text-cyan-400 font-medium">{inv.investigation_id}</td>
                  <td className="py-2.5 px-3 font-medium text-slate-200 max-w-xs truncate">{inv.subject}</td>
                  <td className="py-2.5 px-3 text-slate-400 max-w-xs truncate">{inv.sender}</td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getRiskColor(inv.risk_category)}`}>
                      {inv.risk_category} ({inv.risk_score})
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono text-slate-500 text-[10px]">
                    {inv.original_digest.slice(0, 12)}...
                  </td>
                  <td className="py-2.5 px-3 text-right">
                    <button
                      onClick={() => onNavigateToEmail(inv.message_id)}
                      className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-medium transition cursor-pointer"
                    >
                      Investigate
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
