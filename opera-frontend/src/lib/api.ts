// API client for Opera backend

const API_BASE = '/api';

export interface Memory {
    id: number;
    type: string;
    content: string;
    source: string;
    timestamp: string;
    confidence: number;
}

export interface Intent {
    category: string;
    description: string;
    confidence: number;
    parameters?: Record<string, any>;
}

export interface PlanStep {
    step_id: number;
    description: string;
    tool_name?: string;
    tool_arguments?: Record<string, any>;
}

export interface Plan {
    plan_id: string;
    steps: PlanStep[];
    estimated_duration_seconds?: number;
}

export const api = {
    // Memory operations
    async getMemories(type?: string): Promise<Memory[]> {
        const url = type ? `${API_BASE}/memory?memory_type=${type}` : `${API_BASE}/memory`;
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to fetch memories');
        return res.json();
    },

    async createMemory(memory: Omit<Memory, 'id' | 'timestamp'>): Promise<Memory> {
        const res = await fetch(`${API_BASE}/memory`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(memory),
        });
        if (!res.ok) throw new Error('Failed to create memory');
        return res.json();
    },

    // Reasoning operations
    async deriveIntent(userInput: string): Promise<Intent> {
        const res = await fetch(`${API_BASE}/intent/derive`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_input: userInput }),
        });
        if (!res.ok) throw new Error('Failed to derive intent');
        return res.json();
    },

    async generatePlan(intent: Intent): Promise<Plan> {
        const res = await fetch(`${API_BASE}/plan/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ intent }),
        });
        if (!res.ok) throw new Error('Failed to generate plan');
        return res.json();
    },

    // Search operations
    async searchMemories(query: string, limit = 10) {
        const res = await fetch(`${API_BASE}/search/semantic`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, limit }),
        });
        if (!res.ok) throw new Error('Failed to search memories');
        return res.json();
    },
};
