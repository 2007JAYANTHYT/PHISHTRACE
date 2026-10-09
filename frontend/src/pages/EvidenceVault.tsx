import React, { useState, useEffect } from 'react';
import {
  Lock,
  ShieldCheck,
  Download,
  Code,
  FileCheck,
  Search,
  History,
  AlertOctagon,
  Clock,
  CheckCircle2
} from 'lucide-react';
import { InvestigationRecord, VerificationResult } from '../lib/types';
import { fetchEvidenceList, verifyEvidence } from '../lib/api';

interface EvidenceVaultProps {
  onSelectEmail: (messageId: string) => void;
}

export const EvidenceVault: React.FC<EvidenceVaultProps> = ({ onSelectEmail }) => {
  const [records, setRecords] = useState<InvestigationRecord[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [verifyingId, setVerifyingId] = useState<string | null>(null);
  const [verificationResults, setVerificationResults] = useState<Record<string, VerificationResult>>({});

  const loadVaultData = async () => {
    setLoading(true);
    try {
      const recs = await fetchEvidenceList();
      setRecords(recs);

      // Fetch audit logs
      const auditRes = await fetch('/api/evidence/audit-log').then((r) => r.json());
      setAuditLogs(auditRes);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVaultData();
  }, []);

  const handleVerify = async (invId: string) => {
    setVerifyingId(invId);
    try {
      const res = await verifyEvidence(invId);
      setVerificationResults((prev) => ({ ...prev, [invId]: res }));
      // Reload audit log
      const auditRes = await fetch('/api/evidence/audit-log').then((r) => r.json());
      setAuditLogs(auditRes);
    } catch (e) {
      console.error(e);
    } finally {
      setVerifyingId(null);
    }
  };

  const filtered = records.filter(
    (r) =>
      search === '' ||
      r.investigation_id.toLowerCase().includes(search.toLowerCase()) ||
      r.subject.toLowerCase().includes(search.toLowerCase()) ||
      r.original_digest.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-950/80 border border-emerald-800 text-emerald-400">
            <Lock className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100 uppercase tracking-wide">
              Forensic Evidence Vault & Cryptographic Ledger
            </h2>
            <p className="text-xs text-slate-400">
              SHA-256 integrity verification, append-only SOC audit trails, and exportable forensic dossiers
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Vault Records */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search investigation ID, subject, or SHA-256..."
                className="w-full pl-9 pr-3 py-2 bg-slate-900 border border-slate-800 focus:border-cyan-500 rounded-lg text-xs text-slate-200 outline-none"
              />
            </div>
            <span className="text-xs font-mono text-slate-400 shrink-0">
              {filtered.length} Archived Dossiers
            </span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow">
            {loading ? (
              <div className="py-16 text-center text-slate-500 text-xs">
                Scanning cryptographic vault...
              </div>
            ) : filtered.length === 0 ? (
              <div className="py-16 text-center text-slate-500 text-xs">
                No investigation records found.
              </div>
            ) : (
              <div className="divide-y divide-slate-800/80">
                {filtered.map((rec) => {
                  const verified = verificationResults[rec.investigation_id];
                  return (
                    <div key={rec.investigation_id} className="p-4 space-y-3">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-xs font-bold text-cyan-400">
                              {rec.investigation_id}
                            </span>
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-800 text-slate-300">
                              {rec.risk_category} ({rec.risk_score})
                            </span>
                          </div>
                          <h4 className="text-sm font-semibold text-slate-200 mt-1">{rec.subject}</h4>
                          <p className="text-xs text-slate-400">Sender: {rec.sender}</p>
                        </div>

                        {/* Action buttons */}
                        <div className="flex items-center gap-2 self-start sm:self-auto">
                          <button
                            onClick={() => handleVerify(rec.investigation_id)}
                            disabled={verifyingId === rec.investigation_id}
                            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition cursor-pointer"
                          >
                            <ShieldCheck className="h-3.5 w-3.5 text-cyan-400" />
                            <span>
                              {verifyingId === rec.investigation_id ? 'Checking...' : 'Verify Hash'}
                            </span>
                          </button>

                          <a
                            href={`/api/evidence/${rec.message_id}/pdf`}
                            download
                            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-slate-700 transition"
                            title="Download PDF Incident Dossier"
                          >
                            <Download className="h-4 w-4" />
                          </a>

                          <a
                            href={`/api/evidence/${rec.investigation_id}/export`}
                            download
                            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                            title="Download JSON Artifact"
                          >
                            <Code className="h-4 w-4" />
                          </a>
                        </div>
                      </div>

                      {/* Hash info */}
                      <div className="p-2.5 rounded bg-slate-950 border border-slate-800/80 font-mono text-[11px] text-slate-400 space-y-1">
                        <div className="truncate">
                          <span className="text-slate-500">Original Raw Digest: </span>
                          <span className="text-slate-300">{rec.original_digest}</span>
                        </div>
                        <div className="truncate">
                          <span className="text-slate-500">Record Export Hash: </span>
                          <span className="text-cyan-400">{rec.export_digest}</span>
                        </div>
                      </div>

                      {/* Real-time verification result */}
                      {verified && (
                        <div
                          className={`p-2.5 rounded border text-xs flex items-center gap-2 ${
                            verified.matches
                              ? 'bg-emerald-950/40 border-emerald-800 text-emerald-300'
                              : 'bg-red-950/40 border-red-800 text-red-300'
                          }`}
                        >
                          {verified.matches ? (
                            <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                          ) : (
                            <AlertOctagon className="h-4 w-4 shrink-0 text-red-400" />
                          )}
                          <span>{verified.details}</span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Append-Only Audit Trail Timeline */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <History className="h-4 w-4 text-cyan-400" />
              Append-Only SOC Audit Log
            </h3>
            <span className="text-[10px] font-mono text-emerald-400">Immutable</span>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow space-y-3 max-h-[640px] overflow-y-auto">
            {auditLogs.length === 0 ? (
              <p className="text-xs text-slate-500">No audit events logged.</p>
            ) : (
              auditLogs.map((log, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 text-xs space-y-1">
                  <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
                    <span>{log.event}</span>
                    <span>{log.timestamp ? log.timestamp.split('T')[1].slice(0, 8) : ''}</span>
                  </div>
                  <div className="font-semibold text-slate-200 text-[11px] truncate">
                    {log.investigation_id}
                  </div>
                  <p className="text-[11px] text-slate-400">{log.analyst_action}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
