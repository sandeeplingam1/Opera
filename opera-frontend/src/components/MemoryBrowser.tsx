'use client';

import { useState, useEffect } from 'react';
import { api, type Memory } from '@/lib/api';

const MEMORY_TYPES = ['episodic', 'semantic', 'preference', 'goal', 'skill'];
const TYPE_COLORS: Record<string, string> = {
    episodic: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
    semantic: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
    preference: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
    goal: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300',
    skill: 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300',
};

export default function MemoryBrowser() {
    const [memories, setMemories] = useState<Memory[]>([]);
    const [filteredType, setFilteredType] = useState<string>();
    const [searchQuery, setSearchQuery] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadMemories();
    }, [filteredType]);

    const loadMemories = async () => {
        setIsLoading(true);
        try {
            const data = await api.getMemories(filteredType);
            setMemories(data);
        } catch (error) {
            console.error('Failed to load memories:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchQuery.trim()) {
            loadMemories();
            return;
        }

        setIsLoading(true);
        try {
            const results = await api.searchMemories(searchQuery);
            setMemories(results.map((r: any) => ({
                id: r.id,
                type: r.memory_type,
                content: r.content,
                source: r.source,
                timestamp: r.timestamp,
                confidence: r.confidence,
            })));
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="h-full flex flex-col bg-slate-50 dark:bg-slate-900">
            {/* Header */}
            <div className="p-6 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">Memory Browser</h1>

                {/* Search */}
                <div className="flex gap-2 mb-4">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        placeholder="Search memories..."
                        className="flex-1 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        onClick={handleSearch}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                    >
                        Search
                    </button>
                </div>

                {/* Filters */}
                <div className="flex gap-2 flex-wrap">
                    <button
                        onClick={() => setFilteredType(undefined)}
                        className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${!filteredType
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300'
                            }`}
                    >
                        All
                    </button>
                    {MEMORY_TYPES.map(type => (
                        <button
                            key={type}
                            onClick={() => setFilteredType(type)}
                            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${filteredType === type
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300'
                                }`}
                        >
                            {type.charAt(0).toUpperCase() + type.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Memory List */}
            <div className="flex-1 overflow-y-auto p-6">
                {isLoading ? (
                    <div className="text-center text-slate-500 py-12">Loading...</div>
                ) : memories.length === 0 ? (
                    <div className="text-center text-slate-500 py-12">No memories found</div>
                ) : (
                    <div className="grid gap-4">
                        {memories.map(memory => (
                            <div
                                key={memory.id}
                                className="bg-white dark:bg-slate-800 rounded-xl p-5 shadow-sm border border-slate-200 dark:border-slate-700 hover:shadow-md transition-shadow"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${TYPE_COLORS[memory.type] || 'bg-slate-100 text-slate-800'}`}>
                                        {memory.type}
                                    </span>
                                    <span className="text-xs text-slate-500">
                                        {new Date(memory.timestamp).toLocaleDateString()}
                                    </span>
                                </div>
                                <p className="text-slate-900 dark:text-slate-100 mb-2">{memory.content}</p>
                                <div className="flex items-center gap-4 text-xs text-slate-500">
                                    <span>Source: {memory.source}</span>
                                    <span>Confidence: {(memory.confidence * 100).toFixed(0)}%</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
