'use client';

import { useEffect, useState } from 'react';
import { FlaskConical, Target, TrendingUp, Lightbulb, RefreshCw } from 'lucide-react';

export default function ABTesting() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/ab');
            if (!response.ok) throw new Error('Failed to fetch A/B testing data');
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
                    <h2 className="text-xl font-semibold text-slate-100">A/B Testing & Prediction Coach</h2>
                    <p className="text-sm text-slate-400 mt-1">Run automated tests and forecast campaign outcomes</p>
                </div>
                <button
                    onClick={fetchData}
                    className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors text-slate-400"
                    title="Refresh Data"
                >
                    <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
            </div>

            {/* Active A/B Tests */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-medium text-slate-100">Active A/B Tests</h3>
                        <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-100 rounded-lg text-sm font-medium transition-colors">
                            + New Test
                        </button>
                    </div>
                    <div className="space-y-4">
                        {data?.active_tests?.map((test: any, i: number) => (
                            <div key={i} className="p-4 bg-slate-700/30 border border-slate-600/50 rounded-lg">
                                <div className="flex items-center justify-between mb-3">
                                    <p className="text-sm font-medium text-slate-200">{test.name}</p>
                                    <span className={`px-2.5 py-1 ${test.status === 'running' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' : 'bg-slate-600/50 text-slate-400 border-slate-500/30'} rounded text-xs border font-medium`}>
                                        {test.status}
                                    </span>
                                </div>
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <p className="text-xs text-slate-400 mb-1.5">Variant A</p>
                                        <div className="flex items-center gap-2">
                                            <div className="flex-1 bg-slate-600/30 rounded-full h-2">
                                                <div className="bg-blue-500 h-2 rounded-full transition-all duration-1000" style={{ width: `${test.variantA}%` }}></div>
                                            </div>
                                            <span className="text-sm font-semibold text-slate-200">{test.variantA}%</span>
                                        </div>
                                    </div>
                                    <div>
                                        <p className="text-xs text-slate-400 mb-1.5">Variant B</p>
                                        <div className="flex items-center gap-2">
                                            <div className="flex-1 bg-slate-600/30 rounded-full h-2">
                                                <div className="bg-emerald-500 h-2 rounded-full transition-all duration-1000" style={{ width: `${test.variantB}%` }}></div>
                                            </div>
                                            <span className="text-sm font-semibold text-slate-200">{test.variantB}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                    <h3 className="text-lg font-medium text-slate-100 mb-6">AI Prediction Coach</h3>
                    <div className="space-y-4">
                        <div className="p-4 bg-blue-500/5 border border-blue-500/20 rounded-lg">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="h-9 w-9 rounded-lg bg-blue-500/10 flex items-center justify-center">
                                    <Target className="w-5 h-5 text-blue-400" />
                                </div>
                                <h4 className="font-semibold text-slate-100 text-sm">{data?.recommendation?.title || 'Recommendation'}</h4>
                            </div>
                            <p className="text-sm text-slate-300 mb-3">
                                {data?.recommendation?.content}
                            </p>
                            <div className="flex gap-2">
                                <button className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-medium transition-colors">
                                    Apply Recommendation
                                </button>
                                <button className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg text-xs transition-colors">
                                    Details
                                </button>
                            </div>
                        </div>

                        <div className="p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-lg">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="h-9 w-9 rounded-lg bg-emerald-500/10 flex items-center justify-center">
                                    <TrendingUp className="w-5 h-5 text-emerald-400" />
                                </div>
                                <h4 className="font-semibold text-slate-100 text-sm">Performance Forecast</h4>
                            </div>
                            <div className="space-y-2">
                                {data?.performance_forecast?.map((item: any, i: number) => (
                                    <div key={i} className="flex justify-between text-sm">
                                        <span className="text-slate-400">{item.label}</span>
                                        <span className={`font-medium ${item.label === 'Confidence Level' ? 'text-emerald-400' : 'text-slate-100'}`}>{item.value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="p-4 bg-purple-500/5 border border-purple-500/20 rounded-lg">
                            <div className="flex items-center gap-3 mb-3">
                                <div className="h-9 w-9 rounded-lg bg-purple-500/10 flex items-center justify-center">
                                    <Lightbulb className="w-5 h-5 text-purple-400" />
                                </div>
                                <h4 className="font-semibold text-slate-100 text-sm">Quick Insights</h4>
                            </div>
                            <ul className="space-y-2 text-sm text-slate-300">
                                {data?.quick_insights?.map((insight: string, i: number) => (
                                    <li key={i} className="flex items-start gap-2">
                                        <span className="text-purple-400 mt-0.5">•</span>
                                        <span>{insight}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            {/* Test Results History */}
            <div className="bg-slate-800/30 backdrop-blur-sm rounded-lg border border-slate-700/50 p-6">
                <h3 className="text-lg font-medium text-slate-100 mb-4">Recent Test Results</h3>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-slate-700/50">
                                <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Test Name</th>
                                <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Winner</th>
                                <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Improvement</th>
                                <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Date</th>
                                <th className="text-left py-3 px-4 text-sm font-medium text-slate-400">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data?.recent_results?.map((result: any, i: number) => (
                                <tr key={i} className="border-b border-slate-700/30 hover:bg-slate-700/20 transition-colors">
                                    <td className="py-3 px-4 text-sm text-slate-200">{result.name}</td>
                                    <td className="py-3 px-4 text-sm text-blue-400">{result.winner}</td>
                                    <td className="py-3 px-4 text-sm text-emerald-400">{result.improvement}</td>
                                    <td className="py-3 px-4 text-sm text-slate-400">{result.date}</td>
                                    <td className="py-3 px-4">
                                        <button className="text-xs text-blue-400 hover:text-blue-300 transition-colors">View Details</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
