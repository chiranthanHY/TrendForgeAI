'use client';

import { useEffect, useState } from 'react';
import { Users, Heart, Target, DollarSign, MessageSquare, FileSpreadsheet, RefreshCw } from 'lucide-react';

export default function PerformanceMetrics() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/metrics');
            if (!response.ok) throw new Error('Failed to fetch performance metrics');
            const json = await response.json();
            setData(json);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const [sendingReport, setSendingReport] = useState(false);

    const sendPerformanceReport = async () => {
        setSendingReport(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/metrics/send-report', {
                method: 'POST'
            });
            const result = await response.json();
            if (response.ok) {
                alert("Performance Report Sent to Slack! 📊");
            } else {
                alert(`Error: ${result.detail}`);
            }
        } catch (err) {
            alert("Failed to connect to the API.");
        } finally {
            setSendingReport(false);
        }
    };

    const sendTestNotification = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/metrics/slack-test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: "Hello from the TrendForgeAI Dashboard! 🚀" })
            });
            const result = await response.json();
            if (response.ok) {
                alert("Slack Notification Sent! Check your channel.");
            } else {
                alert(`Error: ${result.detail}`);
            }
        } catch (err) {
            alert("Failed to connect to the API.");
        }
    };

    if (loading && !data) {
        return (
            <div className="flex items-center justify-center h-64">
                <RefreshCw className="w-8 h-8 text-slate-400 animate-spin" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-semibold text-slate-100">Performance Metrics & Slack Integration Hub</h2>
                    <p className="text-sm text-slate-400 mt-1">Track metrics and automate reporting with team collaboration</p>
                </div>
                <button
                    onClick={fetchData}
                    className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors text-slate-400"
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </div>

            {/* Key Metrics Dashboard */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {data?.key_metrics?.map((metric: any, i: number) => {
                    const icons: any = { Users, Heart, Target, DollarSign };
                    const Icon = icons[metric.icon] || Target;
                    return (
                        <div key={i} className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-5">
                            <div className="flex items-center justify-between mb-3">
                                <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                                    <Icon className="w-5 h-5 text-slate-300" />
                                </div>
                                <span className="text-xs text-emerald-400 font-medium">{metric.change}</span>
                            </div>
                            <p className="text-slate-400 text-xs mb-1">{metric.label}</p>
                            <p className="text-2xl font-bold text-slate-100">{metric.value}</p>
                        </div>
                    );
                })}
            </div>

            {/* Performance Chart & Slack Integration */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <h3 className="text-lg font-medium text-slate-100 mb-4">Campaign Performance (Last 30 Days)</h3>
                    <div className="h-64 flex items-end justify-between gap-2">
                        {data?.campaign_performance?.map((point: any, i: number) => (
                            <div key={i} className="flex-1 flex flex-col items-center gap-2">
                                <div
                                    className="w-full bg-slate-600 hover:bg-slate-500 rounded-t transition-all duration-500"
                                    style={{ height: `${point.value}%` }}
                                ></div>
                                <span className="text-xs text-slate-500">{point.label}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <MessageSquare className="w-5 h-5 text-slate-300" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Slack Alerts</h3>
                    </div>
                    <div className="space-y-3">
                        {data?.slack_alerts?.map((alert: any, i: number) => (
                            <div key={i} className="p-3 bg-slate-700/30 border border-slate-600/50 rounded-lg">
                                <p className="text-sm text-slate-200">{alert.msg}</p>
                                <p className="text-xs text-slate-400 mt-1">{alert.time}</p>
                            </div>
                        ))}
                    </div>
                    <div className="space-y-2 mt-4">
                        <button
                            onClick={sendTestNotification}
                            className={`w-full py-2 ${data?.integration_status.find((s: any) => s.name === "Slack Bot")?.status === "Connected" ? 'bg-blue-600 hover:bg-blue-700' : 'bg-slate-700 cursor-not-allowed opacity-50'} text-white rounded-lg text-sm font-medium transition-colors`}
                        >
                            Send Test Notification
                        </button>
                        <button
                            onClick={sendPerformanceReport}
                            disabled={sendingReport}
                            className={`w-full py-2 ${data?.integration_status.find((s: any) => s.name === "Slack Bot")?.status === "Connected" ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-slate-700 cursor-not-allowed opacity-50'} text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2`}
                        >
                            {sendingReport ? <RefreshCw className="w-4 h-4 animate-spin" /> : null}
                            Send Full Intelligence Report
                        </button>
                        <button
                            className="w-full py-2 bg-slate-700 hover:bg-slate-600 border border-slate-600 text-slate-200 rounded-lg text-sm font-medium transition-colors"
                        >
                            Configure Webhook
                        </button>
                    </div>
                </div>
            </div>

            {/* Google Sheets Integration */}
            <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
                        </div>
                        <div>
                            <h3 className="text-lg font-medium text-slate-100">Google Sheets Integration</h3>
                            <p className="text-xs text-slate-400">Automated metrics tracking and reporting</p>
                        </div>
                    </div>
                    <button className="px-4 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 rounded-lg text-sm font-medium transition-colors">
                        Export to Sheets
                    </button>
                </div>
                <div className="grid grid-cols-4 gap-4">
                    {data?.integration_status?.map((sheet: any, i: number) => (
                        <div key={i} className="p-4 bg-slate-700/30 rounded-lg text-center">
                            <p className="text-sm text-slate-400 mb-2">{sheet.name}</p>
                            <p className={`text-base font-semibold ${sheet.status === 'Synced' || sheet.status === 'Connected' ? 'text-emerald-400' : 'text-amber-400'}`}>
                                {sheet.status}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
