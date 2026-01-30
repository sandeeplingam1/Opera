'use client';

import { useVoice } from '@/hooks/useVoice';
import { useState } from 'react';

export default function VoiceControls() {
    const { isListening, isSpeaking, config, setConfig, startListening, stopListening, speak, stopSpeaking } = useVoice();
    const [testText, setTestText] = useState("Hello! I'm Opera, your personal intelligence assistant.");

    const handleVoiceInput = (transcript: string) => {
        console.log('Voice input:', transcript);
        // TODO: Send to chat interface
    };

    const toggleListening = () => {
        if (isListening) {
            stopListening();
        } else {
            startListening(handleVoiceInput);
        }
    };

    return (
        <div className="p-6 bg-white dark:bg-slate-800 rounded-xl shadow-lg space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
                    🎙️ Voice Controls
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                    Talk to Opera and hear it speak
                </p>
            </div>

            {/* Voice Enable Toggle */}
            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
                <div>
                    <div className="font-medium text-slate-900 dark:text-white">Voice Enabled</div>
                    <div className="text-sm text-slate-600 dark:text-slate-400">Turn on voice features</div>
                </div>
                <button
                    onClick={() => setConfig({ ...config, enabled: !config.enabled })}
                    className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${config.enabled ? 'bg-blue-600' : 'bg-slate-300'
                        }`}
                >
                    <span
                        className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${config.enabled ? 'translate-x-7' : 'translate-x-1'
                            }`}
                    />
                </button>
            </div>

            {/* Voice Selection */}
            <div>
                <label className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
                    Voice Character
                </label>
                <select
                    value={config.voice}
                    onChange={(e) => setConfig({ ...config, voice: e.target.value })}
                    className="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={!config.enabled}
                >
                    <option value="alloy">Alloy (Neutral)</option>
                    <option value="echo">Echo (Male)</option>
                    <option value="fable">Fable (British)</option>
                    <option value="onyx">Onyx (Deep)</option>
                    <option value="nova">Nova (Friendly)</option>
                    <option value="shimmer">Shimmer (Warm)</option>
                </select>
            </div>

            {/* Speed Control */}
            <div>
                <label className="block text-sm font-medium text-slate-900 dark:text-white mb-2">
                    Speaking Speed: {config.speed}x
                </label>
                <input
                    type="range"
                    min="0.5"
                    max="2"
                    step="0.1"
                    value={config.speed}
                    onChange={(e) => setConfig({ ...config, speed: parseFloat(e.target.value) })}
                    className="w-full"
                    disabled={!config.enabled}
                />
            </div>

            {/* Test TTS */}
            <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-900 dark:text-white">
                    Test Opera's Voice
                </label>
                <textarea
                    value={testText}
                    onChange={(e) => setTestText(e.target.value)}
                    className="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    disabled={!config.enabled}
                />
                <button
                    onClick={() => speak(testText)}
                    disabled={!config.enabled || isSpeaking}
                    className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white rounded-lg font-medium transition-colors"
                >
                    {isSpeaking ? '🔊 Speaking...' : '🔊 Test Voice'}
                </button>
            </div>

            {/* Voice Input */}
            <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-900 dark:text-white">
                    Voice Input
                </label>
                <button
                    onClick={toggleListening}
                    disabled={!config.enabled}
                    className={`w-full px-4 py-3 rounded-lg font-medium transition-colors ${isListening
                            ? 'bg-red-600 hover:bg-red-700 text-white animate-pulse'
                            : 'bg-green-600 hover:bg-green-700 text-white'
                        } disabled:bg-slate-300`}
                >
                    {isListening ? '🎤 Listening... (Click to stop)' : '🎤 Start Voice Input'}
                </button>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                    Click and speak to Opera. Your speech will be transcribed in real-time.
                </p>
            </div>

            {/* Auto-speak toggle */}
            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700 rounded-lg">
                <div>
                    <div className="font-medium text-slate-900 dark:text-white">Auto-speak Responses</div>
                    <div className="text-sm text-slate-600 dark:text-slate-400">Opera speaks all responses</div>
                </div>
                <button
                    onClick={() => setConfig({ ...config, autoSpeak: !config.autoSpeak })}
                    disabled={!config.enabled}
                    className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${config.autoSpeak ? 'bg-blue-600' : 'bg-slate-300'
                        }`}
                >
                    <span
                        className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${config.autoSpeak ? 'translate-x-7' : 'translate-x-1'
                            }`}
                    />
                </button>
            </div>

            {/* Status Indicators */}
            <div className="grid grid-cols-2 gap-4">
                <div className={`p-3 rounded-lg text-center ${isListening ? 'bg-green-100 dark:bg-green-900/30' : 'bg-slate-100 dark:bg-slate-700'}`}>
                    <div className="text-2xl">{isListening ? '🎤' : '🔇'}</div>
                    <div className="text-sm font-medium text-slate-900 dark:text-white">
                        {isListening ? 'Listening' : 'Not Listening'}
                    </div>
                </div>
                <div className={`p-3 rounded-lg text-center ${isSpeaking ? 'bg-blue-100 dark:bg-blue-900/30' : 'bg-slate-100 dark:bg-slate-700'}`}>
                    <div className="text-2xl">{isSpeaking ? '🔊' : '🔇'}</div>
                    <div className="text-sm font-medium text-slate-900 dark:text-white">
                        {isSpeaking ? 'Speaking' : 'Silent'}
                    </div>
                </div>
            </div>
        </div>
    );
}
