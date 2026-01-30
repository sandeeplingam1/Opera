'use client';

import { useState, useEffect } from 'react';

interface AgentMessage {
    message: string;
    trigger: string;
    urgency: string;
    timestamp: string;
    read: boolean;
}

interface Thought {
    content: string;
    type: string;
    priority: number;
    timestamp: string;
}

export default function AutonomousPanel() {
    const [isActive, setIsActive] = useState(false);
    const [messages, setMessages] = useState<AgentMessage[]>([]);
    const [thoughts, setThoughts] = useState<Thought[]>([]);
    const [status, setStatus] = useState<any>(null);

    const loadStatus = async () => {
        try {
            const res = await fetch('/api/agent/status');
            const data = await res.json();
            setStatus(data);
            setIsActive(data.is_active);
        } catch (error) {
            console.error('Failed to load status:', error);
        }
    };

    const loadMessages = async () => {
        try {
            const res = await fetch('/api/agent/messages');
            const data = await res.json();
            setMessages(data);
        } catch (error) {
            console.error('Failed to load messages:', error);
        }
    };

    const loadThoughts = async () => {
        try {
            const res = await fetch('/api/agent/thoughts');
            const data = await res.json();
            setThoughts(data);
        } catch (error) {
            console.error('Failed to load thoughts:', error);
        }
    };

    const toggleAgent = async () => {
        const endpoint = isActive ? '/api/agent/stop' : '/api/agent/start';
        try {
            await fetch(endpoint, { method: 'POST' });
            await loadStatus();
            if (!isActive) {
                // Start polling when activated
                const interval = setInterval(() => {
                    loadMessages();
                    loadThoughts();
                }, 5000);
                return () => clearInterval(interval);
            }
        } catch (error) {
            console.error('Failed to toggle agent:', error);
        }
    };

    const markRead = async () => {
        try {
            await fetch('/api/agent/messages/read', { method: 'POST' });
            await loadMessages();
        } catch (error) {
            console.error('Failed to mark read:', error);
        }
    };

    useEffect(() => {
        loadStatus();
        loadMessages();
        loadThoughts();

        const interval = setInterval(() => {
            loadStatus();
            loadMessages();
            loadThoughts();
        }, 10000);

        return () => clearInterval(interval);
    }, []);

    const URGENCY_COLORS: Record<string, string> = {
        high: 'bg-red-100 border-red-400 text-red-900 dark:bg-red-900/30 dark:border-red-600 dark:text-red-200',
        medium: 'bg-yellow-100 border-yellow-400 text-yellow-900 dark:bg-yellow-900/30 dark:border-yellow-600 dark:text-yellow-200',
        low: 'bg-blue-100 border-blue-400 text-blue-900 dark:bg-blue-900/30 dark:border-blue-600 dark:text-blue-200',
    };

    return (
        <div className="h-full flex flex-col bg-slate-50 dark:bg-slate-900">
            {/* Header */}
            <div className="p-6 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                            🤖 Autonomous Mind
                            {isActive && <span className="text-sm font-normal text-green-600 dark:text-green-400 animate-pulse">● Active</span>}
                        </h1>
                        <p className="text-sm text-slate-600 dark:text-slate-400">
                            Opera thinking independently and making decisions
                        </p>
                    </div>
                    <button
                        onClick={toggleAgent}
                        className={`px-6 py-3 rounded-lg font-medium transition-colors ${isActive
                                ? 'bg-red-600 hover:bg-red-700 text-white'
                                : 'bg-green-600 hover:bg-green-700 text-white'
                            }`}
                    >
                        {isActive ? 'Pause Mind' : 'Activate Mind'}
                    </button>
                </div>

                {status && (
                    <div className="mt-4 grid grid-cols-4 gap-4 text-sm">
                        <div className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                            <div className="text-slate-600 dark:text-slate-400">Total Thoughts</div>
                            <div className="text-2xl font-bold text-slate-900 dark:text-white">{status.total_thoughts}</div>
                        </div>
                        <div className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                            <div className="text-slate-600 dark:text-slate-400">Unread Messages</div>
                            <div className="text-2xl font-bold text-slate-900 dark:text-white">{status.unread_messages}</div>
                        </div>
                        <div className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                            <div className="text-slate-600 dark:text-slate-400">Autonomy Level</div>
                            <div className="text-2xl font-bold text-slate-900 dark:text-white">{(status.personality?.autonomy * 100).toFixed(0)}%</div>
                        </div>
                        <div className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                            <div className="text-slate-600 dark:text-slate-400">Proactiveness</div>
                            <div className="text-2xl font-bold text-slate-900 dark:text-white">{(status.personality?.proactiveness * 100).toFixed(0)}%</div>
                        </div>
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* Unsolicited Messages */}
                <div>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
                            📬 Messages from Opera
                        </h2>
                        {messages.length > 0 && (
                            <button
                                onClick={markRead}
                                className="text-sm text-blue-600 hover:text-blue-700"
                            >
                                Mark all read
                            </button>
                        )}
                    </div>

                    {messages.length === 0 ? (
                        <div className="text-center py-8 text-slate-500">
                            No messages yet. Opera will speak up when it has something to say.
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {messages.map((msg, idx) => (
                                <div
                                    key={idx}
                                    className={`p-4 rounded-xl border-2 ${URGENCY_COLORS[msg.urgency]}`}
                                >
                                    <div className="flex items-start justify-between">
                                        <p className="flex-1 font-medium">{msg.message}</p>
                                        <span className="text-xs opacity-75 ml-2">
                                            {new Date(msg.timestamp).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    <div className="text-xs mt-2 opacity-75">
                                        Trigger: {msg.trigger}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Current Thoughts */}
                <div>
                    <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">
                        💭 Current Thoughts
                    </h2>
                    {thoughts.length === 0 ? (
                        <div className="text-center py-8 text-slate-500">
                            Opera's mind is quiet. Activate to start thinking.
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {thoughts.map((thought, idx) => (
                                <div
                                    key={idx}
                                    className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700"
                                >
                                    <div className="flex items-center gap-2 mb-2">
                                        <span className="text-xs font-semibold uppercase text-slate-600 dark:text-slate-400">
                                            {thought.type}
                                        </span>
                                        <span className="text-xs text-slate-500">
                                            Priority: {thought.priority}/10
                                        </span>
                                    </div>
                                    <p className="text-slate-900 dark:text-slate-100">{thought.content}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
