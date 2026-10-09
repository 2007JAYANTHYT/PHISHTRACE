import React from 'react';
import {
  ShieldAlert,
  Inbox,
  LayoutDashboard,
  Network,
  Lock,
  Settings,
  Cpu,
  Mail,
  Upload,
  RefreshCw
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  aiMode: string;
  activeModel?: string;
  onSelectModel?: (modelId: string) => void;
  gmailConnected: boolean;
  onQuickUpload: () => void;
  onRefresh: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  aiMode,
  activeModel = 'google/gemma-2-9b-it',
  onSelectModel,
  gmailConnected,
  onQuickUpload,
  onRefresh
}) => {
  const [modelDropdownOpen, setModelDropdownOpen] = React.useState(false);

  const modelsList = [
    { id: 'google/gemma-2-9b-it', name: 'Gemma 2 9B (Open Weights)', tag: 'Google' },
    { id: 'meta/llama-3.3-70b-versatile', name: 'Llama 3.3 70B (High Reasoning)', tag: 'Meta' },
    { id: 'mistralai/Mistral-7B-Instruct-v0.3', name: 'Mistral 7B (Ultra Fast)', tag: 'Mistral' },
    { id: 'qwen/qwen-2.5-7b-instruct', name: 'Qwen 2.5 7B (Code & YARA)', tag: 'Alibaba' },
    { id: 'phishtrace/cyber-forensics-nlp', name: 'Cyber Forensics Engine', tag: 'Zero-Latency' },
  ];

  const navItems = [
    { id: 'dashboard', label: 'SOC Dashboard', icon: LayoutDashboard },
    { id: 'inbox', label: 'Triage Inbox', icon: Inbox },
    { id: 'investigation', label: 'Investigation Workspace', icon: ShieldAlert },
    { id: 'campaigns', label: 'Campaign Explorer', icon: Network },
    { id: 'evidence', label: 'Evidence Vault', icon: Lock },
    { id: 'settings', label: 'Settings & AI', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-cyan-500 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <ShieldAlert className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg tracking-wider text-slate-100 uppercase">PhishTrace</span>
                <span className="px-1.5 py-0.5 text-[10px] font-mono font-semibold rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                  SOC v1.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-mono tracking-tight">AI Threat Intel & Forensic Platform</p>
            </div>
          </div>

          {/* Navigation tabs */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-slate-800 text-cyan-400 border border-slate-700 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Actions & Status Pills */}
          <div className="flex items-center gap-2.5">
            {/* Interactive LLM Model Selector Dropdown */}
            <div className="relative">
              <button
                onClick={() => setModelDropdownOpen(!modelDropdownOpen)}
                className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs transition cursor-pointer"
                title="Select Active LLM Model"
              >
                <Cpu className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
                <span className="text-slate-400 text-[11px]">LLM:</span>
                <span className="font-mono text-cyan-300 text-[11px] font-medium truncate max-w-[130px]">
                  {modelsList.find((m) => m.id === activeModel)?.tag || 'Gemma'}
                </span>
              </button>

              {modelDropdownOpen && (
                <div className="absolute right-0 mt-2 w-72 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-2 z-50 text-xs">
                  <div className="px-2 py-1 text-[10px] font-mono font-bold text-slate-400 uppercase border-b border-slate-800 mb-1">
                    Select Active Cyber LLM
                  </div>
                  {modelsList.map((m) => (
                    <button
                      key={m.id}
                      onClick={() => {
                        onSelectModel?.(m.id);
                        setModelDropdownOpen(false);
                      }}
                      className={`w-full text-left px-2.5 py-1.5 rounded-lg flex items-center justify-between transition cursor-pointer ${
                        activeModel === m.id
                          ? 'bg-cyan-950 text-cyan-300 font-bold border border-cyan-800'
                          : 'hover:bg-slate-800 text-slate-300'
                      }`}
                    >
                      <span className="truncate">{m.name}</span>
                      <span className="text-[9px] font-mono px-1 rounded bg-slate-800 text-slate-400 ml-1">
                        {m.tag}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Gmail integration badge */}
            <div
              className={`hidden sm:flex items-center gap-1.5 px-2 py-1 rounded text-[11px] font-mono border ${
                gmailConnected
                  ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400'
                  : 'bg-slate-900 border-slate-800 text-slate-400'
              }`}
              title={gmailConnected ? 'Live Gmail Read-Only Connected' : 'Gmail Inactive (Using Seed & .EML Upload)'}
            >
              <Mail className="h-3 w-3" />
              <span>{gmailConnected ? 'Gmail Live' : 'Demo Mode'}</span>
            </div>

            {/* Quick Upload action */}
            <button
              onClick={onQuickUpload}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-semibold text-xs rounded shadow-md transition-all cursor-pointer"
            >
              <Upload className="h-3.5 w-3.5" />
              <span>Analyze .EML</span>
            </button>

            {/* Refresh */}
            <button
              onClick={onRefresh}
              className="p-1.5 text-slate-400 hover:text-cyan-400 hover:bg-slate-800 rounded transition cursor-pointer"
              title="Refresh Telemetry"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
