'use client';

import { useState, useEffect } from 'react';
import { Zap, FileText, History, RefreshCw, Calendar, ExternalLink } from 'lucide-react';

export default function ContentGeneration() {
    const [topic, setTopic] = useState('');
    const [platform, setPlatform] = useState('LinkedIn');
    const [productInfo, setProductInfo] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');
    const [history, setHistory] = useState<any[]>([]);
    const [loadingHistory, setLoadingHistory] = useState(false);

    const fetchHistory = async () => {
        setLoadingHistory(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/content/history');
            if (response.ok) {
                const data = await response.json();
                setHistory(data.items || []);
            }
        } catch (err) {
            console.error('Failed to fetch history', err);
        } finally {
            setLoadingHistory(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleGenerate = async () => {
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch('http://localhost:8000/api/v1/content/generate?use_async=false', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic,
                    platform,
                    product_info: productInfo,
                    num_variations: 1,
                }),
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            setResult(data);
            fetchHistory(); // Refresh history after generation
        } catch (err: any) {
            setError(err.message || 'Failed to generate content');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-xl font-semibold text-slate-100">Content Generation & Optimization Engine</h2>
                <p className="text-sm text-slate-400 mt-1">Create marketing content using LLMs and optimize based on trends</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Generate Content Panel */}
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <Zap className="w-5 h-5 text-slate-300" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Generate Content</h3>
                    </div>

                    <div className="space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">Topic</label>
                            <input
                                type="text"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                                placeholder="e.g., AI in Healthcare, Sustainable Fashion"
                                className="w-full px-4 py-2.5 bg-slate-900/50 border border-slate-700/50 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:border-slate-600 focus:ring-1 focus:ring-slate-600 transition-colors"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">Platform</label>
                            <select
                                value={platform}
                                onChange={(e) => setPlatform(e.target.value)}
                                className="w-full px-4 py-2.5 bg-slate-900/50 border border-slate-700/50 rounded-lg text-slate-100 focus:outline-none focus:border-slate-600 focus:ring-1 focus:ring-slate-600 transition-colors"
                            >
                                <option value="LinkedIn">LinkedIn</option>
                                <option value="Twitter">Twitter</option>
                                <option value="Facebook">Facebook</option>
                                <option value="Instagram">Instagram</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">Product Information</label>
                            <textarea
                                value={productInfo}
                                onChange={(e) => setProductInfo(e.target.value)}
                                placeholder="Describe your product or service..."
                                rows={4}
                                className="w-full px-4 py-2.5 bg-slate-900/50 border border-slate-700/50 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:border-slate-600 focus:ring-1 focus:ring-slate-600 transition-colors resize-none"
                            />
                        </div>

                        <button
                            onClick={handleGenerate}
                            disabled={loading || !topic || !productInfo}
                            className="w-full py-3 bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-500 text-slate-100 font-medium rounded-lg transition-colors disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
                                    Generating...
                                </>
                            ) : (
                                <>
                                    <Zap className="w-4 h-4" />
                                    Generate Optimized Content
                                </>
                            )}
                        </button>

                        {error && (
                            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                                <p className="text-red-400 text-sm">{error}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Generated Content Panel */}
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6 flex flex-col">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <FileText className="w-5 h-5 text-slate-300" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Generated Content</h3>
                    </div>

                    {!result && !loading && (
                        <div className="flex flex-col items-center justify-center flex-1 text-center py-12">
                            <div className="h-16 w-16 rounded-full bg-slate-700/30 flex items-center justify-center mb-4">
                                <FileText className="w-8 h-8 text-slate-500" />
                            </div>
                            <p className="text-slate-400 text-sm">Your AI-generated content will appear here</p>
                            <p className="text-slate-500 text-xs mt-2">Powered by Gemini 2.0 Flash</p>
                        </div>
                    )}

                    {loading && (
                        <div className="flex flex-col items-center justify-center flex-1 py-12">
                            <div className="relative">
                                <div className="h-16 w-16 rounded-full border-4 border-slate-700/30"></div>
                                <div className="absolute top-0 left-0 h-16 w-16 rounded-full border-4 border-slate-400 border-t-transparent animate-spin"></div>
                            </div>
                            <p className="text-slate-300 mt-6 text-sm font-medium">Crafting optimized content...</p>
                            <p className="text-slate-500 text-xs mt-2">Analyzing trends & engagement patterns</p>
                        </div>
                    )}

                    {result && (
                        <div className="space-y-4 flex-1 overflow-y-auto pr-2 custom-scrollbar">
                            <div className="flex items-center gap-2">
                                <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-emerald-400 text-xs font-medium uppercase tracking-wider">
                                    {result.status}
                                </span>
                                {result.result?.quality_score && (
                                    <span className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-xs font-medium">
                                        Quality: {result.result.quality_score}/10
                                    </span>
                                )}
                            </div>

                            {result.result?.final_content && (
                                <div className="p-4 bg-slate-900/50 border border-slate-700/50 rounded-lg group relative">
                                    <h4 className="text-xs font-medium text-slate-400 mb-2">Optimized Content</h4>
                                    <p className="text-slate-100 text-sm leading-relaxed whitespace-pre-wrap">{result.result.final_content}</p>
                                </div>
                            )}

                            {result.result?.critique_notes && (
                                <div className="p-4 bg-blue-500/5 border border-blue-500/20 rounded-lg">
                                    <div className="flex items-center gap-2 mb-2">
                                        <Zap className="w-3 h-3 text-blue-400" />
                                        <h4 className="text-xs font-medium text-blue-400">AI Optimization Notes</h4>
                                    </div>
                                    <p className="text-slate-300 text-sm italic">{result.result.critique_notes}</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Content History */}
            <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
                            <History className="w-5 h-5 text-slate-300" />
                        </div>
                        <h3 className="text-lg font-medium text-slate-100">Recent Generations</h3>
                    </div>
                    <button
                        onClick={fetchHistory}
                        className="flex items-center gap-2 text-sm text-slate-400 hover:text-slate-200 transition-colors"
                    >
                        <RefreshCw className={`w-4 h-4 ${loadingHistory ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                </div>

                {history.length === 0 && !loadingHistory ? (
                    <div className="py-12 text-center">
                        <p className="text-slate-500 text-sm">No generation history yet</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {history.map((item) => (
                            <div key={item.id} className="bg-slate-700/30 border border-slate-700/50 rounded-lg p-4 hover:border-slate-600 transition-colors group">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <span className="px-2 py-0.5 bg-slate-800 text-[10px] text-slate-300 rounded border border-slate-700/50">
                                            {item.platform}
                                        </span>
                                        <h4 className="text-sm font-medium text-slate-200 mt-2 line-clamp-1">{item.topic}</h4>
                                    </div>
                                    <span className="text-[10px] text-slate-500 flex items-center gap-1">
                                        <Calendar className="w-3 h-3" />
                                        {new Date(item.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                                <p className="text-xs text-slate-400 line-clamp-3 mb-3">{item.final_content}</p>
                                <div className="flex items-center justify-between pt-3 border-t border-slate-700/50">
                                    <span className="text-[10px] font-medium text-emerald-400">Score: {item.quality_score}/10</span>
                                    <button
                                        onClick={() => setResult({ status: 'completed', result: item })}
                                        className="text-[10px] text-blue-400 hover:text-blue-300 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                                    >
                                        View Details <ExternalLink className="w-2.5 h-2.5" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
