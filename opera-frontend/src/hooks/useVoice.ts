// Voice control hook for Opera

import { useState, useEffect, useRef } from 'react';

interface VoiceConfig {
    enabled: boolean;
    voice: string;
    speed: number;
    autoSpeak: boolean;
}

export function useVoice() {
    const [isListening, setIsListening] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [config, setConfig] = useState<VoiceConfig>({
        enabled: false,
        voice: 'alloy',
        speed: 1.0,
        autoSpeak: false
    });

    const recognitionRef = useRef<any>(null);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    // Initialize speech recognition
    useEffect(() => {
        if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
            const recognition = new (window as any).webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onresult = (event: any) => {
                const transcript = event.results[event.results.length - 1][0].transcript;

                // Trigger callback
                if (recognitionRef.current?.onTranscript) {
                    recognitionRef.current.onTranscript(transcript);
                }
            };

            recognition.onerror = (event: any) => {
                console.error('Speech recognition error:', event.error);
                setIsListening(false);
            };

            recognition.onend = () => {
                setIsListening(false);
            };

            recognitionRef.current = recognition;
        }
    }, []);

    const startListening = (onTranscript: (text: string) => void) => {
        if (recognitionRef.current) {
            recognitionRef.current.onTranscript = onTranscript;
            recognitionRef.current.start();
            setIsListening(true);
        }
    };

    const stopListening = () => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
            setIsListening(false);
        }
    };

    const speak = async (text: string) => {
        if (!config.enabled) return;

        setIsSpeaking(true);

        try {
            const res = await fetch('/api/voice/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text,
                    voice: config.voice,
                    speed: config.speed
                })
            });

            if (!res.ok) throw new Error('TTS failed');

            const blob = await res.blob();
            const audioUrl = URL.createObjectURL(blob);

            const audio = new Audio(audioUrl);
            audioRef.current = audio;

            audio.onended = () => {
                setIsSpeaking(false);
                URL.revokeObjectURL(audioUrl);
            };

            await audio.play();
        } catch (error) {
            console.error('Speech failed:', error);
            setIsSpeaking(false);
        }
    };

    const stopSpeaking = () => {
        if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
            setIsSpeaking(false);
        }
    };

    return {
        isListening,
        isSpeaking,
        config,
        setConfig,
        startListening,
        stopListening,
        speak,
        stopSpeaking
    };
}
