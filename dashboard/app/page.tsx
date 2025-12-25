'use client';

import { useState } from 'react';
import { Zap, BarChart3, TrendingUp, FlaskConical } from 'lucide-react';
import ContentGeneration from './components/ContentGeneration';
import SentimentTrends from './components/SentimentTrends';
import PerformanceMetrics from './components/PerformanceMetrics';
import ABTesting from './components/ABTesting';

type TabType = 'content' | 'sentiment' | 'performance' | 'ab-testing';

interface Tab {
  id: TabType;
  label: string;
  icon: React.ReactNode;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('content');

  const tabs: Tab[] = [
    { id: 'content', label: 'Content Generation', icon: <Zap className="w-5 h-5" /> },
    { id: 'sentiment', label: 'Sentiment & Trends', icon: <BarChart3 className="w-5 h-5" /> },
    { id: 'performance', label: 'Performance Metrics', icon: <TrendingUp className="w-5 h-5" /> },
    { id: 'ab-testing', label: 'A/B Testing', icon: <FlaskConical className="w-5 h-5" /> },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-black to-slate-800">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(100,116,139,0.1),transparent_50%)] pointer-events-none" />

      <div className="relative">
        <header className="border-b border-slate-800/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-slate-50 tracking-tight">TrendForgeAI</h1>
                <p className="text-slate-400 text-sm mt-1">AI-Based Automated Content Marketing Optimizer</p>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 border border-slate-700/50 rounded-lg">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
                  <span className="text-slate-300 text-sm">API Online</span>
                </div>
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  className="px-4 py-2 text-slate-300 hover:text-slate-100 text-sm transition-colors"
                >
                  API Docs
                </a>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-6">
          <nav className="flex gap-1 pt-6 border-b border-slate-800/50">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 text-sm font-medium transition-all relative
                  ${activeTab === tab.id
                    ? 'text-slate-100'
                    : 'text-slate-400 hover:text-slate-300'
                  }`}
              >
                {tab.icon}
                <span>{tab.label}</span>
                {activeTab === tab.id && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-slate-300 shadow-[0_0_10px_rgba(203,213,225,0.5)]" />
                )}
              </button>
            ))}
          </nav>

          <main className="py-8">
            {activeTab === 'content' && <ContentGeneration />}
            {activeTab === 'sentiment' && <SentimentTrends />}
            {activeTab === 'performance' && <PerformanceMetrics />}
            {activeTab === 'ab-testing' && <ABTesting />}
          </main>
        </div>
      </div>
    </div>
  );
}
