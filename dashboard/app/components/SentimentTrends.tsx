'use client';

import { useEffect, useState } from 'react';
import { Smile, TrendingUp, Rocket, Linkedin, Twitter, Facebook, Instagram, RefreshCw } from 'lucide-react';

export default function SentimentTrends() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/sentiment');
            if (!response.ok) throw new Error('Failed to fetch sentiment data');
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

    if (loading && !data) {
        return (
            <div className="flex items-center justify-center h-64">
                <RefreshCw className="w-8 h-8 text-slate-400 animate-spin" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                {error}
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-semibold text-slate-100">Sentiment & Trend Analysis System</h2>
                    <p className="text-sm text-slate-400 mt-1">Analyze audience reactions and predict content performance</p>
                </div>
                <button
                    onClick={fetchData}
                    className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors text-slate-400"
                    title="Refresh Data"
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Sentiment Score */}
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <Smile className="w-5 h-5 text-emerald-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Sentiment Score</h3>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-end gap-2">
                            <span className="text-4xl font-bold text-slate-100">{data?.sentiment_score || '0.0'}</span>
                            <span className="text-slate-400 text-sm mb-1.5">/10</span>
                        </div>
                        <div className="w-full bg-slate-700/30 rounded-full h-2">
                            <div
                                className="bg-emerald-500 h-2 rounded-full transition-all duration-1000"
                                style={{ width: `${(data?.sentiment_score || 0) * 10}%` }}
                            ></div>
                        </div>
                        <p className="text-xs text-slate-400">Positive audience sentiment detected</p>
                    </div>
                </div>

                {/* Trending Topics */}
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <TrendingUp className="w-5 h-5 text-orange-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Trending Topics</h3>
                    </div>
                    <div className="space-y-2">
                        {data?.trending_topics?.map((topic: any, i: number) => (
                            <div key={i} className="flex items-center justify-between p-2.5 bg-slate-700/30 rounded-lg">
                                <span className="text-sm text-slate-200">{topic.topic}</span>
                                <span className="text-xs text-emerald-400 font-medium">{topic.change}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Viral Potential */}
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <Rocket className="w-5 h-5 text-blue-400" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Viral Potential</h3>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-end gap-2">
                            <span className="text-4xl font-bold text-slate-100">{data?.viral_potential || '0'}</span>
                            <span className="text-slate-400 text-sm mb-1.5">%</span>
                        </div>
                        <div className="w-full bg-slate-700/30 rounded-full h-2">
                            <div
                                className="bg-blue-500 h-2 rounded-full transition-all duration-1000"
                                style={{ width: `${data?.viral_potential || 0}%` }}
                            ></div>
                        </div>
                        <p className="text-xs text-slate-400">High probability of viral spread</p>
                    </div>
                </div>
            </div>

            {/* Social Media Analysis */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <h3 className="text-lg font-medium text-slate-100 mb-4">Social Media Reactions</h3>
                    <div className="space-y-3">
                        {data?.platform_reactions?.map((item: any, i: number) => {
                            const icons: any = { LinkedIn: Linkedin, Twitter: Twitter, Facebook: Facebook, Instagram: Instagram };
                            const Icon = icons[item.platform] || Smile;
                            return (
                                <div key={i} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                                    <div className="flex items-center gap-3">
                                        <div className="h-9 w-9 rounded-lg bg-slate-600/50 flex items-center justify-center">
                                            <Icon className="w-4 h-4 text-slate-300" />
                                        </div>
                                        <div>
                                            <p className="text-sm font-medium text-slate-200">{item.platform}</p>
                                            <p className="text-xs text-slate-400">{item.sentiment}</p>
                                        </div>
                                    </div>
                                    <span className="text-lg font-bold text-slate-100">{item.score}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <h3 className="text-lg font-medium text-slate-100 mb-4">Predicted Performance</h3>
                    <div className="space-y-4">
                        {data?.predicted_performance?.map((item: any, i: number) => (
                            <div key={i} className={`p-4 rounded-lg bg-slate-700/10 border border-slate-700/30`}>
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm text-slate-300">{item.label}</span>
                                    <span className="text-lg font-bold text-slate-100">{item.value}</span>
                                </div>
                                <div className="w-full bg-slate-700/30 rounded-full h-1.5">
                                    <div
                                        className="bg-slate-500 h-1.5 rounded-full"
                                        style={{ width: `${item.progress}%` }}
                                    ></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
