import React, { useState, useRef } from 'react';
import { Upload, X, FileText, CheckCircle2, AlertCircle, Loader2, Sparkles } from 'lucide-react';
import { uploadEmlFile } from '../../lib/api';
import { EmailDetail } from '../../lib/types';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAnalysisComplete: (email: EmailDetail) => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onAnalysisComplete,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progressStep, setProgressStep] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFileProcess = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.eml') && !file.name.toLowerCase().endsWith('.txt')) {
      setError('Please select a valid RFC email file (.eml extension).');
      return;
    }

    setLoading(true);
    setError(null);
    setProgressStep('Parsing MIME envelope and calculating SHA-256 evidence digest...');

    try {
      setTimeout(() => setProgressStep('Tracing Received hops & checking RFC1918 boundaries...'), 400);
      setTimeout(() => setProgressStep('Running deterministic threat scoring & URL analysis...'), 800);
      setTimeout(() => setProgressStep('Generating Open-Source Gemma AI incident assessment...'), 1200);

      const result = await uploadEmlFile(file);
      setProgressStep('Complete! Navigating to forensic dossier...');
      setTimeout(() => {
        setLoading(false);
        onClose();
        onAnalysisComplete(result);
      }, 500);
    } catch (err: any) {
      setLoading(false);
      setError(err.message || 'Failed to analyze uploaded email');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileProcess(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-lg bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-6">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-100 transition"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-lg bg-cyan-950/80 border border-cyan-800 text-cyan-400">
            <Upload className="h-6 w-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-100">Upload Email for Forensics</h3>
            <p className="text-xs text-slate-400">Safe, isolated analysis with cryptographic evidence logging</p>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-950/60 border border-red-800 flex items-center gap-2 text-xs text-red-300">
            <AlertCircle className="h-4 w-4 shrink-0 text-red-400" />
            <span>{error}</span>
          </div>
        )}

        {loading ? (
          <div className="py-12 flex flex-col items-center justify-center text-center">
            <Loader2 className="h-10 w-10 text-cyan-400 animate-spin mb-4" />
            <h4 className="font-semibold text-slate-200 text-sm mb-1">Analyzing Threat Vectors</h4>
            <p className="text-xs font-mono text-cyan-400 animate-pulse">{progressStep}</p>
          </div>
        ) : (
          <div>
            <div
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
                isDragging
                  ? 'border-cyan-400 bg-cyan-950/30'
                  : 'border-slate-700 hover:border-slate-500 bg-slate-950/40'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".eml,.txt"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileProcess(e.target.files[0]);
                  }
                }}
              />
              <FileText className="h-12 w-12 mx-auto text-slate-500 mb-3" />
              <p className="text-sm font-medium text-slate-200">
                Drag and drop your <span className="text-cyan-400 font-mono">.eml</span> file here
              </p>
              <p className="text-xs text-slate-500 mt-1">or click to browse from local computer</p>
              <div className="mt-4 flex items-center justify-center gap-2 text-[11px] text-slate-400 font-mono">
                <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                <span>Zero Execution Sandbox | SHA-256 Preserved | Max 15MB</span>
              </div>
            </div>

            <div className="mt-4 p-3 rounded-lg bg-slate-950/60 border border-slate-800 text-[11px] text-slate-400">
              <span className="font-semibold text-slate-300">Security Guarantee: </span>
              Attachments and scripts are never executed or rendered without full HTML sanitization.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
