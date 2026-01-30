'use client';

import { useState, useEffect } from 'react';

interface Insight {
    type: string;
    message: string;
    priority: string;
    memories: number[];
    timestamp: string;
}

const PRIORITY_COLORS: Record<string, string> = {
    high: 'bg-red-100 border-red-300 text-red-800 dark:bg-red-900/20 dark:border-red-700 dark:text-red-300',
    medium: 'bg-yellow-100 border-yellow-300 text-yellow-800 dark:bg-yellow-900/20 dark:border-yellow-700 dark:text-yellow-300',
    low: 'bg-blue-100 border-blue-300 text-blue-800 dark:bg-blue-900/20 dark:border-blue-700 dark:text-blue-300',
};

const TYPE_ICONS: Record<string, string> = {
    pattern: '🔄',
    goal_tracking: '🎯',
    connection: '🔗',
    suggestion: '💡',
};

export default function InsightsPanel() {
    const [insights, setInsights] = useState<Insight[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const loadInsights = async () => {
        try {
            const res = await fetch('/api/insights/');
            if (!res.ok) throw new Error('Failed to load insights');
            const data = await res.json();
            setInsights(data);
        } catch (error) {
            console.error('Failed to load insights:', error);
        }
    };

    const triggerAnalysis = async () => {
        setIsLoading(true);
        try {
            const res = await fetch('/api/insights/analyze', { method: 'POST' });
            if (!res.ok) throw new Error('Analysis failed');
            const data = await res.json();
            console.log('Analysis complete:', data);
            await loadInsights();
        } catch (error) {
            console.error('Analysis failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        loadInsights();
        // Auto-refresh every 60 seconds
        const interval = setInterval(loadInsights, 60000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-full flex flex-col bg-slate-50 dark:bg-slate-900">
            {/* Header */}
            <div className="p-6 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Proactive Insights</h1>
                        <p className="text-sm text-slate-600 dark:text-slate-400">AI-generated insights from your memories</p>
                    </div>
                    <button
                        onClick={triggerAnalysis}
                        disabled={isLoading}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg font-medium transition-colors"
                    >
                        {isLoading ? 'Analyzing...' : 'Analyze Now'}
                    </button>
                </div>
            </div>

            {/* Insights List */}
            <div className="flex-1 overflow-y-auto p-6">
                {insights.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="text-6xl mb-4">🤖</div>
                        <p className="text-slate-600 dark:text-slate-400 mb-4">
                            No insights yet. Click "Analyze Now" to generate proactive insights.
                        </p>
                        <p className="text-sm text-slate-500">
                            Opera will find patterns, track goals, and suggest actions.
                        </p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {insights.map((insight, idx) => (
                            <div
                                key={idx}
                                className={`p-5 rounded-xl border-2 ${PRIORITY_COLORS[insight.priority] || PRIORITY_COLORS.low}`}
                            >
                                <div className="flex items-start gap-3">
                                    <div className="text-3xl">{TYPE_ICONS[insight.type] || '📌'}</div>
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className="font-semibold capitalize">{insight.type.replace('_', ' ')}</span>
                                            <span className="text-xs opacity-75">
                                                {new Date(insight.timestamp).toLocaleString()}
                                            </span>
                                        </div>
                                        <p className="text-sm leading-relaxed">{insight.message}</p>
                                        {insight.memories.length > 0 && (
                                            <div className="mt-2 text-xs opacity-75">
                                                Related to {insight.memories.length} memory/memories
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
