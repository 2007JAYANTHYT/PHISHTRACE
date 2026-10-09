import React, { useState } from 'react';
import {
  Search,
  Filter,
  Upload,
  ShieldAlert,
  AlertTriangle,
  CheckCircle,
  FileText,
  Calendar,
  User,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { EmailSummary } from '../lib/types';

interface InboxProps {
  emails: EmailSummary[];
  onSelectEmail: (id: string) => void;
  onQuickUpload: () => void;
  loading: boolean;
}

export const Inbox: React.FC<InboxProps> = ({
  emails,
  onSelectEmail,
  onQuickUpload,
  loading,
}) => {
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All');

  const filtered = emails.filter((e) => {
    const matchesSearch =
      search === '' ||
      e.subject.toLowerCase().includes(search.toLowerCase()) ||
      e.sender_from.toLowerCase().includes(search.toLowerCase());

    const matchesCategory =
      categoryFilter === 'All' || e.risk_category.toLowerCase() === categoryFilter.toLowerCase();

    return matchesSearch && matchesCategory;
  });

  const getRiskBadge = (cat: string, score: number) => {
    switch (cat.toLowerCase()) {
      case 'critical':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-red-950/80 border border-red-800 text-red-400 flex items-center gap-1">
            <ShieldAlert className="h-3 w-3" /> Critical ({score})
          </span>
        );
      case 'high':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-orange-950/80 border border-orange-800 text-orange-400 flex items-center gap-1">
            <AlertTriangle className="h-3 w-3" /> High ({score})
          </span>
        );
      case 'guarded':
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-yellow-950/80 border border-yellow-800 text-yellow-400 flex items-center gap-1">
            <AlertTriangle className="h-3 w-3" /> Guarded ({score})
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-emerald-950/80 border border-emerald-800 text-emerald-400 flex items-center gap-1">
            <CheckCircle className="h-3 w-3" /> Low ({score})
          </span>
        );
    }
  };

  return (
    <div className="space-y-5">
      {/* Top Header & Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
        <div>
          <h2 className="text-lg font-bold text-slate-100 uppercase tracking-wide">
            Email Threat Ingestion & Triage Inbox
          </h2>
          <p className="text-xs text-slate-400">
            Real-time feed of parsed messages, detection ratings, and investigation triggers
          </p>
        </div>

        <button
          onClick={onQuickUpload}
          className="flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-slate-950 font-bold text-xs rounded-lg shadow transition cursor-pointer self-start sm:self-auto"
        >
          <Upload className="h-4 w-4" />
          <span>Upload & Analyze .EML</span>
        </button>
      </div>

      {/* Filter and Search Controls */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Search Input */}
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by subject, sender, or domain..."
            className="w-full pl-9 pr-3 py-2 bg-slate-900 border border-slate-800 focus:border-cyan-500 rounded-lg text-xs text-slate-200 outline-none"
          />
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
          {['All', 'Critical', 'High', 'Guarded', 'Low'].map((cat) => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition cursor-pointer shrink-0 ${
                categoryFilter === cat
                  ? 'bg-cyan-950 border border-cyan-700 text-cyan-300 font-bold'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Email Feed Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow">
        {loading ? (
          <div className="py-20 text-center text-slate-500 text-xs">
            <div className="animate-spin h-6 w-6 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto mb-2" />
            <span>Scanning inbox telemetry...</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-16 text-center text-slate-500 text-xs">
            <FileText className="h-8 w-8 mx-auto text-slate-600 mb-2" />
            <p>No email messages match your filter query.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-mono text-[11px] bg-slate-950/40">
                  <th className="py-3 px-4">Threat Verdict</th>
                  <th className="py-3 px-4">Sender / Display Name</th>
                  <th className="py-3 px-4">Subject</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Source</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filtered.map((item) => (
                  <tr
                    key={item.id}
                    onClick={() => onSelectEmail(item.id)}
                    className="hover:bg-slate-800/40 transition cursor-pointer"
                  >
                    <td className="py-3 px-4 whitespace-nowrap">
                      {getRiskBadge(item.risk_category, item.risk_score)}
                    </td>
                    <td className="py-3 px-4 max-w-xs">
                      <div className="font-semibold text-slate-200 truncate">
                        {item.sender_display_name || item.sender_from}
                      </div>
                      <div className="text-[11px] font-mono text-slate-400 truncate">
                        {item.sender_from}
                      </div>
                    </td>
                    <td className="py-3 px-4 max-w-md">
                      <div className="font-medium text-slate-200 truncate">
                        {item.subject}
                      </div>
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-400 whitespace-nowrap text-[11px]">
                      {item.date}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                        item.source_type === 'gmail_live'
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                          : item.source_type === 'uploaded'
                          ? 'bg-cyan-950 text-cyan-400 border border-cyan-800'
                          : 'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}>
                        {item.source_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectEmail(item.id);
                        }}
                        className="px-3 py-1.5 rounded bg-slate-800 hover:bg-cyan-950 hover:text-cyan-300 hover:border-cyan-700 border border-slate-700 text-slate-200 text-xs font-medium transition cursor-pointer"
                      >
                        Deep Forensic
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
