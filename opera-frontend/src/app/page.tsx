'use client';

import { useState } from 'react';
import ChatInterface from '@/components/ChatInterface';
import MemoryBrowser from '@/components/MemoryBrowser';
import InsightsPanel from '@/components/InsightsPanel';
import AutonomousPanel from '@/components/AutonomousPanel';
import VoiceControls from '@/components/VoiceControls';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'memories' | 'insights' | 'mind' | 'voice'>('chat');

  return (
    <div className="h-screen flex flex-col bg-slate-900">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Opera</h1>
            <p className="text-sm text-blue-100">Personal Intelligence OS</p>
          </div>

          {/* Navigation */}
          <nav className="flex gap-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'chat'
                ? 'bg-white text-blue-600'
                : 'bg-blue-700/50 hover:bg-blue-700 text-white'
                }`}
            >
              Chat
            </button>
            <button
              onClick={() => setActiveTab('memories')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'memories'
                ? 'bg-white text-blue-600'
                : 'bg-blue-700/50 hover:bg-blue-700 text-white'
                }`}
            >
              Memories
            </button>
            <button
              onClick={() => setActiveTab('insights')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'insights'
                ? 'bg-white text-blue-600'
                : 'bg-blue-700/50 hover:bg-blue-700 text-white'
                }`}
            >
              💡 Insights
            </button>
            <button
              onClick={() => setActiveTab('mind')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'mind'
                ? 'bg-white text-blue-600'
                : 'bg-blue-700/50 hover:bg-blue-700 text-white'
                }`}
            >
              🤖 Mind
            </button>
            <button
              onClick={() => setActiveTab('voice')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'voice'
                  ? 'bg-white text-blue-600'
                  : 'bg-blue-700/50 hover:bg-blue-700 text-white'
                }`}
            >
              🎙️ Voice
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'memories' && <MemoryBrowser />}
        {activeTab === 'insights' && <InsightsPanel />}
        {activeTab === 'mind' && <AutonomousPanel />}
        {activeTab === 'voice' && (
          <div className="h-full overflow-y-auto p-6 bg-slate-50 dark:bg-slate-900">
            <div className="max-w-2xl mx-auto">
              <VoiceControls />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 text-slate-400 text-center text-sm py-3 border-t border-slate-700">
        Opera - Personal Intelligence Operating System
      </footer>
    </div>
  );
}
