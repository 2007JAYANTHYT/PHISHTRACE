import React, { useState, useEffect } from 'react';
import { Navbar } from './components/layout/Navbar';
import { UploadModal } from './components/shared/UploadModal';
import { Dashboard } from './pages/Dashboard';
import { Inbox } from './pages/Inbox';
import { Investigation } from './pages/Investigation';
import { Campaigns } from './pages/Campaigns';
import { EvidenceVault } from './pages/EvidenceVault';
import { Settings } from './pages/Settings';
import {
  fetchDashboard,
  fetchEmails,
  fetchEmailDetail,
  fetchCampaigns
} from './lib/api';
import {
  DashboardSummary,
  EmailSummary,
  EmailDetail,
  CampaignCluster
} from './lib/types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [emails, setEmails] = useState<EmailSummary[]>([]);
  const [campaigns, setCampaigns] = useState<CampaignCluster[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<EmailDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [uploadModalOpen, setUploadModalOpen] = useState<boolean>(false);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [sum, ems, camps] = await Promise.all([
        fetchDashboard(),
        fetchEmails(),
        fetchCampaigns(),
      ]);
      setSummary(sum);
      setEmails(ems);
      setCampaigns(camps);

      // Default select the most critical or recent email
      if (ems.length > 0 && !selectedEmail) {
        const detail = await fetchEmailDetail(ems[0].id);
        setSelectedEmail(detail);
      }
    } catch (err) {
      console.error('Failed to load initial SOC telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const handleSelectEmail = async (id: string) => {
    try {
      const detail = await fetchEmailDetail(id);
      setSelectedEmail(detail);
      setActiveTab('investigation');
    } catch (err) {
      console.error('Failed to fetch email detail:', err);
    }
  };

  const handleAnalysisComplete = (newDetail: EmailDetail) => {
    setSelectedEmail(newDetail);
    setActiveTab('investigation');
    loadInitialData(); // Refresh list and counters
  };

  return (
    <div className="min-h-screen bg-[#070a12] text-slate-100 flex flex-col font-sans">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        aiMode={summary?.ai_status?.provider || 'Gemma Open Weights'}
        gmailConnected={summary?.gmail_status?.connected || false}
        onQuickUpload={() => setUploadModalOpen(true)}
        onRefresh={loadInitialData}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && (
          <Dashboard
            summary={summary}
            onNavigateToEmail={handleSelectEmail}
            onNavigateTab={setActiveTab}
            onQuickUpload={() => setUploadModalOpen(true)}
          />
        )}

        {activeTab === 'inbox' && (
          <Inbox
            emails={emails}
            onSelectEmail={handleSelectEmail}
            onQuickUpload={() => setUploadModalOpen(true)}
            loading={loading}
          />
        )}

        {activeTab === 'investigation' && (
          <Investigation
            email={selectedEmail}
            onRefresh={() => selectedEmail && handleSelectEmail(selectedEmail.id)}
          />
        )}

        {activeTab === 'campaigns' && (
          <Campaigns
            campaigns={campaigns}
            onSelectEmail={handleSelectEmail}
          />
        )}

        {activeTab === 'evidence' && (
          <EvidenceVault
            onSelectEmail={handleSelectEmail}
          />
        )}

        {activeTab === 'settings' && (
          <Settings />
        )}
      </main>

      <UploadModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onAnalysisComplete={handleAnalysisComplete}
      />

      {/* SOC Status Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-4 text-center text-xs text-slate-500 font-mono">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            PhishTrace Platform  --  Hacktoberfest Hack Day Bengaluru 2026 | Team Dark
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <span>Gemma 4 / Gemma 2 Open Weights</span>
            <span>*</span>
            <span>RFC 5322 Forensics</span>
            <span>*</span>
            <span>SHA-256 Verified</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
